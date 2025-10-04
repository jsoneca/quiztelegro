import google.generativeai as genai
import os
import random

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gerar_pergunta():
    prompt = """
    Gere uma pergunta curta e divertida de múltipla escolha sobre cultura geral.
    Retorne exatamente neste formato:
    Pergunta: ...
    Opções:
    A) ...
    B) ...
    C) ...
    D) ...
    Resposta correta: (A, B, C ou D)
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    texto = response.text.strip()

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
            correta = {"A":0,"B":1,"C":2,"D":3}[letra]
    if not pergunta or len(opcoes) < 4:
        pergunta = "Qual desses é um animal?"
        opcoes = ["Cadeira", "Carro", "Cachorro", "Pedra"]
        correta = 2
    indices = list(range(len(opcoes)))
    random.shuffle(indices)
    opcoes = [opcoes[i] for i in indices]
    correta = indices.index(correta)
    return pergunta, opcoes, correta
