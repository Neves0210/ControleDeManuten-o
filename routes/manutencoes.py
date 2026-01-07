from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date
from models import db
from models.manutencao import Manutencao
from models.quarto import Quarto
from models.item_manutencao import ItemManutencao

manutencoes_bp = Blueprint("manutencoes", __name__, url_prefix="/manutencoes")

# LISTAR
@manutencoes_bp.route("/")
def listar():
    manutencoes = Manutencao.query.all()

    for m in manutencoes:
        m.atualizar_status()
    db.session.commit()

    return render_template("manutencoes/list.html", manutencoes=manutencoes)

# NOVA MANUTENÇÃO
# NOVA MANUTENÇÃO (POR QUARTO)
@manutencoes_bp.route("/nova/<int:quarto_id>", methods=["GET", "POST"])
def nova_por_quarto(quarto_id):
    quarto = Quarto.query.get_or_404(quarto_id)
    itens = ItemManutencao.query.all()

    if request.method == "POST":
        item_id = request.form["item_id"]
        item = ItemManutencao.query.get_or_404(item_id)

        manutencao = Manutencao(
            quarto_id=quarto.id,
            item_id=item.id,
            proxima_manutencao=date.today()
        )

        manutencao.registrar_execucao(item.periodicidade_dias)

        db.session.add(manutencao)
        db.session.commit()

        return redirect(
            url_for("quartos.manutencoes_do_quarto", quarto_id=quarto.id)
        )

    return render_template(
        "manutencoes/form_por_quarto.html",
        quarto=quarto,
        itens=itens
    )

# EXECUTAR MANUTENÇÃO
@manutencoes_bp.route("/executar/<int:id>")
def executar(id):
    manutencao = Manutencao.query.get_or_404(id)
    quarto_id = manutencao.quarto_id

    item = manutencao.item
    manutencao.registrar_execucao(item.periodicidade_dias)

    db.session.commit()

    return redirect(
        url_for("quartos.manutencoes_do_quarto", quarto_id=quarto_id)
    )

# EXCLUIR
@manutencoes_bp.route("/excluir/<int:id>")
def excluir(id):
    manutencao = Manutencao.query.get_or_404(id)
    quarto_id = manutencao.quarto_id

    db.session.delete(manutencao)
    db.session.commit()

    return redirect(
        url_for("quartos.manutencoes_do_quarto", quarto_id=quarto_id)
    )
