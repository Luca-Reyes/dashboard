import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

def run_full_analysis():
    """
    Script único para cargar, procesar y analizar la encuesta de percepción
    basada en los indicadores y las hipótesis proporcionadas.
    """
    
    # --- 0. Configuración Inicial ---
    warnings.filterwarnings('ignore')
    sns.set(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 7)
    
    print("Iniciando el script de análisis integral...")

    # --- 1. Definición de Mapeos y Columnas Clave ---
    
    # Diccionarios de mapeo según el archivo "Indicadores.xlsx"
    map_competencias = {
        'Ninguno': 1,
        'Básico': 2,
        'Intermedio': 3,
        'Avanzado': 4,
        'Experto': 5
    }
    
    map_acuerdo = {
        'Totalmente en desacuerdo': 1,
        'En desacuerdo': 2,
        'Neutral': 3,
        'De acuerdo': 4,
        'Totalmente de acuerdo': 5
    }
    
    map_importancia = {
        'Sin importancia': 1,
        'Poca importancia': 2,
        'Neutral': 3,
        'Importante': 4,
        'Muy importante': 5
    }
    
    # Definición de columnas (copiadas de la estructura del CSV)
    
    # Demográficas (para H3)
    col_carrera = 'Por favor, escribe el nombre de tu carrera o programa de estudios.'
    col_semestre = '¿Qué semestre estás cursando actualmente?'
    
    # Indicador 1A: Competencias Técnicas (para H1, H2, H3, H5)
    cols_dc = [
        'Análisis e interpretación de datos.',
        'Fundamentos de ciberseguridad.',
        'Conceptos básicos de programación y automatización.',
        'Manejo de herramientas de IA (ej. ChatGPT, Copilot, Gemini, DALL-E)'
    ]
    
    # Indicador 1B: Habilidades Blandas
    cols_blandas = [
        'Pensamiento crítico y resolución de problemas complejos',
        'Comunicación efectiva en entornos digitales',
        'Adaptabilidad y aprendizaje continuo',
        'Creatividad e innovación',
        'Colaboración en equipos multidisciplinarios'
    ]
    
    # Indicador 2: Pertinencia de la Formación (para H2)
    cols_pertinencia = [
        'El currículo de mi carrera está alineado con las habilidades demandadas por el mercado laboral digital.',
        'Mi universidad promueve activamente el desarrollo de competencias digitales y blandas.',
        'Siento que la formación que he recibido me prepara para trabajos que aún no existen.',
        'El uso de la tecnología y la IA está bien integrado en las asignaturas de mi carrera.',
        'La metodología de enseñanza en mi carrera fomenta la adaptabilidad y el aprendizaje continuo.'
    ]
    
    # Indicador 3A: Confianza en Empleabilidad
    # Variable específica para H1 y H4: Percepción del impacto de la IA
    col_ai_impact = 'Creo que mi conocimiento sobre herramientas de IA mejorará mis oportunidades laborales.'
    
    # Indicador 3B: Importancia de Factores
    cols_factores = [
        'Habilidades técnicas y digitales (ej. programación, análisis de datos)',
        'Habilidades blandas (ej. pensamiento crítico, adaptabilidad)',
        'Experiencia práctica o pasantías',
        'Red de contactos (networking)',
        'Título académico de la universidad'
    ]
    
    # Indicador 4A: Percepción Universidad y Profesorado
    cols_univ_prof = [
        'El profesorado de mi carrera está capacitado para integrar herramientas de IA en la enseñanza.',
        'Mi universidad fomenta la innovación en las metodologías de enseñanza para adaptarse a la era digital.',
        'Mi universidad tiene los recursos adecuados (plataformas, software) para formar profesionales en la era digital.',
        'En general, recomendaría mi universidad como una institución que prepara para los desafíos del mercado laboral digital.'
    ]

    # --- 2. Carga y Limpieza de Datos ---
    
    file_path = "encuesta_limpia_ESPOCH.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {file_path}")
        return

    # Lista de todas las columnas a procesar y sus mapeos
    all_cols_to_process = [
        (cols_dc, map_competencias),
        (cols_blandas, map_competencias),
        (cols_pertinencia, map_acuerdo),
        ([col_ai_impact], map_acuerdo), # Como lista para el loop
        (cols_factores, map_importancia),
        (cols_univ_prof, map_acuerdo)
    ]
    
    # Aplicar mapeos y conversión a numérico
    for col_list, mapping in all_cols_to_process:
        for col in col_list:
            if col in df.columns:
                df[col] = df[col].map(mapping)
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                print(f"Advertencia: La columna '{col}' no se encontró. Se omitirá.")

    # --- 3. Ingeniería de Indicadores (Promedios) ---
    
    # Promedios de los indicadores
    df['COMP_DIGITAL'] = df[cols_dc].mean(axis=1)
    df['COMP_BLANDAS'] = df[cols_blandas].mean(axis=1)
    df['COMP_PERTINENCIA'] = df[cols_pertinencia].mean(axis=1)
    df['COMP_FACTORES'] = df[cols_factores].mean(axis=1)
    df['COMP_UNIV_PROF'] = df[cols_univ_prof].mean(axis=1)
    
    # Variables específicas para hipótesis
    df['PERCEP_IA'] = df[col_ai_impact]
    df['DOMINIO_DATOS'] = df['Análisis e interpretación de datos.'] # Proxy para H4 y H5

    # Limpieza de variables demográficas
    df['CARRERA'] = df[col_carrera].str.strip().str.title()
    df['SEMESTRE'] = df[col_semestre].str.strip()

    # --- 4. Análisis Descriptivo y Frecuencias ---
    
    print("\n" + "="*50)
    print(" PARTE 1: ANÁLISIS DESCRIPTIVO DE FRECUENCIAS")
    print("="*50)
    
    print("\n--- Frecuencia por Carrera (Top 10) ---")
    print(df['CARRERA'].value_counts().head(10).to_markdown(numalign="left", stralign="left"))
    
    print("\n--- Frecuencia por Semestre ---")
    print(df['SEMESTRE'].value_counts().to_markdown(numalign="left", stralign="left"))
    
    print("\n" + "="*50)
    print(" PARTE 2: PROMEDIOS GENERALES POR INDICADOR (Escala 1-5)")
    print("="*50)
    
    promedios = {
        "Indicador 1 (Competencias Digitales)": df['COMP_DIGITAL'].mean(),
        "Indicador 1 (Competencias Blandas)": df['COMP_BLANDAS'].mean(),
        "Indicador 2 (Pertinencia Formación)": df['COMP_PERTINENCIA'].mean(),
        "Indicador 3 (Importancia Factores)": df['COMP_FACTORES'].mean(),
        "Indicador 4 (Percepción Univ/Prof)": df['COMP_UNIV_PROF'].mean(),
        "Variable (Percepción Impacto IA)": df['PERCEP_IA'].mean()
    }
    
    for key, val in promedios.items():
        print(f"- {key}: {val:.2f}")

    # --- 5. Diagnóstico Avanzado: Prueba de Hipótesis ---

    print("\n" + "="*50)
    print(" PARTE 3: DIAGNÓSTICO AVANZADO (PRUEBA DE HIPÓTESIS)")
    print("="*50)
    
    # Función para interpretar correlación
    def interpretar_corr(r, p):
        if p < 0.05:
            fuerza = "débil"
            if abs(r) > 0.3: fuerza = "moderada"
            if abs(r) > 0.5: fuerza = "fuerte"
            direccion = "positiva" if r > 0 else "negativa"
            return f"Se encontró una correlación {direccion} {fuerza} y estadísticamente significativa (r={r:.3f}, p={p:.4f}). Hipótesis VALIDADA."
        else:
            return f"No se encontró correlación estadísticamente significativa (r={r:.3f}, p={p:.4f}). Hipótesis RECHAZADA."
    
    # Preparar datos (eliminando NaNs para las pruebas)
    df_h1 = df[['COMP_DIGITAL', 'PERCEP_IA']].dropna()
    df_h2 = df[['COMP_DIGITAL', 'COMP_PERTINENCIA']].dropna()
    df_h4 = df[['PERCEP_IA', 'DOMINIO_DATOS']].dropna()
    df_h5 = df[['COMP_DIGITAL', 'DOMINIO_DATOS']].dropna()

    # H1: Correlación entre Competencias Digitales y Percepción de IA
    print("\n--- H1: Competencias Digitales vs Percepción Impacto IA ---")
    r_h1, p_h1 = stats.pearsonr(df_h1['COMP_DIGITAL'], df_h1['PERCEP_IA'])
    print(interpretar_corr(r_h1, p_h1))

    # H2: Correlación entre Competencias Digitales y Pertinencia de Formación
    print("\n--- H2: Competencias Digitales vs Pertinencia de Formación ---")
    r_h2, p_h2 = stats.pearsonr(df_h2['COMP_DIGITAL'], df_h2['COMP_PERTINENCIA'])
    print(interpretar_corr(r_h2, p_h2))

    # H3: Diferencias de Competencias Digitales entre Carreras (ANOVA)
    print("\n--- H3: Diferencias de Competencias Digitales por Carrera ---")
    # Filtrar carreras con suficientes respuestas (ej. > 5) para que ANOVA sea robusto
    carreras_validas = df['CARRERA'].value_counts()[df['CARRERA'].value_counts() > 5].index
    df_h3 = df[df['CARRERA'].isin(carreras_validas) & df['COMP_DIGITAL'].notna()]
    
    if len(carreras_validas) > 1:
        grupos_h3 = [df_h3['COMP_DIGITAL'][df_h3['CARRERA'] == c] for c in carreras_validas]
        f_val_h3, p_val_h3 = stats.f_oneway(*grupos_h3)
        
        if p_val_h3 < 0.05:
            print(f"Prueba ANOVA significativa (F={f_val_h3:.2f}, p={p_val_h3:.4f}). Existen diferencias significativas en el promedio de competencias digitales entre carreras. Hipótesis VALIDADA.")
        else:
            print(f"Prueba ANOVA no significativa (F={f_val_h3:.2f}, p={p_val_h3:.4f}). No se encontraron diferencias significativas entre carreras. Hipótesis RECHAZADA.")
        
        # Generar gráfico Boxplot
        plt.figure(figsize=(15, 8))
        sns.boxplot(data=df_h3, x='CARRERA', y='COMP_DIGITAL', palette='viridis')
        plt.title('H3: Promedio de Competencias Digitales por Carrera (N > 5)')
        plt.ylabel('Promedio Competencias Digitales (1-5)')
        plt.xlabel('Carrera')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('H3_competencias_por_carrera.png')
        print("-> Gráfico 'H3_competencias_por_carrera.png' guardado.")
    else:
        print("No hay suficientes carreras con >5 respuestas para realizar una comparativa ANOVA.")

    # H4: Correlación entre Percepción de IA e Interés en BI (Proxy: Dominio de Datos)
    print("\n--- H4: Percepción IA vs Interés/Dominio en Análisis de Datos (Proxy) ---")
    r_h4, p_h4 = stats.pearsonr(df_h4['PERCEP_IA'], df_h4['DOMINIO_DATOS'])
    print(interpretar_corr(r_h4, p_h4))

    # H5: Correlación entre Competencias Digitales y Uso de BI (Proxy: Dominio de Datos)
    print("\n--- H5: Competencias Digitales vs Interés/Dominio en Análisis de Datos (Proxy) ---")
    r_h5, p_h5 = stats.pearsonr(df_h5['COMP_DIGITAL'], df_h5['DOMINIO_DATOS'])
    print(interpretar_corr(r_h5, p_h5))
    
    # Generar gráfico Regplot
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df_h5, x='COMP_DIGITAL', y='DOMINIO_DATOS',
                line_kws={"color": "red", "lw": 2},
                scatter_kws={'alpha': 0.3})
    plt.title('H5: Competencias Digitales vs. Dominio de Análisis de Datos')
    plt.xlabel('Promedio Competencias Digitales (General)')
    plt.ylabel('Dominio de Análisis de Datos (Proxy)')
    plt.tight_layout()
    plt.savefig('H5_competencias_vs_datos.png')
    print("-> Gráfico 'H5_competencias_vs_datos.png' guardado.")

    print("\n" + "="*50)
    print(" ANÁLISIS COMPLETO FINALIZADO")
    print("="*50)

# --- Ejecutar el script ---
if __name__ == "__main__":
    run_full_analysis()