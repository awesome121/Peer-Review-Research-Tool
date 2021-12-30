
import csv

class Database:
    def __init__(self):
        self.DATABASE = "db_core.csv"
        self.ADDRESS_FILE = "address_list.csv"
        self.NUM_REVIEW_FILE = "num_review.csv"
        self.max_submission = 6

        self.NUM_REVIEW_REQUEST = 3

    def create_database():
        """ subscriber.db: email address of subscribers
            db_core.db: a joined table
            num_review.db: currently number of received distribution for each submission
        """
        # addr_list = get_addr_list(NUM_REVIEW_FILE)

        # core = open(DATABASE, 'w', encoding='utf-8-sig')
        # core.write("{},{},{},{},{},{},{},{},{},{},{}\n".format('Author', 'Submission ID', \
        #     'Date Received (Submission)', 'Date Distributed', 'Reviewer', \
        #         'Distribution ID', 'Date Received (Review)', 'evaluation ID', \
        #             'Date Received (evaluation)', 'evaluation', 'Comment'))
        
        # for addr in addr_list:
        #     for submission_id in range(1, self.max_submission+1):
        #         for _ in range(NUM_REVIEW_REQUEST):
        #             core.write(f"{addr},{submission_id}" + "," * 9 + "\n")
        # core.close()
        # init_num_review(addr_list)
        raise NotImplementedError

    def init_num_review(addr_list):
        # num_review_file = open(NUM_REVIEW_FILE, 'w', encoding='utf-8-sig')
        # num_review_file.write('Reviewer,' + ','.join(\
        #     [f'Submission {i}' for i in range(1, self.max_submission+1)]) + '\n')
        # for addr in addr_list:
        #     num_review_file.write(f"{addr}," + ','.join(\
        #     [f'0' for i in range(self.max_submission)]) + '\n')
        # num_review_file.close()
        raise NotImplementedError



    def get_addr_list(addr_file):
        """parse text, return a list of addresses"""
        # addr_file = open(ADDRESS_FILE, encoding='utf-8-sig')
        # addr_list = addr_file.read().splitlines()
        # addr_file.close()
        return addr_list

    #-----------------------------------


    def is_subscriber(self, addr):
        """Return True if the address is in address list"""
        return True
        # file = open(ADDRESS_FILE, encoding='utf-8-sig')
        # lines = file.read().splitlines()
        # file.close()
        # for line in lines:
        #     if line.strip() == addr:
        #         return True
        # return False

    def find_author_by_dist_id(dist_id):
        """Return original author corresponding to this hash value
        return None if author not find
        """
        # file = open(DATABASE, encoding='utf-8-sig')
        # reader = csv.DictReader(file)
        # for row in reader:
        #     if row['Distribution ID'] == dist_id:
        #         file.close()
        #         return row['Author']
        # file.close()

    def draw_reviewers(author):
        """draw three reviewers and increment their num of reviews"""
        return ['cgo54@uclive.ac.nz']

    def store_submission_by_dist_id(author, submission_id, date_on_submit,\
                date_on_dist, reviewer, dist_id):
        """store submission into the (author, submission) entry
        return True on success, False otherwise
        """
        # is_stored = False
        # if ',' in date_on_submit:
        #     date_on_submit = date_on_submit.split(',')[1] 
        # with open(DATABASE, 'r', encoding='utf-8-sig') as file:
        #     rows = file.read().splitlines()
        # for i in range(len(rows)):
        #     row = rows[i].split(',')
        #     if author in row[0] and row[1] == submission_id \
        #         and not row[5]: # not existing dist id
        #         row[2:6] = [date_on_submit, date_on_dist, reviewer, dist_id]
        #         rows[i] = ','.join(row[:])
        #         is_stored = True
        #         print('1')
        #         break
        #     else:
        #         print(2)
        # with open(DATABASE, 'w', encoding='utf-8-sig') as file:
        #     file.write('\n'.join(rows)+'\n')
        return is_stored


    def store_evaluation_by_evaluation_id(author, evaluation_id, date_on_rate, evaluation, comment):
        """store evaluation into the (author, submission) entry
        return True on success, False otherwise
        """
        is_stored = False
        if ',' in date_on_rate:
            date_on_rate = date_on_rate.split(',')[1] 
        with open(DATABASE, 'r', encoding='utf-8-sig') as file:
            rows = file.read().splitlines()
        for i in range(len(rows)):
            row = rows[i].split(',')
            if author in row[0] and row[7] == evaluation_id:
                row[8:11] = [date_on_rate, evaluation, comment]
                print(date_on_rate, evaluation)
                rows[i] = ','.join(row[:])
                is_stored = True
                print(1)
                break
            else:
                print(2)
        with open(DATABASE, 'w', encoding='utf-8-sig') as file:
            file.write('\n'.join(rows)+'\n')
        return is_stored
    #create_database()