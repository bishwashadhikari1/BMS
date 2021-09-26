import datetime
from tkinter import *
import sqlite3

e = datetime.datetime.now()

print ("Current date and time = %s" % e)

print ("Today's date:  = %s/%s/%s" % (e.day, e.month, e.year))

print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))

print("transaction ID: ' %s%s%s%s%s%s" % (e.year, e.month, e.day, e.hour, e.minute, e.second))








