import datetime

import sqlite3

e = datetime.datetime.now()

print ("Current date and time = %s" % e)

print ("Today's date:  = %s/%s/%s" % (e.day, e.month, e.year))

print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))

print("transaction ID: ' %s%s%s%s%s%s" % (e.year, e.month, e.day, e.hour, e.minute, e.second))


c = sqlite3.connect("databases/12.db")
a = c.cursor()
a.execute("DELETE from customers")
c_data = a.fetchall()
print(c_data)
print(j)
print(j[3])
c.commit()
c.close()


def next_page():
    if (len(d) + 10) > upper_limit:
        lower_limit += 10
        upper_limit += 10
    if (len(d) + 10) > upper_limit and len(d) < (upper_limit + 10):
        lower_limit += 10
        upper_limit = len(d)

    for details in range(lower_limit, upper_limit):
        place_location = 210
        print(details)
        present_value = lower_limit
        for detail_number in d:
            present_value += 1
            Label(home_page, text=detail_number[1], bg="#5678A9", font=10).place(x=295, y=place_location)
            Label(home_page, text=detail_number[0], bg="#5678A9", font=10).place(x=370, y=place_location)
            Label(home_page, text=detail_number[2], bg="#5678A9", font=10).place(x=570, y=place_location)
            Label(home_page, text=detail_number[3], bg="#5678A9", font=10).place(x=700, y=place_location)
            Label(home_page, text=detail_number[5], bg="#5678A9", font=10).place(x=900, y=place_location)
            Label(home_page, text=detail_number[4], bg="#5678A9", font=10).place(x=1050, y=place_location)
            Label(home_page, text=detail_number[6], bg="#5678A9", font=10).place(x=1200, y=place_location)
            place_location += 40
            if present_value == upper_limit:
                break


def previous_page():
    global u, l, pressed_atleast_once
    lower_limit = l
    upper_limit = u
    if len(d) > 10 and lower_limit >= 10:
        lower_limit -= 10
        upper_limit -= 10

    for details in range(lower_limit, upper_limit):
        place_location = 210
        print(details)
        present_value = lower_limit
        while present_value != upper_limit:
            for detail_number in d:
                present_value += 1
                Label(home_page, text=detail_number[1], bg="#5678A9", font=10).place(x=295, y=place_location)
                Label(home_page, text=detail_number[0], bg="#5678A9", font=10).place(x=370, y=place_location)
                Label(home_page, text=detail_number[2], bg="#5678A9", font=10).place(x=570, y=place_location)
                Label(home_page, text=detail_number[3], bg="#5678A9", font=10).place(x=700, y=place_location)
                Label(home_page, text=detail_number[5], bg="#5678A9", font=10).place(x=900, y=place_location)
                Label(home_page, text=detail_number[4], bg="#5678A9", font=10).place(x=1050, y=place_location)
                Label(home_page, text=detail_number[6], bg="#5678A9", font=10).place(x=1200, y=place_location)
                place_location += 40
    l = lower_limit
    u = upper_limit
    pressed_atleast_once = False