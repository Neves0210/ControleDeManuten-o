from flask import Blueprint, render_template, request, redirect, url_for
from models import db
from models.quarto import Quarto
from models.andar import Andar
from models.manutencao import Manutencao

quartos_bp = Blueprint("quartos", __name__, url_prefix="/quartos")

# # READ
# @quartos_bp.route("/")
# def listar():
#     quartos = Quarto.query.all()
#     return render_template("quartos/list.html", quartos=quartos)


# CREATE
@quartos_bp.route("/novo/<int:andar_id>", methods=["GET", "POST"])
def novo_no_andar(andar_id):
    andar = Andar.query.get_or_404(andar_id)

    if request.method == "POST":
        numero = request.form["numero"]

        quarto = Quarto(
            numero=numero,
            andar_id=andar.id
        )

        db.session.add(quarto)
        db.session.commit()

        return redirect(
            url_for("andares.quartos_do_andar", andar_id=andar.id)
        )

    return render_template(
        "quartos/form.html",
        andar=andar
    )

# UPDATE
@quartos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    quarto = Quarto.query.get_or_404(id)
    andar_id = quarto.andar_id  # guarda o contexto

    if request.method == "POST":
        quarto.numero = request.form["numero"]
        db.session.commit()

        return redirect(
            url_for("andares.quartos_do_andar", andar_id=andar_id)
        )

    return render_template(
        "quartos/form.html",
        quarto=quarto,
        andar=quarto.andar
    )


# DELETE
@quartos_bp.route("/excluir/<int:id>")
def excluir(id):
    quarto = Quarto.query.get_or_404(id)
    andar_id = quarto.andar_id  # guarda antes de excluir

    db.session.delete(quarto)
    db.session.commit()

    return redirect(
        url_for("andares.quartos_do_andar", andar_id=andar_id)
    )


#Manutencao
@quartos_bp.route("/<int:quarto_id>/manutencoes")
def manutencoes_do_quarto(quarto_id):
    quarto = Quarto.query.get_or_404(quarto_id)
    manutencoes = Manutencao.query.filter_by(quarto_id=quarto.id).all()

    # Atualiza status automaticamente
    for m in manutencoes:
        m.atualizar_status()

    from models import db
    db.session.commit()

    return render_template(
        "manutencoes/por_quarto.html",
        quarto=quarto,
        manutencoes=manutencoes
    )
