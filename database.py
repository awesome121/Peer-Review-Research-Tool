"""
    Provided (with header, see example):
    email_addr.csv          format: email_addr
    deadline.csv            format: submission_id, date

    Generated:
    database.db
    
    Tables in database.db:
    email_list
    deadline
    num_review
    db_core
"""


import csv, sqlite3

class Database:
    """
        Database class, this class is expected to run continously for weeks
        This class handles internal database tables using sqlite3, it interacts
        with Mailhandler class.
    """
    def __init__(self):
        """
            Set constant file names and parameters
        """
        # Provided files:
        self.EMAIL_ADDR = "email_addr.csv"
        self.DEADLINE = "deadline.csv"
        # Database generated file:
        self.DATABASE = "database.db"
        # tables
        self.TB_EMAIL_LIST = "email_list"
        self.TB_DEADLINE = "deadline"
        self.TB_NUM_REVIEW = "num_review"
        self.TB_CORE = "core"
        # Database constants:
        self.MAX_SUBMISSION = 6
        self.NUM_REVIEW_REQUEST = 3
#--------------------------------------------------
    def create_database(self):
        """ 
            ===This function can be called only on initialising database===
            This function further calls subsequent functions init_email_list, 
            init_deadline, init_num_review, init_core to initialise tables
            email_list, deadline, num_review, and core respectively.
        
            email_list: email address of subscribers
            deadline: submission ID, date
            num_review: currently number of received distribution for each submission 
            core: a joined table
        """
        con = sqlite3.connect(self.DATABASE)
        cur = con.cursor()
        self.init_email_list(cur)
        self.init_deadline(cur)
        self.init_num_review(cur)
        self.init_core(cur)
        con.commit()
        con.close()

    def init_email_list(self, cur):
        """
            ===This function can be called only on initialising database===
            Provided:
                email_addr.csv 
            Generates:
                email_addr table in database.db
        """
        cur.execute(f'CREATE TABLE {self.TB_EMAIL_LIST} (address text)')
        with open(self.EMAIL_ADDR) as file:
            lines = file.read().splitlines()
        cur.executemany(lines)

    def init_deadline(self, cur):
        """
            ===This function can be called only on initialising database===
            Provided:
                deadline.csv 
            Generates:
                deadline table in database.db
        """
        cur.execute(f'CREATE TABLE {self.TB_DEADLINE} (submission_id integer, date text)')
        with open(self.DEADLINE) as file:
            lines = file.read().splitlines()
        cur.executemany(lines)

    def init_num_review(self, cur):
        """
            ===This function can be called only on initialising database===
            Provided:
                email_addr.csv 
            Generates:
                num_review table in database.db
        """
        cur.execute(f'CREATE TABLE {self.TB_NUM_REVIEW} (reviewer text, number integer)')
        with open(self.EMAIL_ADDR) as file:
            lines = file.read().splitlines()
        lines = [(line, 0) for line in lines]
        cur.executemany(lines)

    def init_core(self, cur):
        """
            ===This function can be called only on initialising database===
            Provided:
                email_addr.csv 
            Generates:
                core table in database.db
        """
        # cur.execute(f'CREATE TABLE {self.TB_CORE} ()')
        # with open(self.EMAIL_ADDR) as file:
        #     addresses = file.read().splitlines()
        
        # cur.executemany(lines)


#--------------------------------------------------

    def is_subscriber(self, addr):
        """
            Return True if addr is in email address list
            False otherwise
        """
        con = sqlite3.connect(self.DATABASE)
        cur = con.cursor()
        cur.execute(f'SELECT * FROM {self.TB_EMAIL_LIST} where address = {addr}')
        result = cur.fetchall()
        con.close()
        return len(result) != 0
   
    def draw_reviewers(self, author):
        """
            Provided:
            a string of an author's email address

            draw three reviewers (except this auther),
            a reviewer can only review maximum 3 different 
            submissions, finally increment their num of 
            reviews in num_review.db.

            Return:
            a list of reviewers' email addresses
        """
        raise NotImplementedError

    def store_submission(self, from_, submission_id, msg_id, date):
        """
            Provided:
            from_: a string of an author's email address
            submission_id: a string of a submission id, e.g. '1', '2', '3'
            msg_id: a string of email message id for this submission
            date: The date on receiving this submission

            Return:
            True on successfully storing
            False if it exists already
        """
        raise NotImplementedError

#--------------------------------------------------
    def export_table(self, table, filename):
        """
            Provided:
            table: a string of table name. (e.g. "db_core")
            filename: a string of filename, where the table in database
                    will be exported to.

            Generates: A string of csv file name with its name corresponding to 
                the table name
            Return: True on success, False otherwise
        """
        try:
            con = sqlite3.connect(self.DATABASE)
            cur = con.cursor()
            cur.execute(f'SELECT * FROM {table}')
            result = cur.fetchall()
            with open(filename, 'wb') as file:
                writer = csv.writer(file)
                header = [description[0] for description in cur.description]
                writer.writerow(header)
                writer.writerows(result)
            con.close()
        except:
            con.close()
            return False
        return True

