from flask import Flask, render_template, request, redirect
from banco import conectar, criar_banco, listar_usuarios, inserir_usuario, excluir_usuario, atualizar_usuario,buscar_usuario

app = Flask(__name__)


    
criar_banco()

@app.route("/")
def inicio():
    nome = "joeliton"
    curso = "Flask"
    aula = "2"
    
    return render_template('index.html', nome=nome, curso=curso, aula=aula)


@app.route("/sobre")
def sobre():
    return render_template('sobre.html')

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/cadastro", methods=["GET", "POST"])
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

@app.route("/usuarios")
def usuarios():
      
    lista = listar_usuarios()
    
    return render_template('usuarios.html', usuarios=lista)

@app.route("/excluir/<int:id>")
def excluir(id):
    
    excluir_usuario(id)
    
    return redirect("/usuarios")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    
    
    
    if request.method == "POST":
        
        nome = request.form["nome"]
        email = request.form["email"]
        idade = request.form["idade"]
        cidade = request.form["cidade"]
        
        atualizar_usuario(nome,email, idade, cidade, id)
        
        
        return redirect("/usuarios")
    
    usuario = buscar_usuario(id)
    
    if usuario is None:
        return "Usuário não encontrado"
        
    return render_template("editar.html", usuario=usuario)
        

if __name__ == "__main__":
    app.run(debug=True)