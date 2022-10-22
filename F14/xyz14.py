# Importar a classe Flask e o objeto request:
from flask import Flask, request
# Criar o objeto Flask app:
app = Flask(__name__)
# http://127.0.0.1:5000/teste/1
# Aceita requisições com o método POST.
# O corpo da requisição deve conter um objeto JSON
# como o apresentado abaixo:
# 
@app.route('/teste/1', methods=['POST'])
def teste_json():
    objeto_json = request.get_json()
    # Verificar se o ojeto no formato JSON é NULL.
    if objeto_json is not None:
        if 'X' in objeto_json:
            X = objeto_json['X']
        if 'Y' in objeto_json:
            Y = objeto_json['Y']
        if 'Z' in objeto_json:
            Z = objeto_json['Z']


    X=int(X)
    Y=int(Y)
    Z=int(Z)

    if (abs(X-Y)<Z and Z<X+Y) and (abs(Y-Z)<X and X<Y+Z) and (abs(Z-X)<Y and Y<Z+X):
        
        triangulo = "Pode ser um triângulo"

    else:
        triangulo = "Não pode ser um triângulo"




    return '''

                <h1>Primeiro valor: {}</h1>
                <h1>Segundo valor: {}</h1>
                <h1>Terceiro valor: {}</h1>
                <h1>Resultado: {}</h1>

                '''.format(X, Y,Z, triangulo)

if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)