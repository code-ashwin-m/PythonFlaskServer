from system.types import UserData
from system.daos import UserDAO
import sqlite3, json

class UserService(): 
    def __init__(self):
        self.conn = sqlite3.connect('database/users.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.dao = UserDAO()

    def signup(self, userdata: UserData):
        current_user:UserData = self.dao.get_user_by_email(userdata.email)
        if (current_user != None):
            raise Exception("User already exists")
        user_new = self.dao.add_user(userdata)
        if (user_new == None):
            raise Exception("User not created")
        return userdata
    
    def signin(self, userdata: UserData):
        current_user = self.dao.get_user_by_email(userdata.email)

        if (current_user == None or current_user.password != userdata.password):
            raise Exception("Email/Password is invalid")
        return current_user

        
        
