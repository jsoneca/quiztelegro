import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from quiz_gemini import gerar_pergunta
from storage_supabase import update_points

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")  # Pode ser o ID do grupo ou usuário

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

# Função principal (não precisa de asyncio.run)
def main():
    # Cria a aplicação do bot
    app = Application.builder().token(TOKEN).build()

    # Adiciona handlers
    app.add_handler(CommandHandler("start", start))

    # JobQueue: envia quiz a cada 45 minutos, primeiro quiz em 5 segundos
    app.job_queue.run_repeating(enviar_quiz, interval=45*60, first=5)

    # Inicia o polling (PTB 20.x já gerencia o loop)
    app.run_polling()

# Executa o bot
if __name__ == "__main__":
    main()
