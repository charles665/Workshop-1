# Workshop 1 — Data Warehouse de Reclutamiento Tecnológico

## Objetivo

En este proyecto construí un ETL que convierte un archivo CSV de aplicaciones a empleos tecnológicos en un Data Warehouse dimensional en PostgreSQL. La finalidad es analizar contrataciones con SQL y Power BI, no consultar directamente el CSV.

## Contexto

La empresa recibe candidatos de diferentes países, tecnologías, niveles de seniority y años de experiencia. Cada aplicación tiene un Code Challenge y una Technical Interview. El sistema permite analizar resultados de contratación desde esas perspectivas.

## Requisitos de negocio

| ID | Requisito | Pregunta | Decisión |
|---|---|---|---|
| R1 | Tendencias de contratación | ¿Cómo cambian aplicaciones, contratados y tasa por mes? | Planear capacidad y detectar cambios. |
| R2 | Tecnologías | ¿Qué tecnologías generan más contratados y mejor tasa? | Priorizar reclutamiento técnico. |
| R3 | Perfiles | ¿Cómo varía la contratación por seniority y experiencia? | Entender perfiles con mejores resultados. |
| R4 | Países | ¿Qué países combinan actividad y buenos resultados? | Orientar búsqueda geográfica. |
| R5 | Evaluaciones | ¿Cómo se relacionan los dos puntajes con HIRED? | Revisar el proceso de evaluación técnica. |

## Trazabilidad

| Requisito | Datos | Dimensión | KPI | Visual |
|---|---|---|---|---|
| R1 | Fecha y HIRED | `Dim_Date` | Applications, Hired, Hiring Rate | Línea mensual |
| R2 | Tecnología y HIRED | `Dim_Technology` | Hired y Hiring Rate | Barras horizontales |
| R3 | Seniority, YOE y HIRED | `Dim_Candidate_Profile` | Applications, Hired, Hiring Rate | Columnas agrupadas |
| R4 | País y HIRED | `Dim_Country` | Applications, Hired, Hiring Rate | Top 15 países |
| R5 | Dos puntajes y HIRED | `Fact_Applications` | Tasa por segmento de evaluación | Barras por segmento |

## Datos y profiling

La fuente sin modificar es `data/raw/candidates.csv`. El notebook `notebooks/data_profiling.ipynb` contiene el profiling reproducible con Pandas.

| Validación | Resultado |
|---|---:|
| Filas / columnas | 50.000 / 10 |
| Nulos / duplicados exactos | 0 / 0 |
| Fechas | 2018-01-01 a 2022-07-04 |
| Países / tecnologías / seniority | 244 / 24 / 7 |
| Años de experiencia | 0 a 30 |
| Puntajes | 0 a 10 en ambas pruebas |
| HIRED | 6.698 aplicaciones (13,40 %) |

## Proceso y grain

El proceso de negocio es la evaluación de una aplicación de candidato en reclutamiento técnico.

> Una fila de `Fact_Applications` representa una aplicación válida del archivo fuente, evaluada en una fecha, país, tecnología y perfil profesional determinados.

Cada fila de hechos equivale a una aplicación antes de agrupar resultados.

## Modelo dimensional

El Star Schema está en [diagrams/star_schema.md](diagrams/star_schema.md).

| Tabla | Uso |
|---|---|
| `Dim_Date` | Fecha, año, trimestre y mes para R1. |
| `Dim_Technology` | Tecnología para R2. |
| `Dim_Candidate_Profile` | Seniority, experiencia y banda de experiencia para R3. |
| `Dim_Country` | País para R4. |
| `Fact_Applications` | Puntajes, HIRED, conteo de aplicaciones y llaves foráneas. |

Todas las dimensiones tienen surrogate keys generadas por el ETL. La fact table guarda esas claves como foreign keys; no utiliza nombres de países o tecnologías como llaves.

## ETL

1. `extract.py` lee el CSV sin reglas de negocio.
2. `transform.py` convierte tipos, limpia categorías, elimina duplicados exactos y valida los datos necesarios.
3. Se aplica la regla: HIRED es 1 cuando Code Challenge y Technical Interview son ambos mayores o iguales a 7; de lo contrario es 0.
4. `dimensional_model.py` crea dimensiones únicas, surrogate keys y la fact table.
5. `load.py` carga dimensiones primero y `Fact_Applications` después.

No se cargan nombres ni correos porque los cinco requisitos no necesitan información personal del candidato.

## Métricas de Power BI

Crear las medidas en `fact_applications`:

```DAX
Applications = SUM(fact_applications[application_count])
Hired = SUM(fact_applications[hired_flag])
Hiring Rate = DIVIDE([Hired], [Applications], 0)
```

- **Applications:** número de aplicaciones recibidas en el filtro actual.
- **Hired:** número de aplicaciones que aprobaron los dos puntajes mínimos.
- **Hiring Rate:** porcentaje contratado; es Hired dividido entre Applications. Formatear como porcentaje.

La guía exacta de columnas para cada visual está en [docs/power_bi_visuals.md](docs/power_bi_visuals.md).

## PostgreSQL y Power BI

Se usa PostgreSQL porque es gratuito, soporta PK, FK y restricciones, y se conecta con Python y Power BI. Para Power BI recomiendo Import: 50.000 filas es un volumen pequeño y este modo es simple para una sustentación.

1. Ejecutar el ETL y cargar PostgreSQL.
2. En Power BI: Obtener datos > Base de datos PostgreSQL.
3. Escribir el servidor, por ejemplo `localhost:5432`, y la base `recruitment_dw`.
4. Elegir Importar y cargar las cinco tablas del esquema `recruitment_dw`.
5. En Modelo, revisar relaciones de uno a muchos desde cada dimensión hacia `fact_applications`.
6. Crear medidas y visuales.

Guardar capturas del conector, Navigator, modelo, dashboard y actualización exitosa. Eso demuestra que Power BI usa el DW y no el CSV.

## SQL, diagramas y ejecución

- `sql/create_tables.sql`: tablas, PK, FK y restricciones.
- `sql/analytical_queries.sql`: una consulta para R1, R2, R3, R4 y R5.
- `sql/validation_queries.sql`: conteos, integridad referencial y regla HIRED.
- [Arquitectura](diagrams/architecture.md), [flujo](diagrams/program_flow.md) y [guía para dibujarlos](docs/diagram_instructions.md).

Para ejecutar: instalar dependencias, copiar `.env.example` como `.env`, probar con `python -m src.main --skip-load` y cargar con `python -m src.main`.

## Estado

| Área | Estado | Evidencia |
|---|---|---|
| Profiling, modelo, ETL y validación ETL | ✅ Cumple | Notebook, `src/` y pruebas de 50.000 hechos |
| SQL y esquema DW | ✅ Preparado | Carpeta `sql/` |
| Carga PostgreSQL y Power BI | ⚠️ Pendiente de ejecución local | Loader e instrucciones disponibles |

## Estructura

- `data/raw/`: fuente original.
- `notebooks/`: profiling inicial.
- `src/`: ETL.
- `sql/`: DW, consultas y validaciones.
- `diagrams/`: diagramas.
- `docs/`: guías de Power BI, diagramas y sustentación.
