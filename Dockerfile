# Usa Python 3.11 (estável)
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Define variável de ambiente
ENV PYTHONUNBUFFERED=1

# Executa o bot
CMD ["python", "main.py"]
