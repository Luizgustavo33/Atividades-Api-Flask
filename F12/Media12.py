# Importar a classe Flask e o objeto request:
from flask import Flask, request
# Criar o objeto Flask app:
app = Flask(__name__)

@app.route('/testes/1')
def TesteMedia():
  #http://127.0.0.1:5000/testes/1?Nota=5&Nota1=5&Nota2=5
  Nota = request.args.get('Nota' ) 
  Nota1 = request.args.get('Nota1' )
  Nota2 = request.args.get('Nota2' )
  total = (float(Nota) + float(Nota1) + float(Nota2)) / 3


  if (total >= 0 and total < 3):
      resultado = "Reprovado"
  elif (total >= 3 and total < 7):
      resultado="para o Exame"
  else:
      resultado="Aprovado"   
  return '''<h1>Média das suas notas: {}</h1>
            <h1>Resultado: {}</h1>'''.format(total, resultado)

if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
  app.run(debug = True, port = 5000)
