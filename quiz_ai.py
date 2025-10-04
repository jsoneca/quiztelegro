import os
from openai import OpenAI
import random

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_pergunta():
    prompt = """
    Gere uma pergunta de múltipla escolha sobre cultura geral.
    Retorne no formato:
    Pergunta: ...
    Opções:
    A) ...
    B) ...
    C) ...
    D) ...
    Resposta correta: (A, B, C ou D)
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    texto = response.choices[0].message.content
    linhas = texto.splitlines()
    pergunta = ""
    opcoes = []
    correta = 0
    for linha in linhas:
        linha = linha.strip()
        if linha.lower().startswith("pergunta"):
            pergunta = linha.split(":", 1)[1].strip()
        elif any(linha.startswith(x) for x in ["A)", "B)", "C)", "D)"]):
            opcoes.append(linha.split(")", 1)[1].strip())
        elif "resposta correta" in linha.lower():
            letra = linha.split(":")[1].strip().upper()[0]
            correta = {"A": 0, "B": 1, "C": 2, "D": 3}[letra]
    if not pergunta or len(opcoes) < 4:
        pergunta = "Qual desses é um animal?"
        opcoes = ["Cadeira", "Carro", "Cachorro", "Pedra"]
        correta = 2
    indices = list(range(len(opcoes)))
    random.shuffle(indices)
    opcoes = [opcoes[i] for i in indices]
    correta = indices.index(correta)
    return pergunta, opcoes, correta
