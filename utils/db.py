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
    # Nueva tabla para materiales subidos por docentes
    c.execute("""
        CREATE TABLE IF NOT EXISTS materiales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            docente TEXT,
            fecha TEXT,
            tipo TEXT, -- 'video' o 'audio'
            nombre TEXT,
            archivo BLOB
        )
    """)
    # Nueva tabla para feedbacks
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            coach TEXT,
            feedback_coach TEXT,
            admin TEXT,
            feedback_admin TEXT,
            fecha TEXT,
            FOREIGN KEY(material_id) REFERENCES materiales(id)
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

# Materiales
def guardar_material(docente, tipo, nombre, archivo_bytes):
    conn = get_connection()
    c = conn.cursor()
    fecha = sqlite3.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO materiales (docente, fecha, tipo, nombre, archivo)
        VALUES (?, ?, ?, ?, ?)
    """, (docente, fecha, tipo, nombre, archivo_bytes))
    conn.commit()
    conn.close()

def obtener_materiales_por_docente(docente):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, fecha, tipo, nombre FROM materiales WHERE docente = ?", (docente,))
    rows = c.fetchall()
    conn.close()
    return rows

def obtener_todos_materiales():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, docente, fecha, tipo, nombre FROM materiales")
    rows = c.fetchall()
    conn.close()
    return rows

def obtener_archivo_material(material_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT archivo, tipo, nombre FROM materiales WHERE id = ?", (material_id,))
    row = c.fetchone()
    conn.close()
    return row

# Feedbacks
def guardar_feedback_coach(material_id, coach, feedback):
    conn = get_connection()
    c = conn.cursor()
    fecha = sqlite3.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT OR REPLACE INTO feedbacks (material_id, coach, feedback_coach, fecha)
        VALUES (?, ?, ?, ?)
    """, (material_id, coach, feedback, fecha))
    conn.commit()
    conn.close()

def guardar_feedback_admin(material_id, admin, feedback):
    conn = get_connection()
    c = conn.cursor()
    fecha = sqlite3.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Actualiza el feedback_admin en el registro existente
    c.execute("""
        UPDATE feedbacks SET admin = ?, feedback_admin = ?, fecha = ?
        WHERE material_id = ?
    """, (admin, feedback, fecha, material_id))
    conn.commit()
    conn.close()

def obtener_feedbacks_por_material(material_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT coach, feedback_coach, admin, feedback_admin, fecha
        FROM feedbacks WHERE material_id = ?
    """, (material_id,))
    row = c.fetchone()
    conn.close()
    return row
