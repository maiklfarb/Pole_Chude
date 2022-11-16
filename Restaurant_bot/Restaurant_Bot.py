from telebot import TeleBot
from Client import Client
from datetime import datetime

app = TeleBot("Restaurant_Bot")
app.config['api_key'] = '5449097213:AAEGC40fY9ccfEPoTF_IIG-wX_Eod1ESl80'
users = []

def log(text):
    print(f"{datetime.now()} -> {text}")

def find_user_by_id(id):
    for user in users:
        if user.id == id:
            return user
    return None

@app.route('/help')
def command_handler(dict_message):
    id_chat = dict_message['chat']['id']
    id = dict_message['from']['id']
    name = dict_message['from']['first_name']

    found_user = find_user_by_id(id)

    if found_user == None:
        found_user = Client(id, id_chat, name)
        users.append(found_user)
        log(f'Создан новый пользователь: {found_user.name} {found_user.role}')


    app.send_message(id_chat, found_user.Get_Commands())
    log(f'{id} - /help')


# Запуск бота
app.poll(debug=True)