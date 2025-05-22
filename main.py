import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Категорії пирогів
pies_categories = {
    "З мʼясом": {
        "🍗🍅🧀": "Курка-томати-сир",
        "🍗🍄🧀": "Курка-гриби-сир",
        "🦃🫑": "Індик-солодкий перець",
        "🐄🧀": "Телятина-сир",
        "🍗🍍🧀": "Курка-ананас-сир",
    },
    "Без мʼяса": {
        "🧅": "Цибулевий",
        "🧀🍃": "Сир-шпинат",
        "🍄🧀": "Гриби-сир",
        "🧀": "Сім сирів",
    },
    "Солодкі": {
        "🍒🫐": "Вишня-лохина",
        "🍒🧀": "Вишня-сир",
    }
}

# Звіти користувачів
user_reports = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/звіт'), types.KeyboardButton('/готово'))
    bot.send_message(message.chat.id, "Вітаю! Натисніть /звіт, щоб почати звіт.", reply_markup=markup)

@bot.message_handler(commands=['звіт'])
def start_report(message):
    chat_id = message.chat.id
    user_reports[chat_id] = []
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🥧 Пироги", callback_data="категорія:Пироги"))
    markup.add(types.InlineKeyboardButton("🥟 Пиріжки", callback_data="категорія:Пиріжки"))
    markup.add(types.InlineKeyboardButton("🥧 Галети", callback_data="категорія:Галети"))
    markup.add(types.InlineKeyboardButton("🍰 Десерти", callback_data="категорія:Десерти"))
    markup.add(types.InlineKeyboardButton("Скасувати", callback_data="скасувати"))
    bot.send_message(chat_id, "Що саме звітуємо?", reply_markup=markup)

@bot.message_handler(commands=['готово'])
def finish_report(message):
    chat_id = message.chat.id
    entries = user_reports.get(chat_id, [])
    if entries:
        text = "Готове:\n" + "\n".join(entries)
    else:
        text = "Поки що нічого не збережено."
    bot.send_message(chat_id, text)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id

    if call.data == "категорія:Пироги":
        markup = types.InlineKeyboardMarkup()
        for subcat in pies_categories.keys():
            markup.add(types.InlineKeyboardButton(subcat, callback_data=f"пироги_кат:{subcat}"))
        markup.add(types.InlineKeyboardButton("↩ Назад до категорій", callback_data="повернутися"))
        bot.edit_message_text("Оберіть підкатегорію пирогів:", chat_id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("пироги_кат:"):
        subcat = call.data.split(":")[1]
        markup = types.InlineKeyboardMarkup(row_width=2)
        for emoji in pies_categories[subcat]:
            markup.add(types.InlineKeyboardButton(emoji, callback_data=f"пиріг:{emoji}:{subcat}"))
        markup.add(types.InlineKeyboardButton("↩ Назад до категорій", callback_data="категорія:Пироги"))
        bot.edit_message_text("Оберіть виріб:", chat_id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("пиріг:"):
        emoji, subcat = call.data.split(":")[1:]
        name = pies_categories[subcat][emoji]
        bot.send_message(chat_id, f"Скільки залишилось з {emoji}?")
        bot.register_next_step_handler_by_chat_id(chat_id, lambda msg: save_quantity(msg, emoji, name))

    elif call.data == "повернутися":
        start_report(call.message)

    elif call.data == "скасувати":
        bot.edit_message_text("Звіт скасовано.", chat_id, call.message.message_id)

def save_quantity(message, emoji, name):
    chat_id = message.chat.id
    qty = message.text.strip()
    if qty.isdigit():
        record = f"{emoji} {name} — {qty} шт."
        user_reports[chat_id].append(record)
        bot.send_message(chat_id, f"Записано: {record}")
    else:
        bot.send_message(chat_id, "Це не виглядає як число. Спробуйте ще раз.")
