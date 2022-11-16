import json
from User import User

class DbContext:
    def __init__(self, connectionString):
        self.connectionString = connectionString
        self.users = []

        self.Load()

    def FindUser(self, chat_id):
        """ Метод посика пользователя по chat_id. """
        for user in self.users:
            if user.chat_id == chat_id:
                return user
        return None

    def Users(self):
        """ Метод получения актуального списка пользователей из БД.ы """
        self.Load()
        return self.users

    def Load(self):
        with open(f"{self.connectionString}/users.json", "r") as file:  # r - read чтение файла
            data = json.load(file)
            self.users = self.Deserialize(data)

    def Deserialize(self, data):
        """ Метод десериализация - конвертация словарей (поток байтов) в классы."""
        users = []

        for user in data["users"]:
            _user = User(user["chat_id"], user['first_name'], user['last_name'])
            users.append(_user)

        return users

    def Serialize(self, data):
        """ Метод сериализация - конвертация классов в словари (поток байтов)."""
        users = []
        for user in data:
            users.append({"chat_id": user.chat_id, "first_name": user.firstname, "last_name": user.lastname})
        return {"users": users}

    def Save(self):
        """ Метод сохранения данных в БД."""

        with open(f"{self.connectionString}/users.json", "w") as file:  # w - записьы
            data = self.Serialize(self.users)
            json.dump(data, file)
