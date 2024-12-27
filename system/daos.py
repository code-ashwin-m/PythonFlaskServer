import sqlite3
from typing import List, Optional
from system.types import UserData
from datetime import datetime, timezone

class UserDAO:
    def __init__(self):
        self.conn = sqlite3.connect('database/users.db', check_same_thread=False)
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
            user.id = cursor.lastrowid
            return user
        
    def get_user_by_email(self, email: str) -> Optional[UserData]:
        cursor = self.conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        if row:
            return UserData(*row)
        return None