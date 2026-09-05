from flask import Flask, render_template, request, redirect
import json
import sqlite3

app = Flask(__name__)

def ler_dados():
    with open("dados.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados

def salvar_dados(dados):
    with open("dados.json","w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

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
        
        dados = ler_dados()
        
        if dados:
            novo_id = max(usuario["id"] for usuario in dados) + 1
        else:
            novo_id = 1

        usuario = {
            "id":novo_id,
            "nome": nome, 
            "email": email,
            "idade": idade,
            "cidade":cidade
        }
        
        
        dados.append(usuario)
        
        salvar_dados(dados)
        
        mensagem = f"{nome} cadastrado com sucesso"

    return render_template("cadastro.html", mensagem=mensagem)

@app.route("/usuarios")
def usuarios():
    dados = ler_dados()
    
    return render_template('usuarios.html', usuarios=dados)

@app.route("/excluir/<int:id>")
def excluir(id):
    dados = ler_dados()
    
    nova_lista = []
    
    for usuario in dados:
        if usuario['id'] != id:
            nova_lista.append(usuario)
    
    salvar_dados(nova_lista)
    
    return redirect("/usuarios")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    dados = ler_dados()
    
    usuario_encontrado = None
    
    for usuario in dados:
        if usuario["id"] == id:
            usuario_encontrado = usuario
            break
    
    if usuario_encontrado is None:
        return "Usuário não encontrado"
    
    if request.method == "POST":
        
        nome = request.form["nome"]
        email = request.form["email"]
        idade = request.form["idade"]
        cidade = request.form["cidade"]
        
        usuario_encontrado["nome"] = nome
        usuario_encontrado["email"] = email
        usuario_encontrado["idade"] = idade
        usuario_encontrado["cidade"] = cidade
        
        salvar_dados(dados)
        
        return redirect("/usuarios")
        
    return render_template("editar.html", usuario=usuario_encontrado)
        

if __name__ == "__main__":
    app.run(debug=True)