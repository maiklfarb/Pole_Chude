class User:
    def __init__(self,chat_id,firstname,lastname=None):
        self.chat_id = chat_id
        self.firstname = firstname
        self.lastname = lastname