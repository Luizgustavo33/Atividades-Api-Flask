# Importar a classe Flask e o objeto request:
from flask import Flask, request
# Criar o objeto Flask app:
app = Flask(__name__)
# http://127.0.0.1:5000/teste/1
# Aceita requisições com os métodos GET e POST.
# GET: gera um formulário em HTML para o usuário
# enviar dados para o servidor.
# POST: lê os dados enviados pelo usuário através
# do furmulário HTML.
@app.route('/teste/1', methods=['GET', 'POST'])
def TesteMMM():
# Trata a requisição com método POST:
    if request.method == 'POST':
        Nu1 = request.form.get('Nu1')
        Nu2 = request.form.get('Nu2')
        Nu3 = request.form.get('Nu3')

        Nu1= float(Nu1)
        Nu2= float(Nu2)
        Nu3= float(Nu3)

    
        if Nu1> Nu2 and Nu1> Nu3:
            maior=Nu1
        elif Nu2> Nu3:
            maior=Nu2
        else:
            maior=Nu3

        if Nu1< Nu2 and Nu1< Nu3:
            menor=Nu1
        elif  Nu2< Nu3:
            menor=Nu2
        else:
            menor=Nu3
        
        media =  (Nu1 + Nu2 + Nu3) / 3
        
        
    
        return '''

<h1>O maior número é: {}</h1>
<h1>O menor número é: {}</h1>

<h1>A média é: {}</h1>'''.format(maior, menor, media)

# Caso contrário, trata a requisição com método GET:
    return '''

<form method="POST">
<div><label>Nu1: <input type="float"

name="Nu1"></label></div>


<div><label>Nu2: <input type="float"

name="Nu2"></label></div>

<div><label>Nu3: <input type="float"

name="Nu3"></label></div>

<input type="submit" value="Enviar">
</form>'''
if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)