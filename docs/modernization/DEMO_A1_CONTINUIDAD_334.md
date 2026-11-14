# A.1 — Punto de control con 334 vínculos

## Publicaciones efectivas en el replay público

Amiga The One, misión 1, fase 2, replay público intacto. Mismo motor diagnóstico Windows x64 para las dos pasadas, con SDL 3.4.0 software/dummy, 12×, sin audio y sin instrumentar `WindowHD.cpp`. Cambia únicamente el manifiesto. Cada pasada devuelve los mismos 1.546 estados de H3 para esta fase, con SHA-256 lógico `5996aea99df370416989b49ed5ca4b6129f6b0ff380f8398490a4de95c3f5259`.

| Medida | 333 vínculos | 334 vínculos |
|---|---:|---:|
| Intentos registrados | 4.554 | 4.554 |
| Publicaciones HD efectivas | 1.786 (39,22 %) | 1.806 (39,66 %) |
| Retornos por faltantes | 2.684 | 2.660 |
| Intentos interrumpidos | 84 | 88 |
| Racha máxima de publicaciones | 685 | 685 |

La racha máxima abarca los intentos 2267–3635 en ambos casos. Se corta ante cualquier resultado distinto de `published` o salto del paso serial de dos establecido para este tramo. Se expresan rachas en publicaciones del replay acelerado. Las puertas previas al registro de intentos limitan la cobertura de esta medida.

De los 24 intentos que dejan de tener faltantes, 20 publican en HD y cuatro se interrumpen (7039, 7041, 7044 y 7052). Ambos logs registran `ordered-resource-bounds`; el aviso aparece una vez por proceso y no identifica por sí solo la causa exacta de cada interrupción. Ninguna publicación previa se pierde. Los 2.580 comandos de la bala pasan de `missing` a `keep`. Con una mejora de 0,44 puntos porcentuales y la misma racha máxima, el siguiente paso es contrastar la continuidad jugando a velocidad normal antes de añadir más claves.

## Prueba manual del 14 de noviembre

Miguel observó que el juego seguía volviendo con frecuencia al soldado clásico. La continuidad jugando queda **NO ACEPTADA**. El punto de control usó el candidato de 334 vínculos, Amiga The One m1p2 a 12×, reloj normal y sin replay. La sesión duró 262,66 s desde el lanzamiento y terminó con código 0.

El censo de transacciones coincide con el registro del lanzador y sus marcas de tiempo. Hubo **4.664 publicaciones HD de 10.987 intentos (42,45 %)**, 6.263 retornos por faltantes y 60 interrupciones. Entre intentos consecutivos registrados hubo 32 transiciones de HD a faltante y 15 de HD a interrupción. La mayor racha tuvo 878 publicaciones, **18,074 s** entre marcas del log (intentos 366–2120, paso serial de dos). El primer retorno registrado, intento 2122 a los 21,392 s desde lanzamiento, fue una interrupción con los siete comandos censados y cero faltantes. A continuación aparece `ordered-resource-bounds`.

La bala se resolvió como dibujo asociado en sus 6.673 comandos. Quedaron 248 claves distintas entre los rechazos por faltantes. En 5.312 rechazos coexistían varias; en 951 había una sola. La clave con más casos como único faltante, `75d5c70c` (tipo 27, hoja 0x9E/F0), cubriría como máximo 140 intentos por sí sola en este registro (1,27 puntos porcentuales). Se prioriza aislar el retorno por límites que cortó la primera racha.

La sesión local es `manual-334-20261114-105752`, bajo `$work`. Se puede recotejar el censo con `python -B tools/modernization/ordered_soldier_coverage.py --log "$session/engine.log" --out <salida-nueva.json>`, donde `$session` señala esa carpeta. Las rachas se calculan sobre los registros `SOLDIER_ORDERED_RESULT` de `presentation-times.jsonl` y se cortan al primer resultado distinto de `published`.

| Registro manual | SHA-256 |
|---|---|
| `engine.log` | `802e3e850423dcf5dfdb6f2f772a081c00e1334c80ab3ee72904492b32860dc0` |
| `presentation-times.jsonl` | `946fd2a468da94b16af033959f68f9324c9c0eaf7e7704eda9a1fa881d6d62a5` |
| `session.json` | `a92b894a13c0ddd584abd92e077efba6deab254e356fd458684f422e7882d88b` |
| `coverage.json` | `f10837ac7f9fa437ed347da8ee55f0d8bdf9e485394fd66981a14ea7e320691a` |

### Lanzamiento de la prueba

Abrir PowerShell y ejecutar:

```powershell
$work = 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1d961-42c0-7db0-bad9-4e57f50d84bc'
$out = Join-Path $work ('manual-334-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
python -B "$work/run_manual_334.py" --source "$work/manual-334-source" --out $out
```

El lanzador local reutiliza el del candidato de 331 vínculos con hashes actualizados. Antes de la sesión, `--prepare-only` verificó los archivos y el comando a cadencia normal.

## Reproducción técnica

### Diagnóstico del primer retorno

Una copia local de `WindowHD.cpp` registra el mensaje de la excepción y los datos del último comando resuelto antes de volver a lanzar la misma excepción. Con el replay público a 12× y 334 vínculos conserva el censo anterior. Las 88 interrupciones nacen de `ordered art clipped geometry` en el enemigo tipo 5, hoja `0x59/F0`: tres por el borde izquierdo y 85 por el derecho. El primer caso tiene `x=-1`, `y=91`, 16 × 14 píxeles y respaldo de 352 píxeles de ancho. El primer caso por la derecha tiene `x=342`, `y=225`, 16 × 14. El compositor HD exige que todo el rectángulo quepa en cada fila; el raster clásico direcciona el destino por desplazamientos lineales y admite estas geometrías cuando las escrituras caben dentro del respaldo.

