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

class SubjectDto:
    def __init__(self, id: int, name: str, created_datetime: Optional[str] = None, modified_datetime: Optional[str] = None):
        self.id = id
        self.name = name
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime

class AvailabilityDto:
    def __init__(self, id: int, user_id: int, 
                 start_time: Optional[str] = None, 
                 end_time: Optional[str] = None, 
                 days: Optional[str] = None, 
                 created_datetime: Optional[str] = None, 
                 modified_datetime: Optional[str] = None,):
        self.id = id  
        self.user_id = user_id 
        self.start_time = start_time 
        self.end_time = end_time 
        self.days = days 
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime

class TeacherSubjectDto:
    def __init__(self, id: int, user_id: int, subject_id: int,
                 created_datetime: Optional[str] = None, 
                 modified_datetime: Optional[str] = None,
                 extra: Optional[str] = None):
        self.id = id
        self.user_id = user_id 
        self.subject_id = subject_id    
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime
        self.extra = extra