"""
Módulo de análisis estadístico.
Funciones para calcular correlaciones, pruebas estadísticas y métricas.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Tuple, Dict


def calculate_spearman_correlation(df: pd.DataFrame, var1: str, var2: str) -> Tuple[float, float]:
    """
    Calcula la correlación de Spearman entre dos variables.
    
    Args:
        df: DataFrame con los datos
        var1: Primera variable
        var2: Segunda variable
        
    Returns:
        Tupla (correlación, p-value)
    """
    data = df[[var1, var2]].dropna()
    
    if len(data) < 10:
        return np.nan, np.nan
    
    correlation, pvalue = stats.spearmanr(data[var1], data[var2])
    
    return correlation, pvalue


def interpret_correlation_strength(correlation: float) -> str:
    """
    Interpreta la fuerza de una correlación.
    
    Args:
        correlation: Valor de correlación (-1 a 1)
        
    Returns:
        Descripción textual de la fuerza
    """
    abs_corr = abs(correlation)
    
    if abs_corr >= 0.7:
        return "Muy fuerte"
    elif abs_corr >= 0.5:
        return "Fuerte"
    elif abs_corr >= 0.3:
        return "Moderada"
    elif abs_corr >= 0.1:
        return "Débil"
    else:
        return "Muy débil"


def test_normality(df: pd.DataFrame, variable: str) -> Dict[str, any]:
    """
    Realiza test de normalidad de Shapiro-Wilk.
    
    Args:
        df: DataFrame con los datos
        variable: Variable a testear
        
    Returns:
        Diccionario con resultados del test
    """
    data = df[variable].dropna()
    
    if len(data) < 10:
        return {
            'test': 'Shapiro-Wilk',
            'statistic': np.nan,
            'pvalue': np.nan,
            'is_normal': None,
            'message': 'Datos insuficientes'
        }
    
    # Shapiro-Wilk solo funciona con muestras <= 5000
    if len(data) > 5000:
        data = data.sample(5000, random_state=42)
    
    statistic, pvalue = stats.shapiro(data)
    
    return {
        'test': 'Shapiro-Wilk',
        'statistic': statistic,
        'pvalue': pvalue,
        'is_normal': pvalue > 0.05,
        'message': f"p-value = {pvalue:.4f} ({'Normal' if pvalue > 0.05 else 'No normal'})"
    }


def calculate_group_statistics(df: pd.DataFrame, variable: str, 
                               group_by: str) -> pd.DataFrame:
    """
    Calcula estadísticas por grupo.
    
    Args:
        df: DataFrame con los datos
        variable: Variable dependiente
        group_by: Variable de agrupación
        
    Returns:
        DataFrame con estadísticas por grupo
    """
    stats_df = df.groupby(group_by)[variable].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max')
    ]).reset_index()
    
    return stats_df


def calculate_top2_box(df: pd.DataFrame, variable: str, 
                       top_values: list = [5, 6]) -> float:
    """
    Calcula el porcentaje de Top-2 Box (dos valores más altos).
    
    Args:
        df: DataFrame con los datos
        variable: Variable a analizar
        top_values: Valores considerados "top" (por defecto 5 y 6)
        
    Returns:
        Porcentaje de Top-2 Box
    """
    data = df[variable].dropna()
    
    if len(data) == 0:
        return np.nan
    
    top2_count = data.isin(top_values).sum()
    top2_percentage = (top2_count / len(data)) * 100
    
    return top2_percentage


def calculate_confidence_interval(data: pd.Series, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Calcula el intervalo de confianza para una media.
    
    Args:
        data: Serie de datos
        confidence: Nivel de confianza (por defecto 95%)
        
    Returns:
        Tupla (límite inferior, límite superior)
    """
    data = data.dropna()
    
    if len(data) < 10:
        return np.nan, np.nan
    
    mean = data.mean()
    std_error = stats.sem(data)
    margin_error = std_error * stats.t.ppf((1 + confidence) / 2, len(data) - 1)
    
    return mean - margin_error, mean + margin_error


