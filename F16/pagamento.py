from flask import Flask
from flask_restx import reqparse, abort, Api, Resource, fields
app = Flask(__name__)   
api = Api(app)

Funcionarios = [{'id': 0, 'nome': 'Ana','horas':8, 'valor': 45.78},
{'id': 1, 'nome': 'Bruna','horas':2, 'valor': 60.0},
{'id': 2, 'nome': 'Carlos','horas':10,'valor': 38.99},
{'id': 3, 'nome': 'Diego','horas':4, 'valor': 45.78},
{'id': 4, 'nome': 'Ester','horas':5, 'valor': 45.78}]

def aborta_se_o_funcionário_nao_existe(id):
    encontrei = False
    for funcionario in Funcionarios:

        if funcionario['id'] == int(id):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem="O funcionario com o  CPF = {} não existe".format(id)) 
    #404:Not Found

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='Número do CPF do funcionario')
parser.add_argument('nome', type=str, help='Nome do funcionario')
parser.add_argument('horas', type=float, help='Quantidade de horas trabalhadas')
parser.add_argument('valor', type=float, help='valor da hora do funcionario')

campos_obrigatorios_para_atualizacao = api.model('Atualizaçao de funcionários', {
  'id': fields.Integer(required=True, description='identificador do funcionários'),
  'nome': fields.String(required=True, description='nome do funcionários'),
  'horas': fields.Integer(required=True, description='quantidade de horas trabalhadas'),
  'valor': fields.Float(required=True, description='valor da hora de trabalho do funcionário'),
})
campos_obrigatorios_para_atualizacao_parcial = api.model('Atualizaçao de funcionários', {
  'horas': fields.Integer(required=True, description='quantidade de horas trabalhadas'),
  'valor': fields.Float(required=True, description='valor da hora de trabalho do funcionário'),
})
campos_obrigatorios_para_insercao = api.model('Inserção de funcionários', {
  'id': fields.Integer(required=False, readonly=True,
description='identificador do funcionários'),
  'nome': fields.String(required=True, description='nome do funcionários'),
  'horas': fields.Integer(required=True, description='quantidade de horas trabalhadas'),
  'valor': fields.Float(required=True, description='valor da hora de trabalho do funcionário'),
})

class funcionario(Resource):
    
 
    def get(self, id):
        aborta_se_o_funcionário_nao_existe(id)
        return Funcionarios[int(id)]
    
    def delete(self, id):
        aborta_se_o_funcionário_nao_existe(id)
        del Funcionarios[int(id)]
        return '', 204, #204: No Content
    

    
    @api.doc(responses={200: 'funcionário substituído'}) #200: OK
    @api.expect(campos_obrigatorios_para_atualizacao)
    def put(self, id):
        aborta_se_o_funcionário_nao_existe(id)
        args = parser.parse_args()
        for funcionario in Funcionarios:
            if funcionario['id'] == int(id):
                funcionario['id'] == int(id)
                funcionario['nome'] = args['nome']
                funcionario['horas'] = args['horas']
                funcionario['valor'] = args['valor']
                break
        return funcionario, 200, #200: OK
    
    @api.doc(responses={200: 'funcionário substituído'}) #200: OK
    @api.expect(campos_obrigatorios_para_atualizacao_parcial)
    def patch(self, id):
        aborta_se_o_funcionário_nao_existe(id)
        args = parser.parse_args()
        for funcionario in Funcionarios:
            if funcionario['id'] == int(id):
                funcionario['id'] == int(id)
                funcionario['horas'] = args['horas']
                funcionario['valor'] = args['valor']
                break
        return funcionario, 200, #200: OK



class ListaFuncionarios(Resource):
    
    #http://127.0.0.1:5000/funcionario
    def get(self):
        return Funcionarios
    
    
    #http://127.0.0.1:5000/funcionario
    #{"nome":"Carla","valor":45.8}
    @api.doc(responses={201: 'funcionário inserido'}) #201: Created
    @api.expect(campos_obrigatorios_para_insercao)  
    def post(self):
        args = parser.parse_args()
        id = -1
        for funcionario in Funcionarios:
            if int(funcionario['id']) > id:
                    id = int(funcionario['id'])
        id = id + 1
        funcionario = {'id': id, 'nome': args['nome'],  'horas': args['horas'], 'valor': args['valor']}
        Funcionarios.append(funcionario)
        return funcionario, 201, #201: Created
    
class ListaPagamentos(Resource):
    def get(self):
        pagamentos = []
        for funcionario in Funcionarios:
            funcionario = {'id': funcionario['id'], 'nome': funcionario['nome'],  'pagamento': funcionario['horas']*funcionario['valor']}
            pagamentos.append(funcionario)
        return pagamentos, 201, #201: Created
    
class pagamento(Resource):
    def get(self, id):
        aborta_se_o_funcionário_nao_existe(id)
        pagamentos = []
        funcionario =  Funcionarios[int(id)]
        funcionario1 = {'id': funcionario['id'], 'nome': funcionario['nome'],  'pagamento': funcionario['horas']*funcionario['valor']}
        pagamentos.append(funcionario1)
        
        return pagamentos, 
class PagamentoMaior(Resource):
    def get(self):
        pagamentos = []
        
        for funcionario in Funcionarios:
           
            funcionario =  float(funcionario['horas']*funcionario['valor'])
            pagamentos.append(funcionario)
            
        maior = float()
        
        for i in pagamentos:
            if i > maior:
                maior = i
        maior= {'maior_pagamento': maior}
        return maior
    
class PagamentoMenor(Resource):
    def get(self):
        pagamentos = []
        
        for funcionario in Funcionarios:
           
            funcionario =  float(funcionario['horas']*funcionario['valor'])
            pagamentos.append(funcionario)
            
        menor = pagamentos[0]
        
        for i in pagamentos:
            if menor >= i:
                menor = i
            
        menor= {'menor_pagamento': menor}
        return menor
class PagamentoTotal(Resource):
    def get(self):
        pagamentos = []
        
        for funcionario in Funcionarios:
           
            funcionario =  float(funcionario['horas']*funcionario['valor'])
            pagamentos.append(funcionario)
            
        total = 0
        for i in pagamentos:
            total = total + i
                
            
        total= {'pagamento_total': total}
        return total
    
##
## Roteamento de recursos:
##  
api.add_resource(funcionario, '/funcionario/<id>')
api.add_resource(ListaFuncionarios, '/funcionario')
api.add_resource(ListaPagamentos, '/pagamento')
api.add_resource(pagamento, '/pagamento/<id>')
api.add_resource(PagamentoMaior, '/pagamento/maior')
api.add_resource(PagamentoMenor, '/pagamento/menor')
api.add_resource(PagamentoTotal, '/pagamento/total')




if __name__ == '__main__':
    app.run(debug=True)