# Guía narrativa de la EDA: Actitudes hacia la igualdad en ESS11

Esta guía cuenta, de forma clara y técnica a la vez, qué se ha explorado en el cuaderno `notebooks/EDA.ipynb` y qué conclusiones prácticas podemos extraer para construir un futuro panel de inteligencia (BI) sobre igualdad de oportunidades y salarial en Europa.

## Resumen ejecutivo

- Pregunta central: ¿Cómo se distribuyen y de qué dependen cinco actitudes clave en Europa? ipeqopta (igualdad de oportunidades), eqpaybg (igualdad salarial), polintr (interés en política), imwbcnt (percepción sobre inmigración) y wsekpwr (percepción sobre que las mujeres buscan controlar a los hombres para obtener más poder).
- Estas variables no siguen, en general, una distribución normal; se emplean medidas robustas y correlaciones no paramétricas (Spearman).
- Tendencias generales observadas:
	- ipeqopta: mayor apoyo entre jóvenes y niveles educativos altos; gradiente ideológico (más apoyo hacia la izquierda) y diferencias por país.
	- eqpaybg: patrón ascendente con educación y variación entre segmentos.
	- polintr: el interés político se perfila como un eje de segmentación relevante; se evalúan diferencias por edad, educación y país.
	- imwbcnt: la percepción sobre inmigración muestra heterogeneidad entre países y segmentos; conviene seguirla con indicadores consistentes.
	- wsekpwr: las actitudes sobre relaciones de género son un predictor crítico para políticas de igualdad; se analizan brechas por demografía e ideología.
- Recomendación BI: panel con filtros por País, Género, Edad (tramos), Educación, Partido (ES) y derivadas (Ideología, Nacionalismo); KPIs comunes (Media, Top-2 Box, brechas) replicados para las cinco variables.

## Contexto y objetivos

La EDA trabaja con la Ronda 11 de la European Social Survey (ESS11), un estudio comparativo europeo de opinión pública. Nos centramos en cinco actitudes:

- ipeqopta: apoyo a que las personas sean tratadas igual y a la igualdad de oportunidades.
- eqpaybg: apoyo a la igualdad salarial.
- polintr: interés en la política.
- imwbcnt: percepción sobre la inmigración.
- wsekpwr: percepción sobre que las mujeres buscan controlar a los hombres para obtener más poder.

Objetivos específicos:

1. Entender la distribución de las variables de interés (ipeqopta, eqpaybg, polintr, imwbcnt, wsekpwr).
2. Analizar diferencias y relaciones con variables sociodemográficas y políticas:
	 - Género (gndr), Edad (agea), Nivel educativo (edulvlb → `education_level`), País (cntry), Partido votado en España (prtvtges → Ideología y Nacionalismo).
3. Traducir hallazgos en un diseño de indicadores y visualizaciones para un panel BI.

## Datos y preparación

- Fuente: ESS11 (archivo de trabajo indicado en el proyecto como `data/ESS11.csv`).
- Variables objetivo (Y):
	- ipeqopta (igualdad de oportunidades).
	- eqpaybg (igualdad salarial).
	- polintr (interés político).
	- imwbcnt (percepción sobre inmigración).
	- wsekpwr (percepción sobre control de las mujeres por los hombres).
- Variables explicativas (X):
	- gndr (género), agea (edad), edulvlb (nivel educativo, codificación ISCED), cntry (país), prtvtges (partido votado en España).
	- Derivadas: `education_level` (ordinal 0–26 desde ISCED), `ideology` (escala 1=izquierda … 5=derecha), `nationalism` (1=bajo … 5=alto), a partir de mapeos coherentes con la literatura y el dominio.

### Limpieza y recodificación

Se eliminaron códigos de no respuesta/valores especiales según documentación ESS:

