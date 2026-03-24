import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# --- CONEXIÓN SEGURA ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.sidebar.title("💎 Miracle 82 ERP")
modulo = st.sidebar.radio("MENÚ", ["🏠 Dashboard", "👥 Clientes (SQL)", "📒 Contabilidad (SQL)"])

# --- MÓDULO: CLIENTES ---
if modulo == "👥 Clientes (SQL)":
    st.title("Gestión de Clientes")
    with st.form("registro_cliente", clear_on_submit=True):
        st.subheader("➕ Nuevo Cliente")
        rtn = st.text_input("RTN")
        nombre = st.text_input("Nombre Social")
        if st.form_submit_button("Guardar Cliente"):
            supabase.table("clientes").insert({"rtn": rtn, "nombre_social": nombre}).execute()
            st.success("Cliente guardado")
            st.rerun()

# --- MÓDULO: CONTABILIDAD ---
elif modulo == "📒 Contabilidad (SQL)":
    st.title("Libro Diario General")
    
    with st.form("nueva_partida", clear_on_submit=True):
        st.subheader("📝 Registrar Asiento Contable")
        col1, col2, col3 = st.columns([1, 2, 2])
        fecha = col1.date_input("Fecha", datetime.date.today())
        empresa = col2.text_input("Empresa/Cliente")
        concepto = col3.text_input("Concepto de la Partida")
        
        c1, c2, c3, c4 = st.columns(4)
        cod = c1.text_input("Código Cuenta")
        nom = c2.text_input("Nombre Cuenta")
        debe = c3.number_input("Debe (L.)", min_value=0.0)
        haber = c4.number_input("Haber (L.)", min_value=0.0)
        
        if st.form_submit_button("Postear Partida en SQL"):
            if (debe > 0 or haber > 0) and nom:
                nueva_fila = {
                    "fecha": str(fecha),
                    "empresa": empresa,
                    "cuenta_codigo": cod,
                    "cuenta_nombre": nom,
                    "debe": debe,
                    "haber": haber,
                    "concepto": concepto
                }
                supabase.table("libro_diario").insert(nueva_fila).execute()
                st.success("✅ Partida registrada correctamente.")
                st.rerun()
            else:
                st.error("Revisa los montos y el nombre de la cuenta.")

    st.divider()
    st.subheader("📖 Historial de Movimientos")
    res = supabase.table("libro_diario").select("*").order("created_at", desc=True).execute()
    if res.data:
        st.dataframe(pd.DataFrame(res.data), use_container_width=True)

# --- DASHBOARD ---
elif modulo == "🏠 Dashboard":
    st.title("Resumen de Miracle 82")
    res_c = supabase.table("clientes").select("id", count="exact").execute()
    res_p = supabase.table("libro_diario").select("id", count="exact").execute()
    
    col1, col2 = st.columns(2)
    col1.metric("Total Clientes", res_c.count if res_c.count else 0)
    col2.metric("Partidas Registradas", res_p.count if res_p.count else 0)
