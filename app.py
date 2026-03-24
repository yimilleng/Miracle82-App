import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- CONEXIÓN SEGURA A SUPABASE ---
# Asegúrate de tener estas llaves en la sección 'Secrets' de Streamlit Cloud
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("⚠️ Error de conexión: Revisa tus 'Secrets' en Streamlit.")
    st.stop()

st.sidebar.title("💎 Miracle 82 ERP")
modulo = st.sidebar.radio("MENÚ", ["🏠 Dashboard", "👥 Clientes (SQL)", "📒 Contabilidad"])

# --- MÓDULO DE CLIENTES CON SQL ---
if modulo == "👥 Clientes (SQL)":
    st.title("Gestión de Clientes en SQL")
    
    # Formulario para insertar datos
    with st.form("registro_cliente", clear_on_submit=True):
        st.subheader("➕ Registrar Nuevo Cliente")
        col1, col2 = st.columns(2)
        with col1:
            rtn = st.text_input("RTN del Cliente")
            nombre = st.text_input("Nombre o Razón Social")
        with col2:
            contacto = st.text_input("Nombre de Contacto")
            tel = st.text_input("Teléfono")
        
        submit = st.form_submit_button("Guardar en Base de Datos")
        
        if submit:
            if rtn and nombre:
                # Datos para enviar a Supabase
                nuevo_cliente = {
                    "rtn": rtn,
                    "nombre_social": nombre,
                    "contacto_principal": contacto,
                    "telefono": tel
                }
                # OPERACIÓN SQL: Insertar fila
                try:
                    supabase.table("clientes").insert(nuevo_cliente).execute()
                    st.success(f"✅ Cliente '{nombre}' guardado exitosamente en SQL.")
                except Exception as err:
                    st.error(f"❌ Error al guardar: {err}")
            else:
                st.warning("Por favor, ingresa al menos el RTN y el Nombre.")

    # Visualización de datos en tiempo real
    st.divider()
    st.subheader("📋 Cartera de Clientes Actual")
    try:
        # OPERACIÓN SQL: Leer datos
        response = supabase.table("clientes").select("*").execute()
        if response.data:
            df_mostrar = pd.DataFrame(response.data)
            st.dataframe(df_mostrar, use_container_width=True)
        else:
            st.info("Aún no hay clientes registrados en la base de datos.")
    except Exception as e:
        st.error(f"No se pudieron cargar los datos: {e}")

# --- MÓDULO DASHBOARD (Resumen) ---
elif modulo == "🏠 Dashboard":
    st.title("Panel General")
    # Aquí podrías hacer un conteo real de clientes usando SQL
    res = supabase.table("clientes").select("id", count="exact").execute()
    total_clientes = res.count if res.count else 0
    st.metric("Clientes Registrados", total_clientes)