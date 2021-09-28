from tkinter import *
from crypt import *
import sqlite3
import datetime

root = Tk()  # creates window
root.title("BMS")
root.iconbitmap('images/icon.ico')
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
                      purchase_qty integer
                    )"""
            )
            c.execute(
                    """ CREATE TABLE transaction_history(
                        transaction_id integer PRIMARY KEY,
                        item_name text,
                        transaction_qty,
                        transaction_type text,
                        customer_txn text,
                        transaction_price integer,
                        transaction_date integer,
                        transaction_vol integer
                    )"""
            )

            c.execute(
                    """CREATE TABLE customers(
                        customer_code integer PRIMARY KEY,
                        customer_name text,
                        customer_organization text,
                        customer_email text,
                        customer_address text,
                        customer_contact integer,
                        customer_volume integer
                    )"""
            )

            c.execute(
                    """CREATE TABLE volume_profile(
                        buy_volume integer,
                        sell_volume integer,
                        buy_qty integer,
                        sell_qty integer
                    )"""
            )
            b.commit()
            c.execute(
                "INSERT INTO volume_profile VALUES(:buy_volume, :sell_volume, :buy_qty, :sell_qty)",
                {
                    "buy_volume": 0,
                    "sell_volume": 0,
                    "buy_qty": 0,
                    "sell_qty": 0,
                },
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
    """sign in page function"""

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

    def clear_un_sign_in(events):
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
    """go to analytics page for the current customer signed in"""

    global home_page_image, class_frame_img, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img

    home_page = LabelFrame(root)
    home_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)

    home_page_image = PhotoImage(file="Images/Analyticspage.png")

    Label(home_page, image=home_page_image).place(x=-1, y=-1)

    s = sqlite3.connect(f'databases/{current_sign_in}.db')
    c = s.cursor()
    c.execute(
        "SELECT * FROM volume_profile"
    )
    g = c.fetchall()
    h = g[0]
    print(h)
    f = h[0] + h[1]
    if f == 0:
        f += 1
    angle_f = (360 * h[0]) / f
    angle_g = (360 * h[1]) / f
    canvas = Canvas(home_page, width=190, height=185, bg="#5678A9", highlightthickness=0)
    canvas.place(x=511, y=206)
    canvas.create_arc((0, 0, 190, 185), fill="#ff0000", outline="#ff0000", start=0, extent=angle_f)
    canvas.create_arc((0, 0, 190, 185), fill="#00ff00", outline="#00ff00", start=angle_f, extent=angle_g)
    g = h[2]
    if h[2] == 0:
        g = 1
    h_3 = g-h[3]
    f_1 = g * 2
    angle_f_1 = (360 * g) / f_1
    angle_g_1 = (360 * h[3]) / f_1
    angle_h_1 = (360 * h_3) / f_1
    canvas = Canvas(home_page, width=190, height=186, bg="#5678A9", highlightthickness=0)
    canvas.place(x=511, y=477)
    canvas.create_arc((0, 0, 190, 185), fill="#ff0000", outline="#ff0000", start=0, extent=angle_f_1)
    canvas.create_arc((0, 0, 190, 185), fill="#00ff00", outline="#00ff00", start=angle_f_1, extent=angle_g_1)
    canvas.create_arc((0, 0, 190, 185), fill="#0000ff", outline="#0000ff", start=(angle_g_1+angle_f_1),
                      extent=angle_h_1)

    txn_import = sqlite3.connect(f'databases/{current_sign_in}.db')
    curs = txn_import.cursor()
    curs.execute(
        "SELECT * FROM transaction_history"
    )
    e = datetime.datetime.now()
    yearmonth = '%s-%s-' % (e.year, e.month)
    print(yearmonth[0:7])
    txn_details_all = curs.fetchall()
    date_1 = date_2 = date_3 = date_4 = date_5 = date_6 = date_7 = date_9 = date_10 = date_11 = date_12 = date_13 = 0
    date_14 = date_15 = date_16 = date_17 = date_18 = date_19 = date_20 = date_21 = date_22 = date_23 = date_24 = 0
    date_25 = date_26 = date_27 = date_28 = date_29 = date_30 = date_31 = date_8 = date_32 = 0

    datee_1 = datee_2 = datee_3 = datee_4 = datee_5 = datee_6 = datee_7 = datee_9 = datee_10 = datee_11 = datee_12 = 0
    datee_14 = datee_15 = datee_16 = datee_17 = datee_18 = datee_19 = datee_20 = datee_21 = datee_22 = datee_23 = 0
    datee_24 = 0
    datee_25 = datee_26 = datee_27 = datee_28 = datee_29 = datee_30 = datee_31 = datee_8 = datee_32 = datee_13 = 0

    for individual_txn in txn_details_all:
        j = individual_txn[6]
        if yearmonth[0:7] == j[0:7]:
            second_last_unit = j[-2:-1]
            if second_last_unit == '-':
                date = j[-1]
            else:
                date = int(f'{j[-2]}{j[-1]}')
            if individual_txn[3] == "Buy":
                if date == 1:
                    date_1 += individual_txn[7]
                elif date == 2:
                    date_2 += individual_txn[7]
                elif date == 3:
                    date_3 += individual_txn[7]
                elif date == 4:
                    date_4 += individual_txn[7]
                elif date == 5:
                    date_5 += individual_txn[7]
                elif date == 6:
                    date_6 += individual_txn[7]
                elif date == 7:
                    date_7 += individual_txn[7]
                elif date == 8:
                    date_8 += individual_txn[7]
                elif date == 9:
                    date_9 += individual_txn[7]
                elif date == 10:
                    date_10 += individual_txn[7]
                elif date == 11:
                    date_11 += individual_txn[7]
                elif date == 12:
                    date_12 += individual_txn[7]
                elif date == 13:
                    date_13 += individual_txn[7]
                elif date == 14:
                    date_14 += individual_txn[7]
                elif date == 15:
                    date_15 += individual_txn[7]
                elif date == 16:
                    date_16 += individual_txn[7]
                elif date == 17:
                    date_17 += individual_txn[7]
                elif date == 18:
                    date_18 += individual_txn[7]
                elif date == 19:
                    date_19 += individual_txn[7]
                elif date == 20:
                    date_20 += individual_txn[7]
                elif date == 21:
                    date_21 += individual_txn[7]
                elif date == 22:
                    date_22 += individual_txn[7]
                elif date == 23:
                    date_23 += individual_txn[7]
                elif date == 24:
                    date_24 += individual_txn[7]
                elif date == 25:
                    date_25 += individual_txn[7]
                elif date == 26:
                    date_26 += individual_txn[7]
                elif date == 27:
                    date_27 += individual_txn[7]
                elif date == 28:
                    date_28 += individual_txn[7]
                elif date == 29:
                    date_29 += individual_txn[7]
                elif date == 30:
                    date_30 += individual_txn[7]
                elif date == 31:
                    date_31 += individual_txn[7]
                elif date == 32:
                    date_32 += individual_txn[7]

            if individual_txn[3] == "Sell":
                if date == 1:
                    datee_1 += individual_txn[7]
                elif date == 2:
                    datee_2 += individual_txn[7]
                elif date == 3:
                    datee_3 += individual_txn[7]
                elif date == 4:
                    date_4 += individual_txn[7]
                elif date == 5:
                    datee_5 += individual_txn[7]
                elif date == 6:
                    datee_6 += individual_txn[7]
                elif date == 7:
                    datee_7 += individual_txn[7]
                elif date == 8:
                    datee_8 += individual_txn[7]
                elif date == 9:
                    datee_9 += individual_txn[7]
                elif date == 10:
                    datee_10 += individual_txn[7]
                elif date == 11:
                    datee_11 += individual_txn[7]
                elif date == 12:
                    datee_12 += individual_txn[7]
                elif date == 13:
                    datee_13 += individual_txn[7]
                elif date == 14:
                    datee_14 += individual_txn[7]
                elif date == 15:
                    datee_15 += individual_txn[7]
                elif date == 16:
                    datee_16 += individual_txn[7]
                elif date == 17:
                    datee_17 += individual_txn[7]
                elif date == 18:
                    datee_18 += individual_txn[7]
                elif date == 19:
                    datee_19 += individual_txn[7]
                elif date == 20:
                    datee_20 += individual_txn[7]
                elif date == 21:
                    datee_21 += individual_txn[7]
                elif date == 22:
                    datee_22 += individual_txn[7]
                elif date == 23:
                    datee_23 += individual_txn[7]
                elif date == 24:
                    datee_24 += individual_txn[7]
                elif date == 25:
                    datee_25 += individual_txn[7]
                elif date == 26:
                    datee_26 += individual_txn[7]
                elif date == 27:
                    datee_27 += individual_txn[7]
                elif date == 28:
                    datee_28 += individual_txn[7]
                elif date == 29:
                    datee_29 += individual_txn[7]
                elif date == 30:
                    datee_30 += individual_txn[7]
                elif date == 31:
                    datee_31 += individual_txn[7]
                elif date == 32:
                    datee_32 += individual_txn[7]
    buy_vol_date = [date_1, date_2, date_3, date_4, date_5, date_6, date_7, date_8, date_9, date_10, date_11, date_12,
                    date_13, date_14, date_14, date_15, date_16, date_17, date_18, date_19, date_20, date_21, date_22,
                    date_23, date_24, date_25, date_26, date_27, date_28, date_29, date_30, date_31, date_32]
    sell_vol_date = [datee_1, datee_2, datee_3, datee_4, datee_5, datee_6, datee_7, datee_8, datee_9, datee_10,
                     datee_11, datee_12, datee_13, datee_14, datee_14, datee_15, datee_16, datee_17, datee_18, datee_19,
                     datee_20, datee_21, datee_22, datee_23, datee_24, datee_25, datee_26, datee_27, datee_28, datee_29,
                     datee_30, datee_31, datee_32]

    graph_details_label = LabelFrame(home_page, bg="#5678A9").place(x=843, y=241)
    canvas_display = Canvas(graph_details_label, bg="#5678A9")
    canvas_display.place(x=843, y=241, width=345, height=381)
    canvas_display.config(bg='#5678A9')
    print(buy_vol_date)
    print(sell_vol_date)
    i = 1
    j = 6
    for vols in buy_vol_date:
        if vols <= 1000:
            vols = 1000
        canvas_display.create_rectangle(i, 370-(vols/40000), i+2, 370,
                                        outline="#f00", fill="#f00")
        i += 10

    for ols in sell_vol_date:
        if ols <= 1000:
            ols = 1000
        canvas_display.create_rectangle(j, 370-(ols/40000), j+2, 370,
                                        outline="#0f0", fill="#0f0")
        j += 10

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
    """ go to customer details page for currently signed in used"""

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
        home_page,
        image=add_customer,
        bg="#5678A9",
        bd=0,
        activebackground="#5678A9",
        command=add_customer_mbox,
    ).place(x=927, y=96)
    Button(
        home_page,
        image=remove_customer,
        bg="#5678A9",
        bd=0,
        activebackground="#5678A9",
        command=remove_customer_mbox,
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
            Label(sb_frame, text=detail_number[1], bg="#5678A9", font=10).place(
                x=10, y=place_location
            )
            Label(sb_frame, text=detail_number[0], bg="#5678A9", font=10).place(
                x=90, y=place_location
            )
            Label(sb_frame, text=detail_number[2], bg="#5678A9", font=10).place(
                x=280, y=place_location
            )
            Label(sb_frame, text=detail_number[3], bg="#5678A9", font=10).place(
                x=410, y=place_location
            )
            Label(sb_frame, text=detail_number[5], bg="#5678A9", font=10).place(
                x=610, y=place_location
            )
            Label(sb_frame, text=detail_number[4], bg="#5678A9", font=10).place(
                x=750, y=place_location
            )
            Label(sb_frame, text=detail_number[6], bg="#5678A9", font=10).place(
                x=875, y=place_location
            )
            place_location += 30


def entry_function():
    """ go to record entry page for current user logged in"""

    global home_page_image, class_frame_img, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img, entry_details, add_transaction_button, add_button, remove_button, error_img, success_img

    home_page = LabelFrame(root)
    home_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)

    Label(home_page, image=entry_img, bg="#000000").place(x=650, y=106)

    entry_details = PhotoImage(file="Images/entry_page_img.png")
    Label(home_page, image=entry_details).place(x=-1, y=-1)

    user_file = sqlite3.connect(f"databases/{current_sign_in}.db")
    curs = user_file.cursor()
    curs.execute("SELECT * FROM customers")
    customers_list = curs.fetchall()
    customer_name_list = ["others", "none"]
    for num in customers_list:
        current_cust = num[1]
        customer_name_list.append(f"{current_cust}")
        print(customer_name_list)
    item_list = [
        "other",
    ]
    curs.execute("SELECT * FROM inventory")
    item_details_list = curs.fetchall()
    for itemss in item_details_list:
        curr_entry = itemss[1]
        item_list.append(f"{curr_entry}")

    item_name_entry = StringVar()
    quantity_entry = IntVar()
    customer_entry = StringVar()
    price_per_unit_entry = IntVar()
    item_add_entry = StringVar()
    item_remove_entry = StringVar()
    transaction_code_entry = StringVar()
    dd_type = StringVar()
    dd_type.set("Buy")
    type_options = ["Buy", "Sell"]
    drop = OptionMenu(home_page, dd_type, *type_options)
    drop.config(
        bg="#5A67A8", activebackground="#5A67A8", width=45, height=1, highlightthickness=0, borderwidth=0
    )
    drop.place(x=344, y=381)

    customer_options = OptionMenu(home_page, customer_entry, *customer_name_list)
    customer_entry.set("none")
    customer_options.config(
        bg="#5A67A8", activebackground="#5A67A8", width=45, borderwidth=0, height=1, highlightthickness=0
    )
    customer_options.place(x=340, y=460)

    item_name_options = OptionMenu(home_page, item_name_entry, *item_list)
    item_name_options.config(
        bg="#5A67A8", activebackground="#5A67A8", width=45, borderwidth=0, height=1, highlightthickness=0
    )
    item_name_options.place(x=340, y=212)

    quantity_entry = Entry(
        home_page, text=quantity_entry, bg="#5A67A8", bd=0, font=8, width=21
    )
    price_per_unit_entry = Entry(
        home_page, text=price_per_unit_entry, bg="#5A67A8", bd=0, font=8, width=21
    )

    item_add_entry = Entry(
        home_page, text=item_add_entry, bg="#5A67A8", bd=0, font=8, width=21
    )

    item_remove_entry = Entry(
        home_page, text=item_remove_entry, bg="#5A67A8", bd=0, font=8, width=21
    )

    transaction_code_remove_entry = Entry(
        home_page, text=transaction_code_entry, bg="#5A67A8", bd=0, font=8, width=21
    )

    quantity_entry.place(x=340, y=297)
    price_per_unit_entry.place(x=340, y=548)
    item_add_entry.place(x=830, y=228)
    item_remove_entry.place(x=830, y=414)
    transaction_code_remove_entry.place(x=830, y=597)

    add_transaction_button = PhotoImage(file="Images/add_transaction_button.png")
    add_button = PhotoImage(file="Images/add_button.png")
    remove_button = PhotoImage(file="Images/remove_button.png")

    def add_transaction_click():
        """ adds the stated transaction if eligible and updates all databases"""

        user_file = sqlite3.connect(f"databases/{current_sign_in}.db")
        c = user_file.cursor()
        e = datetime.datetime.now()
        transaction_id_entry = "%s%s%s%s%s%s" % (
            e.year,
            e.month,
            e.day,
            e.hour,
            e.minute,
            e.second,
        )
        today_date = "%s-%s-%s" % (e.year, e.month, e.day)
        txn_volume = int(price_per_unit_entry.get()) * int(quantity_entry.get())
        c.execute(
            "INSERT INTO transaction_history VALUES(:transaction_id, :item_name, :transaction_qty, \
            :transaction_type, :customer_txn, :transaction_price, :transaction_date, :transaction_vol)",
            {
                "transaction_id": transaction_id_entry,
                "item_name": item_name_entry.get(),
                "transaction_qty": quantity_entry.get(),
                "transaction_type": dd_type.get(),
                "customer_txn": customer_entry.get(),
                "transaction_price": price_per_unit_entry.get(),
                "transaction_date": today_date,
                "transaction_vol": txn_volume,
            },
        )
        user_file.commit()
        c.execute(f"SELECT * FROM customers WHERE customer_name='{customer_entry.get()}'")
        existing_datas = c.fetchall()
        print(existing_datas)
        existing_data = existing_datas[0]
        data_0 = existing_data[0]
        data_1 = existing_data[1]
        data_2 = existing_data[2]
        data_3 = existing_data[3]
        data_4 = existing_data[4]
        data_5 = existing_data[5]
        data_6 = existing_data[6]
        updated_data = data_6 + txn_volume
        c.execute(f"DELETE FROM customers WHERE customer_name='{customer_entry.get()}'")

        user_file.commit()

        c.execute(
            "INSERT INTO customers VALUES(:customer_code, :customer_name, :customer_organization, :customer_email,\
            :customer_address, :customer_contact, :customer_volume)",
            {
                "customer_code": data_0,
                "customer_name": data_1,
                "customer_organization": data_2,
                "customer_email": data_3,
                "customer_address": data_4,
                "customer_contact": data_5,
                "customer_volume": updated_data,
            },
        )
        user_file.commit()
        c.execute(f"SELECT * FROM inventory WHERE item_name='{item_name_entry.get()}'")
        existing_item_stats = c.fetchall()
        existing_item_stat = existing_item_stats[0]
        dataa_0 = existing_item_stat[0]
        dataa_1 = existing_item_stat[1]
        dataa_2 = int(existing_item_stat[2])
        dataa_3 = int(existing_item_stat[3])
        dataa_4 = int(existing_item_stat[4])
        c.execute(f"DELETE FROM inventory WHERE item_name ='{item_name_entry.get()}'")
        user_file.commit()
        if dd_type.get() == "Buy":
            dataa_2 += int(quantity_entry.get())
            dataa_4 += int(quantity_entry.get())
        elif dd_type.get() == "Sell":
            dataa_2 -= int(quantity_entry.get())
            dataa_3 += int(quantity_entry.get())
        c.execute(
            "INSERT INTO inventory VALUES(:item_code, :item_name, :remaining_qty, :sold_qty, :purchase_qty)",
            {
                "item_code": dataa_0,
                "item_name": dataa_1,
                "remaining_qty": dataa_2,
                "sold_qty": dataa_3,
                "purchase_qty": dataa_4,
            },
        )
        user_file.commit()

        c.execute("SELECT * FROM volume_profile")
        vol_r = c.fetchall()
        vol_p = vol_r[0]
        vol_0 = vol_p[0]
        vol_1 = vol_p[1]
        vol_2 = vol_p[2]
        vol_3 = vol_p[3]
        if dd_type.get() == "Buy":
            vol_0 += txn_volume
            vol_2 += int(quantity_entry.get())
        elif dd_type.get() == "Sell":
            vol_1 += txn_volume
            vol_3 += int(quantity_entry.get())
        c.execute("DELETE  FROM volume_profile")
        user_file.commit()

        c.execute(
            "INSERT INTO volume_profile VALUES(:buy_volume, :sell_volume, :buy_qty, :sell_qty)",
            {
                "buy_volume": vol_0,
                "sell_volume": vol_1,
                "buy_qty": vol_2,
                "sell_qty": vol_3,
            },
        )
        user_file.commit()

    def add_item_click():
        """ adds a new item to the inventory list"""

        e = datetime.datetime.now()
        item_code_entry = "%s%s%s%s%s%s" % (
            e.year,
            e.month,
            e.day,
            e.hour,
            e.minute,
            e.second,
        )
        user_info = sqlite3.connect(f"databases/{current_sign_in}.db")
        c = user_info.cursor()
        c.execute(
            "INSERT INTO inventory VALUES(:item_code, :item_name, :remaining_qty, :sold_qty, :purchase_qty)",
            {
                "item_code": item_code_entry,
                "item_name": item_add_entry.get(),
                "remaining_qty": 0,
                "sold_qty": 0,
                "purchase_qty": 0,
            },
        )
        user_info.commit()

    def remove_transaction_click():
        """ removes the transaction details of the transaction id inputted"""

        global success_img
        success_img = PhotoImage(file="Images/success_label.png")
        user_file = sqlite3.connect(f"databases/{current_sign_in}.db")
        c = user_file.cursor()
        c.execute(
            f"DELETE FROM transaction_history WHERE transaction_id={transaction_code_entry.get()}"
        )
        user_file.commit()
        Label(home_page, image=success_img, bg="#5678A9").place(x=1118, y=630)

    def remove_item_click():
        """ deletes a particular item history with it's name"""

        global success_img
        success_img = PhotoImage(file="Images/success_label.png")
        user_file = sqlite3.connect(f"databases/{current_sign_in}.db")
        c = user_file.cursor()
        c.execute(
            f"DELETE FROM inventory WHERE item_name='{item_remove_entry.get()}'"
        )
        user_file.commit()
        Label(home_page, image=success_img, bg="#5678A9").place(x=1108, y=453)

    Button(
        home_page,
        image=add_transaction_button,
        bg="#5678A9",
        command=add_transaction_click,
        bd=0,
        activebackground="#5678A9",
    ).place(x=425, y=615)
    Button(
        home_page,
        image=add_button,
        bg="#5678A9",
        command=add_item_click,
        bd=0,
        activebackground="#5678A9",
    ).place(x=994, y=270)
    Button(
        home_page,
        image=remove_button,
        bg="#5678A9",
        command=remove_item_click,
        bd=0,
        activebackground="#5678A9",
    ).place(x=978, y=453)
    Button(
        home_page,
        image=remove_button,
        bg="#5678A9",
        command=remove_transaction_click,
        bd=0,
        activebackground="#5678A9",
    ).place(x=981, y=631)
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
    """jumps to inventory page for currently signed in user"""

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

    c = sqlite3.connect(f"databases/{current_sign_in}.db")
    b = c.cursor()
    b.execute("SELECT * FROM inventory")
    d = b.fetchall()
    item_details_label = LabelFrame(home_page, bg="#5678A9").place(x=292, y=206)
    canvas_display = Canvas(item_details_label, bg="#5678A9")
    canvas_display.place(x=292, y=206, width=956, height=476)
    sb = Scrollbar(item_details_label, orient=VERTICAL, command=canvas_display.yview)
    sb.place(relx=1, rely=0, relheight=1, anchor='ne')
    canvas_display.configure(yscrollcommand=sb.set)
    canvas_display.bind('<Configure>', lambda e: canvas_display.configure(scrollregion=canvas_display.bbox("all")))
    sb_frame = Frame(canvas_display)
    sb_frame.config(bg="#5678A9")
    canvas_display.create_window((0, 0), height=(len(d) * 30 + 11), width=966, window=sb_frame)
    canvas_display.config(bg='#5678A9')

    for details in range(1, len(d)):
        place_location = 10
        print(details)
        for detail_number in d:
            Label(sb_frame, text=detail_number[0], bg="#5678A9", font=10).place(
                x=10, y=place_location
            )
            Label(sb_frame, text=detail_number[1], bg="#5678A9", font=10).place(
                x=190, y=place_location
            )
            Label(sb_frame, text=detail_number[2], bg="#5678A9", font=10).place(
                x=380, y=place_location
            )
            Label(sb_frame, text=detail_number[4], bg="#5678A9", font=10).place(
                x=650, y=place_location
            )
            Label(sb_frame, text=detail_number[3], bg="#5678A9", font=10).place(
                x=830, y=place_location
            )
            place_location += 30


