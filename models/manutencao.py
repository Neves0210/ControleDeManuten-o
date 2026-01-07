from . import db
from datetime import date, timedelta

class Manutencao(db.Model):
    __tablename__ = "manutencoes"

    id = db.Column(db.Integer, primary_key=True)

    quarto_id = db.Column(
        db.Integer,
        db.ForeignKey("quartos.id"),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("itens_manutencao.id"),
        nullable=False
    )

    ultima_manutencao = db.Column(db.Date, nullable=True)
    proxima_manutencao = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(20), default="Pendente")

    # 🔥 RELACIONAMENTOS (ESSENCIAL)
    item = db.relationship("ItemManutencao", backref="manutencoes")

    def atualizar_status(self):
        hoje = date.today()
        if self.proxima_manutencao < hoje:
            self.status = "Atrasado"
        elif self.proxima_manutencao == hoje:
            self.status = "Pendente"
        else:
            self.status = "OK"

    def registrar_execucao(self, periodicidade_dias):
        hoje = date.today()
        self.ultima_manutencao = hoje
        self.proxima_manutencao = hoje + timedelta(days=periodicidade_dias)
        self.atualizar_status()
