import pandas as pd
import re
import logging
from unidecode import unidecode
import sys

# --- Configuración del Script ---

# Ajusta estos nombres de archivos según sea necesario
ARCHIVO_ENTRADA = 'ENCUESTA_DE_PERCEPCIÓN_EN_EL_USO__DE_LA_INTELIGENCIA_ARTIFICIAL_Y_LA_EMPLEABILIDAD_-_all_versions_-_labels_-_2025-10-30-15-38-54.xlsx'
ARCHIVO_SALIDA_EXCEL = 'encuesta_limpia_ESPOCH.xlsx' # <<< Nombre de salida actualizado
ARCHIVO_SALIDA_CSV = 'encuesta_limpia_ESPOCH.csv'     # <<< Nombre de salida actualizado
ARCHIVO_REPORTE = 'reporte_limpieza_ESPOCH.log'   # <<< Nombre de salida actualizado

# ¡Importante! Columna a limpiar (basado en el snippet de tu archivo)
COLUMNA_OBJETIVO = '¿En qué universidad estudias actualmente?'

# Valor estandarizado para ESPOCH
VALOR_NORMALIZADO = 'ESPOCH'

# Variaciones conocidas de ESPOCH (después de limpiar minúsculas, tildes y puntuación)
# Agrega más variaciones aquí si las descubres
ESPOCH_VARIANTS = {
    'espoch',
    'escuela superior politecnica de chimborazo',
    'esc sup politec chimborazo',
    'politecnica de chimborazo',
    'escuela superior politecnica chimborazo',
    'epoch'
    # Agrega 'escuela superior politecnica de chimborazo' por si acaso, aunque ya está cubierta
}

# --- Configuración del Logger (Reporte) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(ARCHIVO_REPORTE, mode='w'), # Escribe el log a un archivo
        logging.StreamHandler(sys.stdout)          # Muestra el log en la consola
    ]
)

def limpiar_y_normalizar_espoch(valor_original):
    """
    Limpia y normaliza una entrada de texto para identificar variantes de ESPOCH.
    """
    # 1. Manejar valores nulos o vacíos
    #if pd.isna(valor_original) or not str(valor_original).strip():
        #return None  # Representa un valor nulo estandarizado

    texto = str(valor_original)

    # 2. Estandarización de texto
    texto_limpio = unidecode(texto)  # Quitar tildes (ej. Politécnica -> Politecnica)
    texto_limpio = texto_limpio.lower()  # Convertir a minúsculas
    texto_limpio = re.sub(r'[^\w\s]', '', texto_limpio)  # Quitar puntuación y caracteres especiales
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()  # Quitar espacios extra

    # 3. Normalización (Mapeo)
    if texto_limpio in ESPOCH_VARIANTS:
        return VALOR_NORMALIZADO
    else:
        # Si no es una variante de ESPOCH, devolvemos el valor original
        return valor_original

