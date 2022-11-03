from flask import Flask, request, jsonify
# Criar o objeto Flask app:
app = Flask(__name__)

@app.route('/salario', methods=['POST'])
def salarios( ):
    
    if 'hora' in request.headers:
        hora = int(request.headers['hora'] )   
            
    if 'hora_extra' in request.headers:
        hora_extra = int(request.headers['hora_extra'])
            
    salario_b =  hora * 40 + hora_extra *50
    salario_l =  salario_b * 0.9
        
    
            
    return jsonify({'salario_bruto': salario_b, 'salario_liquido': salario_l  })

if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)