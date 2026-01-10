from flask import Blueprint, render_template, request, redirect, url_for
from models.andar import Andar
from models.quarto import Quarto
from models import db
from utils.auth import login_required

andares_bp = Blueprint("andares", __name__, url_prefix="/andares")

@andares_bp.route("/")
@login_required
def listar():
    return render_template("andares/list.html", andares=Andar.query.all())

@andares_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    if request.method == "POST":
        db.session.add(Andar(nome=request.form["nome"]))
        db.session.commit()
        return redirect(url_for("andares.listar"))

    return render_template("andares/form.html")

@andares_bp.route("/excluir/<int:id>")
@login_required
def excluir(id):
    andar = Andar.query.get_or_404(id)
    db.session.delete(andar)
    db.session.commit()
    return redirect(url_for("andares.listar"))

@andares_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    andar = Andar.query.get_or_404(id)

    if request.method == "POST":
        andar.nome = request.form["nome"]
        db.session.commit()
        return redirect(url_for("andares.listar"))

    return render_template("andares/form.html", andar=andar)

@andares_bp.route("/<int:andar_id>/quartos")
@login_required
def quartos_do_andar(andar_id):
    andar = Andar.query.get_or_404(andar_id)
    quartos = Quarto.query.filter_by(andar_id=andar_id).all()

    return render_template(
        "quartos/list.html",
        andar=andar,
        quartos=quartos
    )