def transactions_function():
    """"displays the transaction history of current user who is signed in"""


    global home_page_image
    global home_page_image, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img

    home_page = LabelFrame(root)
    home_page.destroy()

    home_page = LabelFrame(root).place(x=0, y=0)

    home_page_image = PhotoImage(file="Images/transaction_hisotry_page_img.png")

    Label(home_page, image=home_page_image).place(x=-1, y=-1)

    c = sqlite3.connect(f"databases/{current_sign_in}.db")
    b = c.cursor()
    b.execute("SELECT * FROM transaction_history")
    d = b.fetchall()
    txn_details_label = LabelFrame(home_page, bg="#5678A9").place(x=292, y=206)
    canvas_display = Canvas(txn_details_label, bg="#5678A9")
    canvas_display.place(x=292, y=206, width=956, height=476)
    sb = Scrollbar(txn_details_label, orient=VERTICAL, command=canvas_display.yview)
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
            Label(sb_frame, text=detail_number[0], bg="#5678A9", font=10).place(
                x=10, y=place_location
            )
            Label(sb_frame, text=detail_number[1], bg="#5678A9", font=10).place(
                x=180, y=place_location
            )
            Label(sb_frame, text=detail_number[2], bg="#5678A9", font=10).place(
                x=280, y=place_location
            )
            Label(sb_frame, text=detail_number[5], bg="#5678A9", font=10).place(
                x=350, y=place_location
            )
            Label(sb_frame, text=detail_number[4], bg="#5678A9", font=10).place(
                x=680, y=place_location
            )
            Label(sb_frame, text=detail_number[3], bg="#5678A9", font=10).place(
                x=580, y=place_location
            )
            Label(sb_frame, text=detail_number[7], bg="#5678A9", font=10).place(
                x=460, y=place_location
            )
            Label(sb_frame, text=detail_number[6], bg="#5678A9", font=10).place(
                x=845, y=place_location
            )
            place_location += 30

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
    """takes back to the title page"""
    title_function()


