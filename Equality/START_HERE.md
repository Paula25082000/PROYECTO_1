# Panel BI - Igualdad en Europa 🚀

Este proyecto contiene un panel de inteligencia completo para analizar actitudes hacia la igualdad en Europa basado en datos del European Social Survey Round 11.

## 🎯 Inicio Rápido

### Opción 1: Script Automático (Recomendado)
```bash
python app/run.py
```

### Opción 2: Inicio Manual
```bash
# 1. Instalar dependencias
pip install -r app/requirements.txt

# 2. Ejecutar aplicación
streamlit run app/app.py
```

## 📁 Estructura del Proyecto

```
Equality/
├── app/                    # 📊 Panel de Inteligencia Streamlit
│   ├── app.py             # Aplicación principal
│   ├── config.py          # Configuración
│   ├── data_loader.py     # Carga de datos
│   ├── visualizations.py  # Gráficos Plotly
│   ├── components.py      # Componentes UI
│   ├── analytics.py       # Análisis estadístico
│   ├── requirements.txt   # Dependencias
│   ├── run.py            # Script de inicio
│   ├── README.md         # Documentación de usuario
│   ├── TECHNICAL_DOCS.md # Documentación técnica
│   └── SUMMARY.md        # Resumen ejecutivo
│
├── data/                  # 📂 Datos del ESS11
│   ├── ESS11.csv         # Dataset principal
│   └── ESS11 codebook.html
│
├── docs/                  # 📖 Documentación del proyecto
│   ├── EDA.md            # Guía narrativa del análisis
│   └── EDA2.md
│
├── notebooks/             # 📓 Jupyter Notebooks
│   ├── EDA.ipynb         # Análisis exploratorio completo
│   └── preprocesamiento.ipynb
│
└── README.md             # Este archivo
```

## ✨ Características del Panel

- 🎨 **Interfaz moderna** con CSS personalizado
- 🔍 **Filtros interactivos** por país, género, edad, educación
- 📊 **Visualizaciones dinámicas** con Plotly
- 📈 **KPIs automáticos** (brechas, gradientes)
- 🇪🇸 **Análisis específico de España** (ideología, partidos)
- 🗺️ **Mapas coropléticos** de Europa
- 📉 **Análisis estadístico** completo (Spearman, Mann-Whitney)
- 💾 **Exportación de datos** filtrados

## 📊 Variables Analizadas

1. **Igualdad de Oportunidades** (ipeqopta)
2. **Igualdad Salarial** (eqpaybg)
3. **Interés Político** (polintr)
4. **Percepción sobre Inmigración** (imwbcnt)
5. **Relaciones de Género** (wsekpwr)

## 🛠️ Tecnologías

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- SciPy

## 📖 Documentación

- **Usuario**: `app/README.md`
- **Técnica**: `app/TECHNICAL_DOCS.md`
- **Resumen**: `app/SUMMARY.md`
- **Análisis**: `docs/EDA.md`

## 🚀 Próximos Pasos

1. Ejecutar el panel: `python app/run.py`
2. Explorar el análisis en `notebooks/EDA.ipynb`
3. Leer la documentación en `docs/EDA.md`
4. Consultar documentación técnica en `app/TECHNICAL_DOCS.md`

---

**¡Disfruta explorando los datos!** 📊✨
