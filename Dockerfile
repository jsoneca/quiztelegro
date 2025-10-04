# Usa Python 3.11
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta padrão (não é essencial pro bot, mas evita warnings)
EXPOSE 8000

# Comando para iniciar o bot
CMD ["python", "main.py"]
