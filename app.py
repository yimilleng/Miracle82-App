import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONEXIÓN SEGURA ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.sidebar.title("💎 Miracle 82 ERP")
modulo = st.sidebar.radio("MENÚ", ["🏠 Dashboard", "👥 Clientes (SQL)", "📒 Contabilidad (SQL)"])

if modulo == "📒 Contabilidad (SQL)":
    st.title("Libro Diario - Registro SQL")
    
    with st.form("form_contable", clear_on_submit=True):
        st.subheader("📝 Nueva Partida")
        
        col_f, col_e, col_c = st.columns([1, 2, 2])
        f_partida = col_f.date_input("Fecha", datetime.date.today())
        e_nombre = col_e.text_input("Empresa/Cliente")
        c_concepto = col_c.text_input("Concepto General")
        
        st.markdown("---")
        c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
        v_codigo = c1.text_input("Código")
        v_nombre = c2.text_input("Nombre de la Cuenta") # <--- ESTE ES EL DATO CRÍTICO
        v_debe = c3.number_input("Debe (L.)", min_value=0.0, step=0.01)
        v_haber = c4.number_input("Haber (L.)", min_value=0.0, step=0.01)
        
        if st.form_submit_button("Guardar Partida"):
            if v_nombre and (v_debe > 0 or v_haber > 0):
                # Diccionario con nombres EXACTOS de las columnas en SQL
                datos_sql = {
                    "fecha": str(f_partida),
                    "empresa": e_nombre,
                    "cuenta_codigo": v_codigo,
                    "cuenta_nombre": v_nombre, # <--- Enviamos 'v_nombre' a 'cuenta_nombre'
                    "debe": v_debe,
                    "haber": v_haber,
                    "concepto": c_concepto
                }
                
                try:
                    supabase.table("libro_diario").insert(datos_sql).execute()
                    st.success(f"✅ Se registró la cuenta: {v_nombre}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error técnico: {e}")
            else:
                st.warning("⚠️ Debes ingresar el nombre de la cuenta y un valor (Debe/Haber).")

    st.subheader("📖 Historial de Movimientos")
    res = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
    if res.data:
        df = pd.DataFrame(res.data)
        # Reordenamos columnas para que se vea mejor
        columnas = ["fecha", "cuenta_codigo", "cuenta_nombre", "debe", "haber", "concepto"]
        st.dataframe(df[columnas], use_container_width=True)
