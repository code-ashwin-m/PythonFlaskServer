import sqlite3, json
from typing import List, Optional
from models import UserDto, SecurityDto, AvailabilityDto, SubjectDto, TeacherSubjectDto
from datetime import datetime, timezone, timedelta

DB_URL = 'database/users.db'

class UserDAO:
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()

    def create_table(self):
        return None
    
    def add_user(self, user: UserDto) -> Optional[UserDto]:
        with self.conn:
            event_datetime = datetime.now(timezone.utc).isoformat()
            user.modified_datetime = event_datetime
            user.created_datetime = event_datetime
            cursor = self.conn.execute(
                "INSERT INTO users (email, display_name, password, role, created_datetime, modified_datetime) VALUES (?, ?, ?, ?, ?, ?)",
                (user.email, user.display_name, user.password, user.role, user.created_datetime, user.modified_datetime) 
            )
            self.conn.close
            user.id = cursor.lastrowid
            return user
        

    def get_user_by_email(self, email: str) -> Optional[UserDto]:
        cursor = self.conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        self.conn.close
        if row:
            return UserDto(*row)
        return None
    
    def get_user_by_id(self, id: int) -> Optional[UserDto]:
        cursor = self.conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (id,)
        )
        row = cursor.fetchone()
        self.conn.close
        if row:
            return UserDto(*row)
        return None
    
class SecurityDao:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()
        self.time_change = timedelta(minutes=15) 
    
    def create_table(self):
        return None
    
    def add_security(self, security_dto: SecurityDto) -> Optional[SecurityDto]:
        with self.conn:
            datetime_now = datetime.now(timezone.utc)
            datetime_expire = datetime_now + self.time_change
            event_datetime = datetime_now.isoformat()
            security_dto.modified_datetime = event_datetime
            security_dto.created_datetime = event_datetime
            security_dto.expire_datetime = datetime_expire.isoformat()

            cursor = self.conn.execute(
                "INSERT INTO Security (user_id, token, expire_datetime, created_datetime, modified_datetime) VALUES (?, ?, ?, ?, ?)",
                (security_dto.user_id, security_dto.token, security_dto.expire_datetime, security_dto.created_datetime, security_dto.modified_datetime) 
            )
            self.conn.close
            security_dto.id = cursor.lastrowid
            return security_dto
    
    def get_security_by_token(self, token: str) -> Optional[SecurityDto]:
        cursor = self.conn.execute(
            "SELECT * FROM Security WHERE token = ?",
            (token,)
        )
        row = cursor.fetchone()
        self.conn.close
        if row:
            return SecurityDto(*row)
        return None
    
    def delete_security_by_token(self, token: str) -> bool:
        with self.conn:
            result = self.conn.execute(
                "DELETE FROM Security WHERE token = ?",
                (token,)
            )
            return result.rowcount > 0
        
class AvailabilityDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()
    
    def create_table(self):
        return None
    
    def add_availability(self, availability_dto: AvailabilityDto) -> Optional[AvailabilityDto]:
        with self.conn:
            datetime_now = datetime.now(timezone.utc)
            event_datetime = datetime_now.isoformat()
            availability_dto.modified_datetime = event_datetime
            availability_dto.created_datetime = event_datetime\

            # cursor = self.conn.execute(
            #     "INSERT INTO Availability (subject_id, user_id, start_date, end_date, start_time, end_time, days, created_datetime, modified_datetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            #     (availability_dto.subject_id, availability_dto.user_id, availability_dto.start_date, availability_dto.end_date, 
            #      availability_dto.start_time, availability_dto.end_time, availability_dto.days, availability_dto.created_datetime, availability_dto.modified_datetime) 
            # )

            cursor = self.conn.execute(
                "INSERT INTO Availability (user_id, start_time, end_time, days, created_datetime, modified_datetime) VALUES (?, ?, ?, ?, ?, ?)",
                (availability_dto.user_id, availability_dto.start_time, availability_dto.end_time, availability_dto.days, availability_dto.created_datetime, availability_dto.modified_datetime) 
            )
            self.conn.close
            availability_dto.id = cursor.lastrowid
            return availability_dto
    
    def delete_availability(self, id: int) -> bool:
        with self.conn:
            result = self.conn.execute(
                "DELETE FROM Availability WHERE id = ?",
                (id,)
            )
            return result.rowcount > 0

    def get_all_availability_by_user_id(self, user_id: int) -> List[AvailabilityDto]:
        with self.conn:
            result = self.conn.execute(
                "SELECT * FROM Availability WHERE user_id = ?",
                (user_id,)
            )
            rows = result.fetchall()
            self.conn.close
            return [AvailabilityDto(*row) for row in rows]
        
class SubjectDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()
    
    def create_table(self):
        return None

    def get_all_subjects(self) -> List[SubjectDto]:
        result = self.conn.execute(
            "SELECT * FROM Subjects"
        )
        rows = result.fetchall()
        self.conn.close
        return [SubjectDto(*row) for row in rows]
    
class TeacherSubjectDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()
    
    def create_table(self):
        return None
    
    def add_subject(self, teacher_subject_dto: TeacherSubjectDto) -> Optional[TeacherSubjectDto]:
        with self.conn:
            datetime_now = datetime.now(timezone.utc)
            event_datetime = datetime_now.isoformat()
            teacher_subject_dto.modified_datetime = event_datetime
            teacher_subject_dto.created_datetime = event_datetime\

            cursor = self.conn.execute(
                "INSERT INTO TeacherSubjects (user_id, subject_id, created_datetime, modified_datetime) VALUES (?, ?, ?, ?)",
                (teacher_subject_dto.user_id, teacher_subject_dto.subject_id, teacher_subject_dto.created_datetime, teacher_subject_dto.modified_datetime) 
            )

            self.conn.close
            teacher_subject_dto.id = cursor.lastrowid
            return teacher_subject_dto
        
    def delete_subject(self, id: int):
        with self.conn:
            result = self.conn.execute(
                "DELETE FROM TeacherSubjects WHERE id = ?",
                (id,)
            )
            return result.rowcount > 0
        
    def get_all_subjects_by_user_id(self, user_id: int) -> List[TeacherSubjectDto]:
        with self.conn:
            result = self.conn.execute(
                "SELECT TeacherSubjects.*, Subjects.name as 'subject_name' FROM TeacherSubjects INNER JOIN Subjects ON TeacherSubjects.subject_id = Subjects.id WHERE TeacherSubjects.user_id = ?",
                (user_id,)
            )
            rows = result.fetchall()
            self.conn.close
            return [TeacherSubjectDto(*row) for row in rows]