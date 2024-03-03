from datetime import datetime

class Event:
    def __init__(self, event_id: str, event_title: str, date: str | datetime, event_description: str | None = None, 
                 head1: str | None = None, head2: str | None = None) -> None:
        '''
        Formate for date is dd-mm-YYYY
        '''
       
        #Data cleaning for event_id
        if type(event_id) != str:
            raise TypeError("Event_ID should be a string")
        elif len(event_id) != 5:
            raise ValueError("The Event_ID should be 5 characters long only")
        elif event_id[0].upper() not in ('M', 'E'):
            raise ValueError("The beginning of Event_ID should be either E for event or M for Meeting")
        elif not event_id[1:].isnumeric():
            raise ValueError("The last 4 characters should be numeric")
        
        #data accepted
        self.event_id: str = event_id.upper()

        #data cleaning for event_title
        if type(event_title) != str:
            raise TypeError("Event_title should be string type")
        elif len(event_title) > 100:
            raise OverflowError("Title is too long")
        elif len(event_title) == 0:
            raise ValueError("Expected some title")
        
        #data accepted
        self.event_title: str = event_title.strip().title()

        #data cleaning for event description
        if event_description != None and type(event_description) != str:
            raise TypeError("Event description should either be none or string")
        elif event_description != None and len(event_description) > 1000:
            raise OverflowError("Description is too long")
        elif event_description == '':
            event_description = None
        
        #data accepted
        if event_description == None:
            event_description = 'Description not provided'
        self.event_description: str = event_description

        #data cleaning for event_date
        if type(date) not in (str, datetime):
            raise TypeError("date should be passed as string or datetime format")
        elif type(date) == str and len(date) != 10:
            raise ValueError("Invalid date")
        
        #data accepted
        if type(date) == datetime:
            self.date: datetime = date
        else:
            self.date: datetime = datetime.strptime(date, r"%d-%m-%Y")
        
        #data cleaning for head1 and head2
        if head1 != None and type(head1) != str:
            raise TypeError("Head 1 should be either none or a string")
        elif head1 != None and len(head1) != 9:
            raise ValueError("Head 1 should be a valid id of the person")
        
        #Data accepted
        if head1 != None:
            self.head1: str | None = head1.strip().title()
        else:
            self.head1: str | None = head1

        #data cleaning for head1 and head2
        if head2 != None and type(head2) != str:
            raise TypeError("Head 2 should be either none or a string")
        elif head2 != None and len(head2) != 9:
            raise ValueError("Head 2 should be a valid id of the person")
        
        #Data accepted
        if head2 != None:
            self.head2: str | None = head2.strip().title()
        else:
            self.head2: str | None = head2


    #defining getters
    def get_event_id(self) -> str:
        return self.event_id
    
    def get_event_name(self)-> str:
        return self.event_title
    
    def get_event_date_str(self, processing: bool = False) -> str:
        assert type(processing) == bool , "Processing should be a boolean"

        if not processing:
            return self.date.strftime(r"%Y-%m-%d")
        else:
            return self.date.strftime(r"%d %B %Y")
        
    def get_event_date_datetime(self) -> datetime:
        return self.date
    
    def get_event_desc(self) -> str:
        return self.event_description
    
    def get_event_head1(self) -> str:
        if self.head1 == None:
            return "No event head 1"
        else:
            return self.head1
        
    def get_event_head2(self) -> str:
        if self.head2 == None:
            return "No event head 2"
        else:
            return self.head2
        
    def head1_exists(self) -> bool:
        if self.head1 == None:
            return False
        return True
    
    def head2_exists(self) -> bool:
        if self.head2 == None:
            return False
        return True
    
    def check_days(self) -> int:
        '''
        Returns number of days left
        If negative, then date has passed
        '''
        date = datetime.now()
        diff = self.date - date
        return diff.days

    #Defining setters

    def set_event_id(self, event_id: str):
        if type(event_id) != str:
            raise TypeError("Event_ID should be a string")
        elif len(event_id) != 5:
            raise ValueError("The Event_ID should be 5 characters long only")
        elif event_id[0].upper() not in ('M', 'E'):
            raise ValueError("The beginning of Event_ID should be either E for event or M for Meeting")
        elif not event_id[1:].isnumeric():
            raise ValueError("The last 4 characters should be numeric")
        
        self.event_id: str = event_id


    def set_event_name(self, event_name):
        if type(event_name) != str:
            raise TypeError("Event_title should be string type")
        elif len(event_name) > 100:
            raise OverflowError("Title is too long")
        elif len(event_name) == 0:
            raise ValueError("Expected some title")
        
        self.event_title: str = event_name


    def set_event_date(self, date: str | datetime):
        '''
        Date to be enttered in 'DD-MM-YYYY' format
        '''

        if type(date) not in (str, datetime):
            raise TypeError("date should be passed as string or datetime format")
        elif type(date) == str and len(date) != 10:
            raise ValueError("Invalid date")
        
        if type(date) == datetime:
            self.date: datetime = date
        else:
            self.date: datetime = datetime.strptime(date, r"%d-%m-%Y")

    def set_event_desc(self, event_description: str | None = None):
        '''
        By default None
        '''
        if event_description != None and type(event_description) != str:
            raise TypeError("Event description should either be none or string")
        elif event_description != None and len(event_description) > 1000:
            raise OverflowError("Description is too long")
        elif event_description == '':
            event_description = None

        if event_description == None:
            event_description = 'Description not provided'
        self.event_description: str = event_description

    def set_event_head1(self, head1: str | None):
        if head1 != None and type(head1) != str:
            raise TypeError("Head 1 should be either none or a string")
        elif head1 != None and len(head1) != 9:
            raise ValueError("Head 1 should be a valid id of the person")
        
        if head1 != None:
            self.head1: str | None = head1.strip().title()
        else:
            self.head1: str | None = head1

    def set_event_head2(self, head2: str | None):
        if head2 != None and type(head2) != str:
            raise TypeError("Head 2 should be either none or a string")
        elif head2 != None and len(head2) != 9:
            raise ValueError("Head 2 should be a valid id of the person")
        
        if head2 != None:
            self.head2: str | None = head2.strip().title()
        else:
            self.head2: str | None = head2

    
