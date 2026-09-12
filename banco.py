import sqlite3


def conectar():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row
    
    conexao.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conexao


def criar_banco():
    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""                   
                   CREATE TABLE IF NOT EXISTS usuarios (
                       id  INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL, 
                       email TEXT NOT NULL UNIQUE,
                       idade INTEGER,
                       cidade TEXT                       
                   )                  
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS contas (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL,
                       email TEXT NOT NULL UNIQUE,
                       senha TEXT NOT NULL
                   )
                   """)
    
    cursor.execute("""
                   
                   CREATE TABLE IF NOT EXISTS tarefas (
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       titulo TEXT NOT NULL,
                       usuario_id INTEGER NOT NULL,
                       
                       FOREIGN KEY (usuario_id)
                       REFERENCES usuarios(id)
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

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO usuarios
                (nome, email, idade, cidade)
            VALUES (?, ?, ?, ?)
        """, (
            nome,
            email,
            idade,
            cidade
        ))

        conexao.commit()

        return True

    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            "Erro ao inserir usuário:",
            erro
        )

        return False

    finally:
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


def buscar_por_email(email):
    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ?",
        (email,)
    )

    usuario = cursor.fetchone()

    conexao.close()

    return usuario


def inserir_conta(nome, email, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
                   INSERT INTO contas (nome, email, senha)
                   VALUES (?, ?, ?)
                   """, (nome, email, senha))

    conexao.commit()
    conexao.close()


def buscar_conta_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM contas WHERE email = ?",
        (email,)
    )

    conta = cursor.fetchone()

    conexao.close()

    return conta

def inserir_tarefa(titulo, usuario_id):
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO tarefas
                (titulo, usuario_id)
            VALUES (?, ?)
        """, (
            titulo,
            usuario_id
        ))

        conexao.commit()

        return True

    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            "Erro ao inserir tarefa:",
            erro
        )

        return False

    finally:
        conexao.close()
        

def listar_tarefas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            tarefas.id,
            tarefas.titulo,
            usuarios.nome AS usuario_nome

        FROM tarefas

        JOIN usuarios
            ON tarefas.usuario_id = usuarios.id
    """)

    tarefas = cursor.fetchall()

    conexao.close()

    return tarefas


def buscar_tarefa(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM tarefas
        WHERE id = ?
    """, (id,))

    tarefa = cursor.fetchone()

    conexao.close()

    return tarefa


def atualizar_tarefa(id, titulo, usuario_id):
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE tarefas
            SET titulo = ?, usuario_id = ?
            WHERE id = ?
        """, (
            titulo,
            usuario_id,
            id
        ))

        conexao.commit()

        return True

    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            "Erro ao atualizar tarefa:",
            erro
        )

        return False

    finally:
        conexao.close()
        

def excluir_tarefa(id):
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM tarefas
            WHERE id = ?
        """, (id,))

        conexao.commit()

        return True

    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            "Erro ao excluir tarefa:",
            erro
        )

        return False

    finally:
        conexao.close()