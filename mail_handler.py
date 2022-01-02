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
        self.access_token_ = "eyJ0eXAiOiJKV1QiLCJub25jZSI6InRQdzVza05BTjgyVDk1WHlLb2pxNTd6cnRQLWlhV1M1eGhSRmNCcE5WWm8iLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCIsImtpZCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEvIiwiaWF0IjoxNjQxMTU1ODA5LCJuYmYiOjE2NDExNTU4MDksImV4cCI6MTY0MTE2MDkyNywiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFTUUEyLzhUQUFBQUtvQ0RJQ3hFMkRUa3pYYXFlTE90UnJjR0F1dTdzWENKb29JQTdhWFB0UGs9IiwiYW1yIjpbInB3ZCJdLCJhcHBfZGlzcGxheW5hbWUiOiJib3QiLCJhcHBpZCI6ImRkODliYjk0LTA3ZjQtNGU1ZC1iNjQxLTEyNWZjOTZiZmRlZSIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiR29uZyIsImdpdmVuX25hbWUiOiJDaGFuZ3hpbmciLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxNTEuMjEwLjE3MS4xMDMiLCJuYW1lIjoiQ2hhbmd4aW5nIEdvbmciLCJvaWQiOiI0NzJkZjIwZS05NmY1LTQ3YWEtOGIzOS1iOWNlZWMwZGE4MDkiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtOTY2MjA0MTQzLTc0NjkzMjY5MC0xMTUzOTQ2Mi0yODE3MjMiLCJwbGF0ZiI6IjE0IiwicHVpZCI6IjEwMDMwMDAwQUU0Q0ZGOEUiLCJyaCI6IjAuQVVFQUp4ZDQzQTV4VlVpOFRHa0NacUcxVVpTN2lkMzBCMTFPdGtFU1g4bHJfZTVCQURrLiIsInNjcCI6IklNQVAuQWNjZXNzQXNVc2VyLkFsbCBNYWlsLlJlYWQgTWFpbC5SZWFkQmFzaWMgTWFpbC5SZWFkV3JpdGUgTWFpbC5TZW5kIG9wZW5pZCBwcm9maWxlIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgVXNlci5SZWFkV3JpdGUgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJCa2ZvdTlVOHdtZzhJb3Zkb3lKU0YzN2ZfN3N2WmU1bVo2di1CdzM3YjZjIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6Ik9DIiwidGlkIjoiZGM3ODE3MjctNzEwZS00ODU1LWJjNGMtNjkwMjY2YTFiNTUxIiwidW5pcXVlX25hbWUiOiJjZ281NEB1Y2xpdmUuYWMubnoiLCJ1cG4iOiJjZ281NEB1Y2xpdmUuYWMubnoiLCJ1dGkiOiJQSVRhVkpCV2wwS1ZydEhpUDY2bkFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX3N0Ijp7InN1YiI6Inp2VWtVMU9oOS1RcVFwZ1E0YXoxVmY4MDBVTms1Q0tqelBoOUU2Rl9CcDAifSwieG1zX3RjZHQiOjEzNjY5MTAwOTB9.mjDJrmPmWuFDldBfn8M8zvoghBM2kCbGIJsWWKrb3vkn9GBqmSu0c1OW_gizCHhOYp0xYh9AVSvMyh4JjZ8tpm-vR8qtnt_zzm8mvMEPnWfHcoh4hvXf62IH3Tj6AGXwOG7zkxjcTOfiKfYfiQWNKxyAv_lzdP_WmWG--mriNur_58Qc6DhwEgV7U5fv86H0GH3Yy6aXXLxaxPo5QSqexVRSoHHz_zNjP19-rsrlm6Z3LHSICKbrjG3S8dWlQrjtTT0RNAFsJp78OrLUd6Ljw6mE4Tvh_CnSkcDk0N6QdH73JTdtO9TrDS2go-tg4JQZT1bfbRFbGBksSfJybWtVWQ"
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
                    print(mail)
                else:
                    self.reply_subm(msg_id, mail, False)
            elif self.parser_.is_review(subject):
                self.db_.store_review(convo_id, date)
                # self.send_eval_req()
            elif self.parser_.is_eval(subject):
                rating, comment = self.parser_.get_eval(mail)
                self.db_.store_eval(convo_id, rating, comment, date)
                # raise NotImplementedError
            else: # subscriber but invalid subject
                # self.send_usage_instruction()
                print(subject)
                # raise NotImplementedError

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
                else message_temp.REVIEW_REQUEST
        data = {
            "message":{  
                "toRecipients":[ mail['from'] ]
            },
            "comment": comment
        }

        # data is required to dumped into json format, 'Content-Type' header is required
        response = requests.post(self.config_['reply_msg'].format(msg_id), json.dumps(data), \
            headers=self.auth_header_ | {'Content-Type': 'application/json'})
        print(response.status_code)
        # print(response.json())
        if 'error' in response:
            print(response)
            print('Error: reply_subm')
            exit(1)



    def send_review_req(self):
        """
            Provided:

        """
        raise NotImplementedError

    def send_eval_req(self):
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
