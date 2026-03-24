import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Miracle 82 ERP", layout="wide")

# --- CONEXIÓN ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except:
    st.error("Error en Secrets")
    st.stop()

st.sidebar.title("💎 Miracle 82")
opcion = st.sidebar.radio("MENÚ", ["Contabilidad"])

if opcion == "Contabilidad":
    st.title("Registro Contable Real-Time")
    
    with st.form("form_contabilidad_v3", clear_on_submit=True):
        f_fecha = st.date_input("Fecha", datetime.date.today())
        f_empresa = st.text_input("Empresa/Cliente")
        
        c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
        f_codigo = c1.text_input("Código")
        f_nombre = c2.text_input("Nombre de la Cuenta") # <--- CAMPO CRÍTICO
        f_debe = c3.number_input("Debe", min_value=0.0)
        f_haber = c4.number_input("Haber", min_value=0.0)
        
        f_concepto = st.text_input("Concepto")
        
        if st.form_submit_button("💾 GUARDAR EN SQL"):
            # 1. Capturamos y limpiamos los datos
            dato_nombre = str(f_nombre).strip()
            dato_codigo = str(f_codigo).strip()
            
            # 2. Validación manual antes de enviar
            if not dato_nombre or dato_nombre == "":
                st.error("❌ El nombre de la cuenta llegó vacío al servidor.")
            elif not dato_codigo:
                st.error("❌ El código es obligatorio.")
            else:
                # 3. Mapeo EXACTO a la nueva tabla
                registro = {
                    "fecha": str(f_fecha),
                    "empresa": f_empresa,
                    "codigo_cta": dato_codigo,
                    "nombre_cta": dato_nombre, # <--- Usando el nuevo nombre de columna
                    "debe": f_debe,
                    "haber": f_haber,
                    "concepto": f_concepto
                }
                
                try:
                    # Intento de inserción con reporte
                    response = supabase.table("libro_diario").insert(registro).execute()
                    st.success(f"✅ Se guardó: {dato_nombre}")
                    st.balloons() # Animación para confirmar éxito
                    st.rerun()
                except Exception as e:
                    st.error(f"Error de SQL: {e}")

    # --- TABLA ---
    st.divider()
    try:
        data_sql = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
        if data_sql.data:
            df = pd.DataFrame(data_sql.data)
            # Mostramos las columnas nuevas
            columnas_finales = ["fecha", "empresa", "codigo_cta", "nombre_cta", "debe", "haber", "concepto"]
            st.dataframe(df[columnas_finales], use_container_width=True)
    except:
        st.info("Esperando primer registro...")
