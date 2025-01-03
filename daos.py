import sqlite3, json
from typing import List, Optional
from datetime import datetime, timezone, timedelta

from orm.model import BaseDao
from model import User, Security, Subject, TeacherSubject, Availability

DB_URL = 'database/users.db'

BaseDao.set_database("database/app.db")
BaseDao.set_module("model")

class UserDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()
        BaseDao.create_table(User)

    def create_table(self):
        return None
    
    def add_user1(self, user: User) -> Optional[User]:
        event_datetime = datetime.now(timezone.utc).isoformat()
        user.modified_datetime = event_datetime
        user.created_datetime = event_datetime
        BaseDao.save(User, user)
        return user

    def get_user_by_email1(self, email: str) -> Optional[User]:
        users = BaseDao.execute_query(BaseDao.query_builder(User).select().where(email=email).build(), False)
        if len(users) > 0 :
            return users[0]
        return None
    
    def get_user_by_id1(self, id: int) -> Optional[User]:
        user = BaseDao.get_by_id(User, id)
        return user
    
class SecurityDao:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()
        BaseDao.create_table(Security)
        self.time_change = timedelta(minutes=15) 
    
    def create_table(self):
        return None
    
    def add_security1(self, security: Security) -> Optional[Security]:
        datetime_now = datetime.now(timezone.utc)
        datetime_expire = datetime_now + self.time_change
        event_datetime = datetime_now.isoformat()
        security.modified_datetime = event_datetime
        security.created_datetime = event_datetime
        security.expire_datetime = datetime_expire.isoformat()
        BaseDao.save(Security, security)
        return security
        
    def get_security_by_token1(self, token: str) -> Optional[Security]:
        securities = BaseDao.execute_query(BaseDao.query_builder(Security).select('*').where(token=token).build(), False)
        if len(securities) > 0:
            return securities[0]
        return None

    def delete_security_by_token1(self, token: str) -> bool:
        BaseDao.execute_query(BaseDao.delete_builder(Security).where(token=token).build())
        return True

class AvailabilityDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()
        BaseDao.create_table(Availability)

    def create_table(self):
        return None
    
    def add_availability1(self, availability: Availability) -> Optional[Availability]:
        datetime_now = datetime.now(timezone.utc)
        event_datetime = datetime_now.isoformat()
        availability.modified_datetime = event_datetime
        availability.created_datetime = event_datetime
        BaseDao.save(Availability, availability)
        return availability
    
    def delete_availability1(self, id: int) -> bool:
        BaseDao.execute_query(BaseDao.delete_builder(Availability).where(id=id).build())

    def get_all_availability_by_user_id1(self, user_id: int) -> List[Availability]:
        results = BaseDao.execute_query(BaseDao.query_builder(Availability).select('*').where(user_id=user_id).build())
        return results
        
class SubjectDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()
        BaseDao.create_table(Subject)
    
    def create_table(self):
        return None

    def get_all_subjects1(self) -> List[Subject]:
        return BaseDao.all(Subject, False)

class TeacherSubjectDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()
        BaseDao.create_table(TeacherSubject)
    
    def create_table(self):
        return None
        
    def add_subject1(self, teacher_subject: TeacherSubject) -> Optional[TeacherSubject]:
        datetime_now = datetime.now(timezone.utc)
        event_datetime = datetime_now.isoformat()
        teacher_subject.modified_datetime = event_datetime
        teacher_subject.created_datetime = event_datetime
        BaseDao.save(TeacherSubject, teacher_subject)
        if teacher_subject.id != None:
            return teacher_subject
        return None
    
    def delete_subject1(self, id: int):
        BaseDao.execute_query(BaseDao.delete_builder(TeacherSubject).where(id=id).build())
        
    def get_all_subjects_by_user_id1(self, user_id: int) -> List[TeacherSubject]:
        query = BaseDao.query_builder(TeacherSubject).build()
        query.query = "SELECT TeacherSubjects.*, Subjects.name as 'extra' FROM TeacherSubjects INNER JOIN Subjects ON TeacherSubjects.subject_id = Subjects.id WHERE TeacherSubjects.user_id = ?"
        query.params.append(user_id)
        return BaseDao.execute_query(query, False)

    def get_all_teachers_by_subject_id1(self, subject_id: int) -> List[TeacherSubject]:
        query = BaseDao.query_builder(TeacherSubject).build()
        query.query = "SELECT TeacherSubjects.*, Users.name as 'extra' FROM TeacherSubjects INNER JOIN Users ON TeacherSubjects.user_id = Users.id WHERE TeacherSubjects.subject_id = ?"
        query.params.append(subject_id)
        return BaseDao.execute_query(query, False)