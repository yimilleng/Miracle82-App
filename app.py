import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONEXIÓN ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("💎 Miracle 82: Registro Contable")

# --- CARGAR CATÁLOGO (Nombre corregido a catalogo_cuentas) ---
@st.cache_data(ttl=60)
def cargar_datos_catalogo():
    try:
        # Aquí usamos el nombre exacto que Supabase nos confirmó
        res = supabase.table("catalogo_cuentas").select("codigo_cta, nombre_cta").execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        return pd.DataFrame()

df_cat = cargar_datos_catalogo()

# --- FORMULARIO DE REGISTRO ---
with st.container():
    st.subheader("📝 Nueva Partida")
    
    col_a, col_b = st.columns(2)
    f_fecha = col_a.date_input("Fecha", datetime.date.today())
    f_empresa = col_b.text_input("Empresa/Cliente")

    # Si encontramos la tabla, mostramos la lista desplegable
    if not df_cat.empty:
        opciones = [f"{row['codigo_cta']} | {row['nombre_cta']}" for _, row in df_cat.iterrows()]
        seleccion = st.selectbox("Seleccione la Cuenta del Catálogo", opciones)
        
        # Extraemos los datos automáticamente de la selección
        f_cod = seleccion.split(" | ")[0]
        f_nom = seleccion.split(" | ")[1]
    else:
        st.error("⚠️ La tabla 'catalogo_cuentas' no responde. Ingrese datos manual:")
        f_cod = st.text_input("Código")
        f_nom = st.text_input("Nombre de la Cuenta")

    c3, c4 = st.columns(2)
    f_deb = c3.number_input("Debe (Lps)", min_value=0.0, format="%.2f")
    f_hab = c4.number_input("Haber (Lps)", min_value=0.0, format="%.2f")
    f_con = st.text_input("Concepto")

    if st.button("💾 GUARDAR EN LIBRO DIARIO"):
        if f_nom.strip() and (f_deb > 0 or f_hab > 0):
            asiento = {
                "fecha": str(f_fecha),
                "empresa": f_empresa,
                "codigo_cta": f_cod,
                "nombre_cta": f_nom,
                "debe": f_deb,
                "haber": f_hab,
                "concepto": f_con
            }
            try:
                supabase.table("libro_diario").insert(asiento).execute()
                st.success(f"✅ Registrado exitosamente: {f_nom}")
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")
        else:
            st.warning("Seleccione una cuenta y coloque un monto válido.")

# --- TABLA DE RESULTADOS ---
st.divider()
st.subheader("📋 Libro Diario Actualizado")
try:
    res_diario = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
    if res_diario.data:
        df_diario = pd.DataFrame(res_diario.data)
        # Mostramos las columnas con los nombres que ya tienes en tus fotos
        columnas_ver = ["fecha", "codigo_cta", "nombre_cta", "debe", "haber", "concepto"]
        st.dataframe(df_diario[columnas_ver], use_container_width=True)
except:
    st.info("Esperando registros...")
