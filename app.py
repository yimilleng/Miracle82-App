import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- CONEXIÓN ---
# Asegúrate de que en Streamlit Cloud > Settings > Secrets tengas:
# SUPABASE_URL = "tu_url"
# SUPABASE_KEY = "tu_key"
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.sidebar.title("💎 Miracle 82 ERP")
# AQUÍ ES DONDE SE CREA EL MENÚ
modulo = st.sidebar.radio("MENÚ", ["🏠 Dashboard", "👥 Clientes (SQL)"])

if modulo == "👥 Clientes (SQL)":
    st.title("Gestión de Clientes en SQL")
    
    # ESTO CREA EL FORMULARIO PARA CREAR CLIENTES
    with st.form("registro_cliente", clear_on_submit=True):
        st.subheader("➕ Registrar Nuevo Cliente")
        rtn = st.text_input("RTN del Cliente")
        nombre = st.text_input("Nombre o Razón Social")
        contacto = st.text_input("Nombre de Contacto")
        tel = st.text_input("Teléfono")
        
        # EL BOTÓN PARA GUARDAR
        btn_guardar = st.form_submit_button("Guardar en Base de Datos SQL")
        
        if btn_guardar:
            if rtn and nombre:
                nuevo = {"rtn": rtn, "nombre_social": nombre, "contacto_principal": contacto, "telefono": tel}
                supabase.table("clientes").insert(nuevo).execute()
                st.success(f"✅ Cliente {nombre} guardado en SQL")
                st.rerun() # Refresca para mostrarlo en la tabla
            else:
                st.error("RTN y Nombre son obligatorios")

    # ESTO MUESTRA LA LISTA DE CLIENTES QUE YA ESTÁN EN SQL
    st.divider()
    st.subheader("📋 Lista de Clientes")
    res = supabase.table("clientes").select("*").execute()
    if res.data:
        st.dataframe(pd.DataFrame(res.data))
