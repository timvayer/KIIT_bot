
import telebot
import os
from kiit_pie_bot import handle_pie_report
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN env var is missing. Please add it in the .env file.")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я працюю!")

handle_pie_report(bot)

bot.infinity_polling()
