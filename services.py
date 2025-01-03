from daos import UserDAO, SecurityDao, AvailabilityDAO, SubjectDAO, TeacherSubjectDAO
import uuid
from typing import List, Optional

from model import User, Security, Subject, TeacherSubject, Availability

class UserService(): 
    def __init__(self):
        self.dao = UserDAO()
        self.securityDao = SecurityDao()

    def signup1(self, user: User):
        current_user:User = self.dao.get_user_by_email1(user.email)
        if (current_user != None):
            raise Exception("User already exists")
        self.dao.add_user1(user)
        if (user.id == None):
            raise Exception("User not created")
        return user
    
    def signin1(self, user: User):
        current_user = self.dao.get_user_by_email1(user.email)
        if (current_user == None or current_user.password != user.password):
            raise Exception("Email/Password is invalid")
        token = str(uuid.uuid4());
        security = Security(None, current_user.id, token)
        self.securityDao.add_security1(security)
        return user, security

    def signout1(self, token: str):
        is_deteted = self.securityDao.delete_security_by_token1(token)
        return is_deteted
    
    def security_check1(self, token) -> Optional[Security]:
        security: Security = self.securityDao.get_security_by_token1(token)
        if (security == None):
            raise Exception("Invalid/Expired token")
        return security
    
    # def get_user_info_by_token(self, token: str):
    #     security: Security = self.securityDao.get_security_by_token1(token)
    #     user = self.dao.get_user_by_id(security.user_id)
    #     return user
    
    def get_user_info_by_id1(self, user_id: int):
        user = self.dao.get_user_by_id1(user_id)
        return user
        
class ProfileService(): 
    def __init__(self):
        self.availability_dao = AvailabilityDAO()
        self.subject_dao = SubjectDAO()
        self.teacher_subject_dao = TeacherSubjectDAO()

    
    def add_availability1(self, availability: Availability) -> Optional[Availability]:
        return self.availability_dao.add_availability1(availability)
    
    def delete_availability1(self, id: int):
        self.availability_dao.delete_availability1(id)

    def get_all_availability_by_user_id1(self, user_id: int) -> List[AvailabilityDto]:
        return self.availability_dao.get_all_availability_by_user_id1(user_id)
    
    def add_subject1(self, teacher_subject_dto: TeacherSubjectDto):
        return self.teacher_subject_dao.add_subject1(teacher_subject_dto)
    
    def delete_subject1(self, id: int):
        self.teacher_subject_dao.delete_subject1(id)
    
    def get_all_subjects_by_user_id1(self, user_id: int) -> List[TeacherSubject]:
        return self.teacher_subject_dao.get_all_subjects_by_user_id1(user_id)
    
    def get_all_subjects1(self) -> List[Subject]:
        return self.subject_dao.get_all_subjects1()
    
    def get_all_teachers_by_subject_id1(self, subject_id: int)-> List[TeacherSubject]:
        user_list = self.teacher_subject_dao.get_all_teachers_by_subject_id1(subject_id)
        return user_list

    
