from models import UserDto, SecurityDto, AvailabilityDto, SubjectDto, TeacherSubjectDto
from daos import UserDAO, SecurityDao, AvailabilityDAO, SubjectDAO, TeacherSubjectDAO
import sqlite3, json, uuid
from typing import List, Optional

class UserService(): 
    def __init__(self):
        self.dao = UserDAO()
        self.securityDao = SecurityDao()

    def signup(self, userdata: UserDto):
        current_user:UserDto = self.dao.get_user_by_email(userdata.email)
        if (current_user != None):
            raise Exception("User already exists")
        user_new = self.dao.add_user(userdata)
        if (user_new == None):
            raise Exception("User not created")
        return userdata
    
    def signin(self, userdata: UserDto):
        current_user = self.dao.get_user_by_email(userdata.email)

        if (current_user == None or current_user.password != userdata.password):
            raise Exception("Email/Password is invalid")
        
        token = str(uuid.uuid4());
        securityDto = SecurityDto(None, current_user.id, token)
        securityDto_new = self.securityDao.add_security(securityDto)
    
        return {
            'user': current_user.to_dict(),
            'security': securityDto_new.to_dict()
        }
    
    def signout(self, token: str):
        is_deteted = self.securityDao.delete_security_by_token(token)
        return is_deteted

    def security_check(self, token) -> Optional[SecurityDto]:
        securityDto: SecurityDao = self.securityDao.get_security_by_token(token)
        if (securityDto == None):
            raise Exception("Invalid/Expired token")
        return securityDto
    
    def get_user_info_by_token(self, token: str):
        securityDto: SecurityDto = self.securityDao.get_security_by_token(token)
        user = self.dao.get_user_by_id(securityDto.user_id)
        return user
    
    def get_user_info_by_id(self, user_id: int):
        user = self.dao.get_user_by_id(user_id)
        return user
        
class ProfileService(): 
    def __init__(self):
        self.availability_dao = AvailabilityDAO()
        self.subject_dao = SubjectDAO()
        self.teacher_subject_dao = TeacherSubjectDAO()

    
    def add_availability(self, availability_dto: AvailabilityDto) -> Optional[AvailabilityDto]:
        new_item = self.availability_dao.add_availability(availability_dto)
        return new_item
    
    def delete_availability(self, id: int):
        self.availability_dao.delete_availability(id)

    def get_all_availability_by_user_id(self, user_id: int) -> List[AvailabilityDto]:
        list_items = self.availability_dao.get_all_availability_by_user_id(user_id)
        return list_items
    
    def add_subject(self, teacher_subject_dto: TeacherSubjectDto):
        new_item = self.teacher_subject_dao.add_subject(teacher_subject_dto)
        return new_item
    
    def delete_subject(self, id: int):
        self.teacher_subject_dao.delete_subject(id)
    
    def get_all_subjects_by_user_id(self, user_id: int) -> List[TeacherSubjectDto]:
        list_items = self.teacher_subject_dao.get_all_subjects_by_user_id(user_id)
        return list_items
    
    def get_all_subjects(self) -> List[SubjectDto]:
        list_items = self.subject_dao.get_all_subjects()
        return list_items
    
    def get_all_teachers_by_subject_id(self, subject_id: int)-> List[TeacherSubjectDto]:
        user_list = self.teacher_subject_dao.get_all_teachers_by_subject_id(subject_id)
        return user_list

    