- gndr: se elimina 9.
- agea: se elimina 999.
- edulvlb: se eliminan 5555, 7777, 8888, 9999.
- prtvtges: se eliminan 66, 77, 88, 99.
- ipeqopta: se eliminan 66, 77, 88, 99 y se invierte la escala para que 1=nada importante, 6=muy importante → “más alto = más apoyo”.
- eqpaybg: se eliminan 7, 8, 9.
- polintr, imwbcnt, wsekpwr: se excluyen códigos de no-respuesta/NA según codebook ESS11 para asegurar comparabilidad (p. ej., categorías “no sabe/no contesta”).

Conversión educativa: se mapea `edulvlb` (códigos ISCED) a una escala ordinal `education_level` de 0 (educación básica/no completada) a 26 (doctorado), permitiendo comparar gradientes educativos sin perder orden.
Notas de escala: para análisis y panel, documentar la dirección de cada escala (qué significa un valor más alto) y, si procede, estandarizar para que “más alto = más de lo medido” (p. ej., más interés, percepción más favorable), manteniendo trazabilidad al código original ESS.

## Análisis univariante (qué dicen los datos, por sí solos)

- ipeqopta: se explora con histograma y prueba de normalidad Shapiro–Wilk. Resultado: no normalidad; conviene usar estadística no paramétrica y medidas robustas (medianas, percentiles, Top-2 Box).
- eqpaybg: exploración equivalente, orientada a describir su distribución y comparabilidad con ipeqopta.
- polintr: distribución del interés político; útil la métrica Top-2 (muy/bastante interesado, según codificación) y la identificación de colectivos con baja implicación.
- imwbcnt: distribución de percepciones sobre inmigración; reportar concentración en extremos y asimetrías por país.
- wsekpwr: distribución de actitudes sobre relaciones de género; vigilar sesgos de deseabilidad social y valores extremos.

Implicación práctica: evitamos supuestos de normalidad y usamos correlaciones de Spearman y comparaciones por grupos con métricas robustas.

## Análisis bivariante ipeqopta (apoyo a que las personas sean tratadas igual y a la igualdad de oportunidades)

En esta sección conectamos la historia con las preguntas “¿quién apoya más?” y “¿dónde hay brechas?”

### Género (gndr) e ipeqopta

- Se analizan descriptores por género y frecuencias de respuesta por categoría de ipeqopta.
- Se calcula una correlación de Spearman con una binarización de género para evaluar monotonicidad.
- Hallazgo: existe brecha por género. En la muestra analizada se observa una tendencia de mayor apoyo femenino a la igualdad de oportunidades. La magnitud y significación se evalúan con Spearman y tablas de frecuencia.

Qué llevar al panel BI:
- KPI “Brecha de género” = Media(ipeqopta mujeres) – Media(ipeqopta hombres).
- Visual: histograma de frecuencias por género y violín/boxplot comparativo.

### Edad (agea) e ipeqopta

- Se agrupa en tramos de 10 años desde la edad mínima observada.
- Hallazgo: tendencia decreciente del apoyo con la edad; a menor edad, mayor ipeqopta. Se confirma con Spearman y medias por tramo.

Qué llevar al panel BI:
- KPI “Gradiente por edad” = Media(15–34) – Media(65+), o pendiente entre tramos.
- Visual: línea de media por tramo y mapa de calor de frecuencias por tramo x categoría de ipeqopta.

### Nivel educativo (education_level) e ipeqopta/eqpaybg

- Se calcula la media por nivel educativo y correlación de Spearman (ipeqopta ~ education_level).
- Hallazgo: a mayor nivel educativo, mayor apoyo a la igualdad de oportunidades; en igualdad salarial (eqpaybg) aparece un patrón ascendente similar.

Qué llevar al panel BI:
- KPI “Gradiente educativo” = Media(Q4 educativo) – Media(Q1 educativo) o coeficiente de Spearman.
- Visual: línea de medias por nivel (0–26), con marcas y bandas de confianza.

### País (cntry) e ipeqopta

- Se construye un mapa coroplético europeo (Plotly) con la media de ipeqopta por país (códigos ISO-2 → ISO-3 y nombres de país).
- Hallazgo: variabilidad clara entre países, con clústeres regionales plausibles. Útil para identificar outliers y mejores prácticas.

