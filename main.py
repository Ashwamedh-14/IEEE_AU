#built in modules
from pickle import load
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
        except Exception as e:
            logger.critical(f"Was not able to connect to database\n{e}", exc_info = True)
            print("The following error occured:", repr(e)) #To indicate what could have potentially caused the crash
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
                    ch = int(input("Enter your choice (1, 2): "))
                    if ch != 1 and ch != 2:
                        print("Enter either 1 or 2 only")
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
        curr.close()  #Operations here for esuring closing of cursor and database
        con.close()
        print("Closing Database")
        print("Switching off systems...")
        logger.debug('Program Exited\n' + '=' * 60 + '\n')
        sleep(5)


#function call
if __name__ == '__main__':
    main()