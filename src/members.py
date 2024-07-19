#Built-In Libraries
import logging
from logging import handlers

#3rd Party library
from mysql.connector import connection, cursor, errors

#self defined modules
from src.printing import print_box
from src.Person import Employee, FOOD
from src.attendence import put_emp_data, count_attendence

import src.cleaning as clean

#setting up the file_handle
LOG_FORMAT = logging.Formatter("%(asctime)s: %(levelname)s: %(filename)s: %(funcName)s\n%(message)s\n")
file_handle = handlers.TimedRotatingFileHandler('./logs/members.log', 'W6')
file_handle.setLevel(logging.DEBUG)
file_handle.setFormatter(LOG_FORMAT)

#setting the logger
logger = logging.getLogger(__name__)
logger.addHandler(file_handle)
logger.setLevel(logging.DEBUG)
logger.propagate = False

#Constants
DIVISION = {'OBS': 'a', 'HEADS': 'b', 'MEMBER': 'c', "WIE": 'w'}
TEAM = {1: ('01', 'RAS'), 
        2: ('02', 'Technical'), 
        3: ('03', 'Logistics'), 
        4: ('04', 'Social Media'), 
        5: ('05', 'CSE'), 
        6: ('06', 'Content'), 
        7: ('07', 'Graphics')}

#Main Functions start
#This function checkes whether a particular member is present or not
def exists(curr: cursor.MySQLCursor, empid: str) -> bool:
    logger.info("Empid that was passed is: %s", empid)
    if type(empid) != str:
        logger.error("Incorrect type was passed to empid with values %s", empid)
        raise TypeError("Incorrect type passed")
    
    curr.execute("select emp_id from employees where emp_id = %s", (empid,))
    data = curr.fetchone()
    logger.info(f"The data obtained from database is:\n{data}")

    if data:
        return True
    return False

