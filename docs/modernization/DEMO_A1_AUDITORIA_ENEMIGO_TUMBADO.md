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

## Integración y comprobación

13 de noviembre de 2026. Una pose en estilo C — Pintado moderado, con el casco y los acentos marrón rojizo de la referencia nativa. Maestro transparente de 1.339 × 1.174 generado con ImageGen integrado a partir del raster auditado y C01 verde A. Derivados de 128 × 112 y 192 × 168 revisados a ambas densidades. El encaje del arte usa la caja ocupada nativa de 10 × 11 en el lienzo de 16 × 14, con desplazamiento (4, 2). [Maestro, derivados y manifiesto](../../assets/modernization/demo-a1-enemy-prone/).

- Candidato verde A con 162 activos y 326 vínculos (319 reemplazos y siete asociados). Los 160 activos y 325 vínculos anteriores conservan contenido y orden. Único vínculo nuevo: la clave auditada de 0x59/F0. SHA-256 del manifiesto generado en Windows `369b2943531860c8d2fbda7a69207d413c66f5de124c47f67bd850ede9507e75`.
- SDL software Windows x64, Clang 23.1.5, SDL 3.4.0, ASan/UBSan PASS a 8× y 12×. Seis cuerpos en orden nativo de composición del fixture. El enemigo se superpone a cuerpos anteriores, queda parcialmente cubierto por el último y sigue visible. Se cotejaron los píxeles compuestos tras recortar cinco filas. Al cambiar su clave, el intento HD deja intacto el destino, clásico coincide con el raster nativo y HD se recupera al restaurar la clave. La caja, el tejado y F4 se ejercitaron en el mismo fixture.
- PENDIENTES aceptación jugando, GPU, audio, CD32, LSan y cobertura restante. El recuento histórico de faltantes no mide publicación HD efectiva en una partida.

### Reproducción

Maestro SHA-256 `6378ee0023531c8045e196ff06f7897af18a6ad531e07fd8a90f8942c84783cf`. Con Pillow 11.3.0, recortar el maestro a la caja alfa ≥ 128, `(312, 141, 1132, 1091)`. Redimensionar con Lanczos a `(10*d, 11*d)` y pegar sin máscara en `(4*d, 2*d)` sobre el lienzo RGBA transparente de `(16*d, 14*d)`. Guardar PNG y bytes RGBA en orden de filas. Los SHA-256 de los dos derivados RGBA figuran en su [manifiesto](../../assets/modernization/demo-a1-enemy-prone/manifest.json).

Generar el candidato con `python -B tools/modernization/prepare_demo_a1_manifest.py --base <verde-A>/qa-rocket-native/art/candidate-manifest.json --out <evidencia>/candidate --with-enemy-prone`. Usar el [verde A verificado](DEMO_A1_VERDE_A.md#reproducción-y-recuperación). En el [directorio local de evidencia](C:/Users/migue/.codex/visualizations/2026/11/13/01a1d4fa-5b29-7551-8509-724c0bb09f0c), `prepare_enemy_input.py <evidencia-caja> <auditoría-enemigo> <evidencia>` amplía el fixture conservado de la [caja](DEMO_A1_AUDITORIA_CAJA_GRANADAS.md#recuperación-local). `run_enemy.ps1 <checkout>` reutiliza su entorno SDL y sanitizadores. SHA-256 de `fixture-run.log` `eca6b2237102214d810d8c4fe61c81f817ad8231cf73ba47302620aedaa06a6e`.
