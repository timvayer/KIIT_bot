import telebot
from flask import Flask, request

TOKEN = "7760817892:AAGAVTC5EZs_TJzhIkYuuXD9tvdTCo_bIKc"  # заміни на свій токен  # заміни на свій токен
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])  # зміна тут
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт! Я працюю.')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Ти сказав: {message.text}")

@app.route('/', methods=['GET'])
def index():
    return 'KIIT_bot is running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
