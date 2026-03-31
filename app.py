import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Miracle 82 ERP", layout="wide", page_icon="💎")

# --- CONEXIÓN A SUPABASE ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_metas_html=True)

# --- NAVEGACIÓN LATERAL ---
with st.sidebar:
    st.image("https://via.placeholder.com/150?text=Miracle+82", width=100) # Aquí irá tu logo
    st.title("Miracle 82 ERP")
    menu = st.radio(
        "MÓDULOS DEL SISTEMA",
        ["📊 Dashboard", "📒 Contabilidad", "🏦 Bancos", "👥 Clientes", "🚚 Proveedores", "📁 Subir Archivos"]
    )
    st.info(f"Usuario: Mauro Garcia\nFecha: {datetime.date.today()}")

# --- MÓDULO 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("Panel de Control Financiero")
    col1, col2, col3 = st.columns(3)
    
    # Simulación de métricas (Esto se conectará a tus tablas después)
    col1.metric("Ingresos Totales", "L. 250,000", "+5%")
    col2.metric("Gastos Totales", "L. 120,000", "-2%")
    col3.metric("Saldo Bancos", "L. 130,000")
    
    st.subheader("Flujo de Caja Mensual")
    chart_data = pd.DataFrame({"Mes": ["Ene", "Feb", "Mar"], "Ingresos": [10, 20, 15], "Gastos": [5, 12, 8]})
    st.line_chart(chart_data.set_index("Mes"))

# --- MÓDULO 2: CONTABILIDAD ---
elif menu == "📒 Contabilidad":
    st.title("Libro Diario y Catálogo")
    tab1, tab2 = st.tabs(["Nueva Partida", "Ver Catálogo"])
    
    with tab1:
        with st.form("form_diario"):
            c1, c2 = st.columns(2)
            f_fecha = c1.date_input("Fecha", datetime.date.today())
            f_emp = c2.text_input("Empresa/Cliente")
            
            # Carga de catálogo para evitar errores de escritura
            res = supabase.table("catalogo_cuentas").select("*").execute()
            df_cat = pd.DataFrame(res.data)
            
            if not df_cat.empty:
                opciones = [f"{r['codigo_cta']} | {r['nombre_cta']}" for _, r in df_cat.iterrows()]
                sel = st.selectbox("Cuenta Contable", opciones)
                f_cod = sel.split(" | ")[0]
                f_nom = sel.split(" | ")[1]
            else:
                f_cod = st.text_input("Código")
                f_nom = st.text_input("Nombre")
            
            c3, c4 = st.columns(2)
            f_deb = c3.number_input("Debe", min_value=0.0)
            f_hab = c4.number_input("Haber", min_value=0.0)
            f_con = st.text_area("Concepto")
            
            if st.form_submit_button("Guardar Partida"):
                # Lógica de inserción en Supabase
                st.success("Partida guardada correctamente")

# --- MÓDULO 3: BANCOS ---
elif menu == "🏦 Bancos":
    st.title("Conciliación y Movimientos Bancarios")
    st.write("Control de chequeras y transferencias.")
    # Aquí puedes agregar un selectbox para elegir el banco (BAC, Ficohsa, etc.)
    banco = st.selectbox("Seleccione Banco", ["BAC Credomatic", "Ficohsa", "Banpais"])
    st.button(f"Ver Estado de Cuenta {banco}")

# --- MÓDULO 4: CLIENTES ---
elif menu == "👥 Clientes":
    st.title("Cartera de Clientes")
    st.button("➕ Agregar Nuevo Cliente")
    # Tabla de ejemplo de clientes
    df_clientes = pd.DataFrame({
        "RTN": ["08011990...", "05011985..."],
        "Nombre": ["Empresa X", "Comercial Y"],
        "Saldo Pendiente": [5000.00, 0.00]
    })
    st.table(df_clientes)

# --- MÓDULO 5: PROVEEDORES ---
elif menu == "🚚 Proveedores":
    st.title("Cuentas por Pagar")
    st.write("Registro de facturas de proveedores y fechas de vencimiento.")

# --- MÓDULO 6: SUBIR ARCHIVOS ---
elif menu == "📁 Subir Archivos":
    st.title("Gestión Documental")
    st.write("Sube facturas (PDF), Excels de planillas o capturas de RTN.")
    
    uploaded_file = st.file_uploader("Arrastra aquí tu archivo", type=['pdf', 'xlsx', 'png', 'jpg'])
    
    if uploaded_file is not None:
        st.success(f"Archivo '{uploaded_file.name}' listo para procesar.")
        if st.button("Procesar Archivo"):
            st.info("Analizando documento con IA...")
