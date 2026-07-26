import streamlit as st 
from conexion import cargar_datos
from indicadores import *
from graficos import *

# 1. CONFIGURACIÓN INICIAL DE PÁGINA (Siempre debe ir primero)
st.set_page_config(page_title="Wigo Motors", layout="wide")

# 2. FUNCIÓN DE LOGIN
def login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if st.session_state.autenticado:
        return True

    st.title("🔒 Inicio de Sesión")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario == "javier" and password == "javier":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

    return False

# 3. CONTROL DE ACCESO
if not login():
    st.stop()  # Detiene la ejecución si no ha ingresado usuario y contraseña correctos

# ==============================================================================
# DASHBOARD DE WIGO MOTORS (Solo visible después de loguearse)
# ==============================================================================

# Botón para cerrar sesión en la barra lateral
with st.sidebar:
    st.write("---")
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

df = cargar_datos()  # UTILIZANDO LA FUNCIÓN QUE NOS DEVUELVE EL DATAFRAME (DF)

st.title("WIGO MOTORS S.A.C.")                      
st.subheader("Buscador comercial") 

st.sidebar.header("Buscador")
tipo_busqueda = st.sidebar.selectbox("Seleccione tipo de búsqueda", ["Marca", "Asesor comercial", "Sede"])   

df_filtrado = df.copy()  # Haciendo una copia del DataFrame 


# FILTRO POR MARCA / ASESOR / SEDE:

if tipo_busqueda == "Marca":
    valor = st.sidebar.selectbox("Seleccionar marca", df["marca"].unique())
    df_filtrado = df[df["marca"] == valor]
    
elif tipo_busqueda == "Asesor comercial":
    valor = st.sidebar.selectbox("Seleccionar asesor", df["asesor_comercial"].unique())
    df_filtrado = df[df["asesor_comercial"] == valor]
    
elif tipo_busqueda == "Sede":
    valor = st.sidebar.selectbox("Seleccionar sede", df["tienda"].unique())
    df_filtrado = df[df["tienda"] == valor]


# MOSTRAR RESULTADOS (TABLA):

st.success(f"Registros encontrados: {len(df_filtrado)}")
st.dataframe(df_filtrado)


# INDICADORES GENERALES: 

st.subheader("Indicadores:")

c1, c2, c3, c4 = st.columns(4)        

c1.metric("Precio Total", f"S/{precio_total(df_filtrado):,.2f}")          
c2.metric("Unidades vendidas", f"{unidades_vendidas(df_filtrado)}")                
c3.metric("Precio promedio", f"S/{precio_promedio(df_filtrado):,.2f}")     
c4.metric("Operaciones", operaciones(df_filtrado))                                          

c5, c6, c7, c8 = st.columns(4)  

c5.metric("Precio más alto", f"S/{precio_maximo(df_filtrado):,.2f}")
c6.metric("Precio más bajo", f"S/{precio_minimo(df_filtrado):,.2f}")


# GRÁFICOS - DASHBOARD 

st.plotly_chart(grafico_ventas(df_filtrado))  
st.plotly_chart(grafico_promedio(df_filtrado))