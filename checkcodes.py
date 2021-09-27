import datetime
from tkinter import *
import sqlite3

e = datetime.datetime.now()

print ("Current date and time = %s" % e)

print ("Today's date:  = %s/%s/%s" % (e.day, e.month, e.year))

print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))

print("transaction ID: ' %s%s%s%s%s%s" % (e.year, e.month, e.day, e.hour, e.minute, e.second))

yearmonth = '%s-%s-' % (e.year, e.month)
print(yearmonth[0:7])

'''txn_import = sqlite3.connect(f'databases/21.db')
curs = txn_import.cursor()
curs.execute(
    "SELECT * FROM transaction_history"
)
txn_details_all = curs.fetchall()
for individual_txn in txn_details_all:
    j = individual_txn[6]
    if yearmonth[0:7] == j[0:7]:
        print(individual_txn)
        print(j)
        second_last_unit = int(f'{j[-2]}{j[-1]}'
        print(second_last_unit)
'''
root = Tk()
root.geometry('400x400')
canvas = Canvas(root)
canvas.place(x=0, y=0)
j=1
for i in range (1,100, 10):
    canvas.create_rectangle(10+i,50 , 12+i, 50+i*2,
                            outline="#0f0", fill="#0f0")
    j +=1
root.mainloop()