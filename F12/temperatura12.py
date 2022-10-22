# Importar a classe Flask e o objeto request:
from flask import Flask, request
# Criar o objeto Flask app:
app = Flask(__name__)

# http://127.0.0.1:5000/testes/1?celsius=10
@app.route('/testes/1')
def Testetemperatura():
  celsius = request.args.get('celsius')
  fahrenheit = (float(celsius) * 1.8) + 32
  return '''<h1>Temperatura em graus Celsius informada: {}</h1>
            <h1>Temperatura em Fahrenheit: {}</h1>'''.format(celsius, fahrenheit)

if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
  app.run(debug = True, port = 5000)
