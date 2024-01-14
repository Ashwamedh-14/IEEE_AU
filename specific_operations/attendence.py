from mysql.connector import connection, cursor, errors
from Support_Files.Person import Employee
from datetime import datetime

def print_box(Data: list[tuple], maxlen: tuple[int], tuple_size: int):
    '''
    To print a box around data to give some semblence to structure
    It is assumed all tuples in data are in equal length
    It is also assumed that all the values in maxlen correspond to max length ofeach data in each tuple 
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
    curr.execute("SELECT * FROM EMPLOYEES")
    emp_list = curr.fetchall()
    emp_list: list[Employee] = put_emp_data(emp_list)
    curr.execute("select date(now())")
    date: datetime = curr.fetchone()[0]
    print(f"Today's date: {date:%d %B %Y}")

    try:
        print(f"{'Student ID':<12}{"Student Name":<40}{"Student Role":<22}{"Presence":<10}")
        for i in emp_list:
            role = curr.execute(f"select role_name from role where role_id = '{i.get}'")
            role = curr.fetchone()[0]
            presence = input(f"{i.get_empID():<12}{i.get_name():<40}{role:<22}")
        
            presence = presence.title()[0]
            if presence not in ('A', 'P'):
                raise ValueError("Attendence is only accepted in A/P format")
            reason = None
            if presence == "A":
                reason = input("what is the reason\n")
                print()
            if reason == '':
                reason = "No specific reason"

            curr.execute("insert into attendence values(%s, %s, %s, %s)", (date.strftime(r"%Y-%m-%d"),
                         i.get_empID(), presence, reason))

    except Exception as e:
        print("The following error occurred", repr(e), sep = '\n')
        print("To fill attendence again, kindly pick the option again")
        con.rollback()
        return

    while True:
        save = input("Save attendence: ").title()[0]
        if save not in ("Y", "N"):
            print("Please enter only yes or no\n")
        break
    if save == 'N':
        print("Attendence not saved")
        con.rollback()
        return
    else:
        print("Attendence saved")
        con.commit()
    
    

def count_attendence(curr: cursor.MySQLCursor, employee: Employee) -> float:
    '''
    To count the percentage of attendence a member has
    '''
    curr.execute(f"select count(*) from attendence where Date >= '{employee.get_DOJ_str(True)}' 
                 and emp_id = '{employee.get_empID()}'")
    total_attendence: int = curr.fetchone()[0]

    curr.execute(f"select count(*) from attendence where emp_id = '{employee.get_empID()}' and 
                 Date >= '{employee.get_DOJ_str(True)} and presence = 'P'")
    present: int = curr.fetchone()[0]
    perc_present = round(present / total_attendence * 100, 2)
    return perc_present

def list_attendence(curr:cursor.MySQLCursor, emp_id: str):
    curr.execute('select Date, Presence from Attendence where emp_id = %s', (emp_id,))
    data = [("Date", "Present")]
    data.extend(curr.fetchall())
    print_box(data, (10, 7), 2)

def list_attendence_all(curr: cursor.MySQLCursor):
    curr.execute('select emp_id from employees')
    ids = curr.fetchall()
    for i in ids:
        list_attendence(curr, i[0])

def update_attendence(curr: cursor.MySQLCursor, empid: str, date: str, upd: str):
    if type(date) != str:
        raise TypeError("Date must be of type string")
    upd = upd.title()[0]
    if upd not in ('P', 'A'):
        raise ValueError("Only Present or absent allowed")
    reason = None
    if upd == 'A':
        reason = input("What was the reason:\n")
    curr.execute('update attendence set presence = %s, reason = %s where date = %s and emp_id = %s',
                 (upd, reason, date, empid))
    print("Attendence successfully update")
    