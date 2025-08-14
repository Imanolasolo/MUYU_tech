import streamlit as st
import datetime
from utils.db import init_db, guardar_observacion
from crud.videos import init_db as init_videos_db, crear_video, obtener_videos, eliminar_video

def dashboard_coach():
    st.title("📝 Panel de Observaciones")
    st.write(f"Bienvenido, {st.session_state['username']}")

    init_db()

    docente = st.selectbox("Docente observado", ["Ana", "Luis", "María", "Pedro"])
    estandar_a = st.slider("Estándar A", 1, 5, 3)
    estandar_b = st.slider("Estándar B", 1, 5, 3)
    notas = st.text_area("Notas de observación")
    subir_video = st.file_uploader("Subir video de la clase", type=["mp4", "mov"])
    subir_foto = st.file_uploader("Subir foto", type=["jpg", "png"])

    if st.button("Guardar observación"):
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        video_bytes = subir_video.read() if subir_video else None
        foto_bytes = subir_foto.read() if subir_foto else None
        guardar_observacion(
            docente, st.session_state["username"], fecha,
            estandar_a, estandar_b, notas, video_bytes, foto_bytes
        )
        st.success("Observación guardada")

    # CRUD Videos
    st.subheader("Gestión de Videos")
    init_videos_db()
    with st.expander("Subir video"):
        vid_nombre = st.text_input("Nombre del video")
        vid_desc = st.text_area("Descripción del video")
        vid_file = st.file_uploader("Archivo de video", type=["mp4", "mov"])
        if st.button("Subir video"):
            if vid_file:
                crear_video(vid_nombre, vid_desc, vid_file.read())
                st.success("Video subido")
            else:
                st.warning("Selecciona un archivo de video")

    videos = obtener_videos()
    st.write("Videos subidos:")
    for v in videos:
        st.write(f"{v[1]} - {v[2]}", key=f"vid_{v[0]}")
        if st.button("Eliminar video", key=f"del_vid_{v[0]}"):
            eliminar_video(v[0])
            st.success("Video eliminado")
            st.experimental_rerun()
