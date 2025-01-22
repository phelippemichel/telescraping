import re
from telethon import TelegramClient
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Telegram
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient('anon', api_id, api_hash)

# Inicializar o Flask
app = Flask(__name__)

# Função para extrair emails de um texto
def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

# Função assíncrona para buscar mensagens no canal
async def scrape_message(channel, limit=100):
    emails = set()
    async for message in client.iter_messages(channel, limit):
        if message.text:
            emails.update(extract_emails(message.text))
    return sorted(emails)

# Rota principal da API
@app.route('/fetch_emails', methods=['POST'])
def fetch_emails():
    data = request.json
    if not data or 'channel_link' not in data or 'limit' not in data:
        return jsonify({'error': 'É necessário fornecer os campos "channel_link" e "limit"'}), 400
    
    channel_link = data['channel_link']
    limit = data.get('limit', 100)
    
    try:
        # Rodar o cliente Telethon no loop de eventos
        with client:
            emails = client.loop.run_until_complete(scrape_message(channel_link, limit))
        return jsonify({'emails': emails}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Iniciar o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
