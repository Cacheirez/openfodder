# Documentación: fuentes vigentes y limpieza

Limpieza del 02-11-2026 solicitada por Miguel. Se eliminan las listas de ejecución duplicadas y los estados viejos presentados como vigentes. No se borran código, maestros, tests, referencias H3 ni evidencia técnica útil.

## Fuentes únicas

| Información | Documento |
|---|---|
| Estado, aceptación y último código probado | [CONTINUIDAD.md](CONTINUIDAD.md) |
| Orden del trabajo | [PLAN_TRABAJO.md](PLAN_TRABAJO.md) |
| Requisitos finales H0–H10 | [ALCANCE_H0_H10.md](ALCANCE_H0_H10.md) |
| Soldados: catálogo y corrección pendiente | [SOLDADOS_COBERTURA_COMPLETA.md](SOLDADOS_COBERTURA_COMPLETA.md) |
| Compilación y reproducción | [DESARROLLO.md](DESARROLLO.md) y workflows |
| Relevo | [PROMPT_NUEVO_HILO.md](PROMPT_NUEVO_HILO.md) |

## Eliminado de la rama activa

- PLAN_MODERNIZACION_ES.md: plan inicial sustituido.
- PLAN_TRABAJO_HISTORICO_HASTA_2_19.md y PLAN_TRABAJO_HISTORICO_2_28_A_2_69.md: bitácoras convertidas en planes paralelos.
- RELEVO_2026-10-29.md y AUDITORIA_CONTINUIDAD_2026-10-28.md: relevos e índices reemplazados.
- H2_H3_AVANCE.md: lista de estado H2/H3 superada por la aceptación H2.6 y los contratos vigentes.
- RESULTADOS.md: resumen de auditoría inicial redundante con evidencias fechadas y código.

Se recuperan en el historial Git anterior a esta limpieza (por ejemplo, commit df933bf69ea50544fe4e9158dc7a8d7cc27db710); no se duplican otra vez en una carpeta de archivo. Las referencias históricas necesarias apuntan a esa revisión fija.

README, CONTINUIDAD, PLAN y PROMPT se reescriben para retirar órdenes caducadas como preparar m1p1, medir coste ya medido, volver a elegir estilo, validar guardado ya aceptado o tratar 3ee12e9 como último ejecutable. Las recetas reutilizables pasan a DESARROLLO y los requisitos finales a ALCANCE_H0_H10.

## Conservado porque aporta

Los contratos de presentación, resolución/ratón, pruebas H2/H3, censos CD32, incidencias técnicas y validaciones fechadas siguen disponibles para entender el código o una regresión. Describen la revisión que los originó; sus «siguientes pasos» históricos no prevalecen sobre el plan actual. No leerlos todos para continuar.

LOTE_SOLDADO_PILOTO conserva cómo se produjo y probó f72d6e7; ahora advierte expresamente de la mezcla observada y de su alcance insuficiente. Los informes PASS no se reescriben como FAIL: las pruebas pasaron, pero no medían continuidad/cobertura completa. La puerta siguiente debe medirlas.

Regla de mantenimiento: una sola actualización del estado, un plan y una evidencia por entrega. Añadir un documento solo si aporta un contrato o resultado no existente; evitar cadenas de resúmenes, versiones del mismo plan y nuevas instrucciones de relevo divergentes.
