from mysql.connector import connect
from pickle import load
from time import sleep

import attendence


def main():
    try:
        #Aesthetics only
        print("Turning on systems")
        print("Connecting with database....")
        sleep(5)

        #inputing database details from binary file
        try:
            with open("cred.dat", 'rb') as myfile:
                data: dict = load(myfile)               #data is stored in a dictionary
                con = connect(host = data['host'],
                              user = data['user'],
                              password = data['password'],
                              database = data['database'])
        except Exception as e:
            print("The following error occured:", repr(e)) #To indicate what could have potentially caused the crash
            return
        curr = con.cursor()
        print("Connection established: ")

        #Main menu of program
        while True:        
            print("Kindly enter anyone of the actions below:")
            print('1. Take attendence')
            print('2. Exit')

            while True:
                #To input only correct values
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
                print() #To maintain some space between one section and another

            else:
                print()
                break

    except KeyboardInterrupt:
        con.rollback()
        print()

    finally:
        curr.close()  #Operations here for esuring closing of cursor and database
        con.close()
        print("Closing Database")
        print("Switching off systems...")
        sleep(5)


#function call
if __name__ == '__main__':
    main()