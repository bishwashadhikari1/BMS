from tkinter import *
from crypt import *
import sqlite3
import datetime

root = Tk()  # creates window
root.geometry("1280x720")
root.config(bg="#5678A9")
sign_in_page = LabelFrame(root)
register_page = LabelFrame(root)
home_page = LabelFrame(root)
analytics_frame = LabelFrame(home_page)
transactions_frame = LabelFrame(home_page)
entry_frame = LabelFrame(home_page)
customers_frame = LabelFrame(home_page)
inventory_frame = LabelFrame(home_page)

upper_limit = 10
lower_limit = 1


def register_page_function():
    """ register page function"""

    global titlepagef, sign_in_page, register_page_image, back_btn_img, tnc_check, error5_img, pw_encrypted

    titlepagef.destroy()
    sign_in_page.destroy()

    username_register = StringVar()
    password_register = StringVar()
    f_name_register = StringVar()
    l_name_register = StringVar()
    e_mail_register = StringVar()
    tnc_check = IntVar()

    register_page = LabelFrame(root, width=1280, height=720)
    register_page.place(x=0, y=0)

    register_page_image = PhotoImage(file="Images/registrationpage.png")
    register_page_background = Label(
        register_page, image=register_page_image, width=1280, height=720
    )
    register_page_background.place(x=-3, y=-3)

    un_entry = Entry(
        register_page, text=username_register, bg="#5A67A8", bd=0, font=13, width=19
    )
    pw_entry = Entry(
        register_page, text=password_register, bg="#5A67A8", bd=0, font=13, width=19
    )
    f_name_entry = Entry(
        register_page, text=f_name_register, bg="#5A67A8", bd=0, font=13, width=19
    )
    l_name_entry = Entry(
        register_page, text=l_name_register, bg="#5A67A8", bd=0, font=13, width=19
    )
    e_mail_entry = Entry(
        register_page, text=e_mail_register, bg="#5A67A8", bd=0, font=13, width=19
    )

    un_entry.place(x=524, y=155)
    pw_entry.place(x=524, y=228)
    f_name_entry.place(x=524, y=298)
    l_name_entry.place(x=524, y=374)
    e_mail_entry.place(x=524, y=447)

    Checkbutton(
        register_page,
        bg="#5A67A8",
        bd=0,
        width=1,
        height=1,
        activebackground="#5A67A8",
        variable=tnc_check,
        onvalue=1,
        offvalue=0,
    ).place(x=512, y=534)

    error_frame = LabelFrame(register_page)
    error_frame.place(x=0, y=0)

    def register_btn():
        """ check eligibility for registration and update database"""

        global error5_img, error3_img, error2_img, error1_img, error4_img, success_register_img

        email_raw = str(e_mail_register.get())
        un_encrypted = str(encrypt(username_register.get(), K))
        pw_encrypted = str(encrypt(password_register.get(), K))
        f_name_encrypted = str(encrypt(f_name_register.get(), K))
        l_name_encrypted = str(encrypt(l_name_register.get(), K))
        e_mail_encrypted = str(encrypt(e_mail_register.get(), K))
        error5_img = PhotoImage(file="Images/error5reg.png")
        error3_img = PhotoImage(file="Images/error3reg.png")
        error1_img = PhotoImage(file="Images/error1reg.png")
        error2_img = PhotoImage(file="Images/error2reg.png")
        error4_img = PhotoImage(file="Images/error4reg.png")

        error1_label = Label(register_page)
        error1_label.destroy()
        error2_label = Label(register_page)
        error2_label.destroy()
        error3_label = Label(register_page)
        error3_label.destroy()
        error4_label = Label(register_page)
        error4_label.destroy()
        error5_label = Label(register_page)
        error5_label.destroy()
        if tnc_check.get() == 0:
            error5_label = Label(register_page, image=error5_img, bg="#5678A9")
            error5_label.place(x=457, y=600)
            valid1 = False
        else:
            valid1 = True

        if len(pw_encrypted) <= 7:
            error3_label = Label(register_page, image=error3_img, bg="#5678A9")
            error3_label.place(x=520, y=564)
            valid2 = False
        else:
            valid2 = True

        if "@" in email_raw and "." in email_raw:
            valid3 = True
        else:
            error2_label = Label(register_page, image=error2_img, bg="#5678A9")
            error2_label.place(x=517, y=580)
            valid3 = False

        a = sqlite3.connect("databases/users_credentials.db")
        c = a.cursor()
        c.execute("SELECT * FROM reg_info")
        existing_users = c.fetchall()

        valid4 = True
        for user in existing_users:
            usrname = user[0]
            if un_encrypted == usrname:
                error4_label = Label(register_page, image=error4_img, bg="#5678A9")
                error4_label.place(x=558, y=488)
                valid4 = False

        valid5 = True
        for email in existing_users:
            emial = email[4]
            if e_mail_encrypted == emial:
                error1_label = Label(register_page, image=error1_img, bg="#5678A9")
                error1_label.place(x=539, y=509)
                valid5 = False

        if valid1 == valid2 == valid3 == valid4 == valid5 == 1:
            success_register_img = PhotoImage(file="Images/registration_success.png")
            Label(register_page, image=success_register_img, bg="#5678A9").place(
                x=410, y=669
            )

            c.execute(
                "INSERT INTO reg_info VALUES (:username, :password, :first_name, :last_name, :email)",
                {
                    "username": un_encrypted,
                    "password": pw_encrypted,
                    "first_name": f_name_encrypted,
                    "last_name": l_name_encrypted,
                    "email": e_mail_encrypted,
                },
            )
            a.commit()
            a.close()
            b = sqlite3.connect(f"databases/{username_register.get()}.db")
            c = b.cursor()
            c.execute(
                """ CREATE TABLE inventory(
                      item_code integer PRIMARY KEY,
                      item_name text,
                      remaining_qty integer,
                      sold_qty integer,
                      purchase_qty,
                      purchase_avg integer,
                      sales_avg integer
            )"""
            )

            c.execute(
                """ CREATE TABLE transaction_history(
            transaction_id integer PRIMARY KEY,
            item_code integer,
            item_name text,
            transaction_date integer,
            transaction_type text,
            transaction_vol integer,
            remaining_vol integer,
            transaction_price integer,
            customer_txn text
            )"""
            )

            c.execute(
                """CREATE TABLE customers(
            customer_code integer,
            customer_name text,
            customer_organization text,
            customer_email text,
            customer_address text,
            customer_contact integer,
            customer_volume integer
            )"""
            )
            b.commit()
            b.close()

    def back_btnnm():
        """takes user back to title page"""

        # sign_in_page.destroy()
        title_function()

    back_btn_img = PhotoImage(file="Images/backbutton.png")

    Button(
        register_page,
        image=back_btn_img,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=back_btnnm,
    ).place(x=29, y=626)

    Button(
        register_page,
        image=register_button_image,
        bg="#5678A9",
        bd=0,
        activebackground="#5678A9",
        command=register_btn,
    ).place(x=526, y=615)


