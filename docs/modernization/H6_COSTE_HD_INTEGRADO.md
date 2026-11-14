# C01 aceptado y coste del motor con SDL

01-11-2026 · plan 2.69.

## Aceptación visual

Miguel: «he abierto c01_12.html y me parece bien el detalle, posición e integración». Se acepta esa comparación de C01 generada con el motor 3ee12e9. No volver a pedirla, ni repetir A/B/C o guardado/persistencia. El HTML representa el mismo instante clásico/HD y su ampliación; no acredita todos los frames/animaciones ni el escalado final de la GPU. La densidad definitiva sigue abierta hasta medir el coste pertinente.

## Método de medición

`tools/modernization/measure_hd_replay_cost.py` ejecuta el motor completo en cuatro modos: clásico, publicación con captura semántica, HD 8× y HD 12×. Usa las tres fases públicas de Amiga The One, con publicación HD real en ambos modos HD, sin forzar misión/fase. Cada ejecución debe terminar las tres fases y conservar los 3.405 estados H3 originales. Las referencias no se regeneran.

Un calentamiento excluido por modo y tres rondas medidas, con orden rotatorio y procesos nuevos. Mismo ejecutable, datos, ventana/FIT, ratón, SDL software y trazas en los cuatro modos. Exportación de imágenes, diagnóstico repetitivo, pausa y planificación artificial desactivados; se eliminan overrides OPENFODDER heredados. Se comprueban marcadores efectivos: pedir HD sin publicar C01 no cuenta como una muestra válida. La publicación base incluye captura semántica para que su comparación con HD mida la ruta adicional.

Métricas: tiempo de pared desde arranque hasta salida del proceso, CPU usuario+sistema y máximo RSS del hijo. Un supervisor Python nuevo por muestra evita acumular el máximo de hijos anteriores. Incluyen arranque, trazas y cierre; excluyen la comprobación H3 posterior. No son latencia por frame, p95/p99, FPS, coste unitario de cada parche, uso VRAM ni tiempo GPU. El marcador HD confirma al menos una publicación, no su frecuencia. No se establece un umbral de rendimiento con tres muestras.

Compilación local optimizada GCC C++14 `-O3 -DNDEBUG`, SDL 3.4.0 estático, `OPENFODDER_NO_MIXER`. Código del motor idéntico al validado en 3ee12e9; HEAD documental de partida a66b4fa. La compilación terminó antes del ensayo. Se conserva [procedencia de compilación, fuentes y dependencias](evidence/hd-integrated-build-2026-11-01.json). No se cambia el motor ni se entrega otro ejecutable Windows por esta medición.

```bash
python tools/modernization/measure_hd_replay_cost.py \
  --exe /ruta/al/openfodder --data Run --out /tmp/hd-cost-nuevo \
  --build-description 'Describir compilador, flags, SDL y audio del ejecutable'
```

Ejecutar sobre una copia de los datos públicos fijados, en Linux, con directorio de salida nuevo. Conserva logs, trazas, hashes e informes aunque una muestra sea rechazada. La medición no se añade a CI como umbral dependiente del host; sus controles de validez tienen pruebas unitarias.

## Intento local rechazado

La primera ejecución en el directorio de trabajo se detuvo en publicación, segunda ronda medida: m1p1 contiene 137 estados frente a 149 esperados. Las 138 líneas, incluida la cabecera, son el prefijo exacto de la muestra válida de la misma configuración; m1p2 y m1p3 coinciden byte a byte. El juego informó de tres fases completas, pero H3 rechazó el ensayo. No se usan sus tiempos como resultado aceptado.

[Informe del rechazo](evidence/hd-integrated-rejected-2026-11-01.json). Es una observación similar a [H5.1](H5_1_MEDICION_INICIAL.md), compatible con la ruta local de escritura, sin causa demostrada. Se programa un único ensayo completo independiente en tmpfs `/dev/shm`, con el mismo binario/opciones/referencias, sin mezclar muestras ni reintentar silenciosamente hasta obtener verde. La política ante un nuevo fallo es detener e investigar.

## Resultados y siguiente paso

Ensayo completo en tmpfs PASS: 16 recorridos × 3 fases = 48 fases, 3.405 estados H3 originales por recorrido; cuatro calentamientos excluidos y doce muestras medidas. Todas las rutas solicitadas se observaron. H3 y el ejecutable conservan sus hashes. El éxito en tmpfs no demuestra la causa de la incidencia anterior ni corrige el escritor de trazas del motor.

| Modo | Pared mediana (mín.–máx.), s | CPU mediana, s | RSS máximo del proceso, mediana MiB |
|---|---:|---:|---:|
| Clásico | 19.924 (19.828–19.970) | 21.278 | 17.18 |
| Publicación + captura | 49.621 (49.502–50.316) | 54.430 | 22.82 |
| HD 8× | 76.816 (76.802–77.256) | 81.929 | 23.68 |
| HD 12× | 76.551 (76.345–77.051) | 81.563 | 23.61 |

Tres muestras por fila. 12× difiere de 8× alrededor de −0,34 % en tiempo de pared; los rangos se solapan y no se interpreta como ventaja de 12×. El aumento de publicación a HD ronda el 55 % en esta campaña; el experimento no atribuye ese coste a una función ni cuenta cuántos frames publican C01. La memoria es RSS del proceso y no memoria del parche o de GPU. No extrapolar a todas las poses, atlas grandes o 60/120/144 Hz.

Decisión: conservar 8× y 12×, manteniendo 12× como candidata coherente con la preferencia visual de Miguel. No reducir calidad por una diferencia no demostrada. Siguiente incremento técnico: instrumentar tiempos y contadores por bloque (captura/contraste, composición, elegibilidad/retorno y operaciones SDL) para localizar trabajo repetido antes de optimizar. Preservar el contraste obligatorio, orden, anclaje, oclusiones y retorno clásico. Después comprobar coste de frame y GPU en Windows; no prometer FPS con estos tiempos de campaña.

No se modifica el motor ni el ZIP 3ee12e9. H5.1 sigue parcial: ahora hay tiempo/CPU/RSS del proceso integrado, faltan percentiles por frame, atribución de coste, GPU y una carga representativa de más arte.

Evidencia: [resultado completo](evidence/hd-integrated-cost-2026-11-01.json), [archivo de logs y trazas](evidence/hd-integrated-traces-2026-11-01.json.gz), [rechazo anterior](evidence/hd-integrated-rejected-2026-11-01.json), [sus trazas](evidence/hd-integrated-rejected-2026-11-01.json.gz) y [manifiesto de integridad](evidence/hd-integrated-archive-2026-11-01.json). El formato compartido almacena cabecera, cuerpo y SHA-256 para reconstruir cada archivo exactamente; `archive_replay_evidence.py` comprueba la reconstrucción byte a byte. Se conserva el contenido completo, sin descartar estados repetidos entre muestras. Tres tests de puertas de medición PASS (incluidos dos nuevos); rechazan rutas inactivas, exportación/sondas contaminantes, fases incompletas y errores. El cambio añade herramientas/evidencia, sin repetir CI del motor inalterado.

