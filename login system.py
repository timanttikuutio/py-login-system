from os import error
import mysql.connector
mydb = mysql.connector.connect(
  host="",
  user="",
  password=""
)
mycursor = mydb.cursor(buffered=True)

def login():
    try:
        mycursor.execute("USE logintest")
        login_username = input("Please enter your username or email: ")
        login_password = input("Please enter your password: ")
        
        check_login = f"SELECT username, id FROM users WHERE username = '{login_username}'"
        check_password = f"SELECT password, id FROM users WHERE password = '{login_password}'"

        mycursor.execute(check_login)
        username_result = mycursor.fetchone()
        userr, userrId = username_result
            
        mycursor.execute(check_password)
        password_result = mycursor.fetchone()
        passr, passId = password_result
        
        if login_username == userr and login_password == passr and userrId == passId:
            print("Logged in successfully")
        else: 
            print("Login failed, wrong username or password")
    except:
        print("Login failed, wrong password or username")
        
    
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
    

def options():
    try:
        print("1. login")
        print("2. register")
        options = input("please pick 1 or 2: ")
        if "1" in options:
            login()
        elif "2" in options:
            register()
        else: 
            print("please only select 1 or 2")
            options()
    except:
        print("please only enter the numbers 1 or 2")
        options()
options()
