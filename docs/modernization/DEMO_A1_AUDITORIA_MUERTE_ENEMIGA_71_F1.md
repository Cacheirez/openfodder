# A.1 — Auditoría de muerte enemiga 0x71/F1

13 de noviembre de 2026. Entrada `8554ba154586f8db8fd350e0399b38f3e7d942cb`. Sesión `interactive-check-02`, Amiga The One, misión 1, fase 2 (Find Grenades). [Evidencia de sesión](evidence/demo-a1-interactive.json).

## Recuento contra 327 vínculos

Se verificaron tamaño y SHA-256 del log, el manifiesto histórico de 322 vínculos y el candidato de 327 (SHA-256 `160af5ec803ff1d0ba1bbdbac8a6a92aefda04a3542beea22d4d310f243eadaf`). Coinciden los 322 vínculos históricos y se identificaron los cinco añadidos. Los comandos cuadran con los 4.456 resultados históricos a 12× (92 publicaciones HD y 4.364 rechazos). Contra el candidato quedan **4.267 intentos sin claves faltantes (95,76 %), 189 con faltantes y 39 claves residuales**.

La clave `f06b98d0debe93b676cd17ba89a9b76e2b91484a08507c83e8d66215dc8237fb` es el único faltante en **12 intentos** y aparece en **33**. Sus 33 comandos son de la ranura 21, generación 162 y escena 186, entre los intentos 4988 y 5076. En el intento 5036 (intervalo 5035) hay siete comandos. El log marcaba como faltantes la insignia F4 y 0x71/F1. El candidato resuelve F4. Resolver también 0x71/F1 dejaría 4.279 intentos históricos sin claves faltantes (96,03 %).

## Identificación nativa

- Enemigo tipo 5, persona IA (1), hoja 0x71, segundo fotograma (F1), estado `eSprite_Anim_Die2` (6), fuera de vehículo y sin destrucción pendiente. Es la dirección de índice 7 del tramo «Death-2 Anim» en `mSprite_AnimationEnemyPtrs`. La rama `Die2` selecciona ese tramo mediante `(Data8 + 0x20) / 2` y aplica módulo 2 al índice de fotograma. [Tabla](../../Source/Sprites.cpp) · [Selector](../../Source/Sprites/Sprite_Troop.cpp).
- Amiga8, tabla `stru_8D418`, segmento `eGFX_IN_GAME`, offset 8406, cuatro planos, dos palabras en tabla, 14 filas, anclaje (0, 0) y paletas de recurso y dibujo 0. El recurso decodificado de 320 × 336 tiene SHA-256 `7a44b4a6dafa1350da974825ea1e2028fd5d3d946f415781966ea1cadc9bb134`. [Tabla Amiga](../../Source/Amiga/SpriteData_Amiga.hpp).
- El cálculo independiente en Python verificó el recurso y la paleta contra los snapshots conservados, reprodujo la clave de referencia y obtuvo la clave exacta del log para 0x71/F1. El renderizador nativo C++ confirmó la clave y generó un raster de 16 × 14 con 51 píxeles visibles y SHA-256 RGBA `9c69e3e0f4a672776be46a0f90d7acccf6629e74d9361236d5d82d81f8cedfbf`. [Cálculo del motor](../../Source/Utils/SoldierVariant.hpp) · [Renderizador](../../tools/modernization/render_walk_native.cpp).

**PENDIENTE** el reemplazo HD de esta pose, su comprobación SDL, la cobertura restante y la aceptación jugando. La auditoría reutiliza el renderizador existente y mide la cobertura del registro sobre el log histórico.

## Recuperación local

Directorio `C:/Users/migue/.codex/visualizations/2026/11/13/01a1d60e-bb33-7a93-a487-d5b1cfb905af`. Ejecutar `python -B verify_residual_327.py <checkout> <a1> <candidato327/candidate-manifest.json> <renderer.exe>`. Usar el árbol `a1` del [Arranque rápido](CONTINUIDAD.md), el [candidato de 327 vínculos](DEMO_A1_AUDITORIA_MARCHA_ENEMIGA_45_F1.md#reproducción) y el [renderizador conservado de F4](DEMO_A1_AUDITORIA_RANGO_F4.md#recuperación-local) con su carpeta `native-snapshots`. El script localiza el log mediante la evidencia de sesión y genera el snapshot, el raster y el resumen.

| Archivo | SHA-256 |
|---|---|
| `verify_residual_327.py` | `206e0f029f0fb251b5675e1c8f1e184bd290a083308de214b0b7123eeab6dc72` |
| `enemy-death-71-f1-derived.json` | `7dedc7d8851f0f8f9a8e223af0ea4af9a073ee267acbcabdfc47219807702cbb` |
| `enemy-death-71-f1-verification.json` | `61178c4f72836a6de35d67a1bd92ce4994913abc1d159b71c08816e329e2651f` |
