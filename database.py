"""
    Provided (with header, see example):
        email_list.csv          format(columns): email_list
        schedule.csv            format(columns): submission_id, date

    Generated:
        database.db
    
    Tables in database.db:
        email_list
        schedule
        num_review
        chain
"""


import csv, sqlite3, sys, os
from socket import timeout
from time import time

class Database:
    """
        Database class, this class is expected to run continously for weeks.
        This class handles internal database tables using sqlite3, it interacts
        with Mailhandler class.
    """
    def __init__(self):
        """
            Set constant file names and parameters
        """
        # Database generated file:
        self.DATABASE = "database.db"
        # tables
        self.TB_EMAIL_LIST = "email_list"
        self.TB_SCHEDULE = "schedule"
        self.TB_NUM_REVIEW = "num_review"
        self.TB_CHAIN = "chain"
        self.TB_CONNECTION = "connection"
        # Database constants:
        self.CON_TIMEOUT = 60 # seconds
        self.MAX_SUBMISSION = 6
        self.NUM_REVIEW_REQUEST = 3
        self.SCHEDULE_LST_MODIFIED_DATE = 0
        self.EMAIL_LST_MODIFIED_DATE = 0
        
#--------------------------------------------------
    def create_database(self):
        """ 
            ===This function can be called only on initialising database===
            This function further calls subsequent functions init_email_list, 
            init_schedule, init_num_review, init_chain to initialise tables
            email_list, schedule, num_review, and chain respectively.

            Resourses (Provided by the user):
                email_list: email address of subscribers
            Tables (Generated):
                schedule: subm_id, start_date, end_date (subm), is_distributed, 
                        end_date (review), end_date (eval)
                num_review: currently number of received distribution for each submission 
                chain: a joined table
        """
        # Establish a connection
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        # Init tables (Create tables and Insert data)
        self.init_email_list(con)
        self.init_schedule(con)
        self.init_num_review(con)
        self.init_chain(con)
        con.close()

    def init_email_list(self, con):
        """
            ===This function can be called only on initialising database===
            Param:
                connection to database.db
                email_list.csv 
            Generates:
                email_list table in database.db
        """
        cur = con.cursor()
        cur.execute(f"CREATE TABLE '{self.TB_EMAIL_LIST}' (address text)")
        con.commit()

    def init_schedule(self, con):
        """
            ===This function can be called only on initialising database===
            Param:
                connection to database.db
                schedule.csv
            Generates:
                schedule table in database.db
        """
        cur = con.cursor()
        cur.execute(f"CREATE TABLE '{self.TB_SCHEDULE}' (subm_id integer, " +\
            "start_date text, 'end_date (subm)' text, is_distributed integer, " +\
            "'end_date (review)' text, 'end_date (eval)' text)")
        con.commit()

    def init_num_review(self, con):
        """
            ===This function can be called only on initialising database===
            Param:
                connection to database.db
            Generates:
                num_review table in database.db
        """
        cur = con.cursor()
        cur.execute(f"SELECT * from {self.TB_EMAIL_LIST}")
        lines = cur.fetchall()
        lines = [(line[0], 0) for line in lines]
        cur.execute(f"CREATE TABLE '{self.TB_NUM_REVIEW}' (reviewer text, number integer)")
        cur.executemany(f"INSERT INTO '{self.TB_NUM_REVIEW}' (reviewer, number) values (?, ?)",\
                         lines)
        con.commit()

    def init_chain(self, con):
        """
            ===This function can be called only on initialising database===
            Param:
                connection to database.db
            Generates:
                chain table in database.db
        """
        cur = con.cursor()
        # header 3 + 4 + 5
        cur.execute(f"CREATE TABLE {self.TB_CHAIN} "+\
        "('msg_id (subm)' text, author text, subm_id integer, subm_received text, " +\
        "'convo_id (review)' text, reviewer text, " + \
            "review_req_sent text, review_received text, " +\
        "'convo_id (eval)' text, rating integer, comment text, " + \
            "eval_req_sent text, eval_received text)")
        con.commit()

    def init_connection(self, con):
        """
           ===This function can be called only on initialising database===
            Param:
                connection to database.db
            Generates:
                connection history table in database.db
        """
        cur = con.cursor()
        cur.execute(f"CREATE TABLE {self.TB_CONNECTION} " + "start_date integer, end_date integer")
        con.commit()

