from flask import Flask, render_template, request, redirect
import json
import sqlite3

app = Flask(__name__)

def criar_banco():
    conexao = sqlite3.connect("banco.db")
    
    cursor = conexao.cursor()
    
    cursor.execute("""                   
                   CREATE TABLE IF NOT EXISTS usuarios (
                       id  INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL, 
                       email TEXT NOT NULL,
                       idade INTEGER,
                       cidade TEXT                       
                   )                  
                   """)
    conexao.commit()
    conexao.close()
    
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
        
        conexao = sqlite3.connect("banco.db")
        
        cursor = conexao.cursor()
        
        cursor.execute("""
                       INSERT INTO usuarios (nome, email, idade, cidade)
                       VALUES (?, ?, ?, ?)
                       """,
                       (nome, email, idade, cidade)
                       )
        conexao.commit()
        
        conexao.close()
        
        mensagem = f"{nome} cadastrado com sucesso"

    return render_template("cadastro.html", mensagem=mensagem)

@app.route("/usuarios")
def usuarios():
      
    conexao = sqlite3.connect("banco.db")
    
    conexao.row_factory = sqlite3.Row
    
    cursor = conexao.cursor()
    
    cursor.execute("""
                   SELECT * FROM usuarios
                   """)
    usuarios = cursor.fetchall()
    
    conexao.close()
    
    return render_template('usuarios.html', usuarios=usuarios)

@app.route("/excluir/<int:id>")
def excluir(id):
    conexao = sqlite3.connect("banco.db")
    
    cursor = conexao.cursor()
    
    cursor.execute(
        "DELETE FROM usuarios WHERE id = ? ",
        (id,)
    )
    
    conexao.commit()
    
    conexao.close()
    
    return redirect("/usuarios")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    
    conexao = sqlite3.connect("banco.db")
    
    conexao.row_factory = sqlite3.Row
    
    cursor = conexao.cursor()
    
    if request.method == "POST":
        
        nome = request.form["nome"]
        email = request.form["email"]
        idade = request.form["idade"]
        cidade = request.form["cidade"]
        
        cursor.execute("""
                       UPDATE usuarios 
                       SET nome = ?, email = ?, idade = ?, cidade = ?
                       WHERE id = ?
            """, (nome, email, idade, cidade, id)
        )
        
        conexao.commit()
        conexao.close()
        
        return redirect("/usuarios")
    
    cursor.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (id,)
    )
    usuario = cursor.fetchone()
    
    conexao.close()
    
    if usuario is None:
        return "Usuário não encontrado"
        
    return render_template("editar.html", usuario=usuario)
        

if __name__ == "__main__":
    app.run(debug=True)