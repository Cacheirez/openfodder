# Microbloque A.1 — publicación inicial de m1p2

8 de noviembre de 2026. Relevo de entrada `3122595`; implementación `babb62b`. Plan 2.74 conservado. **Publicación inicial desbloqueada en Windows; B continúa bloqueado.** [Evidencia](evidence/demo-a1-publication.json).

## Cambio acotado

- Cuatro vínculos explícitos en `assets/modernization/demo-a1-associated.json`: rango tipo 21, hojas 0x95/F0 y 0x7C/F0; ave tipo 19, hoja 0x98/F0–F1. La segunda clave del rango conserva su marcador transparente original: `Sprite_Handle_Player_Rank`, salida `loc_1AF63`. No se añade arte ni una excepción por clave observada.
- Tres claves capturadas desde la ruta real; la del marcador se reconstruye desde la tabla TheOne y los bytes/paleta retenidos del rango, y reproduce exactamente su clave observada. Las cuatro se verifican con `LoadNativeWalkSnapshot`/`SoldierVariantKey`, hash del recurso y raster nativo. Tabla: `mSpriteSheetTypes_InGame_Amiga_TheOne`; `eGFX_IN_GAME2` conserva la paleta efectiva 0 que selecciona el backend Amiga, no el campo bruto 13480 de la tabla.
- El único cambio del resolver permite conservar el ave Amiga tipo 19/0x98/F0–F1 válida, fuera de vehículo y sin destrucción pendiente, **después de encontrar un vínculo exacto**. Cuerpos, enemigos, civiles, otras hojas/frames y claves desconocidas no reciben este permiso.
- `prepare_demo_a1_manifest.py` exige el manifiesto D6 exacto, comprueba los 160 activos por SHA-256 y copia sus bytes sin modificarlos. Resultado: 80 poses, 160 activos, **318 `replace-art` + 4 `keep-associated` = 322 vínculos**. No se modifica ningún lanzador ni se entrega un paquete.

## Publicación efectiva y bloqueos restantes

Se recompila el motor Windows x64 con MSVC 19.44 y SDL 3.4.0 ya instalados, sin reconstruir dependencias. Proyecto diagnóstico existente adaptado; ejecución medida con `WindowHD.cpp` **idéntico al de Source, sin instrumentación de captura**. Compilación sin mixer, recorrido `--nosound`; no es un nuevo ejecutable de entrega. El SHA del ejecutable nuevo figura en la evidencia y difiere del D6 anterior.

Replay público m1p2 intacto, SDL software/dummy, 12×, cadencia de producción sin override, sin pausa ni supresión de entidades:

| Medida | Resultado |
|---|---:|
| Intentos ordenados | 4.554 |
| Publicaciones HD efectivas | **680** |
| Publicaciones de cuerpos HD | **3.248** |
| Retornos por claves ausentes | **3.874** |
| Comandos sin censar | 0 |

Primera publicación: intento 365, escena 186, intervalo 364; siete comandos, **cinco cuerpos reemplazados y dos elementos conservados**, cero faltantes. Ave F0 y F1 se conservan por sus claves. El primer tramo tiene 117 transacciones publicadas consecutivas entre los intentos elegibles; **no se convierte esta cifra en segundos ni se equipara a continuidad jugable**, porque las puertas de paleta y otras presentaciones no están incluidas en ese contador.

Primer rechazo posterior: intento 599, intervalo 598, enemigo tipo 5/hoja 0x54/F0, clave `19a04cf62b5486e35710f8d51a8b4fc7a6154c546b9ed944023575dd4dd503f6`. En la traza el primer enemigo dibujado sigue apareciendo en tick 203 (~4,06 s nominales). Se mantienen 83 claves enemigas y 29 claves del jugador sin cubrir, además de proyectiles, sombras, vegetación y otros estados. Se registran en la evidencia sin añadir vinculaciones. Ninguna patrulla tranquila de 30–60 s está demostrada.

La medición intermedia con solo tres vínculos publicaba 297 intervalos y detectó el marcador 0x7C del rango; se conserva localmente, sustituida por la medición final. La tentativa `measured-complete` arrancó antes de preparar correctamente su manifiesto: **descartada**, nunca cobertura válida. El resultado publicado procede exclusivamente de `verified`, iniciado con el manifiesto final ya disponible y verificado.

