import datetime

import sqlite3

e = datetime.datetime.now()

print ("Current date and time = %s" % e)

print ("Today's date:  = %s/%s/%s" % (e.day, e.month, e.year))

print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))

print("transaction ID: ' %s%s%s%s%s%s" % (e.year, e.month, e.day, e.hour, e.minute, e.second))


c = sqlite3.connect("databases/3.db")
a = c.cursor()
a.execute("SELECT * FROM customers")
c_data = a.fetchall()
print(c_data)
j = c_data[-1]
print(j)
print(j[3])
