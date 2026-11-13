# A.1 — Auditoría de muerte enemiga 0x71/F1

13 de noviembre de 2026. Entrada `8554ba154586f8db8fd350e0399b38f3e7d942cb`. Sesión `interactive-check-02`, Amiga The One, misión 1, fase 2 (Find Grenades). [Evidencia de sesión](evidence/demo-a1-interactive.json).

## Recuento contra 327 vínculos

Se verificaron tamaño y SHA-256 del log, el manifiesto histórico de 322 vínculos y el candidato de 327 (SHA-256 `160af5ec803ff1d0ba1bbdbac8a6a92aefda04a3542beea22d4d310f243eadaf`). Coinciden los 322 vínculos históricos y se identificaron los cinco añadidos. Los comandos cuadran con los 4.456 resultados históricos a 12× (92 publicaciones HD y 4.364 rechazos). Contra el candidato quedan **4.267 intentos sin claves faltantes (95,76 %), 189 con faltantes y 39 claves residuales**.

La clave `f06b98d0debe93b676cd17ba89a9b76e2b91484a08507c83e8d66215dc8237fb` es el único faltante en **12 intentos** y aparece en **33**. Sus 33 comandos son de la ranura 21, generación 162 y escena 186, entre los intentos 4988 y 5076. En el intento 5036 (intervalo 5035) hay siete comandos. El log marcaba como faltantes la insignia F4 y 0x71/F1. El candidato resuelve F4. Resolver también 0x71/F1 dejaría 4.279 intentos históricos sin claves faltantes (96,03 %).

## Identificación nativa

- Enemigo tipo 5, persona IA (1), hoja 0x71, segundo fotograma (F1), estado `eSprite_Anim_Die2` (6), fuera de vehículo y sin destrucción pendiente. Es la dirección de índice 7 del tramo «Death-2 Anim» en `mSprite_AnimationEnemyPtrs`. La rama `Die2` selecciona ese tramo mediante `(Data8 + 0x20) / 2` y aplica módulo 2 al índice de fotograma. [Tabla](../../Source/Sprites.cpp) · [Selector](../../Source/Sprites/Sprite_Troop.cpp).
- Amiga8, tabla `stru_8D418`, segmento `eGFX_IN_GAME`, offset 8406, cuatro planos, dos palabras en tabla, 14 filas, anclaje (0, 0) y paletas de recurso y dibujo 0. El recurso decodificado de 320 × 336 tiene SHA-256 `7a44b4a6dafa1350da974825ea1e2028fd5d3d946f415781966ea1cadc9bb134`. [Tabla Amiga](../../Source/Amiga/SpriteData_Amiga.hpp).
- El cálculo independiente en Python verificó el recurso y la paleta contra los snapshots conservados, reprodujo la clave de referencia y obtuvo la clave exacta del log para 0x71/F1. El renderizador nativo C++ confirmó la clave y generó un raster de 16 × 14 con 51 píxeles visibles y SHA-256 RGBA `9c69e3e0f4a672776be46a0f90d7acccf6629e74d9361236d5d82d81f8cedfbf`. [Cálculo del motor](../../Source/Utils/SoldierVariant.hpp) · [Renderizador](../../tools/modernization/render_walk_native.cpp).

