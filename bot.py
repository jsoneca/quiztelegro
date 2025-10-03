import os
from dotenv import load_dotenv
from telegram import Update, Poll
from telegram.ext import Application, CommandHandler, PollHandler, ContextTypes
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
client = OpenAI(api_key=os.getenv('XAI_API_KEY'), base_url="https://api.x.ai/v1")

scores = {}

class QuizQuestion(BaseModel):
    question: str = Field(description="Pergunta do quiz")
    options: List[str] = Field(description="4 opções de resposta")
    correct_answer: str = Field(description="Resposta correta")
    correct_index: int = Field(description="Índice da opção correta (0-3)")

class QuizSet(BaseModel):
    questions: List[QuizQuestion] = Field(description="Lista de perguntas")

async def generate_quiz_with_ai(topic: str, num_questions: int = 3):
    completion = client.beta.chat.completions.parse(
        model="grok-3",
        messages=[
            {"role": "system", "content": f"Gere {num_questions} perguntas de múltipla escolha sobre '{topic}', com 4 opções (A, B, C, D)."},
            {"role": "user", "content": f"Tópico: {topic}. Gere {num_questions} perguntas."}
        ],
        response_format=QuizSet,
    )
    quiz = completion.choices[0].message.parsed
    return {
        'questions': [
            {
                'question': q.question,
                'options': q.options,
                'correct_index': q.options.index(q.correct_answer)
            }
            for q in quiz.questions
        ]
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Envie /quiz para começar um quiz.')

async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quiz_data = await generate_quiz_with_ai("História do Brasil", 3)
    user_id = update.effective_user.id
    scores[user_id] = 0
    for i, q in enumerate(quiz_data['questions']):
        message = await context.bot.send_poll(
            chat_id=update.effective_chat.id,
            question=q['question'],
            options=q['options'],
            type=Poll.QUIZ,
            correct_option_id=q['correct_index'],
            is_anonymous=False,
            open_period=30
        )
        context.bot_data[message.poll.id] = {'user_id': user_id, 'question_num': i+1}

async def handle_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poll: Poll = update.poll
    user_id = context.bot_data.get(poll.id, {}).get('user_id')
    if not user_id:
        return
    user_answer = next((opt.text for opt in poll.options if opt.voter_count > 0), None)
    correct_option = poll.options[poll.correct_option_id].text
    is_correct = user_answer == correct_option
    if is_correct:
        scores[user_id] += 1
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Correto! +1 ponto 🎉")
    question_num = context.bot_data.get(poll.id, {}).get('question_num', 0)
    if question_num == 3:
        final_score = scores.get(user_id, 0)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Quiz finalizado! Pontuação: {final_score}/3. Use /quiz para outro!"
        )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(PollHandler(handle_poll))
    app.run_polling()

if __name__ == '__main__':
    main()
