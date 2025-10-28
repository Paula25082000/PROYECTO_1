# Documentación Técnica - Panel BI Igualdad en Europa

## 📋 Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Flujo de Datos](#flujo-de-datos)
3. [Componentes Principales](#componentes-principales)
4. [Convenciones de Código](#convenciones-de-código)
5. [Optimización y Performance](#optimización-y-performance)
6. [Testing y Validación](#testing-y-validación)
7. [Despliegue](#despliegue)

---

## 🏗️ Arquitectura del Sistema

### Patrón de Diseño

La aplicación sigue un patrón **MVC adaptado para Streamlit**:

- **Model (Modelo)**: `data_loader.py`, `analytics.py`
- **View (Vista)**: `visualizations.py`, `components.py`
- **Controller (Controlador)**: `app.py`
- **Config (Configuración)**: `config.py`

```
┌─────────────────────────────────────────────┐
│              Streamlit App (app.py)         │
│                 [Controller]                │
└──────────┬──────────────────────┬───────────┘
           │                      │
┌──────────▼──────────┐  ┌────────▼──────────┐
│   Components        │  │  Visualizations   │
│   [View Layer]      │  │  [View Layer]     │
└──────────┬──────────┘  └───────────────────┘
           │
┌──────────▼──────────┐  ┌───────────────────┐
│   DataLoader        │  │   Analytics       │
│   [Model Layer]     │  │   [Model Layer]   │
└──────────┬──────────┘  └───────────────────┘
           │
┌──────────▼──────────┐
│      Config         │
│   [Configuration]   │
└─────────────────────┘
```

### Separación de Responsabilidades

| Módulo | Responsabilidad | Dependencias |
|--------|----------------|--------------|
| `config.py` | Constantes, configuración global | Ninguna |
| `data_loader.py` | Carga, limpieza, transformación | config, pandas, streamlit |
| `analytics.py` | Análisis estadístico, métricas | pandas, numpy, scipy |
| `visualizations.py` | Gráficos interactivos | plotly, pandas, config |
| `components.py` | Componentes UI reutilizables | streamlit, pandas, config |
| `app.py` | Orquestación, flujo de usuario | Todos los anteriores |

---

## 🔄 Flujo de Datos

### 1. Carga Inicial

```python
# app.py
@st.cache_resource
def initialize_app():
    loader = get_data_loader()
    return loader

data_loader = initialize_app()
df = data_loader.get_data()  # Carga con caché
```

**Optimización**: `@st.cache_resource` evita recargar datos en cada interacción.

### 2. Aplicación de Filtros

```python
# Usuario interactúa con sidebar
filters = render_sidebar(df)

# Filtrado en cascada
df_filtered = data_loader.get_filtered_data(df, filters)
df_filtered = apply_education_filter(df_filtered, filters['education_filter'])
```

**Flujo**:
1. Usuario selecciona filtros en sidebar
2. `render_sidebar()` retorna diccionario de filtros
3. `get_filtered_data()` aplica filtros básicos
4. `apply_education_filter()` aplica filtro educativo por cuartiles

### 3. Análisis y Visualización

```python
# Análisis
gender_analysis = perform_gender_comparison(df_filtered, variable)

# Visualización
fig = create_gender_comparison(df_filtered, variable)
st.plotly_chart(fig, use_container_width=True)
```

**Pipeline**:
1. Función de análisis procesa datos → retorna dict/DataFrame
2. Función de visualización crea figura Plotly
3. Streamlit renderiza gráfico interactivo

---

## 🧩 Componentes Principales

### DataLoader (`data_loader.py`)

**Métodos clave**:

```python
class DataLoader:
    def load_raw_data(self) -> pd.DataFrame
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame
    def get_filtered_data(self, df: pd.DataFrame, filters: dict) -> pd.DataFrame
    def get_variable_stats(self, df: pd.DataFrame, variable: str) -> dict
    def calculate_gender_gap(self, df: pd.DataFrame, variable: str) -> float
    def calculate_age_gradient(self, df: pd.DataFrame, variable: str) -> float
    def get_country_ranking(self, df: pd.DataFrame, variable: str) -> tuple
```

**Transformaciones aplicadas en `clean_data()`**:

1. Eliminación de valores inválidos (según `INVALID_VALUES` en config)
2. Inversión de escala `ipeqopta`: `7 - valor_original`
3. Mapeo educativo: `edulvlb` → `education_level` (0-26)
4. Creación de tramos de edad: `agea` → `age_group`
5. Derivadas políticas: `prtvtges` → `ideology`, `nationalism`, `party_name`
6. Mapeos geográficos: `cntry` → `country_name`, `country_iso3`
7. Etiquetas de género: `gndr` → `gender_label`

### Visualizations (`visualizations.py`)

**Funciones de gráficos**:

| Función | Tipo de Gráfico | Uso Principal |
|---------|----------------|---------------|
| `create_distribution_histogram` | Histograma | Distribución univariante |
| `create_gender_comparison` | Boxplot | Comparación por género |
| `create_age_trend` | Línea | Tendencia por edad |
| `create_education_trend` | Línea | Tendencia por educación |
| `create_country_map` | Coroplético | Comparación geográfica |
| `create_party_bar_chart` | Barras horizontales | Ranking por partido |
| `create_ideology_scatter` | Dispersión + tendencia | Correlación ideología |
| `create_correlation_heatmap` | Heatmap | Matriz de correlaciones |
| `create_violin_plot` | Violín | Distribuciones comparativas |

**Configuración estándar**:
- Template: `plotly_white` (definido en config)
- Paleta: `COLOR_PALETTE` (definido en config)
- Config: `PLOTLY_CONFIG` (botones, exportación)

### Analytics (`analytics.py`)

**Funciones estadísticas**:

```python
# Correlaciones
calculate_spearman_correlation(df, var1, var2) -> (correlation, p_value)

# Tests
test_normality(df, variable) -> dict  # Shapiro-Wilk
perform_gender_comparison(df, variable) -> dict  # Mann-Whitney U

# Correlaciones bivariantes
perform_age_correlation(df, variable) -> dict
perform_education_correlation(df, variable) -> dict

# Gradientes
calculate_ideology_gradient(df, variable) -> float

# Resúmenes
generate_summary_statistics(df, variable) -> pd.DataFrame
```

**Criterios estadísticos**:
- Nivel de significancia: α = 0.05
- Mínimo de observaciones: 10 (análisis), 30 (ranking países)
- Método de correlación: **Spearman** (no paramétrico)
- Test de comparación: **Mann-Whitney U** (no paramétrico)

---

## 📜 Convenciones de Código

### Estilo

- **PEP 8**: Estilo estándar de Python
- **Docstrings**: Todas las funciones públicas documentadas
- **Type hints**: En firmas de funciones principales
- **Nombres descriptivos**: Variables y funciones auto-explicativas

### Nomenclatura

```python
# Variables
df_clean          # DataFrame limpio
df_filtered       # DataFrame filtrado
selected_var      # Variable seleccionada por usuario

# Funciones
render_*()        # Componentes UI que renderizan en Streamlit
create_*()        # Funciones que crean objetos (figuras, DataFrames)
calculate_*()     # Funciones de cálculo que retornan valores
perform_*()       # Funciones de análisis que retornan dicts
get_*()          # Getters que retornan datos

# Constantes (config.py)
ALL_CAPS          # DEPENDENT_VARS, COLOR_PALETTE
```

### Organización de Imports

```python
# 1. Standard library
import sys
from pathlib import Path

# 2. Third-party
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# 3. Local modules
from config import CONSTANTS
from data_loader import DataLoader
```

---

## ⚡ Optimización y Performance

### Caché de Streamlit

```python
# Caché de recursos (singletons)
@st.cache_resource
def initialize_app():
    return get_data_loader()

# Caché de datos (por parámetros)
@st.cache_data
def load_raw_data(_self):
    return pd.read_csv(_self.file_path)
```

**Estrategia**:
- `@st.cache_resource`: Para objetos singleton (DataLoader)
- `@st.cache_data`: Para datos que dependen de parámetros
- `show_spinner=False`: Para operaciones rápidas

### Optimización de DataFrame

```python
# Lectura eficiente
df = pd.read_csv(file_path, low_memory=False)

# Filtrado en cascada (evita copias innecesarias)
df_filtered = df.copy()  # Solo una copia
for col, values in filters.items():
    df_filtered = df_filtered[df_filtered[col].isin(values)]

# Selección de columnas relevantes
df_plot = df[['var1', 'var2', 'var3']].dropna()
```

### Limitación de Datos

```python
# Shapiro-Wilk: máximo 5000 muestras
if len(data) > 5000:
    data = data.sample(5000, random_state=42)

# Ranking países: mínimo 30 observaciones
country_means = country_means[country_means['count'] >= 30]
```

---

## 🧪 Testing y Validación

### Validaciones Implementadas

1. **Existencia de archivo de datos**
```python
if not DATA_FILE.exists():
    st.error(f"No se encontró {DATA_FILE}")
    st.stop()
```

2. **Validación de datos filtrados**
```python
render_data_quality_warning(df_filtered, min_obs=30)
```

3. **Validación de variables**
```python
if variable not in df.columns:
    return {}
```

4. **Validación de muestra**
```python
if len(data) < 10:
    return {'error': 'Datos insuficientes'}
```

### Testing Manual

**Checklist** para validación:

- [ ] Carga de datos sin errores
- [ ] Todos los filtros funcionan correctamente
- [ ] Gráficos se renderizan para cada variable
- [ ] KPIs muestran valores coherentes
- [ ] No hay errores en consola
- [ ] Exportación CSV funciona
- [ ] Responsive en diferentes tamaños de pantalla

---

## 🚀 Despliegue

### Opción 1: Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app/app.py

# O usar script de inicio
python app/run.py
```

### Opción 2: Streamlit Cloud

1. Subir proyecto a GitHub
2. Conectar repositorio en [share.streamlit.io](https://share.streamlit.io)
3. Configurar:
   - Main file: `app/app.py`
   - Python version: 3.9+
   - Requirements: `app/requirements.txt`

### Opción 3: Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build
docker build -t equality-panel .

# Run
docker run -p 8501:8501 equality-panel
```

### Variables de Entorno

**Opcional** - Para configuración avanzada:

```bash
# .env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_THEME_BASE=light
```

---

## 📊 Estructura de Datos

### DataFrame Principal (después de limpieza)

```python
df_clean.columns:
[
    # Variables originales ESS11
    'gndr', 'agea', 'edulvlb', 'cntry', 'prtvtges',
    'ipeqopta', 'eqpaybg', 'polintr', 'imwbcnt', 'wsekpwr',
    
    # Variables derivadas
    'education_level',   # int 0-26
    'age_group',        # categorical
    'ideology',         # float 1-5
    'nationalism',      # float 1-5
    'party_name',       # str
    'country_name',     # str
    'country_iso3',     # str (ISO 3166-1 alpha-3)
    'gender_label'      # str ('Hombre'/'Mujer')
]
```

### Tipos de Datos

```python
dtypes = {
    'gndr': int64,
    'agea': int64,
    'education_level': float64,
    'age_group': category,
    'ipeqopta': int64,
    'ideology': float64,
    'country_name': object,
    # ...
}
```

---

## 🔧 Mantenimiento

### Actualizar Datos ESS

1. Descargar nuevo CSV de ESS
2. Colocar en `data/ESS11.csv`
3. Verificar codebook para cambios en códigos
4. Actualizar `INVALID_VALUES` en `config.py` si es necesario

### Añadir Nueva Variable

1. **Config**: Añadir a `DEPENDENT_VARS` o `EXPLICATIVE_VARS`
2. **Limpieza**: Añadir valores inválidos a `INVALID_VALUES`
3. **Descripción**: Añadir a `VAR_DESCRIPTIONS`
4. **Visualización**: La app debería funcionar automáticamente

### Añadir Nuevo Gráfico

1. Crear función en `visualizations.py`
2. Seguir patrón existente (parámetros: df, variable, title)
3. Usar `PLOTLY_TEMPLATE` y `COLOR_PALETTE`
4. Retornar `go.Figure`
5. Añadir al flujo en `app.py`

---

## 📚 Referencias

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Express API](https://plotly.com/python/plotly-express/)
- [ESS11 Codebook](../data/ESS11%20codebook.html)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)

---

**Última actualización**: Octubre 2025
