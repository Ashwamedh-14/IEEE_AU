#built in modules
from pickle import load, dump
from time import sleep
import logging
from logging import handlers

#third party modules
from mysql.connector import connect

#self defined modules
import src.attendence as attendence
import src.members as members

#Setting up the logger
LOG_FORMAT = logging.Formatter("%(asctime)s: %(levelname)s: %(filename)s\n%(message)s\n") #Specifying the format of output log
file_handle = handlers.TimedRotatingFileHandler(r'logs/root.log', "W6")
file_handle.setLevel(logging.DEBUG)
file_handle.setFormatter(LOG_FORMAT)
logger = logging.getLogger(__name__)                                            #Creating Logger
logger.addHandler(file_handle)
logger.setLevel(logging.DEBUG)                                                  #Setting Log level
logger.propagate = False




def main():
    logger.debug(f"Starting the program {__name__}")
    try:
        #Aesthetics only
        print("Turning on systems")
        print("Connecting with database....")
        sleep(5)

        #inputing database details from binary file
        try:
            flag = True
            logger.debug("Opening the file")
            with open("cred.dat", 'rb') as myfile:
                logger.debug(f"File opened {myfile.name}")
                data: dict = load(myfile)               #data is stored in a dictionary

                logger.debug("Setting up connection with IEEE Database")
                con = connect(host = data['host'],
                              user = data['user'],
                              password = data['password'],
                              database = data['database'])
                logger.debug("Connection established")

        except FileNotFoundError as e:
            flag = False
            logger.error(f"The cred file was not there. Creating a new one...")
            d = {}
            print("Looks like you don't have a credential file")
            sleep(1)
            print("We'll set one up for you")
            sleep(1)
            print("Kindly enter all the details")
            d["host"] = input("Enter the host of the database: ")
            d["user"] = input("Enter the user of the database: ")
            d["password"] = input("Enter the password of the database: ")
            d["database"] = input("Enter the name of the database to be used: ")

            #creating file
            with open("cred.dat", "wb") as myfile:
                dump(d, myfile)
            print("Credentials saved successfully")
            print("If you want to resave the credentials. Simply delete the credential file, i.e., cred.dat")
            print("Please restart the program")
            return

        except Exception as e:
            flag = False
            logger.critical(f"Was not able to connect to database\n{e}", exc_info = True)
            print(f"The following error occured:\n{repr(e)}") #To indicate what could have potentially caused the crash
            return
        curr = con.cursor()
        print("Connection established: ")

        #Main menu of program
        while True: 
            logger.debug("Main Menu")       
            print("Kindly enter anyone of the actions below:")
            print('1. Take attendence')
            print("2. Members Related")
            print('3. Exit')

            while True:
                #To input only correct values
                try:
                    ch = int(input("Enter your choice (1, 2 or 3): "))
                    if ch < 1 or ch > 3:
                        print("Enter between 1 and 3 inclusive only")
                    else:
                        print()
                        break
                except ValueError:
                    print("Kindly enter only numbers")
                print()
                logger.info(f"Value enttered was {ch}")

            if ch == 1:
                logger.debug("Going into the attendence module")
                attendence.attend_main(con, curr)
                print() #To maintain some space between one section and another
                logger.debug("Out of the attendence Module")

            elif ch == 2:
                logger.debug("Going into the members module")
                members.members_main(con, curr)
                print() #To maintain some space between one section and another
                logger.debug("Out of members file")

            else:
                logger.debug("Closing Program")
                print()
                break

    except KeyboardInterrupt:
        logger.debug("KeyboardInterrupt was hit")
        con.rollback()
        print()

    finally:
        if not flag:
            return
        curr.close()  #Operations here for esuring closing of cursor and database
        con.close()
        print("Closing Database")
        print("Switching off systems...")
        logger.debug('Program Exited\n' + '=' * 60 + '\n')
        sleep(5)


#function call
if __name__ == '__main__':
    main()