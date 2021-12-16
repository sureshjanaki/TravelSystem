import sqlite3
import re
import os
import csv


# Database stuff
if os.path.exists('trvlag.db'):
    connection = sqlite3.connect('trvlag.db')
    cur = connection.cursor()
else:
    connection = sqlite3.connect('trvlag.db')
    cur = connection.cursor()
    cur.execute('''CREATE TABLE "user" (
                "USER_ID"	INTEGER NOT NULL,
                "LOGIN"	TEXT NOT NULL UNIQUE,
                "CRYPT_P"	TEXT NOT NULL,
                "ACCESS_COUNT"	INTEGER NOT NULL,
                PRIMARY KEY("USER_ID" AUTOINCREMENT))''')

    cur.execute('''CREATE TABLE "location" (
                "ID"	INTEGER NOT NULL,
                "COUNTRY_NAME"	TEXT NOT NULL,
                "S_DATE"    TEXT NOT NULL,
                "E_DATE"    TEXT NOT NULL,
                "PRICE"	FLOAT NOT NULL,
                "SPOT_AVAILABLE" INTEGER NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT))''')

    cur.execute('''CREATE TABLE "booking" (
                "ID"	INTEGER NOT NULL,
                "LOGIN"	TEXT NOT NULL,
                "COUNTRY_NAME"	TEXT NOT NULL,
                "S_DATE"    TEXT NOT NULL,
                "E_DATE"    TEXT NOT NULL,
                "PRICE"	FLOAT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT))''')

    cur.execute("INSERT INTO location(COUNTRY_NAME,S_DATE,E_DATE,PRICE,SPOT_AVAILABLE) VALUES ('Canada', '2021-01-30', '2021-04-30', '1200', '5')")
    cur.execute("INSERT INTO location(COUNTRY_NAME,S_DATE,E_DATE,PRICE,SPOT_AVAILABLE) VALUES ('Canada', '2021-05-30', '2021-08-30', '1200', '5')")
    cur.execute("INSERT INTO location(COUNTRY_NAME,S_DATE,E_DATE,PRICE,SPOT_AVAILABLE) VALUES ('Canada', '2021-09-30', '2021-12-30', '1200', '5')")
    cur.execute("INSERT INTO location(COUNTRY_NAME,S_DATE,E_DATE,PRICE,SPOT_AVAILABLE) VALUES ('Usa', '2021-01-30', '2021-04-30', '1300', '5')")
    cur.execute("INSERT INTO location(COUNTRY_NAME,S_DATE,E_DATE,PRICE,SPOT_AVAILABLE) VALUES ('Usa', '2021-05-30', '2021-08-30', '1300', '5')")
    cur.execute("INSERT INTO location(COUNTRY_NAME,S_DATE,E_DATE,PRICE,SPOT_AVAILABLE) VALUES ('Usa', '2021-09-30', '2021-12-30', '1300', '5')")
    cur.execute("INSERT INTO location(COUNTRY_NAME,S_DATE,E_DATE,PRICE,SPOT_AVAILABLE) VALUES ('Brazil', '2021-01-30', '2021-04-30', '1400', '5')")
    cur.execute("INSERT INTO location(COUNTRY_NAME,S_DATE,E_DATE,PRICE,SPOT_AVAILABLE) VALUES ('Brazil', '2021-05-30', '2021-08-30', '1400', '5')")
    cur.execute("INSERT INTO location(COUNTRY_NAME,S_DATE,E_DATE,PRICE,SPOT_AVAILABLE) VALUES ('Brazil', '2021-09-30', '2021-12-30', '1400', '5')")

    connection.commit()
    connection.close()


def encrypt(txt):  # encryption
    set1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    set2 = 'TIMEODANSFRBCGHJKLPQUVWXYZtimeodansfrbcghjklpquvwxyz9876543210'
    tab = str.maketrans(set1, set2)
    trans = txt.translate(tab)
    return trans


def decrypt(txt):  # decryption
    set1 = 'TIMEODANSFRBCGHJKLPQUVWXYZtimeodansfrbcghjklpquvwxyz9876543210'
    set2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    tab = str.maketrans(set1, set2)
    trans = txt.translate(tab)
    return trans


#  email validation
def email_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    while not (re.fullmatch(regex, email)):
        print("Invalid Email! Please try again!")
        email = input("Enter your email address: ")
    else:
        pass
    return email


#  password validation
def password_check(pswd):
    while not re.fullmatch(r'[A-Za-z0-9]{8,}', pswd):
        print("Invalid password! Make sure your password is at least 8 letters, including a capital letter and a number!")
        pswd = input("Enter your password: ")
    else:
        pass
    return pswd


def clean(string):  # removing space
    cleaning = string.replace(" ", "")
    return cleaning


print("***********************************************")
print("Are you a new user? Press 1 to sign up!")
print("Are you an existing user? Press 2 to login and make a booking!")
print("Press 3 to exit!")
print("")


while True:
    opt = input("Please select your option: ")
    if opt == '1':  # sign up
        email = clean(input("Enter your email address: "))
        email_add = email_check(email)
        pswd = password_check(input("Enter your password: "))
        password_encryption = encrypt(pswd)
        access_count = '0'
        connection = sqlite3.connect("trvlag.db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM user WHERE LOGIN=?", [email_add])
        if cur.fetchone():
            print("Email address already exists! Please try again!")
        else:
            cur.execute("INSERT INTO user(LOGIN, CRYPT_P, ACCESS_COUNT) VALUES (?, ?, ?)",
                        [email_add, password_encryption, access_count])
            connection.commit()
            connection.close()
            print("Welcome")

    elif opt == "2":  # login in
        email = clean(input("Enter your email address: "))
        email_add = email_check(email)
        pswd = password_check(input("Enter your password: "))
        password_encryption = encrypt(pswd)
        connection = sqlite3.connect("trvlag.db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM user WHERE LOGIN = ? and CRYPT_P = ?", [email_add, password_encryption])
        if cur.fetchone() is None:
            print("Invalid email address or password! Please try again!")
        else:
            cur.execute("UPDATE user SET ACCESS_COUNT = ACCESS_COUNT + 1 WHERE LOGIN =?", [email_add])
            cur.execute("SELECT * FROM user WHERE LOGIN=?", [email_add])
            record = cur.fetchall()
            for row in record:
                print("Access Count: ", row[3])
                connection.commit()
                connection.close()
                print("Welcome back")
    elif opt == "3":  # backup and log out
        connection = sqlite3.connect("trvlag.db")
        cur = connection.cursor()
        cur.execute("select * from user")
        with open("user.csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter="\t")
            csv_writer.writerow([i[0] for i in cur.description])
            csv_writer.writerows(cur)
        dirpath = os.getcwd() + "/user.csv"
        connection.close()
        # print("Data exported Successfully into {}".format(dirpath))
        print("See you soon!")
        print("Have a great day!")
        break

    else:  # opt validation
        print("Invalid option!")
        print("Press 1 to if you are a new user!")
        print("Press 2 to if you are an existing user!")
        print("Press 3 to exit!")
        print("")
