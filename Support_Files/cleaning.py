def clean_string(s: str, name: bool = False):
    s = s.strip()
    if name:
        return s.title()
    return s

def get_Int(upper: int = None, lower: int = None):
    '''Get an integer subject to lower and upper bounds inclusive'''
    while True:
        try:
            a = int(input())
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
