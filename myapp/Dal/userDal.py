import mysql.connector as my
from myapp.Models.userModel import User 
from decimal import Decimal
from myapp.Dal.cnxDal import Database 


class UserDao:
    def __init__(self)->None:
        self.cnx = Database.get_connection()
        
    def getusers(self)->list:
        users:list[User]=[]
        query = "SELECT * FROM users;"
        if self.cnx != None :
            cursor=self.cnx.cursor(dictionary=True) 
            cursor.execute(query)
            rows=cursor.fetchall()
            for row in rows : # type: ignore
                users.append(User(username=row['username'],email=row['email'],password=row['password'],isadmin=row['isadmin'])) # type: ignore
        return rows
    
    def auth(self, login: str, password: str) -> User | None:
        query = "SELECT * FROM users WHERE email = %s;"
        
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query, (login,))
            row = cursor.fetchone()

            if row is not None:
            
                password = row['password'] # type: ignore
        
                return User(
                        username=row['username'],#type: ignore
                        email=row['email'],#type: ignore
                        password=row['password'],#type: ignore
                        isadmin=row['isadmin']#type: ignore
                    )

        return None
    

    def enregister(self, email: str, username: str, password: str) -> bool:
        query = "INSERT INTO users (email, username, password, isadmin) VALUES (%s, %s, %s, %s);"

        if self.cnx is not None:
                
                cursor = self.cnx.cursor(dictionary=True)
                cursor.execute("SELECT id FROM users WHERE email = %s;", (email,))
                existing_user = cursor.fetchone()
                if existing_user:
                    print(" Email déjà utilisé !")
                    return False

                
                cursor.execute(query, (email, username, password,0))
                self.cnx.commit()
                return True
        return False
    
if __name__ == "__main__":
    userDao = UserDao()
    lst_user = userDao.getusers()
    print(any(user['id'] == 2 and user['isadmin'] != 1 for user in lst_user))
    #print(userDao.register("hmizourais557@gmail.com","hamza rais","hamzay989"))
    #print(userDao.auth("admin@esisa.ma", "1234"))