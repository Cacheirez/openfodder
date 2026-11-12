# A.1 — Auditoría del enemigo tumbado 0x59/F0

12 de noviembre de 2026. Entrada `d9756ffea90ffdabead53efee0f70787aaba8734`. Prueba manual `interactive-check-02`, Amiga The One, misión 1, fase 2 (Find Grenades). [Evidencia de la sesión](evidence/demo-a1-interactive.json).

## Recuento contra el candidato

Se comprobaron tamaño y SHA-256 del log, el manifiesto histórico de 322 vínculos y el candidato de 325, SHA-256 `5a7197d0f21b62d15c4be4cc44c379aa84455c35b436b584dbb3e389fee26cfc`. Se cotejaron los comandos y resultados de los 4.456 intentos a 12× y las tres claves añadidas al candidato (F4, tejado y caja). Los resultados registrados fueron 92 publicaciones y 4.364 rechazos. El recuento por conjuntos de claves faltantes deja **3.977 intentos sin faltantes y 479 con faltantes**, con 41 claves residuales.

La primera clave, `0ae80fd93ee8120c3e003e5b0e9383b2514910c7353812e498a587247d5455d8`, es el **único faltante en 275 intentos y aparece en 359**. Se registraron 360 comandos en la escena 186, entre los intentos 4107 y 4829, en las ranuras 21 (generación 162) y 20 (generación 161). En un intento ambas ranuras usan la misma clave. La segunda clave tiene 12 intentos como único faltante y 33 en total. Cubrir la primera dejaría 4.252 de 4.456 intentos sin faltantes en el recuento (95,42 %). La publicación HD efectiva sigue PENDIENTE.

## Identificación nativa

- `eSprite_Enemy` (tipo 5), persona IA (1), hoja 0x59, frame 0, animación `eSprite_Anim_None` (0), fuera de vehículo y sin destrucción pendiente. 0x59 es la última entrada del tramo de tumbado (`Prone`, índice de dirección 7) de `mSprite_AnimationEnemyPtrs`. [Tabla de animación](../../Source/Sprites.cpp) · [Selector](../../Source/Sprites/Sprite_Troop.cpp).
- Amiga8, `stru_8D118`, segmento `eGFX_IN_GAME` (0), offset 6750. Recurso planar de 320 × 336, cuatro planos, paleta del recurso y de dibujo 0, 14 filas, dos palabras en la tabla, anclaje (0, 0). Recurso decodificado SHA-256 `7a44b4a6dafa1350da974825ea1e2028fd5d3d946f415781966ea1cadc9bb134`. [Tabla Amiga](../../Source/Amiga/SpriteData_Amiga.hpp).
- El cálculo Python comprobó primero la clave de un snapshot de referencia del mismo recurso y la coincidencia de sus colores con la referencia de A.1. Con la geometría de 0x59/F0 y el estado descrito reprodujo la clave del log. El renderizador nativo la verificó con el código C++ y produjo un raster de 16 × 14 con 67 píxeles visibles, SHA-256 RGBA `33560bed47a5af3e46db0408a8220e81ac23132ad72059b6f2744d887086515d`. El snapshot derivado reconstruye la variante a partir de referencias conservadas. [Cálculo del motor](../../Source/Utils/SoldierVariant.hpp) · [Renderizador](../../tools/modernization/render_walk_native.cpp).

El registro exige reemplazo para esta pose de un cuerpo. Quedan PENDIENTES el arte, la integración en SDL y la aceptación jugando. La auditoría usa el log existente y el renderizador conservado. [Registro](../../Source/Utils/OrderedSoldierRegistry.hpp).

## Recuperación local

Directorio `C:/Users/migue/.codex/visualizations/2026/11/12/01a1d0cf-34dc-7bf2-839c-e2c860d0c1fc`. Ejecutar `python -B verify_residual_325.py <checkout> <a1> <box-candidate/candidate-manifest.json> <renderer.exe>`. Usar el árbol `a1` de [Continuidad](CONTINUIDAD.md), el manifiesto de 325 vínculos de la [integración de la caja](DEMO_A1_AUDITORIA_CAJA_GRANADAS.md#recuperación-local) y el [renderizador de F4](DEMO_A1_AUDITORIA_RANGO_F4.md#recuperación-local). El directorio `native-snapshots` junto al ejecutable contiene el snapshot `042ddc7dcc89d3c06b666b9eeb3faf0000b99b19f57ef29d8ac53df2c5957157.json` y el recurso local. El script comprueba sus hashes y lee el log desde la evidencia de la sesión.

| Archivo | SHA-256 |
|---|---|
| `verify_residual_325.py` | `16ab7a4e639981acbc35e6125cc252c6ae3cbba6af151f6ce25a1a9a1ba247ab` |
| `enemy-prone-derived.json` | `fbd0a80065fca86644378476e94fedb1653975a1b704473b1be55e1c062f507c` |
| `enemy-prone-verification.json` | `08d90ea4873c2b68458f15db9124345fdee76bf36faa748fdfcb4ffaa09acdeb` |
