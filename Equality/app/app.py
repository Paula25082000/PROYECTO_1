"""
Panel de Inteligencia: Igualdad en Europa (ESS11)
Aplicación principal de Streamlit

Autor: Panel BI - Equality Project
Fecha: 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Importar módulos personalizados
from config import (
    PAGE_CONFIG, APP_TITLE, APP_SUBTITLE, DEPENDENT_VARS,
    VAR_DESCRIPTIONS, COLOR_PALETTE
)
from data_loader import get_data_loader, DataLoader
from components import (
    render_sidebar, apply_education_filter, render_kpi_cards,
    render_variable_selector, render_section_header, render_info_box,
    render_stats_table, render_data_quality_warning, create_download_button,
    render_methodology_expander, render_footer
)
from visualizations import (
    create_distribution_histogram, create_gender_comparison,
    create_age_trend, create_education_trend, create_country_map,
    create_party_bar_chart, create_ideology_scatter,
    create_correlation_heatmap, create_top_bottom_chart,
    create_violin_plot, create_gender_frequency_histogram
)
from analytics import (
    calculate_spearman_correlation, test_normality,
    calculate_group_statistics, perform_gender_comparison,
    perform_age_correlation, perform_education_correlation,
    calculate_ideology_gradient, generate_summary_statistics,
    interpret_correlation_strength
)


# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(**PAGE_CONFIG)


# ============================================================================
# CSS PERSONALIZADO
# ============================================================================

def load_custom_css():
    """Carga estilos CSS personalizados para mejorar la UX/UI."""
    st.markdown("""
    <style>
    /* Estilo general */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Títulos */
    h1 {
        color: #2c3e50;
        font-weight: 700;
        padding-bottom: 10px;
        border-bottom: 3px solid #3498db;
    }
    
    h2 {
        color: #34495e;
        font-weight: 600;
        margin-top: 30px;
    }
    
    h3 {
        color: #7f8c8d;
        font-weight: 500;
    }
    
    /* Métricas KPI */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #2c3e50;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 600;
        color: #7f8c8d;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ecf0f1;
    }
    
    /* Botones */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #ecf0f1;
        border-radius: 5px;
        font-weight: 600;
    }
    
    /* Menú de navegación */
    .nav-menu {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    
    .nav-menu h4 {
        color: #2c3e50;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #3498db;
    }
    
    .nav-link {
        display: block;
        padding: 8px 12px;
        margin: 5px 0;
        color: #34495e;
        text-decoration: none;
        border-radius: 5px;
        transition: all 0.3s;
        font-size: 14px;
    }
    
    .nav-link:hover {
        background-color: #ecf0f1;
        color: #3498db;
        padding-left: 18px;
    }
    
    .nav-link::before {
        content: "→ ";
        margin-right: 5px;
    }
    
    /* Cajas de información */
    .stAlert {
        border-radius: 5px;
        padding: 15px;
    }
    
    /* Tablas */
    [data-testid="stDataFrame"] {
        border-radius: 5px;
    }
    
    /* Separadores */
    hr {
        margin: 30px 0;
        border: none;
        border-top: 2px solid #ecf0f1;
    }
    </style>
    """, unsafe_allow_html=True)


load_custom_css()


# ============================================================================
# INICIALIZACIÓN DE DATOS
# ============================================================================

@st.cache_resource
def initialize_app():
    """Inicializa la aplicación y carga los datos."""
    loader = get_data_loader()
    return loader


# Cargar datos
with st.spinner("⏳ Cargando datos del ESS11..."):
    data_loader = initialize_app()
    df = data_loader.get_data()


# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

# Título y subtítulo
st.title(APP_TITLE)
st.markdown(f"*{APP_SUBTITLE}*")
st.markdown("---")

# Renderizar sidebar con filtros
filters = render_sidebar(df)

# Aplicar filtros
df_filtered = data_loader.get_filtered_data(df, filters)

# Aplicar filtro educativo especial
if 'education_filter' in filters and filters['education_filter']:
    df_filtered = apply_education_filter(df_filtered, filters['education_filter'])

# Advertencia de calidad de datos
render_data_quality_warning(df_filtered, min_obs=30)

# Estadísticas generales en el sidebar
st.sidebar.markdown("---")
st.sidebar.metric("Observaciones filtradas", f"{len(df_filtered):,}")
st.sidebar.metric("% del total", f"{(len(df_filtered)/len(df)*100):.1f}%")

# Menú de navegación
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="nav-menu">
    <h4>📋 Navegación</h4>
    <a href="#origen-de-los-datos" class="nav-link">Origen de los Datos</a>
    <a href="#limpieza-de-datos" class="nav-link">Limpieza de Datos</a>
    <a href="#exploraci-n-de-datos" class="nav-link">Exploración de Datos</a>
    <a href="#an-lisis-espec-fico-espa-a" class="nav-link">Análisis España</a>
    <a href="#matriz-de-correlaci-n" class="nav-link">Correlaciones</a>
    <a href="#conclusiones-clave" class="nav-link">Conclusiones</a>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SECCIÓN: ORIGEN Y DATOS
# ============================================================================

st.markdown('<a id="origen-de-los-datos"></a>', unsafe_allow_html=True)
render_section_header(
    "Origen de los Datos",
    "Información sobre la fuente de datos y el contexto del estudio",
    "📚"
)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### European Social Survey Round 11 (ESS11)
    
    La **European Social Survey (ESS)** es un estudio comparativo europeo de opinión pública 
    que se realiza cada dos años desde 2002. La Ronda 11 (2023) incluye respuestas de más de 
    40,000 personas en más de 30 países europeos.
    
    **Objetivos del ESS11:**
    - Monitorear actitudes, creencias y patrones de comportamiento en Europa
    - Proporcionar datos de alta calidad para investigación académica y políticas públicas
    - Facilitar comparaciones entre países y a lo largo del tiempo
    
    **Variables clave en este panel:**
    - **Igualdad de oportunidades** (ipeqopta): Apoyo a que todas las personas sean tratadas igual
    - **Igualdad salarial** (eqpaybg): Apoyo a la equidad salarial entre géneros
    - **Interés político** (polintr): Nivel de interés en asuntos políticos
    - **Percepción sobre inmigración** (imwbcnt): Actitudes hacia la inmigración
    - **Relaciones de género** (wsekpwr): Percepciones sobre dinámicas de poder entre géneros
    """)

