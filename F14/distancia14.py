from flask import Flask, request, jsonify
# Criar o objeto Flask app:
app = Flask(__name__)
P =[]

# http://127.0.0.1:5000/P/5.0/5.0/5.0/9.0
@app.route('/P/<float:x1>/<float:y1>/<float:x2>/<float:y2>', methods=['POST'])
def Receber_Valores(x1, y1, x2, y2):

    d= pow((x2-x1)**2 + (y2-y1)**2,0.5)
    P.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2':y2, 'd':d})


  

    return  jsonify(P)



if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)