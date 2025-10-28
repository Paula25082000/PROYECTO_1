"""
Configuración central de la aplicación Streamlit.
Define constantes, paletas de colores, y configuraciones globales.
"""

# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================
import os
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Archivo de datos principal
DATA_FILE = DATA_DIR / "ESS11.csv"

# ============================================================================
# VARIABLES DEL DATASET ESS11
# ============================================================================

# Variables explicativas (X)
EXPLICATIVE_VARS = {
    'gndr': 'Género',
    'agea': 'Edad',
    'edulvlb': 'Nivel Educativo (ISCED)',
    'cntry': 'País',
    'prtvtges': 'Partido Votado (España)'
}

# Variables dependientes (Y)
DEPENDENT_VARS = {
    'ipeqopta': 'Igualdad de Oportunidades',
    'eqpaybg': 'Igualdad Salarial',
    'polintr': 'Interés en Política',
    'imwbcnt': 'Percepción sobre Inmigración',
    'wsekpwr': 'Percepción Control Mujeres'
}

# Valores a eliminar por variable (códigos de no respuesta)
INVALID_VALUES = {
    'gndr': [9],
    'agea': [999],
    'edulvlb': [5555, 7777, 8888, 9999],
    'prtvtges': [66, 77, 88, 99],
    'ipeqopta': [66, 77, 88, 99],
    'eqpaybg': [7, 8, 9],
    'polintr': [7, 8, 9],
    'imwbcnt': [77, 88, 99],
    'wsekpwr': [7, 8, 9]
}

# ============================================================================
# ESCALAS Y MAPEOS
# ============================================================================

# Mapeo de nivel educativo ISCED a escala ordinal 0-26
EDUCATION_SCALE = {
    0: 0,     # No completada
    113: 5,   # Primaria 1
    129: 6,   # Primaria 2
    212: 8,   # Secundaria inferior 1
    213: 9,   # Secundaria inferior 2
    221: 10,  # Secundaria superior 1
    222: 11,  # Secundaria superior 2
    223: 12,  # Secundaria superior 3
    229: 13,  # Secundaria superior general
    311: 15,  # Post-secundaria no terciaria 1
    312: 16,  # Post-secundaria no terciaria 2
    313: 17,  # Post-secundaria no terciaria 3
    321: 18,  # Terciaria ciclo corto 1
    322: 19,  # Terciaria ciclo corto 2
    421: 20,  # Grado/Licenciatura 1
    422: 21,  # Grado/Licenciatura 2
    423: 22,  # Grado/Licenciatura 3
    510: 23,  # Máster 1
    520: 24,  # Máster 2
    610: 25,  # Doctorado 1
    620: 26,  # Doctorado 2
    710: 24,  # Máster equivalente
    720: 26,  # Doctorado equivalente
    800: 26   # Doctorado
}

# Mapeo de partidos políticos españoles a ideología (1=izquierda, 5=derecha)
# Basado en códigos reales del ESS11 para España (prtvtges)
IDEOLOGY_SCALE = {
    1: 4,   # PP - Derecha
    2: 2,   # PSOE - Centroizquierda
    3: 5,   # VOX - Derecha radical
    4: 1,   # SUMAR - Izquierda
    5: 1,   # ERC - Izquierda nacionalista
    6: 4,   # JuntsxCat - Derecha nacionalista
    7: 1,   # EH-Bildu - Izquierda nacionalista
    8: 3,   # EAJ-PNV - Centroderecha nacionalista
    9: 1,   # BNG - Izquierda nacionalista
    10: 3,  # Coalición Canaria - Centroderecha regionalista
    11: 4,  # UPN - Derecha regionalista
    12: 2,  # PACMA - Centroizquierda ecologista
    50: 3,  # Other - Centro (por defecto)
    51: 3,  # Voto en Blanco - Neutral
    52: 3   # Voto Inválido - Neutral
}

