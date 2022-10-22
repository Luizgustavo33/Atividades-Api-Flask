from flask import Flask, request, jsonify
# Criar o objeto Flask app:
app = Flask(__name__)
comidas = [{'Codigo': '1', 'Produto': 'Cachorro quente', 'Preco': 12},
{'Codigo': '2', 'Produto': 'Sanduíche', 'Preco': 23.89},
{'Codigo': '3', 'Produto': 'Pastel', 'Preco': 3.98},
{'Codigo': '4', 'Produto': 'Refrigerante', 'Preco': 5.72},
{'Codigo': '5', 'Produto': 'Suco', 'Preco': 4.35}]

 #http://127.0.0.1:5000/comidas
@app.route('/comidas', methods=['GET'])
def retornar_todos_os_produtos():
    return jsonify({'comidas': comidas})

 #http://127.0.0.1:5000/comidas/5
@app.route('/comidas/<string:Codigo>', methods=['GET'])
def retornar_dados_do_produto_informado(Codigo):
    resp = {'Codigo': '', 'Produto': '', 'Preco': None}
    for comida in comidas:
        if comida['Codigo'] == Codigo:
            resp = comida
    return jsonify(resp)

#http://127.0.0.1:5000/comidas/6/Empada/5.45
@app.route('/comidas/<string:Codigo>/<string:Produto>/<float:Preco>', methods=['POST'])

def inserir_produto(Codigo, Produto, Preco):
    comidas.append({'Codigo': Codigo, 'Produto': Produto, 'Preco': Preco})
    return jsonify({'Codigo': Codigo, 'Produto': Produto, 'Preco': Preco})

# http://127.0.0.1:5000/comidas/4/Refrigerante/5.48
@app.route('/comidas/<string:Codigo>/<string:Produto>/<float(signed=True):Preco>', methods=['PATCH'])
def alterar_preco_do_produto(Codigo, Produto, Preco):
    resp = {'Codigo': '', 'Produto': '', 'Preco': None}
    for comida in comidas:
        if comida['Codigo'] == Codigo:
            if comida['Produto'] == Produto:
                comida['Preco'] += Preco


            resp = comida
    return jsonify(resp)

# http://127.0.0.1:5000/comidas/3/Coxinha/5.48
@app.route('/comidas/<string:Codigo>/<string:Produto>/<float(signed=True):Preco>', methods=['PUT'])
def alterar_dados_do_produto_totalmente(Codigo, Produto, Preco):
    resp = {'Codigo': '', 'Produto': '', 'PreCo': None}
    for comida in comidas:
        if comida['Codigo'] == Codigo:
            comida['Produto'] = Produto
            comida['Preco'] += Preco
            resp = comida
    return jsonify(resp)

#http://127.0.0.1:5000/comidas/5
@app.route('/comidas/<string:Codigo>', methods=['DELETE'])
def remover_produto(Codigo):
    for i, comida in enumerate(comidas):
        if comida['Codigo'] == Codigo:
            del comidas[i]
    return jsonify({'comidas': comidas})
if __name__ == '__main__':

    app.run(debug = True, port = 5000)


