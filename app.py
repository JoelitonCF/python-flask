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

if __name__ == "__main__":
    app.run(debug=True)