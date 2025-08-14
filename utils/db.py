import sqlite3

DB_PATH = "observaciones.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS observaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            docente TEXT,
            coach TEXT,
            fecha TEXT,
            estandar_a INTEGER,
            estandar_b INTEGER,
            notas TEXT,
            video BLOB,
            foto BLOB
        )
    """)
    conn.commit()
    conn.close()

def guardar_observacion(docente, coach, fecha, estandar_a, estandar_b, notas, video, foto):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO observaciones (docente, coach, fecha, estandar_a, estandar_b, notas, video, foto)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (docente, coach, fecha, estandar_a, estandar_b, notas, video, foto))
    conn.commit()
    conn.close()

def obtener_observaciones_por_docente(docente):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT fecha, coach, estandar_a, estandar_b, notas FROM observaciones WHERE docente = ?", (docente,))
    rows = c.fetchall()
    conn.close()
    return rows

def importar_observaciones_desde_excel(df):
    conn = get_connection()
    c = conn.cursor()
    for _, row in df.iterrows():
        c.execute("""
            INSERT INTO observaciones (docente, coach, fecha, estandar_a, estandar_b, notas, video, foto)
            VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)
        """, (
            row.get("Docente"),
            row.get("Coach"),
            row.get("Fecha"),
            row.get("Estándar A"),
            row.get("Estándar B"),
            row.get("Notas")
        ))
    conn.commit()
    conn.close()
