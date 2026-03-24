import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Miracle 82 ERP", layout="wide", page_icon="💎")

# --- CONEXIÓN A SUPABASE ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.sidebar.title("💎 Miracle 82")
modulo = st.sidebar.radio("MENÚ", ["🏠 Dashboard", "👥 Clientes", "📒 Contabilidad"])

if modulo == "📒 Contabilidad":
    st.title("Registro de Partidas Contables")
    
    with st.form("form_contable", clear_on_submit=True):
        st.subheader("📝 Datos del Asiento")
        c_sup1, c_sup2 = st.columns(2)
        f_fecha = c_sup1.date_input("Fecha", datetime.date.today())
        f_empresa = c_sup2.text_input("Empresa / Cliente (Opcional)")
        
        st.markdown("---")
        st.write("### Detalle de la Cuenta")
        c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
        
        # Usamos variables con nombres claros para evitar errores
        f_codigo = c1.text_input("Código de Cuenta")
        f_nombre = c2.text_input("Nombre de la Cuenta *")
        f_debe = c3.number_input("Debe (Lps)", min_value=0.0, format="%.2f")
        f_haber = c4.number_input("Haber (Lps)", min_value=0.0, format="%.2f")
        
        f_concepto = st.text_input("Concepto / Descripción")
        
        submit = st.form_submit_button("🚀 Guardar Partida en SQL")
        
        if submit:
            # VALIDACIÓN: Antes de enviar, verificamos que el nombre tenga texto real
            nombre_limpio = f_nombre.strip()
            codigo_limpio = f_codigo.strip()
            
            if not nombre_limpio or not codigo_limpio:
                st.error("❌ ERROR: El Código y el Nombre de la cuenta son OBLIGATORIOS.")
            elif f_debe == 0 and f_haber == 0:
                st.error("❌ ERROR: Debe ingresar un monto en el Debe o en el Haber.")
            else:
                # Preparamos el envío exacto
                datos_para_sql = {
                    "fecha": str(f_fecha),
                    "empresa": f_empresa if f_empresa else "General",
                    "cuenta_codigo": codigo_limpio,
                    "cuenta_nombre": nombre_limpio,
                    "debe": f_debe,
                    "haber": f_haber,
                    "concepto": f_concepto if f_concepto else "Sin concepto"
                }
                
                try:
                    supabase.table("libro_diario").insert(datos_para_sql).execute()
                    st.success(f"✅ Se guardó correctamente: {nombre_limpio}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error de base de datos: {e}")

    # --- TABLA DE HISTORIAL ---
    st.divider()
    st.subheader("📖 Movimientos Registrados")
    res = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
    if res.data:
        df = pd.DataFrame(res.data)
        # Reordenamos para que el contador vea lo importante primero
        df_ver = df[["fecha", "empresa", "cuenta_codigo", "cuenta_nombre", "debe", "haber", "concepto"]]
        st.dataframe(df_ver, use_container_width=True)

else:
    st.title("Bienvenido a Miracle 82")
    st.write("Selecciona un módulo en el menú de la izquierda para comenzar.")
