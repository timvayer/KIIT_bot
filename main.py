from telebot import TeleBot, types
from handlers.report import handle_report
from handlers.gotove import handle_gotove
from handlers.pyrizhky import handle_pyrizhky
from handlers.finalize import handle_finalize
from handlers.state import State

import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/звіт')
    bot.send_message(message.chat.id, "Привіт! Натисни /звіт, щоб розпочати.", reply_markup=markup)

@bot.message_handler(commands=['звіт'])
def report(message):
    handle_report(bot, message)

# Обробники категорій
@bot.callback_query_handler(func=lambda call: call.data.startswith("готове"))
def gotove_callback(call):
    handle_gotove(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("пиріжки"))
def pyrizhky_callback(call):
    handle_pyrizhky(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("завершити"))
def finalize_callback(call):
    handle_finalize(bot, call)

print("Бот працює...")
bot.infinity_polling()