def sign_in_page_function():
    """ sign in page function """

    global titlepagef, sign_in_page_image, sign_in_page_background, back_btn_img, sign_error1, sign_error2
    global current_sign_in, username_signin

    titlepagef.destroy()

    username_signin = StringVar()
    username_signin.set("Username")

    password_signin = StringVar()
    password_signin.set("Password")

    sign_in_page = LabelFrame(root, width=1280, height=720)
    sign_in_page.place(x=0, y=0)

    sign_in_page_image = PhotoImage(file="Images/signinpage.png")
    sign_in_page_background = Label(
        sign_in_page, image=sign_in_page_image, width=1280, height=720
    )
    sign_in_page_background.place(x=-3, y=-3)

    def clear_un_sign_in(event):
        """ remove username placeholder after selection"""

        if username_signin.get() == "Username":
            username_signin.set("")

    def clear_password_signin(events):
        """ remove password placeholder after selection"""

        if password_signin.get() == "Password":
            password_signin.set("")

    un_sign_in = Entry(
        sign_in_page, text=username_signin, bg="#5A67A8", bd=0, font=13, width=17
    )
    un_sign_in.place(x=535, y=302)
    un_sign_in.bind("<Button-1>", clear_un_sign_in)

    password_sign_in = Entry(
        sign_in_page,
        text=password_signin,
        bg="#5A67A8",
        bd=0,
        font=13,
        width=17,
        show="*",
    )
    password_sign_in.place(x=535, y=372)
    password_sign_in.bind("<Button-1>", clear_password_signin)

    def back_btnn():
        """takes user back to title page"""

        sign_in_page.destroy()
        title_function()

    back_btn_img = PhotoImage(file="Images/backbutton.png")

    Button(
        sign_in_page,
        image=back_btn_img,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=back_btnn,
    ).place(x=29, y=626)

    def submit_sign_in():
        """ verify sign in details then provide access accordingly"""

        global sign_error1, sign_error2, current_sign_in

        a = sqlite3.connect("databases/users_credentials.db")
        c = a.cursor()
        c.execute("SELECT * from reg_info")
        existing_users = c.fetchall()

        sign_error1 = PhotoImage(file="Images/signerror1.png")
        sign_error2 = PhotoImage(file="Images/signerror2.png")

        valid_sign_in = False
        password_not_matched = False
        for records in existing_users:
            username_rec = records[0]
            password_rec = records[1]

            if username_rec == encrypt(
                    username_signin.get(), K
            ) and password_rec == encrypt(password_signin.get(), K):
                valid_sign_in = True
                current_sign_in = username_signin.get()


            elif username_rec == encrypt(
                    username_signin.get(), K
            ) and password_rec != encrypt(password_signin.get(), K):
                password_not_matched = True

        if valid_sign_in is True:
            home_page_function()

        if password_not_matched is True and valid_sign_in is False:
            Label(sign_in_page, image=sign_error2, bg="#5678A9").place(x=532, y=442)

        if password_not_matched is False and valid_sign_in is False:
            Label(sign_in_page, image=sign_error1, bg="#5678A9").place(x=549, y=416)

    Button(
        sign_in_page,
        image=sign_in_button_image,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=submit_sign_in,
    ).place(x=551, y=464)


