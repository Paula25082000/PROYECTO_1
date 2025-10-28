# 🌍 Panel ESS11: Igualdad y Sociedad en Europa

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Un análisis interactivo de Igualdad y Sociedad en Europa basado en datos del European Social Survey Round 11**

[🚀 Demo](#-inicio-rápido) • [📊 Características](#-características-principales) • [📖 Documentación](#-documentación) • [🛠️ Tecnologías](#️-tecnologías)

</div>

---

## 📋 Tabla de Contenidos

- [Acerca del Proyecto](#-acerca-del-proyecto)
- [Origen de los Datos](#-origen-de-los-datos)
- [Características Principales](#-características-principales)
- [Inicio Rápido](#-inicio-rápido)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Variables Analizadas](#-variables-analizadas)
- [Metodología](#-metodología)
- [Análisis Exploratorio (EDA)](#-análisis-exploratorio-eda)
- [Panel de Inteligencia](#-panel-de-inteligencia)
- [Tecnologías](#️-tecnologías)
- [Documentación](#-documentación)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 🎯 Acerca del Proyecto

**Igualdad y Sociedad en Europa** es un proyecto de análisis de datos que combina exploración estadística avanzada con visualización interactiva para examinar la actitud hacia la Igualdad de Oportunidades y Salarial, el Interés Político, la Inmigración y las Relaciones de Género.

### 🎓 Contexto

Este proyecto nace como parte de un bootcamp de análisis de datos, con el objetivo de:

1. **Analizar** patrones y tendencias en diferentes actitudes en 30+ países europeos
2. **Identificar** brechas significativas por género, edad, educación e ideología
3. **Visualizar** datos complejos de manera accesible e interactiva
4. **Proporcionar** insights accionables para investigadores y policy makers

### 🔍 Pregunta Central

> ¿Cómo varían las actitudes hacia de igualdad y sociedad en Europa y qué factores sociodemográficos y políticos las influencian?

---

## 📊 Origen de los Datos

### European Social Survey (ESS11)

El **European Social Survey** es un proyecto de investigación académica que mide actitudes, creencias y comportamientos de población en más de 30 países europeos desde 2002.

**Datos utilizados:**
- **Ronda:** ESS Round 11 (2023)
- **Tamaño de muestra:** ~40,000+ encuestados
- **Países:** 30+ países europeos
- **Formato:** CSV con 600+ variables
- **Fuente:** [europeansocialsurvey.org](https://www.europeansocialsurvey.org/)

**Calidad de los datos:**
- Muestreo probabilístico representativo
- Metodología estandarizada entre países
- Controles de calidad rigurosos
- Documentación completa (codebook incluido)

---

## ✨ Características Principales

### 🎨 Panel Interactivo

- **Filtros dinámicos** por país, género, edad, educación y partido político (España)
- **Visualizaciones interactivas** con Plotly (mapas, gráficos, scatter plots)
- **KPIs automáticos** que calculan brechas y gradientes en tiempo real
- **Exportación de datos** filtrados para análisis adicional
- **Diseño responsive** optimizado para diferentes dispositivos

### 📈 Análisis Estadístico Robusto

- **Tests de normalidad** (Shapiro-Wilk)
- **Correlaciones no paramétricas** (Spearman)
- **Comparaciones de grupos** (Mann-Whitney U)
- **Análisis multivariante** con matrices de correlación
- **Interpretaciones automáticas** de significancia estadística

### 🌐 Análisis Multinivel

- **Nivel Individual:** Diferencias por género, edad, educación
- **Nivel País:** Comparaciones entre 30+ países europeos
- **Nivel Ideológico:** Análisis específico para España (partidos políticos)
- **Nivel Temporal:** Análisis de gradientes generacionales

### 🇪🇸 Foco en España

- Análisis por partido político votado
- Escalas de ideología (izquierda-derecha)
- Escalas de nacionalismo
- Comparativas con media europea

---

## 🚀 Inicio Rápido

### Requisitos Previos

```bash
# Python 3.8 o superior
python --version

# pip actualizado
pip install --upgrade pip
```

### Instalación

#### Opción 1: Script Automático (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/equality-europe.git
cd equality-europe

# Ejecutar script de inicio
python app/run.py
```

El script automáticamente:
1. ✅ Verifica dependencias
2. ✅ Instala paquetes faltantes
3. ✅ Valida estructura de datos
4. ✅ Lanza el dashboard

#### Opción 2: Manual

```bash
# 1. Instalar dependencias
pip install -r app/requirements.txt

# 2. Ejecutar aplicación
streamlit run app/app.py

# 3. Abrir navegador en http://localhost:8501
```

### 🐳 Docker (Próximamente)

```bash
docker build -t equality-dashboard .
docker run -p 8501:8501 equality-dashboard
```

---

## 📁 Estructura del Proyecto

```
Equality/
│
├── 📂 app/                          # 🎯 Aplicación Streamlit
│   ├── app.py                       # ⚙️ Aplicación principal (1,000+ líneas)
│   ├── config.py                    # 🔧 Configuración global
│   ├── data_loader.py               # 📥 Carga y limpieza de datos
│   ├── visualizations.py            # 📊 Gráficos Plotly
│   ├── components.py                # 🎨 Componentes UI
│   ├── analytics.py                 # 📈 Análisis estadístico
│   ├── requirements.txt             # 📦 Dependencias
│   ├── run.py                       # 🚀 Script de inicio
│   ├── README.md                    # 📖 Documentación de usuario
│   ├── TECHNICAL_DOCS.md            # 🔬 Documentación técnica
│   ├── SUMMARY.md                   # 📋 Resumen ejecutivo
│   └── CAMBIOS.md                   # 📝 Historial de cambios
│
├── 📂 data/                         # 💾 Datos del ESS11
│   ├── ESS11.csv                    # 📄 Dataset principal (~150MB)
│   └── ESS11 codebook.html          # 📚 Diccionario de datos
│
├── 📂 notebooks/                    # 📓 Análisis exploratorio
│   ├── EDA.ipynb                    # 🔬 Análisis exploratorio completo
│   └── preprocesamiento.ipynb       # 🧹 Limpieza de datos
│
├── 📂 docs/                         # 📖 Documentación narrativa
│   └── EDA.md                       # 📝 Guía narrativa del análisis
│
├── README.md                        # 👋 Este archivo
└── START_HERE.md                    # 🎯 Guía de inicio rápido
```

### 🎨 Arquitectura del Sistema

El proyecto sigue un patrón **MVC adaptado para Streamlit**:

```
┌─────────────────────────────────────────────┐
│         Streamlit App (app.py)              │
│            [Controller]                     │
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

---

## 🔬 Variables Analizadas

### Variables Dependientes (Y)

| Variable | Descripción | Escala | Interpretación |
|----------|-------------|--------|----------------|
| **ipeqopta** | Igualdad de Oportunidades | 1-6 | Mayor valor = Mayor apoyo a igualdad |
| **eqpaybg** | Igualdad Salarial | 1-5 | Mayor valor = Mayor apoyo a igualdad salarial |
| **polintr** | Interés Político | 1-4 | Mayor valor = Mayor interés en política |
| **imwbcnt** | Percepción sobre Inmigración | 0-10 | Mayor valor = Percepción más positiva |
| **wsekpwr** | Relaciones de Género | 1-5 | Mayor valor = Mayor percepción de búsqueda de poder |

### Variables Independientes (X)

| Variable | Tipo | Categorías/Rango |
|----------|------|------------------|
| **cntry** | Categórica | 30+ países europeos |
| **gndr** | Binaria | Hombre / Mujer |
| **agea** | Numérica | 15-99 años |
| **edulvlb** | Ordinal | ISCED 0-8 (transformada a 0-26) |
| **prtvtges** | Categórica | Partidos políticos España |

### Variables Derivadas

- **education_level:** Escala ordinal 0-26 desde ISCED
- **age_group:** Tramos de edad (15-24, 25-34, ..., 65+)
- **ideology:** Escala 1-5 (izquierda-derecha) para España
- **nationalism:** Escala 1-5 (bajo-alto) para España

---

## 📊 Metodología

### 🧹 Limpieza de Datos

1. **Eliminación de valores inválidos:**
   - Códigos de no respuesta (77, 88, 99, etc.)
   - Valores "No sabe/No contesta"
   - Registros incompletos en variables clave

2. **Transformaciones:**
   - Inversión de escalas para coherencia interpretativa
   - Conversión ISCED a escala ordinal educativa
   - Creación de tramos de edad
   - Mapeo de partidos políticos a ideología/nacionalismo

3. **Validación:**
   - Verificación de rangos válidos
   - Control de consistencia entre variables
   - Identificación de outliers

### 📈 Análisis Estadístico

#### Tests de Normalidad
- **Shapiro-Wilk** para evaluar distribución de variables
- Resultado: Variables no normales → Uso de estadística no paramétrica

#### Correlaciones
- **Spearman** para evaluar asociaciones monotónicas
- Interpretación de fuerza:
  - |ρ| < 0.3: Débil
  - 0.3 ≤ |ρ| < 0.7: Moderada
  - |ρ| ≥ 0.7: Fuerte

#### Comparaciones de Grupos
- **Mann-Whitney U** para diferencias género
- **Kruskal-Wallis** para diferencias entre múltiples grupos
- Nivel de significancia: α = 0.05

#### Medidas Robustas
- Mediana en lugar de media cuando hay outliers
- Percentiles 25/75 para dispersión
- Top-2 Box (% categorías más altas)

---

## 🔍 Análisis Exploratorio (EDA)

El análisis exploratorio completo se encuentra en:
- **Notebook:** `notebooks/EDA.ipynb` (2,700+ líneas de código)
- **Narrativa:** `docs/EDA.md` (guía técnica y narrativa)

### 📌 Hallazgos Principales

#### 1️⃣ Igualdad de Oportunidades (ipeqopta)

**Tendencias Generales:**
- ✅ Mayor apoyo entre **jóvenes** (gradiente generacional significativo)
- ✅ Mayor apoyo en **niveles educativos altos** (correlación positiva moderada)
- ✅ **Brecha de género:** Mujeres muestran mayor apoyo
- ✅ **Gradiente ideológico:** Mayor apoyo en izquierda política (España)

**Por País:**
- Top 5: Países nórdicos (Noruega, Suecia, Dinamarca) + Holanda
- Bottom 5: Europa del Este (Bulgaria, Hungría)

#### 2️⃣ Igualdad Salarial (eqpaybg)

**Tendencias Generales:**
- ✅ Patrón ascendente con **educación**
- ✅ **Brecha de género** presente pero menor que en ipeqopta
- ✅ Variación significativa entre **segmentos generacionales**

**Insights:**
- Las actitudes hacia igualdad salarial correlacionan positivamente con igualdad de oportunidades
- Diferencias importantes entre países de Europa Occidental vs Oriental

#### 3️⃣ Interés Político (polintr)

**Tendencias Generales:**
- ✅ Mayor en **hombres** que mujeres
- ✅ Aumenta con **edad** y **nivel educativo**
- ✅ Predictor importante de otras actitudes hacia igualdad

**Segmentación:**
- Eje clave para identificar colectivos con baja participación
- Correlaciona con percepción sobre democracia

#### 4️⃣ Percepción sobre Inmigración (imwbcnt)

**Tendencias Generales:**
- ✅ Alta **heterogeneidad** entre países
- ✅ Correlación con **ideología** política
- ✅ Diferencias por **nivel educativo**

**Insights:**
- Tema polarizante con concentración en extremos
- Importante considerar contexto nacional

#### 5️⃣ Relaciones de Género (wsekpwr)

**Tendencias Generales:**
- ✅ **Predictor crítico** para políticas de igualdad
- ✅ Brechas significativas por **demografía e ideología**
- ✅ Variación por **contexto cultural**

---

## 🎨 Panel de Inteligencia

### 🖥️ Secciones del Dashboard

#### 1. 📚 Origen de los Datos
- Contexto del ESS11
- Descripción de variables
- Descarga de datos filtrados
- Muestra interactiva de datos

#### 2. 📖 Explicación de Variables
- Descripciones detalladas
- Estadísticas descriptivas (media, mediana, desviación)
- Test de normalidad (Shapiro-Wilk)
- Métricas de calidad

#### 3. 🔍 Análisis Exploratorio (EDA)

**5 tabs interactivos por variable:**

##### 📊 Distribución General
- Histograma de frecuencias
- Estadísticas completas
- Test de normalidad
- Interpretación automática

##### 👥 Análisis por Género
- Boxplot y violín comparativos
- KPIs: Media H/M, brecha de género
- Test Mann-Whitney U
- Interpretación de significancia

##### 📅 Análisis por Edad
- Tendencia por tramos de edad
- Correlación de Spearman
- KPIs: Gradiente jóvenes-mayores
- Interpretación de fuerza

##### 🎓 Análisis por Educación
- Tendencia por nivel educativo (0-26)
- Correlación de Spearman
- KPIs: Gradiente Q4-Q1
- Interpretación de relación

##### 🌍 Análisis por País
- Mapa coroplético europeo
- Ranking Top 5 / Bottom 5
- Tabla comparativa
- Visualización de diferencias

#### 4. 🇪🇸 Análisis España

**3 tabs especializados:**

##### 🗳️ Por Partido Político
- Gráfico de barras horizontal
- Estadísticas por partido
- Filtro de muestra mínima

##### ⬅️➡️ Por Ideología
- Dispersograma con tendencia
- Gradiente izquierda-derecha
- Correlación de Spearman
- Interpretación

##### 🏴 Por Nacionalismo
- Dispersograma con tendencia
- Correlación con variable
- KPIs y p-values

#### 5. 📈 Matriz de Correlaciones
- Heatmap interactivo Spearman
- Todas las variables dependientes
- Escala de colores RdBu
- Interpretación de valores

#### 6. 💡 Conclusiones
- Hallazgos principales
- Implicaciones para políticas públicas
- Próximos pasos

#### 7. 🤖 Machine Learning
- Placeholder para futuras implementaciones
- Roadmap detallado

### 🎛️ Filtros Interactivos

El panel incluye filtros dinámicos que se aplican a todas las visualizaciones:

- 🌍 **País:** Multi-select (todos los países o selección específica)
- 👥 **Género:** Radio button (Todos/Hombres/Mujeres)
- 📅 **Edad:** Multi-select por tramos (15-24, 25-34, ..., 65+)
- 🎓 **Educación:** Slider por cuartiles educativos
- 🗳️ **Partido Político:** Multi-select (solo España)

**Características:**
- ⚡ Actualización en tiempo real
- 📊 Indicadores de datos filtrados
- ⚠️ Advertencias de calidad de muestra
- 💾 Posibilidad de exportar datos filtrados

---

## 🛠️ Tecnologías

### Core Stack

| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Python** | 3.8+ | Lenguaje principal |
| **Streamlit** | 1.28+ | Framework web interactivo |
| **Pandas** | 2.0+ | Manipulación de datos |
| **NumPy** | 1.24+ | Operaciones numéricas |
| **Plotly** | 5.17+ | Visualizaciones interactivas |
| **SciPy** | 1.11+ | Análisis estadístico |

### Librerías Adicionales

- **pyarrow:** Lectura rápida de CSV
- **pathlib:** Manejo de rutas multiplataforma

### Optimizaciones

- ⚡ **Caché de Streamlit:** Evita recargas innecesarias
- 🚀 **Lazy loading:** Carga de datos bajo demanda
- 📦 **Vectorización:** Operaciones eficientes con NumPy/Pandas

---

## 📖 Documentación

### Para Usuarios

- **[START_HERE.md](START_HERE.md):** Guía de inicio rápido
- **[app/README.md](app/README.md):** Manual de usuario del dashboard
- **[docs/EDA.md](docs/EDA.md):** Guía narrativa del análisis exploratorio

### Para Desarrolladores

- **[app/TECHNICAL_DOCS.md](app/TECHNICAL_DOCS.md):** Arquitectura y componentes técnicos
- **[app/CAMBIOS.md](app/CAMBIOS.md):** Historial de cambios y versiones
- **[app/SUMMARY.md](app/SUMMARY.md):** Resumen ejecutivo del proyecto

### Notebooks

- **[notebooks/EDA.ipynb](notebooks/EDA.ipynb):** Análisis exploratorio completo con código
- **[notebooks/preprocesamiento.ipynb](notebooks/preprocesamiento.ipynb):** Pipeline de limpieza

---

## 📸 Capturas de Pantalla

> _Próximamente: Capturas del dashboard interactivo_

### Vista Principal
- Filtros laterales + KPIs dinámicos
- Mapas de Europa interactivos
- Gráficos comparativos por variable

### Análisis por País
- Mapa coroplético coloreado por intensidad
- Rankings Top/Bottom
- Tabla de estadísticas

### Análisis España
- Dispersogramas ideología vs actitudes
- Comparativas por partido político
- Tendencias políticas

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto:

### Cómo Contribuir

1. **Fork** el repositorio
2. Crea una **rama** para tu feature (`git checkout -b feature/amazing-feature`)
3. **Commit** tus cambios (`git commit -m 'Add amazing feature'`)
4. **Push** a la rama (`git push origin feature/amazing-feature`)
5. Abre un **Pull Request**

### Áreas de Mejora

- 🧪 **Testing:** Implementar tests unitarios y de integración
- 🌐 **i18n:** Internacionalización (inglés, francés, alemán)
- 🤖 **ML:** Modelos predictivos de actitudes
- 📊 **Visualizaciones:** Nuevos tipos de gráficos
- 🚀 **Performance:** Optimizaciones adicionales
- 🐳 **Docker:** Containerización completa
- ☁️ **Deploy:** Configuración para cloud (AWS, GCP, Azure)

### Código de Conducta

- Sé respetuoso y constructivo
- Documenta tus cambios
- Sigue las convenciones de código existentes
- Escribe tests para nuevas funcionalidades

---

## 📊 Estadísticas del Proyecto

- **Líneas de código:** ~2,500+ (Python)
- **Notebooks:** 2,700+ líneas (Jupyter)
- **Documentación:** 1,500+ líneas (Markdown)
- **Visualizaciones:** 15+ tipos diferentes
- **Tests estadísticos:** 5+ (Shapiro-Wilk, Mann-Whitney, Spearman, etc.)
- **Países analizados:** 30+
- **Variables procesadas:** 10+ (5 dependientes, 5+ independientes)

---

## 🎓 Aprendizajes

### Técnicas Aplicadas

- ✅ Análisis exploratorio de datos (EDA) completo
- ✅ Limpieza y transformación de datos reales
- ✅ Estadística inferencial no paramétrica
- ✅ Visualización interactiva con Plotly
- ✅ Desarrollo de aplicaciones web con Streamlit
- ✅ Arquitectura modular y escalable
- ✅ Documentación técnica profesional
- ✅ Control de versiones con Git

### Skills Desarrollados

- 🐍 Python avanzado (Pandas, NumPy, SciPy)
- 📊 Visualización de datos (Plotly, Matplotlib)
- 🌐 Desarrollo web (Streamlit)
- 📈 Análisis estadístico
- 📖 Storytelling con datos
- 🔧 Ingeniería de software (arquitectura, testing, documentación)

---

## 📄 Licencia

Este proyecto no tiene ninguna Licencia.

**Datos del ESS:**
- Los datos del European Social Survey están disponibles bajo su propia licencia
- Citar apropiadamente: ESS Round 11 (2023). Data file edition 1.0. Sikt - Norwegian Agency for Shared Services in Education and Research, Norway - Data Archive and distributor of ESS data for ESS ERIC

---

## 👥 Autores

**Proyecto desarrollado como parte del Bootcamp de Data Analytics por Paula Eulalia Bosch García de Araoz, investigadora del Instituto de Políticas y Bienes Públicos del CSIC (España)**

- Análisis exploratorio y limpieza de datos
- Desarrollo del dashboard interactivo
- Documentación técnica y narrativa

---

## 🙏 Agradecimientos

- **European Social Survey (ESS)** por proporcionar datos de alta calidad
- **Streamlit** por el framework de visualización
- **Plotly** por las librerías de gráficos interactivos
- **Bootcamp Data Analytics** por la formación y apoyo

---

## 📧 Contacto

¿Preguntas, sugerencias o colaboraciones?

- 📧 Email: [paula.bosch@csic.es]
- 💼 LinkedIn: [www.linkedin.com/in/paula-bosch-garcía-de-araoz-795909229]
- 🐙 GitHub: [@Paula25082000]

---

<div align="center">

**⭐ Si este proyecto te ha sido útil, considera darle una estrella ⭐**

**Hecho con ❤️| 2025**

[⬆ Volver arriba](#-equality-in-europe---bi-dashboard)

</div>
