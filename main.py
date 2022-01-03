import os
from database import Database
from mail_parser import MailParser
from mail_handler import MailHandler

db = Database()
os.system("rm database.db")
db.create_database()
parser_ = MailParser()
mail_handler = MailHandler()
mail_handler.db_ = db
mail_handler.parser_ = parser_
mail_handler.login_test()
while True:
    mails = mail_handler.check_inbox()
    mail_handler.process_unread(mails)