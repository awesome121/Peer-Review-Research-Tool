"""
    Database class only generates a single database file:
        database.db
    
    Tables in database.db:
        email_list
        submission
        schedule
        chain
        connection
        
    Please see table initialization for details
"""

import csv, sqlite3, time

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
        self.TB_SUBMISSION = "submission"
        self.TB_SCHEDULE = "schedule"
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
            init_schedule, init_chain to initialise tables
            email_list, schedule, and chain respectively.

            Resourses (Provided by the user):
                email_list: email address of subscribers
            Tables (Generated):
                schedule: subm_id, start_date, end_date (subm), is_distributed, 
                        end_date (review), end_date (eval)
                chain: a joined table
        """
        # Establish a connection
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        # Init tables (Create tables and Insert data)
        self.init_email_list(con)
        self.init_submission(con)
        self.init_schedule(con)
        self.init_chain(con)
        self.init_connection(con)
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

    def init_submission(self, con):
        """
            ===This function can be called only on initialising database===
            Param:
                connection to database.db 
            Generates:
                email_list table in database.db
        """
        cur = con.cursor()
        cur.execute(f"CREATE TABLE {self.TB_SUBMISSION} ('msg_id (subm)' text,\
                    author text, subm_id integer, subm_received text, num_review integer)")
        con.commit()

    def init_schedule(self, con):
        """
            ===This function can be called only on initialising database===
            Param:
                connection to database.db
            Generates:
                schedule table in database.db
        """
        cur = con.cursor()
        cur.execute(f"CREATE TABLE '{self.TB_SCHEDULE}' (subm_id integer, " +\
            "start_date integer, 'end_date (subm)' integer, is_distributed integer, " +\
            "'end_date (review)' integer, 'end_date (eval)' integer)")
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
        cur.execute(f"CREATE TABLE {self.TB_CONNECTION} (start_date integer, end_date integer)")
        con.commit()

#--------------------------------------------------
    def update_email_list(self, input_csv_file):
        """
            This function takes the email addresses in a csv file,
            inserts them into database, if it's new, it will be added.
            if it already exists, nothing changes. 
            Param:
                input_csv_file: A csv file which contains a list of email.
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        with open(input_csv_file, encoding='utf-8-sig') as file:
            lines = file.read().splitlines()
        lines = [(line,) for line in lines]
        cur.executemany(f"INSERT OR REPLACE INTO '{self.TB_EMAIL_LIST}' (address) values (?)",\
                        lines)
        con.commit()
        con.close()

    def update_connection(self, start_date, end_date):
        """
            This function is used to update an existing connection
            Param:
                start_date: start date of this connection
                end_date: most recent date of this connection
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        cur.execute(f"UPDATE {self.TB_CONNECTION} SET end_date = {end_date} \
                    WHERE start_date = {start_date}")
        con.commit()
        con.close()

    def update_schedule(self, subm_id, subm_start, subm_deadline, \
                                        review_deadline, eval_deadline):
        """
            This function is used to update an existing schedule
            Param:
                subm_id: an integer of submission id
                subm_start: an integer (unixstamp), submission start date
                subm_deadline: an integer (unixstamp), submission deadline
                review_deadline: an integer (unixstamp), review deadline
                eval_deadline: an integer (unixstamp), evaluation deadline
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        cur.execute(f"UPDATE {self.TB_SCHEDULE} SET start_date = {subm_start} \
                        ,'end_date (subm)' = {subm_deadline}, 'end_date (review)'\
                         = {review_deadline}, 'end_date (eval)' = {eval_deadline}\
                     WHERE subm_id = {subm_id}")
        con.commit()
        con.close()
            
    def store_connection(self, start_date):
        """
            This function is used to store a connection
            Param:
                start_date: start date of this new connection
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        cur.execute(f"INSERT INTO {self.TB_CONNECTION} (start_date, end_date) \
                    values (?, ?)", (start_date, start_date))
        con.commit()
        con.close()

    def store_schedule(self, subm_id, subm_start, subm_deadline, review_deadline, eval_deadline):
        """
            This function is used to store a new schedule
            Param:
                subm_id: an integer of submission id
                subm_start: an integer (unixstamp), submission start date
                subm_deadline: an integer (unixstamp), submission deadline
                review_deadline: an integer (unixstamp), review deadline
                eval_deadline: an integer (unixstamp), evaluation deadline
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        cur.execute(f"INSERT INTO '{self.TB_SCHEDULE}' (subm_id, start_date, " +\
                        " 'end_date (subm)', is_distributed, 'end_date (review)'," +\
                        " 'end_date (eval)') values (?, ?, ?, 0, ?, ?)", (subm_id,\
                             subm_start, subm_deadline, review_deadline, eval_deadline))
        con.commit()
        con.close()

    def store_subm(self, msg_id, author, subm_id, subm_received):
        """
            Param:
                author: a string of an author's email address
                subm_id: an integer of a submission id, e.g. 1, 2, 3
                subm_received: a string of the date on receiving this submission
            Return:
                True on successfully storing
                False if it exists already
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM {self.TB_SUBMISSION} "+\
                            f"WHERE author = '{author}' AND subm_id = {subm_id}")\
                    .fetchone()
        if result is not None: # already exists
            con.close()
            return False
        else:
            cur.execute(f"INSERT INTO {self.TB_SUBMISSION} ('msg_id (subm)', author, subm_id, subm_received,\
                         num_review) values (?, ?, ?, ?, 0)", (msg_id, author, subm_id, subm_received))
            con.commit()
            con.close()
            return True

    def store_review_req(self, msg_id, author, subm_id, subm_received, review_convo_id, reviewer, date_sent):
        """
            Param:
                msg_id: submission message id
                author: a string of email address
                subm_id: an integer of submission id
                subm_received: a string of date
                review_convo_id: initialised when review request was sent
                reviewer: a string of reviewer's email address to whom it's sent
                date_sent: a string of date on sending the review request
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"INSERT INTO {self.TB_CHAIN} ('msg_id (subm)', author, subm_id, subm_received, 'convo_id (review)',\
                    reviewer, review_req_sent, review_received, 'convo_id (eval)', rating, comment,\
                    eval_req_sent, eval_received) values (?,?,?,?,?,?,?" + ", NULL" * 6 + ")",\
                    (msg_id, author, subm_id, subm_received, review_convo_id, reviewer, date_sent))
        con.commit()
        con.close()

    def store_review(self, review_convo_id, date_received):
        """
            Param:
                review_convo_id: initialised when review request was sent
                date_received: a string of date on receiving the review
            Return:
                True on successfully storing
                False if it exists already
        """
        print("store review:\nreview_convo_id:", review_convo_id)
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        result = cur.execute(f""" SELECT * FROM {self.TB_CHAIN} WHERE """ +\
                        f""" "convo_id (review)" = '{review_convo_id}' """)\
                    .fetchone()
        print(result)
        if result['review_received'] is not None: # review_received exists
            con.commit()
            con.close()
            return False
        cur.execute(f""" UPDATE {self.TB_CHAIN} SET review_received = '{date_received}' """ +\
            f""" WHERE "convo_id (review)" = '{review_convo_id}' """)
        con.commit()
        con.close()
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
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        cur.execute(f""" UPDATE {self.TB_CHAIN} SET "eval_req_sent" = '{date_sent}', """ +\
                f""" "convo_id (eval)" = '{eval_convo_id}' """ +\
                f""" WHERE "convo_id (review)" = '{review_convo_id}' """)
        con.commit()
        con.close()
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
        # print('store_eval, eval convo id:', eval_convo_id)
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
        # self.view_table_information('chain')
        return True

    #==================================================
    def get_author_by_prefix(self, prefix):
        """
            Param:
                prefix: beginning string of a student's email address
            Return:
                A list of email addresses matched by 'prefix'
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM {self.TB_EMAIL_LIST} WHERE address LIKE '{prefix}%'")\
                        .fetchall()
        con.close()
        result = [item[0] for item in result]
        return result

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

    def get_undistributed_subm_id(self):
        """
            Get undistributed submission id and mark it as distributed
            Return:
                subm_id: the marked submission id, None if it doesn't exist
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        subm_id = cur.execute(f"SELECT subm_id FROM {self.TB_SCHEDULE} WHERE "+\
                 f"""is_distributed = 0 AND {int(time.time())} >= "end_date (subm)" """+\
                        " ORDER BY subm_id ").fetchone()
        if subm_id:
            subm_id = subm_id[0]
            cur.execute(f"UPDATE {self.TB_SCHEDULE} SET is_distributed = 1 WHERE"+\
                        f" subm_id = {subm_id}")
            con.commit()
        con.close()
        return subm_id

    def get_subms_by_id(self, subm_id):
        """
            Param:
                subm_id: an integer of submission id
            Return:
                a list of tuples ('msg_id', 'author', subm_id, subm_received)
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM {self.TB_SUBMISSION} WHERE subm_id = {subm_id}")\
                    .fetchall()
        return result

    def get_subm_by_author(self, author):
        """
            Param:
                author: student's email address
            Return:
                A list of (subm_id, subm_received) matched by this author
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT subm_id, subm_received FROM {self.TB_SUBMISSION}\
                             WHERE author = '{author}' ORDER BY subm_id")\
                            .fetchall()
        con.close()
        return result
    
    def get_reviewers_by_subm(self, author, subm):
        """
            Param:
                author: student's email address
                subm: submission id
            Return:
                A list of tuples which contains reviewers and date
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT reviewer, review_received FROM {self.TB_CHAIN} WHERE author = '{author}'\
                     and subm_id = '{subm}'")\
                        .fetchall()
        con.close()
        return result
    
    def get_other_reviewers_by_subm(self, author, subm_id, except_):
        """
            Param:
                author: student's email address
                subm_id: submission id
            Return:
                A list of tuples which contains 'reviewer', 'review_received', 'rating'
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT reviewer, rating, review_received FROM {self.TB_CHAIN}"+\
                f" WHERE author = '{author}' and subm_id = '{subm_id}' and reviewer != '{except_}'")\
                        .fetchall()
        con.close()
        return result
   
    def get_reviews_by_reviewer(self, reviewer):
        """
            Param:
                reviewer: student's email address
            Return:
                A list of tuples which contains 'authors', 'subm_id', 'reviewed date' and 'rating'
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT author, subm_id, review_received, rating FROM {self.TB_CHAIN}"+\
                        f" WHERE reviewer = '{reviewer}'")\
                        .fetchall()
        con.close()
        return result

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
    
    def get_subscriber_total(self):
        """
            Return an integer, the number of subscribers in email list.
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT COUNT(*) from '{self.TB_EMAIL_LIST}'").fetchone()
        con.commit()
        con.close()
        # result is a list of tuples, the tuples are columns corresponds to the header
        count = result[0][0]
        return count
    
    def get_all_email_addr(self):
        """
            Return a list of all email addresses in database
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM {self.TB_EMAIL_LIST}").fetchall()
        con.close()
        result = [item[0] for item in result]
        return result

    def get_schedule(self, subm_id=None):
        """
            Param:
                subm_id: If given, return a specific schedule, otherwise return all schedules
            Return:
                A list of tuples of (subm_id, subm start date, subm_deadline, is_distributed
                review_deadline, eval_deadline)
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        if subm_id:
            result = cur.execute(f"SELECT * FROM {self.TB_SCHEDULE} WHERE subm_id = {subm_id}").fetchone()
        else:
            result = cur.execute(f"SELECT * FROM {self.TB_SCHEDULE} ORDER BY subm_id").fetchall()
        con.close()
        return result

    def get_last_conn(self):
        """
            Return the last connection (start_date, end_date)
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM {self.TB_CONNECTION} ORDER BY start_date DESC").fetchone()
        con.close()
        if result is None:
            return None, None
        return result
 #=================================================

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

    def draw_reviewers(self, author):
        """
            Randomly draw three reviewers (except this auther),
            a reviewer can only review maximum 3 different 
            submissions, finally increment their num of 
            reviews in submission table.
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
        reviewers += cur.execute(f"SELECT author FROM '{self.TB_SUBMISSION}' " +\
            f"WHERE num_review < 3 and author != '{author}' and num_review = 0 ORDER BY RANDOM() LIMIT 3").fetchall()
        # number = 1
        reviewers += cur.execute(f"SELECT author FROM '{self.TB_SUBMISSION}' " +\
            f"WHERE num_review < 3 and author != '{author}' and num_review = 1 ORDER BY RANDOM() LIMIT 3").fetchall()
        # number = 2
        reviewers += cur.execute(f"SELECT author FROM '{self.TB_SUBMISSION}' " +\
            f"WHERE num_review < 3 and author != '{author}' and num_review = 2 ORDER BY RANDOM() LIMIT 3").fetchall()
        if len(reviewers) > 3:
            reviewers = reviewers[0:3]
        cur.executemany(f"UPDATE {self.TB_SUBMISSION} SET num_review = num_review + 1 WHERE author = (?)", reviewers)
        con.commit()
        con.close()
        reviewers = [reviewer[0] for reviewer in reviewers]
        return reviewers

    def add_addr(self, addr):
        """
            Param:
                addr: a student's email address
            Return:
                True if successfully inserted, False otherwise
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM {self.TB_EMAIL_LIST} WHERE address = '{addr}'")\
                            .fetchall()
        result = [item[0] for item in result]
        if result:
            con.close()
            return False
        else:
            result = cur.execute(f"INSERT INTO {self.TB_EMAIL_LIST} (address) values ('{addr}')")
            con.commit()
            con.close()
            return True

    def remove_email_addr(self, addresses):
        """
            Param: 
                addresses: a list of email addresses
            This function removes a list of email addresses
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        for addr in addresses:
            cur.execute(f"DELETE FROM {self.TB_EMAIL_LIST} WHERE address = '{addr}' ")
        con.commit()
        con.close()

    def remove_schedule(self, subm_id):
        """
            Param: 
                subm_id: submission id
            This function removes a schedule with subm_id
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        cur.execute(f"DELETE FROM {self.TB_SCHEDULE} WHERE subm_id = {subm_id}")
        con.commit()
        con.close()

    def exist_schedule(self, subm_id):
        """
            Param: 
                subm_id: submission id
            Return:
                True if a schedule with subm_id exists, False otherwise 
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT COUNT(*) FROM {self.TB_SCHEDULE} WHERE subm_id = {subm_id}")\
                                .fetchone()
        con.close()
        count = result[0]
        return count == 1
        

    def is_subm_distributed(self, subm_id):
        """
            Param: 
                subm_id: submission id
            Return:
                True if subm_id was distributed, False otherwise 
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        result = cur.execute(f"SELECT is_distributed FROM {self.TB_SCHEDULE} \
                        WHERE subm_id = {subm_id}").fetchone()[0]
        con.close()
        return result == 1

    def is_subm_started(self, subm_id):
        """
            Param: 
                subm_id: submission id
            Return:
                True if subm_id has started, False otherwise 
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        subm_start_date = cur.execute(f'SELECT start_date FROM {self.TB_SCHEDULE} WHERE subm_id = {subm_id}').fetchone()[0]
        con.commit()
        con.close()
        return time.time() > subm_start_date
    
    def is_subm_end(self, subm_id):
        """
            Param: 
                subm_id: submission id
            Return:
                True if subm_id has ended, False otherwise 
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        subm_end_date = cur.execute(f'SELECT "end_date (subm)" FROM {self.TB_SCHEDULE} WHERE subm_id = {subm_id}').fetchone()[0]
        con.commit()
        con.close()
        return time.time() > subm_end_date

    def is_review_end(self, subm_id):
        """
            Param: 
                subm_id: submission id
            Return:
                True if review of subm_id has ended, False otherwise 
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        review_end_date = cur.execute(f'SELECT "end_date (review)" FROM {self.TB_SCHEDULE} WHERE subm_id = {subm_id}').fetchone()[0]
        con.commit()
        con.close()
        return time.time() > review_end_date

    def is_eval_end(self, subm_id):
        """
            Param: 
                subm_id: submission id
            Return:
                True if evaluation of subm_id has ended, False otherwise 
        """
        con = sqlite3.connect(self.DATABASE, timeout=self.CON_TIMEOUT)
        cur = con.cursor()
        eval_end_date = cur.execute(f'SELECT "end_date (eval)" FROM {self.TB_SCHEDULE} WHERE subm_id = {subm_id}').fetchone()[0]
        con.commit()
        con.close()
        return time.time() > eval_end_date

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

