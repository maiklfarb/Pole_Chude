# импорт класса TeleBot
from telebot import TeleBot
# Создание объекта TeleBot
Bot = TeleBot('Bot')
# Установка токена
Bot.config['api_key'] = '5449097213:AAEGC40fY9ccfEPoTF_IIG-wX_Eod1ESl80'
# Создание функции, которая на "привет" от пользователя,
# будет реагировать "hi!"
@Bot.route('привет')
def Hello_Handler(message):
    id = message['chat']['id']
    Bot.send_message(id,'hi')

# Создание функции, которая на "пока" от пользователя,
# будет реагировать "bb!"
@Bot.route('пока')
def Bb_Handler(message):
    id = message['chat']['id']
    Bot.send_message(id,'bb')

# Запуск бота
Bot.poll(debug=True)