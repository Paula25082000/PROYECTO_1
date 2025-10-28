"""
Componentes de visualización con Plotly Express.
Contiene funciones para crear gráficos interactivos reutilizables.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
from config import (
    COLOR_PALETTE, PLOTLY_CONFIG, PLOTLY_TEMPLATE,
    ISO2_TO_ISO3
)


def create_distribution_histogram(df: pd.DataFrame, variable: str, 
                                  title: str = None) -> go.Figure:
    """
    Crea un histograma de distribución de una variable.
    
    Args:
        df: DataFrame con los datos
        variable: Variable a visualizar
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    if title is None:
        title = f"Distribución de {variable}"
    
    fig = px.histogram(
        df, 
        x=variable,
        nbins=30,
        title=title,
        labels={variable: variable},
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=[COLOR_PALETTE['primary']]
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_title=variable,
        yaxis_title="Frecuencia"
    )
    
    return fig


def create_gender_frequency_histogram(df: pd.DataFrame, variable: str, 
                                       title: str = None) -> go.Figure:
    """
    Crea un histograma de frecuencias por género (hombres vs mujeres) en porcentaje.
    
    Args:
        df: DataFrame con los datos
        variable: Variable a visualizar
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    if title is None:
        title = f"Distribución de {variable} por Género"
    
    df_plot = df[['gender_label', variable]].dropna()
    
    fig = px.histogram(
        df_plot,
        x=variable,
        color='gender_label',
        nbins=20,
        title=title,
        labels={'gender_label': 'Género', variable: variable},
        template=PLOTLY_TEMPLATE,
        color_discrete_map={
            'Hombre': COLOR_PALETTE['gender_male'],
            'Mujer': COLOR_PALETTE['gender_female']
        },
        barmode='overlay',  # Superponer para mejor comparación
        opacity=0.7,
        histnorm='percent'  # Normalizar a porcentajes
    )
    
    fig.update_layout(
        xaxis_title=variable,
        yaxis_title="Porcentaje de Respuestas (%)",
        legend_title="Género"
    )
    
    return fig


def create_gender_comparison(df: pd.DataFrame, variable: str, 
                             title: str = None) -> go.Figure:
    """
    Crea un gráfico de comparación por género (boxplot).
    
    Args:
        df: DataFrame con los datos
        variable: Variable dependiente a comparar
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    if title is None:
        title = f"{variable} por Género"
    
    df_plot = df[['gender_label', variable]].dropna()
    
    fig = px.box(
        df_plot,
        x='gender_label',
        y=variable,
        title=title,
        labels={'gender_label': 'Género', variable: variable},
        template=PLOTLY_TEMPLATE,
        color='gender_label',
        color_discrete_map={
            'Hombre': COLOR_PALETTE['gender_male'],
            'Mujer': COLOR_PALETTE['gender_female']
        }
    )
    
    fig.update_layout(showlegend=False)
    
    return fig


def create_age_trend(df: pd.DataFrame, variable: str, 
                    title: str = None) -> go.Figure:
    """
    Crea un gráfico de tendencia por tramos de edad.
    
    Args:
        df: DataFrame con los datos
        variable: Variable dependiente a analizar
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    if title is None:
        title = f"{variable} por Tramo de Edad"
    
    # Calcular medias por tramo de edad
    age_means = df.groupby('age_group', observed=True)[variable].agg(['mean', 'count']).reset_index()
    age_means = age_means[age_means['count'] >= 10]  # Filtro de muestra mínima
    
    fig = px.line(
        age_means,
        x='age_group',
        y='mean',
        title=title,
        labels={'age_group': 'Tramo de Edad', 'mean': f'Media de {variable}'},
        template=PLOTLY_TEMPLATE,
        markers=True
    )
    
    fig.update_traces(
        line_color=COLOR_PALETTE['primary'],
        line_width=3,
        marker=dict(size=10)
    )
    
    return fig


def create_education_trend(df: pd.DataFrame, variable: str,
                          title: str = None) -> go.Figure:
    """
    Crea un gráfico de tendencia por nivel educativo.
    
    Args:
        df: DataFrame con los datos
        variable: Variable dependiente a analizar
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    if title is None:
        title = f"{variable} por Nivel Educativo"
    
    # Calcular medias por nivel educativo
    edu_means = df.groupby('education_level')[variable].agg(['mean', 'count']).reset_index()
    edu_means = edu_means[edu_means['count'] >= 10]
    edu_means = edu_means.sort_values('education_level')
    
    fig = px.line(
        edu_means,
        x='education_level',
        y='mean',
        title=title,
        labels={'education_level': 'Nivel Educativo (0-26)', 'mean': f'Media de {variable}'},
        template=PLOTLY_TEMPLATE,
        markers=True
    )
    
    fig.update_traces(
        line_color=COLOR_PALETTE['success'],
        line_width=3,
        marker=dict(size=8)
    )
    
    return fig


