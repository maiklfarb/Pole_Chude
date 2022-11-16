import datetime

from telebot import TeleBot #импортируем бота
from random import choice #импортируем рандом
from DbContext import DbContext
from User import User
# Константы используется для упрощения написания кода,
# ты в любой момент можешь просто напросто забыть
# как пишется то или иное слово, написать его в проверке неправильно
# в итоге программа не будет работать, а использование
# переменных позволяет тебе избегать таких случаев,
# так как написав часть название переменной, PyCharm подскажет, что дальше.

# константа победного случая
WIN_CASE = 'win'

# константа слова
WIN_LETTER_CASE = 'win_letter'

#константа проиграшного случая
LOOSE_CASE = 'loose'

# Объект бота
app = TeleBot("Pole_Chudes") # название бота
dbContext = DbContext("data")
# Сохраняем токен в словарь конфиг (настройки)
app.config['api_key'] = '5449097213:AAEGC40fY9ccfEPoTF_IIG-wX_Eod1ESl80'#токен бота

# Создаем комнаты
rooms = []
isStart = False

def rooms_generator(rooms, count):
    for i in range(count):
        rooms.append(generate_room(i))

def generate_room(id):
    room = {}
    room["id"] = f"Room_{id}"
    room["users"] = []
    room["game"] = {'word': None, 'letters': []}
    room["current_user"] = 0
    room['current_quantity'] = 0
    room['quantity'] = 5
    return room
rooms_generator(rooms,5)
print(rooms)
# словарь слов с их значением
words = {'арбуз': 'вид цветковых растений семейства тыквенных и название его съедобных плодов. '
                  'Вьющееся и тянущееся виноградное растение, это высоко культивируемый фрукт во '
                  'всем мире, насчитывающий более 1000 разновидностей.',
         'галерея': 'вытянутое в длину крытое помещение или переход между частями здания или соседними зданиями.',
         'принтер': 'предназначенное для вывода текстовой или графической информации, хранящейся в компьютере, на'
                    ' твёрдый физический носитель, обычно бумагу или полимерную плёнку, малыми тиражами (от единиц до сотен).',
         'утюг': 'элемент бытовой техники для разглаживания складок и заминов на одежде. Процесс разглаживания называют глажкой или глаженьем.',
         'ноутбук': 'переносной компьютер, в корпусе которого объединены типичные компоненты ПК, включая дисплей, клавиатуру и устройство указания'
                    ' (обычно сенсорная панель или тачпад), а также аккумуляторные батареи.'}

# Словарь, характеризующий текущее слово в игре, которое нужно угадать
# 'word' - само слово
# 'letters' - список неотгаданных букв
word = {'word': None, 'letters': []}

def log(username, text):
    """ Функция логирования, позволяет понять какой процесс происходит в данный момент времени"""
    print(f"{datetime.datetime.utcnow()} ->  {username}: {text}")

def randomWord():
    _words = []

    for k in words.keys():
        _words.append(k)
    word = choice(_words)

    return word

def splitWord(word):
    """ Возвращает список букв из слова """

    return list(word)

def GenerateWord(word):
    word['word'] = randomWord()
    word['letters'] = splitWord(word['word'])

    log("Bot", f"создано слово - {words}")

def WinUser(username):
    """ Функция обработки победы """

    # Заносим в лог информацию о победе
    log("Bot", f"победитель - {username}")

    # Генерируем новое слово для игрыы
    GenerateWord(word)

def CheckUserText(text, username):
    # Если текст пользователя совпал с загаданным словом
    if word['word'] == text:
        # Обрабатываем победу
        WinUser(username)
        # Возвращаем статус победыы
        return WIN_CASE
    # если пользователь угадал букву (если текст пользователя находится в неотгаданных буквах)
    elif text in word['letters']:
        # узнаем координаты буквы в слове
        coords = CheckLetterCoord(text, word['letters'])

        # удаляем буквы в этих колординатах
        for coord in coords:
            del word['letters'][coord]

        # логируем информацию о текущем состоянии игрыы
        log("Bot", f"текущее состояние - {word}")

        # Если неугаданных букв 0
        if len(word['letters']) == 0:
            # Обрабатываем победу
            WinUser(username)
            # Возвращаем статус победыы
            return WIN_CASE
        # Если остались неугаданные буквы
        else:
            # Обрабатываем действие "угадана буква"
            WinLetter(username)
            # Возвращаем статус - угадана буква
            return WIN_LETTER_CASE
    # Если не угадал бкву или слово
    else:
        # Обрабатываем поражение пользователя
        LooseUser(username)
        # Возвращаем статус пораженияы
        return LOOSE_CASE

