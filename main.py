from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот КІІТ.")

app = ApplicationBuilder().token("ТВОЙ_ТОКЕН").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
