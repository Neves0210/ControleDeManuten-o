from app import app
from models import db
from models.cargo import Cargo

cargos_padrao = [
    ("Admin", "Administrador do sistema"),
    ("Supervisor", "Responsável pela equipe e controle das manutenções"),
    ("Manutencao", "Executa manutenções"),
    ("Recepcao", "Visualiza status dos quartos"),
    ("Visualizador", "Apenas visualização")
]

with app.app_context():
    for nome, descricao in cargos_padrao:
        cargo = Cargo.query.filter_by(nome=nome).first()

        if not cargo:
            cargo = Cargo(nome=nome, descricao=descricao)
            db.session.add(cargo)
            print(f"Cargo criado: {nome}")
        else:
            print(f"Cargo já existe: {nome}")

    db.session.commit()
