"""
Módulo de carga y preprocesamiento de datos.
Gestiona la lectura del CSV, limpieza de valores inválidos y transformaciones.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st
from config import (
    DATA_FILE, INVALID_VALUES, EDUCATION_SCALE, 
    IDEOLOGY_SCALE, NATIONALISM_SCALE, PARTY_NAMES,
    ISO2_TO_ISO3, ISO2_TO_NAME, AGE_BINS, AGE_LABELS
)


class DataLoader:
    """
    Clase para cargar y preprocesar datos del ESS11.
    Implementa caché de Streamlit para optimizar el rendimiento.
    """
    
    def __init__(self, file_path: Path = DATA_FILE):
        """
        Inicializa el cargador de datos.
        
        Args:
            file_path: Ruta al archivo CSV de datos
        """
        self.file_path = file_path
        self.df_raw = None
        self.df_clean = None
        
    @st.cache_data(show_spinner=False)
    def load_raw_data(_self) -> pd.DataFrame:
        """
        Carga los datos crudos desde el CSV.
        Usa caché de Streamlit para evitar recargas innecesarias.
        
        Returns:
            DataFrame con los datos sin procesar
        """
        try:
            df = pd.read_csv(_self.file_path, low_memory=False)
            return df
        except FileNotFoundError:
            st.error(f"❌ No se encontró el archivo de datos en: {_self.file_path}")
            st.stop()
        except Exception as e:
            st.error(f"❌ Error al cargar los datos: {str(e)}")
            st.stop()
    
    @st.cache_data(show_spinner=False)
    def clean_data(_self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia los datos eliminando valores inválidos y creando variables derivadas.
        
        Args:
            df: DataFrame con datos crudos
            
        Returns:
            DataFrame limpio y procesado
        """
        df_clean = df.copy()
        
        # 1. Eliminar valores inválidos de variables explicativas
        for var, invalid_vals in INVALID_VALUES.items():
            if var in df_clean.columns:
                df_clean = df_clean[~df_clean[var].isin(invalid_vals)]
        
        # 2. Invertir escala de ipeqopta (para que más alto = más apoyo)
        if 'ipeqopta' in df_clean.columns:
            df_clean['ipeqopta'] = 7 - df_clean['ipeqopta']
        
        # 3. Invertir escala de polintr (para que más alto = más interés)
        # Original: 1=muy interesado, 4=nada interesado
        # Nueva: 1=nada interesado, 4=muy interesado
        if 'polintr' in df_clean.columns:
            max_val = df_clean['polintr'].max()
            df_clean['polintr'] = max_val + 1 - df_clean['polintr']
        
        # 4. Crear variable education_level (escala ordinal 0-26 desde ISCED)
        if 'edulvlb' in df_clean.columns:
            df_clean['education_level'] = df_clean['edulvlb'].map(EDUCATION_SCALE)
            # Rellenar valores no mapeados con interpolación
            df_clean['education_level'] = df_clean['education_level'].fillna(
                df_clean['education_level'].median()
            )
        
        # 5. Crear tramos de edad
        if 'agea' in df_clean.columns:
            df_clean['age_group'] = pd.cut(
                df_clean['agea'], 
                bins=AGE_BINS, 
                labels=AGE_LABELS,
                right=False
            )
        
        # 6. Crear variables derivadas de partido político (solo para España)
        if 'prtvtges' in df_clean.columns:
            df_clean['ideology'] = df_clean['prtvtges'].map(IDEOLOGY_SCALE)
            df_clean['nationalism'] = df_clean['prtvtges'].map(NATIONALISM_SCALE)
            df_clean['party_name'] = df_clean['prtvtges'].map(PARTY_NAMES)
        
        # 7. Añadir nombres de países en español
        if 'cntry' in df_clean.columns:
            df_clean['country_name'] = df_clean['cntry'].map(ISO2_TO_NAME)
            df_clean['country_iso3'] = df_clean['cntry'].map(ISO2_TO_ISO3)
        
        # 8. Crear etiquetas de género
        if 'gndr' in df_clean.columns:
            df_clean['gender_label'] = df_clean['gndr'].map({1: 'Hombre', 2: 'Mujer'})
        
        return df_clean
    
    def get_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Obtiene los datos limpios y procesados.
        
        Args:
            force_reload: Si True, fuerza la recarga desde disco
            
        Returns:
            DataFrame limpio
        """
        if force_reload or self.df_clean is None:
            self.df_raw = self.load_raw_data()
            self.df_clean = self.clean_data(self.df_raw)
        
        return self.df_clean
    
    def get_filtered_data(self, df: pd.DataFrame, filters: dict) -> pd.DataFrame:
        """
        Aplica filtros al DataFrame según los criterios especificados.
        
        Args:
            df: DataFrame a filtrar
            filters: Diccionario con filtros {columna: valores}
            
        Returns:
            DataFrame filtrado
        """
        df_filtered = df.copy()
        
        for column, values in filters.items():
            if column in df_filtered.columns and values:
                # Si values es una lista vacía o None, no filtrar
                if isinstance(values, list) and len(values) > 0:
                    df_filtered = df_filtered[df_filtered[column].isin(values)]
                elif not isinstance(values, list) and values is not None:
                    df_filtered = df_filtered[df_filtered[column] == values]
        
        return df_filtered
    
    def get_variable_stats(self, df: pd.DataFrame, variable: str) -> dict:
        """
        Calcula estadísticas descriptivas de una variable.
        
        Args:
            df: DataFrame con los datos
            variable: Nombre de la variable a analizar
            
        Returns:
            Diccionario con estadísticas descriptivas
        """
        if variable not in df.columns:
            return {}
        
        data = df[variable].dropna()
        
        return {
            'count': len(data),
            'mean': data.mean(),
            'median': data.median(),
            'std': data.std(),
            'min': data.min(),
            'max': data.max(),
            'q25': data.quantile(0.25),
            'q75': data.quantile(0.75)
        }
    
    def calculate_gender_gap(self, df: pd.DataFrame, variable: str) -> float:
        """
        Calcula la brecha de género para una variable.
        
        Args:
            df: DataFrame con los datos
            variable: Variable dependiente a analizar
            
        Returns:
            Brecha de género (Media mujeres - Media hombres)
        """
        if variable not in df.columns or 'gndr' not in df.columns:
            return np.nan
        
        female_mean = df[df['gndr'] == 2][variable].mean()
        male_mean = df[df['gndr'] == 1][variable].mean()
        
        return female_mean - male_mean
    
    def calculate_age_gradient(self, df: pd.DataFrame, variable: str) -> float:
        """
        Calcula el gradiente por edad (jóvenes vs mayores).
        
        Args:
            df: DataFrame con los datos
            variable: Variable dependiente a analizar
            
        Returns:
            Gradiente (Media 15-34 - Media 65+)
        """
        if variable not in df.columns or 'age_group' not in df.columns:
            return np.nan
        
        young_mean = df[df['age_group'].isin(['15-24', '25-34'])][variable].mean()
        old_mean = df[df['age_group'] == '65+'][variable].mean()
        
        return young_mean - old_mean
    
    def calculate_education_gradient(self, df: pd.DataFrame, variable: str) -> float:
        """
        Calcula el gradiente educativo (Q4 vs Q1).
        
        Args:
            df: DataFrame con los datos
            variable: Variable dependiente a analizar
            
        Returns:
            Gradiente educativo (Media Q4 - Media Q1)
        """
        if variable not in df.columns or 'education_level' not in df.columns:
            return np.nan
        
        q1_threshold = df['education_level'].quantile(0.25)
        q4_threshold = df['education_level'].quantile(0.75)
        
        q1_mean = df[df['education_level'] <= q1_threshold][variable].mean()
        q4_mean = df[df['education_level'] >= q4_threshold][variable].mean()
        
        return q4_mean - q1_mean
    
    def get_country_ranking(self, df: pd.DataFrame, variable: str, 
                           top_n: int = 5) -> tuple:
        """
        Obtiene el ranking de países para una variable.
        
        Args:
            df: DataFrame con los datos
            variable: Variable dependiente a analizar
            top_n: Número de países a mostrar en top/bottom
            
        Returns:
            Tupla (top_countries, bottom_countries) como DataFrames
        """
        if variable not in df.columns or 'country_name' not in df.columns:
            return pd.DataFrame(), pd.DataFrame()
        
        country_means = df.groupby('country_name')[variable].agg(['mean', 'count']).reset_index()
        country_means = country_means[country_means['count'] >= 30]  # Filtro de muestra mínima
        country_means = country_means.sort_values('mean', ascending=False)
        
        top_countries = country_means.head(top_n)
        bottom_countries = country_means.tail(top_n).sort_values('mean', ascending=True)
        
        return top_countries, bottom_countries


def get_data_loader() -> DataLoader:
    """
    Factory function para obtener una instancia del cargador de datos.
    
    Returns:
        Instancia de DataLoader
    """
    return DataLoader()
