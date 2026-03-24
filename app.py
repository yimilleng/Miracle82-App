import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONEXIÓN SEGURA ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("💎 Miracle 82: Gestión Contable")

# --- CARGAR EL CATÁLOGO DESDE SQL ---
def obtener_catalogo():
    try:
        # Traemos los códigos y nombres de la tabla que acabas de crear
        res = supabase.table("catalogo").select("codigo_cta, nombre_cta").execute()
        return pd.DataFrame(res.data)
    except:
        return pd.DataFrame()

df_cat = obtener_catalogo()

# --- FORMULARIO DE REGISTRO ---
with st.form("registro_p", clear_on_submit=True):
    st.subheader("📝 Nueva Partida")
    
    c_top1, c_top2 = st.columns(2)
    f_fecha = c_top1.date_input("Fecha", datetime.date.today())
    f_empresa = c_top2.text_input("Empresa/Cliente")
    
    st.markdown("---")
    
    # Aquí es donde usamos el catálogo que ya creaste
    if not df_cat.empty:
        # Creamos la lista: "1110101001 | Caja General"
        opciones = [f"{row['codigo_cta']} | {row['nombre_cta']}" for _, row in df_cat.iterrows()]
        seleccion = st.selectbox("Seleccione la Cuenta", opciones)
        
        # Separamos los datos para enviarlos a la tabla libro_diario
        f_cod = seleccion.split(" | ")[0]
        f_nom = seleccion.split(" | ")[1]
    else:
        st.error("⚠️ No se encontró el catálogo en SQL. Verifica la tabla 'catalogo'.")
        f_cod = ""
        f_nom = ""

    c3, c4 = st.columns(2)
    f_deb = c3.number_input("Debe (Lps)", min_value=0.0, format="%.2f")
    f_hab = c4.number_input("Haber (Lps)", min_value=0.0, format="%.2f")
    
    f_con = st.text_input("Concepto o Descripción")
    
    if st.form_submit_button("💾 GUARDAR PARTIDA"):
        if f_nom and (f_deb > 0 or f_hab > 0):
            nuevo_registro = {
                "fecha": str(f_fecha),
                "empresa": f_empresa,
                "codigo_cta": f_cod,
                "nombre_cta": f_nom,
                "debe": f_deb,
                "haber": f_hab,
                "concepto": f_con
            }
            try:
                supabase.table("libro_diario").insert(nuevo_registro).execute()
                st.success(f"✅ Partida de '{f_nom}' guardada exitosamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")
        else:
            st.warning("Asegúrate de seleccionar una cuenta y que el monto sea mayor a 0.")

# --- VISUALIZACIÓN DEL LIBRO DIARIO ---
st.divider()
st.subheader("📖 Movimientos Registrados")
try:
    data_sql = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
    if data_sql.data:
        df_ver = pd.DataFrame(data_sql.data)
        # Mostramos solo las columnas que nos interesan en orden
        cols = ["fecha", "empresa", "codigo_cta", "nombre_cta", "debe", "haber", "concepto"]
        st.dataframe(df_ver[cols], use_container_width=True)
except:
    st.info("Esperando registros...")