def title_function():
    """ title page function"""

    global titlepagef, titlepageimage, sign_in_button_image, register_button_image

    titlepageimage = PhotoImage(file="Images/titlepage.png")

    sign_in_button_image = PhotoImage(file="Images/signinbutton.png")

    register_button_image = PhotoImage(file="Images/registerbutton.png")

    titlepagef = LabelFrame(root, width=1280, height=720)
    titlepagef.place(x=0, y=0)

    background = Label(titlepagef, image=titlepageimage, width=1280, height=720)
    background.place(x=-3, y=-3)

    sign_in_button = Button(
        titlepagef,
        image=sign_in_button_image,
        bg="#5678A9",
        width=252,
        height=68,
        borderwidth=0,
        activebackground="#5678A9",
        command=sign_in_page_function,
    )
    sign_in_button.place(x=514, y=262)
    register_button = Button(
        titlepagef,
        image=register_button_image,
        bg="#5678A9",
        width=252,
        height=68,
        borderwidth=0,
        activebackground="#5678A9",
        command=register_page_function,
    )
    register_button.place(x=514, y=342)


def home_page_function():
    """calls home page"""

    global home_page_image, class_frame_img, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img

    sign_in_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)

    home_page_image = PhotoImage(file="Images/homepage.png")

    Label(home_page, image=home_page_image).place(x=-1, y=-1)

    analytics_img = PhotoImage(file="Images/Analytics.png")
    customers_img = PhotoImage(file="Images/Customer.png")
    entry_img = PhotoImage(file="Images/Entry.png")
    inventory_img = PhotoImage(file="Images/Inventory.png")
    transactions_img = PhotoImage(file="Images/Transactions.png")
    sign_out_img = PhotoImage(file="Images/Sign Out.png")

    analytics_frame = LabelFrame(home_page)
    transactions_frame = LabelFrame(home_page)
    entry_frame = LabelFrame(home_page)
    customers_frame = LabelFrame(home_page)
    inventory_frame = LabelFrame(home_page)

    Button(
        home_page,
        image=analytics_img,
        bg="#5678A9",
        command=analytics_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=543)
    Button(
        home_page,
        image=customers_img,
        bg="#5678A9",
        command=customers_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=154)
    Button(
        home_page,
        image=entry_img,
        bg="#5678A9",
        command=entry_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=60, y=410)
    Button(
        home_page,
        image=inventory_img,
        bg="#5678A9",
        command=inventory_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=25, y=20)
    Button(
        home_page,
        image=transactions_img,
        bg="#5678A9",
        command=transactions_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=10, y=283)
    Button(
        home_page,
        image=sign_out_img,
        bg="#5678A9",
        command=sign_out_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=35, y=664)


