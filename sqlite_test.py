from socket import timeout
import sqlite3, requests
import sys
from sys import stdout
from sqlite3.dbapi2 import sqlite_version
import threading
import database, os, time

# def view_table_information(table_name):
#         """
#         A function used to view table's information

#         """
#         con = sqlite3.connect("database.db")
#         cur = con.cursor()
#         cur.execute(f"SELECT * FROM {table_name}")
#         result = cur.fetchall()
#         print(result)

#         cur.execute("select * from chain where 'msg_id (subm)' = ?;", ('AAQkADgxMDlmYmI5LWY2MTQtNGE4MS1hYWI4LTVmMGE2ZDFmMDRhNQAQAI1SVplX-UlFhMPJS8AEd-k=',))
#         result = cur.fetchall()
#         print(result)

#         cur.execute(f"UPDATE chain SET 'convo_id (review)' = '----', " +\
#         f"reviewer = '----', review_req_sent = '----' " +\
#         f"WHERE 'msg_id (subm)' = 'AAQkADgxMDlmYmI5LWY2MTQtNGE4MS1hYWI4LTVmMGE2ZDFmMDRhNQAQAI1SVplX-UlFhMPJS8AEd-k='")
#         con.commit()

#         cur.execute(f"SELECT * FROM {table_name}")
#         result = cur.fetchall()
#         print(result)
#         con.close()


# header = {'Authorization': 'Bearer ' + "eyJ0eXAiOiJKV1QiLCJub25jZSI6IjE3QmxvSWdsS2lZVW9JZG5HYkZ1S2dNUW9DT1M5TEFkNGRUS0I1aGZMU0UiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCIsImtpZCI6Ik1yNS1BVWliZkJpaTdOZDFqQmViYXhib1hXMCJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kYzc4MTcyNy03MTBlLTQ4NTUtYmM0Yy02OTAyNjZhMWI1NTEvIiwiaWF0IjoxNjQxNjAwNzE3LCJuYmYiOjE2NDE2MDA3MTcsImV4cCI6MTY0MTYwNjI3OSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkUyWmdZQkM3WnlZYmVxQ2piOHJuVjg5V3FITWttbXhmTmJQcXUvL1ZCVm5SeGkxU3ltNEEiLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6ImJvdCIsImFwcGlkIjoiZGQ4OWJiOTQtMDdmNC00ZTVkLWI2NDEtMTI1ZmM5NmJmZGVlIiwiYXBwaWRhY3IiOiIwIiwiZmFtaWx5X25hbWUiOiJHb25nIiwiZ2l2ZW5fbmFtZSI6IkNoYW5neGluZyIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjE1MS4yMTAuMTY5LjczIiwibmFtZSI6IkNoYW5neGluZyBHb25nIiwib2lkIjoiNDcyZGYyMGUtOTZmNS00N2FhLThiMzktYjljZWVjMGRhODA5Iiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTk2NjIwNDE0My03NDY5MzI2OTAtMTE1Mzk0NjItMjgxNzIzIiwicGxhdGYiOiIxNCIsInB1aWQiOiIxMDAzMDAwMEFFNENGRjhFIiwicmgiOiIwLkFVRUFKeGQ0M0E1eFZVaThUR2tDWnFHMVVaUzdpZDMwQjExT3RrRVNYOGxyX2U1QkFEay4iLCJzY3AiOiJJTUFQLkFjY2Vzc0FzVXNlci5BbGwgTWFpbC5SZWFkIE1haWwuUmVhZEJhc2ljIE1haWwuUmVhZFdyaXRlIE1haWwuU2VuZCBvcGVuaWQgcHJvZmlsZSBVc2VyLlJlYWQgVXNlci5SZWFkQmFzaWMuQWxsIFVzZXIuUmVhZFdyaXRlIGVtYWlsIiwic2lnbmluX3N0YXRlIjpbImttc2kiXSwic3ViIjoiQmtmb3U5VTh3bWc4SW92ZG95SlNGMzdmXzdzdlplNW1aNnYtQnczN2I2YyIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJPQyIsInRpZCI6ImRjNzgxNzI3LTcxMGUtNDg1NS1iYzRjLTY5MDI2NmExYjU1MSIsInVuaXF1ZV9uYW1lIjoiY2dvNTRAdWNsaXZlLmFjLm56IiwidXBuIjoiY2dvNTRAdWNsaXZlLmFjLm56IiwidXRpIjoiOFZwWnFBSUkxVUt1US1CVUI1c1FBUSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19zdCI6eyJzdWIiOiJ6dlVrVTFPaDktUXFRcGdRNGF6MVZmODAwVU5rNUNLanpQaDlFNkZfQnAwIn0sInhtc190Y2R0IjoxMzY2OTEwMDkwfQ.V6ZX-9zbsjc_hTmy2F9sYyP4CeXv92ArVtv3ehDcPmcUVp3ULdNhsWgO_nv8GTN86AKlnndJsMr3iarRRJ4wDJ9LKaypplGVEkWx9ZcoxrMwa2u86nQTxWDgLspwwKXL9VGqBSTZrrcfaVw2dC58PgwTkXyDJKz6LN2K2BIpUSy0bDC_h7bZ83jOzmEWdjeCVngWpE-AKGp4R0dS9mmQdsTrAwmPRyPwJADDhZNtB4jSH-H1r4tztDS9EgGzx9yihMtguo5B4F_9tYQZb8RqJdPmpyDMsWE8Cv8cta15bHOG__dXEjZ4BuavfTvz3zar7i0Mn0SvuC07nNqVuW7ZHg"}
# response = requests.get("https://graph.microsoft.com/v1.0/me/messages?$filter= conversationId eq 'AAQkADgxMDlmYmI5LWY2MTQtNGE4MS1hYWI4LTVmMGE2ZDFmMDRhNQAQAJS_RqixRihLrdUDJlUUPVE='", headers=header).json()
# print(response)
# print(len())
# for mail in response['value']:
#         if mail['sender']['emailAddress']['addreess'] != 'cgo54@uclive.ac.nz':
#                 mail = 


