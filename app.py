import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Miracle 82 ERP", layout="wide", page_icon="💎")

# --- CONEXIÓN A SUPABASE ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- NAVEGACIÓN LATERAL ---
st.sidebar.title("💎 Miracle 82 ERP")
menu = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    ["📊 Dashboards", "📒 Contabilidad", "🏦 Bancos", "👥 Clientes", "🚚 Proveedores", "📁 Subir Archivos"]
)

# --- MÓDULO 1: DASHBOARDS ---
if menu == "📊 Dashboards":
    st.title("Panel de Control Financiero")
    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas Totales", "L. 0.00", "0%")
    col2.metric("Cuentas por Cobrar", "L. 0.00", "0%")
    col3.metric("Saldo en Bancos", "L. 0.00")
    st.info("Las métricas se actualizarán automáticamente al registrar partidas.")

# --- MÓDULO 2: CONTABILIDAD ---
elif menu == "📒 Contabilidad":
    st.title("Libro Diario y Catálogo")
    # Bloque de prueba rápida
test_data = supabase.table("catalogo_cuentas").select("count", count="exact").execute()
st.write(f"Cuentas encontradas en la base de datos: {test_data.count}")
    
    # Cargar catálogo real
    res_cat = supabase.table("catalogo_cuentas").select("codigo_cta, nombre_cta").execute()
    df_cat = pd.DataFrame(res_cat.data)
    
    if not df_cat.empty:
        opciones = [f"{r['codigo_cta']} | {r['nombre_cta']}" for _, r in df_cat.iterrows()]
        
        with st.form("nueva_partida", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            f_fecha = col_a.date_input("Fecha", datetime.date.today())
            f_empresa = col_b.text_input("Empresa/Cliente")
            
            f_cuenta = st.selectbox("Seleccione Cuenta del Catálogo", opciones)
            f_cod = f_cuenta.split(" | ")[0]
            f_nom = f_cuenta.split(" | ")[1]
            
            col_c, col_d = st.columns(2)
            f_debe = col_c.number_input("Debe (Lps)", min_value=0.0)
            f_haber = col_d.number_input("Haber (Lps)", min_value=0.0)
            f_concepto = st.text_area("Concepto")
            
            if st.form_submit_button("💾 Guardar Registro"):
                # Aquí puedes agregar la lógica de insert a la tabla 'libro_diario'
                st.success(f"Asiento registrado exitosamente en {f_nom}")
    else:
        st.warning("El catálogo está vacío. Por favor, verifica la carga del CSV.")

# --- MÓDULO 3: BANCOS ---
elif menu == "🏦 Bancos":
    st.title("Gestión de Bancos")
    st.write("Control de chequeras y conciliación bancaria.")
    st.selectbox("Seleccionar Cuenta Bancaria", ["BAC - 7412...", "Ficohsa - 1002...", "Banpais - 5001..."])

# --- MÓDULO 4: CLIENTES ---
elif menu == "👥 Clientes":
    st.title("Cartera de Clientes")
    st.button("➕ Registrar Nuevo Cliente")
    st.text_input("Buscar por RTN")

# --- MÓDULO 5: PROVEEDORES ---
elif menu == "🚚 Proveedores":
    st.title("Cuentas por Pagar")
    st.date_input("Próximos Vencimientos")

# --- MÓDULO 6: SUBIR ARCHIVOS ---
elif menu == "📁 Subir Archivos":
    st.title("Gestión Documental")
    archivo = st.file_uploader("Sube facturas o estados de cuenta", type=["pdf", "xlsx", "csv"])
    if archivo:
        st.success("Archivo listo para procesamiento.")
