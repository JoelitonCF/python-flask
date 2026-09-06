import sqlite3

def conectar():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row
    
    return conexao


def criar_banco():
    conexao = conectar()
    
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
    
def listar_usuarios():
    conexao = conectar()
    
    cursor = conexao.cursor()
        
    cursor.execute("""
                       SELECT * FROM usuarios
                       """)
    usuarios = cursor.fetchall()
        
    conexao.close()
    
    return usuarios

def inserir_usuario(nome, email, idade, cidade):
    conexao = conectar()
            
    cursor = conexao.cursor()
    
    cursor.execute("""
                    INSERT INTO usuarios (nome, email, idade, cidade)
                    VALUES (?, ?, ?, ?)
                    """,
                    (nome, email, idade, cidade)
                    )
    conexao.commit()
    
    conexao.close()

def buscar_usuario(id):
    
    conexao = conectar()
        
    cursor = conexao.cursor()
    cursor.execute(
            "SELECT * FROM usuarios WHERE id = ?",
            (id,)
        )
    usuario = cursor.fetchone()
        
    conexao.close()
    return usuario

def atualizar_usuario(nome, email, idade, cidade, id):
    conexao = conectar()
        
    cursor = conexao.cursor()
    cursor.execute("""
                           UPDATE usuarios 
                           SET nome = ?, email = ?, idade = ?, cidade = ?
                           WHERE id = ?
                """, (nome, email, idade, cidade, id)
            )
            
    conexao.commit()
    conexao.close()

def excluir_usuario(id):
    conexao = conectar()
        
    cursor = conexao.cursor()
    
    cursor.execute(
        "DELETE FROM usuarios WHERE id = ? ",
        (id,)
    )
    
    conexao.commit()
    
    conexao.close()