def analytics_function():
    global home_page_image, class_frame_img, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img

    home_page = LabelFrame(root)
    home_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)

    home_page_image = PhotoImage(file="Images/Analyticspage.png")

    Label(home_page, image=home_page_image).place(x=-1, y=-1)

    Button(
        home_page,
        image=analytics_img,
        bg="#5678A9",
        command=analytics_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=543)
    Button(
        home_page,
        image=customers_img,
        bg="#5678A9",
        command=customers_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=154)
    Button(
        home_page,
        image=entry_img,
        bg="#5678A9",
        command=entry_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=60, y=410)
    Button(
        home_page,
        image=inventory_img,
        bg="#5678A9",
        command=inventory_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=25, y=20)
    Button(
        home_page,
        image=transactions_img,
        bg="#5678A9",
        command=transactions_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=10, y=283)
    Button(
        home_page,
        image=sign_out_img,
        bg="#5678A9",
        command=sign_out_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=35, y=664)


def customers_function():
    global home_page_image, class_frame_img, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img, add_customer, remove_customer, add_c_window, sb_frame, canvas_display, cust_details_label

    home_page = LabelFrame(root)
    home_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)
    home_page_image = PhotoImage(file="Images/customers_page.png")

    Label(home_page, image=home_page_image).place(x=-2, y=-1)

    add_customer = PhotoImage(file="Images/add customer.png")
    remove_customer = PhotoImage(file="Images/remove_customer.png")
    add_c_window = PhotoImage(file="Images/add_customer_window.png")

    Button(
        home_page, image=add_customer, bg="#5678A9", bd=0, activebackground="#5678A9", command=add_customer_mbox
    ).place(x=927, y=96)
    Button(
        home_page, image=remove_customer, bg="#5678A9", bd=0, activebackground="#5678A9", command=remove_customer_mbox
    ).place(x=310, y=96)
    Button(
        home_page,
        image=analytics_img,
        bg="#5678A9",
        command=analytics_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=543)
    Button(
        home_page,
        image=customers_img,
        bg="#5678A9",
        command=customers_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=154)
    Button(
        home_page,
        image=entry_img,
        bg="#5678A9",
        command=entry_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=60, y=410)
    Button(
        home_page,
        image=inventory_img,
        bg="#5678A9",
        command=inventory_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=25, y=20)
    Button(
        home_page,
        image=transactions_img,
        bg="#5678A9",
        command=transactions_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=10, y=283)
    Button(
        home_page,
        image=sign_out_img,
        bg="#5678A9",
        command=sign_out_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=35, y=664)

    c = sqlite3.connect(f"databases/{current_sign_in}.db")
    b = c.cursor()
    b.execute("SELECT * FROM customers")
    d = b.fetchall()
    cust_details_label = LabelFrame(home_page, bg="#5678A9").place(x=292, y=206)
    canvas_display = Canvas(cust_details_label, bg="#5678A9")
    canvas_display.place(x=292, y=206, width=956, height=476)
    sb = Scrollbar(cust_details_label, orient=VERTICAL, command=canvas_display.yview)
    sb.place(relx=1, rely=0, relheight=1, anchor='ne')
    canvas_display.configure(yscrollcommand=sb.set)
    canvas_display.bind('<Configure>', lambda e: canvas_display.configure(scrollregion=canvas_display.bbox("all")))
    sb_frame = Frame(canvas_display)
    sb_frame.config(bg="#5678A9")
    canvas_display.create_window((0, 0), height=(len(d)*30+11), width=966, window=sb_frame)
    canvas_display.config(bg='#5678A9')

    for details in range(1, len(d)):
        place_location = 10
        print(details)
        for detail_number in d:
            Label(sb_frame, text=detail_number[1], bg="#5678A9", font=10).place(x=10, y=place_location)
            Label(sb_frame, text=detail_number[0], bg="#5678A9", font=10).place(x=90, y=place_location)
            Label(sb_frame, text=detail_number[2], bg="#5678A9", font=10).place(x=280, y=place_location)
            Label(sb_frame, text=detail_number[3], bg="#5678A9", font=10).place(x=410, y=place_location)
            Label(sb_frame, text=detail_number[5], bg="#5678A9", font=10).place(x=610, y=place_location)
            Label(sb_frame, text=detail_number[4], bg="#5678A9", font=10).place(x=750, y=place_location)
            Label(sb_frame, text=detail_number[6], bg="#5678A9", font=10).place(x=890, y=place_location)
            place_location += 30