def main():
    """
    Función principal para ejecutar el proceso de limpieza.
    """
    logging.info("--- Iniciando Proceso de Limpieza, Normalización y FILTRADO ---")

    # --- 1. Cargar Datos ---
    try:
        df = pd.read_excel(ARCHIVO_ENTRADA)
        logging.info(f"Archivo '{ARCHIVO_ENTRADA}' cargado exitosamente.")
        logging.info(f"Total de registros leídos: {len(df)}")
    except FileNotFoundError:
        logging.error(f"Error: El archivo '{ARCHIVO_ENTRADA}' no fue encontrado.")
        return
    except Exception as e:
        logging.error(f"Error al leer el archivo Excel: {e}")
        return

    if COLUMNA_OBJETIVO not in df.columns:
        logging.error(f"Error: La columna '{COLUMNA_OBJETIVO}' no se encuentra en el archivo.")
        logging.info(f"Columnas disponibles: {list(df.columns)}")
        return

    # Guardar una copia para el reporte de cambios
    df_original = df.copy()

    # --- 2. Manejo de Duplicados ---
    registros_antes_duplicados = len(df)
    df.drop_duplicates(inplace=True)
    registros_despues_duplicados = len(df)
    duplicados_eliminados = registros_antes_duplicados - registros_despues_duplicados
    logging.info(f"Se eliminaron {duplicados_eliminados} registros duplicados.")

    # --- 3. Limpieza y Normalización ---
    logging.info(f"Iniciando limpieza de la columna '{COLUMNA_OBJETIVO}'...")
    columna_original = df[COLUMNA_OBJETIVO]
    nulos_antes = columna_original.isna().sum()

    # Aplicar la función de limpieza
    df['columna_limpia_espoch'] = columna_original.apply(limpiar_y_normalizar_espoch)

    nulos_despues = df['columna_limpia_espoch'].isna().sum()
    logging.info(f"Valores nulos/vacíos antes: {nulos_antes}")
    logging.info(f"Valores nulos/vacíos después (estandarizados): {nulos_despues}")

    # <<< --- INICIO: SECCIÓN DE FILTRADO --- >>>
    registros_antes_filtrado = len(df)
    logging.info(f"Total de registros antes del filtrado (después de duplicados): {registros_antes_filtrado}")
    
    # Filtramos para quedarnos solo con las filas que SÍ fueron mapeadas a VALOR_NORMALIZADO
    # Usamos .copy() para evitar SettingWithCopyWarning
    df_filtrado = df[df['columna_limpia_espoch'] == VALOR_NORMALIZADO].copy() 
    
    registros_despues_filtrado = len(df_filtrado)
    registros_descartados = registros_antes_filtrado - registros_despues_filtrado
    
    # Asignar el valor normalizado a la columna original en el DataFrame filtrado
    # Esto asegura que todos los registros conservados tengan 'ESPOCH' en la columna original
    df_filtrado[COLUMNA_OBJETIVO] = VALOR_NORMALIZADO

    logging.info(f"Se han filtrado los datos. Se conservan {registros_despues_filtrado} registros de '{VALOR_NORMALIZADO}'.")
    logging.info(f"Se descartaron {registros_descartados} registros (de otras universidades o nulos).")
    # <<< --- FIN: SECCIÓN DE FILTRADO --- >>>


    # --- 4. Generación de Reporte de Cambios ---
    logging.info("--- Reporte de Cambios (Muestreo de filas CONSERVADAS) ---")

    # <<< Lógica de reporte actualizada para reflejar el filtrado >>>
    # Comparamos la columna original (usando el índice de df_filtrado) con la limpia
    indices_conservados = df_filtrado.index
    df_cambios = df_original.loc[indices_conservados].copy() # Tomamos los originales de las filas conservadas
    df_cambios['columna_limpia_espoch'] = df_filtrado['columna_limpia_espoch'] # Añadimos la columna limpia
    
    # Filtramos para mostrar solo los que realmente cambiaron (ej. "Esc. Sup." -> "ESPOCH")
    df_cambios_reales = df_cambios[df_cambios[COLUMNA_OBJETIVO] != df_cambios['columna_limpia_espoch']]
    
    mapeados_a_espoch = len(df_filtrado)
    total_cambios_visibles = len(df_cambios_reales)

    logging.info(f"Total de registros conservados de '{VALOR_NORMALIZADO}': {mapeados_a_espoch}")
    logging.info(f"Total de registros que necesitaron normalización (ej. 'Esc. Sup.' -> 'ESPOCH'): {total_cambios_visibles}")

    if total_cambios_visibles > 0:
        logging.info("Ejemplos de normalización (Antes -> Después):")
        ejemplos_str = df_cambios_reales[[COLUMNA_OBJETIVO, 'columna_limpia_espoch']].drop_duplicates().head(10).to_string()
        for linea in ejemplos_str.split('\n'):
            logging.info(f"  {linea}")
    else:
        logging.info("No se detectaron cambios de normalización en los datos conservados (todos ya decían 'ESPOCH').")


    # --- 5. Guardar Resultados ---
    # Eliminar la columna auxiliar antes de guardar para que no aparezca en el archivo final
    df_filtrado.drop(columns=['columna_limpia_espoch'], inplace=True)

    try:
        # <<< Guardar el DataFrame FILTRADO >>>
        df_filtrado.to_excel(ARCHIVO_SALIDA_EXCEL, index=False, engine='openpyxl')
        df_filtrado.to_csv(ARCHIVO_SALIDA_CSV, index=False, encoding='utf-8-sig')

        logging.info(f"Archivo Excel (SOLO ESPOCH) guardado en: '{ARCHIVO_SALIDA_EXCEL}'")
        logging.info(f"Archivo CSV (SOLO ESPOCH) guardado en: '{ARCHIVO_SALIDA_CSV}'")
        logging.info(f"Reporte de limpieza guardado en: '{ARCHIVO_REPORTE}'")

    except Exception as e:
        logging.error(f"Error al guardar los archivos de salida: {e}")

    logging.info("--- Proceso de Limpieza y Filtrado Finalizado ---")

if __name__ == "__main__":
    main()