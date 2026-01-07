from . import db

class ItemManutencao(db.Model):
    __tablename__ = "itens_manutencao"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    periodicidade_dias = db.Column(db.Integer, nullable=False)