#Display members according to their team
def display_members(curr: cursor.MySQLCursor, team: int | str | None, hierarchy: str | None) -> None:
    '''
    Pass a '*' in team if all members are required
    Else pass the team number

    Valid inputs in hierarchy are OBS, Heads, Members, WIE (case-insensitive)

    Team is only applicable if hierarchy is Heads, Members or given as '*' in which case hierarchy is ignored
    '''


    logger.info("Team passed is %s with type %s and hierarchy passed is %s with type %s", team, type(team), hierarchy, type(hierarchy))
    if team != None and type(team) not in (str, int):
        raise TypeError("Incorrect type passed to team")
    if type(team) == int and (team < 1 or team > 7):
        raise ValueError("Team can only take values None, '*' or integers from 1 to 7")

    if hierarchy != None and type(hierarchy) != str:
        raise TypeError("Incorrect type passed to hierarchy. Ensure its string type")
    if hierarchy != None and hierarchy.upper() not in DIVISION.keys():
        raise ValueError("Incorrect Value passed to hierarchy. Should be OBS, Heads, Members or WIE only")

    if team == None:
        team = ''
    if hierarchy == None:
        hierarchy = ''
    
    #In case all members are required
    if team == '*':
        head = ('Student ID', 'Student Name', 'Department')
        curr.execute(f'''select emp_id, concat_ws(' ',first_name,surname), role_name 
                     from employees natural join role  
                     order by role_id, emp_id''')
        data: list[tuple[str,...]] = [head] + curr.fetchall()

        #selecting the maximum length of name in database
        curr.execute(f"select max(length(concat_ws(' ',first_name,surname))) from employees")
        max_name: int = curr.fetchone()[0]
        if max_name == None:
            max_name = 0
        max_name = max(len('Member Name'), max_name)
        logger.info("Maximum length of name is: %s", max_name)

        #selecting maximum length of role_name in database
        curr.execute(f'''select max(length(role_name)) 
                     from role''')
        max_role: int = curr.fetchone()[0]
        if max_role == None:
            max_role = 0
        max_role = max(len("Team"), max_role)
        logger.info("Maximum length of role name is: %s", max_role)
        length = (10, max_name, max_role)

    #In case only members are required
    elif hierarchy.lower() == 'member':
        head: tuple = ('Member ID', 'Member Name', 'Team')
        curr.execute(f'''select emp_id, concat_ws(' ',first_name,surname), role_name
                     from employees natural join role
                     where lower(role_id) like 'c{TEAM[team][0]}%'
                     order by role_id, emp_id''')
        data: list[tuple[str, ...]] = [head] + curr.fetchall()
        
        #selecting the maximum length of name in database
        curr.execute(f'''select max(length(concat_ws(' ',first_name,surname))) from employees where lower(role_id) like "c{TEAM[team][0]}%"''')
        max_name: int = curr.fetchone()[0]
        if max_name == None:
            max_name = 0
        max_name = max(len('Member Name'), max_name)
        logger.info(f"Maximum  length of name column is {max_name}")
        
        #selecting maximum length of role_name in database
        curr.execute(f'''select max(length(role_name)) from role where lower(role_id) like 'c{TEAM[team][0]}' ''')
        max_role: int = curr.fetchone()[0]
        if max_role == None:
            max_role = 0
        max_role = max(len("Team"), max_role)
        logger.info(f"Maximum length of role_name column is: {max_role}")
        length = (9, max_name, max_role)

    elif hierarchy.lower() == 'heads':
        head: tuple = ('Head ID', 'Head Name', 'Team')
        curr.execute(f'''select emp_id, concat_ws(' ',first_name,surname), role_name
                     from employees natural join role
                     where lower(role_id) like 'b{TEAM[team][0]}%'
                     order by role_id, emp_id''')
        data: list[tuple[str, ...]] = [head] + curr.fetchall()
        
        #selecting the maximum length of name in database
        curr.execute(f'''select max(length(concat_ws(' ',first_name,surname))) from employees where lower(role_id) like "b{TEAM[team][0]}%"''')
        max_name: int = curr.fetchone()[0]
        if max_name == None:
            max_name = 0
        max_name = max(len('Member Name'), max_name)
        logger.info(f"Maximum  length of name is {max_name}")
        
        #selecting maximum length of role_name in database
        curr.execute(f'''select max(length(role_name)) from role where lower(role_id) like 'b{TEAM[team][0]}' ''')
        max_role: int = curr.fetchone()[0]
        if max_role == None:
            max_role = 0
        max_role = max(len("Team"), max_role)
        logger.info(f"Maximum length of role_name is: {max_role}")
        length = (9, max_name, max_role)

    elif hierarchy.lower() == 'wie':
        head: tuple = ('WIE ID', 'WIE Name', 'Chair')
        curr.execute('''select emp_id, concat_ws(' ',first_name,surname), role_name
                     from employees natural join role
                     where lower(role_id) like 'w%'
                     order by role_id, emp_id''')
        data: list[tuple[str, ...]] = [head] + curr.fetchall()
        
        #selecting the maximum length of name in database
        curr.execute(f'''
                     select max(length(concat_ws(' ',first_name,surname))) 
                     from employees where lower(role_id) like "w%"
                     ''')
        max_name: int = curr.fetchone()[0]
        if max_name == None:
            max_name = 0
        max_name = max(len('Member Name'), max_name)
        logger.info(f"Maximum  length of name is {max_name}")
        
        #selecting maximum length of role_name in database
        curr.execute(f'''select max(length(role_name)) from role where lower(role_id) like 'w%' ''')
        max_role: int = curr.fetchone()[0]
        if max_role == None:
            max_role = 0
        max_role = max(len("Team"), max_role)
        logger.info(f"Maximum length of role_name is: {max_role}")
        length = (9, max_name, max_role)
        
    elif hierarchy.lower() == 'obs':
        head: tuple = ('OBS ID', 'OBS Name', 'Chair')
        curr.execute('''select emp_id, concat_ws(' ',first_name,surname), role_name
                     from employees natural join role
                     where lower(role_id) like 'a%'
                     order by role_id, emp_id''')
        data: list[tuple[str, ...]] = [head] + curr.fetchall()
        
        #selecting the maximum length of name in database
        curr.execute(f'''
                     select max(length(concat_ws(' ',first_name,surname))) 
                     from employees where lower(role_id) like "a%"
                     ''')
        max_name: int = curr.fetchone()[0]
        if max_name == None:
            max_name = 0
        max_name = max(len('Member Name'), max_name)
        logger.info(f"Maximum  length of name is {max_name}")
        
        #selecting maximum length of role_name in database
        curr.execute(f'''select max(length(role_name)) from role where lower(role_id) like 'a%' ''')
        max_role: int = curr.fetchone()[0]
        if max_role == None:
            max_role = 0
        max_role = max(len("Team"), max_role)
        logger.info(f"Maximum length of role_name is: {max_role}")
        length = (9, max_name, max_role)

    else:
        print("Some invalid input was enterred")
        return

    #printing the box
    print_box(data, length, 3)
    print('\n')

