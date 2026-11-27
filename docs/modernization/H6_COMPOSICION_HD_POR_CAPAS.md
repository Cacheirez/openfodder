# H6 — composición eficiente de fondo nativo y parche HD

30-10-2026 · plan 2.62. Implementación aislada en `Source/Utils/SoldierArtHDLayers.hpp`. No conectada a SDL ni activada en el juego. Mantiene 8×/12×; 1× solo oráculo. El compositor completo anterior permanece como referencia independiente para la salida.

## Contrato y orden

`ComposeSoldierArtHDLayers` recibe la misma captura propia, destino, estabilidad de paleta y recurso que el piloto anterior. Devuelve fondo RGB nativo propio y, solo en éxito, un parche de 16d×14d píxeles, anclaje lógico, densidad y escena. El parche ya contiene el fondo y la mezcla alfa calculada: **se copia con reemplazo, no se mezcla de nuevo**. El fondo no incluye el cuerpo clásico retirado. La pareja es una unidad indivisible de una captura; no combinar fondo de un frame con parche de otro ni reutilizarla tras cambiar destino/escena. No existe caché ni una nueva política temporal en este incremento.

Se reutiliza `ComposeSoldierArt` con cuerpo transparente para recuperar el fondo real y las mismas puertas de elegibilidad. La política sigue siendo conservadora: un comando posterior que toque el cuerpo, incluso escritura del mismo color o OR cero, provoca retorno clásico. Save/Restore/Clear posteriores y destinos/recortes/pitch no soportados mantienen la protección previa. No hay oclusión parcial HD nueva. Un comando en otro destino no tapa esta pose. El anclaje procede del comando capturado; no recalcula entidades, cámara, visibilidad ni RNG.

La salida separada es equivalente a ampliar el fondo nativo por vecino más cercano y copiar el parche en `(logicalX*d,logicalY*d)`. Esa expansión se ejecuta **solo en la prueba de equivalencia**, no en el productor nuevo. El consumidor SDL futuro deberá mantener las mismas transformaciones y filtros en ambas partes, sin costuras ni doble mezcla. La igualdad demostrada se refiere al raster entero de densidad d; no promete igualdad con filtrado lineal o escalas físicas fraccionarias. Necesitará pruebas específicas de resize/DPI, generaciones, errores de textura y retorno clásico antes de integrarse.

## Memoria

La ruta anterior materializa todo el canvas a densidad d. Esta conserva únicamente el fondo nativo y el rectángulo HD. En Amiga 320×225:

| Salida retenida | 8× | 12× |
|---|---:|---:|
| Compositor completo anterior | 18.432.000 bytes | 41.472.000 bytes |
| Fondo nativo + parche nuevo | 345.344 bytes | 417.024 bytes |

Son bytes de píxeles de salida; excluyen recursos, escena, referencias temporales, capacidad del asignador y GPU. El límite `maxPatchBytes` del nuevo API es **solo del parche** (129.024 bytes por defecto), distinto del presupuesto de salida completa del API anterior. Rechazo devuelve fondo clásico nativo exacto, parche vacío y densidad 1. No se amplía un frame completo ni se reservan texturas GPU. Persisten rasterizaciones nativas de referencia y copias para mantener el contraste existente; no se declara coste nulo.

## Pruebas

`python tools/modernization/check_soldier_art_hd.py`: ASan/UBSan local, LSan desactivado explícitamente como en el ensayo anterior. La fixture existente, también en CTest Windows/Linux, compara cada píxel de la reconstrucción por capas contra el compositor completo. Cubre PC/Amiga, densidades 1/8/12, desplazamiento, transparencia 0/128/255, comandos tempranos/tardíos, 132 casos de guard, destinos independientes, pitch, recursos inválidos, presupuesto del parche, repeticiones 0/1/5 y control 352×272 a 12×. No equivale a replays nuevos del motor integrado. Las fuentes de simulación, H3 y PNG originales no cambian.

## Medición

Herramienta `measure_soldier_art_hd_layers.py`: compara modos 8/12 completos y 208/212 por capas, misma escena Amiga con 65 comandos/dos destinos, 200 muestras, 20 calentamientos y tres rondas de orden rotatorio. La medición incluye construir/destruir salida; excluye expansión del oráculo, PNG, preparación y hash completo. Los hashes dentro de cada modo comprueban estabilidad; los formatos distintos no comparten hash. Equivalencia píxel a píxel se verifica aparte. No mide SDL, GPU ni el Windows de Miguel. [Resultados completos y muestras](evidence/hd-layers-cost-2026-10-30.json), 12 procesos/2.400 composiciones medidas. Host Linux compartido; no umbral de aceptación ni extrapolación GPU.

## Aceptación de opciones y siguiente paso

Miguel confirma el 30-10: «ahora ya funcionan las opciones, graba y mantiene los valores». Se acepta guardado/persistencia observados; no atribuir una prueba separada de REVERT, caducidad o todos los fallos de recuperación si no se ha comunicado. H5.6 global sigue parcial por opciones de monitor/modos/FPS/interfaz pendientes.

Siguiente: consumidor SDL opcional para esta pareja de superficies, con contraste clásico, identidad temporal, filtros/transformación común y recuperación ante errores. Todavía sin fijar densidad ni producir animaciones masivas; cursor y terrenos pendientes. PR abierto, borrador y sin fusionar.

### Resultado local

| Ruta | Mediana ms | p95 ms | p99 ms | Salida bytes | RSS máximo KiB |
|---|---:|---:|---:|---:|---:|
| Completa 8× | 11.887 | 17.803 | 21.070 | 18432000 | 24236 |
| Completa 12× | 41.271 | 52.763 | 68.027 | 41472000 | 46840 |
| Capas 8× | 1.210 | 1.827 | 2.881 | 345344 | 15028 |
| Capas 12× | 1.397 | 2.014 | 3.923 | 417024 | 15028 |

La mejora corresponde al productor CPU aislado y a sus píxeles retenidos. Falta coste de publicación SDL, escalado físico y GPU; no equivale al tiempo total de frame. Fuentes exactas identificadas por SHA-256 dentro del informe.
