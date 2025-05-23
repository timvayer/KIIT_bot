from .state import bot, user_states, user_reports
from telebot import types
from .gotove import show_main_menu

def start_report(message):
    chat_id = message.chat.id
    user_reports[chat_id] = {}
    show_main_menu(chat_id)
