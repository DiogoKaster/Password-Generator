# This program generates a password and saves it in a separated file. Beyond that,
# it also saves the website and the email that you used to sign with the password

from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT = ("Arial", 12, "bold")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, f"{password}")
    pyperclip.copy(password)

    return password


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_all():
    website = website_entry.get()
    email = email_entry.get()
    password = password_generator()
    new_dict = {
        website: {
            "email": email,
            "password": password
        }
    }

    user_answer = messagebox.askokcancel(title="Data", message=f"These are the details?\nWebsite: {website}\n"
                                                               f"Email: {email}\nPassword:{password}")

    website_entry.delete(0, END)
    password_entry.delete(0, END)
    email_entry.delete(0, END)
    email_entry.insert(0, "@gmail.com")

    verify_answer = verify(website, email, password)

    if user_answer and verify_answer:
        try:
            with open("passwords.json", "r") as file:
                # Reading old data
                new_file = json.load(file)
                # Updating old data with new data
                new_file.update(new_dict)
        except FileNotFoundError:
            with open("passwords.json", "w") as file:
                json.dump(new_dict, file, indent=4)  # json data has a dictionary structure, the indent is to
    # make the file readable
        else:
            with open("passwords.json", "w") as file:
                json.dump(new_file, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            email_entry.delete(0, END)
            email_entry.insert(0, "@gmail.com")


def verify(a, b, c):
    if a == "" or b == "" or c == "":
        messagebox.showinfo(title="Warning", message="There are too many empty datas.")
        return False
    else:
        return True


# --------------------- SEARCH PASSWORD SETUP ------------------------- #


def search_password():
    try:
        with open("passwords.json", "r") as file:
            new_file = json.load(file)
    except FileNotFoundError:
        print("There are no file yet")
    else:
        website = website_entry.get()
        try:
            website_dict = new_file[website]
        except KeyError:
            messagebox.showinfo(title="Warning", message=f"No {website} account is registered")
        else:
            messagebox.showinfo(title="Data", message=f"Your {website} account email is {website_dict['email']}\nYour"
                                                      f"password is {website_dict['password']}")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Generator")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=2, row=0)

Label(window, text="Website:", font=FONT).grid(column=0, row=1)
website_entry = Entry(width=33)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2)

Label(window, text="Email/Username:", font=FONT).grid(column=0, row=2)
email_entry = Entry(width=60)
email_entry.insert(0, "@gmail.com")
email_entry.grid(column=1, row=2, columnspan=3)

Label(window, text="Password:", font=FONT).grid(column=0, row=3)
password_entry = Entry(width=32)
password_entry.grid(column=1, row=3, columnspan=2)

generate_button = Button(text="Generate Password", font=FONT, command=password_generator)
generate_button.grid(column=3, row=3)

add_button = Button(text="Add", font=FONT, width=36, command=save_all)
add_button.grid(column=2, row=4, columnspan=2)

search_button = Button(text="Search", width=15, font=FONT, command=search_password)
search_button.grid(column=3, row=1)

window.mainloop()
