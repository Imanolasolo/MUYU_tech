import sqlite3

DB_PATH = "videos.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT,
            archivo BLOB
        )
    """)
    conn.commit()
    conn.close()

def crear_video(nombre, descripcion, archivo_bytes):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO videos (nombre, descripcion, archivo) VALUES (?, ?, ?)", (nombre, descripcion, archivo_bytes))
    conn.commit()
    conn.close()

def obtener_videos():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, nombre, descripcion FROM videos")
    rows = c.fetchall()
    conn.close()
    return rows

def eliminar_video(video_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()
