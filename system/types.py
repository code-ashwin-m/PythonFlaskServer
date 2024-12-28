from datetime import datetime
from typing import Optional
class UserData:
    def __init__(self, id: int, email: str, password: str, display_name: str, role: int, pic_url: Optional[str] = None, created_datetime: Optional[str] = None, modified_datetime: Optional[str] = None):
        self.id = id
        self.email = email
        self.display_name = display_name
        self.password = password
        self.role = role
        self.pic_url = pic_url
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime