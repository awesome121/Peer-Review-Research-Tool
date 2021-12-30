"""
    Provided (with header, see example):
    email_addr.csv          format: email_addr
    deadline.csv            format: submission_id, date

    Generated:
    email_addr.db:
    deadline.db
    num_review.db
    db_core.db
"""


import csv

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
        # Database generated files:
        self.DB_EMAIL_ADDR = "email_addr.db"
        self.DB_DEADLINE = "deadline.db"
        self.DB_NUM_REVIEW = "num_review.db"
        self.DB_CORE = "db_core.db"
        # Database constants:
        self.MAX_SUBMISSION = 6
        self.NUM_REVIEW_REQUEST = 3
#--------------------------------------------------
    def create_database():
        """ 
            ===This function can be called only on initialising database===
            This function further calls subsequent functions init_email_list, 
            init_deadline, init_num_review, init_db_core to initialise 
            email_list.db, deadline.db, num_review.db, and db_core.db respectively.
        
            email_list.db: email address of subscribers
            deadline.db: submission ID, date
            num_review.db: currently number of received distribution for each 
            submission db_core.db: a joined table
        """
        raise NotImplementedError

    def init_email_list():
        """
            ===This function can be called only on initialising database===
            Provided:
                email_addr.csv 
            Generates:
                email_addr.db
        """
        raise NotImplementedError

    def init_deadline():
        """
            ===This function can be called only on initialising database===
            Provided:
                deadline.csv 
            Generates:
                deadline.db
        """
        raise NotImplementedError

    def init_num_review():
        """
            ===This function can be called only on initialising database===
            Provided:
                num_review.csv 
            Generates:
                num_review.db
        """
        raise NotImplementedError

    def init_db_core():
        """
            ===This function can be called only on initialising database===
            Provided:
                db_core.csv 
            Generates:
                db_core.db
        """
        raise NotImplementedError
#--------------------------------------------------

    def is_subscriber(self, addr):
        """
            Return True if addr is in email address list
            False otherwise
        """
        raise NotImplementedError
   
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
    def export_table(table, filename):
        """
            Provided:
            table: a string of a table name. (e.g. "db_core")

            Return:
            A csv file with its name corresponding to the table name
        """
        raise NotImplementedError

