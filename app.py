import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard miproyecto1", layout="wide")
st.title("📊 Dashboard: Factores de Empleabilidad")
st.markdown("Proyecto: **Miproyecto1**")

# Cargar y mostrar datos
try:
    df = pd.read_csv("miproyecto1/encuesta_limpia_ESPOCH.csv")
    st.subheader("🔍 Datos de la encuesta (primeras 10 filas)")
    st.dataframe(df.head(10))
except Exception as e:
    st.error(f"❌ Error al cargar los datos: {e}")

# Mostrar gráficos
st.subheader("📈 Gráficos generados")

col1, col2 = st.columns(2)

with col1:
    try:
        st.image("miproyecto1/grafico_factores_empleabilidad.png", caption="Ranking de Factores de Empleabilidad", use_column_width=True)
    except:
        st.warning("No se encontró: grafico_factores_empleabilidad.png")

with col2:
    try:
        st.image("miproyecto1/grafico_distribucion_indicadores.png", caption="Distribución de Indicadores", use_column_width=True)
    except:
        st.warning("No se encontró: grafico_distribucion_indicadores.png")

st.markdown("---")
st.caption("Dashboard generado con Streamlit • Datos actualizados desde CSV")
