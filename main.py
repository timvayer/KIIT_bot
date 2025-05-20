import telebot
from flask import Flask, request

TOKEN = "7760817892:AAGAVTC5EZs_TJzhlkYuuXD9tvdTCo_bIKc"
bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Я працюю.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Ти сказав: {message.text}")

@app.route('/', methods=['GET'])
def index():
    return 'KIIT_bot is running'

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url="https://kiit-bot.onrender.com/webhook")
    app.run(host='0.0.0.0', port=10000)