# Mapeo de partidos a nacionalismo (1=bajo, 5=alto)
# Basado en códigos reales del ESS11 para España (prtvtges)
NATIONALISM_SCALE = {
    1: 1,   # PP - No nacionalista
    2: 1,   # PSOE - No nacionalista
    3: 1,   # VOX - No nacionalista
    4: 1,   # SUMAR - No nacionalista
    5: 4,   # ERC - Independentista
    6: 4,   # JuntsxCat - Independentista
    7: 4,   # EH-Bildu - Independentista
    8: 3,   # EAJ-PNV - Nacionalista
    9: 3,   # BNG - Nacionalista
    10: 2,  # Coalición Canaria - Regionalista moderado
    11: 2,  # UPN - Regionalista moderado
    12: 1,  # PACMA - No nacionalista
    50: 2,  # Other - Bajo (por defecto)
    51: 2,  # Voto en Blanco - Neutral
    52: 2   # Voto Inválido - Neutral
}

# Nombres de partidos políticos
# Basado en códigos reales del ESS11 para España (prtvtges)
PARTY_NAMES = {
    1: "PP",
    2: "PSOE",
    3: "VOX",
    4: "SUMAR",
    5: "ERC",
    6: "JuntsxCat",
    7: "EH-Bildu",
    8: "EAJ-PNV",
    9: "BNG",
    10: "Coalición Canaria",
    11: "UPN",
    12: "PACMA",
    50: "Otro",
    51: "Voto en Blanco",
    52: "Voto Inválido"
}

# Mapeo de códigos ISO2 a ISO3 para mapas
ISO2_TO_ISO3 = {
    'AT': 'AUT', 'BE': 'BEL', 'BG': 'BGR', 'CH': 'CHE', 'CY': 'CYP',
    'CZ': 'CZE', 'DE': 'DEU', 'DK': 'DNK', 'EE': 'EST', 'ES': 'ESP',
    'FI': 'FIN', 'FR': 'FRA', 'GB': 'GBR', 'GR': 'GRC', 'HR': 'HRV',
    'HU': 'HUN', 'IE': 'IRL', 'IS': 'ISL', 'IT': 'ITA', 'LT': 'LTU',
    'LV': 'LVA', 'ME': 'MNE', 'MK': 'MKD', 'NL': 'NLD', 'NO': 'NOR',
    'PL': 'POL', 'PT': 'PRT', 'RO': 'ROU', 'RS': 'SRB', 'SE': 'SWE',
    'SI': 'SVN', 'SK': 'SVK'
}

# Mapeo de códigos ISO2 a nombres de países
ISO2_TO_NAME = {
    'AT': 'Austria', 'BE': 'Bélgica', 'BG': 'Bulgaria', 'CH': 'Suiza',
    'CY': 'Chipre', 'CZ': 'República Checa', 'DE': 'Alemania', 'DK': 'Dinamarca',
    'EE': 'Estonia', 'ES': 'España', 'FI': 'Finlandia', 'FR': 'Francia',
    'GB': 'Reino Unido', 'GR': 'Grecia', 'HR': 'Croacia', 'HU': 'Hungría',
    'IE': 'Irlanda', 'IS': 'Islandia', 'IT': 'Italia', 'LT': 'Lituania',
    'LV': 'Letonia', 'ME': 'Montenegro', 'MK': 'Macedonia del Norte',
    'NL': 'Países Bajos', 'NO': 'Noruega', 'PL': 'Polonia', 'PT': 'Portugal',
    'RO': 'Rumanía', 'RS': 'Serbia', 'SE': 'Suecia', 'SI': 'Eslovenia',
    'SK': 'Eslovaquia'
}

# ============================================================================
# CONFIGURACIÓN DE VISUALIZACIÓN
# ============================================================================

# Paleta de colores principal
COLOR_PALETTE = {
    'primary': '#1f77b4',      # Azul principal
    'secondary': '#ff7f0e',    # Naranja
    'success': '#2ca02c',      # Verde
    'warning': '#d62728',      # Rojo
    'info': '#9467bd',         # Púrpura
    'gender_male': '#3498db',  # Azul para hombres
    'gender_female': '#e74c3c', # Rosa/rojo para mujeres
    'gradient_start': '#2ecc71', # Verde para gradientes positivos
    'gradient_end': '#e74c3c'   # Rojo para gradientes negativos
}

