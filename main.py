from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from quiz_gemini import gerar_pergunta
from storage_supabase import update_points, get_user
import asyncio, os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # ID do grupo ou usuário que receberá os quizzes

app = Application.builder().token(TOKEN).build()

async def enviar_quiz(context: CallbackContext):
    pergunta, opcoes, correta = gerar_pergunta()
    texto = f"🎬 *Quiz de Cinema e Cultura Pop!*\n\n{pergunta}\n"
    for i, opcao in enumerate(opcoes):
        texto += f"{chr(65+i)}) {opcao}\n"

    await context.bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode="Markdown")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Oi! 🥳 Sou a Lorelay 🌟\nUse /quiz para começar!")
    await enviar_quiz(context)

async def job_scheduler():
    app.job_queue.run_repeating(enviar_quiz, interval=45*60, first=5)

def main():
    app.add_handler(CommandHandler("start", start))
    app.job_queue.run_repeating(enviar_quiz, interval=45*60, first=5)
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
