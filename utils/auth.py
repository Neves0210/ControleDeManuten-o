from functools import wraps
from flask import session, redirect, url_for, abort
from models.usuario import Usuario
from flask import session
from models.usuario import Usuario

def usuario_logado():
    if "usuario_id" in session:
        return Usuario.query.get(session["usuario_id"])
    return None

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def cargo_required(cargos_permitidos):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "usuario_id" not in session:
                return redirect(url_for("auth.login"))

            usuario = Usuario.query.get(session["usuario_id"])

            if not usuario or usuario.cargo.nome not in cargos_permitidos:
                abort(403)

            return f(*args, **kwargs)
        return decorated
    return decorator
