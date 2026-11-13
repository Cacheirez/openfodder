# A.1 — Auditoría de marcha enemiga 0x45/F1

13 de noviembre de 2026. Entrada `cf97c05c6c0a64fcd3406c91b0c481b44d2e4ad1`. Sesión `interactive-check-02`, Amiga The One, misión 1, fase 2 (Find Grenades). [Evidencia del log](evidence/demo-a1-interactive.json).

## Recuento contra el candidato

Se verificaron tamaño y SHA-256 del log, el manifiesto histórico de 322 vínculos y el candidato de 326, con SHA-256 `369b2943531860c8d2fbda7a69207d413c66f5de124c47f67bd850ede9507e75`. Los 322 vínculos históricos coinciden y se verificaron los cuatro añadidos. Los 4.456 intentos a 12× cuadran con sus comandos y resultados históricos (92 publicaciones y 4.364 rechazos). Al recalcular los conjuntos de claves faltantes quedan **4.252 intentos sin faltantes (95,42 %), 204 con faltantes y 40 claves residuales**.

La clave prioritaria, `77d34d3f0593010865c1185e626929f4491ff2303b6656397cd640fb0334356a`, es el único faltante en **15 intentos** y aparece en 18. Los 18 comandos corresponden a la ranura 21, generación 162, escena 186, entre los intentos 4675 y 4807. En el intento 4675 (intervalo 4674) hay ocho comandos. El log marcaba como faltantes 0x59/F0 y 0x45/F1, y el candidato actual ya resuelve 0x59/F0. La siguiente clave en el recuento tiene 12 intentos como único faltante y 33 en total. Cubrir 0x45/F1 elevaría el recuento sin faltantes a **4.267 de 4.456 (95,76 %)**.

## Identificación nativa

- `eSprite_Enemy` (tipo 5), persona IA (1), hoja 0x45, frame 1, estado `eSprite_Anim_None` (0), fuera de vehículo y sin destrucción pendiente. 0x45 es la dirección de índice 3 del tramo de marcha en `mSprite_AnimationEnemyPtrs`. [Tabla de animación](../../Source/Sprites.cpp) · [Selector](../../Source/Sprites/Sprite_Troop.cpp).
- Amiga8, `stru_8CE38`, segmento `eGFX_IN_GAME` (0), offset 5620, cuatro planos, paletas de recurso y dibujo 0, 14 filas, dos palabras en la tabla y anclaje (0, 0). Recurso decodificado de 320 × 336, SHA-256 `7a44b4a6dafa1350da974825ea1e2028fd5d3d946f415781966ea1cadc9bb134`. [Tabla Amiga](../../Source/Amiga/SpriteData_Amiga.hpp).
- El cálculo independiente en Python reprodujo primero la clave del snapshot de referencia del recurso y verificó su paleta con la referencia de A.1. Después reprodujo la clave del log para 0x45/F1. El renderizador nativo C++ confirmó la misma clave y generó un raster de 16 × 14 con 72 píxeles visibles, SHA-256 RGBA `289cd896517de5f2376eeac5ac294b6c9c6762c7d174e2bfc6ef41510d4155ee`. El snapshot de la pose se reconstruyó a partir de referencias conservadas. [Cálculo del motor](../../Source/Utils/SoldierVariant.hpp) · [Renderizador](../../tools/modernization/render_walk_native.cpp).

La pose requiere un reemplazo de cuerpo en el registro. Arte, composición SDL, publicación HD efectiva y aceptación jugando quedan PENDIENTES. [Registro](../../Source/Utils/OrderedSoldierRegistry.hpp).

## Recuperación local

