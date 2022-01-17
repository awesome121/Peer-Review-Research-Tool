import os, time, threading, admin_UI, sys, msal, json, sys, database
import login_mfa
from database import Database
from mail_parser import MailParser
from mail_handler import MailHandler
# os.system("rm database.db")
# db.create_database()

class App:
    def __init__(self):
        self.token = None
        self.listener = None
        self.listener_t = None
        self.distributor = None
        self.distributor_t = None
        self.deadline_monitor_t = None
        
        self.load_config()
        # self.connect() # event-driven function
        
        if os.path.exists("database.db"):
            login_mfa.AdminUI(self, True)
        else:
            self.db = database.Database()
            self.db.create_database()
            # admin_UI.Admin_UI(self, False)
        #main thread create UI


    def load_config(self):
        with open("configuration.json") as conf:
            self.config_ = json.load(conf)
        self.client_id_ = self.config_['client_id'] 
        self.tenant_id_ = self.config_['tenant_id'] 
        self.scopes_ = self.config_['scope']

    def connect(self):
        """UI event-driven function"""
        self.login()
        self.listener_t = threading.Thread(target=self.create_listener)
        self.listener_t.start()

        self.deadline_monitor_t = threading.Thread(target=self.deadline_monitor)
        self.deadline_monitor_t.start()

    def deadline_monitor(self):
        while True:
            # self.check_deadline()
            self.refresh_token()
    
    def check_deadline(self):
        pass
        # if it's deadline:
            # threading.Thread(target=create_distributor) # around 11:59 pm, stay 1-2 hours

    def create_listener(self):
        auth_header = {'Authorization': 'Bearer ' + self.token}
        self.listener = MailHandler(auth_header)
        self.listener.listen()

    def create_distributor(self):
        auth_header = {'Authorization': 'Bearer ' + self.token}
        self.distributor = MailHandler(auth_header)
        self.distributor.distribute_subm()


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
        if accounts:
            print("Pick the account you want to use to proceed:")
            print(accounts)
            # Assuming the end user chose this one
            chosen = accounts[0]
            # Now let's try to find a token in cache for this account
            result = self.app.acquire_token_silent(self.scopes_, account=chosen)
        if not result:
            flow = self.app.initiate_device_flow(scopes=self.scopes_)
            print(flow["message"])
            sys.stdout.flush()
            result = self.app.acquire_token_by_device_flow(flow)
        if "access_token" in result:
            self.token = result['access_token']
        else:
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))
    

    def refresh_token(self):
        accounts = self.app.get_accounts()
        result = self.app.acquire_token_silent(self.scopes_, account=accounts[0])
        print(result['expires_in'], threading.get_ident(), threading.active_count())
        time.sleep(1)
        # print(sys.getrefcount(self))
        if self.token != result['access_token']:
            # print(result['access_token'])
            self.token = result['access_token']
            auth_header = {'Authorization': 'Bearer ' + self.token}
            self.listener.auth_header_ = auth_header
            if self.distributor:
                self.distributor.auth_header_ = auth_header

    
if __name__ == '__main__':
    app = App()





