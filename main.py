from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from storage_supabase import salvar_usuario, atualizar_pontos, obter_usuario
from quiz_ai import gerar_pergunta
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Bem-vindo ao Quiz Bot.")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta, opcoes, correta = gerar_pergunta()
    salvar_usuario(update.effective_user.id, update.effective_user.username)
    await update.message.reply_poll(
        question=pergunta,
        options=opcoes,
        type="quiz",
        correct_option_id=correta,
        is_anonymous=False
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.run_polling()

if __name__ == "__main__":
    main()
