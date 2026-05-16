import streamlit as st
import sys
from pathlib import Path

# Garantizar que Streamlit Cloud encuentre los módulos locales al ejecutar desde subcarpetas
sys.path.append(str(Path(__file__).parent))

from decimal import Decimal
from datetime import date
from loan_models import PaymentFrequency
from loan_schedule import LoanScheduleGenerator
import pandas as pd
import plotly.express as px

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

ui_currency = st.sidebar.text_input(
    label="Moneda",
    value="NOK"
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
    # 4.1 Preparar parámetros para el backend (Decimal)
    principal = Decimal(str(ui_principal))
    annual_rate = Decimal(str(ui_rate_percentage)) / Decimal('100')
    
    # 4.2 Enviar los datos al motor matemático correcto
    with st.spinner('Procesando cálculos financieros...'):
        if "1" in ui_system_type:
            schedule = LoanScheduleGenerator.generate_annuity_schedule(
                principal, annual_rate, date.today(), ui_years, PaymentFrequency.MONTHLY
            )
        elif "2" in ui_system_type:
            schedule = LoanScheduleGenerator.generate_serial_schedule(
                principal, annual_rate, date.today(), ui_years, PaymentFrequency.MONTHLY
            )
        else:
            schedule = LoanScheduleGenerator.generate_bullet_schedule(
                principal, annual_rate, date.today(), ui_years, PaymentFrequency.MONTHLY
            )
            
    # 4.3 Convertir la respuesta a Pandas DataFrame para visualización
    df = pd.DataFrame([row.__dict__ for row in schedule])
    df['due_date'] = df['due_date'].astype(str) # Formato de fecha
    
    # 4.4 KPIs (Key Performance Indicators)
    total_interest = df['interest_paid'].sum()
    total_paid = df['payment_amount'].sum()
    
    st.markdown("### 📊 Resumen de la Operación")
    col1, col2, col3 = st.columns(3)
    col1.metric("Capital Solicitado", f"{ui_principal:,.2f}")
    col2.metric("Interés Total a Pagar", f"{float(total_interest):,.2f}")
    col3.metric("Costo Total (Capital + Interés)", f"{float(total_paid):,.2f}")
    
    st.markdown("---")
    
    # 4.5 Gráfico de Barras Apiladas (Composición de la cuota)
    st.markdown("### 📈 Composición de la Cuota (Capital e Interés)")
    
    # Preparamos los datos
    chart_data = df[['due_date', 'principal_paid', 'interest_paid', 'payment_amount']].copy()
    chart_data.rename(columns={'payment_amount': 'Cuota Total'}, inplace=True)
    
    # Transformar a formato Long para Plotly (solo apilamos Capital e Interés)
    chart_data_melted = chart_data.melt(
        id_vars=['due_date', 'Cuota Total'], 
        value_vars=['principal_paid', 'interest_paid'],
        var_name='Componente', 
        value_name='Monto'
    )
    
    # Nombres elegantes para la leyenda
    chart_data_melted['Componente'] = chart_data_melted['Componente'].replace({
        'principal_paid': 'Amortización Capital',
        'interest_paid': 'Interés'
    })

    # Crear el gráfico de barras apiladas
    fig = px.bar(
        chart_data_melted, 
        x='due_date', 
        y='Monto', 
        color='Componente',
        barmode='stack',
        color_discrete_map={
            'Amortización Capital': '#E55342', # Naranja/Rojo estilo el diseño
            'Interés': '#52BDE9'               # Celeste claro estilo el diseño
        },
        hover_data={'Cuota Total': ':,.2f', 'due_date': False, 'Componente': False}
    )
    
    # Formateo Premium de Ejes
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title=f"Monto ({ui_currency.upper()})",
        height=450,
        hovermode="x unified",
        legend_title=None,
        margin=dict(l=20, r=20, t=40, b=20), # Agregamos márgenes para separar de los bordes
        bargap=0.2 # Espacio entre las columnas para un diseño más limpio
    )
    
    # Formatear el eje X para mostrar años enteros, y el eje Y con separadores de miles
    fig.update_xaxes(
        dtick="M12", # Mostrar etiqueta cada 12 meses (1 año)
        tickformat="%Y" # Mostrar solo el año "2026", "2027"
    )
    fig.update_yaxes(tickformat=",.0f")
    
    # Dar formato de moneda a los valores del tooltip (hover)
    fig.update_traces(hovertemplate="%{y:,.2f}")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 4.6 Tabla de datos interactiva
    st.markdown("### 🗓️ Cronograma de Amortización Oficial")
    st.dataframe(
        df, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "payment_number": "Nº Cuota",
            "due_date": "Fecha de Pago",
            "payment_amount": st.column_config.NumberColumn("Cuota Total a Pagar", format="%.2f"),
            "principal_paid": st.column_config.NumberColumn("Amortización Capital", format="%.2f"),
            "interest_paid": st.column_config.NumberColumn("Pago Interés", format="%.2f"),
            "remaining_balance": st.column_config.NumberColumn("Saldo Restante", format="%.2f"),
        }
    )
else:
    st.write("👈 Ajusta los parámetros en la barra lateral y presiona 'Generar Cronograma'.")
