from flask import Blueprint, render_template, request, redirect, url_for
from models import db
from models.usuario import Usuario
from models.cargo import Cargo
from utils.auth import cargo_required

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.route("/")
@cargo_required(["Admin"])
def listar():
    usuarios = Usuario.query.all()
    return render_template("usuarios/list.html", usuarios=usuarios)


@usuarios_bp.route("/novo", methods=["GET", "POST"])
@cargo_required(["Admin"])
def novo():
    cargos = Cargo.query.all()

    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]
        cargo_id = request.form["cargo_id"]

        usuario = Usuario(username=username, cargo_id=cargo_id)
        usuario.set_senha(senha)

        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for("usuarios.listar"))

    return render_template("usuarios/form.html", cargos=cargos)


@usuarios_bp.route("/excluir/<int:id>")
@cargo_required(["Admin"])
def excluir(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.username == "admin":
        return redirect(url_for("usuarios.listar"))

    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("usuarios.listar"))
