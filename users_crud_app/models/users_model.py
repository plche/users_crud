from users_crud_app.config.mysqlconnection import connectToMySQL

class User:
    def __init__(self, id, first_name, last_name, email, created_at, updated_at):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def getUsers(cls):
        query = "SELECT * FROM users;"
        queryResult = connectToMySQL("users_schema").query_db(query)
        usersList = []
        for user in queryResult:
            usersList.append(User(user["id"], user["first_name"], user["last_name"], user["email"], user["created_at"], user["updated_at"]))
        return usersList
    
    @classmethod
    def addUser(cls, newUser):
        query = "INSERT INTO users(first_name, last_name, email) VALUES(%(first_name)s, %(last_name)s, %(email)s);"
        queryResult = connectToMySQL("users_schema").query_db(query, newUser)
        return queryResult

    @classmethod
    def getUser(cls, user):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        queryResult = connectToMySQL("users_schema").query_db(query, user)
        print("queryResult", type(queryResult))
        print("queryResult[0]", type(queryResult[0]))
        print("queryResult[0].created_at", type(queryResult[0]["created_at"]))
        return queryResult[0]

    @classmethod
    def updateUser(cls, user):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        queryResult = connectToMySQL("users_schema").query_db(query, user)
        return queryResult

    @classmethod
    def removeUser(cls, user):
        query = "DELETE FROM users WHERE id=%(id)s;"
        queryResult = connectToMySQL("users_schema").query_db(query, user)
        return queryResult