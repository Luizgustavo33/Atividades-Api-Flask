# Importar a classe Flask, objeto request e o objeto jsonify:
from flask import Flask, request, jsonify
# Criar o objeto Flask app:
app = Flask(__name__)
produtos = [{'nome': 'sapato', 'preco': 128.55},
{'nome': 'camisa', 'preco': 49.89},
{'nome': 'calça', 'preco': 89.99},
{'nome': 'bermuda', 'preco': 78.63}]

# http://127.0.0.1:5000/produtos
@app.route('/produtos', methods=['GET'])
def retornar_todos_os_produtos():
    resp = produtos
    if 'X-nome-produto' in request.headers:
        nome = request.headers['X-nome-produto']
        for produto in produtos:
         if produto['nome'] == nome:
            resp = produto
    return jsonify(resp)

if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)