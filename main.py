import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # ex: https://seusite.com/bot

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot iniciado!")

async def enviar_quiz(context: ContextTypes.DEFAULT_TYPE):
    chat_id = os.environ.get("CHAT_ID")  # ID do grupo ou chat
    await context.bot.send_message(chat_id, "Hora do quiz!")

if __name__ == "__main__":
    # Cria a aplicação do bot
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))

    # Jobs programados
    app.job_queue.run_repeating(enviar_quiz, interval=45*60, first=5)  # quiz a cada 45 min

    # Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),  # Porta do servidor
        webhook_url=WEBHOOK_URL,
    )
