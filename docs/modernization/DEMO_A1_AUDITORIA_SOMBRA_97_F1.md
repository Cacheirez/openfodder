# A.1 — Auditoría de la sombra del soldado 0x97/F1

13 de noviembre de 2026. Entrada `72ecd0f08530de6149b9346951af70afda412598`. Sesión `interactive-check-02`, Amiga The One, misión 1, fase 2 (Find Grenades). [Evidencia de sesión](evidence/demo-a1-interactive.json).

## Recuento frente a 328 vínculos

Se verificaron el tamaño y el SHA-256 del log, el manifiesto histórico de 322 vínculos y el candidato de 328 (SHA-256 `6c0298c134ed77611906d69d4f8010cee70cfdaf7e6babfdf3c64234feeea1ce`). El candidato conserva los 322 vínculos históricos y añade seis. Los comandos reproducen los 4.456 resultados registrados a 12× (92 publicaciones HD y 4.364 rechazos). Frente al candidato, **4.279 intentos quedan sin claves faltantes**, 177 conservan faltantes y se cuentan 38 claves residuales.

`c7fcc929ce1739035307df6e6b084f2a5d05dea74dba4ec2c8487cf3cdef04e1` es el **único faltante en 21 intentos** y aparece en **69**. Se registró un comando de esta clave por intento, en la escena 186, entre los intentos 4824 y 5028. En el intento 4988 (intervalo 4987, ocho comandos), el log marcó como faltantes la sombra, la insignia F4 y la muerte enemiga 0x71/F1. El candidato resuelve las dos últimas. Añadir la clave de la sombra dejaría **4.300 de 4.456 intentos históricos sin claves faltantes (96,50 %)**.

## Identificación nativa

- `eSprite_Player_Shadow` (tipo 22). `Sprite_Handle_Player_Shadow` selecciona 0x97/F1 y usa F0 cuando la altura del propietario supera 8. La rama válida coloca la sombra respecto al propietario, con desplazamiento adicional de `mHeight >> 2` en ambos ejes, +5 en X y −3 en Y. [Tipo](../../Source/Sprites.hpp) · [Manejador](../../Source/Sprites/Sprite_Troop.cpp).
- La tabla `mSpriteSheetTypes_InGame_Amiga_TheOne` selecciona `stru_8DB38`. F1 está en `eGFX_IN_GAME2`, offset 2750, dos palabras en la tabla, cuatro filas y modificadores (0, 0). Recurso Amiga8 decodificado de 320 × 256, cuatro planos, SHA-256 `3dd8d73e4700b42f081f25b25b547b5bd76c9124580ecbd5e01729527e9d8f11`. Persona, animación, vehículo, destrucción y paletas efectivas de recurso y dibujo tienen valor 0 para la clave auditada. [Tabla Amiga](../../Source/Amiga/SpriteData_Amiga.hpp).
- Python reprodujo primero la clave de referencia 0x95/F0 a partir de su snapshot conservado y calculó después la clave exacta de 0x97/F1 con la geometría de la tabla y el mismo recurso y paleta. El renderizador nativo C++ confirmó la clave y generó un raster de 16 × 4 con 24 píxeles visibles, SHA-256 RGBA `6ef0fa8d3314f5bf7355c67d5d50be634a1ba5b88a17bd3b06913904f56c763e`. [Cálculo del motor](../../Source/Utils/SoldierVariant.hpp) · [Renderizador](../../tools/modernization/render_walk_native.cpp).

La auditoría confirmó el recuento histórico y la identificación nativa. La cifra proyectada mide exclusivamente la resolución de claves sobre el log histórico.

## Recuperación local

