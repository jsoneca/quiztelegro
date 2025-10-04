import google.generativeai as genai
import os
import random

# Configura o Gemini com a sua chave
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gerar_pergunta():
    prompt = """
    Gere uma pergunta curta e divertida de múltipla escolha sobre CINEMA, SÉRIES ou CULTURA POP.
    As perguntas devem ser sobre temas conhecidos, como filmes famosos, personagens, atores, trilhas sonoras ou prêmios.
    Evite perguntas muito difíceis ou específicas.
    Retorne exatamente neste formato:

    Pergunta: ...
    Opções:
    A) ...
    B) ...
    C) ...
    D) ...
    Resposta correta: (A, B, C ou D)
    """

    # Usa o modelo mais rápido e leve do Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    texto = response.text.strip()

    # Processa a resposta e extrai pergunta, opções e resposta correta
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
            correta = {"A": 0, "B": 1, "C": 2, "D": 3}.get(letra, 0)

    # Caso o modelo gere algo fora do formato
    if not pergunta or len(opcoes) < 4:
        pergunta = "Quem interpretou o Homem de Ferro nos filmes da Marvel?"
        opcoes = ["Chris Evans", "Robert Downey Jr.", "Tom Holland", "Mark Ruffalo"]
        correta = 1

    # Embaralha as opções sem perder a posição da correta
    indices = list(range(len(opcoes)))
    random.shuffle(indices)
    opcoes = [opcoes[i] for i in indices]
    correta = indices.index(correta)

    return pergunta, opcoes, correta
