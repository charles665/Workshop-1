# Defense guide

| Professor question | Short answer | Explanation |
|---|---|---|
| Why this business process? | It is the recruitment application evaluation process represented by each source row. | It directly contains the assessments and hiring outcome needed by the five requirements. |
| Why this grain? | One fact row is one candidate application. | It matches the dataset's atomic event and prevents ambiguous aggregation. |
| Why these dimensions? | Each gives context required by a business question: time, technology, profile, and geography. | No dimension was created merely because a source column existed. |
| Why a fact table? | It centralizes application-level measures linked to analytical context. | Scores, HIRED and the application count can be aggregated consistently. |
| Why surrogate keys? | They give dimensions independent, stable warehouse identifiers. | The fact stores integer FK values rather than source attributes, as required by the workshop. |
| Where is HIRED applied? | In `apply_business_rules`, before dimensional transformation and loading. | It is calculated only when both scores are at least seven. |
| Why ETL? | It validates and transforms operational data before analytical loading. | This makes the process reproducible and keeps the DW analytical. |
| Why PostgreSQL? | It is open source, supports PK/FK constraints, Python and Power BI. | It is sufficient and professional without adding unnecessary technologies. |
| Why Import in Power BI? | The dataset is small and academic refreshes are manual. | Import is simple, reliable and faster to demonstrate than DirectQuery. |
| How do you prove Power BI is not using CSV? | The Power BI source and model show the PostgreSQL `recruitment_dw` tables. | Connector, Navigator and Model-view screenshots provide evidence. |
| How is referential integrity guaranteed? | PostgreSQL FK constraints enforce it and validation SQL checks it. | Dimensions are loaded before the fact, and unmapped keys stop the ETL. |
| How are R1-R5 connected to the model? | The traceability table maps each requirement to data, dimensions, measures, SQL and visuals. | This ensures the model exists to answer business needs, not just to store data. |
| What decisions are supported? | Capacity, technology focus, profile criteria, country targeting and evaluation-process review. | Each decision corresponds to an analytical output, not a decorative chart. |
| ¿Por qué propuso R4? | R4 analiza países para saber dónde hay actividad de reclutamiento y buenos resultados. | No repite R1, R2 ni R3: agrega la perspectiva geográfica. La empresa puede decidir dónde concentrar búsqueda o campañas. |
| ¿Por qué propuso R5? | R5 analiza juntas las dos evaluaciones y su relación con HIRED. | Permite comprobar cómo Code Challenge y entrevista se conectan con la decisión de contratación y si una etapa limita resultados. |
| ¿Cómo explica Applications? | Es el número de aplicaciones en el filtro actual. | Cada fila de la fact representa una aplicación y `application_count` vale 1. |
| ¿Cómo explica Hired? | Es el número de aplicaciones que aprobaron ambos puntajes mínimos. | `hired_flag` vale 1 solo si los dos puntajes son mayores o iguales a 7. |
| ¿Cómo explica Hiring Rate? | Es el porcentaje de aplicaciones contratadas. | Se calcula como Hired dividido entre Applications y permite comparar grupos de tamaño diferente. |
