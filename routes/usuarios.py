from flask import Blueprint, render_template, request, redirect, url_for, flash
from banco import listar_usuarios, inserir_usuario, excluir_usuario, atualizar_usuario, buscar_usuario, buscar_por_email
from auth_utils import login_required
from flask import abort

usuarios_bp = Blueprint(
    "usuarios",
    __name__,
    url_prefix="/usuarios"
)


@usuarios_bp.route("/usuarios")
@login_required
def usuarios():

    lista = listar_usuarios()

    return render_template('usuarios.html', usuarios=lista)


@usuarios_bp.route("/cadastro", methods=["GET", "POST"])
@login_required
def cadastro():
    mensagem = None

    if request.method == "POST":

        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        idade = request.form["idade"].strip()
        cidade = request.form["cidade"].strip()

        if not nome or not email or not idade or not cidade:
            mensagem = "Preencha todos os campos"

        elif "@" not in email:
            mensagem = "Email inválido"

        elif not idade.isdigit():
            mensagem = "A idade deve ser em número"

        elif buscar_por_email(email):
            mensagem = "Este email já esta cadastrado"

        else:
            idade = int(idade)

            if idade < 0:
                mensagem = "A idade deve ser menor que zero"
            else:

                sucesso = inserir_usuario(
                    nome, email, idade, cidade
                )
                
                if sucesso:
                    
                    flash("Usuário cadastrado com sucesso!", "success")

                    return redirect(
                        url_for("usuarios.usuarios")
                    )
                else:
                    flash("Não foi possivel cadastrar o usuário.", "error")
                    

    return render_template("cadastro.html", mensagem=mensagem)


@usuarios_bp.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir(id):

    excluir_usuario(id)

    flash("Usuário excluído com sucesso!", "success")

    return redirect(
        url_for("usuarios.usuarios")
    )


@usuarios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    usuario = buscar_usuario(id)

    if usuario is None:
        abort(404)

    if request.method == "POST":

        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        idade = request.form["idade"].strip()
        cidade = request.form["cidade"].strip()

        atualizar_usuario(nome, email, idade, cidade, id)

        flash("Usuário atualizado com sucesso!", "success")

        return redirect(
            url_for("usuarios.usuarios")
        )

    usuario = buscar_usuario(id)

    if usuario is None:
        return abort(404)

    return render_template("editar.html", usuario=usuario)