with col2:
    st.info(f"""
    **📊 Datos Cargados:**
    - **Total observaciones:** {len(df):,}
    - **Países incluidos:** {df['cntry'].nunique()}
    - **Variables analizadas:** {len(DEPENDENT_VARS)}
    - **Período:** 2023
    """)
    
    # Botón de descarga
    create_download_button(
        df_filtered,
        "ess11_filtered_data.csv",
        "📥 Descargar datos filtrados"
    )

# Mostrar muestra de datos
with st.expander("👁️ Ver muestra de datos (primeras 100 filas)"):
    st.dataframe(df_filtered.head(100), use_container_width=True)


# ============================================================================
# SECCIÓN: EXPLICACIÓN DE LOS DATOS
# ============================================================================

render_section_header(
    "Explicación de las Variables",
    "Descripción detallada de las variables analizadas",
    "📖"
)

# Selector de variable para ver descripción
selected_var_desc = st.selectbox(
    "Seleccionar variable para ver descripción:",
    options=list(DEPENDENT_VARS.keys()),
    format_func=lambda x: DEPENDENT_VARS[x],
    key="var_desc_select"
)

st.markdown(VAR_DESCRIPTIONS[selected_var_desc])

# Explicación de limpieza de datos
st.markdown("---")
st.markdown('<a id="limpieza-de-datos"></a>', unsafe_allow_html=True)
st.markdown("#### 🧹 Limpieza de Datos Aplicada")

# Diccionario con explicaciones de limpieza por variable (simplificado)
cleaning_explanations = {
    'ipeqopta': """
    **Valores eliminados:** 66, 77, 88, 99 (No aplicable, Rechazo, No sabe, Sin respuesta)
    
    **Transformación:** Inversión de escala (7 - valor original) para que valores más altos indiquen mayor apoyo.
    """,
    'eqpaybg': """
    **Valores eliminados:** 7, 8, 9 (Rechazo, No sabe, Sin respuesta)
    
    **Transformación:** Ninguna.
    """,
    'polintr': """
    **Valores eliminados:** 7, 8, 9 (Rechazo, No sabe, Sin respuesta)
    
    **Transformación:** Inversión de escala (5 - valor original) para que valores más altos indiquen mayor interés.
    """,
    'imwbcnt': """
    **Valores eliminados:** 77, 88, 99 (Rechazo, No sabe, Sin respuesta)
    
    **Transformación:** Ninguna.
    """,
    'wsekpwr': """
    **Valores eliminados:** 7, 8, 9 (Rechazo, No sabe, Sin respuesta)
    
    **Transformación:** Ninguna.
    """
}

st.info(cleaning_explanations[selected_var_desc])

st.markdown("**Nota:** También se eliminan observaciones con valores inválidos en variables explicativas "
            "(género: 9, edad: 999, educación: 5555/7777/8888/9999, partido: 66/77/88/99).")

st.markdown("---")

# Estadísticas descriptivas de la variable seleccionada
stats = data_loader.get_variable_stats(df_filtered, selected_var_desc)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Media", f"{stats.get('mean', 0):.3f}")
with col2:
    st.metric("Mediana", f"{stats.get('median', 0):.3f}")
with col3:
    st.metric("Desv. Est.", f"{stats.get('std', 0):.3f}")
with col4:
    st.metric("Observaciones", f"{stats.get('count', 0):,}")

# Test de normalidad
normality = test_normality(df_filtered, selected_var_desc)
render_info_box(
    "Test de Normalidad (Shapiro-Wilk)",
    normality['message'],
    "info" if normality['is_normal'] else "warning"
)


# ============================================================================
# SECCIÓN: ANÁLISIS EXPLORATORIO (EDA)
# ============================================================================
st.markdown('<a id="exploraci-n-de-datos"></a>', unsafe_allow_html=True)
render_section_header(
    "Análisis Exploratorio de Datos (EDA)",
    "Análisis bivariante de variables dependientes con factores sociodemográficos",
    "🔍"
)

# Selector de variable para EDA
selected_var = render_variable_selector(DEPENDENT_VARS, key="eda_var_select")

# Tabs para diferentes análisis
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribución General",
    "👥 Análisis por Género",
    "📅 Análisis por Edad",
    "🎓 Análisis por Educación",
    "🌍 Análisis por País"
])

