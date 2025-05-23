import telebot
from telebot import types
import os

from handlers import gotove, pyrizhky, report, finalize, state

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Головне меню
@bot.message_handler(commands=['start', 'звіт'])
def handle_start(message):
    chat_id = message.chat.id

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🥧 Готове", callback_data="gotove"),
        types.InlineKeyboardButton("🧊 Заморозка", callback_data="zamorozka"),
        types.InlineKeyboardButton("🥛 Молоко", callback_data="moloko"),
        types.InlineKeyboardButton("💧 Напої", callback_data="napoyi"),
        types.InlineKeyboardButton("🧃 Соки", callback_data="soky"),
        types.InlineKeyboardButton("☕ Кава / Матча / Чаї", callback_data="kava"),
        types.InlineKeyboardButton("📦 Розхідники", callback_data="rozxidnyky"),
        types.InlineKeyboardButton("✅ Завершити звіт", callback_data="finalize"),
    )
    bot.send_message(chat_id, "З чого почнемо?", reply_markup=keyboard)

# Колбеки основного меню
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "gotove":
        gotove.start_gotove(bot, call.message)
    elif call.data == "pyrizhky":
        pyrizhky.start_pyrizhky(bot, call.message)
    elif call.data == "report":
        report.show_report(bot, call.message)
    elif call.data == "finalize":
        finalize.send_final_report(bot, call.message)
    else:
        bot.send_message(call.message.chat.id, "Ця функція ще в розробці.")

# Запуск бота
if __name__ == '__main__':
    print("KIIT_helper_bot is running...")
    bot.infinity_polling()
