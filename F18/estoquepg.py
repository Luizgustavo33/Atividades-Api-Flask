from flask import Flask
from flask_restful import reqparse, Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:adm@localhost:5432/F18'

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)

class ProdutoDataBase(db.Model):
    
    __tablename__ = "Produto_Estoque"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(256), unique=True, nullable=False)
    quantidade = db.Column(db.Integer,  nullable=False)
    preco = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    
    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        
    def create(self):
        db.session.add(self)
        db.session.commit()
        
        return self
    def __repr__(self):
        return f"{self.id, self.nome, self.quantidade, self.preco}"
    
class ProdutoDataBaseSchema(marshmallow.SQLAlchemyAutoSchema):
    
    class Meta:
        model = ProdutoDataBase
        sqla_session = db.session
    id = fields.Number()  # dump_only=True)
    nome = fields.String(required=True)
    quantidade = fields.Integer(required=True)
    preco = fields.Float(required=True)
api = Api(app)
# Parse dos dados enviados na requisição no formato JSON:
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='identificador do produto')
parser.add_argument('nome', type=str, help='nome do produto')
parser.add_argument('quantidade', type=int, help='quantidade de produtos')
parser.add_argument('preco', type=float, help='preço do produto')



# Produto:
# 1) Apresenta um único produto.
# 2) Remove um único produto.
# 3) Atualiza (substitui) um produto.


class Produto(Resource):
    def get(self, id):
        produto = ProdutoDataBase.query.get(id)
        produto_schema = ProdutoDataBaseSchema()
        resp = produto_schema.dump(produto)
        return {"produto": resp}, 200  # 200: Ok
    
    def delete(self, id):
        produto = ProdutoDataBase.query.get(id)
        db.session.delete(produto)
        db.session.commit()
        return '', 204  # 204: No Content
    
    def put(self, id):
        produto_json = parser.parse_args()
        produto = ProdutoDataBase.query.get(id)
        if produto_json.get('nome'):
            produto.nome = produto_json.nome
        if produto_json.get('quantidade'):
            produto.quantidade = produto_json.quantidade
        if produto_json.get('preco'):
            produto.preco = produto_json.preco
            
        db.session.add(produto)
        db.session.commit()
        
        produto_schema = ProdutoDataBaseSchema(only=['id', 'nome', 'quantidade', 'preco'])
        resp = produto_schema.dump(produto)
        
        return {"produto": resp}, 200  # 200: OK
    
    def patch(self, id):
        produto_json = parser.parse_args()
        produto = ProdutoDataBase.query.get(id)
        
        if produto_json.get('quantidade'):
            produto.quantidade = produto_json.quantidade
        if produto_json.get('preco'):
            produto.preco = produto_json.preco
            
        db.session.add(produto)
        db.session.commit()
        
        produto_schema = ProdutoDataBaseSchema(only=['id', 'nome', 'quantidade', 'preco'])
        resp = produto_schema.dump(produto)
        
        return {"produto": resp}, 200  # 200: OK
# ListaProduto:
# 1) Apresenta a lista de produtos.
# 2) Insere um novo produto.
class ListaProduto(Resource):
    def get(self):
        produtos = ProdutoDataBase.query.all()
        produto_schema = ProdutoDataBaseSchema(many=True)  # Converter objto Python para JSON.
        resp = produto_schema.dump(produtos)
        return {"produtos": resp}, 200  # 200: Ok
    
    def post(self):

        produto_json = parser.parse_args()
        produto_schema = ProdutoDataBaseSchema()
        produto = produto_schema.load(produto_json)
        produtoDataBase = ProdutoDataBase(produto['nome'], produto['quantidade'], produto['preco'])
        resp = produto_schema.dump(produtoDataBase.create())
        return {"produto": resp}, 201  # 201: 
    
class ListaEstoque(Resource):
    def get(self):
        estoque = []
        produtos = ProdutoDataBase.query.all()
        produto_schema = ProdutoDataBaseSchema(many=True)  
        for produto in produto_schema.dump(produtos):
            produto = {'id': produto['id'], 'nome': produto['nome'], 'quantidade' : produto['quantidade'],'preco':produto['preco'], 'total_estoque': produto['quantidade']*produto['preco']}
            estoque.append(produto)
        return {"Produtos_estoque":estoque}, 201, #201: Created
    
