import os
import logging
import openai
import telebot
from flask import Flask, request

# Logging
logging.basicConfig(level=logging.INFO)

# Environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# Flask app
app = Flask(__name__)

# Відповідь на будь-яке текстове повідомлення
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    user_input = message.text
    chat_id = message.chat.id
    logging.info(f"===> Нове повідомлення: {user_input}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=1000,
            temperature=0.7
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = "Помилка при зверненні до ChatGPT. Спробуй ще раз."
        logging.error(f"OpenAI error: {e}")

    bot.send_message(chat_id, reply)

# Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Unsupported Media Type', 415

# Set webhook (одноразово)
@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    bot.remove_webhook()
    success = bot.set_webhook(url=WEBHOOK_URL + "/webhook")
    return "Webhook встановлено" if success else "Помилка встановлення"

# Gunicorn entry point
if __name__ == '__main__':
    app.run(debug=True)
