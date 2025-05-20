import os
import logging
from flask import Flask, request
import openai
import telebot
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(API_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    user_text = message.text.strip()
    logging.info(f"Від користувача: {user_text}")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        response = completion.choices[0].message.content.strip()
        bot.send_message(message.chat.id, response)
    except Exception as e:
        logging.error(f"Помилка OpenAI: {e}")
        bot.send_message(message.chat.id, "Вибач, щось пішло не так...")

@app.route('/')
def index():
    return 'Бот працює!', 200

if __name__ == '__main__':
    app.run()