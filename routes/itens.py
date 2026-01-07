from flask import Blueprint, render_template, request, redirect, url_for
from models import db
from models.item_manutencao import ItemManutencao

itens_bp = Blueprint("itens", __name__, url_prefix="/itens")

# READ
@itens_bp.route("/")
def listar():
    itens = ItemManutencao.query.all()
    return render_template("itens/list.html", itens=itens)

# CREATE
@itens_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form["nome"]
        periodicidade = request.form["periodicidade"]

        db.session.add(
            ItemManutencao(
                nome=nome,
                periodicidade_dias=periodicidade
            )
        )
        db.session.commit()
        return redirect(url_for("itens.listar"))

    return render_template("itens/form.html")

# UPDATE
@itens_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    item = ItemManutencao.query.get_or_404(id)

    if request.method == "POST":
        item.nome = request.form["nome"]
        item.periodicidade_dias = request.form["periodicidade"]
        db.session.commit()
        return redirect(url_for("itens.listar"))

    return render_template("itens/form.html", item=item)

# DELETE
@itens_bp.route("/excluir/<int:id>")
def excluir(id):
    item = ItemManutencao.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("itens.listar"))
