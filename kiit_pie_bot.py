import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(BOT_TOKEN)

# Головне меню
@bot.message_handler(commands=['start', 'звіт'])
def main_menu(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Звіт", callback_data="start_report"))
    bot.send_message(message.chat.id, "Обери опцію:", reply_markup=markup)

# Обробка вибору "Звіт"
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

# Обробка вибору "Пироги"
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
        InlineKeyboardButton("🧀", callback_data="pie_сім_сирів")
    )
    bot.edit_message_text("Обери пиріг, щоб ввести кількість шматків:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# Заглушка для введення кількості
@bot.callback_query_handler(func=lambda call: call.data.startswith("pie_"))
def enter_quantity(call):
    pie_name = call.data.replace("pie_", "").replace("_", " ").capitalize()
    bot.send_message(call.message.chat.id, f"Скільки шматків залишилось для «{pie_name}»? Напиши відповідь числом.")

print("Бот запущено.")
bot.polling()