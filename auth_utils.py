from functools import wraps

from flask import session, redirect, url_for, flash

def login_required(funcao):

    @wraps(funcao)
    def verificar_login(*args, **kwargs):

        if "conta_id" not in session:

            flash(
                "Você precisa fazer login.",
                "error"
            )

            return redirect(
                url_for("auth.login")
            )

        return funcao(*args, **kwargs)

    return verificar_login