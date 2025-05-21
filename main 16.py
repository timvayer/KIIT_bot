
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(BOT_TOKEN)

user_pie_data = {}

pie_labels = {
    "pie_курка_ананас": "🍗🍍 Курка-ананас",
    "pie_курка_гриби_сир": "🍗🍄🧀 Курка-гриби-сир",
    "pie_курка_томати_сир": "🍗🍅🧀 Курка-томати-сир",
    "pie_мясо_овочі": "🐄🧀 Мʼясо-овочі",
    "pie_індик_перець": "🦃🫑 Індик-перець",
    "pie_цибулевий": "🧅 Цибулевий",
    "pie_сир_шпинат": "🧀🍃 Сир-шпинат",
    "pie_сир_гриби": "🍄🧀 Сир-гриби",
    "pie_сім_сирів": "🧀 Сім сирів"
}

@bot.message_handler(commands=['start', 'звіт'])
def main_menu(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Звіт", callback_data="start_report"))
    bot.send_message(message.chat.id, "Обери опцію:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_report")
def report_categories(call):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Пироги", callback_data="category_pies"),
        InlineKeyboardButton("Пиріжки", callback_data="category_pyrizhky"),
        InlineKeyboardButton("Галети", callback_data="category_galety"),
        InlineKeyboardButton("Десерти", callback_data="category_deserty")
    )
    bot.edit_message_text("Що готове на завтра? Обери категорію:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "category_pies")
def show_pies(call):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("🍗🍍", callback_data="pie_курка_ананас"),
        InlineKeyboardButton("🍗🍄🧀", callback_data="pie_курка_гриби_сир"),
        InlineKeyboardButton("🍗🍅🧀", callback_data="pie_курка_томати_сир"),
        InlineKeyboardButton("🐄🧀", callback_data="pie_мясо_овочі"),
        InlineKeyboardButton("🦃🫑", callback_data="pie_індик_перець"),
        InlineKeyboardButton("🧅", callback_data="pie_цибулевий"),
        InlineKeyboardButton("🧀🍃", callback_data="pie_сир_шпинат"),
        InlineKeyboardButton("🍄🧀", callback_data="pie_сир_гриби"),
        InlineKeyboardButton("🧀", callback_data="pie_сім_сирів"),
    )
    markup.add(InlineKeyboardButton("Завершити", callback_data="finish_pies"))
    bot.edit_message_text("Обери пиріг, щоб ввести кількість шматків:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("pie_"))
def ask_quantity(call):
    pie_key = call.data
    chat_id = call.message.chat.id
    user_pie_data[chat_id] = user_pie_data.get(chat_id, {})
    user_pie_data[chat_id]["pending"] = pie_key
    bot.send_message(chat_id, f"Скільки шматків залишилось для «{pie_labels[pie_key]}»?")

@bot.message_handler(func=lambda message: message.chat.id in user_pie_data and "pending" in user_pie_data[message.chat.id])
def save_quantity(message):
    chat_id = message.chat.id
    pending_key = user_pie_data[chat_id]["pending"]
    try:
        amount = int(message.text)
        user_pie_data[chat_id][pending_key] = amount
        del user_pie_data[chat_id]["pending"]
        show_pies(message)
    except ValueError:
        bot.send_message(chat_id, "Будь ласка, введи число.")

@bot.callback_query_handler(func=lambda call: call.data == "finish_pies")
def finish_pie_block(call):
    chat_id = call.message.chat.id
    data = user_pie_data.get(chat_id, {})
    lines = []
    for key, value in data.items():
        if key != "pending":
            lines.append(f"{pie_labels.get(key, key)} — {value}")
    text = "🥧 *Готове:*
" + "\n".join(lines) if lines else "Жодного пирога не обрано."
    bot.send_message(chat_id, text, parse_mode="Markdown")

print("Бот запущено.")
bot.polling()
