from flask import Flask
from flask_restx import reqparse, abort, Api, Resource, fields
app = Flask(__name__)   
api = Api(app)

Produtos = [{'id': 0, 'nome': 'calca','quantidade':12, 'preco': 89.94},
{'id': 1, 'nome': 'camisa','quantidade':54, 'preco': 49.99},
{'id': 2, 'nome': 'saia','quantidade':33,'preco': 72.14},
{'id': 3, 'nome': 'sapato','quantidade':12, 'preco': 99.11},
{'id': 4, 'nome': 'vestido','quantidade':47, 'preco': 78.32}]

def aborta_se_o_produto_nao_existe(id):
    encontrei = False
    for produto in Produtos:

        if produto['id'] == int(id):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem="O produto com o código = {} não existe".format(id)) 
    #404:Not Found

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='Número do código do produto')
parser.add_argument('nome', type=str, help='Nome do produto')
parser.add_argument('quantidade', type=float, help='Quantidade de produtos ')
parser.add_argument('preco', type=float, help='preco do produto')
parser.add_argument('produtos_vendidos', type=int, help='quantidade de produtos vendidos')
parser.add_argument('produtos_comprados', type=int, help='quantidade de produtos comprados')



campos_obrigatorios_para_atualizacao = api.model('Atualizaçao dos produtos', {
  'id': fields.Integer(required=True, description='identificador dos produtos'),
  'nome': fields.String(required=True, description='nome do produto'),
  'quantidade': fields.Integer(required=True, description='quantidade de produtos'),
  'preco': fields.Float(required=True, description='preco do produto'),
})
campos_obrigatorios_para_atualizacao_parcial = api.model('Atualizaçao dos produtos', {
  'quantidade': fields.Integer(required=True, description='quantidade de produtos'),
  'preco': fields.Float(required=True, description='preco do produto'),
})
campos_obrigatorios_para_insercao = api.model('Inserção de produtos', {
  'id': fields.Integer(required=False, readonly=True,
description='identificador dos produtos'),
  'nome': fields.String(required=True, description='nome do produto'),
  'quantidade': fields.Integer(required=True, description='quantidade de produtos'),
  'preco': fields.Float(required=True, description='preco do produto'),
})
campos_obrigatorios_para_vendas_e_compras = api.model('Vendas de produtos', {
'produtos_vendidos': fields.Integer(required=True,
description='quantidade de produtos vendidos')
})

campos_obrigatorios_para_vendas_e_compras = api.model('Compra de produtos', {
'produtos_comprados': fields.Integer(required=True,
description='quantidade de produtos comprados')})

class produto(Resource):
    
 
    def get(self, id):
        aborta_se_o_produto_nao_existe(id)
        return Produtos[int(id)]
    
    def delete(self, id):
        aborta_se_o_produto_nao_existe(id)
        del Produtos[int(id)]
        return '', 204, #204: No Content
    

    
    @api.doc(responses={200: 'produto substituído'}) #200: OK
    @api.expect(campos_obrigatorios_para_atualizacao)
    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in Produtos:
            if produto['id'] == int(id):
                produto['id'] == int(id)
                produto['nome'] = args['nome']
                produto['quantidade'] = args['quantidade']
                produto['preco'] = args['preco']
                break
        return produto, 200, #200: OK
    
    @api.doc(responses={200: 'produto substituído'}) #200: OK
    @api.expect(campos_obrigatorios_para_atualizacao_parcial)
    def patch(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in Produtos:
            if produto['id'] == int(id):
                produto['quantidade'] = args['quantidade']
                produto['preco'] = args['preco']
                break
        return produto, 200, #200: OK



class ListaProdutos(Resource):
    
    #http://127.0.0.1:5000/produto
    def get(self):
        return Produtos
    
    
    #http://127.0.0.1:5000/produto
    #{"nome":"Carla","preco":45.8}
    @api.doc(responses={201: 'produto inserido'}) #201: Created
    @api.expect(campos_obrigatorios_para_insercao)  
    def post(self):
        args = parser.parse_args()
        id = -1
        for produto in Produtos:
            if int(produto['id']) > id:
                    id = int(produto['id'])
        id = id + 1
        produto = {'id': id, 'nome': args['nome'],  'quantidade': args['quantidade'], 'preco': args['preco']}
        Produtos.append(produto)
        return produto, 201, #201: Created
    
class ListaEstoque(Resource):
    def get(self):
        estoque = []
        for produto in Produtos:
            produto = {'id': produto['id'], 'nome': produto['nome'], 'quantidade' : produto['quantidade'],'preco':produto['preco'], 'total_estoque': produto['quantidade']*produto['preco']}
            estoque.append(produto)
        return estoque, 201, #201: Created
    
class Estoque(Resource):
    def get(self, id):
        aborta_se_o_produto_nao_existe(id)
        estoque = []
        produto =  Produtos[int(id)]
        produto1 = {'id': produto['id'], 'nome': produto['nome'], 'quantidade' : produto['quantidade'],'preco':produto['preco'], 'total_estoque': produto['quantidade']*produto['preco']}
        estoque.append(produto1)
        
        return estoque

class EstoqueMaior(Resource):
    def get(self):
        estoque = []
        
        for produto in Produtos:
           
            produto =  float(produto['quantidade'])
            estoque.append(produto)
            
        maior = float()
        
        for i in estoque:
            if i > maior:
                maior = i
        for i in range(len(Produtos)):
            if maior == Produtos[i]['quantidade']:
                maior = Produtos[i]
            else:
                continue
        
        return maior
    
class EstoqueMenor(Resource):
    def get(self):
        estoque = []
        
        for produto in Produtos:
           
            produto =  int(produto['quantidade'])
            estoque.append(produto)
            
        menor = estoque[0]
        
        for i in estoque:
            if menor >= i:
                menor = i
        
        for i in range(len(Produtos)):
            if menor == Produtos[i]['quantidade']:
                menor = Produtos[i]
            else:
                continue
                
            

        
        return menor
class EstoqueTotal(Resource):
    def get(self):
        estoque = []
        
        for produto in Produtos:
           
            produto =  float(produto['quantidade']*produto['preco'])
            estoque.append(produto)
            
        total = 0
        for i in estoque:
            total = total + i
                
            
        total= {'valor_total_estoque': total}
        return total
    
class Venda(Resource):
    @api.expect(campos_obrigatorios_para_vendas_e_compras)

    def patch(self, id):    
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in Produtos:
            if produto['id'] == int(id):
                produto['quantidade'] = int(produto['quantidade']-args['produtos_vendidos'])
                break
        return produto, 200, #200: OK
        
class Compra(Resource):
    @api.expect(campos_obrigatorios_para_vendas_e_compras)
    def patch(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in Produtos:
            if produto['id'] == int(id):
                produto['quantidade'] = int(produto['quantidade']+args['produtos_comprados'])
                break
        return produto, 200, #200: OK
      

    
##
## Roteamento de recursos:
##  
api.add_resource(produto, '/produto/<id>')
api.add_resource(ListaProdutos, '/produto')
api.add_resource(ListaEstoque, '/estoque')
api.add_resource(Estoque, '/estoque/<id>')
api.add_resource(EstoqueMaior, '/estoque/maior')
api.add_resource(EstoqueMenor, '/estoque/menor')
api.add_resource(EstoqueTotal, '/estoque/total')
api.add_resource(Venda, '/venda/<id>')
api.add_resource(Compra, '/compra/<id>')







if __name__ == '__main__':
    app.run(debug=True)