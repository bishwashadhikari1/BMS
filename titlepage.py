from tkinter import *
from crypt import *
import sqlite3

root = Tk()  # creates window
root.geometry("1280x720")
root.config(bg="#5678A9")
sign_in_page = LabelFrame(root)
register_page = LabelFrame(root)

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

    register_page_image = PhotoImage(file='Images/registrationpage.png')
    register_page_background = Label(register_page, image=register_page_image, width=1280, height=720)
    register_page_background.place(x=-3, y=-3)

    un_entry = Entry(register_page, text=username_register, bg="#5A67A8", bd=0, font=13, width=19)
    pw_entry = Entry(register_page, text=password_register, bg="#5A67A8", bd=0, font=13, width=19)
    f_name_entry = Entry(register_page, text=f_name_register, bg="#5A67A8", bd=0, font=13, width=19)
    l_name_entry = Entry(register_page, text=l_name_register, bg="#5A67A8", bd=0, font=13, width=19)
    e_mail_entry = Entry(register_page, text=e_mail_register, bg="#5A67A8", bd=0, font=13, width=19)

    un_entry.place(x=524, y=155)
    pw_entry.place(x=524, y=228)
    f_name_entry.place(x=524, y=298)
    l_name_entry.place(x=524, y=374)
    e_mail_entry.place(x=524, y=447)


    Checkbutton(register_page,
                bg="#5A67A8",
                bd=0,
                width=1,
                height=1,
                activebackground="#5A67A8",
                variable=tnc_check,
                onvalue=1,
                offvalue=0,
                ).place(x=512, y=534)

    button_is = "OFF"

    error_frame = LabelFrame(register_page)
    error_frame.place(x=0, y=0)

    def register_btn():
        global error5_img, error3_img, error2_img, error1_img, error4_img

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

        a = sqlite3.connect('databases/users_credentials.db')
        c = a.cursor()
        c.execute("SELECT * FROM reg_info")
        existing_users = c.fetchall()

        valid4 = True
        for user in existing_users:
            usrname = user[0]
            if un_encrypted == usrname:
                error4_label = Label(register_page, image=error4_img, bg= "#5678A9")
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
            c.execute("INSERT INTO reg_info VALUES (:username, :password, :first_name, :last_name, :email)", {
                'username': un_encrypted,
                'password': pw_encrypted,
                'first_name': f_name_encrypted,
                'last_name': l_name_encrypted,
                'email': e_mail_encrypted
            })
            a.commit()
            a.close()

    def back_btnnm():
        """takes user back to title page"""

        sign_in_page.destroy()
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

    Button(register_page, image=register_button_image, bg="#5678A9", bd=0, activebackground="#5678A9",
           command=register_btn).place(x=526, y=612)

def sign_in_page_function():
    """ sign in page function """

    global titlepagef, sign_in_page_image, sign_in_page_background, back_btn_img

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

    un_sign_in = Entry(sign_in_page, text=username_signin, bg="#5A67A8", bd=0, font=13, width=17)
    un_sign_in.place(x=535, y=302)
    un_sign_in.bind("<Button-1>", clear_un_sign_in)

    password_sign_in = Entry(sign_in_page, text=password_signin, bg="#5A67A8", bd=0, font=13, width=17, show="*")
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

        pass

    Button(
        sign_in_page,
        image=sign_in_button_image,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=submit_sign_in
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
        command=register_page_function
    )
    register_button.place(x=514, y=342)


title_function()  # title page initiation
mainloop()
