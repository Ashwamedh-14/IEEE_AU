import datetime as dt
import cleaning as clean

class Person:
    def __init__(self, name: str, DOB: str | dt.datetime):
        '''DOB must be in YYYY-MM-DD format'''
        if type(name) != str or type(DOB) not in (str, dt.datetime):
            raise TypeError("Incorrect types passed to name or DOB")

        self.name: str = (name.strip()).title()
        if type(DOB) == str:
            self.DOB: dt.datetime = dt.datetime.strptime(clean.clean_string(DOB), r"%Y-%m-%d")
        else:
            self.DOB: dt.datetime = DOB

    def __str__(self) -> str:
        return f"Hi, I am {self.name} and was born on {self.DOB}"

    def get_name(self) -> str:
        return self.name

    def get_DOB_str(self, processing: bool = False) -> str:
        if self.DOB == None:
            raise ValueError("DOB not passed")
        if processing:
            return self.DOB.strftime(r"%Y-%m-%d")
        return self.DOB.strftime(r"%d %B %Y")

    def get_DOB_datetime(self) -> dt.datetime:
        if self.DOB == None:
            raise ValueError("DOB not passed")
        return self.DOB

    def get_details(self) -> tuple[str,str]:
        '''return date in DD Month Name YYYY type format'''
        if self.DOB == None:
            return self.name
        return self.name, self.DOB.strftime(r"%d %B %Y")
        
    def get_age(self) -> int:
        if self.DOB == None:
            raise ValueError("DOB not enterred")
        today = dt.datetime.today()
        if self.DOB.month > today.month:
            return today.year - self.DOB.year - 1
        elif self.DOB.month < today.month:
            return today.year - self.DOB.year
        elif self.DOB.day > today.day:
            return today.year - self.DOB.year - 1
        else: 
            return today.year - self.DOB.year
    
    def set_name(self, name: str):
        if type(name) != str:
            raise TypeError("Incorrect type passed to name")
        self.name = (name.strip()).title()

    def set_DOB(self, DOB: str | dt.datetime):
        if DOB not in (str, dt.datetime):
            raise ValueError("Incorrect type passed to DOB")

        '''
        DOB should be in YYYY-MM-DD format
        '''
        if type(DOB) == str:
            self.DOB: dt.datetime = dt.datetime.strptime(clean.clean_string(DOB), r"%Y-%m-%d")
        else:
            self.DOB: dt.datetime = DOB
    

class User(Person):
    def __init__(self, name: str, DOB: str | dt.datetime, user_id: str, password: str, phno: int = None, email: str = None):
        super().__init__(name, DOB)
        if type(phno) == str and (phno.strip()).lower() == 'null':
            phno = None
        if type(email) == str and email.lower() == 'null':
            email = None
        self.user_id: str = user_id
        self.password: str = password
        self.phno: int = phno
        self.email: str = email

    def get_uid(self):
        return self.user_id

    def get_password(self):
        return self.password

    def get_phonenum(self):
        return self.phno

    def get_email(self):
        return self.email

    def set_userid(self, userid: str):
        self.userid = userid

    def set_password(self, password: str):
        self.password = password

    def set_phno(self, phno: int):
        self.phno = phno

    def has_phnonum(self):
        if self.phno == None:
            return False
        return True
    
    def has_email(self):
        if self.email == None:
            return False
        return True


class Administrator(Person):
    def __init__(self, name: str, DOB: str | dt.datetime, security_key: str | int):
        super().__init__(name, DOB)
        if type(security_key) == int:
            self.security_key: str | int = security_key
        else:
            self.security_key: str | int = security_key.strip()

    def get_security_key(self):
        return self.security_key
    
    def set_security_key(self, security_key: str | int):
        if type(security_key) == int:
            self.security_key = security_key
        else:
            self.security_key = security_key.strip()

class Employee(Person):
    def __init__(self, name: str, DOB: str | dt.datetime, emp_ID: str, DOJ: str | dt.datetime, role: str):
        super().__init__(name, DOB)
        if type(emp_ID) != str or type(DOJ) not in (str, dt.datetime) or type(role) != str:
            raise TypeError("Incorrect types passed to arguments, emp_ID, DOJ or role")
        self.emp_ID: str = clean.clean_string(emp_ID)
        if type(DOJ) == str:
            self.DOJ: dt.datetime = dt.datetime.strptime(DOJ, r"%Y-%m-%d")
        else:
            self.DOJ: dt.datetime = DOJ
        if role == '':
            role = None
        else:
            self.role: str = clean.clean_string(role)

    def get_empID(self) -> str:
        return self.emp_ID
    
    def get_DOJ_str(self, processing: bool = False) ->str:
        if type(processing) != bool:
            raise ValueError("Processing should be of type bool")
        if bool:
            return self.DOJ.strftime(r"%Y-%m-%d")
        else:
            return self.DOJ.strftime(r"%d-%m-%Y")
    
    def get_DOJ_dt(self):
        return self.DOJ
    
    def get_role(self) -> str | None:
        return self.role
    
    def set_empID(self, empID: str):
        if type(empID) != str:
            raise TypeError("Incorrect type passed")
        self.emp_ID: str = clean.clean_string(empID)

    def set_DOJ(self, DOJ: str | dt.datetime):
        if type(DOJ) not in (str, dt.datetime):
            raise TypeError("DOJ should be either string or datetime object")
        if type(DOJ) == str:
            self.DOJ: dt.datetime = dt.datetime.strptime(clean.clean_string(DOJ), r"%Y-%m-%d")
        else:
            self.DOJ = DOJ
    
    def set_role(self, role: str):
        if type(role) not in (str, None):
            raise TypeError("Role should be a string")
        self.role = clean.clean_string(role)