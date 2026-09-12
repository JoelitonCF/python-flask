from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask import abort

from auth_utils import login_required

from banco import (
    listar_tarefas,
    listar_usuarios,
    inserir_tarefa,
    buscar_tarefa,
    atualizar_tarefa,
    excluir_tarefa
)

tarefas_bp = Blueprint(
    "tarefas",
    __name__
)

@tarefas_bp.route("/tarefas")
@login_required
def tarefas():

    lista = listar_tarefas()

    return render_template(
        "tarefas.html",
        tarefas=lista
    )
    
@tarefas_bp.route(
    "/tarefas/cadastrar",
    methods=["GET", "POST"]
)
@login_required
def cadastrar():

    usuarios = listar_usuarios()

    if request.method == "POST":

        titulo = request.form["titulo"].strip()
        usuario_id = request.form["usuario_id"]

        if not titulo:
            flash(
                "Informe o título da tarefa.",
                "error"
            )

            return render_template(
                "cadastrar_tarefa.html",
                usuarios=usuarios
            )

        sucesso = inserir_tarefa(
            titulo,
            usuario_id
        )

        if sucesso:

            flash(
                "Tarefa cadastrada com sucesso!",
                "success"
            )

            return redirect(
                url_for("tarefas.tarefas")
            )

        else:

            flash(
                "Não foi possível cadastrar a tarefa.",
                "error"
            )

    return render_template(
        "cadastrar_tarefa.html",
        usuarios=usuarios
    )
    
@tarefas_bp.route(
    "/tarefas/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar(id):

    tarefa = buscar_tarefa(id)

    if tarefa is None:
        abort(404)

    usuarios = listar_usuarios()

    if request.method == "POST":

        titulo = request.form["titulo"].strip()

        usuario_id = int(
            request.form["usuario_id"]
        )

        if not titulo:

            flash(
                "Informe o título da tarefa.",
                "error"
            )

            return render_template(
                "editar_tarefa.html",
                tarefa=tarefa,
                usuarios=usuarios
            )

        sucesso = atualizar_tarefa(
            id,
            titulo,
            usuario_id
        )

        if sucesso:

            flash(
                "Tarefa atualizada com sucesso!",
                "success"
            )

            return redirect(
                url_for("tarefas.tarefas")
            )

        flash(
            "Não foi possível atualizar a tarefa.",
            "error"
        )

    return render_template(
        "editar_tarefa.html",
        tarefa=tarefa,
        usuarios=usuarios
    )
    
@tarefas_bp.route(
    "/tarefas/excluir/<int:id>",
    methods=["POST"]
)
@login_required
def excluir(id):

    tarefa = buscar_tarefa(id)

    if tarefa is None:
        abort(404)

    sucesso = excluir_tarefa(id)

    if sucesso:

        flash(
            "Tarefa excluída com sucesso!",
            "success"
        )

    else:

        flash(
            "Não foi possível excluir a tarefa.",
            "error"
        )

    return redirect(
        url_for("tarefas.tarefas")
    )