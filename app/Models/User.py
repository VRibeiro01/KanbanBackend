class User:
    user_id = 0
    username = ""
    password = ""

    def __init__(self, uid, username, password):
        self.user_id = uid
        self.username = username
        self.password = password

    def toJson(self):
        return {"user_id": self.user_id, "username": self.username,  "password": self.password}

