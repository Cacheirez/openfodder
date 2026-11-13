# A.1 — Auditoría de marcha enemiga 0x44/F1

13 de noviembre de 2026. Entrada `bbebb5d35730e59c0d66469b2893f577d78666ab`. Sesión `interactive-check-02`, Amiga The One, misión 1, fase 2 (Find Grenades). [Evidencia del log](evidence/demo-a1-interactive.json).

## Recuento frente al candidato de 330 vínculos

Se verificaron el tamaño y SHA-256 del log, el manifiesto histórico de 322 vínculos y el candidato de 330 (SHA-256 `0688714a37fa96baa19997348269b109768f9a3aba9878db19c97217d648fa59`). Los 322 vínculos históricos coinciden. Los comandos reproducen los resultados originales a 12× (92 publicaciones HD y 4.364 rechazos). Frente al candidato quedan **4.315 de 4.456 intentos sin claves faltantes (96,84 %), 141 con faltantes y 36 claves residuales**.

`af38382eee31380c6ba6d0469c9237f48400fa21bdeb3e8f09efbdd149988d77` es el único faltante en **12 intentos** y aparece en **15**. Los 15 comandos corresponden a la ranura 21, generación 162, escena 186, entre los intentos 4705 y 4813. El intento 4705 (intervalo 4704) tiene ocho comandos. En el log faltaban F4, 0x59/F0 y 0x44/F1. El candidato ya cubre F4 y 0x59/F0.

La clave `e7476cf9e71cde317e8ce0af74df9f13d0686e2d9aa4ba104d77f94a456c65d6` empata en ambos recuentos. El orden lexicográfico sitúa primero a 0x44/F1. Eliminando solo 0x44/F1 de los conjuntos de faltantes del log quedan **4.327 de 4.456 intentos sin faltantes (97,11 %) y 35 claves residuales**. Es una proyección sobre el registro histórico.

## Identificación nativa

- Enemigo tipo 5, persona IA (1), hoja 0x44, frame 1, `eSprite_Anim_None` (0), fuera de vehículo y sin destrucción pendiente. 0x44 ocupa el índice 2 del tramo de marcha en `mSprite_AnimationEnemyPtrs`. [Tabla de animación](../../Source/Sprites.cpp) · [Estados](../../Source/Sprites.hpp).
- Amiga The One, formato Amiga8, `stru_8CE08`, segmento `eGFX_IN_GAME` (0), offset 5614, dos palabras en tabla, 14 filas, cuatro planos, ambas paletas efectivas a 0 y anclaje (0, 0). Recurso decodificado de 320 × 336, SHA-256 `7a44b4a6dafa1350da974825ea1e2028fd5d3d946f415781966ea1cadc9bb134`. [Tabla Amiga](../../Source/Amiga/SpriteData_Amiga.hpp).
- El cálculo independiente en Python comprobó el recurso y la paleta, reprodujo primero la clave del snapshot de referencia y encontró una única combinación de variante que coincidía con la clave histórica. El renderizador nativo C++ volvió a calcular la misma clave desde el snapshot reconstruido y produjo un raster de 16 × 14 con 67 píxeles de alfa distinto de cero. SHA-256 RGBA `18484cf62316380c2b8a03f3919d565887d1cb85a9460a17a7d8071b0deafefb`. [Cálculo del motor](../../Source/Utils/SoldierVariant.hpp) · [Renderizador](../../tools/modernization/render_walk_native.cpp).

La auditoría identificó un reemplazo de cuerpo. [Registro](../../Source/Utils/OrderedSoldierRegistry.hpp).

## Recuperación local

