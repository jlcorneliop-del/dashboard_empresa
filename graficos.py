# GRÁFICOS EJECUTIVOS PARA INFORME GERENCIAL
# ----------------------------------------
import plotly.express as px

# 1. Ventas por Marca (Barras Verticales)
def grafico_ventas(df):
    ventas = df.groupby("marca")["cantidad"].sum().reset_index()
    fig = px.bar(
        ventas, x="marca", y="cantidad",
        title="<b>Unidades Vendidas por Marca</b>",
        labels={"marca": "Marca", "cantidad": "Unidades"},
        color="cantidad",
        color_continuous_scale="Blues",
        text_auto=True
    )
    fig.update_layout(template="plotly_white", coloraxis_showscale=False, margin=dict(t=40, b=20, l=10, r=10))
    return fig

# 2. Precio Promedio por Marca
def grafico_promedio(df):
    promedio = df.groupby("marca")["precio_venta"].mean().reset_index()
    fig = px.bar(
        promedio, x="marca", y="precio_venta",
        title="<b>Precio Promedio por Marca (S/)</b>",
        labels={"marca": "Marca", "precio_venta": "Promedio (S/)"},
        color_discrete_sequence=["#1E88E5"],
        text_auto=".2f"
    )
    fig.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=10, r=10))
    return fig

# 3. Participación por Sede / Tienda (Gráfico de Dona)
def grafico_sedes(df):
    sedes = df.groupby("tienda")["precio_venta"].sum().reset_index()
    fig = px.pie(
        sedes, values="precio_venta", names="tienda",
        title="<b>Participación en Ingresos por Sede</b>",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=10, r=10))
    return fig

# 4. Métodos de Pago Preferidos
def grafico_metodo_pago(df):
    metodos = df.groupby("metodo_pago")["cantidad"].sum().reset_index()
    fig = px.bar(
        metodos, y="metodo_pago", x="cantidad",
        orientation='h',
        title="<b>Preferencia de Método de Pago</b>",
        labels={"metodo_pago": "Método", "cantidad": "Unidades"},
        color_discrete_sequence=["#26A69A"],
        text_auto=True
    )
    fig.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=10, r=10))
    return fig