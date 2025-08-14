import sqlite3

DB_PATH = "documentos.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT,
            archivo BLOB
        )
    """)
    conn.commit()
    conn.close()

def crear_documento(nombre, descripcion, archivo_bytes):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO documentos (nombre, descripcion, archivo) VALUES (?, ?, ?)", (nombre, descripcion, archivo_bytes))
    conn.commit()
    conn.close()

def obtener_documentos():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, nombre, descripcion FROM documentos")
    rows = c.fetchall()
    conn.close()
    return rows

def eliminar_documento(doc_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM documentos WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()
