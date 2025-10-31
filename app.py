import streamlit as st
import pandas as pd
import os
import glob

# Configuración de la página
st.set_page_config(page_title="Dashboard Miproyecto1", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .section {
        background: white;
        padding: 20px;
        margin: 20px 0;
        border-radius: 8px;
        box-shadow: 0 1px 5px rgba(0,0,0,0.05);
    }
    .graph-card {
        background: #fff;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .download-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: #e3f2fd;
        color: #1976d2;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
    }
    .download-btn:hover {
        background: #bbdefb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título principal
st.markdown(
    """
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;'>
        <h1>📊 Dashboard: Factores de Empleabilidad</h1>
        <p style='font-size: 1.1em;'>Proyecto: <strong>Miproyecto1</strong></p>
    </div>
    """,
    unsafe_allow_html=True
)

# Función para encontrar archivos por patrón
def buscar_archivos(carpeta, patron):
    return sorted(glob.glob(os.path.join(carpeta, patron)))

# --- SECCIÓN 1: DATOS DE LA ENCUESTA ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🔍 Datos de la encuesta")

csv_files = buscar_archivos("Miproyecto1", "*.csv")
xlsx_files = buscar_archivos("Miproyecto1", "*.xlsx")

if csv_files:
    try:
        df_csv = pd.read_csv(csv_files[0])
        st.write(f"📄 Archivo cargado: `{os.path.basename(csv_files[0])}`")
        st.dataframe(df_csv.head(10), use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error al cargar CSV: {e}")

elif xlsx_files:
    try:
        df_xlsx = pd.read_excel(xlsx_files[0])
        st.write(f"📄 Archivo cargado: `{os.path.basename(xlsx_files[0])}`")
        st.dataframe(df_xlsx.head(10), use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error al cargar XLSX: {e}")
else:
    st.warning("⚠️ No se encontró ningún archivo de datos (.csv o .xlsx).")

st.markdown("</div>", unsafe_allow_html=True)

# --- SECCIÓN 2: DICCIONARIO DE VARIABLES ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📋 Diccionario de variables")

diccionario_files = buscar_archivos("Miproyecto1", "Diccionario de varibales.xlsx")

if diccionario_files:
    try:
        df_dicc = pd.read_excel(diccionario_files[0])
        st.write(f"📘 Archivo cargado: `{os.path.basename(diccionario_files[0])}`")
        st.dataframe(df_dicc, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error al cargar Diccionario de varibales: {e}")
else:
    st.info("ℹ️ No se encontró el archivo `Diccionario de varibales.xlsx`.")

st.markdown("</div>", unsafe_allow_html=True)

# --- SECCIÓN 3: GRÁFICOS PNG ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📈 Gráficos generados")

png_files = buscar_archivos("Miproyecto1", "*.png")

if png_files:
    cols = st.columns(2)
    for i, img_path in enumerate(png_files):
        col = cols[i % 2]
        with col:
            with st.container():
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
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("⬇️ Descargar archivos")

with st.expander("📂 Archivos disponibles"):
    all_files = []
    all_files.extend(csv_files)
    all_files.extend(xlsx_files)
    all_files.extend(diccionario_files)  # Nuevo archivo
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
                    key=f"download_{i}"  # 👈 CLAVE ÚNICA PARA EVITAR ERROR
                )
    else:
        st.info("No hay archivos para descargar.")

st.markdown("</div>", unsafe_allow_html=True)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #7f8c8d; font-size: 0.9em;'>"
    "Dashboard generado con Streamlit • Datos actualizados desde CSV/XLSX • Imágenes generadas automáticamente"
    "</p>",
    unsafe_allow_html=True
)
