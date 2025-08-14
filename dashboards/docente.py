import streamlit as st
import pandas as pd
from utils.db import init_db, obtener_observaciones_por_docente

def dashboard_docente():
    st.title("📚 Panel Docente")
    st.write(f"Bienvenido, {st.session_state['username']}")

    init_db()

    st.subheader("Observaciones recibidas")
    rows = obtener_observaciones_por_docente(st.session_state["username"])
    if rows:
        df = pd.DataFrame(rows, columns=["Fecha", "Coach", "Estándar A", "Estándar B", "Notas"])
        st.dataframe(df)
    else:
        st.info("No hay observaciones registradas.")
