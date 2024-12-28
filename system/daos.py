import sqlite3, json
from typing import List, Optional
from system.types import UserData, SecurityDto
from datetime import datetime, timezone, timedelta

DB_URL = 'database/users.db'

class UserDAO:
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()

    def create_table(self):
        return None
    
    def add_user(self, user: UserData) -> Optional[UserData]:
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
        

    def get_user_by_email(self, email: str) -> Optional[UserData]:
        cursor = self.conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        self.conn.close
        if row:
            return UserData(*row)
        return None
    
    def get_user_by_id(self, id: int) -> Optional[UserData]:
        cursor = self.conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (id,)
        )
        row = cursor.fetchone()
        self.conn.close
        if row:
            return UserData(*row)
        return None
    
class SecurityDao:
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL, check_same_thread=False)
        self.create_table()
        self.time_change = timedelta(minutes=15) 
    
    def create_table(self):
        return None
    
    def add_security(self, securityDto: SecurityDto) -> Optional[SecurityDto]:
        with self.conn:
            datetime_now = datetime.now(timezone.utc)
            datetime_expire = datetime_now + self.time_change
            event_datetime = datetime_now.isoformat()
            securityDto.modified_datetime = event_datetime
            securityDto.created_datetime = event_datetime
            securityDto.expire_datetime = datetime_expire.isoformat()

            cursor = self.conn.execute(
                "INSERT INTO Security (user_id, token, expire_datetime, created_datetime, modified_datetime) VALUES (?, ?, ?, ?, ?)",
                (securityDto.user_id, securityDto.token, securityDto.expire_datetime, securityDto.created_datetime, securityDto.modified_datetime) 
            )
            self.conn.close
            securityDto.id = cursor.lastrowid
            return securityDto
    
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
    
    def delete_security_by_token(self, token: str) -> Optional[SecurityDto]:
        with self.conn:
            result = self.conn.execute(
                "DELETE FROM Security WHERE token = ?",
                (token,)
            )
            return result.rowcount > 0
        

