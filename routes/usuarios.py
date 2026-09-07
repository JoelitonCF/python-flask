from flask import Blueprint, render_template, request, redirect, url_for
from banco import listar_usuarios, inserir_usuario, excluir_usuario, atualizar_usuario, buscar_usuario

usuarios_bp = Blueprint(
    "usuarios",
    __name__,
    url_prefix="/usuarios"
)

@usuarios_bp.route("/")
def usuarios():
      
    lista = listar_usuarios()
    
    return render_template('usuarios.html', usuarios=lista)

@usuarios_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    mensagem = None
   
    
    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        idade = request.form["idade"]
        cidade = request.form["cidade"]
        
        inserir_usuario(
            nome, email, idade, cidade
        )
        
        mensagem = f"{nome} cadastrado com sucesso"

    return render_template("cadastro.html", mensagem=mensagem)

@usuarios_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    
    excluir_usuario(id)
    
    return redirect(
        url_for("usuarios.usuarios")
    )


@usuarios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    
    
    
    if request.method == "POST":
        
        nome = request.form["nome"]
        email = request.form["email"]
        idade = request.form["idade"]
        cidade = request.form["cidade"]
        
        atualizar_usuario(nome,email, idade, cidade, id)
        
        
        return redirect(
            url_for("usuarios.usuarios")
        )
    
    usuario = buscar_usuario(id)
    
    if usuario is None:
        return "Usuário não encontrado"
        
    return render_template("editar.html", usuario=usuario)