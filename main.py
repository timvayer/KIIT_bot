import os
import telebot
import openai
from flask import Flask, request

# Зчитування токенів із середовища
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Перевірка наявності токенів
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не встановлено в Environment Variables.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не встановлено в Environment Variables.")

# Ініціалізація ботів
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

@app.route('/', methods=['GET'])
def index():
    return 'KIIT ChatGPT bot is running!'

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привіт! Я ChatGPT-бот. Напиши мені щось.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # можеш змінити на іншу модель
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message["content"]
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"Виникла помилка: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
