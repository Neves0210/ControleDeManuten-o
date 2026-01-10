from flask import Blueprint, render_template, request, redirect, url_for, session
from models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and usuario.verificar_senha(senha):
            session["usuario_id"] = usuario.id
            return redirect(url_for("dashboard"))

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
