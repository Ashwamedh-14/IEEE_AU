'''
Owner :- Ayush Purohit
Created :- 12th January 2024

This file is the starting point for the whole program.
'''


#built in modules
from time import sleep
import logging
from logging import handlers
from os import getenv

#third party modules
from mysql.connector import connect, errors
from dotenv import load_dotenv

#self defined modules
import src.attendence as attendence
import src.members as members


#Main function starts here
def main() -> None:

    #Setting up the logger
    LOG_FORMAT = logging.Formatter("%(asctime)s: %(levelname)s: %(filename)s\n%(message)s\n") #Specifying the format of output log
    file_handle = handlers.TimedRotatingFileHandler(r'logs/root.log', "W6")
    file_handle.setLevel(logging.DEBUG)
    file_handle.setFormatter(LOG_FORMAT)
    logger = logging.getLogger(__name__)                                            #Creating Logger
    logger.addHandler(file_handle)
    logger.setLevel(logging.DEBUG)                                                  #Setting Log level
    logger.propagate = False

    logger.debug(f"Starting the program {__name__}")
    try:
        #Aesthetics only
        print("Turning on systems")
        print("Connecting with database....")
        sleep(5)

        load_dotenv()    #loading environment variables stored in .env into the running nevironment
        logger.debug(f"Host : {getenv('HOST')}\nUser : {getenv('USER')}\nPassword : {getenv('PASSWORD')}\nDatabase : {getenv('DATABASE')}")

        #inputing database details from binary file
        flag = False
        con = connect(
            host = getenv('HOST'),
            user = getenv('USER'),
            password = getenv('PASSWORD'),
            database = getenv('DATABASE')
        )

        curr = con.cursor()
        flag = True

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
                    ch = int(input("Enter your choice (1 - 3): "))
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
                break


    #In case the credentials are invalid
    except errors.DatabaseError as e:
        print("It looks like the credentials stored are invalid.")
        print("Kindly check whether your environment varables are properly configured or not")
        return

    except KeyboardInterrupt:
        logger.debug("KeyboardInterrupt was hit")
        con.rollback()
        print()

    except Exception as e:
        flag = False
        logger.critical(f"Was not able to connect to database\n{e}", exc_info = True)
        print(f"The following error occured:\n{repr(e)}") #To indicate what could have potentially caused the crash
        return

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