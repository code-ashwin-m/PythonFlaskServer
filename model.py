from typing import Optional
from orm.model import BaseModel, FieldInteger, FieldString, FieldForeign, FieldList
class User(BaseModel):
    _table = "Users"
    _fields = [
        FieldInteger('id', generated_id=True),
        FieldString('email', nullable=False, unique=True),
        FieldString('name', nullable=False),
        FieldString('password', nullable=False),
        FieldInteger('role', nullable=False),
        FieldString('pic_url', nullable=True),
        FieldString('created_datetime'),
        FieldString('modified_datetime')
    ]
    def __init__(self):
        pass

    def __init__(self, id: int = None, email: str = None, password: str = None, name: str = None, role: int = None, pic_url: Optional[str] = None, created_datetime: Optional[str] = None, modified_datetime: Optional[str] = None):
        self.id = id
        self.email = email
        self.name = name
        self.password = password
        self.role = role
        self.pic_url = pic_url
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime

class Security(BaseModel):
    _table = "Security"
    _fields = [
        FieldInteger('id', generated_id=True),
        FieldForeign('user_id', 'User'),
        FieldString('token', nullable=False),
        FieldString('expire_datetime', nullable=False),
        FieldString('created_datetime'),
        FieldString('modified_datetime')
    ]

    def __init__(self, id: int = None, user_id: str = None, token: str = None, expire_datetime: Optional[str] = None, created_datetime: Optional[str] = None, modified_datetime: Optional[str] = None):
        self.id = id
        self.user_id = user_id
        self.token = token
        self.expire_datetime = expire_datetime
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime

class Subject(BaseModel):
    _table = "Subjects"
    _fields = [
        FieldInteger('id', generated_id=True),
        FieldString('name', nullable=False),
        FieldString('created_datetime'),
        FieldString('modified_datetime')
    ]

    def __init__(self, id: int = None, name: str = None, created_datetime: Optional[str] = None, modified_datetime: Optional[str] = None):
        self.id = id
        self.name = name
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime


class Availability(BaseModel):
    _table = "Availabilities"
    _fields = [
        FieldInteger('id', generated_id=True),
        FieldForeign('user_id', 'User'),
        FieldString('start_time'),
        FieldString('end_time'),
        FieldString('days'),
        FieldString('created_datetime'),
        FieldString('modified_datetime')
    ]

    def __init__(self, id: int = None, user_id: int = None, 
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

class TeacherSubject(BaseModel):
    _table = "TeacherSubjects"
    _fields = [
        FieldInteger('id', generated_id=True),
        FieldForeign('user_id', 'User'),
        FieldForeign('subject_id', 'Subject'),
        FieldString('created_datetime'),
        FieldString('modified_datetime')
    ]

    def __init__(self, id: int = None, user_id: int = None, subject_id: int = None,
                 created_datetime: Optional[str] = None, 
                 modified_datetime: Optional[str] = None,
                 extra: Optional[str] = None):
        self.id = id
        self.user_id = user_id 
        self.subject_id = subject_id    
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime
        self.extra = extra