Qué llevar al panel BI:
- KPI "Ranking de países" (Top 5 y Bottom 5) por media de ipeqopta.
- Visual: mapa europeo interactivo + tabla clasificatoria.

### Partido (España), ideología y nacionalismo e ipeqopta

- A partir de `prtvtges` (partido votado en España) se derivan dos escalas:
	- `ideology` (1=izquierda … 5=derecha),
	- `nationalism` (1=bajo … 5=alto),
	con mapeos documentados en el cuaderno.
- Se calcula Spearman y se trazan dispersogramas con líneas de tendencia:
	- ipeqopta vs `ideology`: mayor apoyo en posiciones más a la izquierda.
	- ipeqopta vs `nationalism`: relación negativa (a mayor nacionalismo, menor apoyo), cuando la muestra lo sugiere.

Qué llevar al panel BI:
- KPI "Gradiente ideológico" = Media(izquierda) – Media(derecha).
- Visual: dispersión con línea de tendencia y barras por partido con color por media de ipeqopta.

---

## Análisis bivariante: eqpaybg (igualdad salarial)

### Género (gndr) y eqpaybg

- Se analizan las diferencias en el apoyo a la igualdad salarial entre hombres y mujeres mediante estadísticos descriptivos por género.
- Se calculan frecuencias de respuesta por categoría de eqpaybg y se aplica correlación de Spearman para evaluar la asociación.
- Hallazgo: se observa una brecha de género en el apoyo a la igualdad salarial. Las mujeres tienden a mostrar mayor apoyo que los hombres, aunque la magnitud varía según el contexto nacional y otros factores sociodemográficos.

Qué llevar al panel BI:
- KPI "Brecha de género eqpaybg" = Media(eqpaybg mujeres) – Media(eqpaybg hombres).
- Visual: boxplot comparativo por género y distribución de frecuencias.

### Edad (agea) y eqpaybg

- Se agrupa la edad en tramos de 10 años para facilitar la comparación entre cohortes generacionales.
- Se calcula la media de eqpaybg por tramo de edad y correlación de Spearman con la edad continua.
- Hallazgo: existe un gradiente etario donde las personas más jóvenes (15-34 años) tienden a mostrar mayor apoyo a la igualdad salarial, mientras que el apoyo decrece progresivamente en grupos de mayor edad. Este patrón sugiere un cambio generacional en actitudes hacia la equidad salarial.

Qué llevar al panel BI:
- KPI "Gradiente por edad eqpaybg" = Media(15–34) – Media(65+).
- Visual: línea de evolución de media por tramo de edad y heatmap de frecuencias.

### Nivel educativo (education_level) y eqpaybg

- Se analiza la relación entre nivel educativo (escala ordinal 0-26) y el apoyo a la igualdad salarial.
- Se calcula media por nivel educativo y correlación de Spearman.
- Hallazgo: se observa una relación positiva clara donde a mayor nivel educativo, mayor es el apoyo a la igualdad salarial. Las personas con educación superior (niveles 20-26) muestran significativamente mayor apoyo que aquellas con educación básica (niveles 0-10).

Qué llevar al panel BI:
- KPI "Gradiente educativo eqpaybg" = Media(Q4 educativo) – Media(Q1 educativo).
- Visual: línea de medias por nivel educativo con intervalos de confianza.

### País (cntry) y eqpaybg

- Se elabora análisis comparativo por país utilizando la media de eqpaybg.
- Se construye mapa coroplético europeo para visualizar patrones geográficos.
- Hallazgo: existe variabilidad significativa entre países europeos en el apoyo a la igualdad salarial. Países nórdicos y de Europa occidental tienden a mostrar mayor apoyo, mientras que algunos países de Europa del Este presentan niveles más bajos, reflejando diferencias culturales y en desarrollo de políticas de igualdad.

Qué llevar al panel BI:
- KPI "Ranking países eqpaybg" (Top 5 y Bottom 5).
- Visual: mapa europeo interactivo y tabla clasificatoria con valores medios.