Directorio `C:/Users/migue/.codex/visualizations/2026/11/13/01a1d620-0623-74b3-9cf0-ae2d8f4454fb`. Ejecutar `python -B verify_residual_328.py <checkout> <a1> <candidato328/candidate-manifest.json> <renderer.exe>`. Usar el árbol `a1` del [Arranque rápido](CONTINUIDAD.md), su carpeta `snapshots`, el [candidato de 328 vínculos](DEMO_A1_AUDITORIA_MUERTE_ENEMIGA_71_F1.md#reproducción-de-la-integración) y el [renderizador de F4](DEMO_A1_AUDITORIA_RANGO_F4.md#recuperación-local). El script obtiene el log de la evidencia de sesión y genera el snapshot derivado, el raster y el resumen.

| Archivo | SHA-256 |
|---|---|
| `verify_residual_328.py` | `1eb996d7e4e9f1f3dc05f24e63ca403170928cd331bb0a8ef0e603e167f91eb8` |
| `player-shadow-97-f1-derived.json` | `6bf07611a99fa111a09b4ed7a7f7f53780b54bd0a2f43ec061a7db22f21109f2` |
| `player-shadow-97-f1-verification.json` | `95f33e318658e0d83163d01ea049ddb49b5e564c50f9151d6b33719165665da6` |

## Integración y comprobación

13 de noviembre de 2026. El candidato de 329 vínculos añade únicamente 0x97/F1 como `keep-associated` al candidato anterior. Conserva sus 328 vínculos en orden y sus 166 activos byte a byte. El nuevo manifiesto tiene 321 reemplazos y ocho asociados. SHA-256 del manifiesto Windows `2e4d729710692c77ba0461d196099f12c469b00617a6d8dfd4cdb28c15974caf`.

- En el log histórico quedan **4.300 de 4.456 intentos sin claves faltantes (96,50 %)**, 156 con faltantes y 37 claves residuales. La primera por número de intentos como único faltante es `d615161944fbf97e9e07f29f4de6849c927c0d4e20087cbb981ec3c73e11dc45`, tipo 5, hoja 0x71, F1, con 15 intentos como único faltante y 18 apariciones. La identificación nativa de esta variante está pendiente.
- SDL software Windows x64, Clang 23.1.5, SDL 3.4.0 y ASan/UBSan **PASS** a 8× y 12×. En cada densidad, la sombra aporta 24 escrituras clásicas, cubre una celda HD anterior, queda cubierta por el último cuerpo en 22 y permanece visible en dos. Se cotejaron las 12 escrituras tras recortar dos filas y la salida SDL completa. Una clave de sombra sin resolver provoca retorno íntegro a clásico y la clave exacta recupera HD.
- Regresiones de F4, tejado, caja, 0x59/F0, 0x45/F1 y la variante de 0x71/F1 ya integrada **PASS**. El mismo fixture **PASS** en MSVC x64 con C++14. Aceptación jugando, GPU, audio, CD32, LSan, H3 y cobertura restante **PENDIENTES** en este bloque.

### Reproducción de la integración

Ejecutar `python -B tools/modernization/prepare_demo_a1_manifest.py --base <verde-A>/qa-rocket-native/art/candidate-manifest.json --out <evidencia>/candidate --with-player-shadow`. La evidencia se conserva en `C:/Users/migue/.codex/visualizations/2026/11/13/01a1d627-114c-7c40-a480-0916c41b9eb0`. Allí, `prepare_shadow_input.py <checkout> <integracion-71> <auditoría-sombra> <evidencia>` contrasta los candidatos, recalcula el residual y añade el snapshot auditado al fixture anterior. Usar [la integración anterior](DEMO_A1_AUDITORIA_MUERTE_ENEMIGA_71_F1.md#reproducción-de-la-integración) y [el snapshot de auditoría](#recuperación-local). Ejecutar `run_enemy.ps1 <checkout>` con ASan/UBSan o `run_enemy_msvc.ps1 <checkout>` con MSVC.

| Archivo | SHA-256 |
|---|---|
| `prepare_shadow_input.py` | `bc3b4f220c0c1ab5ee2c5eb613e4d9b62bc5ee91c988ee34edf391e28dc528b3` |
| `fixture-run.log` | `76d717b7828190bbe9791363e4eb47cd0a17964deb9d924b4a82d8a672cb35c4` |
