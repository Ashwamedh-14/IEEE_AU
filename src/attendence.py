#In-built libraries
from datetime import datetime
import logging
from logging import handlers

#Third Party libraries
from mysql.connector import connection, cursor, errors

#Self made libraries
from src.Support_Files.Person import Employee
from src.Support_Files import cleaning as clean
from src.Support_Files.printing import print_box

#Setting Up the Logger
LOG_FORMAT = logging.Formatter("%(asctime)s: %(levelname)s: %(filename)s: %(funcName)s\n%(message)s\n")
file_handle = handlers.TimedRotatingFileHandler("./logs/Attendence.log", "W6")
file_handle.setFormatter(LOG_FORMAT)
file_handle.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(file_handle)
logger.setLevel(logging.DEBUG)
logger.propagate = False

#This function exists to turn table rows into manageable employee class
def put_emp_data(data_list: list[tuple[str | int | datetime]]) -> Employee | list[Employee]:
    l = []
    for i in data_list:
        logger.info(f"Data in:\n{i}")
        emp = Employee(i[1], i[2], i[0], i[4], i[3],i[5], i[6], i[7])
        logger.info(f"Data out:\n{str(emp)}")
        l.append(emp)
    if len(l) == 1:
        return l[0]
    return l

#The Function that takes attendence of the members
def take_attendence(con: connection.MySQLConnection, curr: cursor.MySQLCursor):
    curr.execute('''SELECT EMP_ID, CONCAT_WS(' ',First_NAME,SURNAME),
                 EMP_DOB, ROLE_ID, DOJ, CONTACT_INFO, EMAIL_ID, FOOD_PREFERENCE
                 FROM EMPLOYEES ORDER BY ROLE_ID ''')      #Getting the full details of all students
    emp_list = curr.fetchall()
    emp_list: list[Employee] = put_emp_data(emp_list)              #Compiling all rows into list of Employee objects
    curr.execute("select date(now())")
    date: datetime = curr.fetchone()[0]                            #Getting the current Date
    logger.info(f"Date that was fetched: {date}")

    while True:
        event: str = input("Enter the Event ID, or press enter to exit: ")
        try:
            logger.info(f"Event Id that was input {event}")
        except UnboundLocalError as e:
            logger.debug("Pressed enter to exit")

        if event == None:
            return
        elif event.isnumeric():       #To make sure only numbers are not enterred
            print("There is no distinction. Please provide")
            continue
        curr.execute('Select event_id from events where event_id = %s', (event,))      #To see whether such an id exists or not
        res = curr.fetchone()
        logger.info(f"Result from checking for the same Event ID in Database: {res}")
        if res == None:             #ID not found
            print("Event ID does not exist")
            continue
        break
    print()

    print("Type P for Present, A for Absent or N/A, No for not required")
    print(f"Today's date: {date:%d %B %Y}")
    print(f"{'Student ID':<12}{"Student Name":<40}{"Student Role":<22}{"Presence":<10}")
    
    i = 0
    while i != len(emp_list):    #So that if there is error in input, we can continue from the same person
        try:
            role = curr.execute(f"select role_name from role where role_id = '{emp_list[i].get_role()}'")
            role = curr.fetchone()[0]
            logger.info(f"Role of person with Employee ID {emp_list[i].get_empID()}: {role}")
            presence = input(f"{emp_list[i].get_empID():<12}{emp_list[i].get_name():<40}{role:<22}")
        
            presence = presence.title().strip()
            logger.info(f"{emp_list[i].get_empID()} was marked {presence} for event {event}")
            if presence not in ('A', 'P', 'Absent', 'Present', 'N/A', 'No'):        #To accept only valid inputs
                raise ValueError("Attendence is only accepted in A/P format")
            presence = presence[0]
            reason = None
            
            if presence == 'N':          #If the person is not supposed to be there for that event
                continue
            
            if presence == "A":                                 #If the person is absent on the event
                reason = input("What is the reason\n").strip()
                print()

            if type(reason) == str and reason.isnumeric():
                raise ValueError("Kya kar rha hai re. Valid reason only, not number nonsense")
            if reason == '':        #If the user does not give input, default is this
                reason = "No specific reason"

            curr.execute("insert into attendence values(%s, %s, %s, %s, %s)", (date.strftime(r"%Y-%m-%d"),
                         emp_list[i].get_empID(), presence, reason, event))
            logger.info(f"Date: {date.strftime(r"%Y-%m-%d")}\nEmployee ID: {emp_list[i].get_empID()}\nPresence: {presence}\nReason: {reason}\nEvent: {event}")
            
        except errors.IntegrityError as e:      #Usually only same day attendence twice problem, might be some other constraint
            print()
            print("You have already filled attendence for today")
            logger.error(f"The following error occured\n{e}", exc_info = True)
            con.rollback()
            return

        except Exception as e:                 #If due to bad input some error occurs, like invalid input
            print()
            print("The following error occurred", repr(e), sep = '\n')
            logger.error(f"The following error occured\n{e}", exc_info = True)
            print()
            continue
        i += 1              #Only increments if no errors occur and all data was inserted successfully

    while True:
        save = input("Save attendence: ").title().strip()
        logger.info(f"Input for save: {save}")
        if save.lower() not in ("y", "n", "yes", "no"):
            print("Please enter only yes or no\n")
            continue
        break
    if save[0] == 'N':
        print("Attendence not saved\n")
        con.rollback()
        return
    else:
        print("Attendence saved\n")
        con.commit()
    print()
    
    
