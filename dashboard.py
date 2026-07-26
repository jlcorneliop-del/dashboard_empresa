import streamlit as st 
from conexion import cargar_datos
from indicadores import *
from graficos import *

# 1. CONFIGURACIÓN GERENCIAL DE PÁGINA
st.set_page_config(
    page_title="Informe Gerencial - Wigo Motors",
    page_icon="📊",
    layout="wide"
)

# 2. FUNCIÓN DE LOGIN
def login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if st.session_state.autenticado:
        return True

    st.title("🔒 Acceso al Sistema Gerencial")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario == "javier" and password == "javier":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

    return False

if not login():
    st.stop()

# ==============================================================================
# INFORME GERENCIAL - WIGO MOTORS S.A.C.
# ==============================================================================

df = cargar_datos()

# ------------------------------------------------------------------------------
# FILTROS GERENCIALES (BARRA LATERAL)
# ------------------------------------------------------------------------------
st.sidebar.title("📌 Filtros de Control")

marcas = ["Todas"] + list(df["marca"].dropna().unique())
marca_sel = st.sidebar.selectbox("Marca:", marcas)

sedes = ["Todas"] + list(df["tienda"].dropna().unique())
sede_sel = st.sidebar.selectbox("Sede / Tienda:", sedes)

asesores = ["Todos"] + list(df["asesor_comercial"].dropna().unique())
asesor_sel = st.sidebar.selectbox("Asesor Comercial:", asesores)

precio_min = float(df["precio_venta"].min())
precio_max = float(df["precio_venta"].max())

rango_precio = st.sidebar.slider(
    "Rango Presupuestario (S/):",
    min_value=precio_min,
    max_value=precio_max,
    value=(precio_min, precio_max),
    step=1000.0,
    format="S/%d"
)

st.sidebar.write("---")
if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.autenticado = False
    st.rerun()

# Lógica de Filtrado
df_filtrado = df.copy()

if marca_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["marca"] == marca_sel]

if sede_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["tienda"] == sede_sel]

if asesor_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["asesor_comercial"] == asesor_sel]

df_filtrado = df_filtrado[
    (df_filtrado["precio_venta"] >= rango_precio[0]) & 
    (df_filtrado["precio_venta"] <= rango_precio[1])
]

# ------------------------------------------------------------------------------
# ENCABEZADO DE INFORME EJECUTIVO
# ------------------------------------------------------------------------------
st.title("🏛️ WIGO MOTORS S.A.C.")
st.caption("Reporte Ejecutivo de Desempeño Comercial y Ventas")

# RESUMEN METRICO (TARJETAS GERENCIALES)
st.markdown("### 📈 Indicadores Clave de Rendimiento (KPIs)")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric("Ingresos Totales", f"S/ {precio_total(df_filtrado):,.2f}")
kpi2.metric("Unidades Vendidas", f"{unidades_vendidas(df_filtrado)} u.")
kpi3.metric("Ticket Promedio", f"S/ {precio_promedio(df_filtrado):,.2f}")
kpi4.metric("Operaciones", f"{operaciones(df_filtrado)}")
kpi5.metric("Precio Máx. Venta", f"S/ {precio_maximo(df_filtrado):,.2f}")

st.write("---")

# ------------------------------------------------------------------------------
# PESTAÑAS DEL INFORME (TABS)
# ------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Visión General", "🎯 Análisis Comercial", "📋 Registro de Datos"])

with tab1:
    st.subheader("Resumen de Desempeño Operativo")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grafico_ventas(df_filtrado), use_container_width=True)
    with col2:
        st.plotly_chart(grafico_sedes(df_filtrado), use_container_width=True)

with tab2:
    st.subheader("Análisis de Precios y Financiamiento")
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(grafico_promedio(df_filtrado), use_container_width=True)
    with col4:
        st.plotly_chart(grafico_metodo_pago(df_filtrado), use_container_width=True)

with tab3:
    st.subheader("Detalle Consolidado de Ventas")
    st.info(f"Se muestran **{len(df_filtrado)}** registros coincidentes con los criterios seleccionados.")
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)