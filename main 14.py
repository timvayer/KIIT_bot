import telebot
from telebot import types
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# === СТАНИ КОРИСТУВАЧІВ ===
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

# === СТАРТ ===
@bot.message_handler(commands=['start', 'звіт'])
def start_report(message):
    chat_id = message.chat.id
    user_reports[chat_id] = {}
    user_states[chat_id] = "main_menu"

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
    markup.add(types.InlineKeyboardButton("🥶 Заморозка", callback_data="заморозка"))
    markup.add(types.InlineKeyboardButton("🥛 Молоко", callback_data="молоко"))
    markup.add(types.InlineKeyboardButton("💧 Напої", callback_data="напої"))
    markup.add(types.InlineKeyboardButton("🧃 Соки", callback_data="соки"))
    markup.add(types.InlineKeyboardButton("☕️ Кава / Матча / Чаї", callback_data="кава"))
    markup.add(types.InlineKeyboardButton("📦 Розхідники", callback_data="розхідники"))
    markup.add(types.InlineKeyboardButton("✅ Завершити звіт", callback_data="завершити"))

    bot.send_message(chat_id, "З чого почнемо?", reply_markup=markup)

# === ПЕРЕХОПЛЕННЯ КНОПОК ===
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
    markup.add(types.InlineKeyboardButton("🥶 Заморозка", callback_data="заморозка"))
    markup.add(types.InlineKeyboardButton("🥛 Молоко", callback_data="молоко"))
    markup.add(types.InlineKeyboardButton("💧 Напої", callback_data="напої"))
    markup.add(types.InlineKeyboardButton("🧃 Соки", callback_data="соки"))
    markup.add(types.InlineKeyboardButton("☕️ Кава / Матча / Чаї", callback_data="кава"))
    markup.add(types.InlineKeyboardButton("📦 Розхідники", callback_data="розхідники"))
    markup.add(types.InlineKeyboardButton("✅ Завершити звіт", callback_data="завершити"))
    bot.send_message(chat_id, "З чого почнемо?", reply_markup=markup)

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

    chat_id = call.message.chat.id
    data = call.data

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
        uk_weekdays = {
    'Monday': 'понеділок',
    'Tuesday': 'вівторок',
    'Wednesday': 'середа',
    'Thursday': 'четвер',
    'Friday': 'пʼятниця',
    'Saturday': 'субота',
    'Sunday': 'неділя'
}
today_dt = datetime.now()
day_name = uk_weekdays[today_dt.strftime('%A')]
today = today_dt.strftime(f"🗓️ %d.%m.%Y, {day_name}")
        header = f"{today}\n📍 Руська, 3"
        bot.send_message(chat_id, f"{header}\n\n(Звіт ще не заповнено.)")
    else:
        bot.send_message(chat_id, "Невідома команда.")

# === ЗАПУСК ===
bot.polling()

# === Пироги для блоку "Готове" ===
pies_list = {
    "🍗🍅🧀": "Курка-томати-сир",
    "🍗🍍🧀": "Курка-ананас-сир",
    "🍗🍄🧀": "Курка-гриби-сир",
    "🐄🧀": "Телятина-сир",
    "🦃🫑": "Індик-солодкий перець",
    "🧅": "Цибулевий",
    "🍄🧀": "Гриби-сир",
    "🧀🍃": "Сир-шпинат",
    "🧀": "Сім сирів",
    "🍒🫐": "Вишня-лохина",
    "🍒🧀": "Вишня-сир"
}

