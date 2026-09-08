from flask import Flask, render_template, request, redirect
from banco import  criar_banco
from routes.usuarios import usuarios_bp
from routes.auth import auth_bp

app = Flask(__name__)
app.secret_key = "minha-chave-secreta"

app.register_blueprint(usuarios_bp)
app.register_blueprint(auth_bp)
   
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

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404

@app.errorhandler(405)
def metodo_nao_permitido(erro):
    return render_template("405.html"), 405

@app.errorhandler(500)
def erro_interno(erro):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)