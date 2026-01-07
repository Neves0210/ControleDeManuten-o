from flask import Flask, render_template, redirect, url_for
from config import *
from models import db

from models.andar import Andar
from models.quarto import Quarto
from models.manutencao import Manutencao


from routes.andares import andares_bp
from routes.quartos import quartos_bp
from routes.itens import itens_bp
from routes.manutencoes import manutencoes_bp

app = Flask(__name__)
app.config.from_object("config")

db.init_app(app)

with app.app_context():
    db.create_all()

# ROTAS PRINCIPAIS
@app.route("/")
def index():
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    andares = Andar.query.all()
    quartos_total = Quarto.query.count()
    manutencoes = Manutencao.query.all()

    total_ok = 0
    total_pendente = 0
    total_atrasado = 0

    for m in manutencoes:
        m.atualizar_status()
        if m.status == "OK":
            total_ok += 1
        elif m.status == "Pendente":
            total_pendente += 1
        elif m.status == "Atrasado":
            total_atrasado += 1

    # Atualiza status no banco
    from models import db
    db.session.commit()

    dados_andares = []

    for andar in andares:
        quartos = andar.quartos
        atrasadas = 0

        for q in quartos:
            for m in q.manutencoes:
                if m.status == "Atrasado":
                    atrasadas += 1

        dados_andares.append({
            "id": andar.id,
            "nome": andar.nome,
            "quartos": len(quartos),
            "atrasadas": atrasadas
        })

    return render_template(
        "dashboard.html",
        quartos_total=quartos_total,
        total_ok=total_ok,
        total_pendente=total_pendente,
        total_atrasado=total_atrasado,
        dados_andares=dados_andares
    )

# REGISTRO DOS BLUEPRINTS
app.register_blueprint(andares_bp)
app.register_blueprint(quartos_bp)
app.register_blueprint(itens_bp)
app.register_blueprint(manutencoes_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