#function to get details of a member
def get_member_details(curr: cursor.MySQLCursor, emp_id: str) -> None:
    try:
        curr.execute('''select EMP_ID, CONCAT_WS(' ', FIRST_NAME, SURNAME),
                     EMP_DOB,ROLE_ID, DOJ, CONTACT_INFO, EMAIL_ID, FOOD_PREFERENCE
                     from employees where emp_id = %s''', (emp_id,))
        data = curr.fetchone()
        logger.info(f"Data obtained from database for {emp_id}:\n{data}")
        if data == None:
            print(f"No record for {emp_id}")
            return
        emp: Employee = put_emp_data([data])
        print(f"Name           : {emp.get_name()}")
        print(f"ID             : {emp.get_empID()}")
        print(f"Date of Birth  : ", end = '')
        try:
            print(emp.get_DOB_str())
        except ValueError:
            print("Not Passed")

        print(f"Date of Joining: ", end = '')

        try:
            print(emp.get_DOJ_str())
        except ValueError:
            print("Not Passed")

        curr.execute('select role_name from role where role_id = %s', (emp.get_role(),))
        print(f"Role           : {curr.fetchone()[0]}")
        print(f"Food Preference: {emp.get_food_choice()}")
        
        curr.execute('select count(*) from attendence where emp_id = %s',
                     (emp.get_empID(),))
        length:int = curr.fetchone()[0]
        logger.info(f"Number of Events {emp.get_name()} was supposed to be in = {length}")
        
        if length == 0:
            print("Meeting not yet conducted")
        else:
            perc = count_attendence(curr, emp)
            print(f"Attendence %   : {perc}")
    except ValueError as e:
        print("The following exception occured:", repr(e), sep = '\n')
        logger.error(f"The following error occurred:\n{e}", exc_info = True)
        print()

#Function to get details of all members
def get_member_details_all(curr: cursor.MySQLCursor) -> None:
    curr.execute('select emp_id from employees order by role_id') 
    ids = curr.fetchall()
    for i in ids:
        get_member_details(curr, i[0])
        print()

