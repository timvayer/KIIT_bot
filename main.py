import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Дані
savory_pyrizhky = {
    "🥔": "Картопля",
    "🥔🍄": "Картопля-гриби",
    "🍄": "Гриби",
    "🥬": "Капуста",
    "🥬🥩": "Капуста-мʼясо",
    "🥩🥗": "Мʼясо-овочі"
}

sweet_pyrizhky = {
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

pies_with_meat = {
    "🍗🍅🧀": "Курка-томати-сир",
    "🍗🍄🧀": "Курка-гриби-сир",
    "🦃🫑": "Індик-солодкий перець"
}

pies_without_meat = {
    "🧅": "Цибулевий",
    "🧀🍄": "Сир-гриби",
    "🧀🥬": "Сир-шпинат",
    "🧀": "Сім сирів"
}

sweet_pies = {
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

# Памʼять
user_reports = {}
user_states = {}

# Команди
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/звіт"))
    bot.send_message(message.chat.id, "Привіт! Щоб почати звіт, натисни /звіт", reply_markup=markup)

@bot.message_handler(commands=["звіт"])
def start_report(message):
    chat_id = message.chat.id
    user_reports[chat_id] = []
    user_states[chat_id] = {"stage": "category"}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🥟 Пиріжки"),
        types.KeyboardButton("🥧 Пироги"),
        types.KeyboardButton("🍅 Галети"),
        types.KeyboardButton("🍰 Десерти")
    )
    bot.send_message(chat_id, "Оберіть категорію:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in user_states)
def handle_state(message):
    chat_id = message.chat.id
    state = user_states[chat_id]

    if state["stage"] == "category":
        text = message.text
        if text == "🥟 Пиріжки":
            state["stage"] = "sub_pyrizhky"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add("З мʼясом", "Без мʼяса", "Солодкі")
            bot.send_message(chat_id, "Оберіть підкатегорію:", reply_markup=markup)
        elif text == "🥧 Пироги":
            state["stage"] = "sub_pies"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add("З мʼясом", "Без мʼяса", "Солодкі")
            bot.send_message(chat_id, "Оберіть підкатегорію:", reply_markup=markup)
        elif text == "🍅 Галети":
            state["stage"] = "galettes"
            send_product_keyboard(chat_id, galettes)
        elif text == "🍰 Десерти":
            state["stage"] = "desserts"
            send_product_keyboard(chat_id, desserts)

    elif state["stage"] == "sub_pyrizhky":
        sub = message.text
        if sub == "З мʼясом":
            state["stage"] = "input"
            state["products"] = {k: v for k, v in savory_pyrizhky.items() if "мʼясо" in v or "овочі" in v}
        elif sub == "Без мʼяса":
            state["stage"] = "input"
            state["products"] = {k: v for k, v in savory_pyrizhky.items() if "мʼясо" not in v}
        elif sub == "Солодкі":
            state["stage"] = "input"
            state["products"] = sweet_pyrizhky
        send_product_keyboard(chat_id, state["products"])

    elif state["stage"] == "sub_pies":
        sub = message.text
        if sub == "З мʼясом":
            state["stage"] = "input"
            state["products"] = pies_with_meat
        elif sub == "Без мʼяса":
            state["stage"] = "input"
            state["products"] = pies_without_meat
        elif sub == "Солодкі":
            state["stage"] = "input"
            state["products"] = sweet_pies
        send_product_keyboard(chat_id, state["products"])

    elif state["stage"] == "input":
        emoji = message.text.strip()
        products = state.get("products", {})
        if emoji in products:
            state["current"] = emoji
            state["stage"] = "amount"
            bot.send_message(chat_id, f"Скільки залишилось з {emoji}?")
        else:
            bot.send_message(chat_id, "Оберіть виріб зі списку.")

    elif state["stage"] == "amount":
        try:
            qty = int(message.text.strip())
            emoji = state["current"]
            name = state["products"][emoji]
            user_reports[chat_id].append(f"{emoji} {name} — {qty} шт.")
            state["stage"] = "input"
            send_product_keyboard(chat_id, state["products"])
        except:
            bot.send_message(chat_id, "Введіть кількість як число.")

@bot.message_handler(commands=["готово"])
def finish_report(message):
    chat_id = message.chat.id
    entries = user_reports.get(chat_id, [])
    if not entries:
        bot.send_message(chat_id, "Нічого не збережено.")
        return
    result = "*Готове:*\n" + "\n".join(entries)
    bot.send_message(chat_id, result, parse_mode="Markdown")
    user_reports.pop(chat_id, None)
    user_states.pop(chat_id, None)

def send_product_keyboard(chat_id, items):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for emoji in items:
        markup.add(types.KeyboardButton(emoji))
    bot.send_message(chat_id, "Оберіть виріб:", reply_markup=markup)

bot.polling(none_stop=True)
