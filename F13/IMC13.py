# Importar a classe Flask e o objeto request:
from flask import Flask, request
# Criar o objeto Flask app:
app = Flask(__name__)

@app.route('/testes/1',  methods=['GET', 'POST'])
def TesteIMC():
    #http://127.0.0.1:5000/testes/1
    if request.method == 'POST':
  
        Altura = request.form.get('Altura') 
        Peso = request.form.get('Peso')
        Altura = float(Altura)
        Peso = float(Peso)

        

        IMC = Peso/Altura**2


        if (IMC<18.5):
            resultado = "Abaixo do peso"
        elif (IMC >= 18.6 and IMC <= 24.9):
            resultado="Peso ideal, parabéns"
        elif (IMC >= 25 and IMC <= 29.9):
            resultado="Levemente acima do peso" 
        elif (IMC >= 30 and IMC <= 34.9):
            resultado="Obesidade grau 1" 
        elif (IMC >= 35 and IMC <= 39.9):
            resultado="Obesidade grau II (severa)"    
        else:
            resultado="Obesidade III (mórbida)" 

        return '''<h1>Cálculo do IMC: {}</h1>
                    <h1>Situação do indivíduo: {}</h1>'''.format(IMC, resultado)
    return '''

<form method="POST">
<div><label>Altura: <input type="float"

name="Altura"></label></div>


<div><label>Peso: <input type="float"

name="Peso"></label></div>
<input type="submit" value="Enviar">
</form>'''
if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
  app.run(debug = True, port = 5000) 
