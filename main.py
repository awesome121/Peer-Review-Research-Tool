import os, time
from database import Database
from mail_parser import MailParser
from mail_handler import MailHandler
# os.system("rm database.db")
# db.create_database()




mail_handler = MailHandler()

mail_handler.login()
while True:
    mails = mail_handler.check_inbox()
    mail_handler.process_unread(mails)
    # db.monitor_schedule()
    time.sleep(1)

def login():
    