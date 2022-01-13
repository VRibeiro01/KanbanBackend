class User:
    user_id = 0
    username = ""
    password = ""
    session_token = ""
    vali_date_from_token = any

    def __init__(self, uid, username, password, session_token, vali_date_from_token):
        self.user_id = uid
        self.username = username
        self.password = password
        self.session_token = session_token
        self.vali_date_from_token = vali_date_from_token

    def __repr__(self):
        return str({"user_id": self.user_id, "username": self.username}).replace("'", "\"")


