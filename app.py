# app.py
import streamlit as st
import jwt
import datetime

# === CONFIGURACIÓN INICIAL ===
st.set_page_config(page_title="Plataforma Muyu", layout="wide")

JWT_SECRET = "secreto_demo"
ROLES = ["Administrador", "Coach", "Docente"]

# Simulación de usuarios
USERS = {
    "admin": {"password": "1234", "role": "Administrador"},
    "coach1": {"password": "1234", "role": "Coach"},
    "docente1": {"password": "1234", "role": "Docente"}
}

# === FUNCIONES DE AUTENTICACIÓN ===
def create_jwt_token(username, role):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_jwt_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except:
        return None

def login():
    st.subheader("Iniciar sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Login"):
        user = USERS.get(username)
        if user and user["password"] == password:
            token = create_jwt_token(username, user["role"])
            st.session_state["token"] = token
            st.session_state["role"] = user["role"]
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

# === IMPORTACIÓN DE DASHBOARDS ===
from dashboards.admin import dashboard_admin
from dashboards.coach import dashboard_coach
from dashboards.docente import dashboard_docente

# === APP ===
if "token" not in st.session_state:
    login()
else:
    payload = decode_jwt_token(st.session_state["token"])
    if not payload:
        st.warning("Sesión expirada. Inicia sesión de nuevo.")
        st.session_state.clear()
        login()
    else:
        role = payload["role"]
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.clear()
            st.rerun()

        if role == "Administrador":
            dashboard_admin()
        elif role == "Coach":
            dashboard_coach()
        elif role == "Docente":
            dashboard_docente()