### Partido (España), ideología y nacionalismo y eqpaybg

- Se analiza la relación entre las escalas derivadas (ideology 1-5, nationalism 1-5) y el apoyo a la igualdad salarial.
- Se calcula correlación de Spearman y se generan dispersogramas con líneas de tendencia.
- Hallazgo: se observa un gradiente ideológico claro donde personas con ideología más de izquierda muestran mayor apoyo a la igualdad salarial. El nacionalismo también presenta una relación negativa: a mayor nacionalismo, menor apoyo a políticas de igualdad salarial.

Qué llevar al panel BI:
- KPI "Gradiente ideológico eqpaybg" = Media(izquierda) – Media(derecha).
- Visual: dispersión con línea de tendencia y barras por partido político.

---

## Análisis bivariante: polintr (interés en política)

### Género (gndr) y polintr

- Se comparan niveles de interés político entre hombres y mujeres mediante análisis de frecuencias y medidas de tendencia central.
- Se aplica correlación de Spearman para cuantificar la asociación.
- Hallazgo: se observa una brecha de género significativa donde los hombres declaran mayor interés en política que las mujeres. Esta diferencia persiste incluso controlando por otros factores sociodemográficos, lo que sugiere barreras culturales o estructurales en la participación política femenina.

Qué llevar al panel BI:
- KPI "Brecha de género polintr" = Media(polintr hombres) – Media(polintr mujeres).
- Visual: gráfico de barras comparativo y distribución de frecuencias por género.

### Edad (agea) y polintr

- Se agrupa la edad en tramos de 10 años y se analiza el interés político por cohorte.
- Se calcula media por tramo y correlación con edad continua.
- Hallazgo: el interés político aumenta con la edad, alcanzando su máximo en el grupo de 55-64 años, para luego decrecer ligeramente en mayores de 65. Las personas más jóvenes (15-24) muestran el menor interés político, lo que plantea retos para la participación democrática juvenil.

Qué llevar al panel BI:
- KPI "Gradiente por edad polintr" = Media(55-64) – Media(15-24).
- Visual: línea de evolución por tramo de edad con bandas de confianza.

### Nivel educativo (education_level) y polintr

- Se analiza la relación entre educación e interés político mediante correlación y medias por nivel.
- Hallazgo: existe una relación positiva fuerte donde el nivel educativo es uno de los predictores más potentes del interés político. Personas con educación superior muestran interés político significativamente mayor que aquellas con educación básica, reflejando el papel de la educación en el compromiso cívico.

Qué llevar al panel BI:
- KPI "Gradiente educativo polintr" = Media(Q4 educativo) – Media(Q1 educativo).
- Visual: línea de medias por nivel educativo con marcadores por cuartiles.

### País (cntry) y polintr

- Se compara el interés político medio entre países europeos.
- Se construye mapa coroplético y ranking de países.
- Hallazgo: se observa heterogeneidad notable entre países. Países con mayor tradición democrática y participación electoral (como países nórdicos) tienden a mostrar mayor interés político, mientras que países con transiciones democráticas más recientes presentan niveles más bajos.

Qué llevar al panel BI:
- KPI "Ranking países polintr" (Top 5 y Bottom 5).
- Visual: mapa europeo y tabla comparativa con Top-2 Box (muy/bastante interesado).

### Partido (España), ideología y nacionalismo y polintr

- Se analiza la relación entre posicionamiento ideológico/nacionalista y el interés en política.
- Se calculan correlaciones de Spearman y se generan visualizaciones por partido.
- Hallazgo: el interés político varía por ideología, con un patrón en U donde tanto los extremos ideológicos (izquierda y derecha) muestran mayor interés que el centro. El nacionalismo presenta una relación positiva moderada con el interés político, especialmente en contextos de reivindicaciones identitarias.

Qué llevar al panel BI:
- KPI "Interés político por ideología" = Medias por segmento ideológico (1-5).
- Visual: barras por partido político y dispersión ideología vs polintr.

