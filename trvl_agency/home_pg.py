import sqlite3
import sys

usr = ""


def home():
    while True:
        try:
            print("***********************************************")
            print("Press 1 to make a new booking")
            print("Press 2 to view and confirm booking(s)")
            print("Press 3 to Cancel booking")
            print("Press 4 to exit!")
            print("***********************************************")
            opt = input("Please select your option: ")
            if opt == '1':  # New booking
                conn = sqlite3.connect('trvlag.db')
                c = conn.cursor()
                c.execute("SELECT DISTINCT COUNTRY_NAME FROM location")
                record = c.fetchall()
                print("Countries available:")
                index = 1
                for row in record:
                    print(index, "--", row[0])
                    index += 1
                else:
                    print("End of Results")
                while index != 0:
                    a = input("Enter the name of the country:->").strip().capitalize()
                    dates = []
                    c.execute("SELECT * FROM location WHERE COUNTRY_NAME = ?", [a])
                    if c.fetchone():
                        c.execute("SELECT * FROM location WHERE COUNTRY_NAME = ?", [a])
                        record = c.fetchall()
                        for row in record:
                            dates.append(row[2])
                            print("\nAvailable Start date:-->", row[2])
                            print("End date:-->", row[3])
                            print("Available Spots:-->", row[5])
                            print("Price per spot:-->", row[4])
                            print("")
                        else:
                            print("End of Results")
                        x = int(input("Please select your package..(Press a number between 1 to 3:)\n"))
                        if 1 <= x <= 4:
                            selected = dates[x - 1]
                            z = int(input("Enter the number of spots desired:-->"))
                            c.execute("SELECT * FROM location WHERE COUNTRY_NAME = ? AND S_DATE = ? AND SPOT_AVAILABLE < ?", [a, selected, z])
                            if c.fetchone():
                                print("Not enough spots available\ncheck available spots for selected country")
                                break
                            else:
                                c.execute("SELECT * FROM booking WHERE LOGIN = ? AND COUNTRY_NAME = ? AND S_DATE = ?", [usr, a, selected])
                                if c.fetchone():
                                    print("you already have a booking for this date\nPlease check your bookings")
                                    conn.commit()
                                    conn.close()
                                    break
                                else:
                                    c.execute("SELECT * FROM location WHERE COUNTRY_NAME = ? AND S_DATE = ?", [a, selected])
                                    rec = c.fetchone()
                                    cn = rec[1]
                                    s_date = rec[2]
                                    e_date = rec[3]
                                    l_usr = usr
                                    price = rec[4]
                                    c.execute("UPDATE location SET SPOT_AVAILABLE = SPOT_AVAILABLE - ? WHERE COUNTRY_NAME = ? AND S_DATE = ?", [z, a, selected])
                                    c.execute("INSERT INTO booking(LOGIN, COUNTRY_NAME, S_DATE, E_DATE, PRICE, SPOT) VALUES (?, ?, ?, ?, ?, ?)", [l_usr, a, s_date, e_date, price, z])
                                    conn.commit()
                                    conn.close()
                                    print("operation success")
                                    break
                        else:
                            print("You have to press 1 or 2 or 3")
                    else:
                        print("This country is not available, check and try again")
            elif opt == "2":  # bookings
                conn = sqlite3.connect('trvlag.db')
                c = conn.cursor()
                c.execute("SELECT * FROM booking WHERE LOGIN = ?", [usr])
                if c.fetchone():
                    c.execute("SELECT * FROM booking WHERE LOGIN = ?", [usr])
                    record = c.fetchall()
                    for row in record:
                        print("\nCountry:-->", row[2])
                        print("Start date:-->", row[3])
                        print("End date:-->", row[4])
                        print("Spots:-->", row[6])
                        print("Price per spot:-->", row[5])
                        print('Total:-->', round((row[6] * row[5]), 2), "\n")
                    else:
                        c.execute("SELECT SUM(PRICE*SPOT) FROM booking WHERE LOGIN = ?", [usr])
                        result = c.fetchone()
                        rslt = str(round(result[0], 2))
                        print("Grand Total: " + rslt)
                        conn.close()
                        cnfirm = input("Confirm bookings? (y or n):-->").lower()
                        if cnfirm != "y":
                            pass
                        else:
                            print("booking confirmed")
                else:
                    print("No bookings under your name")     
            elif opt == "3":  # Cancel booking
                conn = sqlite3.connect('trvlag.db')
                c = conn.cursor()
                c.execute("SELECT * FROM booking WHERE LOGIN = ?", [usr])
                record = c.fetchall()
                for row in record:
                    print("\nCountry:-->", row[2])
                    print("Start date:-->", row[3])
                    print("End date:-->", row[4])
                    print("Spots:-->", row[6])
                    print("Price per spot:-->", row[5])
                    print('Total:-->', round((row[6] * row[5]), 2), "\n")
                else:
                    print("End of Results\n")
                a = input("Enter the name of the country to cancel booking:->").strip()
                c.execute("SELECT * FROM booking WHERE LOGIN = ? AND COUNTRY_NAME = ?", [usr, a])
                if c.fetchone():
                    cnfrm = input("Are you sure want to cancel this booking?....(y or n):-->").lower()
                    if cnfrm == "y":
                        c.execute("DELETE FROM booking WHERE LOGIN = ? AND COUNTRY_NAME = ?", [usr, a])
                        conn.commit()
                        print("operation success")
                    else:
                        break
                else:
                    print("you have no booking for this country")
                
            elif opt == "4":  # exit
                print("exiting...")
                sys.exit()                     
            else:
                print("Press 1 or 2 or 3 or 4")
        except IndexError:
            print("No such dates available")       
        except sqlite3.OperationalError as e:
            print(e)
            print("Database might be locked check and run again")
            sys.exit()
        except sqlite3.IntegrityError as e:
            print(e)
            break
        except FileNotFoundError:
            print("file not existent closing in 5secs \nplease wait...")
            sys.exit()
        except PermissionError:
            print("file in use on your system process")
            sys.exit()