# --- TAB 1: DISTRIBUCIÓN GENERAL ---
with tab1:
    st.subheader(f"Distribución de {DEPENDENT_VARS[selected_var]}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Histograma
        fig_hist = create_distribution_histogram(
            df_filtered,
            selected_var,
            f"Distribución de {DEPENDENT_VARS[selected_var]}"
        )
        st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': True})
    
    with col2:
        # Estadísticas completas
        summary_stats = generate_summary_statistics(df_filtered, selected_var)
        st.dataframe(summary_stats, use_container_width=True)
    
    # Test de normalidad
    normality = test_normality(df_filtered, selected_var)
    if normality['is_normal']:
        st.success(f"✅ La variable sigue una distribución normal (p = {normality['pvalue']:.4f})")
    else:
        st.warning(f"⚠️ La variable NO sigue una distribución normal (p = {normality['pvalue']:.4f}). "
                  "Se recomienda usar estadística no paramétrica (Spearman, Mann-Whitney).")

# --- TAB 2: ANÁLISIS POR GÉNERO ---
with tab2:
    st.subheader(f"{DEPENDENT_VARS[selected_var]} por Género")
    
    # Realizar análisis de género
    gender_analysis = perform_gender_comparison(df_filtered, selected_var)
    
    if 'error' not in gender_analysis:
        # Calcular correlación de Spearman para género
        data_gender = df_filtered[['gndr', selected_var]].dropna()
        
        if len(data_gender) >= 10:
            corr, pval = calculate_spearman_correlation(df_filtered, 'gndr', selected_var)
            
            gender_corr = {
                'correlation': corr,
                'p_value': pval,
                'strength': interpret_correlation_strength(corr),
                'significant': pval < 0.05,
                'direction': 'positiva' if corr > 0 else 'negativa'
            }
        else:
            gender_corr = None
        
        # Primera fila de KPIs: Medias y Brecha
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Media Hombres", f"{gender_analysis['male_mean']:.3f}")
        with col2:
            st.metric("Media Mujeres", f"{gender_analysis['female_mean']:.3f}")
        with col3:
            st.metric("Brecha de Género", f"{gender_analysis['gap']:.3f}")
        
        # Segunda fila de KPIs: Correlación, Fuerza y Significación
        if gender_corr:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Correlación con Género", f"{gender_corr['correlation']:.3f}")
            with col2:
                st.metric("Fuerza", gender_corr['strength'])
            with col3:
                significacion = "Sí (p < 0.05)" if gender_corr['significant'] else "No (p ≥ 0.05)"
                st.metric("Significación", significacion)
            
            # Nota interpretativa personalizada por variable (en verde si positiva, rojo si negativa)
            gender_notes = {
                'ipeqopta': {
                    'positive': "**Nota:** Una correlación positiva indica que las mujeres creen **MÁS** en la igualdad de las personas y apoyan **MÁS** la igualdad de oportunidades que los hombres.",
                    'negative': "**Nota:** Una correlación negativa indica que los hombres creen **MÁS** en la igualdad de las personas y apoyan **MÁS** la igualdad de oportunidades que las mujeres."
                },
                'eqpaybg': {
                    'positive': "**Nota:** Una correlación positiva indica que las mujeres apoyan **MÁS** la igualdad salarial entre géneros que los hombres.",
                    'negative': "**Nota:** Una correlación negativa indica que los hombres apoyan **MÁS** la igualdad salarial entre géneros que las mujeres."
                },
                'polintr': {
                    'positive': "**Nota:** Una correlación positiva indica que las mujeres tienen **MÁS** interés en política que los hombres.",
                    'negative': "**Nota:** Una correlación negativa indica que los hombres tienen **MÁS** interés en política que las mujeres."
                },
                'imwbcnt': {
                    'positive': "**Nota:** Una correlación positiva indica que las mujeres tienen una percepción **MÁS POSITIVA** sobre la inmigración que los hombres.",
                    'negative': "**Nota:** Una correlación negativa indica que los hombres tienen una percepción **MÁS POSITIVA** sobre la inmigración que las mujeres."
                },
                'wsekpwr': {
                    'positive': "**Nota:** Una correlación positiva indica que las mujeres están **MÁS DE ACUERDO** con que las mujeres buscan tener más poder que los hombres.",
                    'negative': "**Nota:** Una correlación negativa indica que los hombres están **MÁS DE ACUERDO** con que las mujeres buscan tener más poder que los hombres."
                }
            }
            
            note_text = gender_notes[selected_var]['positive'] if corr > 0 else gender_notes[selected_var]['negative']
            
            # Verde para correlación positiva, rojo para negativa
            if corr > 0:
                st.success(note_text)  # Verde
            else:
                st.error(note_text)  # Rojo
        
        # Gráfico de frecuencias por género
        fig_gender = create_gender_frequency_histogram(
            df_filtered,
            selected_var,
            f"Distribución por Género - {DEPENDENT_VARS[selected_var]}"
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    else:
        st.warning("⚠️ Datos insuficientes para análisis por género.")

# --- TAB 3: ANÁLISIS POR EDAD ---
with tab3:
    st.subheader(f"{DEPENDENT_VARS[selected_var]} por Edad")
    
    # Realizar análisis de edad
    age_analysis = perform_age_correlation(df_filtered, selected_var)
    
    if 'error' not in age_analysis:
        # KPIs en una sola fila
        age_gradient = data_loader.calculate_age_gradient(df_filtered, selected_var)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Correlación con Edad", f"{age_analysis['correlation']:.3f}")
        with col2:
            st.metric("Fuerza", age_analysis['strength'])
        with col3:
            st.metric("Gradiente (Jóvenes-Mayores)", f"{age_gradient:.3f}")
        with col4:
            significacion = "Sí (p < 0.05)" if age_analysis['significant'] else "No (p ≥ 0.05)"
            st.metric("Significación", significacion)
        
        # Nota interpretativa personalizada por variable (en verde si negativa, rojo si positiva para edad)
        age_notes = {
            'ipeqopta': {
                'positive': "**Nota:** Una correlación positiva indica que las personas **MÁS MAYORES** apoyan **MÁS** la igualdad de oportunidades.",
                'negative': "**Nota:** Una correlación negativa indica que las personas **MÁS JÓVENES** apoyan **MÁS** la igualdad de oportunidades."
            },
            'eqpaybg': {
                'positive': "**Nota:** Una correlación positiva indica que las personas **MÁS MAYORES** apoyan **MÁS** la igualdad salarial.",
                'negative': "**Nota:** Una correlación negativa indica que las personas **MÁS JÓVENES** apoyan **MÁS** la igualdad salarial."
            },
            'polintr': {
                'positive': "**Nota:** Una correlación positiva indica que las personas **MÁS MAYORES** tienen **MÁS** interés en política.",
                'negative': "**Nota:** Una correlación negativa indica que las personas **MÁS JÓVENES** tienen **MÁS** interés en política."
            },
            'imwbcnt': {
                'positive': "**Nota:** Una correlación positiva indica que las personas **MÁS MAYORES** tienen una percepción **MÁS POSITIVA** sobre la inmigración.",
                'negative': "**Nota:** Una correlación negativa indica que las personas **MÁS JÓVENES** tienen una percepción **MÁS POSITIVA** sobre la inmigración."
            },
            'wsekpwr': {
                'positive': "**Nota:** Una correlación positiva indica que las personas **MÁS MAYORES** están **MÁS DE ACUERDO** con que las mujeres buscan tener más poder.",
                'negative': "**Nota:** Una correlación negativa indica que las personas **MÁS JÓVENES** están **MÁS DE ACUERDO** con que las mujeres buscan tener más poder."
            }
        }
        
        note_text = age_notes[selected_var]['positive'] if age_analysis['correlation'] > 0 else age_notes[selected_var]['negative']
        
        # Verde para correlación positiva, rojo para negativa
        if age_analysis['correlation'] > 0:
            st.success(note_text)  # Verde
        else:
            st.error(note_text)  # Rojo
        
        # Visualización
        fig_age = create_age_trend(
            df_filtered,
            selected_var,
            f"{DEPENDENT_VARS[selected_var]} por Tramo de Edad"
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    else:
        st.warning("⚠️ Datos insuficientes para análisis por edad.")

# --- TAB 4: ANÁLISIS POR EDUCACIÓN ---
with tab4:
    st.subheader(f"{DEPENDENT_VARS[selected_var]} por Nivel Educativo")
    
    # Realizar análisis educativo
    edu_analysis = perform_education_correlation(df_filtered, selected_var)
    
    if 'error' not in edu_analysis:
        # KPIs en una sola fila
        edu_gradient = data_loader.calculate_education_gradient(df_filtered, selected_var)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Correlación con Educación", f"{edu_analysis['correlation']:.3f}")
        with col2:
            st.metric("Fuerza", edu_analysis['strength'])
        with col3:
            st.metric("Gradiente (Q4-Q1)", f"{edu_gradient:.3f}")
        with col4:
            significacion = "Sí (p < 0.05)" if edu_analysis['significant'] else "No (p ≥ 0.05)"
            st.metric("Significación", significacion)
        
        # Nota interpretativa personalizada por variable (en verde si positiva, rojo si negativa)
        edu_notes = {
            'ipeqopta': {
                'positive': "**Nota:** Una correlación positiva indica que las personas con **MAYOR NIVEL EDUCATIVO** apoyan **MÁS** la igualdad de oportunidades.",
                'negative': "**Nota:** Una correlación negativa indica que las personas con **MENOR NIVEL EDUCATIVO** apoyan **MÁS** la igualdad de oportunidades."
            },
            'eqpaybg': {
                'positive': "**Nota:** Una correlación positiva indica que las personas con **MAYOR NIVEL EDUCATIVO** apoyan **MÁS** la igualdad salarial.",
                'negative': "**Nota:** Una correlación negativa indica que las personas con **MENOR NIVEL EDUCATIVO** apoyan **MÁS** la igualdad salarial."
            },
            'polintr': {
                'positive': "**Nota:** Una correlación positiva indica que las personas con **MAYOR NIVEL EDUCATIVO** tienen **MÁS** interés en política.",
                'negative': "**Nota:** Una correlación negativa indica que las personas con **MENOR NIVEL EDUCATIVO** tienen **MÁS** interés en política."
            },
            'imwbcnt': {
                'positive': "**Nota:** Una correlación positiva indica que las personas con **MAYOR NIVEL EDUCATIVO** tienen una percepción **MÁS POSITIVA** sobre la inmigración.",
                'negative': "**Nota:** Una correlación negativa indica que las personas con **MENOR NIVEL EDUCATIVO** tienen una percepción **MÁS POSITIVA** sobre la inmigración."
            },
            'wsekpwr': {
                'positive': "**Nota:** Una correlación positiva indica que las personas con **MAYOR NIVEL EDUCATIVO** están **MÁS DE ACUERDO** con que las mujeres buscan tener más poder.",
                'negative': "**Nota:** Una correlación negativa indica que las personas con **MENOR NIVEL EDUCATIVO** están **MÁS DE ACUERDO** con que las mujeres buscan tener más poder."
            }
        }
        
        note_text = edu_notes[selected_var]['positive'] if edu_analysis['correlation'] > 0 else edu_notes[selected_var]['negative']
        
        if edu_analysis['correlation'] > 0:
            st.success(note_text)  # Verde si correlación positiva (mayor educación = más apoyo)
        else:
            st.error(note_text)  # Rojo si correlación negativa
        
        # Visualización
        fig_edu = create_education_trend(
            df_filtered,
            selected_var,
            f"{DEPENDENT_VARS[selected_var]} por Nivel Educativo"
        )
        st.plotly_chart(fig_edu, use_container_width=True)
    
    else:
        st.warning("⚠️ Datos insuficientes para análisis educativo.")

# --- TAB 5: ANÁLISIS POR PAÍS ---
with tab5:
    st.subheader(f"{DEPENDENT_VARS[selected_var]} por País")
    
    # Mapa coroplético - ampliado a ancho completo sin columnas laterales
    st.markdown("### 🗺️ Mapa de Europa")
    fig_map = create_country_map(
        df_filtered,
        selected_var,
        f"{DEPENDENT_VARS[selected_var]} por País"
    )
    # Usar contenedor completo sin restricciones para maximizar el ancho del mapa
    st.plotly_chart(fig_map, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['select2d', 'lasso2d']
    })
    
    # Ranking de países
    st.markdown("### 🏆 Ranking de Países")
    
    top_countries, bottom_countries = data_loader.get_country_ranking(
        df_filtered,
        selected_var,
        top_n=5
    )
    
    if not top_countries.empty and not bottom_countries.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top 5 Países**")
            st.dataframe(
                top_countries[['country_name', 'mean', 'count']].rename(columns={
                    'country_name': 'País',
                    'mean': 'Media',
                    'count': 'N'
                }),
                hide_index=True,
                use_container_width=True
            )
        
        with col2:
            st.markdown("**Bottom 5 Países**")
            st.dataframe(
                bottom_countries[['country_name', 'mean', 'count']].rename(columns={
                    'country_name': 'País',
                    'mean': 'Media',
                    'count': 'N'
                }),
                hide_index=True,
                use_container_width=True
            )
        
        # Gráfico comparativo
        fig_top_bottom = create_top_bottom_chart(
            top_countries,
            bottom_countries,
            selected_var,
            f"Top 5 y Bottom 5 Países - {DEPENDENT_VARS[selected_var]}"
        )
        st.plotly_chart(fig_top_bottom, use_container_width=True)
    
    else:
        st.warning("⚠️ Datos insuficientes para ranking de países.")


# ============================================================================
# SECCIÓN: ANÁLISIS ESPAÑA (IDEOLOGÍA Y PARTIDOS)
# ============================================================================

if 'ES' in df_filtered['cntry'].values:
    st.markdown('<a id="an-lisis-espec-fico-espa-a"></a>', unsafe_allow_html=True)
    render_section_header(
        "Análisis Específico: España",
        "Análisis de actitudes por partido político, ideología y nacionalismo",
        "🟥🟨🟥"
    )
    
    # Filtrar solo España
    df_spain = df_filtered[df_filtered['cntry'] == 'ES'].copy()
    
    if len(df_spain) >= 30:
        # Selector de variable
        selected_var_spain = render_variable_selector(DEPENDENT_VARS, key="spain_var_select")
        
        # Tabs para análisis España
        tab_spain1, tab_spain2, tab_spain3 = st.tabs([
            "🗳️ Por Partido",
            "⬅️➡️ Por Ideología",
            "🏴 Por Nacionalismo"
        ])
        
        # --- TAB: POR PARTIDO ---
        with tab_spain1:
            st.subheader(f"{DEPENDENT_VARS[selected_var_spain]} por Partido Político")
            
            fig_party = create_party_bar_chart(
                df_spain,
                selected_var_spain,
                f"{DEPENDENT_VARS[selected_var_spain]} por Partido"
            )
            st.plotly_chart(fig_party, use_container_width=True)
            
            # Estadísticas por partido
            party_stats = calculate_group_statistics(
                df_spain[df_spain['party_name'].notna()],
                selected_var_spain,
                'party_name'
            )
            
            st.markdown("### Estadísticas por Partido")
            st.dataframe(
                party_stats.rename(columns={
                    'party_name': 'Partido',
                    'count': 'N',
                    'mean': 'Media',
                    'median': 'Mediana',
                    'std': 'Desv. Est.',
                    'min': 'Mínimo',
                    'max': 'Máximo'
                }),
                hide_index=True,
                use_container_width=True
            )
        
        # --- TAB: POR IDEOLOGÍA ---
        with tab_spain2:
            st.subheader(f"{DEPENDENT_VARS[selected_var_spain]} por Ideología")
            
            # Verificar datos suficientes
            if df_spain['ideology'].notna().sum() >= 10:
                # Calcular correlación y gradiente ideológico
                corr, pval = calculate_spearman_correlation(df_spain, 'ideology', selected_var_spain)
                ideo_gradient = calculate_ideology_gradient(df_spain, selected_var_spain)
                
                # Métricas en una fila
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Gradiente Ideológico", f"{ideo_gradient:.3f}")
                with col2:
                    st.metric("Correlación con Ideología", f"{corr:.3f}")
                with col3:
                    st.metric("Fuerza", interpret_correlation_strength(corr))
                with col4:
                    significacion = "Sí (p < 0.05)" if pval < 0.05 else "No (p ≥ 0.05)"
                    st.metric("Significación", significacion)
                
                # Nota interpretativa personalizada por variable
                ideology_notes = {
                    'ipeqopta': {
                        'positive': "**Nota:** Una correlación positiva indica que los votantes de **DERECHA** apoyan **MÁS** la igualdad de oportunidades.",
                        'negative': "**Nota:** Una correlación negativa indica que los votantes de **IZQUIERDA** apoyan **MÁS** la igualdad de oportunidades."
                    },
                    'eqpaybg': {
                        'positive': "**Nota:** Una correlación positiva indica que los votantes de **DERECHA** apoyan **MÁS** la igualdad salarial.",
                        'negative': "**Nota:** Una correlación negativa indica que los votantes de **IZQUIERDA** apoyan **MÁS** la igualdad salarial."
                    },
                    'polintr': {
                        'positive': "**Nota:** Una correlación positiva indica que los votantes de **DERECHA** tienen **MÁS** interés en política.",
                        'negative': "**Nota:** Una correlación negativa indica que los votantes de **IZQUIERDA** tienen **MÁS** interés en política."
                    },
                    'imwbcnt': {
                        'positive': "**Nota:** Una correlación positiva indica que los votantes de **DERECHA** tienen una percepción **MÁS POSITIVA** sobre la inmigración.",
                        'negative': "**Nota:** Una correlación negativa indica que los votantes de **IZQUIERDA** tienen una percepción **MÁS POSITIVA** sobre la inmigración."
                    },
                    'wsekpwr': {
                        'positive': "**Nota:** Una correlación positiva indica que los votantes de **DERECHA** perciben **MÁS** control de las mujeres sobre los hombres.",
                        'negative': "**Nota:** Una correlación negativa indica que los votantes de **IZQUIERDA** perciben **MÁS** control de las mujeres sobre los hombres."
                    }
                }
                
                note_text = ideology_notes[selected_var_spain]['positive'] if corr > 0 else ideology_notes[selected_var_spain]['negative']
                
                # Verde para correlación positiva, rojo para negativa
                if corr > 0:
                    st.success(note_text)  # Verde
                else:
                    st.error(note_text)  # Rojo
                
                # Tabla de clasificación de partidos por ideología
                with st.expander("📋 Ver clasificación de partidos por ideología"):
                    st.markdown("**Escala ideológica asignada a cada partido (1=Izquierda, 5=Derecha):**")
                    
                    ideology_data = {
                        'Partido': ['SUMAR', 'ERC', 'EH-Bildu', 'BNG', 'PSOE', 'PACMA', 
                                   'EAJ-PNV', 'Coalición Canaria', 'PP', 'JuntsxCat', 'UPN', 'VOX'],
                        'Ideología': [1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5],
                        'Clasificación': ['Izquierda', 'Izquierda nacionalista', 'Izquierda nacionalista', 
                                         'Izquierda nacionalista', 'Centroizquierda', 'Centroizquierda ecologista',
                                         'Centroderecha nacionalista', 'Centroderecha regionalista', 
                                         'Derecha', 'Derecha nacionalista', 'Derecha regionalista', 'Derecha radical']
                    }
                    st.table(pd.DataFrame(ideology_data))
                
                # Dispersograma
                fig_ideo = create_ideology_scatter(
                    df_spain,
                    selected_var_spain,
                    f"{DEPENDENT_VARS[selected_var_spain]} vs Ideología"
                )
                st.plotly_chart(fig_ideo, use_container_width=True)
            else:
                st.warning("⚠️ Datos insuficientes para análisis de ideología.")
        
        # --- TAB: POR NACIONALISMO ---
        with tab_spain3:
            st.subheader(f"{DEPENDENT_VARS[selected_var_spain]} por Nacionalismo")
            
            # Verificar datos suficientes
            if df_spain['nationalism'].notna().sum() >= 10:
                # Calcular correlación
                corr, pval = calculate_spearman_correlation(df_spain, 'nationalism', selected_var_spain)
                
                # Calcular gradiente nacionalista (similar a ideológico)
                # Gradiente = diferencia entre Q4 (alto nacionalismo) y Q1 (bajo nacionalismo)
                df_nat_valid = df_spain[['nationalism', selected_var_spain]].dropna()
                if len(df_nat_valid) >= 20:
                    q1 = df_nat_valid['nationalism'].quantile(0.25)
                    q4 = df_nat_valid['nationalism'].quantile(0.75)
                    mean_low_nat = df_nat_valid[df_nat_valid['nationalism'] <= q1][selected_var_spain].mean()
                    mean_high_nat = df_nat_valid[df_nat_valid['nationalism'] >= q4][selected_var_spain].mean()
                    nat_gradient = mean_high_nat - mean_low_nat
                else:
                    nat_gradient = 0
                
                # Métricas en una fila
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Gradiente Nacionalista", f"{nat_gradient:.3f}")
                with col2:
                    st.metric("Correlación con Nacionalismo", f"{corr:.3f}")
                with col3:
                    st.metric("Fuerza", interpret_correlation_strength(corr))
                with col4:
                    significacion = "Sí (p < 0.05)" if pval < 0.05 else "No (p ≥ 0.05)"
                    st.metric("Significación", significacion)
                
                # Nota interpretativa personalizada por variable
                nationalism_notes = {
                    'ipeqopta': {
                        'positive': "**Nota:** Una correlación positiva indica que las personas con **MAYOR NACIONALISMO** apoyan **MÁS** la igualdad de oportunidades.",
                        'negative': "**Nota:** Una correlación negativa indica que las personas con **MENOR NACIONALISMO** apoyan **MÁS** la igualdad de oportunidades."
                    },
                    'eqpaybg': {
                        'positive': "**Nota:** Una correlación positiva indica que las personas con **MAYOR NACIONALISMO** apoyan **MÁS** la igualdad salarial.",
                        'negative': "**Nota:** Una correlación negativa indica que las personas con **MENOR NACIONALISMO** apoyan **MÁS** la igualdad salarial."
                    },
                    'polintr': {
                        'positive': "**Nota:** Una correlación positiva indica que las personas con **MAYOR NACIONALISMO** tienen **MÁS** interés en política.",
                        'negative': "**Nota:** Una correlación negativa indica que las personas con **MENOR NACIONALISMO** tienen **MÁS** interés en política."
                    },
                    'imwbcnt': {
                        'positive': "**Nota:** Una correlación positiva indica que las personas con **MAYOR NACIONALISMO** tienen una percepción **MÁS POSITIVA** sobre la inmigración.",
                        'negative': "**Nota:** Una correlación negativa indica que las personas con **MENOR NACIONALISMO** tienen una percepción **MÁS POSITIVA** sobre la inmigración."
                    },
                    'wsekpwr': {
                        'positive': "**Nota:** Una correlación positiva indica que las personas con **MAYOR NACIONALISMO** perciben **MÁS** control de las mujeres sobre los hombres.",
                        'negative': "**Nota:** Una correlación negativa indica que las personas con **MENOR NACIONALISMO** perciben **MÁS** control de las mujeres sobre los hombres."
                    }
                }
                
                note_text = nationalism_notes[selected_var_spain]['positive'] if corr > 0 else nationalism_notes[selected_var_spain]['negative']
                
                # Verde para correlación positiva, rojo para negativa
                if corr > 0:
                    st.success(note_text)  # Verde
                else:
                    st.error(note_text)  # Rojo
                
                # Tabla de clasificación de partidos por nacionalismo
                with st.expander("📋 Ver clasificación de partidos por nacionalismo"):
                    st.markdown("**Escala de nacionalismo asignada a cada partido (1=Bajo, 5=Alto):**")
                    
                    nationalism_data = {
                        'Partido': ['PP', 'PSOE', 'VOX', 'SUMAR', 'PACMA', 'Coalición Canaria', 'UPN', 
                                   'EAJ-PNV', 'BNG', 'ERC', 'JuntsxCat', 'EH-Bildu'],
                        'Nacionalismo': [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4],
                        'Tipo': ['No nacionalista', 'No nacionalista', 'No nacionalista', 
                                'No nacionalista', 'No nacionalista', 'Regionalista moderado', 'Regionalista moderado',
                                'Nacionalista', 'Nacionalista', 
                                'Independentista', 'Independentista', 'Independentista']
                    }
                    st.table(pd.DataFrame(nationalism_data))
                
                # Dispersograma nacionalismo
                fig_nat = create_ideology_scatter(
                    df_spain,
                    selected_var_spain,
                    f"{DEPENDENT_VARS[selected_var_spain]} vs Nacionalismo",
                    x_var='nationalism'
                )
                st.plotly_chart(fig_nat, use_container_width=True)
            else:
                st.warning("⚠️ Datos insuficientes para análisis de nacionalismo.")
    
    else:
        st.warning("⚠️ Datos insuficientes de España en la selección actual.")


# ============================================================================
# SECCIÓN: MATRIZ DE CORRELACIONES
# ============================================================================

st.markdown('<a id="matriz-de-correlaci-n"></a>', unsafe_allow_html=True)
render_section_header(
    "Matriz de Correlaciones",
    "Análisis de correlaciones entre todas las variables dependientes (Spearman)",
    "📈"
)

# Crear matriz de correlación
variables_for_corr = list(DEPENDENT_VARS.keys())
available_vars = [v for v in variables_for_corr if v in df_filtered.columns]

if len(available_vars) >= 2:
    fig_corr = create_correlation_heatmap(
        df_filtered,
        available_vars,
        "Matriz de Correlación (Spearman)"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.info("""
    💡 **Interpretación:**
    - Valores cercanos a **1** (rojo): correlación positiva fuerte
    - Valores cercanos a **-1** (azul): correlación negativa fuerte
    - Valores cercanos a **0** (blanco): sin correlación
    """)
    
    # =========================================================================
    # INTERPRETACIONES DESTACADAS
    # =========================================================================
    st.markdown("### � INTERPRETACIONES DESTACADAS")
    
    # Calcular todas las correlaciones con p-values
    df_multivar = df_filtered[available_vars].dropna()
    
    if len(df_multivar) >= 10:
        interpretations = []
        
        for i, var1 in enumerate(available_vars):
            for j, var2 in enumerate(available_vars):
                if i < j:  # Solo pares únicos (evitar duplicados y diagonal)
                    corr, pval = calculate_spearman_correlation(df_multivar, var1, var2)
                    
                    # Solo mostrar correlaciones significativas Y con valor absoluto > 0.1
                    if pval < 0.05 and abs(corr) > 0.1:
                        # Determinar fuerza
                        abs_corr = abs(corr)
                        if abs_corr < 0.20:
                            fuerza = "MUY DÉBIL"
                        elif abs_corr < 0.40:
                            fuerza = "DÉBIL"
                        elif abs_corr < 0.60:
                            fuerza = "MODERADA"
                        elif abs_corr < 0.80:
                            fuerza = "FUERTE"
                        else:
                            fuerza = "MUY FUERTE"
                        
                        # Significancia
                        if pval < 0.001:
                            sig = "***"
                        elif pval < 0.01:
                            sig = "**"
                        else:
                            sig = "*"
                        
                        interpretations.append({
                            'var1': var1,
                            'var2': var2,
                            'corr': corr,
                            'pval': pval,
                            'fuerza': fuerza,
                            'sig': sig,
                            'abs_corr': abs_corr
                        })
        
        # Ordenar por valor absoluto de correlación (de mayor a menor)
        interpretations.sort(key=lambda x: x['abs_corr'], reverse=True)
        
        if interpretations:
            for interp in interpretations:
                var1_name = DEPENDENT_VARS[interp['var1']]
                var2_name = DEPENDENT_VARS[interp['var2']]
                
                # Formato compacto sin columnas
                st.markdown(f"""
                ✓ **{var1_name}** vs **{var2_name}**: Correlación = **{interp['corr']:.4f}** ({interp['fuerza']}) | p-value: {interp['pval']:.4e} {interp['sig']}
                """)
        else:
            st.info("ℹ️ No se encontraron correlaciones significativas mayores a 0.1 entre las variables.")
    else:
        st.warning("⚠️ Datos insuficientes para calcular correlaciones significativas.")
else:
    st.warning("⚠️ Se necesitan al menos 2 variables para crear matriz de correlación.")


# ============================================================================
# SECCIÓN: CONCLUSIONES
# ============================================================================

st.markdown('<a id="conclusiones-clave"></a>', unsafe_allow_html=True)
render_section_header(
    "Conclusiones Clave",
    "Hallazgos principales del análisis exploratorio",
    "💡"
)

st.markdown("""
### 🎯 Hallazgos Principales

Basándose en el análisis exploratorio de datos del ESS11, se identifican los siguientes patrones clave:

#### 1. **Igualdad de Oportunidades (ipeqopta)**
- ✅ **Mayor apoyo entre mujeres**, jóvenes y personas con mayor nivel educativo
- ✅ **Gradiente ideológico claro**: mayor apoyo en votantes de izquierda (SUMAR, ERC, EH-Bildu, BNG)
- ✅ **Variabilidad significativa entre países**: patrones regionales evidentes
- 🔍 **En España**: correlación negativa con ideología (izquierda apoya más) y con nacionalismo

#### 2. **Igualdad Salarial (eqpaybg)**
- ✅ **Brecha de género consistente**: las mujeres muestran mayor apoyo
- ✅ **Efecto generacional**: los jóvenes apoyan más la igualdad salarial
- ✅ **Educación como predictor fuerte**: a mayor educación, mayor apoyo
- 🔍 **En España**: correlación negativa con ideología (izquierda apoya más)

#### 3. **Interés Político (polintr)**
- ⚠️ **Brecha de género persistente**: los hombres declaran mayor interés
- ✅ **Pico en edades medias** (45-64 años)
- ✅ **Fuerte correlación con educación**: la educación predice el compromiso político
- 🔍 **En España**: el interés político varía según contexto, con mayor participación en partidos nacionalistas

#### 4. **Percepción sobre Inmigración (imwbcnt)**
- ✅ **Cambio generacional evidente**: los jóvenes tienen actitudes más favorables
- ✅ **Educación como factor crítico**: a mayor educación, percepciones más positivas
- ✅ **Correlación negativa con nacionalismo**: menor nacionalismo predice actitudes más favorables
- 🔍 **En España**: votantes de izquierda y partidos no nacionalistas (PP, PSOE, VOX, SUMAR, PACMA) muestran percepciones más positivas

#### 5. **Relaciones de Género (wsekpwr)**
- ⚠️ **Brecha de género muy significativa**: los hombres muestran mayor acuerdo
- ✅ **Efecto de la educación**: la educación reduce creencias sobre dinámicas de control
- ✅ **Relevancia para políticas de igualdad**: indicador crítico de actitudes subyacentes
- 🔍 **En España**: correlación positiva con ideología de derecha y con nacionalismo

### 📊 Implicaciones para Políticas Públicas

1. **Educación como palanca de cambio**: La educación emerge como predictor consistente de actitudes 
   favorables hacia la igualdad en múltiples dimensiones.

2. **Brechas generacionales**: Los datos sugieren cambios actitudinales positivos en cohortes más jóvenes,
   pero también desafíos en la participación política juvenil.

3. **Variabilidad entre países**: La heterogeneidad entre países sugiere que las políticas y contextos
   nacionales importan significativamente.

4. **Persistencia de brechas de género**: Las diferencias de género en actitudes y participación política
   requieren intervenciones específicas.

### 🔮 Próximos Pasos

- **Análisis multivariante**: Modelos de regresión para aislar efectos independientes
- **Análisis longitudinal**: Comparación con rondas anteriores del ESS para tendencias temporales
- **Segmentación avanzada**: Análisis de clusters para identificar tipologías de países/grupos
""")


# ============================================================================
# METODOLOGÍA Y FOOTER
# ============================================================================

render_methodology_expander()
render_footer()