#This function is made to check the percentage of attendence a particular member has
def count_attendence(curr: cursor.MySQLCursor, employee: Employee) -> float:
    '''
    To count the percentage of attendence a member has
    '''
    logger.info(f"Employee Details:\n{str(employee)}")
    curr.execute(f'''select count(*) from attendence where emp_id = "{employee.get_empID()}"''')
    total_attendence: int = curr.fetchone()[0]
    logger.info(f"Total events in which {employee.get_name()} was supposed to be present: {total_attendence}")

    curr.execute(f'''select count(*) from attendence where emp_id = '{employee.get_empID()}' and presence = "P"''')

    present: int = curr.fetchone()[0]
    logger.info(f"Total number of events {employee.get_name()} was present in: {present}")
    perc_present: float = round(present / total_attendence * 100, 2)
    logger.info(f"Percentage of attendence: {perc_present}")
    return perc_present

#This function lists attendence of a particular person
def list_attendence(curr:cursor.MySQLCursor, emp_id: str):
    try:
        curr.execute('''SELECT EMP_ID, CONCAT_WS(' ',First_NAME,SURNAME),
                    EMP_DOB, ROLE_ID, DOJ, CONTACT_INFO, EMAIL_ID, FOOD_PREFERENCE
                    FROM EMPLOYEES WHERE EMP_ID = %s''', (emp_id,))
        data = curr.fetchall()
        logger.info(f"Data obtained from database for {emp_id}:\n{data}")
        if data == None:
            print(f"No attendence taken for {emp_id}")
            return
        emp: Employee = put_emp_data(data)
        curr.execute('''select A.Date, A.Presence, E.event_name, A.Reason from Attendence A natural join Events E where emp_id = %s order by emp_id'''
                     , (emp.get_empID(),))
        d = curr.fetchall()
        logger.info(f"Attendence data obtained:\n{d}")
        if d != []:
            data = [("Date", "Attendence", "Event", "Reason for not Attending")]
            data.extend(d)
            r_length = 0
            for i in range(1, len(data)):
                if data[i][3] == None:
                    data[i] = data[i][0].strftime(r'%d-%m-%Y'), data[i][1], data[i][2], "Not Applicable"
                    r_length = max(r_length, 14)
                else:
                    r_length = max(r_length, len(data[i][3]))
                    data[i] = data[i][0].strftime(r'%d-%m-%Y'), data[i][1], data[i][2], data[i][3]
        print(f"Name           : {emp.get_name()}")
        print(f"ID             : {emp.get_empID()}")
        print(f"Date of Joining: ", end = '')

        try:
            print(emp.get_DOJ_str())
        except ValueError:
            print("Not Passed")
        
        curr.execute('select max(length(E.event_name)), max(length(A.Reason)) from attendence A natural join events E where A.emp_id = %s',
                     (emp.get_empID(),))
        length1, length2 = curr.fetchone()
        if length2 == None:
            length2 = 0
        logger.info(f"Length of longest Event Name {emp.get_name()} was in = {length1}")
        
        if d == []:
            print("Meeting not yet conducted")
        else:
            length1 = max(length1, 5)
            length2 = max(length2, 24, r_length)
            perc = count_attendence(curr, emp)
            print(f"Attendence %   : {perc}")
            print_box(data, (10, 10, length1, length2), 4)
    except ValueError as e:
        print("The following exception occured:", repr(e), sep = '\n')
        logger.error(f"The following error occurred:\n{e}", exc_info = True)
        print()