def create_country_map(df: pd.DataFrame, variable: str,
                      title: str = None) -> go.Figure:
    """
    Crea un mapa coroplético europeo por país.
    
    Args:
        df: DataFrame con los datos
        variable: Variable dependiente a visualizar
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    if title is None:
        title = f"{variable} por País"
    
    # Calcular medias por país
    country_data = df.groupby(['country_iso3', 'country_name'])[variable].mean().reset_index()
    
    fig = px.choropleth(
        country_data,
        locations='country_iso3',
        color=variable,
        hover_name='country_name',
        title=title,
        scope='europe',
        color_continuous_scale='RdYlGn',
        labels={variable: f'Media {variable}'},
        template=PLOTLY_TEMPLATE
    )
    
    fig.update_geos(
        showcountries=True,
        countrycolor="lightgray",
        showcoastlines=True,
        coastlinecolor="gray"
    )
    
    fig.update_layout(
        height=700,  # Aumentado de 600 a 700 para mayor tamaño
        margin=dict(l=0, r=0, t=50, b=0),  # Márgenes reducidos para aprovechar el espacio
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='mercator',
            # Ajuste de la proyección para centrar y ampliar Europa
            projection_scale=1.5,  # Zoom aumentado para mayor visualización
            center=dict(lat=54, lon=15)  # Centrado en Europa
        )
    )
    
    return fig


def create_party_bar_chart(df: pd.DataFrame, variable: str,
                           title: str = None) -> go.Figure:
    """
    Crea un gráfico de barras por partido político (solo España).
    
    Args:
        df: DataFrame con los datos
        variable: Variable dependiente a visualizar
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    if title is None:
        title = f"{variable} por Partido Político (España)"
    
    # Filtrar solo España y calcular medias por partido
    df_spain = df[df['cntry'] == 'ES'].copy()
    party_means = df_spain.groupby('party_name')[variable].agg(['mean', 'count']).reset_index()
    party_means = party_means[party_means['count'] >= 10]
    party_means = party_means.sort_values('mean', ascending=True)
    
    fig = px.bar(
        party_means,
        y='party_name',
        x='mean',
        orientation='h',
        title=title,
        labels={'party_name': 'Partido', 'mean': f'Media de {variable}'},
        template=PLOTLY_TEMPLATE,
        color='mean',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        showlegend=False,
        height=500
    )
    
    return fig


