import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- CONEXIÓN ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("💎 Prueba de Catálogo Miracle 82")

# --- INTENTO DE LECTURA ---
try:
    # Traemos los datos de la tabla que creaste
    res = supabase.table("catalogo").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success("✅ ¡Conexión exitosa! Catálogo encontrado.")
        # Creamos la lista desplegable
        opciones = [f"{r['codigo_cta']} | {r['nombre_cta']}" for _, r in df.iterrows()]
        seleccion = st.selectbox("Selecciona una cuenta:", opciones)
        
        # Botón de prueba
        if st.button("Probar Registro"):
            st.write(f"Has seleccionado: {seleccion}")
    else:
        st.warning("⚠️ La tabla 'catalogo' está vacía en Supabase.")
except Exception as e:
    st.error(f"❌ Error de conexión: {e}")
    st.info("Revisa si el nombre de la tabla en Supabase es exactamente 'catalogo' (en minúsculas).")
