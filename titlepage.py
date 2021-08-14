from tkinter import *

from PIL import ImageTk, Image

root = Tk()
root.geometry("1280x720")
root.config(bg="#5678A9")


def sign_in_page_function():
    """ sign in function """

    global titlepagef, sign_in_page_image, sign_in_page_background, back_btn_img

    titlepagef.destroy()

    username_signin = StringVar()
    username_signin.set("Username")

    sign_in_page = LabelFrame(root, width=1280, height=720)
    sign_in_page.place(x=0, y=0)

    sign_in_page_image = PhotoImage(file="Images/signinpage.png")
    sign_in_page_background = Label(
        sign_in_page, image=sign_in_page_image, width=1280, height=720
    )
    sign_in_page_background.place(x=-3, y=-3)

    def clear_un_sign_in(event):
        if username_signin.get() == "Username":
            username_signin.set("")

    un_sign_in = Entry(sign_in_page, text=username_signin, bg="#5A67A8", bd=0, font=13, width=17)
    un_sign_in.place(x=535, y=302)
    un_sign_in.bind("<Button-1>", clear_un_sign_in)

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
    )
    register_button.place(x=514, y=342)


title_function()  # title page initiation
mainloop()
