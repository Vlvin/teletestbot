import os
import sqlite3
os.system('cat > ID.db')
conn = sqlite3.connect("ID.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users(userid, userfirst, userlast)")
conn.commit()
conn.close()
