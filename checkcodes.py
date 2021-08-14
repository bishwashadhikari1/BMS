import sqlite3

a = sqlite3.connect('users_credentials.db')
c = a.cursor()
c.execute("CREATE TABLE reg_info(username text, password text, first_name text,last_name text,email text)")
a.commit()
a.close()
