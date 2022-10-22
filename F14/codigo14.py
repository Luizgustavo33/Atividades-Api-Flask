# Importar a classe Flask e o objeto request:
from flask import Flask, request
# Criar o objeto Flask app:
app = Flask(__name__)
# http://127.0.0.1:5000/teste/1
# Aceita requisições com o método POST.
# O corpo da requisição deve conter um objeto JSON
# como o apresentado abaixo:

#{"codigo":"1"}

@app.route('/teste/1', methods=['POST'])
def teste_json():
    objeto_json = request.get_json()
    # Verificar se o ojeto no formato JSON é NULL.
    if objeto_json is not None:
        if 'codigo' in objeto_json:
            codigo = objeto_json['codigo']

    if codigo == "1":

        Produto = "Sapato a R$ 99,99"
    elif codigo == "2":
        Produto="Bolsa a R$ 183,89"
    elif codigo == "3":
        Produto="Camisa a R$ 49,98"

    elif codigo == "4":
        Produto="Calça a R$ 89,72"

    elif codigo == "5":
        Produto="Blusa a R$ 97,35"

    else:
        Produto="Não existe esse produto no estoque"
    
    return '''

                <h1>Código selecionado: {}</h1>
                <h1>Retorno: {}</h1>
                

                '''.format(codigo, Produto)

if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)
        