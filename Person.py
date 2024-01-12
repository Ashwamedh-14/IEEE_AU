import datetime as dt

class Person:
    def __init__(self, name: str, DOB: str | dt.datetime):
        '''DOB must be in YYYY-MM-DD format'''
        self.name: str = (name.strip()).title()
        if type(DOB) == str:
            DOB = dt.datetime.strptime(DOB, r"%Y-%m-%d")
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

    def set_name(self, name: str):
        self.name = (name.strip()).title()

    def set_DOB(self, DOB: str):
        '''
        DOB should be in YYYY-MM-DD format
        '''
        self.DOB: dt.datetime = dt.datetime.strptime(DOB, r"%Y-%m-%d")

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