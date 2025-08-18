import streamlit as st
import datetime
from utils.db import init_db, guardar_observacion, obtener_todos_materiales, obtener_archivo_material, guardar_feedback_coach, obtener_feedbacks_por_material
from crud.videos import init_db as init_videos_db, crear_video, obtener_videos, eliminar_video

def dashboard_coach():
    st.title("📝 Panel de Observaciones")
    st.write(f"Bienvenido, {st.session_state['username']}")

    init_db()

    # Feedback a materiales subidos por docentes
    st.subheader("Materiales subidos por docentes")
    materiales = obtener_todos_materiales()
    for m in materiales:
        st.markdown(f"**{m[4]}** ({m[3]}) - {m[2]} - Docente: {m[1]}")
        if st.button("Ver archivo", key=f"ver_mat_{m[0]}"):
            archivo_data = obtener_archivo_material(m[0])
            if archivo_data:
                archivo_bytes, tipo_archivo, nombre_archivo = archivo_data
                if tipo_archivo == "video":
                    st.video(archivo_bytes)
                elif tipo_archivo == "audio":
                    st.audio(archivo_bytes)
        # Feedback coach
        feedback = obtener_feedbacks_por_material(m[0])
        feedback_coach = feedback[1] if feedback else ""
        nuevo_feedback = st.text_area("Feedback para el docente", value=feedback_coach or "", key=f"fb_coach_{m[0]}")
        if st.button("Guardar feedback", key=f"save_fb_{m[0]}"):
            guardar_feedback_coach(m[0], st.session_state["username"], nuevo_feedback)
            st.success("Feedback guardado")
            st.rerun()
        # Mostrar feedback admin si existe
        if feedback and feedback[3]:
            st.success(f"Feedback del admin ({feedback[2]}): {feedback[3]}")
        st.markdown("---")

    