#--------------------------------------------------
    def update_email_list(self, input_csv_file):
        """
        Provided:
            A csv file which contains a list of email.
        Output:
            Updated email list table
        """
        # Establish a connection
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        # Get the cursor
        cur = con.cursor()
        with open(input_csv_file, encoding='utf-8-sig') as file:
            lines = file.read().splitlines()
        lines = [(line,) for line in lines]
        cur.executemany(f"INSERT INTO '{self.TB_EMAIL_LIST}' (address) values (?)", lines)
        con.commit()
        con.close()

    def update_schedule(self, subm_id, start_date, end_date, end_date_review, end_date_eval):
        # Establish a connection
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        # Get the cursor
        cur = con.cursor()

        cur.execute(f"INSERT INTO '{self.TB_SCHEDULE}' (subm_id, start_date, " +\
                        " 'end_date (subm)', is_distributed, 'end_date (review)'," +\
                        " 'end_date (eval)') values (?, ?, ?, 0, ?, ?)", (subm_id,\
                             start_date, end_date, end_date_review, end_date_eval))
        con.commit()
        con.close()

    def update_connection(self):
        # Establish a connection
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        # Get the cursor
        cur = con.cursor()

        cur.execute(f"UPDATE '{self.TB_CONNECTION}' (subm_id, start_date, " +\
                        " 'end_date (subm)', is_distributed, 'end_date (review)'," +\
                        " 'end_date (eval)') values (?, ?, ?, 0, ?, ?)", )
        con.commit()
        con.close()

    def monitor_schedule(self):
        """
            This function will constantly monitoring schedule.csv.
            If schedule.csv has been changed, update_schedule will be called.
            If there is a submission deadline due, distibute submissions.
        """
        # If the last modified date has been changed.
        if os.path.getmtime(self.SCHEDULE) != self.SCHEDULE_LST_MODIFIED_DATE:
            # Update self.TB_EMAIL_LIST
            self.update_schedule()
            # Store the lastest last modified date
            self.SCHEDULE_LST_MODIFIED_DATE = os.path.getmtime(self.SCHEDULE)
        # if there is a submission deadline due:
        # return subm_id
        # else:
        #     return -1
            
    def get_subscriber_total(self):
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT COUNT(*) from '{self.TB_EMAIL_LIST}'").fetchone()
        con.commit()
        con.close()
        # result is a list of tuples, the tuples are columns corresponds to the header
        count = result[0][0]
        return count

    def is_subscriber(self, addr):
        """
            Return True if addr is in email address list
            False otherwise.
            Param:
                addr: a string that representing an email address
            Return:
                True or False (boolean)
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM '{self.TB_EMAIL_LIST}' WHERE address = '{addr}'")\
                    .fetchone()
        con.commit()
        con.close()
        return result is not None

    def draw_authors(self, subm_id):
        """
            Param:
                subm_id: an integer of submission id
            Return:
                a list of tuples ('author', 'msg_id (subm)') whose submission 
                needs to be distributed
        """
        raise NotImplementedError
   
    def draw_reviewers(self, author):
        """
            Randomly draw three reviewers (except this auther),
            a reviewer can only review maximum 3 different 
            submissions, finally increment their num of 
            reviews in num_review.db.
            Param:
                author: a string of an author's email address 
            Return:
                a list of reviewers' email addresses
        """
        reviewers = []
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        # Reviewer who has lowest number of work will have highest priority
        # number = 0
        reviewers += cur.execute(f"SELECT reviewer FROM '{self.TB_NUM_REVIEW}' " +\
            f"WHERE number < 3 and reviewer != '{author}' and number = 0 ORDER BY RANDOM() LIMIT 3").fetchall()
        # number = 1
        reviewers += cur.execute(f"SELECT reviewer FROM '{self.TB_NUM_REVIEW}' " +\
            f"WHERE number < 3 and reviewer != '{author}' and number = 1 ORDER BY RANDOM() LIMIT 3").fetchall()
        # number = 2
        reviewers += cur.execute(f"SELECT reviewer FROM '{self.TB_NUM_REVIEW}' " +\
            f"WHERE number < 3 and reviewer != '{author}' and number = 2 ORDER BY RANDOM() LIMIT 3").fetchall()
        if len(reviewers) > 3:
            reviewers = reviewers[0:3]
        cur.executemany(f"UPDATE {self.TB_NUM_REVIEW} SET number = number + 1 WHERE reviewer = (?)", reviewers)
        con.commit()
        con.close()
        return reviewers

    def store_subm(self, subm_msg_id, author, subm_id, date):
        """
            Param:
                subm_msg_id: submission message id
                author: a string of an author's email address
                subm_id: an integer of a submission id, e.g. 1, 2, 3
                date: a string of the date on receiving this submission
            Return:
                True on successfully storing
                False if it exists already
        """
        
        print('store_subm, subm msg id:', subm_msg_id)
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        print(f"SELECT * FROM {self.TB_CHAIN} " +\
            f"WHERE author = '{author}' AND subm_id = {subm_id}")
        result = cur.execute(f"SELECT * FROM {self.TB_CHAIN} "+\
                            f"WHERE author = '{author}' AND subm_id = {subm_id}")\
                    .fetchone()
        if result is not None: # already exists
            con.commit()
            con.close()
            return False
        cur.execute(f"INSERT INTO {self.TB_CHAIN} " +\
        "('msg_id (subm)', author, subm_id, subm_received, " +\
        "'convo_id (review)', reviewer, review_req_sent, review_received, " +\
        "'convo_id (eval)', rating, comment, eval_req_sent, eval_received)" +\
        f" values (?,?,?,?" + ", NULL" * 9 + ")",\
            (subm_msg_id, author, subm_id, date))
        con.commit()
        con.close()
        self.view_table_information('chain')
        return True

    def store_review_req(self, subm_msg_id, review_convo_id, reviewer, date_sent):
        """
            Param:
                subm_msg_id: submission message id
                review_convo_id: initialised when review request was sent
                reviewer: a string of reviewer's email address to whom it's sent
                date_sent: a string of date on sending the review request
            Return:
                True on successfully storing
                False otherwise
        """
        print('store_review_req, subm convo id:', subm_msg_id)
        print('store_review_req, review convo id:', review_convo_id)
        self.view_table_information('chain')
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        cur.execute(f""" UPDATE {self.TB_CHAIN} SET "convo_id (review)" = '{review_convo_id}', """ +\
                f""" reviewer = '{reviewer}', review_req_sent = '{date_sent}' """ +\
                f""" WHERE "msg_id (subm)" = '{subm_msg_id}' """)
        con.commit()
        con.close()
        self.view_table_information('chain')
        return True

    def store_review(self, review_convo_id, date_received):
        """
            Param:
                review_convo_id: initialised when review request was sent
                date_received: a string of date on receiving the review
            Return:
                True on successfully storing
                False if it exists already
        """
        print('store_review, review convo id:', review_convo_id)
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        result = cur.execute(f""" SELECT * FROM {self.TB_CHAIN} WHERE """ +\
                        f""" "convo_id (review)" = '{review_convo_id}' """)\
                    .fetchone()
        if result['review_received'] is not None: # review_received exists
            con.commit()
            con.close()
            return False
        cur.execute(f""" UPDATE {self.TB_CHAIN} SET review_received = '{date_received}' """ +\
            f""" WHERE "convo_id (review)" = '{review_convo_id}' """)
        con.commit()
        con.close()
        self.view_table_information('chain')
        return True
        

    def store_eval_req(self, review_convo_id, eval_convo_id, date_sent):
        """
            Param:
                review_convo_id: submission conversation id
                eval_convo_id: evaluation conversation id
                date_sent: a string of date on sending the evaluation request
            Return:
                True on successfully storing
                False otherwise
        """
        print('store_eval_req, review convo id:', review_convo_id)
        print('store_eval_req, eval convo id:', eval_convo_id)
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        cur.execute(f""" UPDATE {self.TB_CHAIN} SET "eval_req_sent" = '{date_sent}', """ +\
                f""" "convo_id (eval)" = '{eval_convo_id}' """ +\
                f""" WHERE "convo_id (review)" = '{review_convo_id}' """)
        con.commit()
        con.close()
        self.view_table_information('chain')
        return True

    def store_eval(self, eval_convo_id, rating, comment, date_received):
        """
            Param:
                eval_convo_id: initialised when evaluation request was sent
                rating: integer, 1-7
                comment: string of author's comment
                date_received: a string of date on receiving the evaluation
            Return:
                True on successfully storing
                False if it exists already
        """
        print('store_eval, eval convo id:', eval_convo_id)
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM {self.TB_CHAIN} WHERE " +\
                            f""" "convo_id (eval)" = '{eval_convo_id}' """)\
                    .fetchone()
        if result['eval_received'] is not None: # eval_received exists
            con.commit()
            con.close()
            return False
        cur.execute(f""" UPDATE {self.TB_CHAIN} SET rating = {int(rating)}, comment = '{comment}', """+\
            f"eval_received = '{date_received}' " +\
            f""" WHERE "convo_id (eval)" = '{eval_convo_id}' """)
        con.commit()      
        con.close()
        self.view_table_information('chain')
        return True

    def get_author_by_convo_id(self, review_convo_id):
        """
            Param:
                eval_convo_id: initialised when evaluation request was sent
            Return:
                author: a string of an author's email address
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        author = cur.execute(f"SELECT author FROM {self.TB_CHAIN} WHERE " +\
                            f""" "convo_id (review)" = '{review_convo_id}' """)\
                    .fetchone()['author']
        return author

    def get_num_item_by_id(self, subm_id, item):
        """
            Param:
                subm_id: a string of submission id
                item: a string, can be submission, review, evaluation
            Return:
                an integer, the number of submission/review/evaluation
                corresponding to subm_id
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        if item == 'submission':
            result = cur.execute(f"SELECT COUNT(*) FROM {self.TB_CHAIN} WHERE subm_id = {subm_id}")\
                                .fetch()
        elif item == 'review':
            result = cur.execute(f"SELECT COUNT(*) FROM {self.TB_CHAIN} WHERE subm_id = {subm_id} " +\
                                "AND review_received != NULL").fetch()
        elif item == 'evaluation':
            result = cur.execute(f"SELECT COUNT(*) FROM {self.TB_CHAIN} WHERE subm_id = {subm_id} " +\
                                "AND eval_received != NULL").fetch()
        else:
            print("ERROR, UNEXPECTED ITEM")
        con.commit()
        con.close()
        # result is a list of tuples, the tuples are columns corresponds to the header
        count = result[0][0]
        return count
        
        
#--------------------------------------------------
    def view_table_information(self, table_name):
        """
            A function used to view table's information
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        result = cur.fetchall()
        print(result)
        con.close()


#--------------------------------------------------
    def export_table(self, table, filename):
        """
            Param:
                table: a string of table name. (e.g. "chain")
                filename: a string of filename, where the table in database
                        will be exported to.
            Generates: 
                A string of csv file name with its name corresponding to 
                the table name
            Return:
                True on success, False otherwise
        """
        try:
            con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
            cur = con.cursor()
            cur.execute(f"SELECT * FROM '{table}'")
            result = cur.fetchall()
            with open(filename, 'wb') as file:
                writer = csv.writer(file)
                header = [description[0] for description in cur.description]
                writer.writerow(header)
                writer.writerows(result)
            con.commit()
            con.close()
        except:
            con.commit()
            con.close()
            return False
        return True

