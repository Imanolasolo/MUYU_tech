import streamlit as st
import pandas as pd
from utils.db import init_db, obtener_observaciones_por_docente, guardar_material, obtener_materiales_por_docente, obtener_feedbacks_por_material, obtener_archivo_material

def dashboard_docente():
    st.title("📚 Panel Docente")
    st.write(f"Bienvenido, {st.session_state['username']}")

    init_db()

    # Subida de material
    st.subheader("Subir video o audio de clase")
    tipo = st.selectbox("Tipo de archivo", ["video", "audio"])
    nombre = st.text_input("Nombre del archivo")
    archivo = st.file_uploader("Selecciona un archivo", type=["mp4", "mov", "mp3", "wav"])
    if st.button("Subir archivo"):
        if archivo and nombre:
            guardar_material(st.session_state["username"], tipo, nombre, archivo.read())
            st.success("Archivo subido correctamente")
            st.rerun()
        else:
            st.warning("Completa todos los campos")

    # Mostrar materiales subidos y feedback recibido
    st.subheader("Tus materiales subidos y feedback recibido")
    materiales = obtener_materiales_por_docente(st.session_state["username"])
    if materiales:
        for m in materiales:
            st.markdown(f"**{m[3]}** ({m[2]}) - {m[1]}")
            # Mostrar archivo (opcional)
            if st.button("Ver archivo", key=f"ver_{m[0]}"):
                archivo_data = obtener_archivo_material(m[0])
                if archivo_data:
                    archivo_bytes, tipo_archivo, nombre_archivo = archivo_data
                    if tipo_archivo == "video":
                        st.video(archivo_bytes)
                    elif tipo_archivo == "audio":
                        st.audio(archivo_bytes)
            # Mostrar feedback
            feedback = obtener_feedbacks_por_material(m[0])
            if feedback:
                coach, feedback_coach, admin, feedback_admin, fecha = feedback
                if feedback_coach:
                    st.info(f"Feedback del coach ({coach}): {feedback_coach}")
                if feedback_admin:
                    st.success(f"Feedback del admin ({admin}): {feedback_admin}")
            else:
                st.write("Sin feedback aún.")
            st.markdown("---")
    else:
        st.info("No has subido materiales aún.")

    st.subheader("Observaciones recibidas")
    rows = obtener_observaciones_por_docente(st.session_state["username"])
    if rows:
        df = pd.DataFrame(rows, columns=["Fecha", "Coach", "Estándar A", "Estándar B", "Notas"])
        st.dataframe(df)
    else:
        st.info("No hay observaciones registradas.")
