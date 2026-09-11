# Workshop 1 — Data Warehouse de Reclutamiento Tecnologico

## 1. Objetivo del proyecto

En este trabajo desarrolle un pipeline ETL en Python para procesar un archivo CSV con solicitudes de empleo en el sector tecnologico y construir un Data Warehouse dimensional.

El proposito central es analizar el proceso de seleccion mediante consultas en SQL e indicadores en Power BI. Todo el analisis analitico se realiza directamente sobre el Data Warehouse en PostgreSQL y no sobre el archivo plano inicial.

## 2. Contexto de negocio

Una organizacion dedicada al reclutamiento IT recibe postulaciones de candidatos distribuidos globalmente, con distintos niveles de seniority, tecnologias y años de experiencia.

Durante el proceso, cada postulante presenta dos pruebas tecnicas:

* Code Challenge Score
* Technical Interview Score

El equipo requiere evaluar el comportamiento global de las contrataciones y responder preguntas operativas como:

* ¿En que periodos del año se concretan mas contrataciones?
* ¿Cuales tecnologias registran mayor cantidad de contratados?
* ¿Que perfiles de candidatos obtienen mejores resultados?
* ¿Que paises concentran la mayor cantidad de postulantes contratados?
* ¿Como influyen los puntajes de las evaluaciones tecnicas en el resultado final?

## 3. Requisitos de negocio

| ID | Requisito | Pregunta de negocio | Decision apoyada |
| R1 | Tendencias de contratacion | ¿Como varian las aplicaciones, contrataciones y la tasa de contratacion por mes? | Planificar la capacidad del equipo de reclutamiento y detectar estacionalidades. |
| R2 | Analisis por tecnologia | ¿Que tecnologias generan mas contrataciones y mejores tasas de exito? | Orientar las estrategias de busqueda y ejecucion de vacantes. |
| R3 | Analisis de perfiles | ¿Como cambia la contratacion segun el seniority y los años de experiencia? | Identificar que perfiles responden mejor al proceso de seleccion. |
| R4 | Analisis geografico | ¿Que paises concentran mayor actividad de postulacion y efectividad? | Definir ubicaciones prioritarias para la busqueda de talento. |
| R5 | Analisis de evaluaciones | ¿Como impactan las puntuaciones tecnicas en la condicion de contratado? | Evaluar el filtro de las pruebas y la consistencia de los puntajes requeridos. |

## 4. Requisitos adicionales propuestos

### R4 — Analisis geografico

 Analiza las aplicaciones y contrataciones distribuidas por pais.

 Permite identificar las regiones geográficas con mayor volumen de candidatos seleccionados.

 Los requisitos R1, R2 y R3 abarcan tiempo, tecnologia y perfil. El requisito R4 complementa la solucion incorporando la dimension territorial.

> "Se propuso R4 para analizar la distribucion geografica del talento seleccionado, lo cual ayuda a dirigir campañas de reclutamiento hacia los paises con mejores resultados."

### R5 — Analisis de evaluaciones

 Analiza de forma conjunta las notas del Code Challenge Score y de la Technical Interview Score.

 Permite entender el impacto combinado de las dos evaluaciones en la contratacion final.

 La regla de negocio exige un rendimiento minimo en ambas pruebas, por lo que analizarlas de manera individual daria una vision incompleta.

 Se propuso R5 porque la contratacion depende de dos filtros tecnicos simultaneos. Analizarlos juntos permite medir la exigencia real del proceso."

## 5. Trazabilidad de requisitos

| Requisito | Datos requeridos | Dimensiones | Medidas/KPI | Consulta SQL | Visualizacion |
|---|---|---|---|---|---|
| R1 | Fecha, HIRED | Dim_Date | Applications, Hired, Hiring Rate | Tendencia mensual | Grafico de lineas |
| R2 | Tecnologia, HIRED | Dim_Technology | Applications, Hired, Hiring Rate | Resultado por tecnologia | Barras horizontales |
| R3 | Seniority, YOE, HIRED | Dim_Candidate_Profile | Applications, Hired, Hiring Rate | Resultado por perfil | Columnas agrupadas |
| R4 | Pais, HIRED | Dim_Country | Applications, Hired, Hiring Rate | Resultado por pais | Top 15 paises |
| R5 | Code Challenge, Interview, HIRED | Fact_Applications | Applications, Hired, Hiring Rate | Segmentos de evaluacion | Barras por segmento |

## 6. Dataset y profiling inicial

El archivo fuente de entrada se encuentra en la ruta:

