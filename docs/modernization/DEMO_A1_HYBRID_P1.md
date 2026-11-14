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

CI Windows/Linux del commit, GPU, CD32, audio, campaña manual y aceptación visual/jugable **PENDIENTES**.

La primera CI Linux de `c4dfbfc` pasó el bloque CTest que contiene el caso híbrido. El paso posterior de productores falló porque el recurso sintético omitía la paleta usada en su dibujo. Se sincronizó la paleta en las pruebas de productores y poses. Ambos contratos pasaron después en WSL con ASan/UBSan/LSan. La CI del ajuste queda pendiente.