import math
NUM_SQL_COMMANDS = 100000

def write():
        # time.sleep(5)
        for _ in range(NUM_SQL_COMMANDS):
                # print(_, flush=True)
                con = sqlite3.connect("database.db", timeout=60)
                cur = con.cursor()
                cur.execute(f"INSERT INTO chain " +\
                "('msg_id (subm)', author, subm_id, subm_received, " +\
                "'convo_id (review)', reviewer, review_req_sent, review_received, " +\
                "'convo_id (eval)', rating, comment, eval_req_sent, eval_received)" +\
                f" values ({_},NULL,NULL,NULL" + ", NULL" * 9 + ")")
                con.commit()
                con.close()
        print('--')
        print(threading.get_ident())

def read():
        for i in range(NUM_SQL_COMMANDS):
                con = sqlite3.connect("database.db", timeout=60)
                cur = con.cursor()
                cur.execute(f"select * from chain where 'msg_id (subm)' = 1 ")
                con.commit()
                con.close()

a = time.perf_counter()
for _ in range(1):
        os.system("rm database.db")
        db = database.Database()
        db.create_database()

        # threads = []
        # for _ in range(1):
        #         t = threading.Thread(target=write)
        #         t.start()
        #         threads.append(t)
        # for t in threads:
        #         t.join()

        threads = []
        for i in range(4):
                threads.append(threading.Thread(target=write))
                threads.append(threading.Thread(target=read))

        for t in threads:
                t.start()
        for t in threads:
                t.join()
b = time.perf_counter()
print(b-a)
# write_t = threading.Thread(target=c)

# read_t.start()
# write_t.start()

# read_t.join()
# write_t.join()
        


