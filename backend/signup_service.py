from models.userdata import UserData
import sqlite3

class SignUpService():
    def __init__(self):
        self.conn = sqlite3.connect('database/users.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def signup(self, userdata: UserData):
        #Already existin user, if yes "user already exists"
        #Table insert entry
        
        statement ="SELECT * FROM Users WHERE EmailID = \"" + userdata.username + "\" AND PasswordHash = \"" + userdata.password + "\""
        print (statement)

        self.cursor.execute(statement)
        output = self.cursor.fetchall() 

        for row in output: 
            print(row) 
        
        if (len(output) > 0):
            row = output[0]

            if (row[1] == userdata.username and row[3] == userdata.password):
                return "Signed In"
            else:
                return "Incorrect email or password"
        else:
            return "User is not present"
        
        
        
            