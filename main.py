from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from quiz_gemini import gerar_pergunta
from storage_supabase import salvar_usuario, atualizar_pontos
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    salvar_usuario(update.effective_user.id, update.effective_user.username)
    await update.message.reply_text("Oi! 🥳 Sou a Lorelay 🌟\nUse /quiz para começar!")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta, opcoes, correta = gerar_pergunta()
    atualizar_pontos(update.effective_user.id, 135)
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