#This function is used to list attendence details of all members
def list_attendence_all(curr: cursor.MySQLCursor):
    curr.execute('select emp_id from employees order by role_id')
    ids = curr.fetchall()
    for i in ids:
        list_attendence(curr, i[0])
        print()

#This function is to update the attendence of a particular member
def update_attendence(curr: cursor.MySQLCursor, empid: str, date: str, upd: str):
    logger.info(f"Date: {date}, Employee ID: {empid}, Update: {upd}")
    if type(date) != str:
        logger.error("Date was not passed as a string")
        raise TypeError("Date must be of type string")
    upd = upd.title()
    if upd not in ('P', 'A', 'Present', 'Absent'):
        logger.error("Upd was not valid, i.e., P, A, Present or Absent")
        raise ValueError("Only Present or Absent allowed")
    reason = None
    if upd == 'A':
        reason = input("What was the reason:\n")
    curr.execute('update attendence set presence = %s, reason = %s where date = %s and emp_id = %s',
                 (upd, reason, date, empid))
    logger.info(f"Date: {date}, Employee ID: {empid}, Upd: {upd}, Reason: {reason}")
    print("Attendence successfully updated\n")

def attend_main(con: connection.MySQLConnection, curr: cursor.MySQLCursor):
    logger.debug("Inside Attendence Module")
    while True:
        print("Select one of the following:")
        print("1. Take Attendence")
        print("2. Update Attendence")
        print("3. List Attendence of Individual")
        print("4. List Attendence of All")
        print("5. Go back")
        while True:
            try:
                ch = int(input("Enter your choice (1 - 5): "))
                logger.info(f"Option number chosen is = {ch}")
                if ch < 1 or ch > 5:
                    print("Valid choices are only between 1 and 5 inclusively")
                else:
                    break
            except ValueError:
                logger.error("A number was not enterred")
                print("Kindly enter a number only")
        print('\n')
        
        if ch == 1:
            try:
                logger.debug("Started taking attendence")
                take_attendence(con, curr)
                logger.debug("Attendence taken successfully")
            except KeyboardInterrupt:
                logger.debug("KeyboardInterrupt was hit")
                print('\n')

        
        elif ch == 2:
            empid = input("Enter the id of the person: ")
            empid = empid.upper().strip()
            date = input("Enter the date of attendence in YYYY-MM-DD format: ")
            date = clean.clean_string(date)
            logger.info(f"Input Employee Id = {empid} and date = {date}")
            while True:
                upd = input("Set attendence to Absent (A) or Present (P): ")
                logger.info(f"Input upd = {upd}")
                if upd.title() not in ('A', 'Absent', 'P', 'Present'):
                    print("Kindly enter Absent or Present Only")
                    continue
                break
            print()
            try:
                curr.execute("select * from attendence where emp_id = %s and date = %s", (empid, date))
                qh = curr.fetchone()
                logger.info(f"The following data was retrived from database for Employee: {empid} and date: {date}\n{qh}")
                if qh:
                    update_attendence(curr, empid, date, upd)
                    logger.debug("Attendence updated successfully")
                    con.commit()
                else:
                    logger.debug("Attendence could not be updated")
                    print("Error 404: Entry not found") 
                    print("Check whether the input date and ID is correct\n")
                    print()
            except Exception as e:
                logger.critical(f"The following error occured:\n{e}", exc_info = True)
                print("The following exception occurred\n", repr(e))
            con.rollback()

        elif ch == 3:
            empid = input("Enter the Student ID: ")
            empid = empid.upper()
            print()
            list_attendence(curr, empid)
            print()

        elif ch == 4:
            list_attendence_all(curr)
            print()
        
        else:
            logger.debug("Exiting Attendence module\n" + "=" * 60 + '\n')
            return
                