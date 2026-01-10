from app import app
from models import db
from models.cargo import Cargo
from models.usuario import Usuario

with app.app_context():
    admin = Cargo.query.filter_by(nome="Admin").first()

    if not admin:
        admin = Cargo(nome="Admin", descricao="Administrador do sistema")
        db.session.add(admin)
        db.session.commit()
        print("Cargo Admin criado")
    else:
        print("Cargo Admin já existe")

    user = Usuario.query.filter_by(username="admin").first()

    if not user:
        user = Usuario(username="admin", cargo_id=admin.id)
        user.set_senha("admin123")
        db.session.add(user)
        db.session.commit()
        print("Usuário admin criado")
    else:
        print("Usuário admin já existe")
