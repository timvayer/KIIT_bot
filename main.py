
import telebot
from telebot import types
from handlers import report, gotove, state, pyrizhky, finalize

bot = telebot.TeleBot("YOUR_BOT_TOKEN")  # Замінити на реальний токен

# Старт
@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📍 Руська, 3", "📍 Лепкого, 6")
    bot.send_message(message.chat.id, "Оберіть локацію для звіту:", reply_markup=markup)
    state.user_state[message.chat.id] = {}

# Локація
@bot.message_handler(func=lambda message: message.text.startswith("📍"))
def select_location(message):
    loc = message.text.replace("📍 ", "")
    state.user_state[message.chat.id] = {"location": loc}
    report.start_report(message, bot)

# Завершення
@bot.message_handler(func=lambda message: message.text == "✅ Завершити звіт")
def finalize_handler(message):
    finalize.send_final_report(message, bot)

# Готове
@bot.callback_query_handler(func=lambda call: call.data == "готове")
def handle_gotove(call):
    gotove.handle_gotove(call, bot)

# Пиріжки
@bot.callback_query_handler(func=lambda call: call.data == "пиріжки")
def handle_pyrizhky(call):
    pyrizhky.handle_pyrizhky(call, bot)

# Пироги
@bot.callback_query_handler(func=lambda call: call.data == "пироги")
def handle_pirohy(call):
    gotove.handle_pirohy(call, bot)

# Галети
@bot.callback_query_handler(func=lambda call: call.data == "галети")
def handle_galety(call):
    gotove.handle_galety(call, bot)

# Команда /звіт
@bot.message_handler(commands=['звіт'])
def report_command(message):
    report.start_report(message, bot)

bot.polling(none_stop=True)