Directorio `C:/Users/migue/.codex/visualizations/2026/11/13/01a1d707-8a99-71d0-8480-b7825ed1dffd`. Ejecutar `python -B verify_residual_330.py <checkout> <a1> <candidato330/candidate-manifest.json> <renderer.exe>`. Usar el árbol `a1` del [Arranque rápido](CONTINUIDAD.md), el manifiesto de `integracion-hit/candidate` documentado en la [integración de Hit](DEMO_A1_AUDITORIA_MUERTE_ENEMIGA_71_F1.md#integración-de-hit) y el [renderizador conservado de F4](DEMO_A1_AUDITORIA_RANGO_F4.md#recuperación-local) con su carpeta `native-snapshots`. El script localiza el log a partir de la evidencia de sesión y genera el snapshot, el raster y el resumen.

| Archivo | SHA-256 |
|---|---|
| `verify_residual_330.py` | `282e86c228d6f4756c6e397b8421f581d434604a59f1d5da591009ed87f8757e` |
| `enemy-walk-44-f1-derived.json` | `df3a3d5e07c0986569c83f2f090735d91fe1c473759990d41fadf8c30212783a` |
| `enemy-walk-44-f1-verification.json` | `51c572f16271ac51f0de1472f6441cdfb84e6f53621e8262f2b9d65832ffbe4d` |

## Integración y comprobación

13 de noviembre de 2026. Maestro RGBA de 1.060 × 1.484 creado con ImageGen integrado a partir del raster nativo auditado y la marcha C01 verde A, dirección 2/F1. La comparativa estática interna cotejó la orientación hacia la izquierda, la zancada, el oliva oscuro y el encaje a ambas densidades. [Maestro, derivados y manifiesto](../../assets/modernization/demo-a1-enemy-walk-44-f1/).

- **Candidato:** 168 activos y 331 vínculos (323 reemplazos y ocho asociados). Los 166 activos y 330 vínculos previos conservan bytes y orden. SHA-256 del manifiesto generado en Windows `16f563342700f2a679c67aed24c8c62effb2a4725cd3b7526593c4fbb6851e3d`.
- **SDL software Windows x64:** Clang 23.1.5, SDL 3.4.0 y ASan/UBSan PASS a 8×/12×. Seis cuerpos. La pose cubre 59 celdas pintadas antes en ambas densidades, queda bajo el cuerpo posterior en 66/67 celdas y aporta a 79/80 celdas visibles. Recorte de cinco filas cotejado por píxel. Una clave faltante deja intacto el destino HD, el retorno produce el raster clásico y la restauración de la clave recupera HD. Regresiones del mismo fixture PASS.
- **Registro histórico:** 4.327 de 4.456 intentos sin faltantes (97,11 %), 129 con faltantes y 35 claves residuales. Primera clave restante `e7476cf9e71cde317e8ce0af74df9f13d0686e2d9aa4ba104d77f94a456c65d6`, tipo 5, hoja 0x45, F0, 12 faltantes únicos y 15 apariciones. Identificación nativa PENDIENTE.
- **PENDIENTES:** aceptación jugando, cobertura restante, GPU, audio, CD32, H3 y LSan para este bloque. La prueba SDL usa una escena controlada y el recuento procede del registro histórico.

### Reproducción de la integración

Maestro SHA-256 `5d53188d8988bc90ccd1b70c55cf40c114cfea6ccd0bb2534c5716ba9ca19f4c`. Con Pillow 11.3.0, recortar la caja alfa ≥ 128 `(129, 118, 903, 1366)`. Redimensionar con Lanczos a `(8*d, 14*d)` y colocar en `(3*d, 0)` sobre el lienzo transparente de `(16*d, 14*d)`. El manifiesto del activo registra los hashes RGBA de ambas densidades.

Generar el candidato con `python -B tools/modernization/prepare_demo_a1_manifest.py --base <verde-A>/qa-rocket-native/art/candidate-manifest.json --out <evidencia>/candidate --with-enemy-walk-44` usando el [verde A verificado](DEMO_A1_VERDE_A.md#reproducción-y-recuperación). En el [directorio de evidencia](C:/Users/migue/.codex/visualizations/2026/11/13/01a1d70e-e9d1-74f0-9951-5079b656d5e3), ejecutar `python -B prepare_walk_44_input.py <checkout> <integracion-hit> <auditoría-44-F1> <evidencia>` y `run_enemy.ps1 <checkout>` con el [fixture de Hit](DEMO_A1_AUDITORIA_MUERTE_ENEMIGA_71_F1.md#integración-de-hit) y el snapshot de la auditoría de arriba. SHA-256 de `fixture-run.log` `60b2c828d12a980667f889f1c706057408bc3b18f37c0e61da4d54e2fbec90a4`. El directorio conserva `prompt-imagegen.txt`, `derive_enemy_walk_44.py` y `comparison.png`.
