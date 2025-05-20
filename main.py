from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# Отримуємо токен з середовища (Render дозволяє додати BOT_TOKEN окремо)
TOKEN = os.getenv("BOT_TOKEN")

# Головне меню
menu = [
    ["☑️ Інвентаризація", "❄️ Заморозка"],
    ["💰 Каса", "📚 Довідка"],
    ["📊 Аналітика"]
]
markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)

# Обробка команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот КІІТ. Обери дію з меню:", reply_markup=markup)

# Обробка повідомлень з меню
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "☑️ Інвентаризація":
        await update.message.reply_text("Тут буде інвентаризація.")
    elif text == "❄️ Заморозка":
        await update.message.reply_text("Тут буде заморозка.")
    elif text == "💰 Каса":
        await update.message.reply_text("Тут буде каса.")
    elif text == "📚 Довідка":
        await update.message.reply_text("Тут буде довідка.")
    elif text == "📊 Аналітика":
        await update.message.reply_text("Тут буде аналітика.")
    else:
        await update.message.reply_text("Не впізнаю цю команду. Обери з меню.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
