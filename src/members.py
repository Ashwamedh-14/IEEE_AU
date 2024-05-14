#Built-In Libraries
import logging
from logging import handlers

#3rd Party library
from mysql.connector import connection, cursor, errors

#self defined modules
from Support_Files.printing import print_box
from Support_Files.Person import Employee, FOOD
from src.attendence import put_emp_data, count_attendence

#setting up the file_handle
LOG_FORMAT = logging.Formatter("%(asctime)s: %(levelname)s: %(filename)s: %(funcName)s\n%(message)s\n")
file_handle = handlers.TimedRotatingFileHandler(r'../logs/members.log', 'W6')
file_handle.setLevel(logging.DEBUG)
file_handle.setFormatter(LOG_FORMAT)

#setting the logger
logger = logging.getLogger(__name__)
logger.addHandler(file_handle)
logger.setLevel(logging.DEBUG)
logger.propagate = False

#Main Functions start
#Constants
DIVISION = {'OBS': 'a', 'HEADS': 'b', 'MEMBER': 'c', "WIE": 'w'}
TEAM = {1: ('01', 'RAS'), 
        2: ('02', 'Technical'), 
        3: ('03', 'Logistics'), 
        4: ('04', 'Social Media'), 
        5: ('05', 'CSE'), 
        6: ('06', 'Content'), 
        7: ('07', 'Graphics')}