```text
data/raw/candidates.csv

## 7. Proceso de negocio

El proceso analizado corresponde a la evaluacion tecnica de postulaciones dentro del flujo de reclutamiento de la organizacion. Cada registro del archivo de origen contiene los atributos del candidato, la fecha de postulacion, el pais de origen, la tecnologia, los años de experiencia y las notas obtenidas en sus dos evaluaciones tecnicas.

## 8. Granularidad (Grain)

El nivel de detalle definido para la tabla de hechos es:

Una fila en Fact_Applications representa una postulación valida realizada por un candidato en una fecha, pais, tecnologia y perfil profesional especificos.

La tabla de hechos almacena eventos individuales a nivel de aplicacion individual y no datos agregados por periodos, regiones o tecnologias.

## 9. Regla de negocio HIRED

La condicion obligatoria para determinar si un candidato es contratado se define mediante la siguiente regla:

text
HIRED = (Code Challenge Score >= 7) AND (Technical Interview Score >= 7)

## 10. Modelo dimensional

Se diseño un esquema en estrella (Star Schema) compuesto por una tabla de hechos central y cuatro tablas de dimension:

| Tabla | Proposito |
|---|---|
| Dim_Date | Soporta el analisis temporal por dia, mes, trimestre y año. |
| Dim_Technology | Clasifica las métricas segun la tecnologia del candidato. |
| Dim_Candidate_Profile | Almacena el seniority, los años de experiencia y los rangos de experiencia. |
| Dim_Country | Permite analizar los resultados por pais de origen. |
| Fact_Applications | Almacena las llaves foraneas, los puntajes de las pruebas y las medidas numericas acumuladas. |

Para mantener la integridad del modelo y desvincular el Data Warehouse de los identificadores del archivo fuente, cada dimension utiliza una llave sustituta (surrogate key) de tipo entero: `date_key`, `country_key`, `technology_key` y `candidate_profile_key`.

## 11. Proceso ETL

El flujo de Extraccion, Transformacion y Carga (ETL) fue construido en Python utilizando Pandas y consta de cinco etapas:

1. Extract: Lectura del archivo plano `candidates.csv` en un DataFrame de Pandas sin aplicar modificaciones.
2. Prepare: Limpieza de datos, conversion de tipos de datos, validacion de campos vacios y formateo de fechas y categorias.
3. Business Transformation: Aplicacion de la regla de negocio `HIRED` para generar el campo `hired_flag` y creacion de rangos de experiencia profesional.
4. Dimensional Transformation: Construccion de las cuatro tablas de dimension, asignacion de claves sustitutas (surrogate keys) y mapeo de las claves foraneas en la tabla de hechos `Fact_Applications`.
5. Load: Creacion del esquema en PostgreSQL e insercion secuencial de los datos, cargando primero las dimensiones y finalmente la tabla de hechos para respetar la integridad referencial.

Los datos personales de los candidatos (nombres y correos electronicos) fueron excluidos del proceso de carga por no ser requeridos en el analisis analitico.

## 12. Explicacion de metricas
Para el analisis visual y la respuesta a los requerimientos de negocio, se crearon tres medidas principales utilizando lenguaje DAX:

Applications
Calcula la cantidad total de postulaciones evaluadas en el contexto de filtro actual.(Applications)

Hired
Suma el total de postulantes que cumplieron de forma satisfactoria la regla de negocio HIRED. (hired_flag)

Hiring Rate
Calcula la proporcion porcentual de contrataciones respecto al volumen total de aplicaciones. Permite realizar comparaciones equitativas entre grupos o categorias de diferente tamaño.(hired/Aplications)

## 13. Base de datos PostgreSQL
Se utilizo PostgreSQL como motor de base de datos relacional para alojar el Data Warehouse dentro del esquema recruitment_dw.

Esta eleccion garantiza el cumplimiento de restricciones de integridad (Primary Keys y Foreign Keys) y ofrece alta compatibilidad tanto para la carga desde Python como para la consulta conectada desde Power BI.

Los scripts SQL asociados al proyecto se estructuran de la siguiente manera:

sql/create_tables.sql: Contiene las sentencias DDL para la creacion del esquema, tablas de dimension, tabla de hechos y la definicion de claves primarias y foraneas.

sql/analytical_queries.sql: Reune las consultas analiticas que responden a los requerimientos de negocio R1 a R5 directamente desde la base de datos.

sql/validation_queries.sql: Incluye consultas de auditoria para verificar la cantidad de registros cargados, la ausencia de claves huérfanas y la correcta aplicacion de la regla HIRED.

## 14. Conexion con Power BI
El tablero de control interactivo fue conectado al Data Warehouse en PostgreSQL utilizando el modo Import (Importar), debido a que el volumen de 50.000 registros es manejable de forma optima en la memoria local de Power BI Desktop.

Pasos para establecer la conexion:

Ejecutar el pipeline ETL en Python para asegurar la carga completa de los datos en PostgreSQL.

Abrir Power BI Desktop y seleccionar la opcion Obtener datos > Base de datos PostgreSQL.

Configurar el servidor en localhost:5432 y especificar la base de datos recruitment_dw.

Seleccionar el modo de conectividad Importar e ingresar las credenciales del usuario de PostgreSQL.

En la ventana del Navegador, seleccionar las 5 tablas pertenecientes al esquema recruitment_dw (dim_date, dim_country, dim_technology, dim_candidate_profile y fact_applications).

Confirmar la creacion automatica de las relaciones de 1 a muchos desde las dimensiones hacia la tabla de hechos en la Vista de Modelo.

Crear las medidas DAX (Applications, Hired y Hiring Rate) y proceder con el diseño de los graficos interactivos.

