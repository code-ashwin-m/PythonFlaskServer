from typing import Optional

class UserDto:
    def __init__(self, id: int, email: str, password: str, display_name: str, role: int, pic_url: Optional[str] = None, created_datetime: Optional[str] = None, modified_datetime: Optional[str] = None):
        self.id = id
        self.email = email
        self.display_name = display_name
        self.password = password
        self.role = role
        self.pic_url = pic_url
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime

class SecurityDto:
    def __init__(self, id: int, user_id: str, token: str, expire_datetime: Optional[str] = None, created_datetime: Optional[str] = None, modified_datetime: Optional[str] = None):
        self.id = id
        self.user_id = user_id
        self.token = token
        self.expire_datetime = expire_datetime
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime

class AvailabilityDto:
    def __init__(self, id: int, subject_id: int, user_id: int, 
                 start_date: Optional[str] = None, 
                 end_date: Optional[str] = None, 
                 start_time: Optional[str] = None, 
                 end_time: Optional[str] = None, 
                 days: Optional[str] = None, 
                 created_datetime: Optional[str] = None, 
                 modified_datetime: Optional[str] = None,
                 subject_name: Optional[str] = None):
        self.id = id
        self.subject_id = subject_id    
        self.user_id = user_id 
        self.start_date = start_date 
        self.end_date = end_date 
        self.start_time = start_time 
        self.end_time = end_time 
        self.days = days 
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime
        self.subject_name = subject_name