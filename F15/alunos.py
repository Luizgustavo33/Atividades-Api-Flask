from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)   
api = Api(app)

Alunos = [{'id': 0, 'nome': 'Ana', 'nota': 72.00},
{'id': 1, 'nome': 'Bruna', 'nota': 71.50},
{'id': 2, 'nome': 'Carlos','nota': 68.50},
{'id': 3, 'nome': 'Diego', 'nota': 70.0},
{'id': 4, 'nome': 'Ester', 'nota': 69.0}]

def aborta_se_o_aluno_não_existe(id):
    encontrei = False
    for aluno in Alunos:

        if aluno['id'] == int(id):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem="O aluno com a matrícula = {} não existe".format(id)) 
    #404:Not Found

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='Número da matrícula do aluno')
parser.add_argument('nome', type=str, help='Nome do aluno')
parser.add_argument('nota', type=float, help='Nota do aluno')

class Aluno(Resource):
    
    #http://127.0.0.1:5000/aluno/0
    def get(self, id):
        aborta_se_o_aluno_não_existe(id)
        return Alunos[int(id)]
    
    #http://127.0.0.1:5000/aluno/1
    def delete(self, id):
        aborta_se_o_aluno_não_existe(id)
        del Alunos[int(id)]
        return '', 204, #204: No Content
    
    #http://127.0.0.1:5000/aluno/1
    #{ "nome":"CARLINHOS","nota":99.9}
    def put(self, id):
        aborta_se_o_aluno_não_existe(id)
        args = parser.parse_args()
        for aluno in Alunos:
            if aluno['id'] == int(id):
                aluno['id'] == int(id)
                aluno['nome'] = args['nome']
                aluno['nota'] = args['nota']
                break
        return aluno, 200, #200: OK



class ListaAlunos(Resource):
    
    #http://127.0.0.1:5000/aluno
    def get(self):
        return Alunos
    
    
    #http://127.0.0.1:5000/aluno
    #{"nome":"Carla","nota":45.8}
    def post(self):
        args = parser.parse_args()
        id = -1
        for aluno in Alunos:
            if int(aluno['id']) > id:
                    id = int(aluno['id'])
        id = id + 1
        aluno = {'id': id, 'nome': args['nome'], 'nota': args['nota']}
        Alunos.append(aluno)
        return aluno, 201, #201: Created
##
## Roteamento de recursos:
##  
api.add_resource(Aluno, '/aluno/<id>')
api.add_resource(ListaAlunos, '/aluno')
if __name__ == '__main__':
    app.run(debug=True)