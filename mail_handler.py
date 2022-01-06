"""
Mail Handler


"""

import re
import msal, sys, requests, json, message_temp, time



class MailHandler:
    """
        Mail Handler class, this class is used to automate an outlook email account,
        and it's expected to run for weeks.
        This class handles internal email routing logics, interacting with Database class.
    """
    def __init__(self):
        """Load and store API configuration parameters"""
        with open("configuration.json") as conf:
            self.config_ = json.load(conf)
        self.client_id_ = self.config_['client_id'] 
        self.tenant_id_ = self.config_['tenant_id'] 
        self.scopes_ = self.config_['scope']
        self.access_token_ = None
        
    def login_test(self):
        self.access_token_ = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IjFBejdrSFBmR2hsVHFKVldYVmxLSGFKMjB2SGZtdXp0anQxOFdDMXAzRDgiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCIsImtpZCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEvIiwiaWF0IjoxNjQxNTAzMjExLCJuYmYiOjE2NDE1MDMyMTEsImV4cCI6MTY0MTUwNzMzNiwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFTUUEyLzhUQUFBQVpxWDZWSmlFTEk1cjI0UGFqNTBkUDhJZTBGSGJ0YkZLMHFPaEprZmM5Zms9IiwiYW1yIjpbInB3ZCJdLCJhcHBfZGlzcGxheW5hbWUiOiJib3QiLCJhcHBpZCI6ImRkODliYjk0LTA3ZjQtNGU1ZC1iNjQxLTEyNWZjOTZiZmRlZSIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiR29uZyIsImdpdmVuX25hbWUiOiJDaGFuZ3hpbmciLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxNTEuMjEwLjE2OS43MyIsIm5hbWUiOiJDaGFuZ3hpbmcgR29uZyIsIm9pZCI6IjQ3MmRmMjBlLTk2ZjUtNDdhYS04YjM5LWI5Y2VlYzBkYTgwOSIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS05NjYyMDQxNDMtNzQ2OTMyNjkwLTExNTM5NDYyLTI4MTcyMyIsInBsYXRmIjoiMTQiLCJwdWlkIjoiMTAwMzAwMDBBRTRDRkY4RSIsInJoIjoiMC5BVUVBSnhkNDNBNXhWVWk4VEdrQ1pxRzFVWlM3aWQzMEIxMU90a0VTWDhscl9lNUJBRGsuIiwic2NwIjoiSU1BUC5BY2Nlc3NBc1VzZXIuQWxsIE1haWwuUmVhZCBNYWlsLlJlYWRCYXNpYyBNYWlsLlJlYWRXcml0ZSBNYWlsLlNlbmQgb3BlbmlkIHByb2ZpbGUgVXNlci5SZWFkIFVzZXIuUmVhZEJhc2ljLkFsbCBVc2VyLlJlYWRXcml0ZSBlbWFpbCIsInNpZ25pbl9zdGF0ZSI6WyJrbXNpIl0sInN1YiI6IkJrZm91OVU4d21nOElvdmRveUpTRjM3Zl83c3ZaZTVtWjZ2LUJ3MzdiNmMiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiT0MiLCJ0aWQiOiJkYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEiLCJ1bmlxdWVfbmFtZSI6ImNnbzU0QHVjbGl2ZS5hYy5ueiIsInVwbiI6ImNnbzU0QHVjbGl2ZS5hYy5ueiIsInV0aSI6IjZ2WHJfWlQtREUyVWN0bkxmMno4QUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfc3QiOnsic3ViIjoienZVa1UxT2g5LVFxUXBnUTRhejFWZjgwMFVOazVDS2p6UGg5RTZGX0JwMCJ9LCJ4bXNfdGNkdCI6MTM2NjkxMDA5MH0.LmQ0hT22N-sEsieFdczhd1X98vfpojnH2-dCTlg-zsnh6Wwpd53KzT6Mv2-tPvF5A3Yd5tZ03bG-TvbjKtSzaTvn1DAkyer6IWA3hTYhbAFNTxATkrQhLK6B1UVKBUgRGLzMe_CcLlHgSrCsD93upUXrm1eK1wzK59w2pkxcXWWvjw0VWPsnwz0QwkYbaGH4aRqRVbstGPttWb5dfbw0jwCDBDavIhkmaVLmmmfHkbFHWdPlxD6t30eSq-jgvaY4QlFpwilsmunqF1Hu3zgx34UfnlNRmN-W6tEOE2SRrpuL0Khpi3Zrl8zJ1Ss4HBT88aMK1DuxqCdzzTuFxl0wSA"
        self.auth_header_ = {'Authorization': 'Bearer ' + self.access_token_}


    def login(self):
        """
            Refresh token if there is a cached token.
            Otherwise, a new device flow is initiated
            An url and an authentication code will be displayed upon initiation 
        """
        result = None
        # Note: If your device-flow app does not have any interactive ability, you can
        #   completely skip the following cache part. But here we demonstrate it anyway.
        # We now check the cache to see if we have some end users signed in before.
        sys.stdout.flush()
        self.app = msal.PublicClientApplication(self.client_id_, authority=self.tenant_id_)
        accounts = self.app.get_accounts()
        print(accounts)
        if accounts:
            print("Pick the account you want to use to proceed:")
            for a in accounts:
                print(a["username"])
            # Assuming the end user chose this one
            chosen = accounts[0]
            # Now let's try to find a token in cache for this account
            result = self.app.acquire_token_silent(self.scopes_, account=chosen)
        if not result:
            flow = self.app.initiate_device_flow(scopes=self.scopes_)
            print(flow["message"])
            sys.stdout.flush()
            result = self.app.acquire_token_by_device_flow(flow)
            print(result['access_token'])
        if "access_token" in result:
            print(result['access_token'])
            self.access_token_ = result['access_token']
            self.auth_header_ = {'Authorization': 'Bearer ' + result['access_token']}
        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))

    def refresh_token(self):
        accounts = self.app.get_accounts()
        result = self.app.acquire_token_silent(self.scopes_, account=accounts[0])
        self.access_token_ = result['access_token']
        self.auth_header_ = {'Authorization': 'Bearer ' + result['access_token']}

    def check_inbox(self):
        """Return a list of unread mails in dict format from inbox"""
        self.refresh_token()
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
            Provided:
                mails: a list of mails in dict format

        """
        for mail in mails:
            msg_id, convo_id, subject, from_, date = self.parser_.parse_mail(mail)
            if not self.db_.is_subscriber(from_):
                continue #ignore non-subscriber
            self.mark_as_read(msg_id)
            if self.parser_.is_subm(subject):
                if self.db_.store_subm(convo_id, from_, \
                                          self.parser_.get_subm_id(subject), date):
                    self.reply_subm(msg_id, mail, True)
                else:
                    self.reply_subm(msg_id, mail, False)
                #test----------draw reviewers-------------
                reviewer = 'changxing.gong@gmail.com'
                #-----------------------------------------
                new_conv_id, date_sent = self.send_req(self.parser_.get_review_req(), \
                                                        mail, reviewer)
                self.db_.store_review_req(convo_id, new_conv_id, reviewer, date_sent)
            elif self.parser_.is_review(subject):
                if self.db_.store_review(convo_id, date):
                    author = self.db_.find_author_by_convo_id(convo_id)
                    new_conv_id, date_sent = self.send_req(self.parser_.get_eval_req(), \
                                                            mail, author)
                    self.db_.store_eval_req(convo_id, new_conv_id, date_sent)
            elif self.parser_.is_eval(subject):
                rating, comment = self.parser_.get_eval(mail)
                self.db_.store_eval(convo_id, rating, comment, date)
            else: # subscriber but invalid subject
                # self.send_usage_instruction()
                print(subject)

    def mark_as_read(self, msg_id):
        """
            Provided:
                msg_id: a string of message id
        """
        data = {'isRead' : 'true'}
        response = requests.patch(self.config_['msg'].format(msg_id), json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        print(response.status_code)
        # print(response.json())
        if 'error' in response:
            print(response)
            print('Error: mark_as_read')
            exit(1)

    def reply_subm(self, msg_id, mail, is_subm_success):
        """
            Provided:
                msg_id: a string of message id
                mail: an email in dict format
                is_success: True if the submission is successful
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

    def send_req(self, subject, mail, dest):
        """
            Provided:
                subject: a string of mail subject
                mail: an email in dict format
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
        response = requests.post(self.config_['send_mail'], json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        print(response)
        if 'error' in response:
            print(response)
            print('Error: send_req')
            exit(1)
        time.sleep(2)
        convo_id, sent_date = self.get_last_convo()
        return convo_id, sent_date

    def get_last_convo(self):
        """
            Return:
                Conversation id of the last sent message
                Sent date of the last sent message
        """
        response = requests.get(self.config_['last_sent_msg'], \
                    headers=self.auth_header_).json()
        convo_id = response['value'][0]['conversationId']  # only one message in list
        print('get_req_convo', convo_id)
        sent_date = response['value'][0]['sentDateTime']
        return convo_id, sent_date

    def send_usage_instruction(self):
        """
            Provided:

        """
        raise NotImplementedError


    def get_attachments(self, msg_id):
        """
            Provided:
                msg_id: a string of message id
            Return:
                A list of attachments
        """
        response = requests.get(self.config_['get_attachments'].format(msg_id), \
                    headers=self.auth_header_).json()
        if 'error' in response:
            print(response)
            print('Error: get_attachments')
            exit(1)
        return response['value']