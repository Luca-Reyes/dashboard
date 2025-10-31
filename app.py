import streamlit as st
import pandas as pd
import os
import glob

# Configuración de la página
st.set_page_config(page_title="Dashboard Miproyecto1", layout="wide")
st.title("📊 Dashboard: Factores de Empleabilidad")
st.markdown("Proyecto: **Miproyecto1**")

# Función para encontrar archivos por patrón
def buscar_archivos(carpeta, patron):
    return sorted(glob.glob(os.path.join(carpeta, patron)))

# --- CARGAR DATOS ---
st.subheader("🔍 Datos de la encuesta")

csv_files = buscar_archivos("Miproyecto1", "*.csv")
xlsx_files = buscar_archivos("Miproyecto1", "*.xlsx")

if csv_files:
    try:
        df_csv = pd.read_csv(csv_files[0])
        st.write(f"📄 Archivo cargado: `{os.path.basename(csv_files[0])}`")
        st.dataframe(df_csv.head(10))
    except Exception as e:
        st.error(f"❌ Error al cargar CSV: {e}")

elif xlsx_files:
    try:
        df_xlsx = pd.read_excel(xlsx_files[0])
        st.write(f"📄 Archivo cargado: `{os.path.basename(xlsx_files[0])}`")
        st.dataframe(df_xlsx.head(10))
    except Exception as e:
        st.error(f"❌ Error al cargar XLSX: {e}")
else:
    st.warning("⚠️ No se encontró ningún archivo de datos (.csv o .xlsx).")

# --- MOSTRAR GRÁFICOS PNG ---
st.subheader("📈 Gráficos generados")

png_files = buscar_archivos("Miproyecto1", "*.png")

if png_files:
    cols = st.columns(2)  # Dos columnas para mostrar los gráficos
    for i, img_path in enumerate(png_files):
        col = cols[i % 2]  # Alterna entre columna izquierda y derecha
        with col:
            try:
                st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)
            except Exception as e:
                st.warning(f"⚠️ Error mostrando {os.path.basename(img_path)}: {e}")
else:
    st.info("ℹ️ No se encontraron archivos de imagen (.png).")

# --- DESCARGA DE ARCHIVOS ---
st.subheader("⬇️ Descargar archivos")

with st.expander("Archivos disponibles"):
    all_files = []
    all_files.extend(csv_files)
    all_files.extend(xlsx_files)
    all_files.extend(png_files)

    if all_files:
        for file_path in all_files:
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"📥 Descargar {os.path.basename(file_path)}",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="application/octet-stream"
                )
    else:
        st.info("No hay archivos para descargar.")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("Dashboard generado con Streamlit • Datos actualizados desde CSV/XLSX • Imágenes generadas automáticamente")
