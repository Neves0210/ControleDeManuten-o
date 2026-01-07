from . import db

class Quarto(db.Model):
    __tablename__ = "quartos"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default="OK")

    andar_id = db.Column(db.Integer, db.ForeignKey("andares.id"), nullable=False)

    manutencoes = db.relationship(
        "Manutencao",
        backref="quarto",
        lazy=True,
        cascade="all, delete"
    )