def add_customer_mbox():
    """adds customer after taking inputs"""

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

    name_entry = Entry(home_page, text=name_c_reg, bg="#5A67A8", bd=0, font=8, width=21)
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
        """add customer after eligibility check"""
        global c_add_success1, c_add_error2, c_add_error3, i
        c_add_success1 = PhotoImage(file="Images/Customer added successfully.png")
        c_add_error2 = PhotoImage(
            file="Images/Customer with this email already exists.png"
        )
        c_add_error3 = PhotoImage(
            file="Images/Customer with this number already exists.png"
        )

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

        if valid1 is True and valid2 is True:
            e = datetime.datetime.now()
            customer_code_reg = "%s%s%s%s%s%s" % (
                e.year,
                e.month,
                e.day,
                e.hour,
                e.minute,
                e.second,
            )
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
        home_page,
        image=add_button,
        bg="#5678A9",
        bd=0,
        activebackground="#5678A9",
        command=add_b_click,
    ).place(x=710, y=535)
    Button(
        home_page,
        image=add_customer,
        bg="#5678A9",
        bd=0,
        activebackground="#5678A9",
        command=add_customer_mbox,
    ).place(x=927, y=96)
    Button(
        home_page,
        image=remove_customer,
        bg="#5678A9",
        bd=0,
        activebackground="#5678A9",
        command=remove_customer_mbox,
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
    """removes a customer from the database after as specified by the user"""

    global home_page_image, class_frame_img, analytics_img, customers_img, entry_img, inventory_img, transactions_img
    global sign_out_img, add_customer, remove_customer, add_c_window, remove_c_window, remove_button
    global remove_success_img, remove_error_img
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
        """removes customer if criteria is met"""

        global remove_success_img, remove_error_img
        b = sqlite3.connect(f"databases/{current_sign_in}.db")
        print(current_sign_in)
        c = b.cursor()
        c.execute("SELECT * FROM customers")
        existing_customers = c.fetchall()
        found = False
        remove_success_img = PhotoImage(file="Images/c_removed_label.png")
        remove_error_img = PhotoImage(file="Images/c_not_found_label.png")
        for customerss in existing_customers:
            print(customerss[0])
            if customerss[0] == remove_c_code.get():
                found = True
                c.execute(
                    f"DELETE  from customers WHERE customer_code='{remove_c_code.get()}'"
                )
                b.commit()
                Label(home_page, image=remove_success_img, bg="#5678A9").place(
                    x=791, y=272
                )
                print("delete successful")
        if found is False:
            print("code not found")
            Label(home_page, image=remove_error_img, bg="#5678A9").place(x=584, y=272)

    Label(home_page, image=remove_c_window).place(x=573, y=198)

    remove_c_code = IntVar()

    code_entry = Entry(
        home_page, text=remove_c_code, bg="#5A67A8", bd=0, font=8, width=21
    )
    code_entry.place(x=606, y=238)

    Button(
        home_page,
        image=remove_button,
        bg="#5678A9",
        bd=0,
        activebackground="#5678A9",
        command=remove_c_click,
    ).place(x=696, y=275)
    Button(
        home_page,
        image=add_customer,
        bg="#5678A9",
        bd=0,
        activebackground="#5678A9",
        command=add_customer_mbox,
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
