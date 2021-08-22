import sqlite3
import crypt
a = sqlite3.connect('databases/users_credentials.db')
c = a.cursor()
c.execute("SELECT * from reg_info")
existing_users = c.fetchall()
g = (existing_users[0])

a.commit()
