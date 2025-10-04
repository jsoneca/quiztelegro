import google.generativeai as genai
import os
import random

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gerar_pergunta():
    prompt = """
    Gere uma pergunta curta e divertida de múltipla escolha sobre CINEMA, SÉRIES ou CULTURA POP.
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

    pergunta = ""
    opcoes = []
    correta = 0

    for linha in texto.splitlines():
        linha = linha.strip()
        if linha.lower().startswith("pergunta"):
            pergunta = linha.split(":", 1)[1].strip()
        elif any(linha.startswith(x) for x in ["A)", "B)", "C)", "D)"]):
            opcoes.append(linha.split(")", 1)[1].strip())
        elif "resposta" in linha.lower():
            letra = linha.split(":")[1].strip().upper()[0]
            correta = {"A": 0, "B": 1, "C": 2, "D": 3}.get(letra, 0)

    if not pergunta or len(opcoes) < 4:
        pergunta = "Quem interpretou o Homem de Ferro nos filmes da Marvel?"
        opcoes = ["Chris Evans", "Robert Downey Jr.", "Tom Holland", "Mark Ruffalo"]
        correta = 1

    indices = list(range(len(opcoes)))
    random.shuffle(indices)
    opcoes = [opcoes[i] for i in indices]
    correta = indices.index(correta)
    return pergunta, opcoes, correta