#This function checkes whether a particular members is present or not
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
    if type(team) == int and team < 1 or team > 7:
        raise ValueError("Team can only take values None, '*' or integers from 1 to 7")

    if type(hierarchy) != str:
        raise TypeError("Incorrect type passed to hierarchy. Ensure its string type")
    if hierarchy.upper() not in ('OBS', 'HEAD', 'MEMBERS', 'WIE'):
        raise ValueError("Incorrect Value passed to hierarchy. Should be OBS, Heads, Members or WIE only")

    if team == None:
        team = ''
    #In case all members are required
    if team == '*':
        head = ('Student ID', 'Student Name', 'Department')
        curr.execute(f'''select emp_id, concat_ws(' ',first_name,surname), role_name 
                     from employees natural join role  
                     order by role_id, emp_id''')
        data: list[tuple[str,...]] = [head] + curr.fetchall()

        #selecting the maximum length of name in database
        curr.execute(f"select max(length(concat_ws(' ',first_name,surname)) from employee")
        max_name: int = curr.fetchone()[0]
        logger.info("Maximum length of name is: %s", max_name)

        #selecting maximum length of role_name in database
        curr.execute(f'''select max(length(role_name)) 
                     from role''')
        max_role: int = curr.fetchone()[0]
        logger.info("Maximum length of role name is: %s", max_role)
        length = (10, max_name, max_role)

    #In case only members are required
    elif hierarchy.lower() == 'members':
        head: tuple = ('Member ID', 'Member Name', 'Team')
        curr.execute(f'''select emp_id, concat_ws(' ',first_name,surname), role_name
                     from employees natural join role
                     where lower(role_id) like 'c{TEAM[team][0]}%'
                     order by role_id, emp_id''')
        data: list[tuple[str, ...]] = [head] + curr.fetchall()
        
        #selecting the maximum length of name in database
        curr.execute(f'''select max(length(concat_ws(' ',first_name,surname)) from employees where lower(role_id) like "c{TEAM[team][0]}%"''')
        max_name: int = curr.fetchone()[0]
        logger.info(f"Maximum  length of name is {max_name}")
        
        #selecting maximum length of role_name in database
        curr.execute(f'''select max(length(role_name)) from role where lower(role_id) like 'c{TEAM[team][0]}' ''')
        max_role: int = curr.fetchone()[0]
        logger.info(f"Maximum length of role_name is: {max_role}")
        length = (9, max_name, max_role)

    elif hierarchy.lower() == 'heads':
        head: tuple = ('Head ID', 'Head Name', 'Team')
        curr.execute(f'''select emp_id, concat_ws(' ',first_name,surname), role_name
                     from employees natural join role
                     where lower(role_id) like 'b{TEAM[team][0]}%'
                     order by role_id, emp_id''')
        data: list[tuple[str, ...]] = [head] + curr.fetchall()
        
        #selecting the maximum length of name in database
        curr.execute(f'''select max(length(concat_ws(' ',first_name,surname)) from employees where lower(role_id) like "b{TEAM[team][0]}%"''')
        max_name: int = curr.fetchone()[0]
        logger.info(f"Maximum  length of name is {max_name}")
        
        #selecting maximum length of role_name in database
        curr.execute(f'''select max(length(role_name)) from role where lower(role_id) like 'b{TEAM[team][0]}' ''')
        max_role: int = curr.fetchone()[0]
        logger.info(f"Maximum length of role_name is: {max_role}")
        length = (9, max_name, max_role)

    elif hierarchy.lower() == 'wie':
        head: tuple = ('WIE ID', 'WIE Name', 'Chair')
        curr.execute('''select emp_id, max(length(concat_ws(' ',first_name,surname)), role_name
                     from employees natural join role
                     where lower(role_id) like 'w%'
                     order by role_id, emp_id''')
        data: list[tuple[str, ...]] = [head] + curr.fetchall()
        
        #selecting the maximum length of name in database
        curr.execute(f'select max(length(concat_ws(' ',first_name,surname)) from employees where lower(role_id) like "w%"')
        max_name: int = curr.fetchone()[0]
        logger.info(f"Maximum  length of name is {max_name}")
        
        #selecting maximum length of role_name in database
        curr.execute(f'''select max(length(role_name)) from role where lower(role_id) like 'w%' ''')
        max_role: int = curr.fetchone()[0]
        logger.info(f"Maximum length of role_name is: {max_role}")
        length = (9, max_name, max_role)
        
    elif hierarchy.lower() == 'obs':
        head: tuple = ('OBS ID', 'OBS Name', 'Chair')
        curr.execute('''select emp_id, max(length(concat_ws(' ',first_name,surname)), role_name
                     from employees natural join role
                     where lower(role_id) like 'a%'
                     order by role_id, emp_id''')
        data: list[tuple[str, ...]] = [head] + curr.fetchall()
        
        #selecting the maximum length of name in database
        curr.execute(f'select max(length(concat_ws(' ',first_name,surname)) from employees where lower(role_id) like "a%"')
        max_name: int = curr.fetchone()[0]
        logger.info(f"Maximum  length of name is {max_name}")
        
        #selecting maximum length of role_name in database
        curr.execute(f'''select max(length(role_name)) from role where lower(role_id) like 'a%' ''')
        max_role: int = curr.fetchone()[0]
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
            print(f"No attendence taken for {emp_id}")
            return
        emp = Employee(data[1], data[2], data[0], data[4], data[3],data[5],data[6],data[7])
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

            name = input("Enter the name of the person: ").strip().title()
            logger.info(f"Name give: {name}")

            dob = input("Enter the person's DOB in format YYYY-MM-DD: ").strip()
            if dob == '':
                dob = None
            logger.info(f"DOB given: {dob}")

            doj = input("Enter the person's DOJ in format YYYY-MM-DD: ").strip()
            if doj == '':
                doj = None
            logger.info(f"DOJ given: {doj}")

            contact = input("Enter the person's mobile number: ").strip()
            logger.info(f"Contact given: {contact}")

            if not contact.isnumeric() or len(str(int(contact))) != 10:
                print("Please enter a valid contact number\n")
                continue

            hierarchy = input("Enter the position of the new person: ").strip()
            logger.info(f"Hierarchy enttered: {hierarchy}")

            if hierarchy.upper() not in DIVISION.keys():
                print("Invalid hierarchy\nEnter one of the following only")
                print(*DIVISION.keys(),end = '\n\n')
                continue
            
            if hierarchy.upper() != 'OBS' and hierarchy.upper() != 'WIE':
                for i, j in TEAM.items():
                    print(f"{i}. {j[1]}")
                while True:
                    try:
                        role = int(input("Kindly enter the role (1-7): "))
                        if role < 1 or role > 7:
                            print("Enter a valid role\n")
                            continue
                        role = DIVISION[hierarchy.upper()].upper() + TEAM[role]
                        break
                    except ValueError as e:
                        logger.error(f"Got error\n{e}\n because {role} was passed as role")
                        print("Kindly enter an integer between 1 and 7 only")
            else:
                role = input("Enter the role_id of the person: ").upper().strip()
            logger.info(f"Role given: {role}")
            
            curr.execute("insert into employees values(%s, %s, %s, %s, %s, %s)", (emp_id, name, dob, role, doj, contact))
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
    print(emp, end = '\n\n')
    
    print("Enter the details you want to change:-")
    print("1. DOB")
    print("2. Role")
    print("3. DOJ")
    print("4. Food Preference")
    print("5. Go Back")

    while True:
        try:
            chk = int(input("Enter your choice: "))
            logger.info(f"Value input in check = {chk}")
            if chk < 1 or chk > 5:
                print("Kindly only enter your choice from 1 to 5\n")
            else:
                break
        except ValueError as e:
            logger.exception(f"The exception that occurred was\n{e}\n\n Value passed {chk:}", exc_info = True)
            print("Kindly ensure you have given an integer only\n")
    print("\n")

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

        while True:
            try:
                preference = int(input("Enter the number corresponding to food preference: "))
                if preference not in FOOD.keys():
                    print("Kindly enter the correct option")
                    while True:
                        a = input("Would you like to enter another? (Y/N): ").strip().upper()
                        a = a[0]
                        if a != 'Y' and a != 'N':
                            print("Kindly enter a valid option")
                        break
                    if a == 'Y':
                        for i, j in FOOD.items():
                            print(f"{i}. {j}")
                emp.set_food_choice(FOOD.get(preference))
                curr.execute("update employee set food_preference = %s where emp_id = %s",
                             (emp.get_food_choice(), emp.get_empID()))
                con.commit()
                print("Food preference updated successfully")
                break
            except ValueError as e:
                logger.exception(f"The error that occured was\n{e}\n\n preference passed {preference}", exc_info = True)
                print("Kindly enter an integer only\n")
                con.rollback()
            except errors.DataError as e:
                logger.exception(f"Food choice given was\n{e}", exc_info = True)
                print("There was an error while inserting data into the database")
                print("Kindly consider contacting your developer")
                break
        
    elif chk == 5:
        print("Exiting...")

    else:
        print("Invalid choice")

    print()
    con.rollback()
    


    #To be completed

