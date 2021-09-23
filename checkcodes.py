import datetime
from tkinter import *


e = datetime.datetime.now()

print ("Current date and time = %s" % e)

print ("Today's date:  = %s/%s/%s" % (e.day, e.month, e.year))

print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))

print("transaction ID: ' %s%s%s%s%s%s" % (e.year, e.month, e.day, e.hour, e.minute, e.second))


def add_customer_mbox():
    global add_c_window
    add_customer_window = Tk()
    add_customer_window.geometry('244x329')
    add_customer_window.config(bg="#5678A9")
    Label(add_customer_window, image=add_c_window).place(x=0, y=0)
    mainloop()

add_customer_mbox()

