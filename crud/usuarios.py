import sqlite3

DB_PATH = "usuarios.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
    conn.commit()
    conn.close()

def crear_usuario(username, password, role):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()

def obtener_usuarios():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, role FROM usuarios")
    rows = c.fetchall()
    conn.close()
    return rows

def eliminar_usuario(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
