# Panel BI - Igualdad en Europa (ESS11)

Panel de inteligencia interactivo desarrollado con Streamlit para analizar actitudes hacia la igualdad de oportunidades y salarial en Europa basado en datos del European Social Survey Round 11.

## 📋 Descripción

Esta aplicación proporciona un análisis completo e interactivo de las actitudes europeas hacia:
- Igualdad de oportunidades
- Igualdad salarial
- Interés político
- Percepción sobre inmigración
- Relaciones de género

## 🏗️ Estructura del Proyecto

```
app/
├── app.py                  # Aplicación principal de Streamlit
├── config.py              # Configuración global (constantes, paletas, rutas)
├── data_loader.py         # Carga y preprocesamiento de datos
├── visualizations.py      # Componentes de visualización con Plotly
├── components.py          # Componentes reutilizables de UI
├── analytics.py           # Funciones de análisis estadístico
└── README.md              # Este archivo
```

## 🚀 Instalación y Ejecución

### Requisitos Previos

- Python 3.8 o superior
- pip instalado

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicación

```bash
# Desde la carpeta raíz del proyecto
streamlit run app/app.py

# O desde la carpeta app
cd app
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📊 Características Principales

### 1. **Filtros Interactivos**
- Filtrado por país, género, edad, educación y partido político
- Actualización en tiempo real de visualizaciones
- Indicadores de calidad de datos

### 2. **Análisis Exploratorio Completo**
- Distribuciones univariantes
- Análisis bivariante por género, edad, educación y país
- Tests estadísticos (Shapiro-Wilk, Mann-Whitney, Spearman)
- Matrices de correlación

### 3. **Visualizaciones Interactivas**
- Histogramas de distribución
- Gráficos de caja (boxplots) y violín
- Mapas coropléticos de Europa
- Gráficos de tendencias por edad y educación
- Dispersogramas con líneas de tendencia
- Rankings de países

### 4. **KPIs Dinámicos**
- Brecha de género
- Gradiente generacional
- Gradiente educativo
- Gradiente ideológico (España)

### 5. **Análisis Específico de España**
- Comparación por partido político
- Análisis por ideología (izquierda-derecha)
- Análisis por nacionalismo

## 🎨 Componentes Técnicos

### `config.py`
Gestiona toda la configuración del proyecto:
- Rutas de archivos y directorios
- Definición de variables del ESS11
- Valores inválidos por variable
- Escalas y mapeos (educación, ideología, nacionalismo, partidos)
- Paletas de colores
- Configuración de Plotly
- Textos y descripciones

### `data_loader.py`
Clase `DataLoader` con responsabilidades:
- Carga de datos desde CSV con caché
- Limpieza de valores inválidos
- Creación de variables derivadas (education_level, ideology, nationalism)
- Aplicación de filtros
- Cálculo de estadísticas descriptivas
- Cálculo de KPIs (brechas, gradientes)

### `visualizations.py`
Funciones para crear gráficos Plotly:
- `create_distribution_histogram()`: Histogramas de distribución
- `create_gender_comparison()`: Comparación por género (boxplot)
- `create_age_trend()`: Tendencia por tramos de edad
- `create_education_trend()`: Tendencia por nivel educativo
- `create_country_map()`: Mapa coroplético europeo
- `create_party_bar_chart()`: Gráfico de barras por partido
- `create_ideology_scatter()`: Dispersograma ideología vs variable
- `create_correlation_heatmap()`: Matriz de correlación
- `create_top_bottom_chart()`: Top y Bottom países
- `create_violin_plot()`: Gráfico de violín

### `components.py`
Componentes reutilizables de UI:
- `render_sidebar()`: Menú lateral con filtros
- `render_kpi_cards()`: Tarjetas de KPIs
- `render_variable_selector()`: Selector de variables
- `render_section_header()`: Encabezados de sección
- `render_info_box()`: Cajas de información
- `render_stats_table()`: Tablas de estadísticas
- `render_data_quality_warning()`: Advertencias de datos
- `create_download_button()`: Botón de descarga
- `render_methodology_expander()`: Información metodológica
- `render_footer()`: Pie de página

### `analytics.py`
Funciones de análisis estadístico:
- `calculate_spearman_correlation()`: Correlación de Spearman
- `test_normality()`: Test de Shapiro-Wilk
- `calculate_group_statistics()`: Estadísticas por grupo
- `perform_gender_comparison()`: Análisis completo por género (Mann-Whitney)
- `perform_age_correlation()`: Correlación con edad
- `perform_education_correlation()`: Correlación con educación
- `calculate_ideology_gradient()`: Gradiente ideológico
- `generate_summary_statistics()`: Resumen estadístico completo

### `app.py`
Aplicación principal que integra todos los componentes:
- Configuración de página y CSS personalizado
- Carga de datos con caché
- Renderizado de sidebar y filtros
- Secciones:
  - Origen de los datos
  - Explicación de variables
  - Análisis exploratorio (EDA) con tabs
  - Análisis específico de España
  - Matriz de correlaciones
  - Conclusiones
  - Machine Learning (placeholder)

## 📚 Fuente de Datos

**European Social Survey Round 11 (ESS11)**
- Período: 2023
- Países: 30+ países europeos
- Observaciones: ~40,000 respuestas
- Variables clave: actitudes hacia igualdad, política, inmigración

## 🔧 Tecnologías Utilizadas

- **Streamlit**: Framework para aplicaciones web interactivas
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Computación numérica
- **Plotly Express**: Visualizaciones interactivas
- **SciPy**: Análisis estadístico (correlaciones, tests)

## 📖 Metodología

### Limpieza de Datos
1. Eliminación de valores inválidos según codebook ESS11
2. Inversión de escala de `ipeqopta` para interpretación intuitiva (1=nada importante → 6=muy importante)
3. Inversión de escala de `polintr` para interpretación intuitiva (1=nada interesado → 4=muy interesado)
4. Creación de variables derivadas:
   - `education_level`: Escala ordinal 0-26 desde ISCED
   - `ideology`: Escala 1-5 (izquierda-derecha) desde partido votado (códigos ESS11 reales)
   - `nationalism`: Escala 1-5 (bajo-alto) desde partido votado (códigos ESS11 reales)
   - `age_group`: Tramos de edad de 10 años

**Partidos políticos de España (códigos ESS11 reales):**
- 1: PP, 2: PSOE, 3: VOX, 4: SUMAR, 5: ERC, 6: JuntsxCat
- 7: EH-Bildu, 8: EAJ-PNV, 9: BNG, 10: Coalición Canaria
- 11: UPN, 12: PACMA, 50: Otro, 51: Voto en Blanco, 52: Voto Inválido

### Análisis Estadístico
- **No paramétrico**: Uso de correlaciones de Spearman debido a no-normalidad
- **Tests de hipótesis**: Mann-Whitney U para comparaciones de género
- **Visualizaciones robustas**: Medianas, cuartiles, boxplots

### KPIs Principales
- **Brecha de género**: Media(mujeres) - Media(hombres)
- **Gradiente etario**: Media(15-34) - Media(65+)
- **Gradiente educativo**: Media(Q4) - Media(Q1)
- **Gradiente ideológico**: Media(izquierda) - Media(derecha)

## 🎯 Casos de Uso

1. **Investigación académica**: Análisis de actitudes europeas hacia igualdad
2. **Políticas públicas**: Identificación de brechas y grupos objetivo
3. **Comunicación**: Visualización de datos complejos de forma accesible
4. **Educación**: Herramienta didáctica para enseñanza de análisis de datos

## 🔮 Roadmap

### Fase 1: Funcionalidades Básicas ✅
- [x] Carga y limpieza de datos
- [x] Visualizaciones interactivas
- [x] Filtros dinámicos
- [x] KPIs principales
- [x] Análisis bivariante completo

### Fase 2: Análisis Avanzado (En desarrollo)
- [ ] Modelos de Machine Learning
- [ ] Análisis de clustering
- [ ] Predicción de actitudes
- [ ] Feature importance

### Fase 3: Mejoras UX/UI
- [ ] Temas personalizables
- [ ] Exportación de informes PDF
- [ ] Comparación entre rondas ESS
- [ ] Modo multiidioma

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está desarrollado con fines educativos y de investigación.

## 📧 Contacto

Para preguntas o sugerencias, consulta la documentación del proyecto en `docs/EDA.md`.

---

**Desarrollado con ❤️ usando Streamlit, Pandas y Plotly**
