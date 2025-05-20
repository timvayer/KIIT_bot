
import os
import logging
from flask import Flask, request
import openai
from telebot import TeleBot

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація змінних середовища
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    logging.error("TELEGRAM_TOKEN не знайдено в середовищі")
if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY не знайдено в середовищі")

bot = TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    logging.info(f"Отримано повідомлення: {user_text}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        reply = response['choices'][0]['message']['content']
        logging.info(f"Відповідь від OpenAI: {reply}")
    except Exception as e:
        reply = "Вибач, сталася помилка при зверненні до OpenAI."
        logging.error(f"Помилка OpenAI: {e}")

    try:
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        logging.error(f"Помилка при надсиланні повідомлення: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        logging.info("===> Отримано повідомлення через webhook")
        bot.process_new_updates([bot.types.Update.de_json(json_string)])
        return '', 200
    else:
        logging.warning("===> Запит без JSON")
        return '', 403

if __name__ == "__main__":
    app.run()
