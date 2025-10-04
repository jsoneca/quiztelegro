import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from quiz_gemini import gerar_pergunta
from storage_supabase import update_points

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

async def enviar_quiz(context: ContextTypes.DEFAULT_TYPE):
    pergunta, opcoes, correta = gerar_pergunta()
    texto = f"🎬 *Quiz de Cinema e Cultura Pop!*\n\n{pergunta}\n"
    for i, opcao in enumerate(opcoes):
        texto += f"{chr(65+i)}) {opcao}\n"
    await context.bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou o bot de quizzes de cinema 🎥")
    await enviar_quiz(context)

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # JobQueue para enviar quiz a cada 45 minutos
    app.job_queue.run_repeating(enviar_quiz, interval=45*60, first=5)
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
