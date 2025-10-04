import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from quiz_gemini import gerar_pergunta
from storage_supabase import update_points

# Variáveis de ambiente
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")  # ID do grupo ou usuário

# Cria aplicação do Telegram
app = Application.builder().token(TOKEN).build()

# Função para enviar o quiz
async def enviar_quiz(context: ContextTypes.DEFAULT_TYPE):
    pergunta, opcoes, correta = gerar_pergunta()
    texto = f"🎬 *Quiz de Cinema e Cultura Pop!*\n\n{pergunta}\n"
    for i, opcao in enumerate(opcoes):
        texto += f"{chr(65+i)}) {opcao}\n"
    await context.bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode="Markdown")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou o bot de quizzes de cinema 🎥")
    await enviar_quiz(context)

# Scheduler para envio automático
async def job_scheduler():
    app.job_queue.run_repeating(enviar_quiz, interval=45*60, first=5)

def main():
    # Adiciona comando /start
    app.add_handler(CommandHandler("start", start))
    
    # Agenda envio automático a cada 45 minutos
    app.job_queue.run_repeating(enviar_quiz, interval=45*60, first=5)
    
    # Roda o bot
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
