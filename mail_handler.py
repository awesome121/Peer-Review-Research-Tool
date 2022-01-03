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
        self.access_token_ = 'eyJ0eXAiOiJKV1QiLCJub25jZSI6IlJJRG9tMjdBOEZaM2J1S090M0VhN1hrQ19QTHhFQ3dKeHRYTW5mWFp2ZmsiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCIsImtpZCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEvIiwiaWF0IjoxNjQxMTc4MDYyLCJuYmYiOjE2NDExNzgwNjIsImV4cCI6MTY0MTE4MzM2NywiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkUyWmdZTEFVTjIzc2Vpb2FzREQ4c1lqL2hVL2M0cnM5NWxSMjNuMzUzZTdjcjNpeitVVUEiLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6ImJvdCIsImFwcGlkIjoiZGQ4OWJiOTQtMDdmNC00ZTVkLWI2NDEtMTI1ZmM5NmJmZGVlIiwiYXBwaWRhY3IiOiIwIiwiZmFtaWx5X25hbWUiOiJMaWFuZyIsImdpdmVuX25hbWUiOiJKdW53ZWkiLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIyMDMuMjExLjcyLjE0OCIsIm5hbWUiOiJKdW53ZWkgTGlhbmciLCJvaWQiOiIyMzAzMjZiZS1jODUxLTQxYjUtODY5MS03MGZlNGE1MjQ1ZGUiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtOTY2MjA0MTQzLTc0NjkzMjY5MC0xMTUzOTQ2Mi0yOTY2MTUiLCJwbGF0ZiI6IjE0IiwicHVpZCI6IjEwMDMyMDAwNEM0NTlDQjYiLCJyaCI6IjAuQVVFQUp4ZDQzQTV4VlVpOFRHa0NacUcxVVpTN2lkMzBCMTFPdGtFU1g4bHJfZTVCQUo4LiIsInNjcCI6IklNQVAuQWNjZXNzQXNVc2VyLkFsbCBNYWlsLlJlYWQgTWFpbC5SZWFkQmFzaWMgTWFpbC5SZWFkV3JpdGUgTWFpbC5TZW5kIG9wZW5pZCBwcm9maWxlIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgVXNlci5SZWFkV3JpdGUgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJtZVdBODU5Zk5mQ2FodXNlRGtHTHJUMDN4NWlodlNtY1JRcmpucFdzUHhzIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6Ik9DIiwidGlkIjoiZGM3ODE3MjctNzEwZS00ODU1LWJjNGMtNjkwMjY2YTFiNTUxIiwidW5pcXVlX25hbWUiOiJqbGkzMjhAdWNsaXZlLmFjLm56IiwidXBuIjoiamxpMzI4QHVjbGl2ZS5hYy5ueiIsInV0aSI6ImFoSVVsU0lMdUVTN3BzTDJJbEhrQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfc3QiOnsic3ViIjoiTkpzX2ZVYnhOZUgzSm1XZERUb3RWNmJaSnRzalRHbzdHRE1BOTZBaFl0ZyJ9LCJ4bXNfdGNkdCI6MTM2NjkxMDA5MH0.o3k31UHdGTznOq-8rq9tQtLBLxokW-1pNBi21A-mcOCcjNKKU6THJXqZOHLWbRoAmcWqnWOIc5YQP9iqwlXzLZ53GA2XYtgSrPOGQJL7Jpuh3Zs3fAj3IgliJurqCEz13-XflUff00ZeV2fdA0M3KjP2fNtn7YybC5r6haVyxQcJXBBC6C--bTUTX9PNQ4F4t8gBt5OqCw0DZJ8EjMerlzbSnEbOhuyx7nNZ4cfjmeW5g1sIz-VU5nib951u31X4qsimBlf2VntoZcL9QXE4hY0O0ZQJIGt4u7E479Qr73j28qDA4lFIf1vMBOhBhh3ImnvDgwnCsCmtw_ckuXjR5w' # test
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