La auditoría reutiliza el renderizador existente y mide la cobertura del registro sobre el log histórico. La comprobación del reemplazo HD figura en [Integración y comprobación](#integración-y-comprobación).

## Recuperación local

Directorio `C:/Users/migue/.codex/visualizations/2026/11/13/01a1d60e-bb33-7a93-a487-d5b1cfb905af`. Ejecutar `python -B verify_residual_327.py <checkout> <a1> <candidato327/candidate-manifest.json> <renderer.exe>`. Usar el árbol `a1` del [Arranque rápido](CONTINUIDAD.md), el [candidato de 327 vínculos](DEMO_A1_AUDITORIA_MARCHA_ENEMIGA_45_F1.md#reproducción) y el [renderizador conservado de F4](DEMO_A1_AUDITORIA_RANGO_F4.md#recuperación-local) con su carpeta `native-snapshots`. El script localiza el log mediante la evidencia de sesión y genera el snapshot, el raster y el resumen.

| Archivo | SHA-256 |
|---|---|
| `verify_residual_327.py` | `206e0f029f0fb251b5675e1c8f1e184bd290a083308de214b0b7123eeab6dc72` |
| `enemy-death-71-f1-derived.json` | `7dedc7d8851f0f8f9a8e223af0ea4af9a073ee267acbcabdfc47219807702cbb` |
| `enemy-death-71-f1-verification.json` | `61178c4f72836a6de35d67a1bd92ce4994913abc1d159b71c08816e329e2651f` |

## Integración y comprobación

13 de noviembre de 2026. Maestro RGBA de 1.341 × 1.173 generado con ImageGen integrado, con la pose nativa como referencia de geometría y C01 verde A y 0x59/F0 como referencias de estilo y uniforme. Se revisaron internamente casco, torso, pierna hacia la izquierda, mano a la derecha y encaje en el lienzo a 8× y 12×. [Maestro, derivados y manifiesto](../../assets/modernization/demo-a1-enemy-death-71-f1/).

- Candidato con 166 activos y 328 vínculos (321 reemplazos y siete asociados). Se cotejaron en orden los 327 vínculos anteriores y byte a byte sus 164 activos. Solo se añadió el vínculo exacto de 0x71/F1. SHA-256 del manifiesto Windows `6c0298c134ed77611906d69d4f8010cee70cfdaf7e6babfdf3c64234feeea1ce`.
- SDL software Windows x64, Clang 23.1.5, SDL 3.4.0 y ASan/UBSan **PASS** a 8× y 12×. Seis cuerpos, 30 celdas con oclusión sobre una capa anterior y 44 modificadas por el cuerpo posterior en cada densidad. Quedan 66 y 65 celdas con aportación visible del enemigo, respectivamente. Comparación de píxeles tras recortar cinco filas, retorno a clásico ante una clave faltante y recuperación HD al restaurarla. Regresiones 0x59/F0, 0x45/F1, caja, tejado y F4 **PASS**.
- La CI Windows de `a0343de` detectó dos desestructuraciones preexistentes en el fixture, que se compila como C++14. Se sustituyeron por acceso a los pares de la tabla. La repetición local con MSVC x64 en C++14 y SDL 3.4.0 dio **PASS** a 8× y 12×, con el mismo resultado y el mismo hash del log.
- Al recalcular el log histórico quedan 4.279 de 4.456 intentos sin claves faltantes (96,03 %), 177 con faltantes y 38 claves residuales. La siguiente por número de intentos como único faltante es `c7fcc929ce1739035307df6e6b084f2a5d05dea74dba4ec2c8487cf3cdef04e1`, tipo 22, hoja 0x97, F1 (21 como único faltante y 69 en total). Identificación nativa PENDIENTE.
- Aceptación jugando, GPU, audio, CD32, LSan y cobertura restante PENDIENTES.

### Reproducción de la integración

Maestro SHA-256 `c091f9328fcdcafb0bdb4b4a0b68120bc830de71420a9438ac8e7bb1c985928d`. Con Pillow 11.3.0, recortar a la caja alfa ≥ 128, `(317, 161, 1139, 880)`. Redimensionar con Lanczos a `(10*d, 9*d)` y pegar sin máscara en `(4*d, 2*d)` sobre el lienzo transparente RGBA de `(16*d, 14*d)`. Se reprodujeron byte a byte ambos PNG, sus RGBA y el [manifiesto](../../assets/modernization/demo-a1-enemy-death-71-f1/manifest.json).

Ejecutar `python -B tools/modernization/prepare_demo_a1_manifest.py --base <verde-A>/qa-rocket-native/art/candidate-manifest.json --out <evidencia>/candidate --with-enemy-death`. En el subdirectorio local `integracion-71` del [directorio de auditoría](#recuperación-local), `prepare_death_input.py <checkout> <evidencia-integración-45-F1> <directorio-auditoría-71-F1> <evidencia>` contrasta los candidatos, recalcula el residual y añade 0x71/F1 al fixture anterior. `run_enemy.ps1 <checkout>` ejecuta la prueba SDL con sanitizadores. SHA-256 del log `8bee6c97b65fbcb44ae9141c80b781ffa0e439165702594a2e3a85aec9506218`. El mismo directorio conserva `prompt-imagegen.txt` y `derive_enemy_death.py`.

## Variante residual Hit `d6151619`

13 de noviembre de 2026. Entrada `e4a32a4e431df15b9fd77ee0b8a64f4f7367de51`. Se verificaron los SHA-256 del log `interactive-check-02` y de ambos manifiestos. Los comandos reproducen los 4.456 resultados originales a 12× (92 publicaciones HD y 4.364 rechazos). Frente al candidato de 329 vínculos quedan 4.300 intentos sin claves faltantes, 156 con faltantes y 37 claves residuales. [Evidencia de sesión](evidence/demo-a1-interactive.json) · [Candidato de 329 vínculos](DEMO_A1_AUDITORIA_SOMBRA_97_F1.md#integración-y-comprobación).

- `d615161944fbf97e9e07f29f4de6849c927c0d4e20087cbb981ec3c73e11dc45` aparece en 18 intentos y es el único faltante en 15. Los 18 comandos son de la ranura 21, generación 162, escena 186, entre los intentos 4903 y 4986. El intento 4958 (intervalo 4957, ocho comandos) tenía dos faltantes en el log original. El candidato ya resuelve la sombra 0x97/F1. Añadir la variante `Hit` dejaría 4.315 de 4.456 intentos históricos sin claves faltantes (96,84 %).
- Python y el renderizador nativo C++ confirmaron la clave exacta. Enemigo tipo 5, persona IA (1), `eSprite_Anim_Hit` (1), fuera de vehículo y sin destrucción pendiente. Usa `stru_8D418`, `eGFX_IN_GAME` offset 8406, ambas paletas efectivas a 0. Frente al snapshot de `Die2`, solo difieren la clave y el estado de animación. Los 896 bytes RGBA del raster de 16 × 14 coinciden byte a byte, con 51 píxeles visibles y SHA-256 `9c69e3e0f4a672776be46a0f90d7acccf6629e74d9361236d5d82d81f8cedfbf`. [Tabla Amiga](../../Source/Amiga/SpriteData_Amiga.hpp) · [Estados](../../Source/Sprites.hpp) · [Renderizador](../../tools/modernization/render_walk_native.cpp).

Integración del vínculo con los activos existentes, prueba SDL y aceptación jugando PENDIENTES. La proyección describe la resolución de claves del log histórico.

### Reproducción de la auditoría Hit

Directorio `C:/Users/migue/.codex/visualizations/2026/11/13/01a1d63f-b3e8-7e81-a616-ccf50b3a42cb`. Ejecutar `python -B verify_residual_329.py <checkout> <a1> <candidato329/candidate-manifest.json> <renderer.exe>`. Usar el árbol `a1` del [Arranque rápido](CONTINUIDAD.md), el [candidato de 329 vínculos](DEMO_A1_AUDITORIA_SOMBRA_97_F1.md#reproducción-de-la-integración) y el [renderizador conservado de F4](DEMO_A1_AUDITORIA_RANGO_F4.md#recuperación-local) con su carpeta `native-snapshots`. El script localiza el log mediante la evidencia de sesión. Comparar el raster generado con `enemy-death-71-f1-native.rgba` del [directorio de auditoría Die2](#recuperación-local).

| Archivo | SHA-256 |
|---|---|
| `verify_residual_329.py` | `fd9adfee8c11f7180e75020ec84c2fb482ec453140acd18bb8a1b1eecd6a2edb` |
| `enemy-death-71-f1-d615-derived.json` | `a347bd969d7d0211499faa16b95280c8be2d943b9f108a0e8a1924d9a46c9d3d` |
| `enemy-death-71-f1-d615-verification.json` | `bf885de66c8d84bbf7e88650a53876429cf77457181292436595b008077fa130` |