# Configuración de gráficos Plotly
PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'grafico_ess11',
        'height': 600,
        'width': 1000,
        'scale': 2
    }
}

# Plantilla de gráficos
PLOTLY_TEMPLATE = 'plotly_white'

# ============================================================================
# CONFIGURACIÓN DE PÁGINA STREAMLIT
# ============================================================================

PAGE_CONFIG = {
    "page_title": "Panel ESS11: Igualdad y Sociedad en Europa",
    "page_icon": "⚖️",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'About': "Panel de Inteligencia sobre Actitudes hacia la Igualdad en Europa - ESS11"
    }
}

# ============================================================================
# TEXTOS Y DESCRIPCIONES
# ============================================================================

APP_TITLE = "⚖️ Panel ESS11: Igualdad y Sociedad en Europa"
APP_SUBTITLE = "Análisis de Actitudes hacia la Igualdad de Oportunidades y Salarial, el Interés Político, la Inmigración y las Relaciones de Género - European Social Survey Round 11"

# Descripciones de variables dependientes
VAR_DESCRIPTIONS = {
    'ipeqopta': """
    **Igualdad de Oportunidades**: Mide el apoyo a que todas las personas sean tratadas por igual 
    y tengan igualdad de oportunidades en la vida.
    
    *Escala*: 1-6 (invertida para interpretación intuitiva)
    - **1** = Nada importante
    - **6** = Muy importante
    
    ⚠️ *Nota*: La escala original del ESS11 (1=muy importante, 6=nada importante) ha sido invertida 
    para que valores más altos indiquen mayor apoyo a la igualdad de oportunidades.
    """,
    'eqpaybg': """
    **Igualdad Salarial**: Mide la percepción sobre si la igualdad salarial entre mujeres y hombres 
    es buena o mala para la economía del país.
    
    *Escala*: 0-6
    - **0** = Muy malo para la economía
    - **6** = Muy bueno para la economía
    
    Valores más altos indican mayor acuerdo con que la igualdad salarial es positiva para la economía.
    """,
    'polintr': """
    **Interés en Política**: Mide el nivel de interés declarado en asuntos políticos.
    
    *Escala*: 1-4 (invertida para interpretación intuitiva)
    - **1** = Nada interesado
    - **2** = Poco interesado
    - **3** = Bastante interesado
    - **4** = Muy interesado
    
    ⚠️ *Nota*: La escala original del ESS11 (1=muy interesado, 4=nada interesado) ha sido invertida 
    para que valores más altos indiquen mayor interés político.
    """,
    'imwbcnt': """
    **Percepción sobre Inmigración**: Mide la percepción sobre si la inmigración hace del país 
    un lugar mejor o peor para vivir.
    
    *Escala*: 0-10
    - **0** = Peor lugar para vivir
    - **10** = Mejor lugar para vivir
    
    Valores más altos indican percepciones más favorables hacia la inmigración.
    """,
    'wsekpwr': """
    **Percepción sobre Control de Género**: Mide la frecuencia percibida con la que las mujeres 
    buscan ganar poder obteniendo control sobre los hombres.
    
    *Escala*: 1-5
    - **1** = Nunca
    - **2** = Raramente
    - **3** = A veces
    - **4** = A menudo
    - **5** = Siempre
    
    Valores más altos indican mayor acuerdo con esta percepción. Esta variable es relevante 
    para analizar actitudes subyacentes sobre relaciones de poder de género.
    """
}

# ============================================================================
# CONFIGURACIÓN DE TRAMOS DE EDAD
# ============================================================================

AGE_BINS = [15, 25, 35, 45, 55, 65, 100]
AGE_LABELS = ['15-24', '25-34', '35-44', '45-54', '55-64', '65+']

# ============================================================================
# CONSTANTES DE ANÁLISIS
# ============================================================================

# Nivel de significancia para pruebas estadísticas
SIGNIFICANCE_LEVEL = 0.05

# Número mínimo de observaciones para análisis
MIN_OBSERVATIONS = 30