def entry_function():
    global home_page_image, class_frame_img, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img, entry_details

    home_page = LabelFrame(root)
    home_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)

    home_page_image = PhotoImage(file="Images/homepage.png")

    Label(home_page, image=home_page_image).place(x=-1, y=-1)
    Label(home_page, image=entry_img, bg="#000000").place(x=650, y=106)

    entry_details = PhotoImage(file="Images/entry_page_img.png")
    Label(home_page, image=entry_details).place(x=-1, y=-1)

    item_name_c_reg = StringVar()
    quantity_c_reg = StringVar()
    type_c_reg = StringVar()
    customer_c_reg = StringVar()
    price_per_unit_c_reg = StringVar()
    item_add_c_reg = StringVar()
    item_remove_c_reg = StringVar()
    transaction_code_c_reg = StringVar()

    item_name_entry = Entry(
        home_page, text=item_name_c_reg, bg="#5A67A8", bd=0, font=8, width=21
    )

    quantity_entry = Entry(
        home_page, text=quantity_c_reg, bg="#5A67A8", bd=0, font=8, width=21
    )

    type_entry = Entry(
        home_page, text=type_c_reg, bg="#5A67A8", bd=0, font=8, width=21
    )

    customer_entry = Entry(
        home_page, text=customer_c_reg, bg="#5A67A8", bd=0, font=8, width=21
    )
    price_per_unit_entry = Entry(
        home_page, text=price_per_unit_c_reg, bg="#5A67A8", bd=0, font=8, width=21
    )

    item_add_entry = Entry(
        home_page, text=item_add_c_reg, bg="#5A67A8", bd=0, font=8, width=21
    )

    item_remove_entry = Entry(
        home_page, text=item_remove_c_reg, bg="#5A67A8", bd=0, font=8, width=21
    )

    transaction_code_entry = Entry(
        home_page, text=transaction_code_c_reg, bg="#5A67A8", bd=0, font=8, width=21
    )

    item_name_entry.place(x=340, y=215)
    quantity_entry.place(x=340, y=297)
    type_entry.place(x=340, y=380)
    customer_entry.place(x=340, y=462)
    price_per_unit_entry.place(x=340, y=548)
    item_add_entry.place(x=830, y=228)
    item_remove_entry.place(x=830, y=414)
    transaction_code_entry.place(x=830, y=597)

    Button(
        home_page,
        image=analytics_img,
        bg="#5678A9",
        command=analytics_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=543)
    Button(
        home_page,
        image=customers_img,
        bg="#5678A9",
        command=customers_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=154)
    Button(
        home_page,
        image=entry_img,
        bg="#5678A9",
        command=entry_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=60, y=410)
    Button(
        home_page,
        image=inventory_img,
        bg="#5678A9",
        command=inventory_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=25, y=20)
    Button(
        home_page,
        image=transactions_img,
        bg="#5678A9",
        command=transactions_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=10, y=283)
    Button(
        home_page,
        image=sign_out_img,
        bg="#5678A9",
        command=sign_out_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=35, y=664)


def inventory_function():
    global home_page_image, class_frame_img, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img

    home_page = LabelFrame(root)
    home_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)

    home_page_image = PhotoImage(file="Images/Inventory_page.png")

    Label(home_page, image=home_page_image).place(x=-1, y=-1)

    Button(
        home_page,
        image=analytics_img,
        bg="#5678A9",
        command=analytics_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=543)
    Button(
        home_page,
        image=customers_img,
        bg="#5678A9",
        command=customers_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=154)
    Button(
        home_page,
        image=entry_img,
        bg="#5678A9",
        command=entry_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=60, y=410)
    Button(
        home_page,
        image=inventory_img,
        bg="#5678A9",
        command=inventory_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=25, y=20)
    Button(
        home_page,
        image=transactions_img,
        bg="#5678A9",
        command=transactions_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=10, y=283)
    Button(
        home_page,
        image=sign_out_img,
        bg="#5678A9",
        command=sign_out_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=35, y=664)


