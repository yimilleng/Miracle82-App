import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Miracle 82 ERP", layout="wide")

# --- CONEXIÓN ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.sidebar.title("💎 Miracle 82")
opcion = st.sidebar.radio("MENÚ", ["Dashboard", "Contabilidad"])

if opcion == "Contabilidad":
    st.title("Libro Diario Profesional")
    
    with st.form("form_final", clear_on_submit=True):
        st.subheader("Nueva Partida")
        
        c_top1, c_top2 = st.columns(2)
        fecha_input = c_top1.date_input("Fecha", datetime.date.today())
        empresa_input = c_top2.text_input("Empresa")
        
        st.markdown("---")
        c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
        
        # Variables con nombres únicos
        cod_data = c1.text_input("Código")
        nom_data = c2.text_input("Nombre de la Cuenta")
        debe_data = c3.number_input("Debe", min_value=0.0)
        habe_data = c4.number_input("Haber", min_value=0.0)
        
        con_data = st.text_input("Concepto General")
        
        if st.form_submit_button("Guardar en SQL"):
            # Quitamos espacios y validamos
            txt_nombre = nom_data.strip()
            txt_codigo = cod_data.strip()
            
            if not txt_nombre or not txt_codigo:
                st.error("❌ El CÓDIGO y el NOMBRE son obligatorios.")
            elif debe_data == 0 and habe_data == 0:
                st.error("❌ El monto no puede ser cero.")
            else:
                # MAPEO DIRECTO A LAS NUEVAS COLUMNAS SIMPLIFICADAS
                registro = {
                    "fecha": str(fecha_input),
                    "empresa": empresa_input,
                    "codigo": txt_codigo,
                    "cuenta": txt_nombre, # <--- Enviamos a la columna 'cuenta'
                    "debe": debe_data,
                    "haber": habe_data,
                    "concepto": con_data
                }
                
                try:
                    # Intento de inserción
                    supabase.table("libro_diario").insert(registro).execute()
                    st.success(f"✅ Guardado: {txt_nombre}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error técnico: {e}")

    # --- VISUALIZACIÓN ---
    st.divider()
    st.subheader("Registros en SQL")
    res = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
    if res.data:
        df = pd.DataFrame(res.data)
        # Seleccionamos las columnas con los nuevos nombres
        st.dataframe(df[["fecha", "empresa", "codigo", "cuenta", "debe", "haber", "concepto"]], use_container_width=True)

else:
    st.write("Seleccione Contabilidad en el menú.")
