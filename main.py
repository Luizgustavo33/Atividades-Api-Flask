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
    return jsonify({'produtos': produtos})
# http://127.0.0.1:5000/produtos/camisa
@app.route('/produtos/<string:nome>', methods=['GET'])
def retornar_dados_do_produto_informado(nome):
    resp = {'produto': '', 'preco': None}
    for produto in produtos:
        if produto['nome'] == nome:
            resp = produto
    return jsonify(resp)
# http://127.0.0.1:5000/produtos/cinto/45.67
@app.route('/produtos/<string:nome>/<float:preco>', methods=['POST'])

def inserir_produto(nome, preco):
    produtos.append({'nome': nome, 'preco': preco})
    return jsonify({'nome': nome, 'preco': preco})
# http://127.0.0.1:5000/produtos/camisa/10.00
# http://127.0.0.1:5000/produtos/camisa/-10.00
@app.route('/produtos/<string:nome>/<float(signed=True):preco>',
methods=['PATCH'])
def alterar_preco_do_produto(nome, preco):
    resp = {'nome': '', 'preco': None}
    for produto in produtos:
        if produto['nome'] == nome: 
            produto['preco'] += preco
            resp = produto
    return jsonify(resp)
# http://127.0.0.1:5000/produtos/camisa
@app.route('/produtos/<string:nome>', methods=['DELETE'])
def remover_produto(nome):
    for i, produto in enumerate(produtos):
        if produto['nome'] == nome:
            del produtos[i]
    return jsonify({'produtos': produtos})
if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)