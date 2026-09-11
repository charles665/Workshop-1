# Power BI: qué arrastrar en cada gráfico

Primero verifica en Vista Modelo que las relaciones sean de uno a muchos desde las dimensiones hacia `fact_applications`.

## Columnas auxiliares

En `dim_date`, crea:

```DAX
year_month = FORMAT(dim_date[full_date], "YYYY-MM")
year_month_order = dim_date[year] * 100 + dim_date[month_number]
```

Selecciona `year_month` y usa Herramientas de columna > Ordenar por columna > `year_month_order`.

En `fact_applications`, crea:

```DAX
assessment_segment =
SWITCH(
    TRUE(),
    fact_applications[code_challenge_score] >= 7 && fact_applications[technical_interview_score] >= 7, "Ambos puntajes ≥ 7",
    fact_applications[code_challenge_score] >= 7 && fact_applications[technical_interview_score] < 7, "Código ≥ 7 / Entrevista < 7",
    fact_applications[code_challenge_score] < 7 && fact_applications[technical_interview_score] >= 7, "Código < 7 / Entrevista ≥ 7",
    "Ambos puntajes < 7"
)
```

## R1: tendencia

En gráfico de líneas: `dim_date[year_month]` al Eje X; `Applications` y `Hired` al Eje Y; `Hiring Rate` a Tooltips. Explicación: comparo el volumen mensual de aplicaciones y contratados.

## R2: tecnologías

En barras horizontales: `dim_technology[technology]` al Eje Y; `Hired` al Eje X; `Applications` y `Hiring Rate` a Tooltips. Ordenar por Hired descendente. Explicación: identifica tecnologías con mayor aporte de contrataciones.

## R3: perfiles

En columnas agrupadas: `dim_candidate_profile[seniority]` al Eje X; `Applications` y `Hired` al Eje Y; `experience_band` como Leyenda o segmentador; `Hiring Rate` a Tooltips. Explicación: compara resultados entre niveles profesionales y experiencia.

## R4: países

En barras horizontales: `dim_country[country]` al Eje Y; `Hired` al Eje X; `Applications` y `Hiring Rate` a Tooltips. En filtros del visual, usar Top N = 15 por Hired. Explicación: un Top 15 es legible incluso si existen 244 países.

## R5: evaluaciones

En barras agrupadas: `fact_applications[assessment_segment]` al Eje Y; `Applications` y `Hired` al Eje X; `Hiring Rate` a Tooltips. Explicación: la regla de contratación requiere los dos puntajes, por eso se analizan juntos.
