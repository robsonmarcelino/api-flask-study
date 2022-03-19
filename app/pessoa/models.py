from app import db

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

    def __repr__(self):
        return '<Pessoa %d>' % self.id             