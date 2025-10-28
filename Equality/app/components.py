"""
Componentes reutilizables de la interfaz de Streamlit.
Incluye sidebar, métricas KPI, secciones, etc.
"""

import streamlit as st
import pandas as pd
from config import DEPENDENT_VARS, ISO2_TO_NAME, PARTY_NAMES


def render_sidebar(df: pd.DataFrame) -> dict:
    """
    Renderiza el menú lateral con filtros interactivos.
    
    Args:
        df: DataFrame con los datos limpios
        
    Returns:
        Diccionario con los filtros seleccionados
    """
    st.sidebar.title("🔍 Filtros")
    st.sidebar.markdown("---")
    
    filters = {}
    
    # Filtro por País
    st.sidebar.subheader("🌍 País")
    countries = ['Todos'] + sorted(df['country_name'].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Seleccionar países",
        options=countries,
        default=['Todos'],
        help="Selecciona uno o más países para filtrar"
    )
    
    if 'Todos' not in selected_countries and selected_countries:
        filters['country_name'] = selected_countries
    
    # Filtro por Género
    st.sidebar.subheader("👥 Género")
    gender_options = ['Todos', 'Hombre', 'Mujer']
    selected_gender = st.sidebar.radio(
        "Seleccionar género",
        options=gender_options,
        help="Filtra los datos por género"
    )
    
    if selected_gender != 'Todos':
        filters['gender_label'] = [selected_gender]
    
    # Filtro por Tramo de Edad
    st.sidebar.subheader("📅 Edad")
    age_groups = ['Todos'] + df['age_group'].dropna().unique().tolist()
    selected_age = st.sidebar.multiselect(
        "Seleccionar tramos de edad",
        options=age_groups,
        default=['Todos'],
        help="Filtra por grupos de edad"
    )
    
    if 'Todos' not in selected_age and selected_age:
        filters['age_group'] = selected_age
    
    # Filtro por Nivel Educativo (cuartiles)
    st.sidebar.subheader("🎓 Nivel Educativo")
    edu_q1 = df['education_level'].quantile(0.25)
    edu_q2 = df['education_level'].quantile(0.50)
    edu_q3 = df['education_level'].quantile(0.75)
    
    edu_option = st.sidebar.select_slider(
        "Nivel educativo",
        options=['Todos', 'Bajo (Q1)', 'Medio-Bajo (Q2)', 'Medio-Alto (Q3)', 'Alto (Q4)'],
        value='Todos',
        help="Filtra por cuartil educativo"
    )
    
    # Aplicar filtro educativo si no es "Todos"
    # (Se aplicará en la función de filtrado principal)
    filters['education_filter'] = edu_option
    
    # Filtro por Partido (solo para España)
    if 'ES' in df['cntry'].values:
        st.sidebar.subheader("🗳️ Partido (España)")
        parties = ['Todos'] + sorted(df[df['cntry'] == 'ES']['party_name'].dropna().unique().tolist())
        selected_parties = st.sidebar.multiselect(
            "Seleccionar partidos",
            options=parties,
            default=['Todos'],
            help="Solo para datos de España"
        )
        
        if 'Todos' not in selected_parties and selected_parties:
            filters['party_name'] = selected_parties
    
    # Información de datos filtrados
    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 **Datos disponibles:** {len(df):,} observaciones")
    
    return filters


def apply_education_filter(df: pd.DataFrame, edu_option: str) -> pd.DataFrame:
    """
    Aplica el filtro de nivel educativo basado en cuartiles.
    
    Args:
        df: DataFrame a filtrar
        edu_option: Opción de educación seleccionada
        
    Returns:
        DataFrame filtrado
    """
    if edu_option == 'Todos':
        return df
    
    q1 = df['education_level'].quantile(0.25)
    q2 = df['education_level'].quantile(0.50)
    q3 = df['education_level'].quantile(0.75)
    
    if edu_option == 'Bajo (Q1)':
        return df[df['education_level'] <= q1]
    elif edu_option == 'Medio-Bajo (Q2)':
        return df[(df['education_level'] > q1) & (df['education_level'] <= q2)]
    elif edu_option == 'Medio-Alto (Q3)':
        return df[(df['education_level'] > q2) & (df['education_level'] <= q3)]
    elif edu_option == 'Alto (Q4)':
        return df[df['education_level'] > q3]
    
    return df


def render_kpi_cards(kpis: dict):
    """
    Renderiza tarjetas de KPIs en columnas.
    
    Args:
        kpis: Diccionario con KPIs {nombre: valor}
    """
    num_kpis = len(kpis)
    cols = st.columns(num_kpis)
    
    for col, (kpi_name, kpi_value) in zip(cols, kpis.items()):
        with col:
            # Determinar color basado en el valor
            if isinstance(kpi_value, (int, float)):
                delta_color = "normal" if kpi_value >= 0 else "inverse"
                st.metric(
                    label=kpi_name,
                    value=f"{kpi_value:.3f}",
                    delta=None
                )
            else:
                st.metric(label=kpi_name, value=kpi_value)


