"""
    Provided (with header, see example):
    email_list.csv          format: email_list
    deadline.csv            format: submission_id, date

    Generated:
    database.db
    
    Tables in database.db:
    email_list
    deadline
    num_review
    db_chain
"""


import csv, sqlite3, sys

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
        self.EMAIL_LIST = "email_list.csv"
        self.DEADLINE = "deadline.csv"
        # Database generated file:
        self.DATABASE = "database.db"
        # tables
        self.TB_EMAIL_LIST = "email_list"
        self.TB_DEADLINE = "deadline"
        self.TB_NUM_REVIEW = "num_review"
        self.TB_CHAIN = "chain"
        # Database constants:
        self.MAX_SUBMISSION = 6
        self.NUM_REVIEW_REQUEST = 3
        
#--------------------------------------------------
    def create_database(self):
        """ 
            ===This function can be called only on initialising database===
            This function further calls subsequent functions init_email_list, 
            init_deadline, init_num_review, init_chain to initialise tables
            email_list, deadline, num_review, and chain respectively.
        
            email_list: email address of subscribers
            deadline: submission ID, date
            num_review: currently number of received distribution for each submission 
            chain: a joined table
        """
        con = sqlite3.connect(self.DATABASE)
        self.init_email_list(con)
        self.init_deadline(con)
        self.init_num_review(con)
        self.init_chain(con)
        con.close()

    def init_email_list(self, con):
        """
            ===This function can be called only on initialising database===
            Provided:
                connection to database.db
                email_list.csv 
            Generates:
                email_list table in database.db
        """
        cur = con.cursor()
        cur.execute(f"CREATE TABLE '{self.TB_EMAIL_LIST}' (address text)")
        with open(self.EMAIL_LIST, encoding='utf-8-sig') as file:
            lines = file.read().splitlines()
        lines = [(line,) for line in lines]
        print(lines)
        cur.executemany(f"INSERT INTO '{self.TB_EMAIL_LIST}' (address) values (?)", lines)
        con.commit()

    def init_deadline(self, con):
        """
            ===This function can be called only on initialising database===
            Provided:
                connection to database.db
                deadline.csv
            Generates:
                deadline table in database.db
        """
        cur = con.cursor()
        cur.execute(f"CREATE TABLE '{self.TB_DEADLINE}' (submission_id integer, date text)")
        with open(self.DEADLINE, encoding='utf-8-sig') as file:
            lines = file.read().splitlines()
        lines = [(line,) for line in lines]
        cur.executemany(f"INSERT INTO '{self.TB_DEADLINE}' (submission_id, date) values (?, ?)"\
                        , lines)
        con.commit()

    def init_num_review(self, con):
        """
            ===This function can be called only on initialising database===
            Provided:
                connection to database.db
            Generates:
                num_review table in database.db
        """
        cur = con.cursor()
        cur.execute(f"SELECT * from {self.TB_EMAIL_LIST}")
        lines = cur.fetchall()
        lines = [(line, 0) for line in lines]
        cur.execute(f"CREATE TABLE '{self.TB_NUM_REVIEW}' (reviewer text, number integer)")
        cur.executemany(f"INSERT INTO '{self.TB_NUM_REVIEW}' (reviewer, number) values (?, ?)",\
                         lines)
        con.commit()

    def init_chain(self, con):
        """
            ===This function can be called only on initialising database===
            Provided:
                connection to database.db
            Generates:
                chain table in database.db
        """
        cur = con.cursor()
        cur.execute(f"SELECT * from {self.TB_EMAIL_LIST}")
        addresses = cur.fetchall()
        lines = []
        for addr in addresses:
            for subm_id in range(1, len(self.MAX_SUBMISSION) + 1):
                lines += [(addr, subm_id) + (None, 0) + (None,) * 6 + (None,) * 3]
        cur.execute(f"CREATE TABLE {self.TB_CHAIN} "+
        "(author text, subm_id integer, subm_received text, " +
        "'convo_id (review)' text, reviewer text, review_req_sent text, review_received text, " +
        "'convo_id (eval)' text, rating integer, comment text, eval_req_sent text, eval_received text"
        )
        cur.executemany(f"INSERT INTO '{self.TB_CHAIN}' " + 
        "(author, subm_id, subm_received, " +
        "'convo_id (review)', reviewer, review_req_sent, review_received" +
        "'convo_id (eval)', rating, comment, eval_req_sent, eval_received)" + 
        " values (" + ", ".join(['?'] * 11) + ")", lines)
        con.commit()


#--------------------------------------------------

    def is_subscriber(self, addr):
        """
            Return True if addr is in email address list
            False otherwise
        """
        con = sqlite3.connect(self.DATABASE)
        cur = con.cursor()
        print(f"SELECT * FROM '{self.TB_EMAIL_LIST}' where address = '{addr}'")
        sys.stdout.flush()
        cur.execute(f"SELECT * FROM '{self.TB_EMAIL_LIST}' where address = '{addr}'")
        result = cur.fetchall()
        print(result)
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


    def store_review(self, ):
        """
            Provided:

        """
        raise NotImplementedError

    def store_evaluation(self, ):
        """
            Provided:

        """
        raise NotImplementedError  

#--------------------------------------------------
    def export_table(self, table, filename):
        """
            Provided:
            table: a string of table name. (e.g. "db_chain")
            filename: a string of filename, where the table in database
                    will be exported to.

            Generates: A string of csv file name with its name corresponding to 
                the table name
            Return: True on success, False otherwise
        """
        try:
            con = sqlite3.connect(self.DATABASE)
            cur = con.cursor()
            cur.execute(f"SELECT * FROM '{table}'")
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

