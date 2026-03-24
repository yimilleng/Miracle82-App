import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONEXIÓN ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("💎 Miracle 82: Registro Contable")

# --- INTENTAR CARGAR EL CATÁLOGO ---
@st.cache_data(ttl=600)
def cargar_catalogo():
    try:
        res = supabase.table("catalogo_cuentas").select("codigo_cta, nombre_cta").execute()
        return pd.DataFrame(res.data)
    except:
        return pd.DataFrame()

df_cat = cargar_catalogo()

# --- FORMULARIO DE REGISTRO ---
with st.container():
    st.subheader("📝 Nueva Partida")
    
    col_a, col_b = st.columns(2)
    f_fecha = col_a.date_input("Fecha", datetime.date.today())
    f_empresa = col_b.text_input("Empresa/Cliente")

    # SI HAY CATÁLOGO, USAMOS SELECTBOX (LISTA)
    if not df_cat.empty:
        opciones = [f"{row['codigo_cta']} | {row['nombre_cta']}" for _, row in df_cat.iterrows()]
        seleccion = st.selectbox("Seleccione la Cuenta", opciones)
        # Extraemos los datos de la selección
        f_cod = seleccion.split(" | ")[0]
        f_nom = seleccion.split(" | ")[1]
    else:
        st.warning("⚠️ No se detectó catálogo en SQL. Ingrese datos manualmente:")
        f_cod = st.text_input("Código de Cuenta")
        f_nom = st.text_input("Nombre de la Cuenta")

    c3, c4 = st.columns(2)
    f_deb = c3.number_input("Debe (Lps)", min_value=0.0, format="%.2f")
    f_hab = c4.number_input("Haber (Lps)", min_value=0.0, format="%.2f")
    f_con = st.text_input("Concepto de la Partida")

    if st.button("💾 GUARDAR EN LIBRO DIARIO"):
        if f_nom.strip() and (f_deb > 0 or f_hab > 0):
            nuevo_asiento = {
                "fecha": str(f_fecha),
                "empresa": f_empresa,
                "codigo_cta": f_cod,
                "nombre_cta": f_nom,
                "debe": f_deb,
                "haber": f_hab,
                "concepto": f_con
            }
            try:
                supabase.table("libro_diario").insert(nuevo_asiento).execute()
                st.success(f"✅ Registrado: {f_nom}")
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")
        else:
            st.error("❌ Verifique el nombre de la cuenta y los montos.")

# --- HISTORIAL ---
st.divider()
st.subheader("📋 Movimientos en SQL")
try:
    data = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
    if data.data:
        st.dataframe(pd.DataFrame(data.data)[["fecha", "codigo_cta", "nombre_cta", "debe", "haber", "concepto"]], use_container_width=True)
except:
    st.info("Aún no hay registros.")
