import os
from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError, pre_load
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pessoa(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   razao = db.Column(db.String(150), nullable=False)
   fantasia = db.Column(db.String(150), nullable=False)
   email = db.Column(db.String(150), nullable=False)
   nascimento = db.Column(db.String(10), nullable=False)

   def __init__(self, razao, fantasia, email, nascimento):
      self.razao = razao
      self.fantasia = fantasia
      self.email = email
      self.nascimento = nascimento

class PessoaSchema(Schema):
    id = fields.Int(dump_only=True)
    razao = fields.Str()
    fantasia = fields.Str()
    email = fields.Str()
    nascimento = fields.Str()
      
pessoa_schema = PessoaSchema()
pessoas_schema = PessoaSchema(many=True)

@app.route('/api/pessoas')
def index():
   pessoas = Pessoa.query.all()
   result = pessoas_schema.dump(pessoas)
   return {"Pessoas": result}


@app.route('/api/pessoas/<id>')
def pessoa_pelo_id(id):
   pessoa = Pessoa.query.get(id)
   return pessoa_schema.dump(pessoa)

@app.route('/api/pessoas/inserir', methods=['POST'])
def new():
    pessoa_razao = request.json['razao']
    pessoa_fantasia = request.json['fantasia']
    pessoa_email = request.json['email']
    pessoa_nascimento = request.json['nascimento']
    pessoa = Pessoa(pessoa_razao, pessoa_fantasia, pessoa_email, pessoa_nascimento)
    db.session.add(pessoa)
    db.session.commit()
    return pessoa_schema.dump(pessoa)

@app.route('/api/pessoas/editar/<id>', methods=['POST'])
def edit(id):
   pessoa = Pessoa.query.get(id)
   pessoa.razao = request.json['razao']
   pessoa.fantasia = request.json['fantasia']
   pessoa.email = request.json['email']
   pessoa.nascimento = request.json['nascimento']
   db.session.commit()
   return pessoa_schema.dump(pessoa)

@app.route('/api/pessoas/deletar/<id>', methods=['POST'])
def delete(id):
   pessoa = Pessoa.query.get(id)
   db.session.delete(pessoa)
   db.session.commit()
   return jsonify({"deleted": "success"})

if __name__ == '__main__':
   db.create_all()
   port = int(os.environ.get("PORT", 5000))
   app.run(host='0.0.0.0', port=port, debug=True)    