Directorio `C:/Users/migue/.codex/visualizations/2026/11/13/01a1d58d-3405-77a1-9dc6-7bd2935c4a8b`. Ejecutar `python -B verify_residual_326.py <checkout> <a1> <candidato326/candidate-manifest.json> <renderer.exe>`. Usar el árbol `a1` del [Arranque rápido](CONTINUIDAD.md), el [candidato de 326 vínculos](DEMO_A1_AUDITORIA_ENEMIGO_TUMBADO.md#reproducción) y el [renderizador conservado de F4](DEMO_A1_AUDITORIA_RANGO_F4.md#recuperación-local) con su carpeta `native-snapshots`. El script localiza el log a partir de la evidencia de sesión y genera el snapshot, el raster y el resumen verificado.

| Archivo | SHA-256 |
|---|---|
| `verify_residual_326.py` | `8fed681504ec311af6874042a8d894bacddff9d8f8080b089c4e450a756e8e8a` |
| `enemy-walk-45-f1-derived.json` | `7baf0cdb1e7a71bc3f0cc5ae5e043e6de0c1d72520a665a3714c1b8712f31b46` |
| `enemy-walk-45-f1-verification.json` | `2e7be279f03357b678423b8ea9faaf651e8449329c73f34f52ee26197224161a` |

## Integración y comprobación

13 de noviembre de 2026. Una pose en estilo C — Pintado moderado. Maestro RGBA de 1.006 × 1.564 generado con ImageGen integrado a partir del raster auditado y el maestro de marcha C01 verde A de dirección 3/F1. Comparativa interna de la orientación, la zancada y el encaje de ambos derivados. [Maestro, derivados y manifiesto](../../assets/modernization/demo-a1-enemy-walk-45-f1/).

- Candidato verde A con 164 activos y 327 vínculos (320 reemplazos y siete asociados). Los 162 activos y 326 vínculos anteriores conservan contenido y orden. La única clave nueva es la auditada de 0x45/F1. SHA-256 del manifiesto generado en Windows `160af5ec803ff1d0ba1bbdbac8a6a92aefda04a3542beea22d4d310f243eadaf`.
- SDL software Windows x64, Clang 23.1.5, SDL 3.4.0 y ASan/UBSan PASS a 8× y 12×. Seis cuerpos en la composición controlada. El enemigo cambia 52 celdas pintadas por capas anteriores en cada densidad y el último cuerpo modifica 66/67 celdas del compuesto. Quedan 83 celdas con aportación visible del enemigo a cada densidad. Se cotejaron los píxeles tras recortar cinco filas. Una clave faltante conserva intacto el destino HD, el retorno coincide con el raster clásico y se recupera HD al restaurar la clave. Regresiones de 0x59/F0, caja, tejado y F4 PASS.
- El recuento del log histórico verificado deja 4.267 de 4.456 intentos sin claves faltantes (95,76 %), 189 con faltantes y 39 claves residuales. La siguiente clave por faltante único y total es `f06b98d0debe93b676cd17ba89a9b76e2b91484a08507c83e8d66215dc8237fb`, tipo 5, hoja 0x71, F1 (12 únicos, 33 totales). Identificación nativa PENDIENTE.
- Aceptación jugando, GPU, audio, CD32, LSan y cobertura restante PENDIENTES. El recuento histórico mide cobertura de claves.

### Reproducción

Maestro SHA-256 `6cf5d1cdc1f6efef6173dac2920c8ed1a6fedab266fc93a079059281b7324bc3`. Con Pillow 11.3.0, recortar el maestro a la caja alfa ≥ 128, `(105, 60, 898, 1483)`. Redimensionar con Lanczos a `(9*d, 14*d)` y pegar sin máscara en `(3*d, 0)` sobre el lienzo RGBA transparente de `(16*d, 14*d)`. Guardar PNG y bytes RGBA en orden de filas. Los SHA-256 de los derivados RGBA figuran en su [manifiesto](../../assets/modernization/demo-a1-enemy-walk-45-f1/manifest.json).

Ejecutar `python -B tools/modernization/prepare_demo_a1_manifest.py --base <verde-A>/qa-rocket-native/art/candidate-manifest.json --out <evidencia>/candidate --with-enemy-walk`. En el [directorio local de evidencia](C:/Users/migue/.codex/visualizations/2026/11/13/01a1d5e1-48ca-7953-a672-6a72c2e00f53), `prepare_walk_input.py <checkout> <evidencia-enemigo-tumbado> <auditoría-45-F1> <evidencia>` contrasta los candidatos, recalcula el residual y amplía el fixture de 0x59/F0. `run_enemy.ps1 <checkout>` ejecuta la comprobación SDL con los sanitizadores. SHA-256 de `fixture-run.log` `67f538e647cc9f740f994f3053d08ea3bf9b26e2f3238bf8969e9336f3e83940`. El directorio conserva también el prompt, el script de derivados y la comparativa visual.
