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
- La primera CI Windows de `ef626db` rechazó el cambio de huella de `Sprite_Core.cpp` en la auditoría de CD32. Se restauró el fichero byte a byte y se trasladó la captura a `RecordMissionSoldier`. Los 42 tests Python, H3 Windows y ambos censos del replay vuelven a coincidir tras el traslado. [Primera CI](https://github.com/Cacheirez/openfodder/actions/runs/43759357805).
- La CI Linux de `8ff4d60` pasó CTest y A2/H3 antes de que la comprobación de superficies rechazase el cambio de huella de `Surface.cpp`. La definición se aloja ahora en el módulo del híbrido y `Surface.cpp` también queda idéntico a la base de la ampliación. **PASS local con sanitizadores** en geometría y procedencia de destinos (97 casos aceptados y 627 rechazos sin escrituras) y grabación de misión (24 escenarios PC/Amiga y transiciones lógicas idénticas). [CI Linux intermedia](https://github.com/Cacheirez/openfodder/actions/runs/43760226920).
- **PASS CI focalizada de `1c1f48b`** en Windows y Linux para CTest y A2/H3. En Linux pasaron también procedencia y geometría de destinos, pausa y grabación de misión. Las baterías completas seguían en ejecución al cerrar este bloque. La comprobación local adicional de C01 en WSL encontró una diferencia CRLF/LF y luego dependencias ausentes en la copia temporal. La revisión automática bloqueó otro intento por el límite de diagnóstico. GPU, CD32, audio, campaña manual y aceptación jugando siguen pendientes. [Windows](https://github.com/Cacheirez/openfodder/actions/runs/43761306232) · [Linux](https://github.com/Cacheirez/openfodder/actions/runs/43761306218).

**Recuperación local.** En el directorio de la prueba jugable, usar el binario de `amiga8-contract/h3-build/Release` y ejecutar `python -B validate-amiga8-replay.py <directorio-nuevo>`. SHA-256 del script `4c0f2344ed7e5c546f8b2bc28ccfae4764674efac0492bfb2124b93ec82ea39c`, del log híbrido final `d7517497891995b94630befad409485818c7d88c64286169bd623a4d38a5926b`. El lanzador local `Probar-P1-Amiga8.ps1` tiene verificados los requisitos de arranque con `-Comprobar`. La prueba interactiva no se ha ejecutado.

## Continuidad del mismo soldado

Análisis autorizado sobre `37b1ca0`, comparando los dos registros del mismo replay con correspondencia exacta de intentos, comandos ordenados, identidades y claves. Para cada pareja adyacente con salto serial de uno o dos, se cuenta el paso HD→clásico cuando algún jugador tipo 0 reemplazado en el primer intento sigue presente en el siguiente. La identidad usa escena, ranura y generación. Se cuentan también las incidencias por soldado, de modo que un mismo retorno puede afectar a varios.

De los 17 retornos de F2, uno desapareció y 16 persistieron. Los 23 retornos nuevos terminan una racha que incluye al menos una publicación añadida por Amiga8. Diez de esas rachas tienen un solo fotograma HD, doce tienen tres y una llega a 924. Los 39 retornos del candidato afectan a 177 incidencias por soldado, frente a 77 en F2. Son publicaciones del replay acelerado.

**Bala 0x9D.** `Sprite_Create_Bullet` selecciona esta hoja y toma el frame de la dirección del tirador. La tabla activa de Amiga The One remite a las ocho filas de `stru_8DC18`, segmento `eGFX_IN_GAME2`, con dos columnas de tabla y siete filas. La hoja congelada de F2 permitió reproducir las 11 claves ausentes observadas para los ocho frames de tipo 6/0x9D. El renderizador nativo confirmó un ejemplo F6 de 16 × 7, clave `12bcea3883edff9ca7c6a4ced22299a342853397359d156b63df6ac91d7fd69d`, SHA-256 RGBA `58fa02ffc398fa37b023df11cccf31e58ded61fbfa32fcfdc6c9f28b4a007670`.

| Escenario del mismo replay | Publicaciones HD | Retornos con el mismo soldado | Incidencias por soldado |
| --- | ---: | ---: | ---: |
| Contrato Amiga8 observado | 2.136 | 39 | 177 |
| Proyección admitiendo solo 0x9D/F6 | 2.160 | 33 | 153 |
| Proyección admitiendo los ocho frames de 0x9D | 2.190 | 24 | 116 |

La simulación pasa un intento a HD solo si tiene un reemplazo de jugador y todos sus faltantes corresponden a la hipótesis. Luego recalcula los cambios sobre toda la secuencia. Para la hoja completa desaparecerían 17 retornos y aparecerían dos. Admitir todos los del tipo 6 proyecta el mismo resultado en este replay. Se propone la hoja 0x9D acotada porque aprovecha el contrato existente y tiene evidencia de los ocho frames.

**Criterios de un eventual ajuste.** Conservar las 2.136 publicaciones previas y reducir los 39 retornos de referencia en el mismo replay. Como objetivo medible, contrastar las cifras proyectadas 2.190 y 24. En prueba focalizada, verificar el orden de dibujo, los rechazos ante procedencia o bytes incompatibles y la recuperación íntegra. Mantener modo estricto, clásico, H3 y pruebas pertinentes. La proyección sigue pendiente de implementación, verificación SDL y aceptación jugando.

**Reproducción local.** En el directorio de la prueba jugable, ejecutar `python -B analizar-cambios-amiga8.py replay-rank-f2/hybrid/engine.log amiga8-contract/replay-final/hybrid/engine.log`. SHA-256 del script `1b7ea1a38ed111f1359346456f793805e5d391e1fbd0fdc895f63763e1216537`, del lector `audit_reader.py` `fef62eb40e068766949069b41a39fa0a29d8ae151566082e647fbfc360462c5e`. Desde la raíz del repositorio, `python -B <directorio>/reconstruir-bala-9d.py <directorio> <log-híbrido-final>` repite la comprobación de las claves. SHA-256 `64857034163d6107f851a7a82250eb25654f7475d18305a46b5105a1def8fe95`.

## Ampliación a la bala 0x9D

La bala tipo 6/0x9D usa el mismo contrato de procedencia nativa que 0x7F. El modo híbrido puede dibujarla en clásico en su turno cuando carece de vínculo y la fila activa de Amiga The One, el recurso retenido y la geometría pasan la validación.

- **PASS replay controlado:** Amiga The One M1P2, SDL software a 12×, mismo manifiesto y las mismas 4.554 transacciones. El híbrido pasa de 2.136 a 2.190 publicaciones HD y de 39 a 24 retornos con el mismo soldado. Se conservan las 2.136 publicaciones previas, desaparecen 17 retornos y aparecen dos. Las incidencias por soldado pasan de 177 a 116. La racha máxima queda en 924. El resultado coincide intento por intento con la proyección. La fase conserva sus 1.546 estados lógicos y el modo estricto conserva sus 1.368 publicaciones y 3.186 rechazos.
- **PASS pruebas focalizadas:** Windows H3, 11 fases y 11.361 estados fijados. WSL con ASan/UBSan/LSan, SDL software 8×/12×, caso F6 entre dos soldados HD, rechazo por offset, identidad o copia incompatible y regresiones de orden, transparencia y recuperación SDL. Pasaron también los 42 tests Python.
- **PASS CI focalizada** de `3a97793` en Windows y Linux para CTest y A2/H3. Las baterías completas seguían en ejecución al cerrar. [Windows](https://github.com/Cacheirez/openfodder/actions/runs/43772392998) · [Linux](https://github.com/Cacheirez/openfodder/actions/runs/43772393001).
- **PENDIENTE:** revisión jugable de Miguel, GPU, CD32, audio y campaña completa.

**Reproducción local.** Desde el directorio de la prueba, ejecutar `python -B validate-amiga8-9d-replay.py <directorio-nuevo>`. Comparar con `python -B check-amiga8-9d-replay.py amiga8-contract/replay-final/hybrid/engine.log <directorio-nuevo>/hybrid/engine.log`. SHA-256 del registro de la medición `25159e3b07ceb0c4cba7a6196aec4e5230967c764f9830fe243cddf26c3ccfb0`.

### Revisión jugable de 0x9D

En PowerShell:

```powershell
& 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1da6a-54a2-7270-8fa9-5eb4a351446f/Probar-P1-9D.ps1'
```

Abre Amiga The One M1P2 a 12×, híbrido y SDL software sin sonido. Se comprobaron el ejecutable, su hash, el manifiesto y las dependencias con `-Comprobar`. Queda pendiente el lanzamiento interactivo. Jugar con normalidad, moviendo y girando al pelotón y disparando. Facilitar la ruta del registro que imprime PowerShell e indicar si los mismos soldados siguen alternando entre HD y clásico y si el cambio se nota respecto a la prueba anterior.

### Resultado jugable y continuidad de los enemigos

El 16-11-2026 Miguel observó menos alternancia que en las pruebas anteriores, con retornos que aún se perciben. La partida híbrida de Amiga The One M1P2 tuvo 4.388 publicaciones HD de 8.105 intentos registrados y 3.717 retornos `missing-variant`. La bala tipo 6/0x9D resolvió `keep` en los 1.113 comandos en que apareció; 82 se publicaron con la escena HD. Los recorridos manuales son distintos. La comparación cuantitativa antes/después está fijada por el replay.

El censo con el mismo soldado presente identifica 27 retornos, con 135 incidencias por soldado y 16 claves faltantes distintas. En 24 retornos todos los faltantes eran enemigos tipo 5. Los tres casos más frecuentes fueron `0x64/F1` (ocho), `0x6A/F1` (cuatro) y `0x6B/F1` (cuatro). Otro retorno combinó enemigo y bala, uno combinó jugador, granada y sombra pequeña, y otro correspondió al tipo 27.

| Muestra | Publicaciones HD observadas → proyectadas | Retornos del pelotón observados → proyectados | Enemigos con HD y nuevo clásico dentro de publicaciones HD |
| --- | ---: | ---: | ---: |
| Partida de Miguel | 4.388 → 4.565 | 27 → 13 | 3 |
| Replay de control 0x9D | 2.190 → 2.340 | 24 → 12 | 5 |

Se proyectó admitir únicamente las tres poses F1 anteriores. Se exige algún jugador resuelto a HD y que todos los faltantes del intento pertenezcan al grupo. Después se recalculan los retornos y las representaciones de cada enemigo por escena, ranura y generación. En el replay se proyecta un cambio directo del mismo enemigo de HD a clásico en dos publicaciones HD adyacentes. Las proyecciones proceden del censo y quedan pendientes de validación de bytes, geometría y composición. En la partida, admitir indiscriminadamente todos los enemigos proyectaría 5.629 publicaciones, pero conservaría 26 retornos con el mismo soldado. La cobertura por sí sola es insuficiente para resolver continuidad.

**Estado.** La mejora percibida de 0x9D queda registrada. La próxima ampliación de dibujos visibles afectaría a cuerpos enemigos con cobertura parcial. Se necesita un tratamiento que preserve la representación de cada actor antes de integrar esas poses. La aceptación jugable permanece pendiente.

**Recuperación.** Registro local `%LOCALAPPDATA%/Temp/OpenFodder-P1-9D-hibrido-20261116-111148.log`, SHA-256 `b532bf0d9c15f763c44269e8385e66230030c4ed6db349dea23c020aed5fc033`. En el directorio de la prueba, ejecutar `python -B analizar-partida-9d.py <registro-manual>`. El script usa el replay validado de 0x9D y el lector anterior. SHA-256 `6f0fea2fd310dcf216bd5197b4a89a2d1d2ec8af0e8a15bca157fca0efe65b08`.

### Siguiente prototipo de continuidad

Miguel encargó elegir la ruta más rápida y efectiva y convertirla en el siguiente paso del plan. Se compararon las políticas sobre el registro manual y el replay controlado de 0x9D. Cada celda indica publicaciones HD y retornos a clásico con el mismo soldado presente.

| Política | Partida de Miguel | Replay | Aspecto del enemigo |
| --- | ---: | ---: | --- |
| 0x9D actual, observado | 4.388 / 27 | 2.190 / 24 | Retornos de escena completa |
| Admitir las tres poses enemigas más frecuentes | 4.565 / 13 | 2.340 / 12 | Tres identidades con HD y clásico en la partida, cinco en el replay |
| Mantener todos los enemigos tipo 5 en clásico durante la fase | 5.629 / 26 | 2.899 / 11 | Clásico fijo, 11 identidades ceden HD en la partida y 10 en el replay |
| Enemigos en clásico fijo y admitir tipo 4/0x7C si emite cero escrituras | 5.671 / 20 | 2.905 / 10 | Clásico fijo |

Las tres últimas filas son proyecciones. Un intento adicional solo puede publicarse si todos sus faltantes pertenecen a la política y queda al menos un soldado jugador HD. En la ruta elegida, las rachas HD de una a tres publicaciones pasan de 34 a 61 en el registro manual y de 20 a 13 en el replay. Este indicador ayuda a distinguir una escena con más HD de una mejora de continuidad que se note jugando. La opción de fijar un estilo por clase de enemigo con cobertura demostrada queda para cuando exista un criterio de selección comprobable antes de dibujarlo.

**Microbloque elegido.** Prototipo opt-in en Amiga The One M1P2. Seleccionar el modo al empezar la fase y conservar a los enemigos tipo 5 en clásico incluso en poses con vínculo HD dentro de este modo. Es una decisión provisional para comprobar continuidad del pelotón y de los enemigos con una regla fija. Reutilizar el registro de procedencia de la tabla activa, extender la comprobación a `eGFX_IN_GAME` para los enemigos que lo usan y comprobar el segmento real de cada fila. La rama de tipo 4/0x7C debe verificar la procedencia y comprobar con el productor recortado que hay cero escrituras. Los errores de integridad y publicación requieren recuperación clásica íntegra. Se conservan las garantías del modo clásico y estricto y el alcance final de H7/H8.

**Criterio de salida.** Antes de otra partida, verificar con recursos originales que los enemigos se dibujan en orden clásico, con oclusiones en ambos sentidos y continuidad por escena, ranura y generación. Probar fila, bytes y recorte inválidos, escritura inesperada en tipo 4 y fallo SDL. Comparar con 0x9D en el mismo replay a igual manifiesto y densidad. Deben disminuir los retornos y las rachas HD cortas en el replay, conservarse las publicaciones anteriores de los soldados y estar ausente la alternancia de enemigos dentro de la escena híbrida. Contrastar la proyección manual antes de pedir otra valoración. H3, CI focalizada y sanitizadores pertinentes siguen siendo criterios.

**Reproducción.** En el directorio de la prueba, ejecutar `python -B comparar-rutas-continuidad.py <directorio> <registro-manual>` y `python -B proyectar-escena-clasica-enemigos.py <directorio> <registro-manual>`. Usan el replay de 0x9D y los lectores anteriores. SHA-256 de los scripts `0ca13ff84beaf4591b7ef73032998d93797bf7f707ff7c0b5d6bb7b277f4b21c` y `e1c990371522ce7063bdede14bf05a829e07d349676d552cae006636c0f5b8f4`.

## Prototipo con enemigos clásicos

`OPENFODDER_SOLDIER_ORDERED_CLASSIC_ENEMIES=1` activa el ensayo sobre el híbrido para Amiga The One M1P2. La selección del proceso se captura de forma fija y la grabación de cada intervalo conserva la política de la fase. El tipo 5 se dibuja en clásico en su turno, incluidas las poses con vínculo HD. La validación usa la fila de la tabla activa, el recurso retenido, los dos segmentos de juego de Amiga8 y los límites del raster. El tipo 4/0x7C exige cero escrituras. Una discrepancia rechaza el intervalo completo.

| Mismo replay M1P2, 4.554 intentos a 12× | Híbrido 0x9D | Prototipo |
| --- | ---: | ---: |
| Publicaciones HD | 2.190 | 2.905 |
| Retornos con el mismo soldado | 24 | 10 |
| Incidencias de retorno por soldado | 116 | 47 |
| Rachas HD de hasta tres publicaciones | 20 | 13 |
| Mayor racha HD | 924 | 1.007 |

- **PASS replay:** se conserva cada una de las publicaciones anteriores de soldados HD. La proyección coincide con los intentos publicados y los retornos. Diez identidades de enemigo se publicaron siempre en clásico. El tipo 4/0x7C se conservó en 31 comandos, seis intentos publicados. Todos los rechazos registrados fueron por variantes ausentes. El modo estricto con el interruptor presente conserva 1.368 publicaciones y 3.186 faltantes. El híbrido 0x9D con el interruptor apagado conserva su censo.
- **PASS focalizado en WSL:** ASan/UBSan/LSan, SDL software a 8×/12×, errores de fila, identidad, bytes, recorte y escritura inesperada, más recuperación íntegra ante fallo SDL. En la prueba del recurso original `0x59/F0` con vínculo HD, sus 67 escrituras cubren HD anterior y 48 quedan cubiertas por un soldado posterior. El resultado SDL coincide píxel a píxel y se recupera el clásico tras un rechazo. Los 42 tests Python pasaron.
- **PASS H3 Windows:** 11 fases y 11.361 estados iguales a la referencia fijada. Las tres pasadas del replay conservan los 1.546 estados de M1P2.
- **PASS CI focalizada** de `1f19c6c` en Windows y Linux para CTest y A2/H3. En Linux pasaron también la identidad y geometría de destinos, la grabación de misión y la detección de escrituras ausentes. Las baterías completas seguían en ejecución al cerrar. [Windows](https://github.com/Cacheirez/openfodder/actions/runs/43851388485) · [Linux](https://github.com/Cacheirez/openfodder/actions/runs/43851388454).
- **PENDIENTE:** valoración jugable, GPU, CD32, audio y campaña completa. El registro manual anterior no equivale a un replay y sus métricas proyectadas quedan como referencia de la valoración.

**Reproducción local.** Desde el directorio de la prueba, ejecutar `python -B validate-classic-enemies-replay.py <directorio-nuevo>`, luego `python -B check-classic-enemies-replay.py <directorio-nuevo>/hybrid/engine.log <directorio-nuevo>/classic-enemies/engine.log`. SHA-256 del registro del prototipo `d3c7fe8afa558249b34246818823f069d8e3276b609117dd63a21b41d306b2fa`. La prueba con el recurso original queda en `classic-enemies/run-native-enemy.sh` y el registro `classic-enemies/enemy-run.log`.

### Revisión jugable con enemigos clásicos

En PowerShell:

```powershell
& 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1da6a-54a2-7270-8fa9-5eb4a351446f/Probar-P1-EnemigosClasicos.ps1'
```

Abre Amiga The One M1P2 a 12× con híbrido, enemigos clásicos, SDL software y sin sonido. Se comprobaron el binario, su hash y las dependencias con `-Comprobar`. El arranque interactivo queda pendiente. Jugar con normalidad, con movimiento y disparos cerca de enemigos. Facilitar la ruta del registro y señalar si el pelotón alterna menos y si los enemigos conservan el mismo aspecto durante la fase.

### Revisión del combate con enemigos clásicos

El 16-11-2026 Miguel apreció algo menos de alternancia y señaló que sigue siendo más visible cuando hay enemigos en pantalla y se interactúa con ellos. Se registraron 5.178 publicaciones HD de 7.503 intentos y 2.325 rechazos por `missing-variant`. Los 8.606 comandos de enemigo tipo 5 resolvieron `keep`. Catorce identidades distintas de enemigo aparecieron en publicaciones HD con su dibujo clásico.

Se observaron nueve pares consecutivos HD→clásico con el mismo soldado en escena, 35 incidencias por soldado. Siete tenían como único faltante el impacto de bala tipo 6 `0x96/F0`. En otro faltaba también una pose de jugador. En el noveno faltaban jugador, granada y sombra pequeña. `Sprite_Handle_Bullet` selecciona `0x96/F0` al entrar en su animación de impacto. El log permite identificar el recurso faltante, sin atribuir el impacto a un enemigo concreto.

| Política simulada | Publicaciones HD manual / replay | Retornos manual / replay | Rachas HD de una a tres publicaciones manual / replay |
| --- | ---: | ---: | ---: |
| Prototipo observado | 5.178 / 2.905 | 9 / 10 | 24 / 13 |
| Admitir impacto tipo 6/0x96 | 5.199 / 2.923 | 9 / 11 | 31 / 20 |
| Admitir sangre tipo 23/0x96 | 5.295 / 2.989 | 11 / 9 | 35 / 11 |
| Admitir impacto y sangre | 5.415 / 3.029 | 8 / 10 | 47 / 19 |

Las proyecciones recalculan las secuencias completas y suponen que los nuevos dibujos pasarían la validación nativa. El impacto aislado elimina siete retornos manuales antiguos y añade otros siete al abrir tramos HD nuevos. Se propone un caso reproducible de combate que conserve el comportamiento de los enemigos clásicos y separe los efectos de impacto, sangre y los faltantes del pelotón. La hipótesis siguiente debe reducir la alternancia, conservar las publicaciones HD anteriores y mantener la recuperación clásica.

Registro local `%LOCALAPPDATA%/Temp/OpenFodder-P1-EnemigosClasicos-hibrido-20261116-123933.log`, SHA-256 `5843cd3e18b51b6558b8eadffeb79b68ae45d0eb8afbc942fa6866d4b88b951b`. Desde el directorio de la prueba, ejecutar `python -B analizar-combate-enemigos-clasicos.py <directorio> <registro-manual>`. SHA-256 del script `069db9b3c06c556e219d3938a7e3d2ecf7517621a8fbdd6280b424f6edcb6795`.

**Caso de combate fijado y comprobado.** `python -B check-combate-p1-replay.py classic-enemies/replay/classic-enemies/engine.log` verifica los diez pares HD→clásico, sus causas y las 13 rachas de hasta tres publicaciones. Comprueba los 1.546 estados del fichero de traza de la fase. Ventanas de referencia: 1436→1438 (impacto), 1493→1495 (sangre), 2014→2016 (jugador), 4801→4803 (jugador, granada y sombra) y 7229→7231 (impacto y sangre). Se reprodujo la comprobación con los registros retenidos. SHA-256 del script `f6ec1ca2856afde1f296325fbeeb812c1334edcf695cb2421d1516f07b8873f8`.

### Búsqueda de un ajuste de combate

Sobre `4d57eb2` se evaluaron los doce dibujos auxiliares (tipo, hoja y frame) que aparecían en los retornos o eran el único faltante con algún jugador HD disponible. Se añadió el caso potencialmente transparente jugador `0x7C/F1`, condicionado a verificar cero escrituras. Se probaron todas las combinaciones no vacías (8.191). Para cada una se recorrió la secuencia completa de los dos registros conservando las publicaciones existentes. Un intento solo ganaba HD cuando quedaba al menos un jugador con reemplazo y la combinación despejaba todos sus faltantes. Se volvieron a contar los cambios del mismo actor y las rachas de uno a tres fotogramas. Esto mide el efecto proyectado de admitir dibujos ya validados y no prueba que el recurso pase el contrato.

| Muestra | Caso | Publicaciones HD | Retornos con el mismo soldado | Rachas HD cortas |
| --- | --- | ---: | ---: | ---: |
| Replay fijado | Prototipo observado | 2.905 | 10 | 13 |
| Replay fijado | Sangre tipo 23/0x96, F0–F3 | 2.989 | 9 | 11 |
| Partida manual | Prototipo observado | 5.178 | 9 | 24 |
| Partida manual | Sangre tipo 23/0x96, F0–F3 | 5.295 | 11 | 35 |

Treinta y dos combinaciones reducen ambas métricas de continuidad en el replay, todas incluyen las cuatro poses de sangre. Ninguna reduce ambas métricas en los dos registros. La combinación mínima aporta 84 publicaciones HD al replay, pero en la partida elimina pocos cortes y crea más tramos cortos. Los estados del pelotón con dibujo visible sin HD quedaron fuera de la simulación. La versión que Miguel probó sigue como referencia.

**Siguiente paso.** Preparar una segunda muestra reproducible de combate con datos públicos que cubra impacto, sangre y una pose faltante del pelotón. Comparar cada propuesta con su control sobre la misma secuencia. Para avanzar se exige conservar las publicaciones previas y reducir los cambios por actor y las rachas cortas en las muestras reproducibles, con el registro manual como contraste. La implementación y la nueva valoración jugable quedan pendientes.

**Reproducción local.** En el directorio de la prueba ejecutar `python -B buscar-ajuste-combate.py <registro-manual> --include-noop`. Usa los registros y lectores de la prueba anterior. SHA-256 del script `397b5245ba0a5971ada13362188092975905889df73d73bff8266ac42f710fce`.

### Muestras adicionales de combate

Se ejecutó el replay público M1P3 a 12× con enemigos clásicos en una copia diagnóstica del binario que selecciona esa fase. El modo publicado mantiene su límite M1P2. Se conservaron el fichero público M1P3 y el manifiesto de 333 vínculos. **PASS** de los 1.710 estados H3 fijados. Se observaron faltantes de impacto, sangre y jugador. La cobertura del pelotón resultó baja (145/5.046 publicaciones), con tres retornos distintos de los causados por el impacto o la sangre y ninguna racha de hasta tres publicaciones. Para la comparación se exige mantener ese cero y disminuir los retornos.

En una copia local independiente de la entrada pública M1P2 se desplazó el primer disparo cuatro ticks de entrada. Se conservaron las semillas y los ficheros fijados. La variante terminó con `Phase Failed` y queda como tramo diagnóstico, sin equipararlo a un replay de fase completo o a un nuevo PASS de H3. Registró 2.889 publicaciones, diez retornos del mismo soldado y diez rachas cortas. La comparación complementaria incluye la sangre y los estados de caída que aparecieron en ese tramo.

| Muestra adicional | Control, HD / retornos / rachas cortas | Sangre 0x96, proyección |
| --- | ---: | ---: |
| M1P3 público | 145 / 3 / 0 | 178 / 3 / 0 |
| Tramo M1P2 con disparo desplazado | 2.889 / 10 / 10 | 2.968 / 12 / 10 |

Ninguna de las 8.191 combinaciones mejora ambas métricas en el replay original y en alguna de las dos muestras adicionales. Se conserva el motor publicado. Los dos enfoques diagnósticos no justifican otra prueba manual del mismo binario.

**Recuperación local.** Ejecutar `python -B comparar-dos-replays-combate.py <registro-manual> <registro-adicional>`, en el directorio de la prueba. SHA-256 del script `f332580a27a202ef972fbc8c7bee2904f5dcce9af141747069b9e387cb7e1505`. Registros: `combate-m1p3/replay/classic-enemies/engine.log` (SHA-256 `3fd92c2ba806bbd49adbed7b54b118e515e33a3ae2e77fca833e65be232dcb01`) y `combate-m1p2-disparo/run1/classic-enemies/engine.log` (SHA-256 `5400e10e3093816b60e6ae49d03cc47877676352ef4e0a6e34c1230587982b99`). La copia M1P2 se prepara con `combate-m1p2-disparo/desplazar-disparo.py`, aplicado a una copia nueva del fichero público.

### Escrituras en la vista durante el combate

Una copia diagnóstica de `WindowHD.cpp` contó las escrituras del raster nativo recortado de cada comando faltante y su intersección con el rectángulo fuente de SDL. Cada comando se cruzó por intervalo, orden y clave. Se comprobó que el replay mantiene los intentos, comandos, decisiones de publicación, métricas de continuidad y los 1.546 estados H3 de M1P2. El recuento mide escrituras que entran en la vista y puede incluir píxeles tapados por dibujos posteriores.

En los diez retornos fijados hay al menos un faltante que escribe dentro de la vista. Impacto y sangre emiten seis escrituras visibles por comando en esos casos. El jugador emite 60 para `0xB3/F0` y 66 para `0x0B/F0`. En el retorno que combina jugador, granada y sombra, la granada `0x7C/F0` emite cero escrituras y la sombra emite siete dentro de la vista.

De los 5.116 comandos faltantes del replay, 471 no emiten escrituras y 140 solo escriben fuera de la vista. Admitir todos esos casos, con el orden de dibujo original, proyecta 2.925 publicaciones HD frente a 2.905. Los retornos por actor suben de diez a 16 y las rachas de uno a tres fotogramas suben de 13 a 19. La hipótesis no cumple el criterio de continuidad. Las proyecciones exploratorias de cubrir estados visibles del pelotón y efectos tampoco muestran un beneficio repetible que justifique una ampliación aislada.

**Punto de decisión.** Conviene definir un tramo de combate con cobertura coherente de los estados del pelotón y efectos visibles, verificable de principio a fin, antes de considerar otra familia artística o una ampliación del compositor. El modo opt-in publicado sigue como referencia. La revisión visual de una nueva versión queda pendiente de una mejora medible.

**Reproducción local.** Desde el directorio de la prueba, ejecutar `python -B check-combate-visibilidad.py combate-visibilidad/replay/classic-enemies/engine.log`. El log se generó con `validate-combate-visibilidad.py` y la copia diagnóstica en `combate-visibilidad/project/WindowHD.cpp`. SHA-256 del log `7462a75733a03b8fd46bba8996aa14095e9996e2f393e44c0e140036d32a794c`, del verificador `dd0c210b8d94d39bc412229d82ad3d7396ce726b6f87a82834ae74f022190842`.

### Tramos de combate completos

Con el alcance autorizado por Miguel se agruparon los faltantes desde cada retorno hasta la siguiente publicación HD. Cuatro encuentros comparten los mismos nueve dibujos: impacto tipo 6/0x96 F0–F3, sangre tipo 23/0x96 F0–F3 y sombra de jugador tipo 22/0x97 F0. Los primeros censos por recurso aislado omitían los frames F1–F3 de impacto porque siempre aparecían con otros faltantes. Se reconstruyeron las nueve claves del registro a partir de la tabla y los bytes originales y se verificaron los nueve rasters con el renderizador nativo. La copia diagnóstica usó nueve vínculos `keep-associated` y el mismo arte, en el orden nativo del compositor.

| Encuentro por intentos | HD previo / llamadas de presentación | HD con el grupo / llamadas |
| --- | ---: | ---: |
| 1436–1537 | 5 / 50 | 50 / 50 |
| 4317–4470 | 5 / 74 | 74 / 74 |
| 5555–5706 | 2 / 71 | 71 / 71 |
| 7148–7223 | 2 / 35 | 35 / 35 |

Se compararon los dos manifiestos con el mismo binario diagnóstico. El verificador cruza cada retorno de `TryRenderMissionHD` con su resultado de cobertura y cuenta también las 86 llamadas sin censo. Las dos pasadas hacen las mismas 4.640 llamadas y conservan los 1.546 estados H3. El grupo conserva las 2.905 publicaciones previas y añade 281. Los retornos con el mismo soldado que se pueden atribuir por identidad bajan de diez a siete. En las llamadas reales se eliminan las tres rachas de uno a tres fotogramas HD, y la mayor pasa de 1.074 a 1.317 publicaciones. Cada uno de los cuatro encuentros da HD en todas sus llamadas. El número serial también se usa fuera del censo y puede saltar entre dos presentaciones HD consecutivas, por lo que el recuento basado en sus huecos es conservador. La partida manual archivada no registra todas las llamadas y queda como contraste, sin inferir la duración real de sus rachas.

**Siguiente paso autorizado.** Integrar el grupo en el modo opcional existente de M1P2 mediante el contrato de procedencia y conservar vinculaciones explícitas, enemigo clásico y recuperación ante fallos. Repetir control y candidato con registro completo de presentaciones, H3, pruebas focalizadas y CI pertinentes. La compilación diagnóstica no se entrega para jugar.

**Recuperación local.** En `combate-tramo`: `reconstruir-tramo.py`, `preparar-manifiesto.py`, `check-tramo.py` y `check-presentaciones.py`. Este último recibe `replay-calls/control/engine.log` y `replay-calls/classic-enemies/engine.log`. SHA-256 de esos dos registros `6d10204a81219f599e4958d98382e983c645f1d661a1c624ec744558337a76de` y `1e03949624974ab9362392bfbdc93576d528ce279932c2cb86578108143ed232`. SHA-256 del verificador `f7e2a1a9e415125f1f74ee4c55a2c972d5e7bc9ca7778fae90639b1c4ffee9fb`.

### Grupo de combate integrado

En el modo opcional de enemigos clásicos de M1P2, los nueve dibujos de impacto, sangre y sombra que carecen de vínculo pasan el contrato de procedencia Amiga8 antes de conservarse en clásico. Se mantiene la precedencia de los vínculos explícitos para estos efectos y la recuperación ante fallos de datos o SDL.

- **PASS replay con el manifiesto original:** 3.186 publicaciones HD (281 adicionales), siete retornos con el mismo soldado (antes diez), cero rachas HD de uno a tres fotogramas (antes tres). Las cuatro secuencias tienen 50/50, 74/74, 71/71 y 35/35 publicaciones HD. El recuento de 4.640 llamadas del motor coincide con el diagnóstico anterior y conserva los 1.546 estados lógicos de la fase.
- **PASS pruebas focalizadas:** Windows H3, 11 fases y 11.361 estados fijados. WSL con ASan/UBSan/LSan, métodos reales de Window y SDL software a 8×/12×, conservación de efectos en su orden, rechazo de procedencia ausente, offset, identidad, bytes y recorte incorrectos, más recuperación íntegra ante fallo SDL. Pasaron los 42 tests Python.
- **PASS CI completa** de `05bd05b` en Windows y Linux. [Windows](https://github.com/Cacheirez/openfodder/actions/runs/43880617284) · [Linux](https://github.com/Cacheirez/openfodder/actions/runs/43880617302).
- **PENDIENTE:** valoración jugable, GPU, CD32, audio y campaña manual completa.

**Reproducción local.** `validate-grupo-combate.py <directorio-nuevo>` usa el binario de `combate-grupo/h3-build/Release`. La variante diagnóstica `validate-grupo-presentaciones.py` conserva la lógica integrada y añade el recuento de cada llamada. Sus resultados se contrastan con `combate-tramo/check-presentaciones.py`. SHA-256 del registro instrumentado `b308749543a254ac360228e7e49c5a1119335cf5135cd7ac4f2931d9e8f6cef2`.

### Revisión jugable del grupo de combate

En PowerShell:

```powershell
& 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1da6a-54a2-7270-8fa9-5eb4a351446f/Probar-P1-Combate.ps1'
```

Amiga The One M1P2 a 12×, híbrido con enemigos clásicos, SDL software y sin sonido. El ejecutable, el manifiesto y las dependencias se comprobaron con `-Comprobar`.

### Resultado jugable del grupo de combate

El 16-11 Miguel observó un cambio breve a clásico al superar un obstáculo durante la primera parte. En la parte final vio a los soldados en clásico prácticamente todo el tiempo, con el pelotón a la derecha de la pantalla. **Continuidad jugable no aceptada.**

- El verificador `tools/modernization/ordered_soldier_coverage.py` validó 9.753 intentos y 97.813 comandos sin registros incompletos: 6.741 publicaciones HD y 3.012 rechazos por variantes ausentes. El censo no incluye todas las llamadas de presentación ni registra coordenadas, por lo que la posición a la derecha y el momento del obstáculo quedan como observaciones de Miguel. Las primeras interrupciones registradas incluyen hojas del jugador `0xB0–0xB2/F0`.
- Los tramos de 721, 387 y 1.331 rechazos desde los intentos 12881, 14541 y 17880 comienzan con el tipo 27 `0x9E/F0` como único faltante, mientras siguen presentes cuatro, tres y un jugador HD del intento anterior. El tipo 27 corresponde al soldado muerto flotando. En el tramo final es faltante en los 1.331 intentos. En 963 es el único faltante y hay un jugador con sustitución HD disponible. En toda la partida se cumplen esas dos condiciones en 1.960 intentos. Es un máximo proyectado y queda pendiente verificar el dibujo nativo y las transiciones resultantes.
- Se observaron dos claves del tipo 27: `75d5c70c84d90a5d6db937d8bd8c2b76a89dad53d9cbca5a228a0fad32ec3566` y `67e7d8c379701379772ff97144f098afb25b9cb6e148f8326f428d554ad9331e`. El registro permanece local en `%TEMP%\OpenFodder-P1-Combate-hibrido-20261116-185238.log` (SHA-256 `c1bbdce79d192f95418a3d9d30e474e37cda7b8615a7d27a941c71b4e71deede`).

### Soldado muerto flotando conservado en orden

El híbrido opt-in de Amiga The One M1P2 conserva el tipo 27 `0x9E/F0` con la procedencia del dibujo original. La fila F0 de `stru_8DC98` usa el segundo segmento, offset 6566, dos columnas, diez filas y desplazamiento cero. La validación de recurso y el compositor aplican las comprobaciones de identidad, paleta, recorte y orden ya usadas por el grupo de combate. El modo estricto del replay conserva sus 1.368 publicaciones y 3.186 faltantes.

- **PASS focalizado** en WSL con ASan/UBSan/LSan a 8×/12×. El fixture de Window con SDL software conserva la escritura nativa entre dos soldados HD, rechaza procedencia o geometría alterada y recupera la imagen clásica completa tras un fallo de SDL.
- **PASS replay público:** 3.186→3.997 publicaciones HD, 7→8 retornos con el mismo jugador y cero rachas de uno a tres, usando la secuencia instrumentada existente de 4.640 llamadas, emparejada por intento con la nueva ejecución. Se conserva cada publicación anterior y los 1.546 estados lógicos. El nuevo registro tiene SHA-256 `214afe3e8bff737c72ab2d74b3f14e68fae45575ee61ca71205e52f42730dfd0`.
- **PASS comparación del tramo con disparo desplazado:** sobre el mismo corte diagnóstico que termina sin superar la fase, 3.098→3.856 publicaciones HD, 9→10 retornos con el mismo jugador y cero rachas de hasta tres intentos HD. Coincide la traza de 1.500 estados entre ambos binarios. Se ejercitaron las dos claves observadas en la partida. SHA-256 del nuevo registro `f418b57fc8653a178f769e5075d8b64f2afe7e8e672bbab3b46a37fab4f56058`.
- **Proyección sobre la partida de Miguel:** 6.741→8.701 publicaciones HD y 963 adicionales en los 1.331 intentos finales. Quedan 34 retornos con el mismo jugador y 15 rachas de hasta tres intentos HD. La proyección se aplica al censo existente. Persiste el riesgo de retornos por poses faltantes del jugador u otros dibujos.

**Recuperación local.** En `C:/Users/migue/.codex/visualizations/2026/11/16/01a1e578-b4e6-7bc2-add9-1f79c31a6e09/` están `proyectar-soldado-flotante.py`, `validar-flotante-wsl.sh`, los registros de `flotante-replay` y `flotante-replay-disparo`, y el ejecutable `flotante-build/Release/native_probe.exe`. El lanzador local `Probar-P1-Flotante.ps1` comprueba el hash del ejecutable y reutiliza los datos y el manifiesto de la revisión anterior.

- **PASS H3 completo en Windows:** las 11 fases y los 11.361 estados canónicos coinciden con la referencia fijada. Evidencia local en `flotante-h3-pc` y `flotante-h3-amiga`.
- **PASS CI focalizada de `52e12f2`:** CTest y A2 con H3 original. El resto de las ejecuciones completas queda pendiente al cerrar este relevo. [Windows](https://github.com/Cacheirez/openfodder/actions/runs/43925846079) · [Linux](https://github.com/Cacheirez/openfodder/actions/runs/43925846329).

### Revisión jugable del soldado flotante

```powershell
& 'C:/Users/migue/.codex/visualizations/2026/11/16/01a1e578-b4e6-7bc2-add9-1f79c31a6e09/Probar-P1-Flotante.ps1'
```

Lanzador comprobado con `-Comprobar`. Al jugar, anotar si los supervivientes conservan el HD en la parte final, especialmente con el pelotón a la derecha como en la partida anterior. Si hay retornos breves, indicar en qué situación aparecen y aportar la ruta del registro. Aceptación jugable, GPU, CD32, audio y campaña manual completa quedan pendientes.

### Resultado jugable y poses del pelotón

El 16-11 Miguel percibió menos cambios a clásico. Señaló saltos desde altura, cruces de río y encuentros directos con enemigos, estos últimos con menor frecuencia. El verificador validó 9.544 intentos y 92.275 comandos: 7.852 publicaciones HD, 1.605 rechazos por variantes ausentes y 87 sin cuerpo sustituible. La anterior partida registró 6.741 publicaciones de 9.753 intentos y 34 retornos con el mismo jugador. Son recorridos manuales distintos.

- **Caída:** diez de los 23 retornos empiezan con una pose del jugador `0xB0/F0`, `0xB6/F0` o `0xB7/F0` como faltante. `Sprite_Update_Direction_Anim` selecciona esta familia al caer. `0xB0/F0` explica cinco retornos y es observable en el replay de disparo desplazado. Cubrir solo ese frame proyecta 30 publicaciones más, 23→18 retornos y 3→1 rachas HD de hasta tres intentos. Cubrir las tres poses observadas proyecta 23→13 retornos y conserva una racha breve.
- **Agua:** siete retornos empiezan con poses de nado del jugador de la familia `0x18–0x1F`. Las 14 poses observadas bloquean 783 intentos sin otros faltantes. Cubrirlas proyecta 765 publicaciones más, 23→18 retornos y 3→2 rachas HD breves. Es un alcance artístico mayor que el piloto de caída.
- **Combate:** hay un enemigo en la escena al inicio de siete retornos. Las 15.226 órdenes de enemigo y 4.244 de soldado flotante quedaron resueltas en clásico dentro del compositor. En 22 de los 23 retornos iniciales faltan exclusivamente poses del jugador. El otro mezcla una pose del jugador y dos dibujos asociados. Admitir hipotéticamente todos los faltantes de entidades distintas al jugador sumaría 189 intentos HD y conservaría los 23 retornos y las tres rachas breves.

Las proyecciones retienen la secuencia de intentos y solo suman publicaciones cuando todos los faltantes pertenecen al grupo evaluado y el intento ya tiene alguna sustitución. El registro carece de coordenadas y de las llamadas excluidas del censo. Las rachas son de intentos registrados. La mejora percibida corresponde a Miguel. La aceptación jugable del pelotón sigue pendiente.

**Recuperación.** Registro local `%TEMP%\OpenFodder-P1-Flotante-hibrido-20261116-192458.log`, SHA-256 `acbc1791699ac656010b424aa279e6b666b26c4202422660542b1ca34900d1e1`. Para volver a medir, validar el censo y agrupar las transiciones de publicado a rechazado por escena, ranura y generación del jugador. El replay de disparo desplazado en `flotante-replay-disparo` contiene tres intentos con `0xB0/F0` ausente.
