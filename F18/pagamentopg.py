from flask import Flask
from flask_restful import reqparse, Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:adm@localhost:5432/F18'

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)

class PessoaDataBase(db.Model):
    
    __tablename__ = "Folha_Pagamento"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(256), unique=True, nullable=False)
    horas = db.Column(db.Integer,  nullable=False)
    valor = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    
    def __init__(self, nome, horas, valor):
        self.nome = nome
        self.horas = horas
        self.valor = valor
        
    def create(self):
        db.session.add(self)
        db.session.commit()
        
        return self
    def __repr__(self):
        return f"{self.id, self.nome, self.horas, self.valor}"
    
class PessoaDataBaseSchema(marshmallow.SQLAlchemyAutoSchema):
    
    class Meta:
        model = PessoaDataBase
        sqla_session = db.session
    id = fields.Number()  # dump_only=True)
    nome = fields.String(required=True)
    horas = fields.Integer(required=True)
    valor = fields.Float(required=True)
api = Api(app)
# Parse dos dados enviados na requisição no formato JSON:
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='identificador a pessoa')
parser.add_argument('nome', type=str, help='nome da pessoa')
parser.add_argument('horas', type=int, help='horas trabalhadas')
parser.add_argument('valor', type=float, help='valor da hora trabalhada')


# Pessoa:
# 1) Apresenta um único pessoa.
# 2) Remove um único pessoa.
# 3) Atualiza (substitui) um pessoa.


class Pessoa(Resource):
    def get(self, id):
        pessoa = PessoaDataBase.query.get(id)
        pessoa_schema = PessoaDataBaseSchema()
        resp = pessoa_schema.dump(pessoa)
        return {"pessoa": resp}, 200  # 200: Ok
    
    def delete(self, id):
        pessoa = PessoaDataBase.query.get(id)
        db.session.delete(pessoa)
        db.session.commit()
        return '', 204  # 204: No Content
    
    def put(self, id):
        pessoa_json = parser.parse_args()
        pessoa = PessoaDataBase.query.get(id)
        if pessoa_json.get('nome'):
            pessoa.nome = pessoa_json.nome
        if pessoa_json.get('horas'):
            pessoa.horas = pessoa_json.horas
        if pessoa_json.get('valor'):
            pessoa.valor = pessoa_json.valor
            
        db.session.add(pessoa)
        db.session.commit()
        
        pessoa_schema = PessoaDataBaseSchema(only=['id', 'nome', 'horas', 'valor'])
        resp = pessoa_schema.dump(pessoa)
        
        return {"pessoa": resp}, 200  # 200: OK
    
    def patch(self, id):
        pessoa_json = parser.parse_args()
        pessoa = PessoaDataBase.query.get(id)
        
        if pessoa_json.get('horas'):
            pessoa.horas = pessoa_json.horas
        if pessoa_json.get('valor'):
            pessoa.valor = pessoa_json.valor
            
        db.session.add(pessoa)
        db.session.commit()
        
        pessoa_schema = PessoaDataBaseSchema(only=['id', 'nome', 'horas', 'valor'])
        resp = pessoa_schema.dump(pessoa)
        
        return {"pessoa": resp}, 200  # 200: OK
# ListaPessoa:
# 1) Apresenta a lista de pessoas.
# 2) Insere um novo pessoa.
class ListaPessoa(Resource):
    def get(self):
        pessoas = PessoaDataBase.query.all()
        pessoa_schema = PessoaDataBaseSchema(many=True)  # Converter objto Python para JSON.
        resp = pessoa_schema.dump(pessoas)
        return {"pessoas": resp}, 200  # 200: Ok
    
    def post(self):

        pessoa_json = parser.parse_args()
        pessoa_schema = PessoaDataBaseSchema()
        pessoa = pessoa_schema.load(pessoa_json)
        pessoaDataBase = PessoaDataBase(pessoa['nome'], pessoa['horas'], pessoa['valor'])
        resp = pessoa_schema.dump(pessoaDataBase.create())
        return {"pessoa": resp}, 201  # 201: 
    
class ListaPagamentos(Resource):
    def get(self):
        pagamento = []
        pessoas = PessoaDataBase.query.all()
        pessoa_schema = PessoaDataBaseSchema(many=True)  
        for pessoa in pessoa_schema.dump(pessoas):
            pessoa = {'id': pessoa['id'], 'nome': pessoa['nome'], 'horas' : pessoa['horas'],'valor':pessoa['valor'], 'total_pagamento': pessoa['horas']*pessoa['valor']}
            pagamento.append(pessoa)
        return {"Pessoas_pagamento":pagamento}, 201, #201: Created
    
class Pagamentos(Resource):
    def get(self, id):
        pagamento = []
        pessoa = PessoaDataBase.query.get(id)
        pessoa_schema = PessoaDataBaseSchema()
        resp = pessoa_schema.dump(pessoa)
        pessoa = {'id': resp['id'], 'nome': resp['nome'], 'horas' : resp['horas'],'valor':resp['valor'], 'total_pagamento': resp['horas']*resp['valor']}
        pagamento.append(pessoa)
        
        return pagamento    
class PagamentosMaior(Resource):
    def get(self):
        pagamento = []
        pessoas = PessoaDataBase.query.all()
        pessoa_schema = PessoaDataBaseSchema(many=True)
        for pessoa in pessoa_schema.dump(pessoas):
           
            pessoa =  float(pessoa['horas']*pessoa['valor'])
            pagamento.append(pessoa)
            
        maior = float()
        
        for i in pagamento:
            if i > maior:
                maior = i
      
        maior= {'maior_pagamento': maior}
        return maior
        
    
class PagamentosMenor(Resource):
    def get(self):
        pagamento = []
        pessoas = PessoaDataBase.query.all()
        pessoa_schema = PessoaDataBaseSchema(many=True)
        
        for pessoa in pessoa_schema.dump(pessoas):
           
            pessoa =  int(pessoa['horas']*pessoa['valor'])
            pagamento.append(pessoa)
            
        menor = pagamento[0]
        
        for i in pagamento:
            if menor >= i:
                menor = i
            
        menor= {'menor_pagamento': menor}
        return menor
        
        
class PagamentosTotal(Resource):
    def get(self):
        pagamento = []
        pessoas = PessoaDataBase.query.all()
        pessoa_schema = PessoaDataBaseSchema(many=True)
        for pessoa in pessoa_schema.dump(pessoas):
           
            pessoa =  float(pessoa['horas']*pessoa['valor'])
            pagamento.append(pessoa)
            
        total = 0
        for i in pagamento:
            total = total + i
                
            
        total= {'valor_total_pagamento': total}
        return total
    

    
# Roteamento de recursos:
##
api.add_resource(Pessoa, '/pessoas/<id>')
api.add_resource(ListaPessoa, '/pessoas')
api.add_resource(ListaPagamentos, '/pagamento')
api.add_resource(Pagamentos, '/pagamento/<id>')
api.add_resource(PagamentosMaior, '/pagamento/maior')
api.add_resource(PagamentosMenor, '/pagamento/menor')
api.add_resource(PagamentosTotal, '/pagamento/total')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
