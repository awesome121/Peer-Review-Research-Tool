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
        
        
    def login(self):
        result = None
        # Note: If your device-flow app does not have any interactive ability, you can
        #   completely skip the following cache part. But here we demonstrate it anyway.
        # We now check the cache to see if we have some end users signed in before.
        sys.stdout.flush()
        app = msal.PublicClientApplication(self.client_id_, authority=self.tenant_id_)
        # accounts = app.get_accounts()
        # if accounts:
        #     print("Pick the account you want to use to proceed:")
        #     for a in accounts:
        #         print(a["username"])
        #     # Assuming the end user chose this one
        #     chosen = accounts[0]
        #     # Now let's try to find a token in cache for this account
        #     result = app.acquire_token_silent(self.config_["scope"], account=chosen)
        # if not result:
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
                return response['value']
            else:
                return []
                
    def process_unread(self, mails):
        for mail in mails:
            msg_id, subject, from_ = self.parser_.parse_mail(mail)
            self.mark_as_read(msg_id)
            if not self.db_.is_subscriber(from_):
                pass #ignore non-subscriber
            elif self.parser_.is_submission(subject):
                self.send_submission_success(msg_id, mail)
            elif self.parser_.is_review(subject):
                self.parser_.get_review_request()
            elif self.parser_.is_evaluation(subject):
                self.parser_.get_evaluation_request()
            else: # subscriber but invalid subject
                raise NotImplementedError

    def mark_as_read(self, msg_id):
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
        data = {
            "message":{  
                "toRecipients":[ mail['from'] ]
            },
            "comment": message_temp.SUBMISSION_SUCCESS
        }
        response = requests.post(self.config_['reply_msg'].format(msg_id), json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        print(response.status_code)
        # print(response.json())
        if 'error' in response:
            print(response)
            print('Error: send_submission_success')
            exit(1)



    def send_message(self):
        raise NotImplementedError

    def draw_reviewers(self):
        raise NotImplementedError
