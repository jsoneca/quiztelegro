import os
import openai
openai.api_key = os.environ.get("OPENAI_API_KEY")

def gerar_quiz():
    prompt = "Crie uma pergunta de múltipla escolha simples com 4 opções (A-D) e indique a correta."
    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    texto = resp.choices[0].message.content.strip()

    # exemplo de retorno esperado (ajuste parsing conforme sua IA gera)
    return {
        "pergunta": "Qual é a capital da França?",
        "opcoes": ["A) Paris", "B) Londres", "C) Roma", "D) Berlim"],
        "correta": "A"
    }
