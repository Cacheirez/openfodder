# H6 — coste del piloto HD aislado

30-10-2026 · plan 2.61. Medición completada; no integración SDL ni densidad definitiva.

## Resultado y decisión técnica

No integrar sin cambios el escalado completo por CPU del piloto. En este host, 12× consume por sí solo más de los 16,67 ms del objetivo de un frame a 60 Hz; 8× tampoco demuestra margen suficiente para un frame completo en todos los escenarios. Esto **no descarta texturas 12×**: el cuello de botella observado pertenece a la ruta de composición de superficie completa, no a una evaluación de GPU o atlas.

Mantener 12× como candidato de calidad y 8× parametrizado. Preparar una ruta que conserve la referencia clásica y las mismas puertas de elegibilidad, pero evite reconstruir/ampliar por CPU todo el canvas para una sola pose: destino físico y texturas/caché en SDL a evaluar. No superponer el soldado al final sin respetar orden, oclusión y destino. La ruta existente sigue aislada y clásica por defecto. No se ha implementado esta optimización.

## Método reproducible

```bash
python tools/modernization/measure_soldier_art_hd.py --out /tmp/hd-cost-new
```

GCC -O3 -DNDEBUG, C++14; Linux compartido, AMD EPYC 9V74, cuota cgroup 8 CPU, límite 8 GiB. Tres rondas, 200 muestras y 20 calentamientos por caso: 108 procesos y 21.600 composiciones medidas. Cada modo/caso/ronda usa proceso nuevo, orden rotatorio. Se miden composición, reservas y destrucción de salida; se excluyen PNG, preparación de recursos/escena y hash completo. El hash se comprueba antes/después y entre rondas; fallback debe igualar el clásico. PASS significa que terminó y conservó esas invariantes, no aprobación de rendimiento.

Plataformas: geometrías PC 320×200 y Amiga 320×225 de las fixtures; 352×272 es un control mayor. Cada una tiene escena simple de una pose y escena sintética de 65 capas/dos destinos (64 capas previas, 1.024 escrituras cada una). No es carga real de una misión ni múltiples actores HD. Modos: clásico (0), C01 nativo (1), HD 8/12, fallback por oclusión (108/112). El destino medido es uno; no se suman dos salidas HD.

Tabla: escena sintética con más comandos, 600 muestras por fila. Tiempos de pared en ms; RSS máximo del proceso completo, no memoria exacta del compositor.

| Geometría | Modo | Mediana ms | p95 ms | p99 ms | Salida MiB | RSS máximo MiB |
|---|---|---:|---:|---:|---:|---:|
| PC 320×200 | Clásico | 0.225 | 0.345 | 0.467 | 0.24 | 14.70 |
| PC 320×200 | C01 nativo | 0.787 | 1.056 | 1.718 | 0.24 | 14.82 |
| PC 320×200 | 8× | 10.026 | 12.799 | 16.169 | 15.62 | 21.49 |
| PC 320×200 | 12× | 34.611 | 44.635 | 48.039 | 35.16 | 41.14 |
| Amiga 320×225 | Clásico | 0.264 | 0.478 | 0.755 | 0.27 | 14.95 |
| Amiga 320×225 | C01 nativo | 0.885 | 1.228 | 1.593 | 0.27 | 14.95 |
| Amiga 320×225 | 8× | 11.126 | 15.415 | 18.440 | 17.58 | 23.67 |
| Amiga 320×225 | 12× | 39.398 | 48.194 | 57.547 | 39.55 | 45.75 |
| Control 352×272 | Clásico | 0.400 | 0.815 | 2.045 | 0.37 | 15.07 |
| Control 352×272 | C01 nativo | 1.193 | 2.071 | 3.387 | 0.37 | 15.07 |
| Control 352×272 | 8× | 16.023 | 22.822 | 28.537 | 23.38 | 30.20 |
| Control 352×272 | 12× | 54.052 | 67.129 | 81.580 | 52.59 | 59.52 |

Las escenas simples y todos los fallback están en el JSON. Los p95/p99 son descriptivos del ensayo compartido; no tiempos de frame ni FPS. Una regresión local ASan/UBSan y operaciones Git coincidieron con parte del ensayo: no es una medición con núcleos aislados. No se ha medido Windows del usuario, SDL upload, VRAM, GPU, sincronización, interfaz completa, animaciones o latencia de entrada.

## Memoria y transferencia: estimación explícita

| Elemento | 8× | 12× |
|---|---:|---:|
| Una pose 16×14 RGBA | 56 KiB | 126 KiB |
| 100 poses, solo píxeles | 5,47 MiB | 12,30 MiB |
| Salida Amiga 320×225 RGBA | 17,58 MiB | 39,55 MiB |
| Dos salidas Amiga retenidas | 35,16 MiB | 79,10 MiB |
| Subida completa Amiga a 60/s, estimación | 1,03 GiB/s | 2,32 GiB/s |

12× usa 2,25 veces los texels de 8×. Las transferencias son aritmética bytes×60; **no ancho de banda medido ni coste de GPU**. Las 100 poses son un ejemplo, no inventario final. Faltan padding de atlas, mipmaps, copias CPU/GPU y demás recursos. El presupuesto existente de 64 MiB es por salida; no limita el proceso ni VRAM. La salida 12× de control ocupa 52,59 MiB y cabe en ese presupuesto, pero no pasa por ello un criterio de rendimiento.

## Evidencia y continuidad

- [Resumen completo, entorno, hashes y percentiles](evidence/hd-cost-2026-10-30.json).
- [Todas las muestras originales comprimidas](evidence/hd-cost-2026-10-30-raw.json.gz), sin eliminar rondas.
- Herramientas: `tools/modernization/measure_soldier_art_hd.py` y `benchmark_soldier_art_hd.cpp`.
- El ensayo comenzó con HEAD d2e05e8 y el include corregido ya en el árbol local. Los hashes registran exactamente las fuentes medidas; compositor idéntico al de 3d82ff2. No se han modificado originales ni H3.
- Regresión local tras el include: `check_soldier_art_hd.py`, PASS 132 guards y contratos PC/Amiga, ASan/UBSan con LSan local desactivado explícitamente. No sustituye CI Windows.

CI y paquete 3d82ff2 cerrados PASS: [evidencia](VALIDACION_3d82ff2.md). Siguiente: validar Save con Miguel y preparar una composición HD eficiente y opcional antes de elegir densidad. La validación manual de Save no bloquea tareas técnicas independientes. Mantener PR abierto/borrador/sin fusionar.
