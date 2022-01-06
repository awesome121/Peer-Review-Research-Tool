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
    chain
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
        self.DEADLINE_LST_MODIFIED_DATE = 0
        
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
        cur.execute(f"CREATE TABLE '{self.TB_DEADLINE}' (subm_id integer, date text)")
        with open(self.DEADLINE, encoding='utf-8-sig') as file:
            lines = file.read().splitlines()
        lines = [(line, '') for line in lines]
        cur.executemany(f"INSERT INTO '{self.TB_DEADLINE}' (subm_id, date) values (?, ?)"\
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
        lines = [(line[0], 0) for line in lines]
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
        # header 3 + 4 + 5
        cur.execute(f"CREATE TABLE {self.TB_CHAIN} "+\
        "('convo_id (subm)' text, author text, subm_id integer, subm_received text, " +\
        "'convo_id (review)' text, reviewer text, " + \
            "review_req_sent text, review_received text, " +\
        "'convo_id (eval)' text, rating integer, comment text, " + \
            "eval_req_sent text, eval_received text)")
        con.commit()


#--------------------------------------------------

    def is_subscriber(self, addr):
        """
            Return True if addr is in email address list
            False otherwise
        """
        con = sqlite3.connect(self.DATABASE)
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM '{self.TB_EMAIL_LIST}' WHERE address = '{addr}'")\
                    .fetchone()
        con.commit()
        con.close()
        return result is not None
   
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
        reviewers = []
        con = sqlite3.connect(self.DATABASE)
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

    def store_subm(self, subm_convo_id, author, subm_id, date):
        """
            Provided:
            subm_convo_id: submission conversation id
            author: a string of an author's email address
            subm_id: an integer of a submission id, e.g. 1, 2, 3
            date: a string of the date on receiving this submission

            Return:
            True on successfully storing
            False if it exists already
        """
        
        print('store_subm, subm convo id:', subm_convo_id)
        con = sqlite3.connect(self.DATABASE)
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
        "('convo_id (subm)', author, subm_id, subm_received, " +\
        "'convo_id (review)', reviewer, review_req_sent, review_received, " +\
        "'convo_id (eval)', rating, comment, eval_req_sent, eval_received)" +\
        f" values (?,?,?,?" + ", NULL" * 9 + ")",\
            (subm_convo_id, author, subm_id, date))
        con.commit()
        con.close()
        self.view_table_information('chain')
        return True

    def store_review_req(self, subm_convo_id, review_convo_id, reviewer, date_sent):
        """
            Provided:
            subm_convo_id: submission conversation id
            review_convo_id: initialised when review request was sent
            reviewer: a string of reviewer's email address to whom it's sent
            date_sent: a string of date on sending the review request
            
            Return:
            True on successfully storing
            False otherwise
        """
        print('store_review_req, subm convo id:', subm_convo_id)
        print('store_review_req, review convo id:', review_convo_id)
        self.view_table_information('chain')
        con = sqlite3.connect(self.DATABASE)
        cur = con.cursor()
        cur.execute(f""" UPDATE {self.TB_CHAIN} SET "convo_id (review)" = '{review_convo_id}', """ +\
                f""" reviewer = '{reviewer}', review_req_sent = '{date_sent}' """ +\
                f""" WHERE "convo_id (subm)" = '{subm_convo_id}' """)
        con.commit()
        con.close()
        self.view_table_information('chain')
        return True

    def store_review(self, review_convo_id, date_received):
        """
            Provided:
            review_convo_id: initialised when review request was sent
            date_received: a string of date on receiving the review
            
            Return:
            True on successfully storing
            False if it exists already
        """
        print('store_review, review convo id:', review_convo_id)
        con = sqlite3.connect(self.DATABASE)
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
            Provided:
            review_convo_id: submission conversation id
            eval_convo_id: evaluation conversation id
            date_sent: a string of date on sending the evaluation request
            
            Return:
            True on successfully storing
            False otherwise
        """
        print('store_eval_req, review convo id:', review_convo_id)
        print('store_eval_req, eval convo id:', eval_convo_id)
        con = sqlite3.connect(self.DATABASE)
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
            Provided:
            eval_convo_id: initialised when evaluation request was sent
            rating: integer, 1-7
            comment: string of author's comment
            date_received: a string of date on receiving the evaluation
            
            Return:
            True on successfully storing
            False if it exists already
        """
        print('store_eval, eval convo id:', eval_convo_id)
        con = sqlite3.connect(self.DATABASE)
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

    def find_author_by_convo_id(self, review_convo_id):
        """
            Provided:
                eval_convo_id: initialised when evaluation request was sent
            Return:
                author: a string of an author's email address
        """
        con = sqlite3.connect(self.DATABASE)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        author = cur.execute(f"SELECT author FROM {self.TB_CHAIN} WHERE " +\
                            f""" "convo_id (review)" = '{review_convo_id}' """)\
                    .fetchone()['author']
        return author
        
        
#--------------------------------------------------
    def view_table_information(self, table_name):
        """
            A function used to view table's information
        
        """
        con = sqlite3.connect(self.DATABASE)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        result = cur.fetchall()
        print(result)
        con.close()
        return 


#--------------------------------------------------
    def export_table(self, table, filename):
        """
            Provided:
            table: a string of table name. (e.g. "chain")
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
            con.commit()
            con.close()
        except:
            con.commit()
            con.close()
            return False
        return True