def render_variable_selector(variables: dict, key: str = "var_select") -> str:
    """
    Renderiza un selector de variables dependientes.
    
    Args:
        variables: Diccionario de variables disponibles
        key: Key única para el widget
        
    Returns:
        Variable seleccionada
    """
    selected_var = st.selectbox(
        "Seleccionar variable a analizar:",
        options=list(variables.keys()),
        format_func=lambda x: variables[x],
        key=key,
        help="Selecciona la variable dependiente para el análisis"
    )
    
    return selected_var


def render_section_header(title: str, description: str = None, icon: str = "📊"):
    """
    Renderiza un encabezado de sección con estilo.
    
    Args:
        title: Título de la sección
        description: Descripción opcional
        icon: Emoji/icono para la sección
    """
    st.markdown(f"## {icon} {title}")
    
    if description:
        st.markdown(description)
    
    st.markdown("---")


def render_info_box(title: str, content: str, box_type: str = "info"):
    """
    Renderiza una caja de información con estilo.
    
    Args:
        title: Título de la caja
        content: Contenido de la caja
        box_type: Tipo de caja (info, warning, success, error)
    """
    if box_type == "info":
        st.info(f"**{title}**\n\n{content}")
    elif box_type == "warning":
        st.warning(f"**{title}**\n\n{content}")
    elif box_type == "success":
        st.success(f"**{title}**\n\n{content}")
    elif box_type == "error":
        st.error(f"**{title}**\n\n{content}")
    else:
        st.info(f"**{title}**\n\n{content}")


def render_stats_table(stats: dict, title: str = "Estadísticas Descriptivas"):
    """
    Renderiza una tabla de estadísticas descriptivas.
    
    Args:
        stats: Diccionario con estadísticas
        title: Título de la tabla
    """
    st.subheader(title)
    
    stats_df = pd.DataFrame([stats]).T
    stats_df.columns = ['Valor']
    stats_df.index.name = 'Estadística'
    
    st.dataframe(stats_df, use_container_width=True)


def render_data_quality_warning(df: pd.DataFrame, min_obs: int = 30):
    """
    Muestra una advertencia si hay pocos datos.
    
    Args:
        df: DataFrame filtrado
        min_obs: Número mínimo de observaciones
    """
    if len(df) < min_obs:
        st.warning(f"⚠️ **Advertencia:** El conjunto de datos filtrado tiene solo {len(df)} observaciones. "
                  f"Se recomienda tener al menos {min_obs} para análisis robustos.")


def create_download_button(df: pd.DataFrame, filename: str, button_text: str = "📥 Descargar datos"):
    """
    Crea un botón para descargar datos en formato CSV.
    
    Args:
        df: DataFrame a descargar
        filename: Nombre del archivo
        button_text: Texto del botón
    """
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label=button_text,
        data=csv,
        file_name=filename,
        mime='text/csv',
    )


def render_methodology_expander():
    """
    Renderiza un expander con información metodológica.
    """
    with st.expander("📖 Metodología y Notas Técnicas"):
        st.markdown("""
        ### Metodología de Análisis
        
        **Datos:** European Social Survey Round 11 (ESS11)
        
        **Limpieza de datos:**
        - Eliminación de valores inválidos según codebook ESS11
        - Inversión de escala de `ipeqopta` para interpretación intuitiva (más alto = más apoyo)
        - Creación de variables derivadas: `education_level`, `ideology`, `nationalism`
        
        **Variables dependientes:**
        - **ipeqopta**: Igualdad de oportunidades (1-6, invertida)
        - **eqpaybg**: Igualdad salarial
        - **polintr**: Interés en política
        - **imwbcnt**: Percepción sobre inmigración
        - **wsekpwr**: Percepción sobre control de género
        
        **Análisis estadístico:**
        - Correlaciones de Spearman (no paramétrico, dado que las variables no siguen distribución normal)
        - Análisis de brechas por género, edad y educación
        - Comparaciones por país con muestra mínima de 30 observaciones
        
        **KPIs principales:**
        - **Brecha de género**: Media(mujeres) - Media(hombres)
        - **Gradiente por edad**: Media(15-34) - Media(65+)
        - **Gradiente educativo**: Media(Q4) - Media(Q1)
        - **Gradiente ideológico**: Media(izquierda) - Media(derecha)
        
        ### Referencias
        - European Social Survey (2023). ESS Round 11 Data.
        - Documentación técnica en `docs/EDA.md`
        """)


def render_footer():
    """
    Renderiza el pie de página de la aplicación.
    """
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p><strong>Panel ESS11: Igualdad y Sociedad en Europa</strong></p>
        <p>Desarrollado con Streamlit, Pandas y Plotly</p>
        <p>Fuente de datos: European Social Survey Round 11</p>
    </div>
    """, unsafe_allow_html=True)
