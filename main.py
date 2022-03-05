import os, time, threading, sys, msal, json
import admin_UI, database
from mail_handler import MailHandler

DIST_INVITING = 1
DIST_DISTRIBUTING = 2


class App:
    """ 
        App class, this class is used to initialize the whole system.
    """
    def __init__(self):
        self.init_param()
        self.load_config()
        self.db = database.Database()
        if os.path.exists("database.db"):
            self.UI_controller = admin_UI.Controller(self, True)
            self.UI_controller.land_on_dashboard()
        else:
            self.db.create_database()
            self.UI_controller = admin_UI.Controller(self, False)
    
    def init_param(self):
        """Initialize parameters"""
        self.listener = None # Mail handler object listening incoming messages
        self.listener_t = None # listener thread object
        self.distributors = [] # Mail handler object for distributing submissions
        self.distributors_t = [] # distributor thread object
        
        self.token = None # Authentication token
        self.flow = None # device code flow
        self.monitor_t = None # used to monitor deadline, refresh token, etc.
        self.is_auth_success = False
        self.is_connected = False

    def load_config(self):
        """Load configuration file"""
        with open("configuration.json") as conf:
            self.config_ = json.load(conf)
        self.client_id_ = self.config_['client_id'] 
        self.tenant_id_ = self.config_['tenant_id'] 
        self.scopes_ = self.config_['scope']

    def connect_succuss(self):
        """This function will be called only by successful token acquisition"""
        print('connection success', flush=True)
        self.is_connected = True
        self.listener_t = threading.Thread(target=self.create_listener)
        self.listener_t.start()

        self.monitor_t = threading.Thread(target=self.monitor)
        self.monitor_t.start()

    def monitor(self):
        """Monitor submission deadline and refresh authentication token"""
        while self.is_connected:
            self.check_deadline()
            self.refresh_token()
            for distributor in self.distributors:
                if self.distributors.distributor_done:
                    self.distributors.remove(distributor)
            time.sleep(1)
        self.init_param()
    
    def check_deadline(self):
        """
            Checking submission start date, if there is one,
            a distributor is created for welcoming
            
            Checking submission deadline, if there is one,
            a distributor is created for distributing.
        """
        subm_id = self.db.get_uninvited_subm_id()
        if subm_id:
            print(f"Creating distributor to invite subm {subm_id}")
            distributor = threading.Thread(target=self.create_distributor, args=(subm_id,DIST_INVITING))
            self.distributors_t.append(distributor)
            distributor.start()
        subm_id = self.db.get_undistributed_subm_id()
        if subm_id:
            print(f"Creating distributor for {subm_id}")
            distributor = threading.Thread(target=self.create_distributor, args=(subm_id,DIST_DISTRIBUTING))
            self.distributors_t.append(distributor)
            distributor.start()
        

    def create_listener(self):
        """
            An MailHandler object is created for listening
        """
        auth_header = {'Authorization': 'Bearer ' + self.token} # API authentication header
        self.listener = MailHandler(self, auth_header)
        self.listener.listen()

    def create_distributor(self, subm_id, typ):
        """
            An MailHandler object is created for distributing
            Param:
                subm_id: submission id that is ready to distribute
                typ: 
                    DIST_INVITING: invite submission
                    DIST_DISTRIBUTING: distributing submission
        """
        auth_header = {'Authorization': 'Bearer ' + self.token} # API authentication header
        distributor = MailHandler(self, auth_header)
        self.distributors.append(distributor)
        if typ == DIST_INVITING:
            distributor.invite_subm(subm_id)
        elif typ == DIST_DISTRIBUTING:
            distributor.distribute_subm(subm_id)

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
                sys.exit()
        except AttributeError:
            sys.exit()
        except:
            sys.exit()
        
    def refresh_token(self):
        """
            Used to refresh authentication token, a new token lasts ~5000 seconds,
            token will be refreshed at ~300 seconds, please see MSAL documentation
            for more information
        """
        time.sleep(0.5)
        accounts = self.app.get_accounts()
        if accounts:
            result = self.app.acquire_token_silent(self.scopes_, account=accounts[0])
        else:
            print("Cannot refresh token")
            self.disconnect()
            return
        print(result['expires_in'], threading.get_ident(), threading.active_count())
        if self.token != result['access_token']:
            self.token = result['access_token']
            auth_header = {'Authorization': 'Bearer ' + self.token}
            self.listener.auth_header_ = auth_header
            if self.distributors:
                for distributor in self.distributors:
                    distributor.auth_header_ = auth_header
    
    def clear_auth_flow(self):
        """Discard authentication flow"""
        self.flow = None

    def disconnect(self):
        """
            This function can be used to interrupt MailHandler object.
            When resetting parameters, token is discarded, which stops MailHandler objects
        """
        self.init_param()

    def get_conn_status(self):
        """Return True if it's connected, False otherwise"""
        return self.is_connected

    def try_connect(self):
        """Event-driven function, used by UI controller to make a connection"""
        self.auth_t = threading.Thread(target=self.login)
        self.auth_t.start()

    def set_auth_success(self):
        """Event-driven function, used by UI controller to notify App object"""
        self.is_auth_success = True

    def interrupt_auth_flow(self):
        """
            Event-driven function, used by UI controller to interrupt 
            MailHandler's authentication flow.
            Reason for calling this function might be canceling connection.
        """
        self.flow['expires_at'] = 0 
    
if __name__ == '__main__':
    app = App()





