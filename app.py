import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONFIGURACIÓN PRO ---
st.set_page_config(page_title="Miracle 82 ERP", layout="wide", page_icon="💎")

# --- CONEXIÓN ---
@st.cache_resource
def init_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_connection()

# --- NAVEGACIÓN ---
st.sidebar.title("💎 Miracle 82 ERP")
menu = st.sidebar.selectbox(
    "Seleccione Módulo",
    ["📊 Dashboards", "📒 Contabilidad", "🏦 Bancos", "👥 Clientes", "🚚 Proveedores", "📁 Subir Archivos"]
)

# --- MÓDULO 1: DASHBOARDS ---
if menu == "📊 Dashboards":
    st.title("Panel de Control Financiero")
    c1, c2, c3 = st.columns(3)
    c1.metric("Ventas Mes", "L. 45,200.00", "+12%")
    c2.metric("Cuentas por Cobrar", "L. 12,800.00", "-5%")
    c3.metric("Disponibilidad Bancos", "L. 85,000.00")
    
    st.markdown("### Resumen de Gastos")
    chart_data = pd.DataFrame({"Categoría": ["Salarios", "Renta", "Servicios"], "Monto": [20000, 8000, 3500]})
    st.bar_chart(chart_data.set_index("Categoría"))

# --- MÓDULO 2: CONTABILIDAD ---
elif menu == "📒 Contabilidad":
    st.title("Módulo Contable")
    tab1, tab2 = st.tabs(["Registro de Partida", "Historial Diario"])
    
    with tab1:
        with st.form("form_contable", clear_on_submit=True):
            col1, col2 = st.columns(2)
            f_fecha = col1.date_input("Fecha", datetime.date.today())
            f_emp = col2.text_input("Empresa/Cliente")
            
            # Carga automática del catálogo que ya arreglamos
            try:
                res_cat = supabase.table("catalogo_cuentas").select("*").execute()
                df_cat = pd.DataFrame(res_cat.data)
                opciones = [f"{r['codigo_cta']} | {r['nombre_cta']}" for _, r in df_cat.iterrows()]
                sel = st.selectbox("Cuenta del Catálogo", opciones)
                f_cod, f_nom = sel.split(" | ")
            except:
                st.error("Error cargando catálogo. Verifique tabla 'catalogo_cuentas'.")
                f_cod, f_nom = "", ""

            c3, c4 = st.columns(2)
            f_deb = c3.number_input("Debe (Lps)", min_value=0.0)
            f_hab = c4.number_input("Haber (Lps)", min_value=0.0)
            f_con = st.text_area("Concepto")

            if st.form_submit_button("💾 Guardar en Libro Diario"):
                if f_nom and (f_deb > 0 or f_hab > 0):
                    data = {"fecha": str(f_fecha), "empresa": f_emp, "codigo_cta": f_cod, 
                            "nombre_cta": f_nom, "debe": f_deb, "haber": f_hab, "concepto": f_con}
                    supabase.table("libro_diario").insert(data).execute()
                    st.success("Asiento guardado.")
                    st.rerun()

# --- MÓDULO 3: BANCOS ---
elif menu == "🏦 Bancos":
    st.title("Gestión de Tesorería")
    st.info("Módulo para conciliaciones bancarias y control de flujos.")
    st.selectbox("Seleccione Banco", ["BAC", "Ficohsa", "Banpais", "Occidente"])
    st.button("Conciliar Movimientos")

# --- MÓDULO 4: CLIENTES ---
elif menu == "👥 Clientes":
    st.title("Administración de Clientes")
    st.text_input("Buscar Cliente por RTN o Nombre")
    st.button("➕ Registrar Nuevo Cliente")

# --- MÓDULO 5: PROVEEDORES ---
elif menu == "🚚 Proveedores":
    st.title("Cuentas por Pagar")
    st.write("Control de facturas de proveedores y fechas de vencimiento.")

# --- MÓDULO 6: SUBIR ARCHIVOS ---
elif menu == "📁 Subir Archivos":
    st.title("Carga de Documentos")
    st.write("Sube facturas (PDF), planillas (Excel) o fotos de comprobantes.")
    archivo = st.file_uploader("Arrastra tus archivos aquí", type=["pdf", "xlsx", "png", "jpg"])
    if archivo:
        st.success(f"Archivo '{archivo.name}' recibido.")
