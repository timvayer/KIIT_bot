import telebot
from telebot import types
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}
user_reports = {}

# === ВИБІР ЛОКАЦІЇ ===
@bot.message_handler(commands=['start', 'звіт'])
def start_report(message):
    chat_id = message.chat.id
    user_reports[chat_id] = {"локація": None}
    user_states[chat_id] = "вибір_локації"

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📍 Руська, 3", callback_data="локація_руська"),
        types.InlineKeyboardButton("📍 Лепкого, 6", callback_data="локація_лепкого")
    )
    bot.send_message(chat_id, "Оберіть локацію для звіту:", reply_markup=markup)

# === ГОЛОВНЕ МЕНЮ ===
def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🥧 Готове", callback_data="готове"))
    markup.add(types.InlineKeyboardButton("🥶 Заморозка", callback_data="заморозка"))
    markup.add(types.InlineKeyboardButton("🥛 Молоко", callback_data="молоко"))
    markup.add(types.InlineKeyboardButton("💧 Напої", callback_data="напої"))
    markup.add(types.InlineKeyboardButton("🧃 Соки", callback_data="соки"))
    markup.add(types.InlineKeyboardButton("☕️ Кава / Матча / Чаї", callback_data="кава"))
    markup.add(types.InlineKeyboardButton("📦 Розхідники", callback_data="розхідники"))
    markup.add(types.InlineKeyboardButton("✅ Завершити звіт", callback_data="завершити"))
    bot.send_message(chat_id, "З чого почнемо?", reply_markup=markup)

# === ПЕРЕХОПЛЕННЯ КНОПОК ===
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("локація_"):
        локація = "Руська, 3" if data == "локація_руська" else "Лепкого, 6"
        user_reports[chat_id]["локація"] = локація
        user_states[chat_id] = "main_menu"
        show_main_menu(chat_id)
        return

    if data == "готове":
        bot.send_message(chat_id, "Розділ 'Готове' ще в розробці.")
    elif data == "заморозка":
        bot.send_message(chat_id, "Розділ 'Заморозка' ще в розробці.")
    elif data == "молоко":
        bot.send_message(chat_id, "Розділ 'Молоко' ще в розробці.")
    elif data == "напої":
        bot.send_message(chat_id, "Розділ 'Напої' ще в розробці.")
    elif data == "соки":
        bot.send_message(chat_id, "Розділ 'Соки' ще в розробці.")
    elif data == "кава":
        bot.send_message(chat_id, "Розділ 'Кава / Матча / Чаї' ще в розробці.")
    elif data == "розхідники":
        bot.send_message(chat_id, "Розділ 'Розхідники' ще в розробці.")
    elif data == "завершити":
        today = datetime.now().strftime("🗓️ %d.%m.%Y, %A")
        локація = user_reports.get(chat_id, {}).get("локація", "Локація не вказана")
        header = f"{today}\n📍 {локація}"
        bot.send_message(chat_id, f"{header}\n\n(Звіт ще не заповнено.)")
    else:
        bot.send_message(chat_id, "Невідома команда.")

# === ЗАПУСК ===
bot.polling()