#Function to add a new member to team
def new_member(curr: cursor.MySQLCursor) -> None:
    while True:
        try:
            emp_id = input("Enter the student id of the person: ").strip().upper()
            logger.info(f"Emp_id given: {emp_id}")
            if len(emp_id) != 9 or emp_id[:2] != 'AU' or not emp_id[2:].isnumeric():
                print("Kindly input a valid student ID\n")
                continue

            elif exists(curr, emp_id):
                print("Employee ID already exists\n")
                continue
            
            #inputs name
            name = input("Enter the name of the person: ").strip().title()
            logger.info(f"Name give: {name}")

            #inputs date of birth
            dob = input("Enter the person's DOB in format YYYY-MM-DD: ").strip()
            if dob == '':
                dob = None
            logger.info(f"DOB given: {dob}")

            #inputs date of joinning
            doj = input("Enter the person's DOJ in format YYYY-MM-DD: ").strip()
            if doj == '':
                doj = None
            logger.info(f"DOJ given: {doj}")

            #inputs mobile number
            contact = input("Enter the person's mobile number: ").strip()
            logger.info(f"Contact given: {contact}")

            #checks whether its a valid mobile number
            if not contact.isnumeric() or len(contact) != 10:
                print("Please enter a valid contact number\n")
                continue

            #To input if the Person is a Head, Member, OBs, or part of WIE
            hierarchy = input("Enter the position of the new person: ").strip()
            logger.info(f"Hierarchy enttered: {hierarchy}")

            #If match not found then loops
            if hierarchy.upper() not in DIVISION.keys():
                print("Invalid hierarchy\nEnter one of the following only")
                print(*DIVISION.keys(),end = '\n\n')
                continue
            
            if hierarchy.upper() != 'OBS' and hierarchy.upper() != 'WIE':
                for i, j in TEAM.items():               #prints the various teams corresponding to their numbers in the map
                    print(f"{i}. {j[1]}")
                role: int = clean.get_Int(7, 1, "Enter the team number (1 - 7): ")
                role = DIVISION[hierarchy.upper()].upper() + TEAM[role][0]
            else:
                role = input("Enter the role_id of the person: ").upper().strip()
            logger.info(f"Role given: {role}")

            #Input email id
            email = input("Kindly enter the email id: ")
            logger.info(f"Email enterred: {email}")

            for i, j in FOOD.items():
                print(f"{i}. {j}")                  #prints the food preferences corresponding to their numbers in the map
            food_preference: int = clean.get_Int(6, 1, "Enter the food preference (1 - 6): ")
            food_preference: str = FOOD.get(food_preference)
            logger.info(f"Food preference given is {food_preference}")
            
            #Splits the name into first name and surname
            first_name, surname = tuple(name.split())

            #writes the data to mysql database
            curr.execute('''insert into employees(EMP_ID, First_Name, EMP_DOB, ROLE_ID, DOJ,
                         CONTACT_INFO, EMAIL_ID, SURNAME, FOOD_PREFERENCE)
                         values(%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                         (emp_id, first_name, dob, role, doj, contact, email, surname, food_preference))

            print("Data inserted successfully") 
        except errors.IntegrityError as e:
            logger.critical(f"The following error occured\n{e}", exc_info = True)
            print("Either the role you have enttered doesn't exists or the ID you enttered already exists")
        
        except KeyError as e:
            logger.critical(f"The following error ocurred\n{e}", exc_info = True)
            print("Kindly enter the correct division, i.e, either \nOBS, Heads, Members or WIE")
        except Exception as e:
            logger.critical(f"The following error occured\n{e}", exc_info = True)
            print("Some unknown error occured. Kindly contact your CSE Department")
        print()
        break

#Function to update member details
def update_member(con: connection.MySQLConnection ,curr: cursor.MySQLCursor, emp: Employee) -> None:
    if type(emp) != Employee:
        logger.error("Employee type was not passed")
        print("The correct employee type was not passed. Kindly consider consulting with the developer")
        return
    print("The student details are: ")
    get_member_details(curr, emp.get_empID())
    
    print("Enter the details you want to change:-")
    print("1. DOB")
    print("2. Role")
    print("3. DOJ")
    print("4. Food Preference")
    print("5. Go Back")

    chk = clean.get_Int(5, 1, "Enter your choice (1 - 5): ")
    print()

    if chk == 1:
        while True:
            try:
                dob = input("Enter new DOB in YYYY-MM-DD format: ")
                logger.info(f"The following DOB was passed, {dob}")
                emp.set_DOB(dob)
                curr.execute("Update employees set emp_dob = %s where emp_id = %s", 
                    (emp.get_DOB_str(True), emp.get_empID())
                    )
                con.commit()
                break
            except ValueError as e:
                logger.exception(f"The error that occured was\n{e}\n\n DOB passed {dob}", exc_info = True)
                print("Kindly enter the DOB in correct format\n")
                con.rollback()
            except errors.DataError as e:
                logger.exception(f"The error that occured was\n{e}\n\n DOB passed {dob}", exc_info = True)
                print("Kindly enter the DOB in correct format\n")
                con.rollback()
        print("DOB was successfully updated")
        
    elif chk == 2:
        curr.execute("select * from roles order by role_id")
        roles: list[tuple[str,str]] = curr.fetchall()
        roles, rows = roles, len(roles)
        print("The positions are: ")
        for i in range(rows):
            if i == 0:
                print("\nOBS")
            elif i == 5:
                print("\nHeads")
            elif i == 12:
                print("\nMembers")
            elif i == 19:
                print("\nWIE")
            print(f"{i + 1}. {roles[i][0]}: {roles[i][1]}")
        print()

        while True:
            try:
                new_role = input("Kindly enter the new role ID for the person (case insensitive): ").strip().upper()
                curr.execute("update employees set role_id = %s where emp_id = %s", (new_role, emp.get_empID()))
                con.commit()
                print("Role updated successfully")
                break
            except errors.IntegrityError as e:
                con.rollback()
                logger.exception(f"The following error occured\n{e}", exc_info = True)
                print("Looks like you enterred a role_id that doesn't exist")
                while True:
                    a = input("Would you like to enter another? (Y/N): ").strip().upper()
                    a = a[0]
                    if a != 'Y' and a != 'N':
                        print("Kindly enter a valid option")
                    break
                if a == 'N':
                    break
            
    elif chk == 3:
        while True:
            try:
                doj = input("Enter new DOJ in YYYY-MM-DD format: ")
                logger.info(f"The following DOJ was passed, {doj}")
                emp.set_DOJ(doj)
                curr.execute("Update employees set DOJ = %s where emp_id = %s", (emp.get_DOB_str(True), emp.get_empID()))
                con.commit()
                break
            except ValueError as e:
                logger.exception(f"The error that occured was\n{e}\n\n DOJ passed {doj}", exc_info = True)
                print("Kindly enter the DOJ in correct format\n")
                con.rollback()
            except errors.DataError as e:
                logger.exception(f"The error that occured was\n{e}\n\n DOJ passed {doj}", exc_info = True)
                print("Kindly enter the DOJ in correct format\n")
                con.rollback()

    elif chk == 4:
        print("The food categories are:")
        for i, j in FOOD.items():
            print(f"{i}. {j}")

        try:
            preference = int(input("Enter the number corresponding to food preference: "))
            if preference not in FOOD.keys():
                print("Kindly enter the correct option")
            emp.set_food_choice(FOOD.get(preference))
            curr.execute("update employees set food_preference = %s where emp_id = %s",
                         (emp.get_food_choice(), emp.get_empID()))
            con.commit()
            print("Food preference updated successfully")

        except errors.DataError as e:
            logger.exception(f"Food choice given was\n{e}", exc_info = True)
            print("There was an error while inserting data into the database")
            print("Kindly consider contacting your developer")
            con.rollback()

        except errors.DatabaseError as e:
            logger.exception(f"Food choice given was\n{e}", exc_info = True)
            print("There was an error while inserting data into the database")
            print("Kindly consider contacting your developer")
            con.rollback()

        
    elif chk == 5:
        print("Exiting...")

    else:
        print("Invalid choice")

    print()
    con.rollback()

#main function of the file
def members_main(con: connection.MySQLConnection, curr: cursor.MySQLCursor) -> None:
    logger.debug("Inside Members Module")
    while True:
        print("Select one of the following")
        print("1. Enter New Members")
        print("2. Update Members")
        print("3. Print Details of Individual Members")
        print("4. Print Details of All Members")
        print("5. Display Members")
        print("6. Go back")
        ch = clean.get_Int(6,1,"Enter your choice (1 - 6): ")
        print()

        #To enter new members
        if ch == 1:
            n = clean.get_natural_num("Enter the number of new members you want to add: ")

            try:
                for i in range(n):
                    new_member(curr)
                con.commit()
            except Exception as e:
                print("OOPs! An error occured. Kindly contact your tech/cse team")
                logger.critical(f"The following exception occured:\n{e}", exc_info = True) 
                con.rollback()
            print()

        #To update current members
        elif ch == 2:
            empid = input("Enter the Student ID of the person: ").upper()
            if exists(curr, empid):
                curr.execute('''
                            select EMP_ID, CONCAT_WS(' ', FIRST_NAME, SURNAME), EMP_DOB, ROLE_ID, DOJ,
                            CONTACT_INFO, EMAIL_ID, FOOD_PREFERENCE FROM EMPLOYEES WHERE EMP_ID = %s
                            ''',
                            (empid,))
                data = curr.fetchall()
                emp: Employee = put_emp_data(data)
                update_member(con, curr, emp)
            else:
                print("Employee does not exists. Kindly check whether you have enterred correct employee data")

        #To print member details
        elif ch == 3:
            empid: str = input("Enter the Student ID of the person: ").strip().upper()
            logger.info(f"{empid} was enttered as the student ID")
            if exists(curr, empid):
                get_member_details(curr, empid)
            else:
                print("The Student Id does not exist")
            print()

        #To print details of all members
        elif ch == 4:
            get_member_details_all(curr)

        #To display members
        elif ch == 5:
            print("Please select one of the following:")
            print("1. All the members")
            print("2. Only the OBS")
            print("3. Only the Heads")
            print("4. Only the Members")
            print("5. Only WIE")
            print("6. Go Back")
            
            op = clean.get_Int(6, 1,"Enter your choice (1 - 6): ")

            if op == 1:
                display_members(curr, '*', None)

            elif op == 2:
                display_members(curr, None, 'obs')
            
            elif op == 3:
                print("These are the teams")
                for i, j in TEAM.items():
                    print(f"{i}. {j[1]}")
                team = clean.get_Int(7, 1, "Enter the Team Number: ")
                display_members(curr, team, 'heads')

            elif op == 4:
                print("These are the teams")
                for i, j in TEAM.items():
                    print(f"{i}. {j[1]}")
                team = clean.get_Int(7, 1, "Enter the Team Number: ")
                display_members(curr, team, 'member')

            elif op == 5:
                display_members(curr, None, 'WIE')

            elif op == 6:
                print()
                pass

            else:
                print("Wrong input", end = '\n\n')

        elif ch == 6:
            logger.debug("Leaving members.main")
            return
        

        else:
            print("Invalid input")