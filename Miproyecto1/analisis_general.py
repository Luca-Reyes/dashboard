import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt

def preparar_datos_para_dashboard():
    """
    Carga, limpia, transforma y exporta los datos de la encuesta,
    además de generar gráficos para dashboard.
    """
    
    warnings.filterwarnings('ignore')
    file_path = "encuesta_limpia_ESPOCH.xlsx"
    print(f"Iniciando el procesamiento del archivo: {file_path}")

    # --- Definición de mapeos ---
    map_competencias = {
        'Ninguno': 1, 'Básico': 2, 'Intermedio': 3, 'Avanzado': 4, 'Experto': 5
    }
    map_acuerdo = {
        'Totalmente en desacuerdo': 1, 'En desacuerdo': 2, 'Neutral': 3,
        'De acuerdo': 4, 'Totalmente de acuerdo': 5
    }
    map_importancia = {
        'Sin importancia': 1, 'Poca importancia': 2, 'Neutral': 3,
        'Importante': 4, 'Muy importante': 5
    }

    # --- Nombres cortos ---
    rename_dict = {
        'Por favor, escribe el nombre de tu carrera o programa de estudios.': 'Demo_Carrera',
        '¿Qué semestre estás cursando actualmente?': 'Demo_Semestre',
        '¿Cuál es tu edad?': 'Demo_Edad',
        '¿Con qué género te identificas?': 'Demo_Genero',
        'Análisis e interpretación de datos.': 'P1_Analisis_Datos',
        'Fundamentos de ciberseguridad.': 'P1_Ciberseguridad',
        'Conceptos básicos de programación y automatización.': 'P1_Programacion',
        'Manejo de herramientas de IA (ej. ChatGPT, Copilot, Gemini, DALL-E)': 'P1_Manejo_IA',
        'Pensamiento crítico y resolución de problemas complejos': 'P2_Pensamiento_Critico',
        'Comunicación efectiva en entornos digitales': 'P2_Comunicacion_Digital',
        'Adaptabilidad y aprendizaje continuo': 'P2_Adaptabilidad',
        'Creatividad e innovación': 'P2_Creatividad',
        'Colaboración en equipos multidisciplinarios': 'P2_Colaboracion',
        'El currículo de mi carrera está alineado con las habilidades demandadas por el mercado laboral digital.': 'P3_Curriculo_Alineado',
        'Mi universidad promueve activamente el desarrollo de competencias digitales y blandas.': 'P3_Promueve_Competencias',
        'Siento que la formación que he recibido me prepara para trabajos que aún no existen.': 'P3_Prepara_Futuro',
        'El uso de la tecnología y la IA está bien integrado en las asignaturas de mi carrera.': 'P3_IA_Integrada',
        'La metodología de enseñanza en mi carrera fomenta la adaptabilidad y el aprendizaje continuo.': 'P3_Metodologia_Adaptable',
        'Me siento seguro(a) de que mi formación académica me prepara para conseguir un empleo relevante en mi área.': 'P4_Confianza_Empleo',
        'Mi perfil de egreso es competitivo en el mercado laboral actual.': 'P4_Perfil_Competitivo',
        'Considero que mis habilidades blandas (ej. comunicación, creatividad) me dan una ventaja en el mercado laboral.': 'P4_Ventaja_Blandas',
        'Creo que mi conocimiento sobre herramientas de IA mejorará mis oportunidades laborales.': 'P4_IA_Oportunidades',
        'Habilidades técnicas y digitales (ej. programación, análisis de datos)': 'P5_Factor_Tecnicas',
        'Habilidades blandas (ej. pensamiento crítico, adaptabilidad)': 'P5_Factor_Blandas',
        'Experiencia práctica o pasantías': 'P5_Factor_Experiencia',
        'Red de contactos (networking)': 'P5_Factor_Networking',
        'Título académico de la universidad': 'P5_Factor_Titulo',
        'El profesorado de mi carrera está capacitado para integrar herramientas de IA en la enseñanza.': 'P6_Profesor_Capacitado_IA',
        'Mi universidad fomenta la innovación en las metodologías de enseñanza para adaptarse a la era digital.': 'P6_Universidad_Innova',
        'Mi universidad tiene los recursos adecuados (plataformas, software) para formar profesionales en la era digital.': 'P6_Recursos_Adecuados',
        'En general, recomendaría mi universidad como una institución que prepara para los desafíos del mercado laboral digital.': 'P6_Recomendaria_Universidad'
    }

    # --- Grupos de columnas ---
    col_groups = {
        'Ind1_Tecnicas': ['P1_Analisis_Datos', 'P1_Ciberseguridad', 'P1_Programacion', 'P1_Manejo_IA'],
        'Ind1_Blandas': ['P2_Pensamiento_Critico', 'P2_Comunicacion_Digital', 'P2_Adaptabilidad', 'P2_Creatividad', 'P2_Colaboracion'],
        'Ind2_Pertinencia': ['P3_Curriculo_Alineado', 'P3_Promueve_Competencias', 'P3_Prepara_Futuro', 'P3_IA_Integrada', 'P3_Metodologia_Adaptable'],
        'Ind3_Confianza': ['P4_Confianza_Empleo', 'P4_Perfil_Competitivo', 'P4_Ventaja_Blandas', 'P4_IA_Oportunidades'],
        'Ind3_Factores': ['P5_Factor_Tecnicas', 'P5_Factor_Blandas', 'P5_Factor_Experiencia', 'P5_Factor_Networking', 'P5_Factor_Titulo'],
        'Ind4_Universidad': ['P6_Profesor_Capacitado_IA', 'P6_Universidad_Innova', 'P6_Recursos_Adecuados', 'P6_Recomendaria_Universidad']
    }

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    df = df.rename(columns=rename_dict)
    columnas_utiles = list(rename_dict.values())
    df_main = df[columnas_utiles].copy()

    # --- Mapeo de valores ---
    for grupo, cols in {
        'competencias': col_groups['Ind1_Tecnicas'] + col_groups['Ind1_Blandas'],
        'acuerdo': col_groups['Ind2_Pertinencia'] + col_groups['Ind3_Confianza'] + col_groups['Ind4_Universidad'],
        'importancia': col_groups['Ind3_Factores']
    }.items():
        if grupo == 'competencias':
            mapa = map_competencias
        elif grupo == 'acuerdo':
            mapa = map_acuerdo
        else:
            mapa = map_importancia
        for c in cols:
            if c in df_main.columns:
                df_main[c] = df_main[c].astype(str).str.strip().map(mapa)
                df_main[c] = pd.to_numeric(df_main[c], errors='coerce')

    # --- Indicadores ---
    df_main['Promedio_Ind1_Tecnicas'] = df_main[col_groups['Ind1_Tecnicas']].mean(axis=1)
    df_main['Promedio_Ind1_Blandas'] = df_main[col_groups['Ind1_Blandas']].mean(axis=1)
    df_main['Promedio_Ind2_Pertinencia'] = df_main[col_groups['Ind2_Pertinencia']].mean(axis=1)
    df_main['Promedio_Ind3_Confianza'] = df_main[col_groups['Ind3_Confianza']].mean(axis=1)
    df_main['Promedio_Ind4_Universidad'] = df_main[col_groups['Ind4_Universidad']].mean(axis=1)

    # --- KPI Generales ---
    df_kpi_generales = pd.DataFrame({
        'Indicador': [
            'Competencias Técnicas', 'Competencias Blandas',
            'Pertinencia Formación', 'Confianza Empleabilidad',
            'Percepción Universidad'
        ],
        'Promedio': [
            df_main['Promedio_Ind1_Tecnicas'].mean(),
            df_main['Promedio_Ind1_Blandas'].mean(),
            df_main['Promedio_Ind2_Pertinencia'].mean(),
            df_main['Promedio_Ind3_Confianza'].mean(),
            df_main['Promedio_Ind4_Universidad'].mean()
        ]
    })

    # --- KPI por carrera ---
    conteo_carreras = df_main['Demo_Carrera'].value_counts()
    carreras_principales = conteo_carreras[conteo_carreras > 5].index
    df_kpi_por_carrera = (
        df_main[df_main['Demo_Carrera'].isin(carreras_principales)]
        .groupby('Demo_Carrera')[
            ['Promedio_Ind1_Tecnicas', 'Promedio_Ind1_Blandas', 
             'Promedio_Ind2_Pertinencia', 'Promedio_Ind3_Confianza', 
             'Promedio_Ind4_Universidad']
        ].mean()
        .reset_index()
    )

    # --- Factores ---
    df_factores = df_main[col_groups['Ind3_Factores']].mean().reset_index()
    df_factores.columns = ['Factor', 'Importancia_Promedio']
    df_factores['Factor'] = df_factores['Factor'].map({
        'P5_Factor_Tecnicas': 'Habilidades Técnicas',
        'P5_Factor_Blandas': 'Habilidades Blandas',
        'P5_Factor_Experiencia': 'Experiencia Práctica',
        'P5_Factor_Networking': 'Networking',
        'P5_Factor_Titulo': 'Título Académico'
    }).fillna(df_factores['Factor'])
    df_factores = df_factores.sort_values(by='Importancia_Promedio', ascending=False)

    # --- FRECUENCIAS ---
    df_frec_carrera = conteo_carreras.reset_index()
    df_frec_carrera.columns = ['Carrera', 'Cantidad_Respuestas']

    # --- Visualizaciones ---
    plt.style.use('ggplot')

    # 1️⃣ Promedios generales
    plt.figure(figsize=(8, 5))
    plt.bar(df_kpi_generales['Indicador'], df_kpi_generales['Promedio'])
    plt.title("Promedios Generales por Indicador")
    plt.ylabel("Promedio (1-5)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("grafico_promedios_generales.png")
    plt.show()

    # 2️⃣ Promedios por carrera
    df_kpi_por_carrera.plot(x='Demo_Carrera', kind='bar', figsize=(10,6))
    plt.title("Promedios por Carrera")
    plt.ylabel("Promedio (1-5)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("grafico_promedios_por_carrera.png")
    plt.show()

    # 3️⃣ Ranking de factores
    plt.figure(figsize=(8,5))
    plt.barh(df_factores['Factor'], df_factores['Importancia_Promedio'])
    plt.title("Ranking de Factores de Empleabilidad")
    plt.xlabel("Importancia Promedio (1-5)")
    plt.tight_layout()
    plt.savefig("grafico_factores_empleabilidad.png")
    plt.show()

    # 4️⃣ Frecuencia de carreras
    plt.figure(figsize=(8,5))
    plt.barh(df_frec_carrera['Carrera'], df_frec_carrera['Cantidad_Respuestas'])
    plt.title("Cantidad de Respuestas por Carrera")
    plt.tight_layout()
    plt.savefig("grafico_frecuencia_carreras.png")
    plt.show()

    # 5️⃣ Distribución de indicadores por carrera
    plt.figure(figsize=(10,6))
    df_main.boxplot(column=['Promedio_Ind1_Tecnicas','Promedio_Ind1_Blandas',
                            'Promedio_Ind2_Pertinencia','Promedio_Ind3_Confianza',
                            'Promedio_Ind4_Universidad'])
    plt.title("Distribución de Promedios por Indicador")
    plt.ylabel("Valor (1-5)")
    plt.tight_layout()
    plt.savefig("grafico_distribucion_indicadores.png")
    plt.show()

    print("\nGráficos generados y guardados como archivos PNG.")

if __name__ == "__main__":
    preparar_datos_para_dashboard()