#main function of the file
def members_main(con: connection.MySQLConnection, curr: cursor.MySQLCursor):
    logger.debug("Inside Members Module")
    while True:
        print("Select one of the following")
        print("1. Enter New Members")
        print("2. Print Member Details")
        print("3. Display Members")
        print("4. Go back")
        while True:
            try:
                ch = int(input("Enter your choice (1-4): "))
                logger.info(f"{ch} was input as choice")
                if ch < 1 or ch > 5:
                    print("Valid Choices are from 1 to 5 only")
                    print()
                else:
                    break
            except ValueError:
                print("Kindly enter a number only")
                logger.error(f"Instead of valid number, {ch} was enttered")
                print()
        print()

        if ch == 1:
            while True:
                try:
                    n = int(input("Enter the total number of new members you want to add: "))
                    logger.info(f"{n} was input to integer")
                    if n < 0:
                        print("Kindly enter a positive integer\n")
                        continue
                    break
                except ValueError as e:
                    print("Please ensure to pass only valid integer\n")
                    logger.error(f"The following error occured\n{e}", exc_info = True)

            try:
                for i in range(n):
                    new_member(curr)
                con.commit()
            except Exception as e:
                print("OOPs! An error occured. Kindly contact your tech/cse team")
                logger.critical(f"The following exception occured:\n{e}", exc_info = True) 
                con.rollback()
            print()

        elif ch == 2:
            empid: str = input("Enter the Student ID of the person: ").strip().upper()
            logger.info(f"{empid} was enttered as the student ID")
            if exists(empid):
                get_member_details(curr, empid)
            else:
                print("The Student Id does not exist")
            print()

        elif ch == 3:
            print("Please select one of the following:")
            print("1. All the members")
            print("2. Only the OBS")
            print("3. Only the Heads")
            print("4. Only the Members")
            print("5. Only WIE")
            print("6. Go Back")
            while True:
                try:
                    op = int(input("Enter your choice (1-4): "))
                    logger.info(f"{op} was input as choice")
                    if op < 1 or op > 6:
                        print("Valid Choices are from 1 to 6 only")
                        print()
                    else:
                        break
                except ValueError:
                    print("Kindly enter a number only")
                    logger.error(f"Instead of valid number, {op} was enttered")
                    print()
            print()

            if ch == 1:
                display_members(curr, '*', None)

            elif ch == 2:
                display_members(curr, None, 'obs')
            
            elif ch == 3:
                print("These are the teams")
                for i, j in DIVISION.values():
                    print(f"{i}. {j[1]}")
                while True:
                    try:
                        team = int(input("Enter the team you want to select: "))
                        if team < 1 or team > 7:
                            print("Please enter a number between 1 and 7")
                            continue
                        break
                    except ValueError:
                        print("Kindly enter an integer only")
                display_members(curr, TEAM[team][0], 'heads')

            elif ch == 4:
                print("These are the teams")
                for i, j in DIVISION.values():
                    print(f"{i}. {j[1]}")
                while True:
                    try:
                        team = int(input("Enter the team you want to select: "))
                        if team < 1 or team > 7:
                            print("Please enter a number between 1 and 7")
                            continue
                        break
                    except ValueError:
                        print("Kindly enter an integer only")
                display_members(curr, TEAM[team][0], 'members')

            elif ch == 5:
                display_members(curr, None, 'WIE')

            elif ch == 6:
                pass

            else:
                print("Wrong input")

        elif ch == 4:
            logger.debug("Leaving members.main")
            return
        

        else:
            print("Invalid input")