@bot.callback_query_handler(func=lambda call: call.data == "готове")
def handle_gotove(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = "готове_категорія"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🥧 Пироги", callback_data="готове_пироги"))
    markup.add(types.InlineKeyboardButton("🥟 Пиріжки", callback_data="готове_пиріжки"))
    markup.add(types.InlineKeyboardButton("🥧 Галети", callback_data="готове_галети"))
    markup.add(types.InlineKeyboardButton("↩ Назад", callback_data="back_to_menu"))

    bot.send_message(chat_id, "Що саме звітуємо в «Готове»?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "готове_пироги")
def show_pies_list(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = "вибір_пирога"

    markup = types.InlineKeyboardMarkup(row_width=2)
    for emoji, name in pies_list.items():
        markup.add(types.InlineKeyboardButton(f"{emoji} {name}", callback_data=f"пиріг_{emoji}"))
    markup.add(types.InlineKeyboardButton("↩ Назад", callback_data="готове"))

    bot.send_message(chat_id, "Оберіть пиріг:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("пиріг_"))
def ask_pie_quantity(call):
    chat_id = call.message.chat.id
    emoji = call.data.replace("пиріг_", "")
    user_states[chat_id] = f"введення_кількості_{emoji}"
    bot.send_message(chat_id, f"Скільки шматків пирога {emoji} залишилось?")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, "").startswith("введення_кількості_"))
def ask_baking_day(message):
    chat_id = message.chat.id
    state = user_states[chat_id]
    emoji = state.replace("введення_кількості_", "")
    кількість = message.text.strip()

    if not кількість.isdigit():
        bot.send_message(chat_id, "Введіть лише число.")
        return

    user_reports.setdefault(chat_id, {}).setdefault("готове", {})[emoji] = {"шматки": int(кількість)}
    user_states[chat_id] = f"вибір_дати_{emoji}"

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Сьогодні", callback_data=f"дата_{emoji}_2"),
        types.InlineKeyboardButton("Вчора", callback_data=f"дата_{emoji}_3"),
        types.InlineKeyboardButton("Позавчора", callback_data=f"дата_{emoji}_4")
    )
    bot.send_message(chat_id, "Коли був спечений цей пиріг?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("дата_"))
def save_pie_entry(call):
    chat_id = call.message.chat.id
    parts = call.data.split("_")
    emoji = parts[1]
    день = parts[2]
    user_reports[chat_id]["готове"][emoji]["день"] = день

    шматки = user_reports[chat_id]["готове"][emoji]["шматки"]
    звіт = f"{emoji} — {шматки}({день})"
    bot.send_message(chat_id, f"Збережено: {звіт}")

    show_main_menu(chat_id)

@bot.callback_query_handler(func=lambda call: call.data == "готове_пироги")
def show_pies_list(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = "вибір_пирога"

    markup = types.InlineKeyboardMarkup(row_width=2)

    # Мʼясні пироги
    bot.send_message(chat_id, "*Мʼясні пироги:*", parse_mode='Markdown')
    markup.add(
        types.InlineKeyboardButton("🍗🍅🧀 Курка-томати-сир", callback_data="пиріг_🍗🍅🧀"),
        types.InlineKeyboardButton("🍗🍍🧀 Курка-ананас-сир", callback_data="пиріг_🍗🍍🧀"),
        types.InlineKeyboardButton("🍗🍄🧀 Курка-гриби-сир", callback_data="пиріг_🍗🍄🧀"),
        types.InlineKeyboardButton("🐄🧀 Телятина-сир", callback_data="пиріг_🐄🧀"),
        types.InlineKeyboardButton("🦃🫑 Індик-солодкий перець", callback_data="пиріг_🦃🫑")
    )
    bot.send_message(chat_id, ".", parse_mode='Markdown')

    # Немʼясні пироги
    bot.send_message(chat_id, "*Немʼясні пироги:*", parse_mode='Markdown')
    markup.add(
        types.InlineKeyboardButton("🧅 Цибулевий", callback_data="пиріг_🧅"),
        types.InlineKeyboardButton("🍄🧀 Гриби-сир", callback_data="пиріг_🍄🧀"),
        types.InlineKeyboardButton("🧀🍃 Сир-шпинат", callback_data="пиріг_🧀🍃"),
        types.InlineKeyboardButton("🧀 Сім сирів", callback_data="пиріг_🧀")
    )
    bot.send_message(chat_id, ".", parse_mode='Markdown')

    # Солодкі пироги
    bot.send_message(chat_id, "*Солодкі пироги:*", parse_mode='Markdown')
    markup.add(
        types.InlineKeyboardButton("🍒🫐 Вишня-лохина", callback_data="пиріг_🍒🫐"),
        types.InlineKeyboardButton("🍒🧀 Вишня-сир", callback_data="пиріг_🍒🧀")
    )

    # Відступ + завершення
    bot.send_message(chat_id, " ", parse_mode='Markdown')
    markup.add(types.InlineKeyboardButton("🔚 З пирогами — все", callback_data="готове"))

    bot.send_message(chat_id, "Оберіть пиріг:", reply_markup=markup)
