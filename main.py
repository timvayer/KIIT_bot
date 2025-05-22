import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

pies = {
    "З мʼясом": {
        "🍗🍅🧀": "Курка-томати-сир",
        "🍗🍄🧀": "Курка-гриби-сир",
        "🦃🫑": "Індик-солодкий перець",
        "🐄🧀": "Телятина-сир",
        "🍗🍄🧀": "Курка-гриби-сир"
    },
    "Без мʼяса": {
        "🧅": "Цибулевий",
        "🧀🍄": "Гриби-сир",
        "🧀🍃": "Сир-шпинат",
        "🧀": "Сім сирів"
    },
    "Солодкі": {
        "🍒🫐": "Вишня-лохина",
        "🍒🧀": "Вишня-сир"
    }
}

pyrizhky = {
    "Солоні": {
        "🥔": "Картопля",
        "🥔🍄": "Картопля-гриби",
        "🍄": "Гриби",
        "🥬": "Капуста",
        "🥬🥩": "Капуста-мʼясо",
        "🥩🥗": "Мʼясо-овочі"
    },
    "Солодкі": {
        "🍒": "Вишня",
        "🍒🍫": "Вишня-шоколад",
        "🍒🌼": "Вишня-мак",
        "🍐": "Груша",
        "Слива": "Слива",
        "Абрикос": "Абрикос",
        "Вишня-крем": "Вишня-крем",
        "Мак-крем": "Мак-крем",
        "Яблуко-кориця": "Яблуко-кориця"
    }
}

galettes = {
    "🥧🍏": "Яблуко-кориця",
    "🥧🍅": "Томати-сир"
}

desserts = {
    "🍰": "Торт Наполеон",
    "🍯": "Пахлава",
    "🥜": "Горішки"
}

@bot.message_handler(commands=["start", "звіт"])
def start_report(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"report": {}, "step": "category"}
    markup = types.InlineKeyboardMarkup()
    for text in ["🥧 Пироги", "🥟 Пиріжки", "🥧 Галети", "🍰 Десерти"]:
        markup.add(types.InlineKeyboardButton(text, callback_data=text))
    markup.add(types.InlineKeyboardButton("Скасувати", callback_data="cancel"))
    bot.send_message(chat_id, "Що саме звітуємо?", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    data = call.data

    if chat_id not in user_data:
        return

    state = user_data[chat_id]

    if data == "Скасувати":
        bot.send_message(chat_id, "Скасовано.")
        user_data.pop(chat_id)
        return

    if state["step"] == "category":
        if "Пироги" in data:
            state["step"] = "pie_sub"
            markup = types.InlineKeyboardMarkup()
            for cat in pies.keys():
                markup.add(types.InlineKeyboardButton(cat, callback_data=cat))
            markup.add(types.InlineKeyboardButton("↩ Назад", callback_data="back"))
            bot.edit_message_text("Оберіть підкатегорію пирогів:", chat_id, call.message.message_id, reply_markup=markup)

        elif "Пиріжки" in data:
            state["step"] = "pyrizhky_sub"
            markup = types.InlineKeyboardMarkup()
            for cat in pyrizhky.keys():
                markup.add(types.InlineKeyboardButton(cat, callback_data=cat))
            markup.add(types.InlineKeyboardButton("↩ Назад", callback_data="back"))
            bot.edit_message_text("Оберіть підкатегорію пиріжків:", chat_id, call.message.message_id, reply_markup=markup)

        elif "Галети" in data:
            state["step"] = "choose_galette"
            markup = types.InlineKeyboardMarkup()
            for e in galettes:
                markup.add(types.InlineKeyboardButton(e, callback_data=e))
            markup.add(types.InlineKeyboardButton("↩ Назад", callback_data="back"))
            bot.edit_message_text("Оберіть виріб:", chat_id, call.message.message_id, reply_markup=markup)

        elif "Десерти" in data:
            state["step"] = "choose_dessert"
            markup = types.InlineKeyboardMarkup()
            for e in desserts:
                markup.add(types.InlineKeyboardButton(e, callback_data=e))
            markup.add(types.InlineKeyboardButton("↩ Назад", callback_data="back"))
            bot.edit_message_text("Оберіть виріб:", chat_id, call.message.message_id, reply_markup=markup)

    elif data == "back":
        start_report(call.message)
        return

    elif state["step"] == "pie_sub" and data in pies:
        state["step"] = "choose_pie"
        state["current_list"] = pies[data]
        show_item_buttons(chat_id, state["current_list"])

    elif state["step"] == "pyrizhky_sub" and data in pyrizhky:
        state["step"] = "choose_pyrizhok"
        state["current_list"] = pyrizhky[data]
        show_item_buttons(chat_id, state["current_list"])

    elif state["step"] in ["choose_pie", "choose_pyrizhok", "choose_galette", "choose_dessert"]:
        if data in state["current_list"]:
            state["pending"] = data
            bot.send_message(chat_id, f"Скільки залишилось з {data}?")

@bot.message_handler(func=lambda m: m.text == "/готово")
def finish_report(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        report = user_data[chat_id].get("report", {})
        if not report:
            bot.send_message(chat_id, "Поки що нічого не збережено.")
        else:
            summary = "\n".join([f"{k} {v}" for k, v in report.items()])
            bot.send_message(chat_id, f"Готове:\n{summary}")
        user_data.pop(chat_id)

@bot.message_handler(func=lambda m: True)
def handle_amount(message):
    chat_id = message.chat.id
    if chat_id in user_data and "pending" in user_data[chat_id]:
        try:
            amount = int(message.text)
            emoji = user_data[chat_id]["pending"]
            name = user_data[chat_id]["current_list"][emoji]
            user_data[chat_id]["report"][f"{emoji} {name}"] = f"{amount} шт."
            del user_data[chat_id]["pending"]
            show_item_buttons(chat_id, user_data[chat_id]["current_list"])
        except:
            bot.send_message(chat_id, "Будь ласка, введіть число.")

def show_item_buttons(chat_id, item_dict):
    markup = types.InlineKeyboardMarkup()
    for k in item_dict:
        markup.add(types.InlineKeyboardButton(k, callback_data=k))
    markup.add(types.InlineKeyboardButton("↩ Назад", callback_data="back"))
    bot.send_message(chat_id, "Оберіть виріб:", reply_markup=markup)

bot.polling()
