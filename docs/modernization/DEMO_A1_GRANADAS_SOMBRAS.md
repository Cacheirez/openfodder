# A.1 — Continuidad de granadas, sombras y explosiones

17-11-2026. Fuente `ae1b6bd`, continuación autorizada por Miguel para resolver retornos del pelotón al recibir daño y lanzar granadas, incluidas las sombras relacionadas. Sin cambios de simulación ni arte nuevo. PR #1 sigue abierta, borrador y sin fusionar. Plan 2.74 vigente; B, nuevas familias, scroll y 16:9 fuera de este bloque.

## Cambio y motivo

Se conserva el ciclo nativo completo en el experimento híbrido de Amiga The One M1P2, manteniendo todos los controles existentes de identidad, procedencia, bytes, geometría, presupuesto y recuperación SDL:

| Tipo/hoja | Frames admitidos | Procedencia y función |
|---|---|---|
| 2/`0x7D` | 0–3 | Granada; altura selecciona frame en `Sprite_Handle_Grenade`. |
| 3/`0x7E` | 0–3 | Sombra independiente, altura cero; sigue al slot anterior y conserva su orden First. |
| 2/`0x7C` | 0 | Fase invisible del lanzamiento, solo con raster sin escrituras. |
| 12/`0x7D` | 0–3 | Transición: el manejador de granada cambia el tipo antes de que el de explosión actualice la hoja. |
| 12 o 39/`0x8E` | 0–6 | Explosión normal/de edificio. |
| 12/`0xC0` | 0–3 | Variante aérea de explosión. |
| 47/`0xC5` | 0–2 | Chispas creadas desde la explosión. |
| 48/`0xC6` | 0–3 | Estelas creadas desde las chispas. |

`ResolvedSpriteResource.hpp` declara estos pares y límites; `OrderedSoldierRegistry.hpp` verifica que la granada invisible solo se conserve sin escrituras y dentro del experimento. `Surface.hpp` y `WindowHD.cpp` reutilizan su captura de procedencia existente; no cambia el dibujo clásico ni el modo estricto. Un faltante o error real sigue rechazando la escena completa. La sombra permanece como comando separado; no se fusiona con el cuerpo ni se dibuja sobre la escena terminada.

La conservación aislada de granada/sombra proyectaba 7.168 publicaciones, pero ocho retornos frente a seis: simplemente trasladaba interrupciones a la explosión. Se incluyeron y verificaron los estados posteriores del mismo ciclo antes de ofrecer un candidato. Las funciones originales `Sprite_Handle_Grenade`, `Sprite_Handle_Explosion`, `Sprite_Create_Sparks` y `Sprite_Handle_Sparks` explican la cadena; no se modifican.

## Tres claves de lanzamiento ya tienen arte

El registro manual contiene `0x0A/F0–F2`, animación 0, paleta efectiva 0. Las referencias anteriores de esa misma dirección/frame Amiga tenían paleta 128. Comparten fuente, geometría y alfa, pero **no colores nativos equivalentes**: la referencia antigua se renderiza negra. Se verificaron las claves reales y se reutiliza el diseño HD del aliado ya aprobado para esa misma pose, dirección y frame. No se inventa una equivalencia de paleta ni se genera arte.

[Vínculos explícitos y diferencias](../../assets/modernization/demo-a1-player-grenade-native-palette.json). Candidato local `granada-candidate/`: **198 activos intactos y 363 vínculos**, conserva los 360 anteriores, incluidos los doce de impacto. La aceptación visual de estas variantes de paleta sigue pendiente.

## Pruebas y resultados

- **PASS técnico WindowHD/SDL software 8×/12×:** Windows Clang 23.1.5 ASan/UBSan y Linux Clang 18.1.3 ASan/UBSan/LSan. Todos los frames del contrato se ejercitan con cuerpos HD, orden original, recorte, ceros/igual color, Save/Restore, rechazo fuera del experimento o sin procedencia, datos inválidos y recuperación SDL completa. Las tres claves del cuerpo pasan además el fixture con su recurso real, dos jugadores y recuperación clásica.
- **PASS de datos reales:** 26 snapshots asociados del replay verificados con el renderizador nativo C++, hashes de recursos y claves. No se publican bytes originales.
- **PASS replay real M1P2:** 4.096 publicaciones HD y 458 faltantes en 4.554 intentos; conserva los 1.546 estados canónicos originales. Son 96 publicaciones más que el diagnóstico de impacto anterior. La conservación de las publicaciones previas se contrasta en la evidencia. El replay no contiene las tres claves nuevas de lanzamiento izquierdo; estas se ejercitan en el fixture real.
- **PASS H3 local Windows del binario diagnóstico:** 11 fases y 11.361 estados idénticos a la referencia original. CTest/CI de implementación se consulta por separado, sin atribuir PASS antes de observarlo.
- **Proyección manual**, condicionada a los contratos nativos: 6.991→7.276 publicaciones, seis→cuatro retornos con el mismo jugador y cero rachas de uno a tres intentos en ambos. No es un replay nuevo de la partida de Miguel. Los cuatro retornos restantes comienzan por daño/muerte `0x22`, `0x2D`, `0x29`, `0x2C`; no se declara resuelto todo el daño.
- **PENDIENTE:** aceptación jugando y artística de Miguel, CD32 comercial, GPU y audio. No extrapolar las cifras de la demo ni confundir preservación clásica provisional con sombras modernas finales.

