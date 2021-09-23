import sys
import os
import sys
import hashlib
import mysql.connector
import time

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="timanttikuutio",
    password="Falcon5547#",
    database="logintest"
)
mycursor = mydb.cursor(buffered=True)


def cls():
    if sys.platform == "linux":
        os.system("clear")
    else:
        os.system("cls")


def login():
    login_username = input("Please enter your username: ")
    login_password = input("Please enter your password: ")

    query = f"SELECT username, email, password, salt, id FROM users WHERE username = %s"

    mycursor.execute(query, (login_username, ))
    try:
        username, email, key, salt, user_id = mycursor.fetchone()
    except TypeError:
        print("Invalid Username or Password.")
        input("Press Enter to continue...")
        cls()
        options()

    salted_pw = hashlib.pbkdf2_hmac("sha256", login_password.encode("utf-8"), salt, 100000)

    if login_username == username and key == salted_pw:
        # thing to run when logged in successfully
        print("Logged in successfully")
        cls()
        loggedIn(username, email, user_id)
    else:
        print("Login failed, wrong username or password")
        input("Press Enter to continue...")
        cls()
        options()


def register():
    new_username = input("please pick a username: ")
    new_email = input("please enter your email: ")
    new_password = input("please pick a password: ")

    salt = os.urandom(32)
    salted_pw = hashlib.pbkdf2_hmac("sha256", new_password.encode("utf-8"), salt, 100000)

    query = "INSERT INTO users (username, email, password, salt) VALUES (%s, %s, %s, %s)"
    mycursor.execute(query, (new_username, new_email, salted_pw, salt))
    mydb.commit()
    print("User successfully created! insert id:", mycursor.lastrowid)
    login()


def loggedIn(user, email, user_id):
    print("1. show username + email")
    print("2. reset password")
    print("3. change username")
    print("4. go back to main page")
    actions = input("please pick 1, 2, 3 or 4: ")
    if actions == "1":
        cls()
        print(f"username: {user} and your id is: {user_id}")
        print(f"email: {email}")
        input("Press Enter to continue...")
        cls()
        loggedIn(user, email, user_id)
    elif actions == "2":
        cls()
        new_password = input("please enter a new password for your account: ")

        salt = os.urandom(32)
        salted_pw = hashlib.pbkdf2_hmac("sha256", new_password.encode("utf-8"), salt, 100000)

        query = "UPDATE users SET password = %s, salt = %s WHERE id = %s"
        mycursor.execute(query, (salted_pw, salt, user_id))
        mydb.commit()
        cls()
        print(f"password successfully changed, new password is: {new_password}")
        input("Press Enter to relog...")
        cls()
        options()
    elif actions == "3":
        cls()
        new_username = input("please enter the new username for your account: ")
        query = "UPDATE users SET username = %s WHERE id = %s"
        mycursor.execute(query, (new_username, user_id))
        mydb.commit()

        cls()
        print(f"username successfully changed, new username is: {new_username}")
        input("Press Enter to relog...")
        cls()
        options()
    elif actions == "4":
        cls()
        options()


def options():
    print("1. login")
    print("2. register")
    inp = input("please pick 1 or 2: ")
    if inp == "1":
        cls()
        login()
    elif inp == "2":
        cls()
        register()
    else:
        print("please only select 1 or 2")
        input("Press Enter to continue...")
        cls()
        options()


options()
