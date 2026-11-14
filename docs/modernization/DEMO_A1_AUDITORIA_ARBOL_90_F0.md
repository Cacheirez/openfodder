# A.1 — Auditoría del árbol 0x90/F0

## Registro del 14 de noviembre

En la partida de Amiga The One, misión 1, fase 2, con 331 vínculos a 12× y reloj normal, se observaron 2.133 publicaciones HD de 3.986 intentos. La auditoría reprodujo el censo del log y comprobó que el candidato de 332 conserva los 331 vínculos en orden y añade la clave exacta de GroundHole. Al proyectar ese vínculo sobre el log quedan 1.046 rechazos por faltantes y seis intentos interrumpidos. [Datos de la partida](DEMO_A1_AUDITORIA_GROUNDHOLE.md#recuento)

El árbol es el primer residual por faltantes únicos. Sus 247 apariciones registradas son de tipo 14, hoja 0x90, frame 0 y densidad 12×, entre los intentos 4.562 y 5.853. En las 247 queda como único faltante tras aplicar GroundHole, con secuencia completa y al menos un reemplazo por intento. Cubrir también el árbol proyecta 3.181 de 3.986 publicaciones posibles (79,80 %), 799 rechazos con 59 claves residuales y seis interrupciones. La proyección usa los intentos de esa partida.

## Identificación nativa

`eSprite_Tree` es el tipo 14. `Sprite_Handle_Tree` selecciona la hoja 0x90 y delega en `Sprite_Handle_Exploidable`. La tabla `mSpriteSheetTypes_InGame_Amiga_TheOne` remite a `stru_8D988`, con un único frame. El recurso es `eGFX_IN_GAME2` (segmento 1) en el formato Amiga8, con offset 1942, hoja decodificada de 320 × 256 y cuatro planos. La entrada tiene dos columnas de tabla, 28 filas y anclaje (0, 0). Las paletas del recurso y del dibujo valen 0. El estado exacto recuperado tiene persona 0, animación 0, vehículo 0 y destrucción 0. [Tipo](../../Source/Sprites.hpp) · [Lógica](../../Source/Sprites/Sprite_Core.cpp) · [Tabla](../../Source/Amiga/SpriteData_Amiga.hpp)

El cálculo Python reprodujo primero una clave de control del mismo recurso a partir de sus campos, bytes planares y colores. Encontró una coincidencia para el árbol entre las combinaciones comprobadas. El renderizador nativo C++ recalculó la misma clave, `a835b7ae71451ea0a37ea0a0c1e77da13a45f003b0cf218314edc6e0c79a1a2d`, y produjo un raster de **16 × 28 con 299 píxeles de alfa distinto de cero**. [Cálculo de la clave](../../Source/Utils/SoldierVariant.hpp) · [Renderizador](../../tools/modernization/render_walk_native.cpp)

El registro exige la clave exacta y limita `keep-associated` a casos admitidos. La integración autoriza únicamente esta variante del árbol. [Registro de variantes](../../Source/Utils/OrderedSoldierRegistry.hpp)

## Reproducción local

Ejecutar desde el checkout en el que se conservan los recursos de las pruebas anteriores. El script comprueba hashes de entrada y deja el snapshot reconstruido, el raster y el resumen en su propio directorio.

```powershell
$repo = (Get-Location).Path
$work = 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1d940-3123-7da0-a37b-fea3f4ad7b74'
$session = 'C:/Users/migue/.codex/visualizations/2026/11/13/01a1d73b-c7f6-7d50-b9da-34a33fff21c4/a1-331/manual-20261114-004828'
$manifest = 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1d935-9486-7263-8dfc-1773e4420637/candidate332/candidate-manifest.json'
$ref = 'C:/Users/migue/.codex/visualizations/2026/11/08/01a1bb46-b87b-7671-82cd-0fdee66db3de/a1/snapshots'
$renderer = 'C:/Users/migue/.codex/visualizations/2026/11/06/01a1b328-fed4-7e22-8351-edd56f133b83/openfodder-d3-crops/openfodder_native_walk_renderer.exe'
python -B "$work/verify_tree.py" $repo $session $manifest $ref $renderer
```

| Evidencia | SHA-256 |
|---|---|
| Log de la partida | `4fa4f351ee3cd0bd4b1ebfda108a195ab7f844ab0e1700495d22b487a558c75c` |
| Candidato de 332 vínculos | `6cb423f96c8b0b698430d2cf0dcfe19c3dbb92734edbf9d0089ab7950b7fba11` |
| Recurso Amiga decodificado | `3dd8d73e4700b42f081f25b25b547b5bd76c9124580ecbd5e01729527e9d8f11` |
| `verify_tree.py` | `f7fcb38a483fc49162359f88ecb0eb7cb4855f4f1fde1bdc9dad5048144451f0` |
| `tree-derived.json` | `ad55cf579c1bef8088b05bfaf0ce82b5421c6ab1e916f1f97066c3fa41173377` |
| `tree-native.rgba` | `ae538338e91a423775d70f577f317ed50230473c70be230cddbc7734d39cacd7` |
| `tree-verification.json` | `8f8aee7a5f07cf8e2f9fe0faa89735bbf9cba4f218f72f9c85330d7ac6b2fcc1` |

## Integración y comprobación

`--with-tree-90` genera el candidato de 333 vínculos (323 reemplazos y diez asociados). Añade un único `keep-associated` al final del candidato de 332. Los 332 vínculos conservan su orden y los 168 activos coinciden byte a byte. `--with-ground-hole` reproduce el manifiesto previo con el mismo SHA-256.

- SDL software Windows x64, Clang 23.1.5, SDL 3.4.0 y ASan/UBSan PASS a 8× y 12×. En cada pasada, el árbol ejecutó 299 escrituras nativas en su posición entre los cuerpos HD. Cubrió 60 celdas HD anteriores y el cuerpo posterior cubrió 90 de sus escrituras. La salida SDL coincidió píxel a píxel con el fotograma compuesto. Otra clave de árbol, incluso con vínculo `keep-associated` explícito, quedó excluida. Al provocar un faltante del árbol, el fotograma volvió íntegro a clásico y recuperó HD al restablecer la clave. Las regresiones del mismo fixture pasaron.
- La partida del 14 de noviembre observó 2.133 publicaciones HD. Con los 333 vínculos, el recuento del mismo log proyecta 3.181 de 3.986 intentos publicables (79,80 %), 799 rechazos, seis interrupciones y 59 claves residuales. La primera por faltantes únicos es `6c2cdf76`, proyectil tipo 6, hoja 0x7F/F0, con 47 faltantes únicos en 450 intentos residuales.
- Aceptación jugando, GPU, audio, CD32 y LSan local PENDIENTES.

### Reproducción de la integración

Desde la raíz del checkout, con la [base verde A verificada](DEMO_A1_VERDE_A.md#reproducción-y-recuperación) y los archivos locales de las auditorías:

```powershell
$work = 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1d953-1f86-7b42-854d-607cc2d2194e'
$previous = 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1d935-9486-7263-8dfc-1773e4420637'
$audit = 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1d940-3123-7da0-a37b-fea3f4ad7b74'
$snapshots = 'C:/Users/migue/.codex/visualizations/2026/11/08/01a1bb46-b87b-7671-82cd-0fdee66db3de/a1/snapshots'
$base = 'C:/Users/migue/.codex/visualizations/2026/11/11/01a1ccf2-ba36-78a2-8403-b24f50437a5c/qa-rocket-native/art/candidate-manifest.json'
$log = 'C:/Users/migue/.codex/visualizations/2026/11/13/01a1d73b-c7f6-7d50-b9da-34a33fff21c4/a1-331/manual-20261114-004828/engine.log'
python -B tools/modernization/prepare_demo_a1_manifest.py --base $base --out "$work/candidate333" --with-tree-90
python -B tools/modernization/prepare_demo_a1_manifest.py --base $base --out "$work/candidate332-regression" --with-ground-hole
python -B "$work/prepare_tree_integration.py" $previous $audit $snapshots $log $work
& "$work/run_tree_sdl.ps1"
```

Para repetir la generación, copiar los dos scripts a un directorio nuevo y usarlo como `$work`. El directorio original conserva el candidato y el log SDL comprobados.

| Evidencia | SHA-256 |
|---|---|
| Manifiesto Windows de 333 vínculos | `dc3eabe3b0ded46ad957d7b4e4546b6539a0526050821cd00133c54f248c105e` |
| `prepare_tree_integration.py` | `e5ba139da423af804a3a930f1ffa00ad4cb42ff20268b882f6189e6a75f36920` |
| `run_tree_sdl.ps1` | `43724ac411f460e698316b4495b48720c67c4de9b2407ff78d48012ceeaf450c` |
| `tree-sdl.log` | `5e17eb3d6ebf98996d9f1c3f574e9138c92be7d09b40d0f034a9f0e132b9e432` |