def transactions_function():
    global home_page_image
    global home_page_image, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img

    home_page = LabelFrame(root)
    home_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)

    home_page_image = PhotoImage(file="Images/homepage.png")

    Label(home_page, image=home_page_image).place(x=-1, y=-1)

    transactions_frame = LabelFrame(home_page).place(x=265, y=88)
    Label(transactions_frame, image=transactions_img, bg="#000000").place(x=650, y=106)

    Button(
        home_page,
        image=analytics_img,
        bg="#5678A9",
        command=analytics_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=543)
    Button(
        home_page,
        image=customers_img,
        bg="#5678A9",
        command=customers_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=154)
    Button(
        home_page,
        image=entry_img,
        bg="#5678A9",
        command=entry_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=60, y=410)
    Button(
        home_page,
        image=inventory_img,
        bg="#5678A9",
        command=inventory_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=25, y=20)
    Button(
        home_page,
        image=transactions_img,
        bg="#5678A9",
        command=transactions_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=10, y=283)
    Button(
        home_page,
        image=sign_out_img,
        bg="#5678A9",
        command=sign_out_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=35, y=664)


def sign_out_function():
    title_function()


def add_customer_mbox():
    global c_add_success1, c_add_error2, c_add_error3
    global home_page_image, class_frame_img, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img, add_customer, remove_customer, add_c_window, add_button

    home_page = LabelFrame(root)
    home_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)
    home_page_image = PhotoImage(file="Images/customers_page.png")

    Label(home_page, image=home_page_image).place(x=-2, y=-1)

    add_customer = PhotoImage(file="Images/add customer.png")
    remove_customer = PhotoImage(file="Images/remove_customer.png")
    add_c_window = PhotoImage(file="Images/add_customer_window.png")
    Label(home_page, image=add_c_window).place(x=573, y=198)

    name_c_reg = StringVar()
    organization_c_reg = StringVar()
    email_c_reg = StringVar()
    number_c_reg = StringVar()
    address_c_reg = StringVar()

    name_entry = Entry(
        home_page, text=name_c_reg, bg="#5A67A8", bd=0, font=8, width=21
    )
    organization_entry = Entry(
        home_page, text=organization_c_reg, bg="#5A67A8", bd=0, font=6, width=21
    )

    email_entry = Entry(
        home_page, text=email_c_reg, bg="#5A67A8", bd=0, font=13, width=21
    )

    number_entry = Entry(
        home_page, text=number_c_reg, bg="#5A67A8", bd=0, font=13, width=21
    )
    address_entry = Entry(
        home_page, text=address_c_reg, bg="#5A67A8", bd=0, font=13, width=21
    )

    name_entry.place(x=602, y=235)
    organization_entry.place(x=602, y=298)
    email_entry.place(x=602, y=363)
    number_entry.place(x=602, y=427)
    address_entry.place(x=602, y=493)

    add_button = PhotoImage(file="Images/add_c_button.png")

    def add_b_click():
        global c_add_success1, c_add_error2, c_add_error3, i
        c_add_success1 = PhotoImage(file="Images/Customer added successfully.png")
        c_add_error2 = PhotoImage(file="Images/Customer with this email already exists.png")
        c_add_error3 = PhotoImage(file="Images/Customer with this number already exists.png")

        b = sqlite3.connect(f"databases/{current_sign_in}.db")
        print(current_sign_in)
        c = b.cursor()
        c.execute("SELECT * FROM customers")
        existing_customers = c.fetchall()
        valid1 = True
        valid2 = True

        for customers in existing_customers:
            if customers[3] == email_c_reg.get():
                valid1 = False
                Label(home_page, image=c_add_error2, bg="#5678A9").place(x=589, y=549)
            elif customers[4] == number_c_reg.get():
                valid2 = False
                Label(home_page, image=c_add_error3, bg="#5678A9").place(x=589, y=549)

        if valid1 == True and valid2 == True:
            e = datetime.datetime.now()
            customer_code_reg = "%s%s%s%s%s%s" % (e.year, e.month, e.day, e.hour, e.minute, e.second)
            Label(home_page, image=c_add_success1, bg="#5678A9").place(x=589, y=549)
            c.execute(
                "INSERT INTO customers VALUES(:customer_code, :customer_name, :customer_organization, :customer_email,\
                :customer_address, :customer_contact, :customer_volume)",
                {
                    "customer_code": customer_code_reg,
                    "customer_name": name_c_reg.get(),
                    "customer_organization": organization_c_reg.get(),
                    "customer_email": email_c_reg.get(),
                    "customer_address": address_c_reg.get(),
                    "customer_contact": number_c_reg.get(),
                    "customer_volume": 0,
                },
            )
            b.commit()
            b.close()

    Button(
        home_page, image=add_button, bg="#5678A9", bd=0, activebackground="#5678A9", command=add_b_click
    ).place(x=710, y=535)
    Button(
        home_page, image=add_customer, bg="#5678A9", bd=0, activebackground="#5678A9", command=add_customer_mbox
    ).place(x=927, y=96)
    Button(
        home_page, image=remove_customer, bg="#5678A9", bd=0, activebackground="#5678A9", command=remove_customer_mbox
    ).place(x=310, y=96)
    Button(
        home_page,
        image=analytics_img,
        bg="#5678A9",
        command=analytics_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=543)
    Button(
        home_page,
        image=customers_img,
        bg="#5678A9",
        command=customers_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=154)
    Button(
        home_page,
        image=entry_img,
        bg="#5678A9",
        command=entry_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=60, y=410)
    Button(
        home_page,
        image=inventory_img,
        bg="#5678A9",
        command=inventory_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=25, y=20)
    Button(
        home_page,
        image=transactions_img,
        bg="#5678A9",
        command=transactions_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=10, y=283)
    Button(
        home_page,
        image=sign_out_img,
        bg="#5678A9",
        command=sign_out_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=35, y=664)


