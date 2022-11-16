from telebot import TeleBot

app = TeleBot("Alica_Bot")
app.config['api_key'] = '5449097213:AAEGC40fY9ccfEPoTF_IIG-wX_Eod1ESl80'

def log(text):
    print(f"{text} -> {text}")

@app.route('/help')
def command_handler(dict_message):

    print(dict_message)
    id_chat = dict_message['chat']['id']
    print(id_chat)
    id = dict_message['from']['id']
    print(id)

    user_text = dict_message['text']
    user_text = user_text.split(' ')

    if (len(user_text) > 1):
        user_text = user_text[1]

    if (user_text == "info"):
        app.send_message(id_chat, "OK info")
        return

    app.send_message(id_chat, "OK")
    return



app.poll(debug=True)