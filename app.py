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

st.sidebar.title("💎 Miracle 82")
modulo = st.sidebar.radio("MENÚ", ["🏠 Dashboard", "👥 Clientes", "📒 Contabilidad"])

if modulo == "📒 Contabilidad":
    st.title("Registro de Partidas Contables")
    
    with st.form("form_contable", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        f_fecha = col_a.date_input("Fecha de la Partida", datetime.date.today())
        f_empresa = col_b.text_input("Nombre de la Empresa / Cliente")
        
        st.markdown("---")
        c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
        f_codigo = c1.text_input("Código de Cuenta (Ej: 1101)")
        f_nombre = c2.text_input("Nombre de la Cuenta (Ej: Caja General)")
        f_debe = c3.number_input("Debe (Lps)", min_value=0.0, format="%.2f")
        f_haber = c4.number_input("Haber (Lps)", min_value=0.0, format="%.2f")
        
        f_concepto = st.text_input("Concepto o Descripción del movimiento")
        
        if st.form_submit_button("🚀 Guardar en Base de Datos"):
            # VALIDACIÓN ESTRICTA
            if not f_nombre or not f_codigo:
                st.error("❌ ERROR: El Código y el Nombre de la Cuenta son obligatorios.")
            elif f_debe == 0 and f_haber == 0:
                st.error("❌ ERROR: El monto no puede ser cero en ambos campos.")
            else:
                datos = {
                    "fecha": str(f_fecha),
                    "empresa": f_empresa,
                    "cuenta_codigo": f_codigo,
                    "cuenta_nombre": f_nombre.strip(),
                    "debe": f_debe,
                    "haber": f_haber,
                    "concepto": f_concepto
                }
                
                try:
                    supabase.table("libro_diario").insert(datos).execute()
                    st.success(f"✅ Registrado exitosamente: {f_nombre}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error técnico de SQL: {e}")

    # Visualización de los datos registrados
    st.divider()
    st.subheader("📖 Historial del Libro Diario")
    res = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
    if res.data:
        df = pd.DataFrame(res.data)
        columnas_ordenadas = ["fecha", "empresa", "cuenta_codigo", "cuenta_nombre", "debe", "haber", "concepto"]
        st.dataframe(df[columnas_ordenadas], use_container_width=True)

else:
    st.title("Panel Principal")
    st.write("Bienvenido al sistema contable de Miracle 82. Selecciona un módulo en la izquierda.")
