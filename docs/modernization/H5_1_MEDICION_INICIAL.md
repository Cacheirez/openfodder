# H5.1 — Medición inicial y decisión de alcance

26-10-2026. Inicio de H5.1, no cierre del hito. Motor de la sonda `9aaaf448`; no se cambia jugabilidad ni se activa publicación por defecto.

## Método

`tools/modernization/measure_presentation_cost.py` compara clásico sin registro, registro/contraste con publicación clásica y publicación desde órdenes con contraste. Usa el mismo ejecutable, fixtures, dos fases públicas, vídeo SDL software, audio desactivado y una presentación. Desactiva explícitamente la sonda de pausa y elimina la programación heredada. Comprueba marcadores reales, ausencia de sanitizadores y H3 original en cada pareja PC/Amiga.

Una ronda de calentamiento excluida y tres rondas medidas; el orden de los modos rota. Total: 12 parejas / 24 fases, todas PASS con 301 estados originales por pareja. Se mide tiempo de pared del proceso completo, incluidos arranque, trazas y cierre. No es coste de rasterización aislado, latencia por frame, FPS, CPU, memoria ni GPU. Host compartido y muestra pequeña: no se establecen umbrales de aceptación ni presupuestos a partir de estas cifras.

## Resultado observado

| Modo | PC m1p1, mediana (rango), s | Amiga m1p1, mediana (rango), s |
|---|---:|---:|
| Clásico | 0,768 (0,767–0,820) | 1,018 (1,018–1,070) |
| Registro y contraste | 2,323 (2,275–2,325) | 3,329 (3,277–3,333) |
| Publicación y contraste | 2,173 (2,125–2,174) | 3,279 (3,174–3,336) |

Tres muestras medidas por celda. [Resultados completos y hashes](evidence/cost-pilot-2026-10-26.json). Hay sobrecoste del conjunto registro/contraste en este ensayo. No se atribuye cada diferencia a un componente ni se concluye que publicación sea más rápida que auditoría con esta muestra.

## Incidencia de observabilidad delimitada

Dos intentos con trazas en el directorio de trabajo fueron rechazados: un JSONL PC quedó truncado (136 y 143 estados completos respectivamente), aunque el replay informó de finalización. Sus prefijos completos coinciden con el control clásico. La sonda de pausa estaba desactivada. Esto amplía el problema de registros observado anteriormente; no demuestra que tenga exactamente la misma causa.

La ejecución completa con salida en `/dev/shm` (tmpfs) pasó. Es evidencia compatible con un problema de la ruta local de escritura, no una causa demostrada ni una corrección del motor. Se conservan los [intentos rechazados](evidence/cost-local-rejected-2026-10-26.json); no se incluyen en las medianas. Si vuelve a aparecer una salida incompleta, el gate debe seguir fallando, sin rebaselinar ni reintentar silenciosamente hasta obtener verde.

## Reproducción

```bash
python3 tools/modernization/measure_presentation_cost.py \
  --exe build/openfodder --data Run --out /dev/shm/openfodder-cost-NUEVO
```

Usar un directorio nuevo con espacio suficiente. Los logs, trazas y selección de hashes se conservan por muestra. El script es una herramienta de medición manual; no añade una puerta de rendimiento dependiente del ruido de CI. Las pruebas Python verifican rechazo de modos inactivos, opciones heredadas y avisos de sanitizadores.

## Siguiente entrega

Captura semántica mínima de cámara y un sprite (H4.2/H4.4): identidad/generación, posición, recurso/anclaje, tick y escena; reproducir primero el original. Preparar los conceptos H6.1 usando el [brief del piloto](H6_PILOTO_VISUAL.md). No ampliar masivamente arte ni optimizar a ciegas: añadir instrumentación por frame y medir CPU/memoria antes de decidir cómo reducir el coste del contraste. La selección de estilo y las pruebas semánticas pueden avanzar sin esperar a todas las escenas ni a resolver la escritura local del entorno.
