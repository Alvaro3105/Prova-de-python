from database import db


class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    responsavel = db.Column(db.String(100), nullable=False)
    departamento = db.Column(db.String(80), nullable=False)
    orcamento = db.Column(db.Float, nullable=False)
    concluido = db.Column(db.Boolean, default=False)