Incidencias de validación: una prueba negativa detectó la granada invisible fuera del ámbito y se corrigió. Las explosiones grandes excedían el backing 96×64 del fixture: se ajustaron sus márgenes y se reservó la última fila para las escrituras Amiga que cruzan una scanline. No se relajó el validador del juego. Las ejecuciones finales usan directorios de trabajo separados. Los intentos fallidos anteriores no cuentan como PASS. Se reutilizaron SDL, compiladores y runtimes existentes.

## Recuperación local y entrega

Carpeta `C:/Users/migue/.codex/visualizations/2026/11/17/01a1ea7b-b727-78f2-a6ac-a4b32dc39150/`:

- `grenade-complete-replay/`, `grenade-complete-h3-{pc,amiga}/`, logs de sanitizadores y snapshots locales.
- `run-grenade-{win.ps1,linux.sh}`, `run-palette-*`, `prepare_grenade_palette.py`, `granada-candidate/` y `grenade-complete-projection.json`.
- Binario diagnóstico `grenade-probe-build/Release/native_probe.exe`, SHA-256 `ad05c26a3fe828997e3787f29694c833b2c91736055a2ffc5773f3bc01617e37`. Captura local solo en el experimento M1P2, con límites conservados de 512 claves y 1 MiB por recurso; incluye poses del jugador y asociados del ciclo.
- Lanzador `Probar-P1-Granadas.ps1`: comprobación de hash/rutas PASS sin abrir el juego. Puede probar híbrido, estricto y clásico. La entrega para jugar espera la CI relevante y el punto de revisión del hito.

[Evidencia documental y hashes](evidence/granada-sombra-ciclo-20261117.json). Tras la CI, la siguiente tarea técnica autorizada es reevaluar daño/muerte con este ciclo resuelto; antes de ampliar direcciones, preparar solo el piloto que necesite revisión de Miguel. Esta hoja de ruta no acepta visualmente nuevas poses.

## CI y contraste entre partidas

Las primeras ejecuciones de `703bbd0` fallaron en `soldier_ordered_hybrid`, dentro de CTest: [Windows](https://github.com/Cacheirez/openfodder/actions/runs/44159368027) y [Linux](https://github.com/Cacheirez/openfodder/actions/runs/44159367951), 28/29 pruebas correctas. El verificador de cobertura seguía esperando 46 publicaciones y 18 recuperaciones del fixture anterior; los 38 casos añadidos aportan 76 de cada una a 8×/12×: resultado observado 122/94. Se corrigió el cálculo y se exigen además dos resoluciones clásicas por cada tipo/hoja/frame nuevo y densidad. No se cambia el motor para satisfacer el contador. El verificador híbrido y el estricto pasan localmente en ambos sistemas, con los sanitizadores existentes. Nueva CI pendiente; no se cierra el bloque hasta observar sus pasos pertinentes.

Contraste condicional con la misma base de 360 vínculos, normalizando las claves ya disponibles antes del ciclo. Son **proyecciones de los registros retenidos**, no nuevas partidas ni aceptación visual:

| Registro del 17-11 | Publicaciones antes→después | Retornos del mismo jugador | Rachas de 1–3 intentos |
|---|---|---|---|
| Caídas, 16:13:44 | 7.829→8.012 | 6→8 | 0→0 |
| Nado, 17:32:34 | 12.499→12.937 | 12→13 | 5→5 |
| Impacto, 19:54:37 | 6.994→7.276 | 6→4 | 0→0 |

La ganancia de publicaciones no acredita una mejora uniforme de continuidad: en dos muestras aparecen más retornos al abrir tramos HD antes bloqueados. No ocultar esta limitación ni presentar granadas/daño como resueltos jugando. La nueva partida contiene dos escenas (186 y 13877); ambas tienen enemigos y sombra F0 conservados sin vínculo explícito, evidencia del experimento activo. El contraste incluye ambas y solo proyecta los nuevos asociados en escenas con esa evidencia; filtrar únicamente 186 habría omitido la segunda escena. Recuperación: `compare_grenade_samples.py` y `granada-samples-projection.json` en la carpeta local actual. La reevaluación de daño/muerte debe partir de estas tres muestras.

**Cierre de los criterios técnicos pertinentes:** `2795b36` supera CTest y A2/H3 en [Windows](https://github.com/Cacheirez/openfodder/actions/runs/44177040158) y [Linux](https://github.com/Cacheirez/openfodder/actions/runs/44177040180). En Linux también se han observado correctos los pasos de destinos y composición ordenada anteriores al replay de vídeo. Las ejecuciones completas continúan en curso en este punto: no se atribuye PASS completo ni se libera el ejecutable como aceptado. Los sanitizadores focalizados locales y H3 completo del binario ya están comprobados. Se cierra el microbloque técnico y se continúa con la reevaluación acotada de daño/muerte, manteniendo pendientes CI completa y revisión jugable.
