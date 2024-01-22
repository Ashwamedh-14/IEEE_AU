from mysql.connector import  errors, cursor, connect
from pickle import load
from time import sleep

import attendence as attendence


def main():
    try:

        print("Turning on systems")
        sleep(5)
        print("Connecting with database....")
        sleep(5)

        try:
            with open("cred.dat", 'rb') as myfile:
                data: dict = load(myfile)
                con = connect(host = data['host'],
                              user = data['user'],
                              password = data['password'],
                              database = data['database'])
        except Exception as e:
            print("The following error occured:", repr(e))
            return
        curr = con.cursor()
        print("Coonnection established: ")

        while True:        
            print("Kindly enter anyone of the actions below:")
            print('1. Take attendence')
            print('2. Exit')

            while True:
                try:
                    ch = int(input("Enter your choice (1, 2): "))
                    if ch != 1 and ch != 2:
                        print("Enter either 1 or 2 only")
                    else:
                        print()
                        break
                except ValueError:
                    print("Kindly enter only numbers")
                print()

            if ch == 1:
                attendence.attend_main(con, curr)
                print()

            else:
                print()
                break

    except KeyboardInterrupt:
        print()

    finally:
        curr.close()
        con.close()
        print("Closing Database")
        sleep(5)
        print("Switching off systems...")
        sleep(7)


if __name__ == '__main__':
    main()