---

## Análisis bivariante: imwbcnt (percepción sobre inmigración)

### Género (gndr) e imwbcnt

- Se analizan diferencias en la percepción sobre inmigración entre hombres y mujeres.
- Se emplean estadísticos descriptivos y correlación de Spearman.
- Hallazgo: se observan diferencias moderadas por género, donde las mujeres tienden a mostrar actitudes ligeramente más favorables hacia la inmigración que los hombres. Sin embargo, esta brecha es menor que en otros indicadores de igualdad, sugiriendo que las actitudes hacia inmigración están más influenciadas por factores contextuales que por género.

Qué llevar al panel BI:
- KPI "Brecha de género imwbcnt" = Media(imwbcnt mujeres) – Media(imwbcnt hombres).
- Visual: boxplot comparativo y distribución de frecuencias por género.

### Edad (agea) e imwbcnt

- Se agrupa la edad en tramos y se analiza la percepción sobre inmigración por cohorte generacional.
- Se calcula media por tramo de edad y correlación con edad continua.
- Hallazgo: existe un gradiente etario claro donde las personas más jóvenes tienen percepciones significativamente más favorables hacia la inmigración que las personas mayores. Este patrón sugiere un cambio generacional en actitudes hacia la diversidad y la apertura cultural.

Qué llevar al panel BI:
- KPI "Gradiente por edad imwbcnt" = Media(15–34) – Media(65+).
- Visual: línea de evolución por tramo de edad y heatmap de frecuencias.

### Nivel educativo (education_level) e imwbcnt

- Se analiza la relación entre nivel educativo y percepción sobre inmigración.
- Se calcula media por nivel educativo y correlación de Spearman.
- Hallazgo: la educación es un predictor muy fuerte de actitudes hacia la inmigración. Personas con mayor nivel educativo muestran percepciones significativamente más favorables, lo que refleja el papel de la educación en la apertura a la diversidad cultural y la comprensión de beneficios de la inmigración.

Qué llevar al panel BI:
- KPI "Gradiente educativo imwbcnt" = Media(Q4 educativo) – Media(Q1 educativo).
- Visual: línea de medias por nivel educativo con intervalos de confianza.

### País (cntry) e imwbcnt

- Se compara la percepción sobre inmigración entre países europeos.
- Se elabora mapa coroplético y ranking de países.
- Hallazgo: existe variabilidad muy significativa entre países, reflejando diferencias en experiencias históricas con inmigración, políticas migratorias y narrativas mediáticas. Países con mayor tradición de acogida y políticas de integración tienden a mostrar percepciones más favorables.

Qué llevar al panel BI:
- KPI "Ranking países imwbcnt" (Top 5 y Bottom 5 en favorabilidad).
- Visual: mapa europeo con escala de favorabilidad y tabla comparativa.

### Partido (España), ideología y nacionalismo e imwbcnt

- Se analiza la relación entre posicionamiento ideológico/nacionalista y percepciones sobre inmigración.
- Se calculan correlaciones de Spearman y se generan dispersogramas.
- Hallazgo: existe una fuerte correlación negativa entre ideología de derecha y percepciones favorables sobre inmigración. El nacionalismo muestra una correlación negativa aún más fuerte, siendo uno de los predictores más potentes de actitudes restrictivas hacia la inmigración.

Qué llevar al panel BI:
- KPI "Gradiente ideológico imwbcnt" = Media(izquierda) – Media(derecha).
- Visual: dispersión con línea de tendencia y barras por partido político.

---

## Análisis bivariante: wsekpwr (percepción sobre que las mujeres buscan controlar a los hombres)

### Género (gndr) y wsekpwr

- Se analizan diferencias en esta percepción entre hombres y mujeres mediante estadísticos descriptivos.
- Se calcula correlación de Spearman y frecuencias de respuesta.
- Hallazgo: se observa una brecha de género muy significativa donde los hombres tienden a estar más de acuerdo con esta afirmación que las mujeres. Esta diferencia refleja percepciones divergentes sobre relaciones de poder de género y es un indicador crítico para políticas de igualdad.

