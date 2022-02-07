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
        self.db_ = Database()
        self.parser_ = MailParser()
    
    def listen(self):
        """
            An infinite loop for listening incoming messages,
                it checks for inbox, retrieve certain number
                of unread emails, and further process them.
            Sleeping for 5 minites if the inbox is empty 
        """
        while self.app.get_conn_status():
            mails = self.check_inbox()
            if len(mails) != 0:
                self.process_unread(mails)
            else:
                time.sleep(60 * 5) # sleep for 5 mins

    def login_test(self):
        """===Only used for testing==="""
        self.access_token_ = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IlhnSW9VQ1BwN0dGcDVnU2huUE1NOUZraWlGUFFKY3dwX2RzZVBRLTl1VlkiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCIsImtpZCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEvIiwiaWF0IjoxNjQxNTA3MDc5LCJuYmYiOjE2NDE1MDcwNzksImV4cCI6MTY0MTUxMTE1NCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFTUUEyLzhUQUFBQTFvZTV0OUUramVVbFNMK25VTHBHNlV0WW5lc05BN2N1NFg5dktxQTE5dzA9IiwiYW1yIjpbInB3ZCJdLCJhcHBfZGlzcGxheW5hbWUiOiJib3QiLCJhcHBpZCI6ImRkODliYjk0LTA3ZjQtNGU1ZC1iNjQxLTEyNWZjOTZiZmRlZSIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiR29uZyIsImdpdmVuX25hbWUiOiJDaGFuZ3hpbmciLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxNTEuMjEwLjE2OS43MyIsIm5hbWUiOiJDaGFuZ3hpbmcgR29uZyIsIm9pZCI6IjQ3MmRmMjBlLTk2ZjUtNDdhYS04YjM5LWI5Y2VlYzBkYTgwOSIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS05NjYyMDQxNDMtNzQ2OTMyNjkwLTExNTM5NDYyLTI4MTcyMyIsInBsYXRmIjoiMTQiLCJwdWlkIjoiMTAwMzAwMDBBRTRDRkY4RSIsInJoIjoiMC5BVUVBSnhkNDNBNXhWVWk4VEdrQ1pxRzFVWlM3aWQzMEIxMU90a0VTWDhscl9lNUJBRGsuIiwic2NwIjoiSU1BUC5BY2Nlc3NBc1VzZXIuQWxsIE1haWwuUmVhZCBNYWlsLlJlYWRCYXNpYyBNYWlsLlJlYWRXcml0ZSBNYWlsLlNlbmQgb3BlbmlkIHByb2ZpbGUgVXNlci5SZWFkIFVzZXIuUmVhZEJhc2ljLkFsbCBVc2VyLlJlYWRXcml0ZSBlbWFpbCIsInNpZ25pbl9zdGF0ZSI6WyJrbXNpIl0sInN1YiI6IkJrZm91OVU4d21nOElvdmRveUpTRjM3Zl83c3ZaZTVtWjZ2LUJ3MzdiNmMiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiT0MiLCJ0aWQiOiJkYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEiLCJ1bmlxdWVfbmFtZSI6ImNnbzU0QHVjbGl2ZS5hYy5ueiIsInVwbiI6ImNnbzU0QHVjbGl2ZS5hYy5ueiIsInV0aSI6IjFzLUhkc21BWmtTQXF3OXpOQ1BUQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfc3QiOnsic3ViIjoienZVa1UxT2g5LVFxUXBnUTRhejFWZjgwMFVOazVDS2p6UGg5RTZGX0JwMCJ9LCJ4bXNfdGNkdCI6MTM2NjkxMDA5MH0.DiQTLl71kYA1nstIy_ANK5oT-b1iiiqACZKp1ZHOAMoEFpKAEtw5v_r2y1rvWBh1i1_SxffjjVlecKEpi1mC91IMSPhKRHvOrOugxZolE4o8LDyTSDdKuix7VysR7gMYIL7R6OfeL8H4uEtiG-gE1SXJ9pO5VSrMmEJh7zWiWuZPuLQwFLgtmuDfRUpSuzFmW9Z8E7wocA9ZIryR0iBxMscZOdKNK98ueAiAvBG37wmKUJTXBko0NaJ7PwacmHu3Hxb0UOe9gWxQFwTk52bFcvtrkYp17QyacVXKd-ycsB6Ru9WKIJiZohVp5MYI87q8RImTnPgl48uZT9T5HqWqaQ"
        self.auth_header_ = {'Authorization': 'Bearer ' + self.access_token_}

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

            Provided:
                mails: a list of mails in dict format
        """
        for mail in mails:
            msg_id, convo_id, subject, from_, date = self.parser_.parse_mail(mail)
            if not self.db_.is_subscriber(from_):
                continue #ignore non-subscriber
            self.mark_as_read(msg_id)
            if self.parser_.is_subm(subject):
                if self.db_.store_subm(msg_id, from_, \
                                          self.parser_.get_subm_id(subject), date):
                    self.reply_subm(msg_id, mail, True)
                else:
                    self.reply_subm(msg_id, mail, False)
                
            elif self.parser_.is_review(subject):
                if self.db_.store_review(convo_id, date):
                    author = self.db_.get_author_by_convo_id(convo_id)
                    new_conv_id, date_sent = self.send_req(self.parser_.get_eval_req(), \
                                                            mail, author)
                    self.db_.store_eval_req(convo_id, new_conv_id, date_sent)
            elif self.parser_.is_eval(subject):
                rating, comment = self.parser_.get_eval(mail)
                self.db_.store_eval(convo_id, rating, comment, date)
            else: # subscriber but invalid subject
                self.reply_usage_prompt(msg_id, mail)
                print(subject)

    def mark_as_read(self, msg_id):
        """
            Mark a message as read in user Inbox.
            Provided:
                msg_id: a string of message id
        """
        data = {'isRead' : 'true'}
        response = requests.patch(self.config_['msg'].format(msg_id), json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        if 'error' in response:
            print(response)
            print('Error: mark_as_read')
            exit(1)

    def reply_subm(self, msg_id, mail, is_subm_success):
        """
            Provided:
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
        response = requests.post(self.config_['reply_subm'].format(msg_id), json.dumps(data), \
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
            Provided:
                subm_id: id of the submission to be distributed
        """
        authors = self.db_.draw_authors(subm_id)
        for author, msg_id in authors:
            reviewers = self.db_.draw_reviewers(author)
            for reviewer in reviewers:
                mail = self.get_mail_by_msg_id(msg_id)
                new_conv_id, date_sent = self.send_req(self.parser_.get_review_req(), \
                                                        mail, reviewer)
                self.db_.store_review_req(msg_id, new_conv_id, reviewer, date_sent)
                if not self.app.get_conn_status():
                    return

    def get_mail_by_msg_id(self, msg_id):
        """
            Provided:
                convo_id: a string of conversation id
            Return:
                an email object in dict form
        """
        response = requests.get(self.config_['msg'].format(msg_id), \
                                headers=self.auth_header_).json()
        return response['value'][0] # only 1 mail in the whole list

    def send_req(self, subject, mail, dest):
        """
            Provided:
                subject: a string of mail subject
                mail: a mail in dict format to be parsed
                dest: a string of email address
            Return: 
                conversation id: newly generated conversation id
                date sent: the date on sending this request
        """
        content = mail['body']['content']
        prompt = message_temp.REVIEW_REQUEST_PROMPT if subject.lower() == 'review-request' \
                    else message_temp.EVAL_REQUEST_PROMPT
        data = {
            "message": {
                "subject": subject,
                "body": {
                "contentType": "HTML",
                "content": f"{prompt + content}"
                },
                "toRecipients": [{
                    "emailAddress": {
                    "address": f"{dest}"
                    }
                }],
            }
        }
        if mail['hasAttachments']:
            data['attachments'] = self.get_attachments(mail['id'])
        response = requests.post(self.config_['create_draft'], json.dumps(data), \
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

    def reply_usage_prompt(self, msg_id, mail):
        """
            Send the prompt message to addr
            Provided:
                addr: An email address
        """
        comment = message_temp.USAGE_PROMPT
        data = {
            "message":{  
                "toRecipients":[ mail['from'] ]
            },
            "comment": comment
        }
        # data is required to dumped into json format, 'Content-Type' header is required
        response = requests.post(self.config_['reply_subm'].format(msg_id), json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        if 'error' in response:
            print(response)
            print('Error: reply_usage_prompt')
            exit(1)

    def get_attachments(self, msg_id):
        """
            Provided:
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