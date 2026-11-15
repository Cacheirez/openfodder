# Prototipo técnico del compositor híbrido

Activar `OPENFODDER_SOLDIER_ORDERED_HYBRID=1` junto con `OPENFODDER_SOLDIER_HD=8` o `12`, un `OPENFODDER_SOLDIER_ORDERED_MANIFEST` válido, `OPENFODDER_CAPTURE_SOLDIER=1` y `OPENFODDER_PRESENT_MISSION_LAYERS=1`.

El primer corte admite de forma provisional el árbol Amiga8 0x90/F0 con los metadatos de su entrada nativa auditada cuando su clave completa carece de vínculo. Un vínculo explícito sigue pasando por las reglas del registro. Se comprueban identidad, bytes retenidos, geometría recortada y huellas de lectura y escritura. Los comandos se reproducen en orden sobre índices y celdas HD, con el respaldo clásico disponible para la recuperación SDL. Las divergencias del oráculo siguen siendo errores visibles. El diagnóstico `OPENFODDER_ORDERED_COVERAGE=1` registra escena, ranura, generación, estado, decisión y resultado de cada transacción.

## Validación de P1.1

- En WSL, GCC 13.3 y SDL 3.4.0 software, ASan/UBSan/LSan. Pasaron 156 escenarios CPU, 348 casos de transacción SDL y los casos de integración del método real de Window. El caso `soldier_ordered_hybrid` usa dos soldados HD y el árbol clásico a 8×/12×. Comprueba oclusiones en ambos sentidos, transparencia, escrituras de cero e igual índice, Save/Restore, rechazo de identidad y bytes inválidos y recuperación pixel a pixel tras fallar el último dibujo SDL. El censo del modo estricto conserva los resultados preexistentes. Reproducir con `ctest --test-dir <build> -R 'soldier_ordered_(sdl_transaction|coverage|hybrid)' --output-on-failure`.
- H3 Windows x64 con el motor y datos públicos existentes en configuración sin mezclador. Las 11 fases y sus 11.361 estados canónicos coinciden con la referencia fijada, mediante las recetas de [desarrollo](DESARROLLO.md).
- Replay público Windows, Amiga The One M1P2, SDL software a 12×. Se comparó el mismo binario y un candidato local de 333 vínculos, obtenido del de 334 retirando únicamente el vínculo preexistente del árbol. Las dos pasadas conservan los 1.546 estados H3 de la fase.

| Modo | Publicaciones HD | Retornos por faltantes | Racha máxima | Publicaciones con árbol nativo |
| --- | ---: | ---: | ---: | ---: |
| Estricto | 1.368 / 4.554 | 3.186 | 628 | 0 |
| Híbrido | 1.894 / 4.554 | 2.660 | 859 | 526 |

La racha cuenta publicaciones consecutivas del replay acelerado. En cada pasada hubo cero interrupciones de transacción. Los soldados siguen sujetos a la cobertura del manifiesto. La mejora de 526 publicaciones mide la recuperación de escenas con el árbol clásico válido cuando falta su vínculo.

GPU, CD32, audio, campaña manual y aceptación visual/jugable **PENDIENTES**.

## Cierre P1.2

La primera CI Linux de `c4dfbfc` pasó el bloque CTest que contiene el caso híbrido. El paso posterior de productores falló porque el recurso sintético omitía la paleta usada en su dibujo. `fc51fb3` sincroniza la paleta en las pruebas de productores y poses. Ambos contratos pasaron después en WSL con ASan/UBSan/LSan y en CI Linux.

