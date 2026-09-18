import math
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
    excluir_tarefa,
    buscar_tarefas,
    listar_tarefas_paginadas,
    contar_tarefas,
    contar_tarefas_busca,
    buscar_tarefas_paginadas
)

tarefas_bp = Blueprint(
    "tarefas",
    __name__
)


@tarefas_bp.route("/tarefas")
@login_required
def tarefas():

    busca = request.args.get(
        "busca",
        ""
    ).strip()

    pagina = request.args.get(
        "pagina",
        1,
        type=int
    )

    if pagina < 1:
        pagina = 1

    por_pagina = 5

    offset = (
        pagina - 1
    ) * por_pagina

    if busca:

        total = contar_tarefas_busca(
            busca
        )

        lista = buscar_tarefas_paginadas(
            busca,
            por_pagina,
            offset
        )

    else:

        total = contar_tarefas()

        lista = listar_tarefas_paginadas(
            por_pagina,
            offset
        )

    total_paginas = math.ceil(
        total / por_pagina
    )

    return render_template(
        "tarefas.html",
        tarefas=lista,
        busca=busca,
        pagina=pagina,
        total_paginas=total_paginas
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

    tarefa = buscar_tarefas(id)

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
