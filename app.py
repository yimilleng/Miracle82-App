import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- CONEXIÓN ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("💎 Miracle 82 - Control Total")

# --- LECTURA DIRECTA (SIN CACHÉ) ---
st.subheader("📝 Registro de Partida")

try:
    # Intentamos leer la tabla que acabamos de crear en el Paso 1
    res = supabase.table("catalogo_cuentas").select("*").execute()
    df_cat = pd.DataFrame(res.data)
    
    if not df_cat.empty:
        # Si hay datos, creamos la lista desplegable
        opciones = [f"{r['codigo_cta']} | {r['nombre_cta']}" for _, r in df_cat.iterrows()]
        seleccion = st.selectbox("Seleccione la Cuenta del Catálogo", opciones)
        
        # Separar datos
        f_cod = seleccion.split(" | ")[0]
        f_nom = seleccion.split(" | ")[1]
        
        # Formulario de montos
        f_empresa = st.text_input("Empresa / Cliente")
        c1, c2 = st.columns(2)
        f_deb = c1.number_input("Debe (Lps)", min_value=0.0)
        f_hab = c2.number_input("Haber (Lps)", min_value=0.0)
        f_con = st.text_input("Concepto")

        if st.button("💾 GUARDAR REGISTRO"):
            if f_deb > 0 or f_hab > 0:
                datos = {
                    "fecha": "2026-03-23", # Fecha fija para prueba
                    "empresa": f_empresa,
                    "codigo_cta": f_cod,
                    "nombre_cta": f_nom,
                    "debe": f_deb,
                    "haber": f_hab,
                    "concepto": f_con
                }
                supabase.table("libro_diario").insert(datos).execute()
                st.success(f"✅ Guardado con éxito: {f_nom}")
                st.rerun()
            else:
                st.error("El monto debe ser mayor a 0")
    else:
        st.error("⚠️ La tabla 'catalogo_cuentas' existe pero no tiene datos.")
except Exception as e:
    st.error(f"❌ Error de conexión: {e}")
    st.info("Asegúrate de haber corrido el SQL del Paso 1.")

# --- TABLA DE RESULTADOS ---
st.divider()
try:
    res_d = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
    if res_d.data:
        st.write("### Historial Reciente")
        st.dataframe(pd.DataFrame(res_d.data)[["codigo_cta", "nombre_cta", "debe", "haber"]], use_container_width=True)
except:
    pass
