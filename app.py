import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Miracle 82 ERP", page_icon="📊", layout="wide")

# Estilo personalizado (Verde esmeralda y Oro)
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #006b3e; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS ---
if 'libro_diario' not in st.session_state:
    st.session_state.libro_diario = pd.DataFrame(columns=['Fecha', 'Empresa', 'Partida', 'Código', 'Cuenta', 'Debe', 'Haber'])

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2652/2652218.png", width=100)
st.sidebar.title("Miracle 82 ASESORES")
archivo_excel = st.sidebar.file_uploader("📂 Cargar Catálogo (Excel)", type=['xlsx'])

if archivo_excel:
    df_cat = pd.read_excel(archivo_excel)
    st.sidebar.success("Catálogo Activo")
    
    menu = ["🏠 Dashboard", "💰 Registrar Venta", "🛒 Registrar Gasto", "📖 Libro Diario"]
    choice = st.sidebar.selectbox("Menú", menu)

    # --- LÓGICA DE REGISTRO ---
    if choice == "💰 Registrar Venta":
        st.header("Registro de Ingresos (ISV 15%)")
        with st.form("venta"):
            empresa = st.selectbox("Empresa", ["Las Delicias de Maleny", "SAMSA", "Miracle 82"])
            total = st.number_input("Total de la Factura (Lps)", min_value=0.0)
            cod_caja = st.text_input("Código de Entrada (Caja/Banco)", "1110101001")
            if st.form_submit_button("Procesar Venta"):
                base = round(total / 1.15, 2)
                isv = round(total - base, 2)
                # (Aquí se añade la lógica de guardado que desarrollamos en Colab)
                st.success(f"Venta registrada. Base: L.{base} | ISV: L.{isv}")

    elif choice == "🏠 Dashboard":
        st.header("Indicadores Financieros")
        col1, col2, col3 = st.columns(3)
        col1.metric("Ventas Totales", "L. 0.00")
        col2.metric("Gastos Totales", "L. 0.00")
        col3.metric("Utilidad Neta", "L. 0.00", delta_color="normal")
        
        st.info("Sube transacciones para ver las gráficas de rendimiento.")

else:
    st.warning("⚠️ Por favor, carga tu catálogo de cuentas en la barra lateral para comenzar.")
