"""
Mail Handler


"""

import re
import msal, sys, requests, json, message_temp, time



class MailHandler:
    def __init__(self):
        with open("configuration.json") as conf:
            self.config_ = json.load(conf)
        self.client_id_ = self.config_['client_id'] 
        self.tenant_id_ = self.config_['tenant_id'] 
        self.scopes_ = self.config_['scope']
        self.access_token_ = None
        
    def login_test(self):
        self.access_token_ = "eyJ0eXAiOiJKV1QiLCJub25jZSI6InhHLXZsV29GT2xianQ5RmVHWXE1aWhvU0NMeEx1c1dUNG5vdzJqYkpCa28iLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCIsImtpZCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEvIiwiaWF0IjoxNjQxMzQ4NTczLCJuYmYiOjE2NDEzNDg1NzMsImV4cCI6MTY0MTM1MzM0OSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFTUUEyLzhUQUFBQU1vaG1JVkhpdGwyS0Q3MmN1WHBUNm5naXlMQ2UrL3pwVndZQTFwZVA0NEU9IiwiYW1yIjpbInB3ZCJdLCJhcHBfZGlzcGxheW5hbWUiOiJib3QiLCJhcHBpZCI6ImRkODliYjk0LTA3ZjQtNGU1ZC1iNjQxLTEyNWZjOTZiZmRlZSIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiR29uZyIsImdpdmVuX25hbWUiOiJDaGFuZ3hpbmciLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxNTEuMjEwLjE3MS4xMDMiLCJuYW1lIjoiQ2hhbmd4aW5nIEdvbmciLCJvaWQiOiI0NzJkZjIwZS05NmY1LTQ3YWEtOGIzOS1iOWNlZWMwZGE4MDkiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtOTY2MjA0MTQzLTc0NjkzMjY5MC0xMTUzOTQ2Mi0yODE3MjMiLCJwbGF0ZiI6IjE0IiwicHVpZCI6IjEwMDMwMDAwQUU0Q0ZGOEUiLCJyaCI6IjAuQVVFQUp4ZDQzQTV4VlVpOFRHa0NacUcxVVpTN2lkMzBCMTFPdGtFU1g4bHJfZTVCQURrLiIsInNjcCI6IklNQVAuQWNjZXNzQXNVc2VyLkFsbCBNYWlsLlJlYWQgTWFpbC5SZWFkQmFzaWMgTWFpbC5SZWFkV3JpdGUgTWFpbC5TZW5kIG9wZW5pZCBwcm9maWxlIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgVXNlci5SZWFkV3JpdGUgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJCa2ZvdTlVOHdtZzhJb3Zkb3lKU0YzN2ZfN3N2WmU1bVo2di1CdzM3YjZjIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6Ik9DIiwidGlkIjoiZGM3ODE3MjctNzEwZS00ODU1LWJjNGMtNjkwMjY2YTFiNTUxIiwidW5pcXVlX25hbWUiOiJjZ281NEB1Y2xpdmUuYWMubnoiLCJ1cG4iOiJjZ281NEB1Y2xpdmUuYWMubnoiLCJ1dGkiOiItZ1R5dzlDSHNVV29VNHdoNTh5NkFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX3N0Ijp7InN1YiI6Inp2VWtVMU9oOS1RcVFwZ1E0YXoxVmY4MDBVTms1Q0tqelBoOUU2Rl9CcDAifSwieG1zX3RjZHQiOjEzNjY5MTAwOTB9.eFyIwvp4mDLJVhFI46FGKQMVG1zYRmMCLDjgt7OjKtWL2rf3396Pjfth13v8cT6A2MY8eAF5k9QZV3XAd9rx1rO9lc4mzIm08OxS0ce_-ii69bQr0jBMvYAIytfg2Rmdi9m2UiaTKU9afPRL2U8oUBa9tpP6AeqXgFnli8fDlPkmBZbxaISFzmOwe9HLFcIkZW8OAD1vmbx93I2_dVmG4X4xo4y0rBP8DrnpOtGASGvV1yiDAgqX9iJVVNUfBJWkC2ZYHdIuMP55bZcZQ04huT_q9i-U-OUXznrVdtPWmEz3uIrD8JortLBo3R2aXT145ha5Rt1LOFuNLOCOpfcQtg"
        self.auth_header_ = {'Authorization': 'Bearer ' + self.access_token_}

    def login(self):
        result = None
        # Note: If your device-flow app does not have any interactive ability, you can
        #   completely skip the following cache part. But here we demonstrate it anyway.
        # We now check the cache to see if we have some end users signed in before.
        sys.stdout.flush()
        app = msal.PublicClientApplication(self.client_id_, authority=self.tenant_id_)
        accounts = app.get_accounts()
        if accounts:
            print("Pick the account you want to use to proceed:")
            for a in accounts:
                print(a["username"])
            # Assuming the end user chose this one
            chosen = accounts[0]
            # Now let's try to find a token in cache for this account
            result = app.acquire_token_silent(self.config_["scope"], account=chosen)
        if not result:
            sys.stdout.flush()
            flow = app.initiate_device_flow(scopes=self.scopes_)
            print(flow["message"])
            sys.stdout.flush()
            result = app.acquire_token_by_device_flow(flow)
            print(result['access_token'])
        if "access_token" in result:
            self.access_token_ = result['access_token']
            self.auth_header_ = {'Authorization': 'Bearer ' + result['access_token']}
        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))  # You may need this when reporting a bug

    def check_inbox(self):
        """Return a list of unread mails in dict format from inbox"""
        response = requests.get(self.config_['inbox'], headers=self.auth_header_).json()
        if 'error' in response:
            # if 'code' in response['error'] and response['error']['code'] == \
            #     'InvalidAuthenticationToken':
            #     self.login()
            # else:
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
                #test
                reviewer = 'changxing.gong@gmail.com'
                new_conv_id, date_sent = self.send_req(self.parser_.get_review_req(), \
                                                        mail, reviewer)
                self.db_.store_review_req(convo_id, new_conv_id, reviewer, date_sent)
            elif self.parser_.is_review(subject):
                self.db_.store_review(convo_id, date)
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

    def reply_subm(self, msg_id, mail, is_success):
        """
            Provided:

        """
        comment = message_temp.SUBMISSION_SUCCESS if is_success \
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

    def draw_reviewers(self):
        """
            Provided:

        """
        raise NotImplementedError

    def get_attachments(self, msg_id):
        response = requests.get(self.config_['get_attachments'].format(msg_id), \
                    headers=self.auth_header_).json()
        if 'error' in response:
            print(response)
            print('Error: get_attachments')
            exit(1)
        return response['value']