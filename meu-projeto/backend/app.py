from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

@app.route('/extrair', methods=['POST'])
def extrair():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"erro": "URL não fornecida"}), 400

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        titulo_tag = soup.find('h1')
        titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Título não encontrado"

        primeiro_paragrafo = next(
            (p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 100),
            "Parágrafo não encontrado"
        )

        return jsonify({
            "titulo": titulo,
            "paragrafo": primeiro_paragrafo
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run()
