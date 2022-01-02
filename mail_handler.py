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
        self.access_token_ = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IkZLaGt1Mk45MmpzUzZwRXFGNGEtblZpRVpqM09OS2pVRjMwRVJBdEt4dXMiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCIsImtpZCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEvIiwiaWF0IjoxNjQxMDc1NjA5LCJuYmYiOjE2NDEwNzU2MDksImV4cCI6MTY0MTA4MDQwNiwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkUyWmdZTmhvMC90M3pXR05peGZpazg2Ym5wR1hYbEphdS9PSlZuRzduV3pneGJnZnZOOEEiLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6ImJvdCIsImFwcGlkIjoiZGQ4OWJiOTQtMDdmNC00ZTVkLWI2NDEtMTI1ZmM5NmJmZGVlIiwiYXBwaWRhY3IiOiIwIiwiZmFtaWx5X25hbWUiOiJHb25nIiwiZ2l2ZW5fbmFtZSI6IkNoYW5neGluZyIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjE1MS4yMTAuMTcxLjEwMyIsIm5hbWUiOiJDaGFuZ3hpbmcgR29uZyIsIm9pZCI6IjQ3MmRmMjBlLTk2ZjUtNDdhYS04YjM5LWI5Y2VlYzBkYTgwOSIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS05NjYyMDQxNDMtNzQ2OTMyNjkwLTExNTM5NDYyLTI4MTcyMyIsInBsYXRmIjoiMTQiLCJwdWlkIjoiMTAwMzAwMDBBRTRDRkY4RSIsInJoIjoiMC5BVUVBSnhkNDNBNXhWVWk4VEdrQ1pxRzFVWlM3aWQzMEIxMU90a0VTWDhscl9lNUJBRGsuIiwic2NwIjoiSU1BUC5BY2Nlc3NBc1VzZXIuQWxsIE1haWwuUmVhZCBNYWlsLlJlYWRCYXNpYyBNYWlsLlJlYWRXcml0ZSBNYWlsLlNlbmQgb3BlbmlkIHByb2ZpbGUgVXNlci5SZWFkIFVzZXIuUmVhZEJhc2ljLkFsbCBVc2VyLlJlYWRXcml0ZSBlbWFpbCIsInNpZ25pbl9zdGF0ZSI6WyJrbXNpIl0sInN1YiI6IkJrZm91OVU4d21nOElvdmRveUpTRjM3Zl83c3ZaZTVtWjZ2LUJ3MzdiNmMiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiT0MiLCJ0aWQiOiJkYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEiLCJ1bmlxdWVfbmFtZSI6ImNnbzU0QHVjbGl2ZS5hYy5ueiIsInVwbiI6ImNnbzU0QHVjbGl2ZS5hYy5ueiIsInV0aSI6ImFFWmdRUW9nbTBlMDk5Z2FRem5QQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfc3QiOnsic3ViIjoienZVa1UxT2g5LVFxUXBnUTRhejFWZjgwMFVOazVDS2p6UGg5RTZGX0JwMCJ9LCJ4bXNfdGNkdCI6MTM2NjkxMDA5MH0.aAytrDhultJ-uyq9eAQZ8x3Tk0xW_VMwKZbBkLFcsotMH4MKUODRhM4Uv-gQol7pWu2dMBfbJd63ViuQpGJ_Yc1UDI3gJ9FDObwwHNcPrkEmefWQtzqOWxCPPLF1_hij9jIB2ojHN3ehNiGI7V5VMKhycBs1eRcoP4QGhVRoloVbvXZVwLCJ6xpYS2-D8mjNyXL05XN2EHH8MDNyMn9Z_DUQ31EEXSWdczI2iZHsCcetlMbYn0_vGDgO8PdlwbWXwt8Zv9PcrPxxr9PrXWl1SM09C9mdJ2qk_EzSXz8hO2eAD_iulrRc5Gr3zfUgN-P09Fvb6oVX_Aj11A0fFTL-VQ"
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
            elif self.parser_.is_review(subject):
                self.db_.store_review(convo_id, date)
                # self.send_eval_req()
            elif self.parser_.is_eval(subject):
                rating, comment = self.parser_.get_eval(mail)
                self.store_eval(convo_id, rating, comment, date)
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
