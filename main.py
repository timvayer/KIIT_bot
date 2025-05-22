import telebot
from telebot import types
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}
user_reports = {}

# === Нижнє меню ===
@bot.message_handler(commands=['start'])
def start_bot(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('/звіт')
    bot.send_message(chat_id, "Привіт! Обери команду нижче:", reply_markup=markup)

# === /звіт ===
@bot.message_handler(commands=['звіт'])
def start_report(message):
    chat_id = message.chat.id
    user_reports[chat_id] = {"локація": None, "готове": {}}
    user_states[chat_id] = "вибір_локації"

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📍 Руська, 3", callback_data="локація_руська"),
        types.InlineKeyboardButton("📍 Лепкого, 6", callback_data="локація_лепкого")
    )
    bot.send_message(chat_id, "Оберіть локацію для звіту:", reply_markup=markup)

# === Головне меню ===
def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🥧 Готове", callback_data="готове"),
        types.InlineKeyboardButton("🥶 Заморозка", callback_data="заморозка")
    )
    markup.row(
        types.InlineKeyboardButton("🥛 Молоко", callback_data="молоко"),
        types.InlineKeyboardButton("💧 Напої", callback_data="напої")
    )
    markup.row(
        types.InlineKeyboardButton("🧃 Соки", callback_data="соки"),
        types.InlineKeyboardButton("☕️ Кава / Матча / Чаї", callback_data="кава")
    )
    markup.row(
        types.InlineKeyboardButton("📦 Розхідники", callback_data="розхідники"),
        types.InlineKeyboardButton("✅ Завершити звіт", callback_data="завершити")
    )
    bot.send_message(chat_id, "З чого почнемо?", reply_markup=markup)

# === Обробка кнопок ===
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
        show_gotove_menu(chat_id)
    elif data == "готове_пироги":
        show_pies_list(chat_id)
    elif data.startswith("пиріг_"):
        emoji = data.replace("пиріг_", "")
        user_states[chat_id] = f"введення_кількості_{emoji}"
        bot.send_message(chat_id, f"Скільки шматків пирога {emoji} залишилось?")
    elif data.startswith("дата_"):
        parts = data.split("_")
        emoji = parts[1]
        день = parts[2]
        шматки = user_reports[chat_id]["готове"][emoji]["шматки"]
        user_reports[chat_id]["готове"][emoji]["день"] = день
        bot.send_message(chat_id, f"Збережено: {emoji} — {шматки} ({день})")
        show_pies_list(chat_id)
    elif data == "завершити":
        now = datetime.utcnow() + timedelta(hours=3)
        weekday = {
            'Monday': 'понеділок', 'Tuesday': 'вівторок', 'Wednesday': 'середа',
            'Thursday': 'четвер', 'Friday': 'пʼятниця', 'Saturday': 'субота', 'Sunday': 'неділя'
        }[now.strftime('%A')]
        дата = now.strftime(f"🗓️ %d.%m.%Y, {weekday}")
        локація = user_reports.get(chat_id, {}).get("локація", "Локація не вказана")
        bot.send_message(chat_id, f"{дата}\n📍 {локація}\n\n(Звіт ще не заповнено.)")

# === Підменю «Готове» ===
def show_gotove_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🥧 Пироги", callback_data="готове_пироги"),
        types.InlineKeyboardButton("🥟 Пиріжки", callback_data="готове_пиріжки"),
    )
    markup.add(
        types.InlineKeyboardButton("🥧 Галети", callback_data="готове_галети"),
    )
    bot.send_message(chat_id, "Що звітуємо першим?", reply_markup=markup)

# === Пироги ===
def show_pies_list(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)

    bot.send_message(chat_id, "*Мʼясні пироги:*", parse_mode='Markdown')
    markup.add(
        types.InlineKeyboardButton("🍗🍅🧀 Курка-томати-сир", callback_data="пиріг_🍗🍅🧀"),
        types.InlineKeyboardButton("🍗🍍🧀 Курка-ананас-сир", callback_data="пиріг_🍗🍍🧀"),
        types.InlineKeyboardButton("🍗🍄🧀 Курка-гриби-сир", callback_data="пиріг_🍗🍄🧀"),
        types.InlineKeyboardButton("🐄🧀 Телятина-сир", callback_data="пиріг_🐄🧀"),
        types.InlineKeyboardButton("🦃🫑 Індик-солодкий перець", callback_data="пиріг_🦃🫑")
    )
    bot.send_message(chat_id, ".", parse_mode='Markdown')

    bot.send_message(chat_id, "*Немʼясні пироги:*", parse_mode='Markdown')
    markup.add(
        types.InlineKeyboardButton("🧅 Цибулевий", callback_data="пиріг_🧅"),
        types.InlineKeyboardButton("🍄🧀 Гриби-сир", callback_data="пиріг_🍄🧀"),
        types.InlineKeyboardButton("🧀🍃 Сир-шпинат", callback_data="пиріг_🧀🍃"),
        types.InlineKeyboardButton("🧀 Сім сирів", callback_data="пиріг_🧀")
    )
    bot.send_message(chat_id, ".", parse_mode='Markdown')

    bot.send_message(chat_id, "*Солодкі пироги:*", parse_mode='Markdown')
    markup.add(
        types.InlineKeyboardButton("🍒🫐 Вишня-лохина", callback_data="пиріг_🍒🫐"),
        types.InlineKeyboardButton("🍒🧀 Вишня-сир", callback_data="пиріг_🍒🧀")
    )
    bot.send_message(chat_id, " ", parse_mode='Markdown')

    markup.add(types.InlineKeyboardButton("🔚 З пирогами — все", callback_data="готове"))

    bot.send_message(chat_id, "Оберіть пиріг:", reply_markup=markup)

# === Обробка введення кількості ===
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, "").startswith("введення_кількості_"))
def ask_baking_day(message):
    chat_id = message.chat.id
    state = user_states[chat_id]
    emoji = state.replace("введення_кількості_", "")
    кількість = message.text.strip()

    if not кількість.isdigit():
        bot.send_message(chat_id, "Введіть лише число.")
        return

    user_reports[chat_id]["готове"][emoji] = {"шматки": int(кількість)}
    user_states[chat_id] = f"вибір_дати_{emoji}"

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Сьогодні", callback_data=f"дата_{emoji}_2"),
        types.InlineKeyboardButton("Вчора", callback_data=f"дата_{emoji}_3"),
        types.InlineKeyboardButton("Позавчора", callback_data=f"дата_{emoji}_4")
    )
    bot.send_message(chat_id, "Коли був спечений цей пиріг?", reply_markup=markup)

# === Запуск ===
bot.polling()
