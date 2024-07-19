#Returns a string with leading and trailing whitespaces from the string and returns it in title case if its a name
def clean_string(s: str, name: bool = False) -> str:
    s = s.strip()
    if name:
        return s.title()
    return s

#Allows user to input only integers
def get_Int(upper: int | None = None, lower: int | None = None, message: str = None) -> int:
    '''Get an integer subject to lower and upper bounds inclusive'''
    if message == None:
        message = ''
    while True:
        try:
            a = int(input(message))
            if upper == None and lower == None:
                print()
                break
            elif upper != None and a > upper:
                print(f"Kindly enter a number smaller than or equal to {upper}")
                print()
            elif lower != None and a < lower:
                print(f"Kindly enter a number larger than or equal to {lower}")
                print()
            return a
        except ValueError:
            print("Kindly enter an integer only")
            print()

#Allows user to input only whole numbers
def get_whole_num(message: str = None) -> int:
    return get_Int(lower = 0, message = message)

#Allows user to input only natural numbers
def get_natural_num(message: str = None) -> int:
    return get_Int(lower = 1, message = message)

#Allows user to input only negative integers
def get_negative_int(message: str = None) -> int:
    return get_Int(upper = -1, message = message)