import os, time, threading, sys, msal, json
import admin_UI, database
from mail_handler import MailHandler
# os.system("rm database.db")
# db.create_database()

class App:
    def __init__(self):
        self.init_param()
        self.load_config()
        # self.connect() # event-driven function
        if os.path.exists("database.db"):
            self.UI_controller = admin_UI.Controller(self, True)
            self.UI_controller.land_on_dashboard()
        else:
            self.db = database.Database()
            self.db.create_database()
            self.UI_controller = admin_UI.Controller(self, False)
    
    def init_param(self):
        self.listener = None
        self.listener_t = None
        self.distributor = None
        self.distributor_t = None
        self.token = None
        self.flow = None
        self.monitor_t = None
        self.is_auth_success = False
        self.is_connected = False

    def load_config(self):
        with open("configuration.json") as conf:
            self.config_ = json.load(conf)
        self.client_id_ = self.config_['client_id'] 
        self.tenant_id_ = self.config_['tenant_id'] 
        self.scopes_ = self.config_['scope']

    def try_connect(self):
        self.auth_t = threading.Thread(target=self.login)
        self.auth_t.start()

    def connect_succuss(self):
        """UI event-driven function"""
        print('connection success', flush=True)
        self.is_connected = True
        self.listener_t = threading.Thread(target=self.create_listener)
        self.listener_t.start()

        self.monitor_t = threading.Thread(target=self.monitor)
        self.monitor_t.start()

    def monitor(self):
        while self.is_connected:
            self.check_deadline()
            self.refresh_token()
            time.sleep(1)
        self.init_param()
    
    def check_deadline(self):
        subm_id = self.db.get_undistributed_subm_id()
        if subm_id:
            threading.Thread(target=self.create_distributor, args=(subm_id,))

    def create_listener(self):
        auth_header = {'Authorization': 'Bearer ' + self.token}
        self.listener = MailHandler(self, auth_header)
        self.listener.listen()

    def create_distributor(self, subm_id):
        auth_header = {'Authorization': 'Bearer ' + self.token}
        self.distributor = MailHandler(self, auth_header)
        self.distributor.distribute_subm(subm_id)


    def login(self):
        """
            Refresh token if there is a cached token.
            Otherwise, a new device flow is initiated
            An url and an authentication code will be displayed upon initiation 
        """
        try:
            # print(threading.active_count())
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
                self.flow = flow
                # print(flow["message"])
                sys.stdout.flush()
                result = self.app.acquire_token_by_device_flow(flow)
            if "access_token" in result: # success
                self.token = result['access_token']
                self.connect_succuss()
            else: # failure
                self.clear_auth_flow()
                sys.exit()
        except AttributeError:
            sys.exit()
        except:
            self.clear_auth_flow()
            sys.exit()
    
    def clear_auth_flow(self):
        try:
            del self.flow
        except AttributeError:
            return
    
    def refresh_token(self):
        accounts = self.app.get_accounts()
        result = self.app.acquire_token_silent(self.scopes_, account=accounts[0])
        print(result['expires_in'], threading.get_ident(), threading.active_count())
        # print(sys.getrefcount(self))
        if self.token != result['access_token']:
            # print(result['access_token'])
            self.token = result['access_token']
            auth_header = {'Authorization': 'Bearer ' + self.token}
            self.listener.auth_header_ = auth_header
            if self.distributor:
                self.distributor.auth_header_ = auth_header

    def set_auth_success(self):
        self.is_auth_success = True

    def reset_auth_success(self):
        self.is_auth_success = False

    def is_authenticated(self):
        return self.is_auth_success

    def interrupt_auth_flow(self):
        self.flow['expires_at'] = 0

    def disconnect(self):
        self.is_connected = False

    def get_conn_status(self):
        return self.is_connected
    
if __name__ == '__main__':
    app = App()





