from . import db

class Andar(db.Model):
    __tablename__ = "andares"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    quartos = db.relationship("Quarto", backref="andar", lazy=True)
