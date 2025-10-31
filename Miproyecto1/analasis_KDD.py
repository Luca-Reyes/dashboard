import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import warnings

def preparar_datos_para_dashboard_interactivo():
    warnings.filterwarnings('ignore')

    file_path = "encuesta_limpia_ESPOCH.xlsx"
    print(f"Iniciando el procesamiento del archivo: {file_path}")

    # === Mapas y configuraciones ===
    map_competencias = {'Ninguno': 1, 'Básico': 2, 'Intermedio': 3, 'Avanzado': 4, 'Experto': 5}
    map_acuerdo = {'Totalmente en desacuerdo': 1, 'En desacuerdo': 2, 'Neutral': 3, 'De acuerdo': 4, 'Totalmente de acuerdo': 5}
    map_importancia = {'Sin importancia': 1, 'Poca importancia': 2, 'Neutral': 3, 'Importante': 4, 'Muy importante': 5}

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

    col_groups = {
        'Ind1_Tecnicas': ['P1_Analisis_Datos', 'P1_Ciberseguridad', 'P1_Programacion', 'P1_Manejo_IA'],
        'Ind1_Blandas': ['P2_Pensamiento_Critico', 'P2_Comunicacion_Digital', 'P2_Adaptabilidad', 'P2_Creatividad', 'P2_Colaboracion'],
        'Ind2_Pertinencia': ['P3_Curriculo_Alineado', 'P3_Promueve_Competencias', 'P3_Prepara_Futuro', 'P3_IA_Integrada', 'P3_Metodologia_Adaptable'],
        'Ind3_Confianza': ['P4_Confianza_Empleo', 'P4_Perfil_Competitivo', 'P4_Ventaja_Blandas', 'P4_IA_Oportunidades'],
        'Ind3_Factores': ['P5_Factor_Tecnicas', 'P5_Factor_Blandas', 'P5_Factor_Experiencia', 'P5_Factor_Networking', 'P5_Factor_Titulo'],
        'Ind4_Universidad': ['P6_Profesor_Capacitado_IA', 'P6_Universidad_Innova', 'P6_Recursos_Adecuados', 'P6_Recomendaria_Universidad']
    }

    df = pd.read_excel(file_path).rename(columns=rename_dict)
    columnas_utiles = list(rename_dict.values())
    df_main = df[columnas_utiles].copy()

    # === Mapear valores ===
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
            df_main[c] = df_main[c].astype(str).map(mapa)
            df_main[c] = pd.to_numeric(df_main[c], errors='coerce')

    # === Cálculo de indicadores ===
    df_main['Promedio_Ind1_Tecnicas'] = df_main[col_groups['Ind1_Tecnicas']].mean(axis=1)
    df_main['Promedio_Ind1_Blandas'] = df_main[col_groups['Ind1_Blandas']].mean(axis=1)
    df_main['Promedio_Ind2_Pertinencia'] = df_main[col_groups['Ind2_Pertinencia']].mean(axis=1)
    df_main['Promedio_Ind3_Confianza'] = df_main[col_groups['Ind3_Confianza']].mean(axis=1)
    df_main['Promedio_Ind4_Universidad'] = df_main[col_groups['Ind4_Universidad']].mean(axis=1)

    # === KPIs Generales ===
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

    # === Gráficos Interactivos ===
    fig1 = px.bar(df_kpi_generales, x='Indicador', y='Promedio',
                  title='Promedios Generales por Indicador',
                  color='Promedio', text='Promedio',
                  color_continuous_scale='tealgrn')
    fig1.update_layout(xaxis_title=None, yaxis_title='Promedio (1-5)', template='plotly_white')

    conteo_carreras = df_main['Demo_Carrera'].value_counts().reset_index()
    conteo_carreras.columns = ['Carrera', 'Cantidad']

    fig2 = px.bar(conteo_carreras, y='Carrera', x='Cantidad',
                  orientation='h', title='Número de Respuestas por Carrera',
                  color='Cantidad', color_continuous_scale='blues')

    # === Factores de empleabilidad ===
    df_factores = df_main[col_groups['Ind3_Factores']].mean().reset_index()
    df_factores.columns = ['Factor', 'Importancia_Promedio']
    fig3 = px.bar(df_factores, x='Importancia_Promedio', y='Factor',
                  orientation='h', title='Importancia Promedio de Factores de Empleabilidad',
                  color='Importancia_Promedio', color_continuous_scale='viridis')

    # === Distribución ===
    cols_box = ['Promedio_Ind1_Tecnicas','Promedio_Ind1_Blandas',
                'Promedio_Ind2_Pertinencia','Promedio_Ind3_Confianza',
                'Promedio_Ind4_Universidad']
    df_box = df_main.melt(value_vars=cols_box, var_name='Indicador', value_name='Promedio')
    fig4 = px.box(df_box, x='Indicador', y='Promedio', points='all',
                  title='Distribución de Promedios por Indicador',
                  color='Indicador', color_discrete_sequence=px.colors.qualitative.Set2)

    # === Mostrar gráficos ===
    fig1.show()
    fig2.show()
    fig3.show()
    fig4.show()

    print("\n✅ Gráficos interactivos generados correctamente. Listos para integrar en dashboard.")

if __name__ == "__main__":
    preparar_datos_para_dashboard_interactivo()