El intento manual 2122 registra esa misma variante de enemigo como último comando, cero faltantes y el mismo aviso general. El log manual carece de coordenadas, por lo que la geometría exacta se acredita en el replay público. El caso mínimo reutiliza una superficie de 96 × 64 y un cuerpo Amiga8 de 16 × 14, probado en `(-1, 20)` y `(86, 20)`; las huellas lineales caben en el respaldo en ambos casos.

En el directorio `$work`, con el proyecto diagnóstico preparado, ejecutar `python -B "$work/diagnose_ordered_bounds.py"` y `python -B "$work/run_ordered_bounds.py"` una vez desde la raíz del checkout. El log resultante se conserva en `replay-bounds/engine.log` (SHA-256 `8d3e52978c8dd08acaf946013bd2117160d3f1fa95c076e6b3c6b4ca885ce707`).

### Replay comparativo original

Desde el checkout del commit de integración `b496e6b` ejecutar `& "$work/build_bullet_replay.ps1"` y `python -B "$work/measure_bullet_replay.py"`, con los candidatos de la [integración](DEMO_A1_AUDITORIA_BALA_7F_F0.md#integración-y-prueba-sdl). Para una repetición, copiar los dos scripts y las carpetas de ambos candidatos a un directorio nuevo. Los logs conservados permiten repetir el análisis sin ejecutar de nuevo el replay. La compilación inicial del proyecto diagnóstico rechazó una ruta con separadores de Windows. Tras normalizarla completó la compilación. La primera medición registró la pasada de 333 válida; se conservó y se corrigió el análisis para contabilizar las interrupciones antes de ejecutar la de 334.

| Evidencia | SHA-256 |
|---|---|
| Replay público `m1p2.ofd` | `b9d3ea3ec77d88f0bfabb647bd06f2d25c52968d55e86d0c21ae1bedae1f0116` |
| Ejecutable diagnóstico | `27884f96c05b319853b6bbdfce6fa121b6c2b1888501286bb7a8fd6c42b1b062` |
| `replay-333/engine.log` | `678786101e7670334a0b7831fafb9ccb4d698f59949ebd32524821e95c5c88de` |
| `replay-334/engine.log` | `e07bc1e7f628a24395ee1c3074711013f512e97fb1de6a9bf540f7a9fa3b78ce` |
| `bullet-replay-summary.json` | `4dacb30cab9a400bd2ad3f13fbc0a9fc81df55fcbd996937f86063f90aeab7ba` |
| `build_bullet_replay.ps1` | `28e0a9795f2405f12a992d3a5ca9049ffade52dfac52238f54b635fb4e642578` |
| `measure_bullet_replay.py` | `42d5a83b26f0508741298d3c824bf214b530116c83ed903268ae33a06104d0a5` |
| `run_manual_334.py` | `272875710c0cb07e2b8a1b731b1c7ccb0739a110f0efe3d883f19317fb9cd008` |

## Corrección del compositor

Los cuerpos Amiga8 usan el mismo direccionamiento lineal que el clásico cuando un recorte por palabras deja píxeles al otro lado de un borde de fila. El compositor conserva el desplazamiento de origen y comprueba que el intervalo escrito cabe en el respaldo. La referencia semántica también rechaza el intervalo inválido antes de acceder al búfer. La selección de poses y el raster original permanecen en sus rutas existentes.

- Windows x64, Clang 23.1.5 con ASan/UBSan PASS. Compositor: 156 escenarios, incluidos los dos bordes Amiga8, recorte superior combinado y rechazo fuera del respaldo en ambos extremos. Regresiones SDL software a 8×/12× PASS. LSan local, GPU y CD32 PENDIENTES.
- Replay público a 12× y 334 vínculos: **1.894 de 4.554 publicaciones efectivas (41,59 %)**, 2.660 faltantes y cero interrupciones. Los 88 intentos interrumpidos antes son los únicos cambios y todos publican. Racha máxima **859** (intentos 2267–3983) frente a 685. Los 1.546 estados lógicos siguen coincidiendo con la referencia de la fase.
- La prueba manual anterior sigue **NO ACEPTADA**. El resto de faltantes exige decidir la cobertura del próximo recorrido de A.1. Una sola clave cubriría como máximo 140 de los 6.263 retornos por faltantes del registro manual.

Desde la raíz del checkout, con el fixture de la integración preparado en `$work`, ejecutar `& "$work/test_ordered_edges.ps1"` y `& "$work/run_edges_sdl.ps1"`. Para el replay, recompilar con `& "$work/build_bullet_replay.ps1"` y ejecutar `python -B "$work/run_ordered_bounds.py" replay-edges-fixed`, usando un nombre de salida nuevo para otra ejecución.

| Evidencia | SHA-256 |
|---|---|
| `ordered-edges.log` | `a02d52b0ffae4e10f4a9784d0d3b2b7acc3534502edd98035111078efcedb9c3` |
| `edges-sdl.log` | `d322ee281c00e16f6eb22a6d1e4346f320445035f3d884f13105da78c0357052` |
| `replay-edges-fixed/engine.log` | `4ac4ca8e51ce354e583756d2fb5297101cc72646e82d724aed04b3f373241787` |
| Ejecutable de diagnóstico corregido | `740379f2f89c6a7dd20e7b51d71085f3dd3d220278d461823d6ffabc6551b600` |
