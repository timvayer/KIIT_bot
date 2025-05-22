import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_state = {}
user_data = {}

# Дані
pyrizhky_savory = {
    "🥔": "Картопля",
    "🥔🍄": "Картопля-гриби",
    "🍄": "Гриби",
    "🥬": "Капуста",
    "🥬🥩": "Капуста-мʼясо",
    "🥩🥗": "Мʼясо-овочі"
}
pyrizhky_sweet = {
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
pies_meat = {
    "🍗🍅🧀": "Курка-томати-сир",
    "🍗🍄🧀": "Курка-гриби-сир",
    "🦃🫑": "Індик-солодкий перець"
}
pies_vege = {
    "🧅": "Цибулевий",
    "🧀🍄": "Сир-гриби",
    "🧀🍃": "Сир-шпинат",
    "🧀": "Сім сирів"
}
pies_sweet = {
    "🍒🫐": "Вишня-чорниця",
    "🍒🧀": "Вишня-сир"
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

# Команди
@bot.message_handler(commands=["start", "звіт"])
def start_report(message):
    cid = message.chat.id
    user_state[cid] = {"stage": "category"}
    user_data[cid] = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🥟 Пиріжки", "🥧 Пироги", "🍅 Галети", "🍰 Десерти")
    markup.add("/готово")
    bot.send_message(cid, "Що саме звітуємо?", reply_markup=markup)

@bot.message_handler(commands=["готово"])
def finish_report(message):
    cid = message.chat.id
    entries = user_data.get(cid, [])
    if not entries:
        bot.send_message(cid, "Поки що нічого не збережено.")
        return
    lines = [f"{e['emoji']} {e['name']} — {e['qty']} шт." for e in entries]
    bot.send_message(cid, "*Готове:*\n" + "\n".join(lines), parse_mode="Markdown")
    user_state.pop(cid, None)
    user_data.pop(cid, None)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    cid = message.chat.id
    text = message.text.strip()
    state = user_state.get(cid, {"stage": None})

    if text == "/готово":
        finish_report(message)
        return

    if state["stage"] == "category":
        if text == "🥟 Пиріжки":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Солоні", "Солодкі", "/готово")
            state["stage"] = "sub_pyrizhky"
            user_state[cid] = state
            bot.send_message(cid, "Оберіть підкатегорію пиріжків:", reply_markup=markup)

        elif text == "🥧 Пироги":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("З мʼясом", "Без мʼяса", "Солодкі", "/готово")
            state["stage"] = "sub_pies"
            user_state[cid] = state
            bot.send_message(cid, "Оберіть підкатегорію пирогів:", reply_markup=markup)

        elif text == "🍅 Галети":
            state["products"] = galettes
            state["stage"] = "choose_item"
            user_state[cid] = state
            send_product_keyboard(cid, galettes)

        elif text == "🍰 Десерти":
            state["products"] = desserts
            state["stage"] = "choose_item"
            user_state[cid] = state
            send_product_keyboard(cid, desserts)

    elif state["stage"] == "sub_pyrizhky":
        if text == "Солоні":
            state["products"] = pyrizhky_savory
        elif text == "Солодкі":
            state["products"] = pyrizhky_sweet
        else:
            return
        state["stage"] = "choose_item"
        user_state[cid] = state
        send_product_keyboard(cid, state["products"])

    elif state["stage"] == "sub_pies":
        if text == "З мʼясом":
            state["products"] = pies_meat
        elif text == "Без мʼяса":
            state["products"] = pies_vege
        elif text == "Солодкі":
            state["products"] = pies_sweet
        else:
            return
        state["stage"] = "choose_item"
        user_state[cid] = state
        send_product_keyboard(cid, state["products"])

    elif state["stage"] == "choose_item":
        if text in state.get("products", {}):
            state["current"] = text
            state["stage"] = "enter_qty"
            user_state[cid] = state
            bot.send_message(cid, f"Скільки залишилось з {text}?")

    elif state["stage"] == "enter_qty":
        if text.isdigit():
            qty = int(text)
            emoji = state["current"]
            name = state["products"].get(emoji, "Невідомо")
            user_data[cid].append({"emoji": emoji, "name": name, "qty": qty})
            state["stage"] = "choose_item"
            user_state[cid] = state
            send_product_keyboard(cid, state["products"])
        else:
            bot.send_message(cid, "Введіть кількість як число.")

def send_product_keyboard(chat_id, products):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(k) for k in products.keys()]
    for i in range(0, len(buttons), 2):
        markup.add(*buttons[i:i+2])
    markup.add("/готово")
    bot.send_message(chat_id, "Оберіть виріб:", reply_markup=markup)

bot.polling(none_stop=True)
