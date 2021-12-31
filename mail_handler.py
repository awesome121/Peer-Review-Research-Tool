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
        self.access_token_ = 'ceyJ0eXAiOiJKV1QiLCJub25jZSI6Imh0V2pUU3RoZlJRZzNCa0kzMnJJdTFCaFJzbFI3MFNieHlxMDB5b25yLVkiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCIsImtpZCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEvIiwiaWF0IjoxNjQwOTExNzI1LCJuYmYiOjE2NDA5MTE3MjUsImV4cCI6MTY0MDkxNjE1OCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFTUUEyLzhUQUFBQUxGRC83ZXFkNHRJNnpFZjRQNFRZNkg2Z1ZOQ3hPNmNzZ0VpZWRpQU5obTQ9IiwiYW1yIjpbInB3ZCJdLCJhcHBfZGlzcGxheW5hbWUiOiJib3QiLCJhcHBpZCI6ImRkODliYjk0LTA3ZjQtNGU1ZC1iNjQxLTEyNWZjOTZiZmRlZSIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiR29uZyIsImdpdmVuX25hbWUiOiJDaGFuZ3hpbmciLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxNTEuMjEwLjE3MS4xMDMiLCJuYW1lIjoiQ2hhbmd4aW5nIEdvbmciLCJvaWQiOiI0NzJkZjIwZS05NmY1LTQ3YWEtOGIzOS1iOWNlZWMwZGE4MDkiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtOTY2MjA0MTQzLTc0NjkzMjY5MC0xMTUzOTQ2Mi0yODE3MjMiLCJwbGF0ZiI6IjE0IiwicHVpZCI6IjEwMDMwMDAwQUU0Q0ZGOEUiLCJyaCI6IjAuQVVFQUp4ZDQzQTV4VlVpOFRHa0NacUcxVVpTN2lkMzBCMTFPdGtFU1g4bHJfZTVCQURrLiIsInNjcCI6IklNQVAuQWNjZXNzQXNVc2VyLkFsbCBNYWlsLlJlYWQgTWFpbC5SZWFkQmFzaWMgTWFpbC5SZWFkV3JpdGUgTWFpbC5TZW5kIG9wZW5pZCBwcm9maWxlIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgVXNlci5SZWFkV3JpdGUgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJCa2ZvdTlVOHdtZzhJb3Zkb3lKU0YzN2ZfN3N2WmU1bVo2di1CdzM3YjZjIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6Ik9DIiwidGlkIjoiZGM3ODE3MjctNzEwZS00ODU1LWJjNGMtNjkwMjY2YTFiNTUxIiwidW5pcXVlX25hbWUiOiJjZ281NEB1Y2xpdmUuYWMubnoiLCJ1cG4iOiJjZ281NEB1Y2xpdmUuYWMubnoiLCJ1dGkiOiI1THgwSW1ubVUwdTg4Q1g3eUozSkFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX3N0Ijp7InN1YiI6Inp2VWtVMU9oOS1RcVFwZ1E0YXoxVmY4MDBVTms1Q0tqelBoOUU2Rl9CcDAifSwieG1zX3RjZHQiOjEzNjY5MTAwOTB9.e_WQ6N5lnmCrXYrR2mqMtjMZdBfUY6UxDnG9jX__-9sZ0ng0Y-FUqh043dKL9UlnMXt7Nxnji541HNrwMC8v4ZgANU9zf3OSQT3c4q85gMsvDMdHWeS8grITYiCx8N_i-z-OYVcrwZYw_KDfT4ITIHguagl_vRy27WYG_iczCFUArSU8xruXuV2Vs2fexkrj4FrsuoTN4G7lthDE20WgRREW-Rr7ycN6x0-DuQcVrZKUj0d72kyq3E8IbTFlK__DbzQk36q5HEkcY5eJC-74mNB0nk5tqscYbDzMXzpjMiA4p6VvBdHxlaZKOav0iw0JEGiYMJ6M4kp-P6M7C_0dfw' # test
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
        """Return a list of unread mails in inbox"""
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
            msg_id, subject, from_ = self.parser_.parse_mail(mail)
            self.mark_as_read(msg_id)
            if not self.db_.is_subscriber(from_):
                pass #ignore non-subscriber
            elif self.parser_.is_submission(subject):
                # db_.store_submission(from_, submission_id, msg_id, date)
                self.send_submission_success(msg_id, mail)
            elif self.parser_.is_review(subject):
                print(mail)
                # db_.store_review()
                # self.send_evaluation_request()
            elif self.parser_.is_evaluation(subject):
                self.store_evaluation()
            else: # subscriber but invalid subject
                # self.send_usage_instruction()
                raise NotImplementedError

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

    def send_submission_success(self, msg_id, mail):
        """
            Provided:

        """
        data = {
            "message":{  
                "toRecipients":[ mail['from'] ]
            },
            "comment": message_temp.SUBMISSION_SUCCESS
        }

        # data is required to dumped into json format, 'Content-Type' header is required
        response = requests.post(self.config_['reply_msg'].format(msg_id), json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        print(response.status_code)
        # print(response.json())
        if 'error' in response:
            print(response)
            print('Error: send_submission_success')
            exit(1)



    def send_review_request(self):
        """
            Provided:

        """
        raise NotImplementedError

    def send_evaluation_request(self):
        """
            Provided:

        """
        raise NotImplementedError

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