## Pruebas técnicas y límites

- Windows LLVM 23.1.5 x64 **ASan/UBSan PASS**, sin hallazgos ni avisos de ejecución. Fixture recompilado con el resolver y pruebas actuales; `detect_leaks=0` por la disponibilidad del runtime Windows, sin atribuir LSan. Ambos frames del ave, rango, claves de otra paleta, frame/hoja/formato inválidos, vehículo, destrucción, cuerpo tipo 0, enemigo tipo 5 y civil tipo 61; rechazo y recuperación del intervalo completo al retirar el cuerpo.
- Comparación exacta del framebuffer SDL con el oráculo CPU a 8×/12×; los píxeles clásicos asociados conservan su raster independiente, recortes y oclusión sobre celdas HD, incluso escrituras del mismo color. También permanecen los casos previos de fallo de publicación/recuperación SDL y censos incompletos. Contrato OFF/ON verificado directamente: 33 transacciones, 16 publicaciones, ocho rechazos por faltantes, cuatro comandos sin censar rechazados. El envoltorio con `TemporaryDirectory` falló al crear su carpeta del sandbox en `%TEMP%`; operación detenida y log conservado, sin atribuirle PASS. El fixture directo y sus contadores se verifican en el directorio autorizado.
- Replay moderno final y contraste clásico con **el nuevo ejecutable**, 1.546 muestras cada uno, coinciden byte a byte con el mismo H3 inmutable y entre sí. Auditoría clásica del intervalo activa en la ruta HD, sin divergencias. No se repite H3 completo de 11 fases/11.361 estados ni pruebas de selectores no modificados; las referencias permanecen intactas.
- CI Linux D6 `42469760868` consultada: job `build` completado con éxito, 57 pasos correctos (58 pasos totales); no relanzada ni atribuida al nuevo código. CI de implementación A.1: Windows `42484711149` y Linux `42484711218` en curso al registrar el relevo; densidades `42484711137` PASS. **CI nueva completa y ASan/UBSan/LSan Linux PENDIENTES.** No se reintenta WSL tras el bloqueo previo ni se reconstruye LLVM.
- **Aceptación visual/jugando PENDIENTE:** las comparaciones de píxeles son pruebas técnicas; no acreditan aceptación de Miguel, GPU, audio, CD32, patrulla a velocidad normal o transiciones pausa/mapa/reanudación. El replay acelerado no mide continuidad interactiva.

## Recuperación y reproducción

Directorio local: `C:/Users/migue/.codex/visualizations/2026/11/08/01a1bb46-b87b-7671-82cd-0fdee66db3de/a1`. Conserva dependencias reutilizadas por ruta, proyecto/build, ejecutable, recursos públicos, snapshots/rasters locales, manifiesto, logs completos, trazas y scripts. Hashes y rutas concretas en la evidencia; no se publican bytes originales ni logs grandes.

1. Combinar D6: `python -B tools/modernization/prepare_demo_a1_manifest.py --base <D6-exacto>/candidate-manifest.json --out <directorio-nuevo>`.
2. En el directorio local, `python -B verify_associated.py`: verifica las cuatro claves contra tablas/bytes y genera `verification.json`, sin aprobar claves nuevas.
3. `test.ps1` recompila y ejecuta el fixture Windows ASan/UBSan con herramientas existentes; logs `fixture-build.log` y `fixture-run.log`. Para el contrato con diagnósticos, ejecutar el mismo fixture con `OPENFODDER_ORDERED_COVERAGE=1`; `coverage-fixture-final.log` conserva el resultado comprobado.
4. `python -B replay_probe.py "Amiga The One" 1 2 <nombre-nuevo>` reproduce el recorrido HD con el manifiesto final. `classic_probe.py` usa HD desactivado. Ambos registran entorno, comandos, hashes y trazas. Comparar el payload normalizado LF con `reference-gameplay-v1.json`, entrada `Amiga_The_One_m1_p2.jsonl`.

**Siguiente tarea única:** reevaluar una patrulla tranquila de 30–60 segundos de m1p2 con varios soldados; consultar antes la CI nueva. B y su activación/paquete no están autorizados ni acreditados. Detenerse tras publicar este relevo; se recomienda abrir un hilo nuevo con `PROMPT_NUEVO_HILO.md`.
