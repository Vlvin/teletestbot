import os
import sqlite3
os.system('type nul > ID.db')
conn = sqlite3.connect("ID.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users(userid, userfirst, userlast)")
conn.commit()
conn.close()