def LooseUser(username):
    log(f"Bot", f"не отгодал буквуы - {username}")

def WinLetter(username):
    log(f"Bot", f"отгодал буквуы - {username}")

def CheckLetterCoord(letter, word):
    """ Функция поиска координат буквы в неоткаданных буквах """
    coords = []
    for i in range(len(word)):
        if word[i] == letter:
            coords.append(i)
    return coords

def show_word():
    """ Функция, которая возвращает представление слова для игрока
        в формате: _ _ _ _, где вместо _ стоят отгаданные буквы """

    # Объявляем переменную, где мы будем хранить представление
    text = ""

    # вытаскиваем текущее слово в игре
    hidden_word = word['word']

    # вытаскиваем текущий список букв в игруы
    hidden_letters = word['letters']

    # Начинаем проходить по координатам текущее слово в игреы
    for i in range(len(hidden_word)):
        # Сохраняем букву, на которой стоим при проходе
        letter = hidden_word[i]

        # Если текущая буква находится в списке неотгаданных букв
        if letter in hidden_letters:
            text += "_ "
        else:
            text += " " + letter

    # Возвращаем представление слова
    return text


def start_handler():
    """ Функция генерации слова для игры и сообщения о начале игры """

    # Генерирует текущее слово в игре
    GenerateWord(word)

    # создаем сообщение о начале игры
    message = f"Игра началась!\nУгадайте слово: {words[word['word']]}\n" \
              f"Текущий вариант: {show_word()}"

    # Возвращаем это сообщениеы
    return message

def status_handler(status):
    """ Функция обработки статустов """

    text = ""
    if status == WIN_CASE:
        text = f'ПОЗДРАВЛЯЕМ, ВЫ ВЫИГРАЛИ!'#присылаем если игрок угадал слово
    elif status == WIN_LETTER_CASE:
        text = f"Вы угадали букву! Текущий вариант: {show_word()}\n"#присылаем если игрок угадал букву
    elif status == LOOSE_CASE:
        text = f"Вы не угадали букву..."#присылаем если игрок не угадал букву
    return text

@app.route('(?!/).+')
def Command_Handler(message):
    """ Метод обработки функции пользовательского текста """

    # Вытаскиваем текст, который прислал пользователь
    user_text = message['text']

    # Вытаскиваем id чата, в которое бот должен будет отправить сообщение
    chat_id = message['chat']['id']

    # Вытаскиваем имя пользователя
    username = message['from']['first_name']
    user_surname = None
    try:  # в try заносишь блок кода, в котором потенциально могут возникнуть ошибки,
          # которые приведут к аварийному завершению программы

        # Пытаемся обратиться к фамилиии
        user_surname = message['from']['last_name']
    except KeyError:    # Указываешь (или не указываешь - если хочешь ловить все ошибки)
                        # ошибку которую ты хочешь отловить, сюда заносишь блок кода, который
                        # будет выполняться, если произойдет ошибка (т.е. программа не будет
                        # аварийно завершена, а выполнется код, напсианный в except)

        # Поймали KeyError - логируем
        log(username, "не имеет фамилии.")

    user = dbContext.FindUser(chat_id)
    if user == None:
        users = dbContext.Users()
        user = User(chat_id, username, user_surname)
        users.append(user)
        dbContext.Save()

    # Заносим в лог информацию о том, что и кто нам отправил
    log(username, f"chat: {chat_id} -> отправлен текст: {user_text}")

    # Если нам прислали слово start
    if user_text == 'start':
        # Запускаем функцию start и сохраняем информацию о старте
        message = start_handler()
        # отправляем информацию о старте в чат с id chat_id
        app.send_message(chat_id, message)
    # если не слово starts
    else:
        # Получаем статус обработки присланного текста (победа/поражение/отгадана буква)
        status = CheckUserText(user_text, username)

        # Получаем сообщение для пользователя по статусу
        message = status_handler(status)

        app.send_message(chat_id, message)

# запуск бота
app.poll(debug=True)

