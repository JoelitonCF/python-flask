from flask import Blueprint, jsonify, request

from banco import listar_tarefas, buscar_tarefa, inserir_tarefa, atualizar_tarefa, excluir_tarefa

api_bp = Blueprint(
    "api", 
    __name__,
    url_prefix="/api"
)

@api_bp.route(
    "/tarefas",
    methods=["GET"]
)
def listar():

    tarefas = listar_tarefas()

    resultado = []

    for tarefa in tarefas:

        resultado.append({
            "id": tarefa["id"],
            "titulo": tarefa["titulo"],
            # "usuario_id": tarefa["usuario_id"],
            "usuario_nome": tarefa["usuario_nome"]
        })

    return jsonify(resultado)

@api_bp.route(
    "/tarefas/<int:id>",
    methods=["GET"]
)
def buscar(id):

    tarefa = buscar_tarefa(id)

    if tarefa is None:

        return jsonify({
            "erro": "Tarefa não encontrada"
        }), 404

    resultado = {
        "id": tarefa["id"],
        "titulo": tarefa["titulo"],
        "usuario_id": tarefa["usuario_id"]
    }

    return jsonify(resultado)

@api_bp.route(
    "/tarefas",
    methods=["POST"]
)
def criar():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "JSON não enviado"
        }), 400

    titulo = dados.get("titulo")
    usuario_id = dados.get("usuario_id")

    if not titulo or not usuario_id:
        return jsonify({
            "erro": "titulo e usuario_id são obrigatórios"
        }), 400
    
    print(titulo, usuario_id)

    sucesso = inserir_tarefa(
        titulo,
        usuario_id
    )

    if not sucesso:
        return jsonify({
            "erro": "Não foi possível criar a tarefa"
        }), 500

    return jsonify({
        "mensagem": "Tarefa criada com sucesso"
    }), 201
    
@api_bp.route(
    "/tarefas/<int:id>",
    methods=["PUT"]
)
def atualizar(id):

    tarefa = buscar_tarefa(id)

    if tarefa is None:
        return jsonify({
            "erro": "Tarefa não encontrada"
        }), 404

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "JSON não enviado"
        }), 400

    titulo = dados.get("titulo")
    usuario_id = dados.get("usuario_id")

    if not titulo or not usuario_id:
        return jsonify({
            "erro": "titulo e usuario_id são obrigatórios"
        }), 400

    sucesso = atualizar_tarefa(
        id,
        titulo,
        usuario_id
    )

    if not sucesso:
        return jsonify({
            "erro": "Não foi possível atualizar"
        }), 500

    return jsonify({
        "mensagem": "Tarefa atualizada com sucesso"
    })
    
    
@api_bp.route(
    "/tarefas/<int:id>",
    methods=["DELETE"]
)
def excluir(id):

    tarefa = buscar_tarefa(id)

    if tarefa is None:
        return jsonify({
            "erro": "Tarefa não encontrada"
        }), 404

    sucesso = excluir_tarefa(id)

    if not sucesso:
        return jsonify({
            "erro": "Não foi possível excluir"
        }), 500

    return jsonify({
        "mensagem": "Tarefa excluída com sucesso"
    })