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
