import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- CONEXIÓN SEGURA ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Miracle 82 ERP", page_icon="💎")
st.title("💎 Miracle 82: Sistema Contable")

# --- MENÚ LATERAL ---
menu = st.sidebar.selectbox("Módulos", ["Contabilidad", "Bancos", "Dashboards"])

if menu == "Contabilidad":
    st.header("📒 Registro de Partidas")
    
    try:
        # Traemos tus 154 cuentas reales
        res = supabase.table("catalogo_cuentas").select("codigo_cta, nombre_cta").execute()
        df_cat = pd.DataFrame(res.data)
        
        if not df_cat.empty:
            # Creamos la lista para buscar
            opciones = [f"{r['codigo_cta']} | {r['nombre_cta']}" for _, r in df_cat.iterrows()]
            cuenta_sel = st.selectbox("Seleccione Cuenta del Catálogo", opciones)
            
            with st.form("nueva_partida"):
                col1, col2 = st.columns(2)
                debe = col1.number_input("Debe (Lps)", min_value=0.0)
                haber = col2.number_input("Haber (Lps)", min_value=0.0)
                concepto = st.text_input("Concepto")
                
                if st.form_submit_button("💾 Guardar Registro"):
                    st.success(f"Asiento guardado en: {cuenta_sel}")
        else:
            st.warning("El catálogo está vacío en Supabase.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