def create_ideology_scatter(df: pd.DataFrame, variable: str,
                            title: str = None, x_var: str = 'ideology') -> go.Figure:
    """
    Crea un dispersograma de variable vs ideología/nacionalismo con línea de tendencia.
    
    Args:
        df: DataFrame con los datos (solo España)
        variable: Variable dependiente a analizar
        title: Título del gráfico
        x_var: Variable a usar en el eje X (por defecto 'ideology', también puede ser 'nationalism')
        
    Returns:
        Figura de Plotly
    """
    if title is None:
        title = f"{variable} vs Ideología"
    
    # Filtrar España y eliminar valores nulos
    df_spain = df[(df['cntry'] == 'ES') & df[x_var].notna() & df[variable].notna()].copy()
    
    if len(df_spain) < 10:
        # Si no hay suficientes datos, retornar gráfico vacío
        fig = go.Figure()
        fig.add_annotation(
            text="Datos insuficientes para España",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Calcular línea de tendencia
    z = np.polyfit(df_spain[x_var], df_spain[variable], 1)
    p = np.poly1d(z)
    
    # Etiquetas dinámicas según la variable
    x_label = 'Ideología (1=Izq, 5=Der)' if x_var == 'ideology' else 'Nacionalismo (1=Bajo, 5=Alto)'
    
    fig = px.scatter(
        df_spain,
        x=x_var,
        y=variable,
        title=title,
        labels={x_var: x_label, variable: variable},
        template=PLOTLY_TEMPLATE,
        opacity=0.5,
        color_discrete_sequence=[COLOR_PALETTE['primary']]
    )
    
    # Añadir línea de tendencia
    x_trend = np.linspace(df_spain[x_var].min(), df_spain[x_var].max(), 100)
    fig.add_trace(
        go.Scatter(
            x=x_trend,
            y=p(x_trend),
            mode='lines',
            name='Tendencia',
            line=dict(color=COLOR_PALETTE['warning'], width=3)
        )
    )
    
    return fig


def create_correlation_heatmap(df: pd.DataFrame, variables: list,
                               title: str = "Matriz de Correlación") -> go.Figure:
    """
    Crea un mapa de calor de correlaciones entre variables.
    
    Args:
        df: DataFrame con los datos
        variables: Lista de variables a correlacionar
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    # Calcular matriz de correlación de Spearman
    corr_matrix = df[variables].corr(method='spearman')
    
    fig = px.imshow(
        corr_matrix,
        text_auto='.2f',
        title=title,
        labels=dict(color="Correlación"),
        color_continuous_scale='RdBu',  # Rojo=positivo, Blanco=0, Azul=negativo
        aspect='auto',
        template=PLOTLY_TEMPLATE,
        zmin=-1,  # Forzar rango de -1 a 1
        zmax=1
    )
    
    fig.update_layout(
        height=600,
        width=800
    )
    
    return fig


def create_top_bottom_chart(top_df: pd.DataFrame, bottom_df: pd.DataFrame,
                            variable: str, title: str = None) -> go.Figure:
    """
    Crea un gráfico de barras combinado para Top y Bottom países.
    
    Args:
        top_df: DataFrame con los países top
        bottom_df: DataFrame con los países bottom
        variable: Variable visualizada
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    if title is None:
        title = f"Top 5 y Bottom 5 Países - {variable}"
    
    # Combinar datos
    top_df = top_df.copy()
    bottom_df = bottom_df.copy()
    top_df['type'] = 'Top 5'
    bottom_df['type'] = 'Bottom 5'
    
    combined = pd.concat([top_df, bottom_df])
    combined = combined.rename(columns={'mean': variable})
    
    fig = px.bar(
        combined,
        y='country_name',
        x=variable,
        color='type',
        orientation='h',
        title=title,
        labels={'country_name': 'País', variable: f'Media {variable}'},
        template=PLOTLY_TEMPLATE,
        color_discrete_map={
            'Top 5': COLOR_PALETTE['success'],
            'Bottom 5': COLOR_PALETTE['warning']
        }
    )
    
    fig.update_layout(height=500)
    
    return fig


def create_violin_plot(df: pd.DataFrame, variable: str, group_by: str,
                       title: str = None) -> go.Figure:
    """
    Crea un gráfico de violín para comparar distribuciones.
    
    Args:
        df: DataFrame con los datos
        variable: Variable dependiente a visualizar
        group_by: Variable de agrupación
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    if title is None:
        title = f"Distribución de {variable} por {group_by}"
    
    fig = px.violin(
        df,
        y=variable,
        x=group_by,
        title=title,
        labels={group_by: group_by, variable: variable},
        template=PLOTLY_TEMPLATE,
        color=group_by,
        box=True,
        points='outliers'
    )
    
    fig.update_layout(showlegend=False)
    
    return fig
