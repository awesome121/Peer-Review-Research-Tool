"""
    API permission and calls can be found in configuration.json.
    Message templates prepended into email can be found in message_temp module.
    Database object is used to interact with database.db file.
    MailHandler parses email subject with the aid of MailParser.

    About authentication process, please refer Microsoft Authentication 
    Lbrary (MSAL) https://msal-python.readthedocs.io/en/latest/ 
    for more details.

    About HTTP requests, please refer https://docs.python-requests.org/en/latest/
    for more details

    This module is imported by main.py, App object normally uses only one 
    MailHandler object, when distributing, another MailHandler object created.
"""

import requests, json, message_temp, time
from database import Database
from mail_parser import MailParser

SLEEP_INTERVAL = 0.2 # checking inbox, in minutes

#=====messagee template constants=======
NON_EXISTING_SUBM = 0
NON_STARTING_SUBM = 1
LATE_SUBM = 2
LATE_REVIEW = 3
LATE_EVAL = 4
INVALID_SUBJECT = 5
#=======================================


class MailHandler:
    """
        Mail Handler class, this class is used to automate an outlook email account,
        and it's expected to run for weeks.
        This class handles internal email routing logics, interacting with Database class.
    """
    def __init__(self, app, auth_header):
        """Load and store API configuration parameters"""
        self.app = app
        self.auth_header_ = auth_header
        with open("configuration.json") as conf:
            self.config_ = json.load(conf)
        self.db = Database()
        self.parser = MailParser()
    
    def listen(self):
        """
            An infinite loop for listening incoming messages,
                it checks for inbox, retrieve certain number
                of unread emails, and further process them.
            Sleeping for 5 minites if the inbox is empty 
        """
        while self.app.get_conn_status():
            # try:
            unread_mails = self.check_inbox()
            if len(unread_mails) != 0:
                self.process_unread(unread_mails)
            else:
                time.sleep(60 * SLEEP_INTERVAL) # sleep for SLEEP_INTERVAL minutes
            # except:
            #     self.app.disconnect()
            #     print('connection lost')
            #     break


    def check_inbox(self):
        """
            Checks user's Inbox, return a list of unread messages.
            The number of messages to retrieve at a time can be configured
                    in "configuration.json".

            Return: a list of unread mails in dict format from inbox
                    If there is no unread, empty list is returned.
        """
        response = requests.get(self.config_['inbox'], headers=self.auth_header_).json()
        if 'error' in response:
            if 'code' in response['error'] and response['error']['code'] == \
                'InvalidAuthenticationToken':
                print('refresh token')
            else:
                print(response)
                print('Error: check_inbox')
                exit(1)
        else:
            if response['totalItemCount']:
                response = requests.get(self.config_['inbox_unread_msg'],\
                     headers=self.auth_header_).json()
                if 'error' in response:
                    print(response)
                    print('Error: check_inbox, inbox_unread_msg')
                    exit(1)
                return response['value'] # a list of mails
            else:
                return []
                
    def process_unread(self, mails):
        """
            Mark each email as read when processing.
            Parse mail subject with the help of MailParser object.
            Process them according to subjects "submission" "review" "evaluation",
                please see MailParser for details

            If it's from a subscriber but invalid subject, send usage prompt.
            If it's from a non-subscriber, ignore.

            Param:
                mails: a list of mails in dict format
        """
        for mail in mails:
            msg_id, convo_id, subject, from_, date = self.parser.parse_mail(mail)
            if not self.db.is_subscriber(from_):
                continue # ignore non-subscriber
            self.mark_as_read(msg_id)
            if self.parser.is_subm(subject):
                self.process_subm(msg_id, from_, subject, date, mail)
            elif self.parser.is_review(subject):
                self.process_review(subject, convo_id, date, mail)
            elif self.parser.is_eval(subject):
                self.process_eval(subject, convo_id, date, mail)
            else: # subscriber but invalid subject
                self.reply_prompt(INVALID_SUBJECT, mail)
                print(subject)

    def mark_as_read(self, msg_id):
        """
            Mark a message as read in user Inbox.
            Param:
                msg_id: a string of message id
        """
        data = {'isRead' : 'true'}
        response = requests.patch(self.config_['msg'].format(msg_id), json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        if 'error' in response:
            print(response)
            print('Error: mark_as_read')
            exit(1)

    def process_subm(self, msg_id, from_, subject, date, mail):
        subm_id = self.parser.get_subm_id(subject)
        if not self.db.exist_schedule(subm_id):
            print("received non-existing submission")
            self.reply_prompt(NON_EXISTING_SUBM, mail)
            # reply submission not exists
        elif not self.db.is_subm_started(subm_id):
            print("received non-starting submission")
            # reply submission not started
            self.reply_prompt(NON_STARTING_SUBM, mail)
        elif self.db.is_subm_end(subm_id):
            print("received submission after deadline")
            # reply receiving submission after deadline
            self.reply_prompt(LATE_SUBM, mail)
        elif self.db.store_subm(msg_id, from_, \
                                    self.parser.get_subm_id(subject), date):
            self.reply_subm(msg_id, mail, True)
        else:
            self.reply_subm(msg_id, mail, False) # submission exists already

    def process_review(self, subject, convo_id, date, mail):
        subm_id = self.parser.get_subm_id(subject)
        if self.db.is_review_end(subm_id):
            print("received review after deadline")
            self.reply_prompt(LATE_REVIEW, mail)
        elif self.db.store_review(convo_id, date):
            author = self.db.get_author_by_convo_id(convo_id)
            new_conv_id, date_sent = self.send_req(self.parser.get_eval_req(subm_id), \
                                                    mail, author)
            self.db.store_eval_req(convo_id, new_conv_id, date_sent)

    def process_eval(self, subject, convo_id, date, mail):
        subm_id = self.parser.get_subm_id(subject)
        if self.db.is_eval_end(subm_id):
            print("received eval after deadline")
            self.reply_prompt(LATE_EVAL, mail)
        else:
            rating, comment = self.parser.get_eval(mail)
            self.db.store_eval(convo_id, rating, comment, date)

    def reply_subm(self, msg_id, mail, is_subm_success):
        """
            Param:
                msg_id: a string of message id
                mail: an email in dict format
                is_subm_success: True if the submission is successful
                            False other wise
        """
        comment = message_temp.SUBMISSION_SUCCESS if is_subm_success \
                else message_temp.SUBMISSION_FAILURE
        data = {
            "message":{  
                "toRecipients":[ mail['from'] ]
            },
            "comment": comment
        }
        # data is required to dumped into json format, 'Content-Type' header is required
        response = requests.post(self.config_['reply_msg'].format(msg_id), json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        # print(response.status_code)
        # print(response.json())
        if 'error' in response:
            print(response)
            print('Error: reply_subm')
            exit(1)

    def distribute_subm(self, subm_id):
        """
            Distribute submission for a specific submission subm_id
            This function draws authors first, then draw 3 reviewers for the author
            Param:
                subm_id: id of the submission to be distributed
        """
        subms = self.db.get_subms_by_id(subm_id) # draw submissions from submission table matched subm_id
        print(f"---distributing submissions {subms}---")
        for msg_id, author, _, subm_received, _ in subms:
            reviewers = self.db.draw_reviewers(author)
            print(f"draw reviewer {reviewers} for author {author}")
            for reviewer in reviewers:
                mail = self.get_mail_by_msg_id(msg_id)
                review_convo_id, date_sent = self.send_req(self.parser.get_review_req(subm_id), \
                                                        mail, reviewer)
                self.db.store_review_req(msg_id, author, subm_id, subm_received, review_convo_id,\
                                         reviewer, date_sent)
                if not self.app.get_conn_status():
                    print("connection lost, distributor terminates")
                    return

    def get_mail_by_msg_id(self, msg_id):
        """
            Param:
                msg_id: a string of message id
            Return:
                an email object in dict form
        """
        response = requests.get(self.config_['msg'].format(msg_id), \
                                headers=self.auth_header_).json()
        return response

    def send_req(self, subject, mail, dest):
        """
            Param:
                subject: a string of mail subject
                mail: a mail in dict format to be parsed
                dest: a string of email address
            Return: 
                conversation id: newly generated conversation id
                date sent: the date on sending this request
        """
        content = mail['body']['content']
        prompt = message_temp.REVIEW_REQUEST_PROMPT if self.parser.is_review(subject) \
                    else message_temp.EVAL_REQUEST_PROMPT
        data = {
            "message": {
                "subject": subject,
                "hasAttachments" : mail['hasAttachments'],
                "body": {
                "contentType": "html",
                "content": f"{prompt+content}"
                },
                "toRecipients": [{
                    "emailAddress": {
                    "address": f"{dest}"
                    }
                }],
            },
        }
        if mail['hasAttachments']:
            data['message']['attachments'] = self.get_attachments(mail['id'])
        response = requests.post(self.config_['send_mail'], json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        if 'error' in response:
            print(response)
            print('Error: send_req')
            exit(1)
        # wait for some time until the message is really sent
        time.sleep(5)
        convo_id, sent_date = self.get_last_sent_convo()
        return convo_id, sent_date

    def get_last_sent_convo(self):
        """
            Get conversation id and sent date of the last sent message
            Return:
                Conversation id of the last sent message
                Sent date of the last sent message
        """
        response = requests.get(self.config_['last_sent_msg'], \
                    headers=self.auth_header_).json()
        convo_id = response['value'][0]['conversationId']  # only one message in list
        sent_date = response['value'][0]['sentDateTime']
        return convo_id, sent_date

    def reply_prompt(self, typ, mail):
        """
            Send the prompt message to addr
            Param:
                typ: an integer, global constant
                mail: incoming mail
        """
        if typ == INVALID_SUBJECT:
            comment = message_temp.INVALID_SUBJECT
        elif typ == NON_EXISTING_SUBM:
            comment = message_temp.NON_EXISTING_SUBM
        elif typ == NON_STARTING_SUBM:
            comment = message_temp.NON_STARTING_SUBM
        elif typ == LATE_SUBM:
            comment = message_temp.USALATE_SUBMGE_PROMPT
        elif typ == LATE_REVIEW:
            comment = message_temp.LATE_REVIEW
        elif typ == LATE_EVAL:
            comment = message_temp.LATE_EVAL
        data = {
            "message":{  
                "toRecipients":[ mail['from'] ]
            },
            "comment": comment
        }
        # data is required to dumped into json format, 'Content-Type' header is required
        response = requests.post(self.config_['reply_msg'].format(mail['id']), json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        if 'error' in response:
            print(response)
            print(f'Error: reply_prompt, typ {typ}')
            exit(1)

    def get_attachments(self, msg_id):
        """
            Param:
                msg_id: a string of message id
            Return:
                A list of attachments given for a specific message
        """
        response = requests.get(self.config_['get_attachments'].format(msg_id), \
                    headers=self.auth_header_).json()
        if 'error' in response:
            print(response)
            print('Error: get_attachments')
            exit(1)
        return response['value']