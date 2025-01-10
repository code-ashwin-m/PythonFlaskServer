from daos import UserDAO, SecurityDao, AvailabilityDAO, SubjectDAO, TeacherSubjectDAO
import uuid
from typing import List, Optional
from model import User, Security, Subject, TeacherSubject, Availability

class UserService(): 
    def __init__(self):
        self.dao = UserDAO()
        self.securityDao = SecurityDao()

    def signup(self, user: User):
        current_user:User = self.dao.get_user_by_email(user.email)
        if (current_user != None):
            raise Exception("User already exists")
        self.dao.add_user(user)
        if (user.id == None):
            raise Exception("User not created")
        return user
    
    def signin(self, user: User):
        current_user = self.dao.get_user_by_email(user.email)
        if (current_user == None or current_user.password != user.password):
            raise Exception("Invalid credentials")
        token = str(uuid.uuid4());
        security = Security(None, current_user.id, token)
        self.securityDao.add_security(security)
        current_user.password = ""
        return current_user, security

    def signout(self, token: str):
        is_deteted = self.securityDao.delete_security_by_token(token)
        return is_deteted
    
    def security_check(self, token) -> Optional[Security]:
        security: Security = self.securityDao.get_security_by_token(token)
        if (security == None):
            raise Exception("Invalid/Expired token")
        return security
    
    def get_user_info_by_id(self, user_id: int):
        user = self.dao.get_user_by_id(user_id)
        return user
        
class ProfileService(): 
    def __init__(self):
        self.availability_dao = AvailabilityDAO()
        self.subject_dao = SubjectDAO()
        self.teacher_subject_dao = TeacherSubjectDAO()

    
    def add_availability(self, availability: Availability) -> Optional[Availability]:
        return self.availability_dao.add_availability(availability)
    
    def delete_availability(self, id: int):
        self.availability_dao.delete_availability(id)

    def get_all_availability_by_user_id(self, user_id: int) -> List[TeacherSubject]:
        return self.availability_dao.get_all_availability_by_user_id(user_id)
    
    def add_subject(self, teacher_subject: TeacherSubject):
        return self.teacher_subject_dao.add_subject(teacher_subject)
    
    def delete_subject(self, id: int):
        self.teacher_subject_dao.delete_subject(id)
    
    def get_all_subjects_by_user_id(self, user_id: int) -> List[TeacherSubject]:
        return self.teacher_subject_dao.get_all_subjects_by_user_id(user_id)
    
    def get_all_subjects(self) -> List[Subject]:
        return self.subject_dao.get_all_subjects()
    
    def get_all_teachers_by_subject_id(self, subject_id: int)-> List[TeacherSubject]:
        user_list = self.teacher_subject_dao.get_all_teachers_by_subject_id(subject_id)
        return user_list

    