def perform_gender_comparison(df: pd.DataFrame, variable: str) -> Dict[str, any]:
    """
    Realiza un análisis comparativo completo por género.
    
    Args:
        df: DataFrame con los datos
        variable: Variable dependiente a analizar
        
    Returns:
        Diccionario con resultados del análisis
    """
    male_data = df[df['gndr'] == 1][variable].dropna()
    female_data = df[df['gndr'] == 2][variable].dropna()
    
    if len(male_data) < 10 or len(female_data) < 10:
        return {'error': 'Datos insuficientes'}
    
    # Test de Mann-Whitney U (no paramétrico)
    u_stat, p_value = stats.mannwhitneyu(male_data, female_data, alternative='two-sided')
    
    return {
        'male_mean': male_data.mean(),
        'female_mean': female_data.mean(),
        'male_median': male_data.median(),
        'female_median': female_data.median(),
        'gap': female_data.mean() - male_data.mean(),
        'u_statistic': u_stat,
        'p_value': p_value,
        'significant': p_value < 0.05
    }


def perform_age_correlation(df: pd.DataFrame, variable: str) -> Dict[str, any]:
    """
    Analiza la correlación entre edad y una variable.
    
    Args:
        df: DataFrame con los datos
        variable: Variable dependiente
        
    Returns:
        Diccionario con resultados del análisis
    """
    data = df[['agea', variable]].dropna()
    
    if len(data) < 10:
        return {'error': 'Datos insuficientes'}
    
    corr, pval = stats.spearmanr(data['agea'], data[variable])
    
    return {
        'correlation': corr,
        'p_value': pval,
        'strength': interpret_correlation_strength(corr),
        'significant': pval < 0.05,
        'direction': 'positiva' if corr > 0 else 'negativa'
    }


def perform_education_correlation(df: pd.DataFrame, variable: str) -> Dict[str, any]:
    """
    Analiza la correlación entre nivel educativo y una variable.
    
    Args:
        df: DataFrame con los datos
        variable: Variable dependiente
        
    Returns:
        Diccionario con resultados del análisis
    """
    data = df[['education_level', variable]].dropna()
    
    if len(data) < 10:
        return {'error': 'Datos insuficientes'}
    
    corr, pval = stats.spearmanr(data['education_level'], data[variable])
    
    return {
        'correlation': corr,
        'p_value': pval,
        'strength': interpret_correlation_strength(corr),
        'significant': pval < 0.05,
        'direction': 'positiva' if corr > 0 else 'negativa'
    }


def calculate_ideology_gradient(df: pd.DataFrame, variable: str) -> float:
    """
    Calcula el gradiente ideológico (izquierda vs derecha).
    
    Args:
        df: DataFrame con los datos (solo España)
        variable: Variable dependiente
        
    Returns:
        Gradiente ideológico (izquierda - derecha)
    """
    df_spain = df[(df['cntry'] == 'ES') & df['ideology'].notna() & df[variable].notna()]
    
    if len(df_spain) < 10:
        return np.nan
    
    left_mean = df_spain[df_spain['ideology'] <= 2][variable].mean()
    right_mean = df_spain[df_spain['ideology'] >= 4][variable].mean()
    
    return left_mean - right_mean


def generate_summary_statistics(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """
    Genera un resumen completo de estadísticas para una variable.
    
    Args:
        df: DataFrame con los datos
        variable: Variable a analizar
        
    Returns:
        DataFrame con resumen de estadísticas
    """
    data = df[variable].dropna()
    
    summary = {
        'Observaciones': len(data),
        'Media': data.mean(),
        'Mediana': data.median(),
        'Desviación Estándar': data.std(),
        'Mínimo': data.min(),
        'Q1 (25%)': data.quantile(0.25),
        'Q2 (50%)': data.quantile(0.50),
        'Q3 (75%)': data.quantile(0.75),
        'Máximo': data.max(),
        'Rango': data.max() - data.min(),
        'IQR': data.quantile(0.75) - data.quantile(0.25)
    }
    
    summary_df = pd.DataFrame([summary]).T
    summary_df.columns = ['Valor']
    
    return summary_df
