from flask import Flask, request, jsonify
# Criar o objeto Flask app:
app = Flask(__name__)

@app.route('/camisas', methods=['POST'])
def total_das_compras( ):
    
    if 'P' in request.headers:
        P = int(request.headers['P'] )   
            
    if 'M' in request.headers:
        M = int(request.headers['M'])
            
    if 'G' in request.headers:
        G = int(request.headers['G'])    
        
    total= P*10 + M*12 + G*15
            
    return jsonify({'total': total })

if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)