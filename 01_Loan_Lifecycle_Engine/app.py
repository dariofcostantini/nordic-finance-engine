import streamlit as st
from decimal import Decimal
from datetime import date
from loan_models import PaymentFrequency
# from loan_schedule import LoanScheduleGenerator # We will use this in step 2

# 1. Configuración básica de la página (Pestaña del navegador)
st.set_page_config(
    page_title="Nordic Loan Engine",
    page_icon="🏦",
    layout="wide" # Usa toda la pantalla, ideal para tablas financieras
)

# 2. Título principal en la UI
st.title("🏦 Nordic Loan Engine")
st.markdown("Generador de cronogramas de amortización con estándares europeos.")

# 3. Sidebar (Barra lateral izquierda) para que el usuario ingrese datos
st.sidebar.header("⚙️ Parámetros del Préstamo")

# Usamos st.number_input para evitar que el usuario ingrese letras y rompa la app
ui_principal = st.sidebar.number_input(
    label="Monto del Préstamo (Principal)",
    min_value=1000.0,
    value=1000000.0,
    step=10000.0
)

ui_rate_percentage = st.sidebar.number_input(
    label="Tasa de Interés Anual (%)",
    min_value=0.0,
    max_value=100.0,
    value=4.5,
    step=0.1
)

ui_years = st.sidebar.number_input(
    label="Plazo en Años",
    min_value=1,
    max_value=40,
    value=25,
    step=1
)

ui_system_type = st.sidebar.selectbox(
    label="Sistema de Amortización",
    options=[
        "1. Sistema Francés (Annuitetslån)", 
        "2. Sistema Alemán (Serielån)", 
        "3. Sistema Americano (Bullet)"
    ]
)

st.sidebar.markdown("---")
# Un botón para darle el control al usuario de cuándo recalcular
calculate_btn = st.sidebar.button("Generar Cronograma", type="primary")

# 4. Zona Principal de la pantalla
if calculate_btn:
    st.info("Aquí conectaremos nuestro motor matemático en el Paso 2.")
    # st.write(f"Has pedido: {ui_principal} a {ui_years} años con el {ui_system_type}")
else:
    st.write("👈 Ajusta los parámetros en la barra lateral y presiona 'Generar Cronograma'.")
