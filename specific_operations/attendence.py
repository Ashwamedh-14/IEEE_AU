from mysql.connector import connection, cursor, errors
from Support_Files.Person import Employee
from datetime import datetime

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
    
    

def count_attendence(curr: cursor.MySQLCursor, empid: str):
    '''
    To count the percentage of attendence a member has
    '''
    ...