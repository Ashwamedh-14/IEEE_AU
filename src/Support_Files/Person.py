import datetime as dt

FOOD: dict[int: str] = {1: "Non-Vegetarian", 2: "Vegetarian (With Onion and Garlic)",
        3: "Vegetarian (Without Onion and Garlic)", 4: "Jain",
        5: "Vegan",6: "Unknown"
        }
class Person:
    def __init__(self, name: str, DOB: str | dt.date, food_preference: str):
        '''DOB must be in YYYY-MM-DD format'''
        if type(name) != str or (type(DOB) not in (str, dt.date) and DOB != None) or (food_preference != None and type(food_preference) != str):
            raise TypeError("Incorrect types passed to name or DOB")

        self.name: str = (name.strip()).title()
        if type(DOB) == str:
            self.DOB: dt.datetime = dt.datetime.strptime(DOB.strip(), r"%Y-%m-%d")
        else:
            self.DOB: dt.datetime = DOB

        if food_preference == None:
            self.food_preference: int = 6
            return

        for i, j in FOOD.items():
            if food_preference.lower() == j.lower():
                self.food_preference: int = i
                break
        else:
            self.food_preference: int = 6


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
        
    def get_food_choice(self) -> str:
        return FOOD[self.food_preference]
    
    def set_name(self, name: str):
        if type(name) != str:
            raise TypeError("Incorrect type passed to name")
        self.name = (name.strip()).title()

    def set_DOB(self, DOB: str | dt.datetime):
        '''
        DOB should be in YYYY-MM-DD format
        '''
        if DOB not in (str, dt.datetime):
            raise ValueError("Incorrect type passed to DOB")
        elif type(DOB) == str:
            self.DOB: dt.datetime = dt.datetime.strptime(DOB.strip(), r"%Y-%m-%d")
        else:
            self.DOB: dt.datetime = DOB
    
    def set_food_choice(self, food_preference: str):
        if food_preference == None or type(food_preference) != str:
            self.food_preference: int = 6
            return
        for i, j in FOOD.items():
            if food_preference.lower == j.lower():
                self.food_preference: int = i
                break
        else:
            self.food_preference: int = 6

class User(Person):
    def __init__(self, name: str, DOB: str | dt.date, user_id: str, password: str, phno: int = None, email: str = None):
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
    def __init__(self, name: str, DOB: str | dt.date, security_key: str | int):
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
    def __init__(self, name: str, DOB: str | dt.date, emp_ID: str, DOJ: str | dt.date, role: str, contant_no: int, email: str, food_preference: str):
        super().__init__(name, DOB,food_preference)
        if type(emp_ID) != str or type(DOJ) not in (str, dt.date) or type(role) != str or type(contant_no) != int or type(email) != str:
            raise TypeError("Incorrect types passed to arguments, emp_ID, DOJ, role, contact_no or email")
        self.emp_ID: str = emp_ID.strip().upper()
        if type(DOJ) == str:
            self.DOJ: dt.datetime = dt.datetime.strptime(DOJ, r"%Y-%m-%d")
        else:
            self.DOJ: dt.datetime = DOJ
        if role == '':
            role = None
        else:
            self.role: str = role.strip().title()
        
        if contant_no // 10 ** 9 in (1,2,3,4,5,6,7,8,9):
            self.contact: int = contant_no
        else:
            self.contact: int = None

        self.email: str = email
        

        

    def __str__(self):
        return f'''Name: {self.name}\nDOB: {self.DOB}\nEmployee ID: {self.emp_ID}\nDate of Joining: {self.DOJ}\nRole: {self.role}'''

    def get_empID(self) -> str:
        return self.emp_ID
    
    def get_DOJ_str(self, processing: bool = False) ->str:
        if type(processing) != bool:
            raise ValueError("Processing should be of type bool")
        if processing:
            return self.DOJ.strftime(r"%Y-%m-%d")
        else:
            return self.DOJ.strftime(r"%d-%B-%Y")
    
    def get_DOJ_dt(self):
        return self.DOJ
    
    def get_role(self) -> str | None:
        return self.role
    
    def get_contact(self) -> int | str:
        if self.contact == None:
            return "Contact not given"
        return self.contact
    
    def get_email(self):
        return self.email
    
    def set_empID(self, empID: str):
        if type(empID) != str:
            raise TypeError("Incorrect type passed")
        self.emp_ID: str = empID.strip()

    def set_DOJ(self, DOJ: str | dt.datetime):
        if type(DOJ) not in (str, dt.datetime):
            raise TypeError("DOJ should be either string or datetime object")
        if type(DOJ) == str:
            self.DOJ: dt.datetime = dt.datetime.strptime(DOJ.strip(), r"%Y-%m-%d")
        else:
            self.DOJ = DOJ
    
    def set_role(self, role: str):
        if type(role) not in (str, None):
            raise TypeError("Role should be a string")
        self.role = role.strip()

    def set_contact(self, contact_no: int):
        if type(contact_no) != int:
            raise TypeError("Incorrect type passed to contact no")
        elif contact_no // 10 ** 9 not in (1,2,3,4,5,6,7,8,9):
            raise ValueError("Incorrect phone number is passed")
        else:
            self.contact: int = contact_no

    def set_email(self, email: str):
        if type(email) != str:
            raise TypeError("Incorrect type passed to email")
        else:
            self.email = email
