import os
import openai
from flask import Flask, request
import telebot

# Ініціалізація токенів
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# Відповідь від ChatGPT
def get_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # або "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "Ти — чемний Telegram-бот, який відповідає коротко й українською."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Помилка: {str(e)}"

# Обробка повідомлення
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    reply = get_gpt_response(user_input)
    bot.send_message(message.chat.id, reply)

# Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid request', 403

# Healthcheck
@app.route('/')
def index():
    return "Telegram-GPT бот працює!"

if __name__ == '__main__':
    app.run()
