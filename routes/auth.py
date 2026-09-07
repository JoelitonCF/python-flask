from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from banco import inserir_conta, buscar_conta_por_email


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/criar-conta", methods=["GET", "POST"])
def criar_conta():

    if request.method == "POST":

        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        senha = request.form["senha"].strip()

        conta_existente = buscar_conta_por_email(email)

        if conta_existente:
            flash(
                "Este email já esta cadastrado",
                "error"
            )

            return redirect(url_for("auth.criar_conta"))

        senha_hash = generate_password_hash(senha)

        inserir_conta(nome, email, senha_hash)

        flash(
            "Conta criada com sucesso",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template("cadastrar_conta.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conta = buscar_conta_por_email(email)

        if conta is None:
            flash(
                "Email ou senha inválidos",
                "error"
            )

            return redirect(
                url_for("auth.login")
            )

        if not check_password_hash(
            conta["senha"], senha
        ):
            flash(
                "Email ou senha inválidos",
                "error"
            )

            return redirect(
                url_for("auth.login")
            )
        session["conta_id"] = conta["id"]
        session["conta_nome"] = conta["nome"]

        flash(
            "Login realizado com sucesso!",
            "success"
        )

        return redirect(
            url_for("usuarios.usuarios")
        )

    render_template("login.html")

auth_bp.route("/logout")
def logout():
    
    session.clear()
    
    flash(
        "Logout realizado com sucesso.",
        "success"
    )
    
    return redirect(
        url_for("auth.login")
    )