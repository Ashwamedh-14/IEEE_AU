from mysql.connector import connection, cursor, errors
from datetime import datetime

from Support_Files.Person import Employee
import Support_Files.cleaning as clean

def print_box(Data: list[tuple], maxlen: tuple[int], tuple_size: int):
    '''
    To print a box around data to give some semblence to structure
    It is assumed all tuples in data are in equal length
    It is also assumed that all the values in maxlen correspond to max length of each data in each tuple 
    of the list
    '''
    
    head = Data[0]
    for j in range(tuple_size):
        print('+' + '-' * (maxlen[j] + 2), end = '')
    print('+')
    for i in range(tuple_size):
        space: int = maxlen[i] + 2
        print('|' + f'{head[i]:^{space}}', end = '')
    print('|')
    for j in range(tuple_size):
        print('+' + '-' * (maxlen[j] + 2), end = '')
    print('+')

    Data = Data[1:]
    for i in Data:
        for j in range(tuple_size):
            space = maxlen[j] + 2
            print('|' + f'{i[j]:^{space}}', end = '')
        print('|')

    for j in range(tuple_size):
        space = maxlen[j] + 2
        print('+' + '-' * space, end = '')
    print('+')




def put_emp_data(data_list: list[tuple[str | int | datetime]]) -> list[Employee]:
    l = []
    for i in data_list:
        emp = Employee(i[1], i[2], i[0], i[4], i[3])
        l.append(emp)
    return l

def take_attendence(con: connection.MySQLConnection, curr: cursor.MySQLCursor):
    curr.execute("SELECT * FROM EMPLOYEES ORDER BY ROLE_ID ")
    emp_list = curr.fetchall()
    emp_list: list[Employee] = put_emp_data(emp_list)
    curr.execute("select date(now())")
    date: datetime = curr.fetchone()[0]
    print(f"Today's date: {date:%d %B %Y}")

    try:
        print(f"{'Student ID':<12}{"Student Name":<40}{"Student Role":<22}{"Presence":<10}")
        for i in emp_list:
            role = curr.execute(f"select role_name from role where role_id = '{i.get_role()}'")
            role = curr.fetchone()[0]
            presence = input(f"{i.get_empID():<12}{i.get_name():<40}{role:<22}")
        
            presence = presence.title().strip()
            if presence not in ('A', 'P', 'Absent', 'Present'):
                raise ValueError("Attendence is only accepted in A/P format")
            reason = None
            if presence == "A":
                reason = input("What is the reason\n")
                print()
            if reason == '':
                reason = "No specific reason"

            curr.execute("insert into attendence values(%s, %s, %s, %s)", (date.strftime(r"%Y-%m-%d"),
                         i.get_empID(), presence, reason))

    except Exception as e:
        print("The following error occurred", repr(e), sep = '\n')
        print("To fill attendence again, kindly pick the option again\n")
        print()
        con.rollback()
        return

    while True:
        save = input("Save attendence: ").title().strip()
        if save not in ("Y", "N", "Yes", "No"):
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
    
    

def count_attendence(curr: cursor.MySQLCursor, employee: Employee) -> float:
    '''
    To count the percentage of attendence a member has
    '''
    curr.execute(f'''select count(*) from attendence where emp_id = "{employee.get_empID()}"''')
    total_attendence: int = curr.fetchone()[0]

    curr.execute(f'''select count(*) from attendence where emp_id = '{employee.get_empID()}' and presence = "P"''')

    present: int = curr.fetchone()[0]
    perc_present: float = round(present / total_attendence * 100, 2)
    return perc_present

def list_attendence(curr:cursor.MySQLCursor, emp_id: str):
    try:
        curr.execute('select * from employees where emp_id = %s', (emp_id,))
        data = curr.fetchone()
        if data == None:
            return
        emp = Employee(data[1], data[2], data[0], data[4], data[3])
        perc = count_attendence(curr, emp)
        curr.execute('select Date, Presence from Attendence where emp_id = %s order by emp_id', (emp.get_empID(),))
        d = curr.fetchall()
        if d != []:
            data = [("Date", "Attendence")]
            data.extend(d)
            for i in range(1, len(data)):
                data[i]: tuple[str, str] = data[i][0].strftime('%d-%m-%Y'), data[i][1]
        print(f"Name           : {emp.get_name()}")
        print(f"ID             : {emp.get_empID()}")
        print(f"Date of Joining: ", end = '')

        try:
            print(emp.get_DOB_str())
        except ValueError:
            print("Not Passed")
        
        print(f"Attendence %   : {perc}")
        if d == []:
            print("Meeting not yet conducted")
        else:
            print_box(data, (10, 10), 2)
    except Exception as e:
        print("The following exception occured:", repr(e), sep = '\n')
        print()

def list_attendence_all(curr: cursor.MySQLCursor):
    curr.execute('select emp_id from employees order by role_id')
    ids = curr.fetchall()
    for i in ids:
        list_attendence(curr, i[0])
        print()

def update_attendence(curr: cursor.MySQLCursor, empid: str, date: str, upd: str):
    if type(date) != str:
        raise TypeError("Date must be of type string")
    upd = upd.title()
    if upd not in ('P', 'A', 'Present', 'Absent'):
        raise ValueError("Only Present or Absent allowed")
    reason = None
    if upd == 'A':
        reason = input("What was the reason:\n")
    curr.execute('update attendence set presence = %s, reason = %s where date = %s and emp_id = %s',
                 (upd, reason, date, empid))
    print("Attendence successfully update\n")

def attend_main(con: connection.MySQLConnection, curr: cursor.MySQLCursor):
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
                if ch < 1 or ch > 5:
                    print("Valid choices are only between 1 and 5 inclusively")
                else:
                    break
            except ValueError:
                print("Kindly enter a number only")
        print('\n')
        
        if ch == 1:
            take_attendence(con, curr)
        
        elif ch == 2:
            empid = input("Enter the id of the person: ")
            empid = empid.upper().strip()
            date = input("Enter the date of attendence in YYYY-MM-DD format: ")
            date = clean.clean_string(date)
            while True:
                upd = input("Set attendence to Absent (A) or Present (P): ")
                if upd.title() not in ('A', 'Absent', 'P', 'Present'):
                    print("Kindly enter Absent or Present Only")
                    continue
                break
            print()
            try:
                curr.execute("select * from attendence where emp_id = %s and date = %s", (empid, date))
                qh = curr.fetchone()
                if qh:
                    update_attendence(curr, empid, date, upd)
                    con.commit()
                else:
                    print("Error 404: Entry not found") 
                    print("Check whether the input date and ID is correct\n")
                    print()
            except Exception as e:
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
            return
                