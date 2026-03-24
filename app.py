import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Miracle 82 ERP", layout="wide")

# --- CONEXIÓN ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("💎 Miracle 82: Registro Contable")

# --- FORMULARIO CON CAPTURA FORZADA ---
with st.container():
    st.subheader("📝 Nueva Partida")
    
    # Campos generales
    col_a, col_b = st.columns(2)
    f_fecha = col_a.date_input("Fecha", datetime.date.today())
    f_empresa = col_b.text_input("Empresa/Cliente", key="empresa")
    
    # Campos de la cuenta
    c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
    # USAMOS KEYS PARA FORZAR LA CAPTURA EN MEMORIA
    f_cod = c1.text_input("Código", key="cod")
    f_nom = c2.text_input("Nombre de la Cuenta", key="nom") 
    f_deb = c3.number_input("Debe", min_value=0.0, format="%.2f", key="deb")
    f_hab = c4.number_input("Haber", min_value=0.0, format="%.2f", key="hab")
    
    f_con = st.text_input("Concepto", key="con")

    if st.button("💾 GUARDAR REGISTRO EN SQL"):
        # Recuperamos los datos directamente de la memoria de la app (session_state)
        val_nombre = st.session_state.nom.strip()
        val_codigo = st.session_state.cod.strip()
        
        if not val_nombre or not val_codigo:
            st.error("❌ ERROR: El nombre y el código de la cuenta son obligatorios.")
        elif st.session_state.deb == 0 and st.session_state.hab == 0:
            st.error("❌ ERROR: Debe ingresar un monto.")
        else:
            # Preparamos el registro
            nuevo_asiento = {
                "fecha": str(f_fecha),
                "empresa": st.session_state.empresa,
                "codigo_cta": val_codigo,
                "nombre_cta": val_nombre, # <--- Enviamos el valor forzado
                "debe": st.session_state.deb,
                "haber": st.session_state.hab,
                "concepto": st.session_state.con
            }
            
            try:
                supabase.table("libro_diario").insert(nuevo_asiento).execute()
                st.success(f"✅ ¡Éxito! Registrada la cuenta: {val_nombre}")
                # Limpiamos manualmente para el siguiente registro
                st.rerun()
            except Exception as e:
                st.error(f"Error de SQL: {e}")

# --- VISUALIZACIÓN ---
st.divider()
st.subheader("📋 Libro Diario Actualizado")
try:
    data = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
    if data.data:
        df = pd.DataFrame(data.data)
        columnas = ["fecha", "empresa", "codigo_cta", "nombre_cta", "debe", "haber", "concepto"]
        st.dataframe(df[columnas], use_container_width=True)
except:
    st.info("Esperando datos...")