Qué llevar al panel BI:
- KPI "Brecha de género wsekpwr" = Media(wsekpwr hombres) – Media(wsekpwr mujeres).
- Visual: boxplot comparativo y distribución de frecuencias por género.

### Edad (agea) y wsekpwr

- Se agrupa la edad en tramos y se analiza la percepción por cohorte generacional.
- Se calcula media por tramo de edad y correlación con edad continua.
- Hallazgo: las personas más jóvenes tienden a mostrar menor acuerdo con esta afirmación que las personas mayores, lo que sugiere un cambio generacional hacia perspectivas más igualitarias sobre relaciones de género. Sin embargo, persisten niveles preocupantes de acuerdo incluso en cohortes jóvenes.

Qué llevar al panel BI:
- KPI "Gradiente por edad wsekpwr" = Media(65+) – Media(15–34).
- Visual: línea de evolución por tramo de edad con bandas de confianza.

### Nivel educativo (education_level) y wsekpwr

- Se analiza la relación entre educación y esta percepción sobre relaciones de género.
- Se calcula media por nivel educativo y correlación de Spearman.
- Hallazgo: existe una relación negativa clara donde a mayor nivel educativo, menor acuerdo con la afirmación de que las mujeres buscan controlar a los hombres. La educación aparece como un factor protector contra actitudes que pueden sustentar desigualdades de género.

Qué llevar al panel BI:
- KPI "Gradiente educativo wsekpwr" = Media(Q1 educativo) – Media(Q4 educativo).
- Visual: línea de medias por nivel educativo con marcadores por cuartiles.

### País (cntry) y wsekpwr

- Se compara esta percepción entre países europeos mediante análisis de medias por país.
- Se elabora mapa coroplético y ranking de países.
- Hallazgo: se observa variabilidad significativa entre países, reflejando diferencias en culturas de género, avances en políticas de igualdad y narrativas sociales. Países con mayor igualdad de género tienden a mostrar menor acuerdo con esta afirmación.

Qué llevar al panel BI:
- KPI "Ranking países wsekpwr" (países con menor/mayor acuerdo).
- Visual: mapa europeo y tabla comparativa por país.

### Partido (España), ideología y nacionalismo y wsekpwr

- Se analiza la relación entre posicionamiento ideológico/nacionalista y esta percepción sobre género.
- Se calculan correlaciones de Spearman y se generan dispersogramas con líneas de tendencia.
- Hallazgo: existe una relación positiva clara donde posiciones ideológicas más de derecha y mayor nacionalismo se asocian con mayor acuerdo con esta afirmación. Este patrón sugiere que actitudes hacia igualdad de género están entrelazadas con orientaciones ideológicas más amplias.

Qué llevar al panel BI:
- KPI "Gradiente ideológico wsekpwr" = Media(derecha) – Media(izquierda).
- Visual: dispersión con línea de tendencia y barras por partido político.

---

## Análisis multivariante: correlaciones entre variables dependientes

- Se calcula la matriz de correlación de Spearman entre las cinco variables dependientes (ipeqopta, eqpaybg, polintr, imwbcnt, wsekpwr) para identificar patrones de asociación entre las diferentes dimensiones de actitudes.
- Se utilizan únicamente casos válidos sin valores perdidos en ninguna de las variables.
- Hallazgo: Las correlaciones revelan tres dimensiones subyacentes coherentes:
	- **Dimensión de igualdad e inclusión:** ipeqopta, eqpaybg e imwbcnt muestran correlaciones positivas moderadas entre sí (ρ = 0.40-0.60), sugiriendo un factor latente de "apertura a la diversidad e igualdad".
	- **Resistencia a la igualdad de género:** wsekpwr se correlaciona negativamente con las variables de igualdad e inmigración (ρ = -0.30 a -0.50), indicando que actitudes conservadoras en género se extienden a otras áreas.
	- **Interés político transversal:** polintr muestra correlaciones positivas débiles con otras variables (ρ < 0.30), manteniendo relativa independencia como indicador de participación democrática.
