#built in modules
from pickle import load, dump
from time import sleep
import logging
from logging import handlers

#third party modules
from mysql.connector import connect, errors

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


def new_credential(cred_file) -> None:
    '''
    cred_file should be the buffered reader for cred.dat file which is opened in binary format with filemode 'wb'
    '''
    d = {}
    print("Kindly enter all the details")
    d["host"] = input("Enter the host of the database: ")
    d["user"] = input("Enter the user of the database: ")
    d["password"] = input("Enter the password of the database: ")
    d["database"] = input("Enter the name of the database to be used: ")
    dump(d, cred_file)
    print("Credentials saved successfully")





def main():
    logger.debug(f"Starting the program {__name__}")
    try:
        #Aesthetics only
        print("Turning on systems")
        print("Connecting with database....")
        sleep(5)

        #inputing database details from binary file
        try:
            flag = True                      # In case we meet an exception, we use this flag to skip code in finally block

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

        #If the file does not exists
        except FileNotFoundError as e:
            flag = False
            logger.error(f"The cred file was not there. Creating a new one...")
            print("Looks like you don't have a credential file")
            sleep(1)
            print("We'll set one up for you")
            sleep(1)

            #creating file
            with open("cred.dat", "wb") as myfile:
                new_credential(myfile)
            print("Credentials saved successfully")
            print("If you want to resave the credentials. Simply delete the credential file, i.e., cred.dat")
            print("Please restart the program")
            return
        
        #In case the credentials are invalid
        except errors.DatabaseError as e:
            flag = False
            print("It looks like the credentials stored are invalid.")
            ch = input("Would you like to save again? (Y / N): ")
            if ch == None:
                return
            elif ch.upper().strip() in ('Y', 'Yes'):
                with open('cred.dat', 'wb') as myfile:
                    new_credential(myfile)
                print("Kindly restart the program")
            else:
                return

        #To catch general exceptions
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
            print("3. Edit / Save credentials")
            print('4. Exit')

            while True:
                #To input only correct values
                try:
                    ch = int(input("Enter your choice (1 - 4): "))
                    if ch < 1 or ch > 4:
                        print("Enter between 1 and 4 inclusive only")
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

            elif ch == 3:
                logger.debug("Editing / Saving credential for database")
                with open('cred.dat', 'wb') as myfile:
                    new_credential(myfile)
                print("To fully save the cred file, kindly exit the program and restart")

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