def remove_customer_mbox():
    global home_page_image, class_frame_img, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img, add_customer, remove_customer, add_c_window, remove_c_window, remove_button

    home_page = LabelFrame(root)
    home_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)
    home_page_image = PhotoImage(file="Images/customers_page.png")

    Label(home_page, image=home_page_image).place(x=-2, y=-1)
    remove_button = PhotoImage(file="Images/remove_c_button.png")

    add_customer = PhotoImage(file="Images/add customer.png")
    remove_customer = PhotoImage(file="Images/remove_customer.png")
    add_c_window = PhotoImage(file="Images/add_customer_window.png")
    remove_c_window = PhotoImage(file="Images/remove_customer_window.png")

    def remove_c_click():
        pass

    Label(home_page, image=remove_c_window).place(x=573, y=198)

    remove_c_code = StringVar()

    code_entry = Entry(
        home_page, text=remove_c_code, bg="#5A67A8", bd=0, font=8, width=21
    )
    code_entry.place(x=606, y=238)

    Button(
        home_page, image=remove_button, bg="#5678A9", bd=0, activebackground="#5678A9", command=remove_c_click
    ).place(x=696, y=275)
    Button(
        home_page, image=add_customer, bg="#5678A9", bd=0, activebackground="#5678A9", command=add_customer_mbox
    ).place(x=927, y=96)
    Button(
        home_page,
        image=analytics_img,
        bg="#5678A9",
        command=analytics_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=543)
    Button(
        home_page,
        image=customers_img,
        bg="#5678A9",
        command=customers_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=20, y=154)
    Button(
        home_page,
        image=entry_img,
        bg="#5678A9",
        command=entry_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=60, y=410)
    Button(
        home_page,
        image=inventory_img,
        bg="#5678A9",
        command=inventory_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=25, y=20)
    Button(
        home_page,
        image=transactions_img,
        bg="#5678A9",
        command=transactions_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=10, y=283)
    Button(
        home_page,
        image=sign_out_img,
        bg="#5678A9",
        command=sign_out_function,
        bd=0,
        activebackground="#5678A9",
    ).place(x=35, y=664)


title_function()

mainloop()