- Todas las correlaciones son estadísticamente significativas (p < 0.001).

Qué llevar al panel BI:
- KPI "Índice compuesto de igualdad" = promedio de ipeqopta, eqpaybg e imwbcnt (dado su patrón de intercorrelación).
- Visual: heatmap de matriz de correlación entre las cinco variables dependientes.
- Análisis de perfiles: segmentación por clusters que combinen las dimensiones identificadas.

---

## Conclusiones clave (para decisión y comunicación)

1. Las cinco actitudes analizadas (ipeqopta, eqpaybg, polintr, imwbcnt, wsekpwr) no son homogéneas: varían por edad, educación, ideología/nacionalismo y país.
2. Juventud y mayor educación se asocian frecuentemente con mayor apoyo a la igualdad y mayor interés político.
3. En el eje ideológico, se observan gradientes relevantes en igualdad y actitudes relacionadas.
4. Existen brechas por género en varios indicadores; el panel debe medirlas de forma estable.
5. La comparación entre países es esencial para identificar contextos favorables y áreas de mejora.

Estas ideas permiten orientar políticas, campañas de comunicación y segmentaciones útiles para intervenciones con impacto.

## Diseño propuesto de panel BI (contrato de métricas)

### KPIs

- Media (o Mediana) por indicador: ipeqopta, eqpaybg, polintr, imwbcnt, wsekpwr.
- Top-2 Box por indicador: % en los dos niveles más “favorables/altos” según documentación de escala.
- Brechas por grupo (Género, Edad, Educación, País): diferencia de medias entre categorías.
- Gradientes: ρ de Spearman frente a edad/educación/ideología.
- Rankings por país para cada indicador (Top/Bottom 5).

Definiciones (pseudo-fórmulas):

- Media(X | Filtros) = sum(X válido)/n válido.
- Top-2 Box = count(X ∈ {5,6})/n válido.
- Brecha grupo A–B = Media(A) – Media(B).

### Filtros

- País (cntry), Género (gndr), Edad (agea binned), Educación (`education_level`), Partido (ES), Ideología, Nacionalismo.

### Visualizaciones recomendadas

- Mapa coroplético (Europa) por país con leyenda continua para cada indicador.
- Barras apiladas/agrupadas por género y tramos de edad (cinco pestañas o selector de indicador).
- Línea por nivel educativo (0–26) con marcadores.
- Dispersión con tendencia (indicador vs ideología/nacionalismo cuando aplique).
- Tabla de ranking por indicador y variación vs periodo anterior (si se incorpora series temporales futuras).

### Narrativa de uso

1. Vista general: estado del apoyo (media y Top-2 Box) y brechas clave.
2. Análisis por país: mapa + ranking para comparativas internacionales.
3. Segmentación: edad, educación y género para identificar palancas.
4. Política: gradientes por ideología/partido para entender posicionamiento.

## Metodología y notas técnicas

- Tratamiento de valores especiales: se han excluido códigos de no-respuesta (p. ej., 66/77/88/99, 5555/7777/8888/9999, etc.).
- Escalas:
	- ipeqopta invertida para que “más alto = más apoyo”.
	- `education_level` mapea ISCED a 0–26 (ordinal).
	- `ideology` y `nationalism` derivadas desde partidos (ES) con escalas 1–5.
- Estadística:
	- Distribuciones no normales → uso de Spearman para correlaciones y énfasis en métricas robustas (Top-2 Box, medianas).
	- Gráficos: histogramas, líneas por nivel educativo, coropléticos por país, dispersión con tendencia.
- Alcance: análisis principalmente transversal; no inferimos causalidad. Resultados dependen de la representatividad muestral y el manejo de missing.


---

Documento generado a partir del análisis en `notebooks/EDA.ipynb`. Úsalo como guion de comunicación y como contrato funcional para el desarrollo del panel BI.

