"""
Mail Handler


"""

import re
import msal, sys, requests, json, message_temp



class MailHandler:
    def __init__(self):
        with open("configuration.json") as conf:
            self.config_ = json.load(conf)
        self.client_id_ = self.config_['client_id'] 
        self.tenant_id_ = self.config_['tenant_id'] 
        self.scopes_ = self.config_['scope']
        self.access_token_ = None
        
    def login_test(self):
        self.access_token_ = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Im4yZGY4NVFPOFhHY1YtbjFuR25tMTNaTWh5Q0kwZF8xUk9mWGNTUWY1SDQiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCIsImtpZCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEvIiwiaWF0IjoxNjQxMjU0MjY0LCJuYmYiOjE2NDEyNTQyNjQsImV4cCI6MTY0MTI1OTM0NSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFTUUEyLzhUQUFBQTFXTUZVNU5ESnkvekg5aTJxcGk2SE95MXhmc2poYXNsaGJFTFRhcFNvQ0k9IiwiYW1yIjpbInB3ZCJdLCJhcHBfZGlzcGxheW5hbWUiOiJib3QiLCJhcHBpZCI6ImRkODliYjk0LTA3ZjQtNGU1ZC1iNjQxLTEyNWZjOTZiZmRlZSIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiTGlhbmciLCJnaXZlbl9uYW1lIjoiSnVud2VpIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMjAzLjIxMS43Mi4xNDgiLCJuYW1lIjoiSnVud2VpIExpYW5nIiwib2lkIjoiMjMwMzI2YmUtYzg1MS00MWI1LTg2OTEtNzBmZTRhNTI0NWRlIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTk2NjIwNDE0My03NDY5MzI2OTAtMTE1Mzk0NjItMjk2NjE1IiwicGxhdGYiOiIxNCIsInB1aWQiOiIxMDAzMjAwMDRDNDU5Q0I2IiwicmgiOiIwLkFVRUFKeGQ0M0E1eFZVaThUR2tDWnFHMVVaUzdpZDMwQjExT3RrRVNYOGxyX2U1QkFKOC4iLCJzY3AiOiJJTUFQLkFjY2Vzc0FzVXNlci5BbGwgTWFpbC5SZWFkIE1haWwuUmVhZEJhc2ljIE1haWwuUmVhZFdyaXRlIE1haWwuU2VuZCBvcGVuaWQgcHJvZmlsZSBVc2VyLlJlYWQgVXNlci5SZWFkQmFzaWMuQWxsIFVzZXIuUmVhZFdyaXRlIGVtYWlsIiwic2lnbmluX3N0YXRlIjpbImttc2kiXSwic3ViIjoibWVXQTg1OWZOZkNhaHVzZURrR0xyVDAzeDVpaHZTbWNSUXJqbnBXc1B4cyIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJPQyIsInRpZCI6ImRjNzgxNzI3LTcxMGUtNDg1NS1iYzRjLTY5MDI2NmExYjU1MSIsInVuaXF1ZV9uYW1lIjoiamxpMzI4QHVjbGl2ZS5hYy5ueiIsInVwbiI6ImpsaTMyOEB1Y2xpdmUuYWMubnoiLCJ1dGkiOiJ2TlZPOGxQVXVVU2N5UFBSUV9NTUFRIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX3N0Ijp7InN1YiI6Ik5Kc19mVWJ4TmVIM0ptV2REVG90VjZiWkp0c2pUR283R0RNQTk2QWhZdGcifSwieG1zX3RjZHQiOjEzNjY5MTAwOTB9.TyV0aQSTPslzk09YnHCd3Me3nKYxPAiSekuYz6T9lZFMLKDl7kiV9GCZtwPukRAmj7PyVcWbt-qYGb_ov5k2aZkOFkhT8bWwgdFQnKd3J4_mG5Cisid9CYnlfYU3HtIiopMVR-L_TJV20XGOUQbUiv-5Pvhk3czm0boRgoO5gHOWUREezqAQ_v3Paa8zVE2dwnvNSGQ5-2EmWIGtntDW66g80AkgVoag-KGvBeOZ5DdqT-3u5gM3ofcX0E1sH_XB-vCkcEwMETTP6ZW6y09qjdEkROCZElKe3AxcFLohsWsflCpnLNuhiZoDUA3JF_9ZCWIjzlG_TrQXFphrxxrvBA"
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
        """Return a list of unread mails in JSON format from inbox"""
        response = requests.get(self.config_['inbox'], headers=self.auth_header_).json()
        if 'error' in response:
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
            mails: a list of mails in JSON representaion

        """
        for mail in mails:
            msg_id, convo_id, subject, from_, date = self.parser_.parse_mail(mail)
            self.mark_as_read(msg_id)
            if not self.db_.is_subscriber(from_):
                pass #ignore non-subscriber
            elif self.parser_.is_subm(subject):
                if self.db_.store_subm(convo_id, from_, \
                                          self.parser_.get_subm_id(subject), date):
                    self.reply_subm(msg_id, mail, True)
                else:
                    self.reply_subm(msg_id, mail, False)
                #test
                reviewer = 'changxing.gong@gmail.com'
                self.send_req(self.parser_.get_review_req(), mail, reviewer)
                # self.db_.store_review_req(reviewer)
            elif self.parser_.is_review(subject):
                self.db_.store_review(convo_id, date)
                self.send_req(self.parser_.get_eval_req(), mail, 'changxing.gong@gmail.com')
                # self.db_.store_eval_req()
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
        if 'error' in response:
            print(response)
            print('Error: send_req')
            exit(1)


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