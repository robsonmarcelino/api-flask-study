import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields
from app import db, app
from app.pessoa.models import Pessoa
 
pessoa = Blueprint('pessoa', __name__)

class PessoaSchema(Schema):
    id = fields.Int(dump_only=True)
    razao = fields.Str()
    fantasia = fields.Str()
    email = fields.Str()
    nascimento = fields.Str()
      
pessoa_schema = PessoaSchema()
pessoas_schema = PessoaSchema(many=True)
 
@pessoa.route('/')
@pessoa.route('/home')
def home():
    return "Seja Bem vindo a API."
 
class PessoaView(MethodView):
 
    def get(self, id=None, page=1):
        if not id:
            pessoa = Pessoa.query.paginate(page, 10).items
        else:
            pessoa = Pessoa.query.filter_by(id=id).first()
            if not pessoa:
                abort(404)

        result = pessoas_schema.dump(pessoa)
        return {"Pessoas": result}                
 
    def post(self):
        pessoa_razao = request.json['razao']
        pessoa_fantasia = request.json['fantasia']
        pessoa_email = request.json['email']
        pessoa_nascimento = request.json['nascimento']
        pessoa = Pessoa(pessoa_razao, pessoa_fantasia, pessoa_email, pessoa_nascimento)
        db.session.add(pessoa)
        db.session.commit()
        return pessoa_schema.dump(pessoa)
 
    def put(self, id):
        pessoa = Pessoa.query.get(id)
        pessoa.razao = request.json['razao']
        pessoa.fantasia = request.json['fantasia']
        pessoa.email = request.json['email']
        pessoa.nascimento = request.json['nascimento']
        db.session.commit()
        return pessoa_schema.dump(pessoa)
 
    def delete(self, id):
        pessoa = Pessoa.query.get(id)
        db.session.delete(pessoa)
        db.session.commit()
        return jsonify({"deleted": "success"})
 
 
pessoa_view =  PessoaView.as_view('pessoa_view')
app.add_url_rule(
    '/api/pessoa/', view_func=pessoa_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/api/pessoa/<int:id>', view_func=pessoa_view, methods=['GET', 'PUT', 'DELETE']
)