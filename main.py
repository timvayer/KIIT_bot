import telebot
from telebot import types
from handlers import gotove, pyrizhky, finalize, state, report

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

@bot.message_handler(commands=['start', 'звіт'])
def start(message):
    report.start_report(message)

@bot.callback_query_handler(func=lambda call: call.data == "готове")
def handle_gotove(call):
    gotove.show_gotove_menu(call)

@bot.callback_query_handler(func=lambda call: call.data == "готове_pies")
def handle_pies(call):
    gotove.show_pies_list(call)

@bot.callback_query_handler(func=lambda call: call.data == "готове_pyrizhky")
def handle_pyrizhky(call):
    pyrizhky.show_pyrizhky_menu(call)

@bot.callback_query_handler(func=lambda call: call.data == "завершити")
def handle_finalize(call):
    finalize.complete_report(call)

print("Бот запущено")
bot.infinity_polling()
