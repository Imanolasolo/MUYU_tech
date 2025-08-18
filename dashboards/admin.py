import streamlit as st
import pandas as pd
import altair as alt
from utils.db import init_db, importar_observaciones_desde_excel, get_connection
from crud.usuarios import init_db as init_usuarios_db, crear_usuario, obtener_usuarios, eliminar_usuario
from crud.documentos import init_db as init_documentos_db, crear_documento, obtener_documentos, eliminar_documento

def dashboard_admin():
    st.title("📊 Dashboard Administrativo")
    st.write(f"Bienvenido, {st.session_state['username']}")

    init_db()

    # Importar datos desde Excel
    st.subheader("Importar observaciones desde Excel")
    excel_file = st.file_uploader("Selecciona un archivo Excel", type=["xlsx"])
    if excel_file:
        df = pd.read_excel(excel_file)
        st.dataframe(df)
        if st.button("Importar datos"):
            importar_observaciones_desde_excel(df)
            st.success("Datos importados correctamente")

    # Mostrar datos desde la base
    conn = get_connection()
    df = pd.read_sql_query("SELECT docente as Docente, estandar_a as 'Estándar A', estandar_b as 'Estándar B', (estandar_a+estandar_b)*10 as Progreso FROM observaciones", conn)
    conn.close()

    st.subheader("Progreso por docente")
    st.dataframe(df)

    if not df.empty:
        chart = alt.Chart(df).mark_bar().encode(
            x="Docente",
            y="Progreso",
            color="Docente"
        )
        st.altair_chart(chart, use_container_width=True)

    # CRUD Usuarios
    st.subheader("Gestión de Usuarios")
    init_usuarios_db()
    with st.expander("Crear usuario"):
        new_username = st.text_input("Nuevo usuario")
        new_password = st.text_input("Contraseña", type="password")
        new_role = st.selectbox("Rol", ["Administrador", "Coach", "Docente"])
        if st.button("Crear usuario"):
            try:
                crear_usuario(new_username, new_password, new_role)
                st.success("Usuario creado")
            except Exception as e:
                st.error(f"Error: {e}")

    usuarios = obtener_usuarios()
    st.write("Usuarios registrados:")
    for u in usuarios:
        st.write(f"{u[1]} ({u[2]})", key=f"user_{u[0]}")
        if st.button("Eliminar", key=f"del_user_{u[0]}"):
            eliminar_usuario(u[0])
            st.success("Usuario eliminado")
            st.rerun()

    # CRUD Documentos
    st.subheader("Gestión de Documentos")
    init_documentos_db()
    with st.expander("Subir documento"):
        doc_nombre = st.text_input("Nombre del documento")
        doc_desc = st.text_area("Descripción")
        doc_file = st.file_uploader("Archivo", type=["pdf", "docx", "xlsx"])
        if st.button("Subir documento"):
            if doc_file:
                crear_documento(doc_nombre, doc_desc, doc_file.read())
                st.success("Documento subido")
            else:
                st.warning("Selecciona un archivo")

    documentos = obtener_documentos()
    st.write("Documentos:")
    for d in documentos:
        st.write(f"{d[1]} - {d[2]}", key=f"doc_{d[0]}")
        if st.button("Eliminar documento", key=f"del_doc_{d[0]}"):
            eliminar_documento(d[0])
            st.success("Documento eliminado")
            st.rerun()
