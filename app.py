import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS ---
st.set_page_config(page_title="Miracle 82 ERP", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #004d2c; }
    [data-testid="stSidebar"] * { color: white; }
    .stMetric { background-color: #ffffff; border-left: 5px solid #d4af37; padding: 10px; border-radius: 5px; box-shadow: 1px 1px 5px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #004d2c; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN SEGURA A SQL (SUPABASE) ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("⚠️ Error: No se encontraron las credenciales en Streamlit Secrets.")
    st.stop()

# --- 3. NAVEGACIÓN LATERAL ---
st.sidebar.title("💎 Miracle 82 ERP")
st.sidebar.write("Sesión: Administrador")
modulo = st.sidebar.radio("MENÚ PRINCIPAL", [
    "🏠 Dashboard", 
    "👥 Clientes (SQL)", 
    "📒 Contabilidad (SQL)",
    "🏦 Bancos",
    "👷 Nóminas"
])

# --- MÓDULO: DASHBOARD ---
if modulo == "🏠 Dashboard":
    st.title("Panel de Control - Miracle 82")
    
    # Resumen rápido desde la DB
    c_count = supabase.table("clientes").select("id", count="exact").execute()
    p_count = supabase.table("libro_diario").select("id", count="exact").execute()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes Activos", c_count.count if c_count.count else 0)
    col2.metric("Asientos Contables", p_count.count if p_count.count else 0)
    col3.metric("Estado de Conexión", "SQL Activo")

# --- MÓDULO: CLIENTES ---
elif modulo == "👥 Clientes (SQL)":
    st.title("Gestión de Clientes")
    
    with st.form("nuevo_cliente", clear_on_submit=True):
        st.subheader("➕ Registrar Cliente")
        c1, c2 = st.columns(2)
        rtn_val = c1.text_input("RTN")
        nombre_val = c2.text_input("Razón Social")
        if st.form_submit_button("Guardar Cliente"):
            if rtn_val and nombre_val:
                supabase.table("clientes").insert({"rtn": rtn_val, "nombre_social": nombre_val}).execute()
                st.success("✅ Cliente guardado.")
                st.rerun()

    st.divider()
    res = supabase.table("clientes").select("*").execute()
    if res.data:
        st.write("### Cartera de Clientes")
        st.dataframe(pd.DataFrame(res.data), use_container_width=True)

# --- MÓDULO: CONTABILIDAD (EL CORAZÓN) ---
elif modulo == "📒 Contabilidad (SQL)":
    st.title("Libro Diario General")
    
    with st.form("registro_contable", clear_on_submit=True):
        st.subheader("📝 Nueva Partida")
        
        # Fila 1: Datos Generales
        f1, f2, f3 = st.columns([1, 2, 2])
        fecha_p = f1.date_input("Fecha", datetime.date.today())
        empresa_p = f2.text_input("Empresa/Proyecto")
        concepto_p = f3.text_input("Concepto General")
        
        st.markdown("---")
        # Fila 2: Datos de la Cuenta (Aquí corregimos el error del nombre)
        d1, d2, d3, d4 = st.columns([1, 2, 1, 1])
        cod_c = d1.text_input("Código de Cuenta")
        nom_c = d2.text_input("Nombre de la Cuenta *") # Campo Obligatorio
        debe_p = d3.number_input("Debe (Lps)", min_value=0.0, format="%.2f")
        haber_p = d4.number_input("Haber (Lps)", min_value=0.0, format="%.2f")
        
        enviar = st.form_submit_button("📦 Postear Partida en SQL")
        
        if enviar:
            # LIMPIEZA Y VALIDACIÓN
            nombre_final = nom_c.strip()
            
            if not nombre_final:
                st.error("❌ ERROR: El nombre de la cuenta no puede estar vacío.")
            elif debe_p == 0 and haber_p == 0:
                st.error("❌ ERROR: Debe ingresar un monto en Debe o Haber.")
            else:
                # Mapeo exacto a las columnas de Supabase
                datos = {
                    "fecha": str(fecha_p),
                    "empresa": empresa_p,
                    "cuenta_codigo": cod_c,
                    "cuenta_nombre": nombre_final, # <--- Se envía limpio
                    "debe": debe_p,
                    "haber": haber_p,
                    "concepto": concepto_p
                }
                
                try:
                    supabase.table("libro_diario").insert(datos).execute()
                    st.success(f"✅ Partida guardada: {nombre_final}")
                    st.rerun()
                except Exception as err:
                    st.error(f"Error al guardar en SQL: {err}")

    # Visualización del Libro
    st.divider()
    st.subheader("📖 Movimientos Recientes")
    query = supabase.table("libro_diario").select("*").order("created_at", desc=True).limit(50).execute()
    if query.data:
        df_diario = pd.DataFrame(query.data)
        # Mostrar solo columnas relevantes
        cols_mostrar = ["fecha", "empresa", "cuenta_codigo", "cuenta_nombre", "debe", "haber", "concepto"]
        st.dataframe(df_diario[cols_mostrar], use_container_width=True)

# --- OTROS MÓDULOS (ESTRUCTURA) ---
else:
    st.title(modulo)
    st.info("Módulo en desarrollo para la siguiente fase de Miracle 82.")
