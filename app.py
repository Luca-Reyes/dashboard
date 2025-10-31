import streamlit as st
import pandas as pd
import os
import glob

# Configuración de la página
st.set_page_config(page_title="Dashboard Miproyecto1", layout="wide")

# Estilos CSS modernos y coloridos
st.markdown(
    """
    <style>
    /* Fondo general */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
        padding: 20px;
    }
    /* Contenedores de sección */
    .section {
        background: white;
        padding: 25px;
        margin: 20px 0;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #667eea;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .section:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }
    /* Tarjetas de gráficos */
    .graph-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        border: 1px solid #eef2ff;
        transition: all 0.3s ease;
    }
    .graph-card:hover {
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.25);
        transform: scale(1.01);
    }
    /* Títulos */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 700;
    }
    h1 {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    /* Tablas con estilo */
    .dataframe {
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 0.9em;
        min-width: 100%;
        border-radius: 8px;
        overflow: hidden;
    }
    .dataframe thead tr {
        background-color: #667eea;
        color: white;
        text-align: left;
    }
    .dataframe th,
    .dataframe td {
        padding: 12px 15px;
    }
    .dataframe tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    .dataframe tbody tr:nth-of-type(even) {
        background-color: #f8f9ff;
    }
    .dataframe tbody tr:last-of-type {
        border-bottom: 2px solid #667eea;
    }
    .dataframe tbody tr:hover {
        background-color: #eef4ff;
    }
    /* Botones de descarga */
    .stDownloadButton > button {
        background: linear-gradient(to right, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #667eea;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título principal con gradiente
st.markdown(
    """
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 16px; margin-bottom: 25px; box-shadow: 0 6px 20px rgba(0,0,0,0.15);'>
        <h1>📊 Dashboard: Factores de Empleabilidad</h1>
        <p style='font-size: 1.2em; opacity: 0.9;'>Proyecto: <strong>Miproyecto1</strong> • Análisis integral de empleabilidad</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Función para encontrar archivos por patrón
def buscar_archivos(carpeta, patron):
    return sorted(glob.glob(os.path.join(carpeta, patron)))

# --- SECCIÓN 1: DATOS COMPLETOS DE LA ENCUESTA ---
st.subheader("🔍 Datos completos de la encuesta")

csv_files = buscar_archivos("Miproyecto1", "*.csv")
xlsx_files = buscar_archivos("Miproyecto1", "*.xlsx")

if csv_files:
    try:
        df_csv = pd.read_csv(csv_files[0])
        st.write(f"📄 Archivo cargado: `{os.path.basename(csv_files[0])}`")
        st.write(f"🔢 Total de filas: **{len(df_csv)}** • Columnas: **{len(df_csv.columns)}**")
        st.dataframe(df_csv, use_container_width=True, height=500)  # 👈 MUESTRA TODO
    except Exception as e:
        st.error(f"❌ Error al cargar CSV: {e}")

elif xlsx_files:
    try:
        df_xlsx = pd.read_excel(xlsx_files[0])
        st.write(f"📄 Archivo cargado: `{os.path.basename(xlsx_files[0])}`")
        st.write(f"🔢 Total de filas: **{len(df_xlsx)}** • Columnas: **{len(df_xlsx.columns)}**")
        st.dataframe(df_xlsx, use_container_width=True, height=500)  # 👈 MUESTRA TODO
    except Exception as e:
        st.error(f"❌ Error al cargar XLSX: {e}")
else:
    st.warning("⚠️ No se encontró ningún archivo de datos (.csv o .xlsx).")

# --- SECCIÓN 2: DICCIONARIO DE VARIABLES ---
st.subheader("📋 Diccionario de variables")

# Nota: el nombre del archivo tiene un typo: "varibales" → lo dejamos así para que funcione
diccionario_files = buscar_archivos("Miproyecto1", "Diccionario de varibales.xlsx")

if diccionario_files:
    try:
        df_dicc = pd.read_excel(diccionario_files[0])
        st.write(f"📘 Archivo cargado: `{os.path.basename(diccionario_files[0])}`")
        st.dataframe(df_dicc, use_container_width=True, height=400)
    except Exception as e:
        st.error(f"❌ Error al cargar Diccionario de varibales: {e}")
else:
    st.info("ℹ️ No se encontró el archivo `Diccionario de varibales.xlsx`.")

# --- SECCIÓN 3: GRÁFICOS PNG ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📈 Gráficos generados")

png_files = buscar_archivos("Miproyecto1", "*.png")

if png_files:
    cols = st.columns(2)
    for i, img_path in enumerate(png_files):
        col = cols[i % 2]
        with col:
            st.markdown(f"<div class='graph-card'>", unsafe_allow_html=True)
            try:
                st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)
            except Exception as e:
                st.warning(f"⚠️ Error mostrando {os.path.basename(img_path)}: {e}")
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("ℹ️ No se encontraron archivos de imagen (.png).")

st.markdown("</div>", unsafe_allow_html=True)


# --- SECCIÓN 4: DESCARGAR ARCHIVOS ---
st.subheader("⬇️ Descargar archivos")

with st.expander("📂 Archivos disponibles"):
    all_files = []
    all_files.extend(csv_files)
    all_files.extend(xlsx_files)
    all_files.extend(diccionario_files)
    all_files.extend(png_files)

    if all_files:
        for i, file_path in enumerate(all_files):
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"📥 Descargar {os.path.basename(file_path)}",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="application/octet-stream",
                    help=f"Haz clic para descargar {os.path.basename(file_path)}",
                    key=f"download_{i}"
                )
    else:
        st.info("No hay archivos para descargar.")


# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #6c757d; font-size: 0.95em; padding: 15px; background: #f8f9fa; border-radius: 10px;'>"
    "<strong>Dashboard Miproyecto1</strong> • Generado con Streamlit • Datos actualizados en tiempo real desde archivos locales"
    "</p>",
    unsafe_allow_html=True
)
