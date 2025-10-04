import google.generativeai as genai
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def gerar_pergunta():
    prompt = """
    Crie uma pergunta de quiz sobre Cinema ou Cultura Pop.
    Retorne no formato: pergunta, [opção1, opção2, opção3, opção4], letra da resposta correta
    """
    resposta = genai.chat.create(model="gemini-1.5-turbo", messages=[{"role": "user", "content": prompt}])
    # Exemplo fictício de parsing
    pergunta = "Qual filme ganhou o Oscar de Melhor Filme em 2022?"
    opcoes = ["Duna", "Não Olhe Para Cima", "Ataque dos Cães", "Belfast"]
    correta = "C"
    return pergunta, opcoes, correta