- Windows `fc51fb3` completó toda la ejecución, con CTest y H3. [GitHub Actions](https://github.com/Cacheirez/openfodder/actions/runs/43596272488).
- Linux `fc51fb3` pasó CTest, H3, ASan/UBSan, LSan sobre 29 demos públicas y publicación activa y pausa SDL con sanitizadores. El diagnóstico general de TSan seguía en curso en el momento de registrar el cierre focalizado de P1. [GitHub Actions](https://github.com/Cacheirez/openfodder/actions/runs/43596272506).

## Revisión manual de P1

El 14-11-2026 Miguel jugó Amiga The One M1P2 en ambos modos a 12× con SDL software y sin sonido, usando el binario del cierre P1 y el manifiesto de 333 vínculos sin el árbol. Observó alternancia entre soldados HD y clásicos en ambas partidas sin un patrón claro durante el juego. **Continuidad jugable NO ACEPTADA.**

| Modo | Publicaciones HD | Retornos por variantes ausentes | Transiciones HD→clásico con el mismo soldado presente |
| --- | ---: | ---: | ---: |
| Híbrido | 811 | 1.545 | 21 |
| Estricto | 1.952 | 5.554 | 24 |

En híbrido, el compositor resolvió conservar el árbol tipo 14 `0x90/F0` en clásico en 255 intentos. En 42 se publicó junto a al menos dos soldados HD identificados por ranura y generación. En estricto, el árbol figuró como faltante en 2.165 intentos y todos volvieron al clásico. Todos los rechazos registrados fueron `missing-variant`. Los recorridos de distinta duración sirven para comprobar el comportamiento en cada modo. La comparación controlada de frecuencia permanece en el replay público.

Para recotejar las transiciones, cruzar `SOLDIER_ORDERED_RESULT` y `SOLDIER_ORDERED_COMMAND` por intento. Contar pares adyacentes `published` → `missing-variant` con salto de uno o dos y al menos un soldado tipo 0 común por ranura y generación. En los 45 pares, los faltantes eran de otros elementos. Catorce de los 21 pares en híbrido contenían el tipo 21 `0x95/F2`. El primer retorno híbrido identificado fue 565 → 567, con cinco soldados comunes y el tipo 6 `0x9D/F2` como único faltante.

Registros locales en `%LOCALAPPDATA%/Temp`:

| Fichero | SHA-256 |
| --- | --- |
| `OpenFodder-P1-hibrido-20261114-152042.log` | `70df55415d3b36df801b4b4c39c967bfc5ab3e5ffa2540d5b943f9752a77684f` |
| `OpenFodder-P1-estricto-20261114-152215.log` | `9deca969bcbb7375f8a092f58eb181ca6f70fa8910fbbf94b83bc4160351debf9` |

## Ampliación de la insignia 0x95/F2

Miguel autorizó la ampliación y los pasos técnicos hasta la próxima revisión jugable. La fila F2 de `stru_8D9F8` selecciona `eGFX_IN_GAME2` en el offset 9084, con dos columnas de tabla y diez filas. Se reconstruyó la clave `5c7e974f5135721496bf24d37d5f3515ba86e2f70517f47d28624b3bb5ff72c2` con los bytes y la paleta de la [auditoría F4](DEMO_A1_AUDITORIA_RANGO_F4.md). Coincide con la única clave F2 del registro híbrido manual. El renderizador nativo confirmó el raster 16 × 10, SHA-256 RGBA `24f8d139f258774a643f2dcfd9431d5b8655791659e806a949bf3a411bcb088b`.

Cuando falta el vínculo exacto, el híbrido conserva F2 si coinciden identidad, fila nativa y metadatos del recurso retenido. La composición sigue verificando el recorte y el respaldo clásico. Los vínculos explícitos conservan su precedencia. F2 fue el único faltante con reemplazos disponibles en 780 de los 1.545 rechazos de la partida híbrida anterior. Es un recuento del registro anterior.

- **PASS** en WSL con SDL software, ASan/UBSan/LSan. El caso integrado del método Window a 8×/12× verifica dos cuerpos HD, árbol e insignia por separado, oclusiones en ambos sentidos, transparencia, escrituras de cero e igual índice, Save/Restore y recuperación píxel a píxel tras fallo SDL. Comprueba rechazo de identidad, frame, offset, bytes truncados y geometría alterada. El modo estricto mantiene el rechazo sin vínculo y el censo previo.
- **PASS** en H3 Windows: las 11 fases y 11.361 estados canónicos coinciden con la referencia fijada. El replay público Amiga M1P2 conserva 1.894 publicaciones HD, 2.660 faltantes, 526 publicaciones con árbol clásico y 1.546 estados H3. El replay usa la insignia F0.
- **PASS** adicional con los bytes originales reconstruidos de F2 en WSL con ASan/UBSan/LSan: a 8×/12× se publicaron cinco soldados HD y se compararon las 70 escrituras de la insignia. Se observaron oclusiones en ambos sentidos, dos retornos completos forzados por densidad y recuperación. El registro local `f2-linux-run.log` conserva el rótulo F4 de la prueba reutilizada, con entrada F2 y 70 escrituras. SHA-256 `93464d15ca200ab44926f97774af0e76a30f40b4382d93f8b8a599f75e68a27d`. La compilación opcional de este fixture con Clang 23.1.5 para Windows quedó bloqueada al enlazar `stl_asan.lib`. El mismo caso se completó en WSL.
- **PASS** CI de `4133a63`: Windows completa y revisión de densidades. En Linux pasaron CTest, H3, ASan/UBSan del motor, LSan sobre 29 demos y publicación activa y pausa con sanitizadores. El diagnóstico general TSan de la ejecución Linux seguía en curso al registrar el cierre focalizado. [Windows](https://github.com/Cacheirez/openfodder/actions/runs/43608997788) · [Linux](https://github.com/Cacheirez/openfodder/actions/runs/43608992500) · [Densidades](https://github.com/Cacheirez/openfodder/actions/runs/43608997787).

### Próxima prueba jugable

En PowerShell:

```powershell
& 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1da6a-54a2-7270-8fa9-5eb4a351446f/Probar-P1-F2.ps1'
```

El comando usa el binario local contrastado con H3, el mismo manifiesto de 333 vínculos y Amiga The One M1P2 a 12× con SDL software y sin sonido. Se comprobaron las dependencias y el hash del binario. La sesión interactiva es la revisión pendiente. Volver a caminar, girar y disparar cerca de los árboles. Facilitar la ruta del registro que imprime PowerShell y señalar si el pelotón sigue alternando entre HD y clásico. Basta con empezar por el modo híbrido. Para una pasada adicional de control, usar `-Modo estricto`.

### Revisión jugable tras la ampliación

El 15-11-2026 Miguel ejecutó `Probar-P1-F2.ps1` en modo híbrido y siguió observando alternancia. **Continuidad jugable NO ACEPTADA.** El registro contiene 5.588 publicaciones HD y 6.532 retornos por `missing-variant`. En los 324 intentos con la insignia F2 se resolvió `keep`, pero cada transacción tenía otros faltantes y se mostró en clásico. La partida anterior siguió otro recorrido.

Con el mismo método de recuento de la primera revisión, se observaron 30 pares HD→clásico con al menos un mismo soldado presente. Los faltantes en esos pares eran siempre de otros elementos. Las variantes más repetidas en los retornos fueron tipo 6 `0x7F/F3` (cinco) y tipo 5 `0x7C/F1` (cuatro). Esta dispersión motiva comprobar un contrato reutilizable antes de plantear otra excepción de una sola variante.

Registro local `%LOCALAPPDATA%/Temp/OpenFodder-P1-F2-hibrido-20261115-202104.log`, SHA-256 `e643ab194a7bf679e774569bb7b43789b0b934eea376b7f544ee090e64fb70e9`.

## Auditoría acotada del contrato nativo

Auditado sobre `0fb556e` con los datos locales de Amiga The One M1P2. Los 30 cambios observados del mismo soldado abarcan 18 claves faltantes. Una sola variante aparece como máximo en cinco de esos cambios. Se cruzaron la tabla activa `mSpriteSheetTypes_InGame_Amiga_TheOne`, los comandos del registro y la hoja Amiga8 congelada de la auditoría F2.

| Caso | Procedencia | Evidencia en esta auditoría |
| --- | --- | --- |
| Bala tipo 6 `0x7F/F3` | `stru_8D718`, offset 2230, 16 × 6 | Se reconstruyó una de dos claves ausentes. El renderizador nativo verificó seis píxeles opacos. |
| Puerta tipo 20 `0x99/F0` | `stru_8DB78`, offset 5970, 16 × 15 | Se reconstruyeron las tres claves ausentes, con animaciones 0, 5 y 6. El renderizador verificó un raster con la misma geometría. |
| Insignia tipo 21 `0x95/F0` | `stru_8D9F8`, offset 9080, 16 × 10 | Fila original comprobada. La clave faltante de esta partida sigue sin reconstruirse con la paleta retenida de F2. |
| Tipo 5 `0x7C/F1` y tipo 21 `0x7C/F0` | `stru_8D618`, offset 560, 16 × 1 | Ocho bytes planares cero y raster transparente para la clave reconstruida de tipo 5 (una de dos). La clave tipo 21 del registro queda sin reconstruir. |

**Comparación reproducible.** Se trató cada rechazo `missing-variant` con censo completo y algún soldado tipo 0 resuelto a HD. Un grupo solo despeja el intento si contiene todos sus faltantes, agrupados por tipo y hoja. La última columna aplica el mismo filtro a los cambios HD→clásico ya identificados en la partida; no simula las transiciones que se producirían con una ruta nueva.

| Hipótesis de cobertura | Intentos manuales despejados | Intentos de replay despejados | Cambios manuales observados que podrían evitarse |
| --- | ---: | ---: | ---: |
| Bala tipo 6/0x7F | 79 | 27 | 5 |
| Insignia tipo 21/0x95 | 507 | 0 | 0 |
| Puerta tipo 20/0x99 | 462 | 176 | 2 |
| Tres grupos visibles juntos | 1.087 | 203 | 7 |
| 0x7C para tipos 5, 20, 21 y 24, condicionado a cero escrituras | 411 | 27 | 4 |
| Grupos visibles y 0x7C juntos | 1.513 | 242 | 11 |

Son techos del censo para estos grupos, con 5.588 publicaciones previas sobre 12.120 intentos manuales y 1.894 sobre 4.554 en el replay. El replay permite medir, con los mismos datos y 1.546 estados fijados, una futura integración. F2 y las muestras exactas de esta partida requieren además una prueba controlada con recursos originales. Los tipos corporales con escrituras visibles quedan fuera de esta propuesta. Sigue habiendo retornos por otras variantes.

**Contrato propuesto.** Validar la procedencia en el productor contra la fila seleccionada por la tabla activa y conservar los metadatos junto a los bytes inmutables de `ResolvedSpriteResource`. La generación identifica la copia retenida, con alcance local al productor. Reutilizar `ValidateMissionSpriteRaster` y la comparación de índices, Save/Restore y presentación clásica de `VerifyMissionAudit`. Conservar la precedencia de vínculos explícitos. Para un dibujo visible sin vínculo, exigir tipo y hoja autorizados, identidad de escena y actor, y coincidencia de segmento, offset, layout, paleta efectiva y geometría con el dibujo capturado. Para `0x7C`, exigir además que el productor del raster recortado emita cero escrituras. Una escritura a índice cero o al mismo índice cuenta como escritura y debe mantener su efecto sobre las celdas HD. Los errores de validación conservan la recuperación íntegra. El log de cobertura contiene claves y decisiones; para demostrar estas condiciones en ejecución se necesita la captura del motor.

**Criterio para una integración posterior.** Mantener los modos clásico y estricto, probar oclusión en ambos sentidos y rechazo de bytes, fila o geometría incorrectos con recuperación íntegra. Comparar base y candidato sobre el mismo replay con H3 fijado, pruebas focalizadas 8×/12× y sanitizadores pertinentes. Pasar otra revisión jugable cuando exista una mejora medida. La auditoría conserva el comportamiento actual del motor.

**Recuperación local.** En el directorio de la prueba jugable, ejecutar `python -B auditar-continuidad-p1.py <registro-manual> replay-rank-f2/hybrid/engine.log`. SHA-256 del script `b8bbb49bfd29284685bf36b785178f4b6319583bc081909b1fc3c3124e081be7`, del replay `603fa725a688a1423c459f096cc6d3477fb32825d03d53d91e2de43247964f05`. `python -B reconstruir-auditoria-p1.py <directorio-de-la-prueba>` repite el cotejo de claves con la hoja local de la auditoría F2. SHA-256 `2fbfe7d67edd7429680d1bf6df5ed9ef750793c9007f056688cd520f79c7302e`.

## Contrato Amiga8

Miguel autorizó la implementación acotada. En el híbrido de Amiga The One, el productor conserva la fila activa de `eGFX_IN_GAME2` y su asociación con la copia inmutable y la identidad del dibujo. El registro usa esa procedencia para resolver faltantes de tipo 6/0x7F, 20/0x99 y 21/0x95. Para 0x7C en tipos 5, 20, 21 y 24, un dibujo sin vínculo se admite si el productor recortado emite cero escrituras. La auditoría clásica e independiente sigue comprobando geometría, composición y respaldo antes de publicar. El registro consulta los vínculos explícitos primero. Las discrepancias de procedencia y las escrituras de un supuesto dibujo transparente rechazan la publicación y activan el retorno clásico.

| Métrica en Amiga The One M1P2 | Estricto | Híbrido F2 | Híbrido Amiga8 |
| --- | ---: | ---: | ---: |
| Publicaciones HD | 1.368 | 1.894 | 2.136 |
| Retornos por variantes ausentes | 3.186 | 2.660 | 2.418 |
| Racha de publicaciones más larga | 628 | 859 | 924 |
| Cambios HD→clásico con el mismo soldado presente | — | 17 | 39 |

El replay a 12× usa el mismo manifiesto de 333 vínculos y conserva los 1.546 estados lógicos de la fase. El cotejo por intento, orden, escena, intervalo, ranura, generación y clave confirma 242 cambios a publicación HD y conserva todas las publicaciones anteriores. El mismo método de pares adyacentes de la auditoría cuenta 17 → 39 cambios del mismo actor en el replay acelerado. El aumento de publicaciones crea tramos HD intercalados donde antes persistía el clásico. La comparación no establece aceptación visual ni cuantifica la alternancia a cadencia normal.

- **PASS** en WSL con ASan/UBSan/LSan y SDL software: método Window a 8×/12×, dos soldados HD, dibujo auxiliar en su orden, hoja transparente sin escrituras y rechazo de offset, identidad, copia incompatible y transparencia con escrituras. Pasaron también las comprobaciones previas de oclusión, Save/Restore y recuperación completa tras fallo SDL.
- **PASS** en H3 Windows: 11 fases y 11.361 estados canónicos idénticos a la referencia fijada. El modo estricto repite exactamente el censo del replay anterior.
- **PENDIENTE** CI focalizada de esta ampliación. GPU, CD32, audio, campaña manual y aceptación jugando siguen pendientes.

**Recuperación local.** En el directorio de la prueba jugable, usar `amiga8-contract/validate-h3.ps1` y luego `python -B validate-amiga8-replay.py` con directorios de salida nuevos. SHA-256 del script de replay `eebe8777d1d7f90c4175b7331bdfa28e06f9e3738a56637a1c81d6f7495b2887`, del log híbrido `6fc3a24665e4332c9d76070ed5be39b04846f35295018626c270273213254a15`. El lanzador local `Probar-P1-Amiga8.ps1` tiene verificados los requisitos de arranque con `-Comprobar`. La prueba interactiva no se ha ejecutado.
