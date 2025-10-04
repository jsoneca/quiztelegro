import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import quiz_ai
from storage_supabase import get_user, update_points, get_ranking

TOKEN = os.environ.get("TELEGRAM_TOKEN")
QUIZ_CACHE = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bem-vindo ao QuizBot! Use /quiz para começar.")

async def quiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = quiz_ai.gerar_quiz()
    QUIZ_CACHE[update.effective_chat.id] = q
    botoes = [[InlineKeyboardButton(o, callback_data=o[0])] for o in q["opcoes"]]
    await update.message.reply_text(f"❓ {q['pergunta']}", reply_markup=InlineKeyboardMarkup(botoes))

async def resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    q = QUIZ_CACHE.pop(query.message.chat.id, None)
    if not q:
        await query.edit_message_text("Quiz expirado, use /quiz para novo.")
        return
    acerto = query.data == q["correta"]
    stats = update_points(query.from_user.id, acerto)
    msg = f"{'✅ Correto' if acerto else '❌ Errado'}! Pontos: {stats['pontos']} | Nível: {stats['nivel']}"
    await query.edit_message_text(msg)

async def perfil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = get_user(update.effective_user.id)
    await update.message.reply_text(f"Seu perfil — Pontos: {stats['pontos']} | Nível: {stats['nivel']}")

async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = get_ranking(10)
    lines = [f"{i+1}) {uid} — {pts} pts — Nível {niv}" for i, (uid, pts, niv) in enumerate(top)]
    await update.message.reply_text("🏅 Ranking:\n" + "\n".join(lines))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz_cmd))
    app.add_handler(CommandHandler("perfil", perfil))
    app.add_handler(CommandHandler("ranking", ranking))
    app.add_handler(CallbackQueryHandler(resposta))
    app.run_polling()

if __name__ == "__main__":
    main()
