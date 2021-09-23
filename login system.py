from os import error
from os import system
from tkinter.constants import N
import mysql.connector
import time
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)
mycursor = mydb.cursor(buffered=True)
cls = lambda: system('cls')



def login():
    try:
        mycursor.execute("USE logintest")

        login_username = input("Please enter your username: ")
        login_password = input("Please enter your password: ")
        
        check_login = f"SELECT username, id FROM users WHERE username = '{login_username}'"
        check_password = f"SELECT password, id FROM users WHERE password = '{login_password}'"

        mycursor.execute(check_login)
        username_result = mycursor.fetchone()
        global userr, userrId
        userr, userrId = username_result

        mycursor.execute(check_password)
        password_result = mycursor.fetchone()
        global passr, passId
        passr, passId = password_result
        
        if login_username == userr and login_password == passr and userrId == passId:
            #thing to run when logged in successfully
            print("Logged in successfully")
            input("Press Enter to continue...")
            cls()
            loggedIn()
        else: 
            print("Login failed, wrong username or password")
            input("Press Enter to continue...")
            cls()
            options()
    except:
        print("Login failed, wrong password or username")
        input("Press Enter to continue...")
        cls()
        options()
        
    
def register():
    mycursor.execute("USE logintest")
    new_username = input("please pick a username: ")
    new_email = input("please enter your email: ")
    new_password = input("please pick a password: ")

    insert_new_user = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    new_user = (new_username, new_email, new_password)
    mycursor.execute(insert_new_user, new_user)
    mydb.commit()
    print("User successfully created! insert id:", mycursor.lastrowid)
    
def loggedIn():
    try:
        check_email = f"SELECT email, id FROM users WHERE id = '{userrId}'"
        mycursor.execute(check_email)
        email_result = mycursor.fetchone()
        emailr, emailrId = email_result
        print("1. show username + email")
        print("2. reset password")
        print("3. change username")
        print("4. go back to main page")
        actions = input("please pick 1 or 2: ")
        if actions == "1":
            cls()
            print(f'username: {userr} and your id is: {userrId}')
            print(f'email: {emailr}')
            input("Press Enter to continue...")
            cls()
            loggedIn()
        elif actions == "2":
            cls()
            mycursor.execute("USE logintest")
            new_pass = input("please enter a new password for your account: ")
            new_pass_sql = "UPDATE users SET password = %s WHERE password = %s AND id = %s"
            placeholders_new_password = (new_pass, passr, emailrId)
            mycursor.execute(new_pass_sql, placeholders_new_password)
            mydb.commit()
            cls()
            print(f"password successfully changed, new password is: {new_pass}")
            input("Press Enter to continue...")
            cls()
            loggedIn()
        elif actions == "3":
            cls()
            mycursor.execute("USE logintest")
            new_username = input("please enter the new username for your account: ")
            new_username_sql = "UPDATE users SET username = %s WHERE username = %s AND id = %s"
            placeholders_new_username = (new_username, userr, emailrId)
            mycursor.execute(new_username_sql, placeholders_new_username)
            mydb.commit()
            cls()
            print(f"username successfully changed, new username is: {new_username}")
            input("Press Enter to continue...")
            cls()
            loggedIn()
        elif actions == "4":
            cls()
            options()
    except Exception as e:
        print(e)
    

def options():
    try:
        print("1. login")
        print("2. register")
        options = input("please pick 1 or 2: ")
        if options == "1":
            cls()
            login()
        elif options == "2":
            cls()
            register()
        elif options == '':
            print("please select 1 or 2 only")
            input("Press Enter to continue...")
            cls()
            options()
        else: 
            print("please only select 1 or 2")
            input("Press Enter to continue...")
            cls()
            options()
    except:
        print("please only enter the numbers 1 or 2")
        input("Press Enter to continue...")
        cls()
        options()
options()