class Estoque(Resource):
    def get(self, id):
        estoque = []
        produto = ProdutoDataBase.query.get(id)
        produto_schema = ProdutoDataBaseSchema()
        resp = produto_schema.dump(produto)
        produto = {'id': resp['id'], 'nome': resp['nome'], 'quantidade' : resp['quantidade'],'preco':resp['preco'], 'total_estoque': resp['quantidade']*resp['preco']}
        estoque.append(produto)
        
        return estoque    
class EstoqueMaior(Resource):
    def get(self):
        estoque = []
        produtos = ProdutoDataBase.query.all()
        produto_schema = ProdutoDataBaseSchema(many=True)
        for produto in produto_schema.dump(produtos):
           
            produto =  float(produto['quantidade'])
            estoque.append(produto)
            
        maior = float()
        
        for i in estoque:
            if i > maior:
                maior = i
        for i in range(len(produto_schema.dump(produtos))):
            if maior == produto_schema.dump(produtos)[i]['quantidade']:
                maior = produto_schema.dump(produtos)[i]
            else:
                continue
        
        return maior
    
class EstoqueMenor(Resource):
    def get(self):
        estoque = []
        produtos = ProdutoDataBase.query.all()
        produto_schema = ProdutoDataBaseSchema(many=True)
        
        for produto in produto_schema.dump(produtos):
           
            produto =  int(produto['quantidade'])
            estoque.append(produto)
            
        menor = estoque[0]
        
        for i in estoque:
            if menor >= i:
                menor = i
        
        for i in range(len(produto_schema.dump(produtos))):
            if menor == produto_schema.dump(produtos)[i]['quantidade']:
                menor = produto_schema.dump(produtos)[i]
            else:
                continue
                
        return menor
class EstoqueTotal(Resource):
    def get(self):
        estoque = []
        produtos = ProdutoDataBase.query.all()
        produto_schema = ProdutoDataBaseSchema(many=True)
        for produto in produto_schema.dump(produtos):
           
            produto =  float(produto['quantidade']*produto['preco'])
            estoque.append(produto)
            
        total = 0
        for i in estoque:
            total = total + i
                
            
        total= {'valor_total_estoque': total}
        return total
    
class Venda(Resource):
 

    def patch(self, id):    
        produto_json = parser.parse_args()
        produto = ProdutoDataBase.query.get(id)
  
        if produto_json.get('quantidade'):
            produto.quantidade = produto.quantidade -produto_json.quantidade 
        
        db.session.add(produto)
        db.session.commit()
        
        produto_schema = ProdutoDataBaseSchema(only=['id', 'nome', 'quantidade', 'preco'])
        resp = produto_schema.dump(produto)
        
        return {"produto": resp}, 200  # 200: OK
        
class Compra(Resource):

    def patch(self, id):    
        produto_json = parser.parse_args()
        produto = ProdutoDataBase.query.get(id)
  
        if produto_json.get('quantidade'):
            produto.quantidade = produto.quantidade + produto_json.quantidade 
        
        db.session.add(produto)
        db.session.commit()
        
        produto_schema = ProdutoDataBaseSchema(only=['id', 'nome', 'quantidade', 'preco'])
        resp = produto_schema.dump(produto)
        
        return {"produto": resp}, 200  # 200: OK
    
# Roteamento de recursos:
##
api.add_resource(Produto, '/produtos/<id>')
api.add_resource(ListaProduto, '/produtos')
api.add_resource(ListaEstoque, '/estoque')
api.add_resource(Estoque, '/estoque/<id>')
api.add_resource(EstoqueMaior, '/estoque/maior')
api.add_resource(EstoqueMenor, '/estoque/menor')
api.add_resource(EstoqueTotal, '/estoque/total')
api.add_resource(Venda, '/venda/<id>')
api.add_resource(Compra, '/compra/<id>')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
