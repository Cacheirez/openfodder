# A.1 — Auditoría de GroundHole 0x7C/F0

14 de noviembre de 2026. Entrada `50b569aca9e7f393160a424402fa8cbd38da722b`. Amiga The One, misión 1, fase 2 (Find Grenades). Sesión `manual-20261114-004828`, candidato de 331 vínculos a 12× y reloj normal.

## Recuento

- El analizador de transacciones reprodujo el censo de la sesión. Hubo 2.133 publicaciones HD de 3.986 intentos (53,51 %), 1.847 rechazos por faltantes y seis intentos interrumpidos. La racha máxima fue de 10,645 s entre marcas del log. Miguel observó mejora y retornos frecuentes al clásico. La aceptación visual sigue PENDIENTE.
- `b27064e821fb760e4ec5e37a830ac2e35b81b46490abf208da81cc928cf63cf4` está ausente del manifiesto. Aparece una vez en cada uno de 1.270 intentos, en la escena 186, ranura 17, generación 158. Es el único faltante en 801 intentos, incluido el primero en que aparece, 2623. En los otros 469 coincide con al menos otra clave faltante.
- Resolver solo esta clave dejaría 2.934 de 3.986 intentos como publicaciones potenciales (73,61 %) al aplicar el cambio al registro. Quedarían 1.046 rechazos por faltantes y los seis intentos interrumpidos. La proyección conserva el resto del registro y la comprobación SDL queda PENDIENTE.

## Identificación nativa

`GroundHole` es el tipo 24 y puede generar enemigos con sus propios temporizadores. El código fija el orden inicial de dibujo y el frame 0 en la transición que activa la generación. El snapshot reconstruido coincide con la clave observada: formato Amiga8, persona 0, animación 0, sin vehículo ni destrucción pendiente. Tabla `stru_8D618`, segmento `eGFX_IN_GAME2` (1), offset 560, recurso decodificado de 320 × 256 y cuatro planos. Ambas paletas efectivas valen 0. La tabla da dos palabras, una fila y anclaje (0, 0). [Lógica original](../../Source/Sprites/Sprite_Effects.cpp) · [Tabla Amiga](../../Source/Amiga/SpriteData_Amiga.hpp)

El cálculo en Python verificó primero la clave de referencia del mismo recurso y paleta. Encontró una única coincidencia para GroundHole entre las combinaciones comprobadas. El renderizador nativo C++ recalculó la clave y obtuvo un raster de **16 × 1 con cero píxeles visibles**. Es una reconstrucción a partir del recurso local y la tabla, con identidad validada por la clave del log. [Clave de variante](../../Source/Utils/SoldierVariant.hpp) · [Renderizador de diagnóstico](../../tools/modernization/render_walk_native.cpp)

El registro consulta la clave exacta antes de decidir si conserva el dibujo nativo. La hoja 0x7C admite `keep-associated` y excluye el reemplazo artístico. Esa ruta es una opción para la decisión posterior. La auditoría conserva el manifiesto de 331 vínculos y el comportamiento del juego. [Registro de variantes](../../Source/Utils/OrderedSoldierRegistry.hpp)

## Recuperación local

El directorio de trabajo es `C:/Users/migue/.codex/visualizations/2026/11/13/01a1d73b-c7f6-7d50-b9da-34a33fff21c4`. Contiene `groundhole-audit/verify_groundhole.py`, el snapshot derivado, el raster y el resumen de verificación. Los recursos originales se conservan localmente.

Desde el directorio anterior, ejecutar:

```powershell
$repo = 'C:/Users/migue/Projects/openfodder'
$ref = 'C:/Users/migue/.codex/visualizations/2026/11/08/01a1bb46-b87b-7671-82cd-0fdee66db3de/a1/snapshots'
$renderer = 'C:/Users/migue/.codex/visualizations/2026/11/06/01a1b328-fed4-7e22-8351-edd56f133b83/openfodder-d3-crops/openfodder_native_walk_renderer.exe'
python -B groundhole-audit/verify_groundhole.py $repo a1-331/manual-20261114-004828 $ref $renderer
```

| Evidencia | SHA-256 |
|---|---|
| Log de la partida | `4fa4f351ee3cd0bd4b1ebfda108a195ab7f844ab0e1700495d22b487a558c75c` |
| Manifiesto de 331 vínculos | `16f563342700f2a679c67aed24c8c62effb2a4725cd3b7526593c4fbb6851e3d` |
| Recurso Amiga decodificado | `3dd8d73e4700b42f081f25b25b547b5bd76c9124580ecbd5e01729527e9d8f11` |
| Script de verificación | `76045b773c6f764ff465fedb7e92216dd12ccdc222b866351edbb12e883e1b85` |
| Snapshot derivado | `7c6685886ae886501657ea6f7d20840b77a6ec716c3e2c2316b35061f8a44b8b` |
| Raster RGBA original | `f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b` |

## Decisión de cobertura

Conservar el dibujo nativo con un vínculo `keep-associated` para la clave exacta auditada. El registro existente admite esa decisión en la hoja 0x7C. El compositor ejecuta el productor clásico en su posición original.

La prueba aislada reconstruyó el snapshot real y colocó GroundHole entre dos cuerpos HD superpuestos. A 8× y 12×, el productor nativo emitió cero escrituras. La composición conservó el orden de las tres observaciones y fue idéntica, píxel a píxel, a la escena con solo los dos cuerpos. Sin el vínculo, el registro marcó un faltante y la composición quedó incompleta. La clave recalculada para otro frame siguió sin resolver. Windows x64, Clang 23.1.5, ASan/UBSan PASS. El vínculo de prueba se creó en memoria. La integración en el candidato, SDL, LSan y la aceptación jugando quedan PENDIENTES.

Desde la raíz del checkout, ejecutar `& 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1d935-9486-7263-8dfc-1773e4420637/run_groundhole_probe.ps1'`. El script usa el snapshot y el recurso local de la auditoría, recompila la prueba y guarda la salida en ese directorio.

| Evidencia | SHA-256 |
|---|---|
| `probe_groundhole.cpp` | `1b0401bf27c84778ed57d2b28aa45d7147fb42df6a720cb197b1bcbb2fcf7530` |
| `run_groundhole_probe.ps1` | `926d603b8b49a349473950f85cab8b53d3b16266e53f434e410f9960b30675f2` |
| `probe-run.log` | `3be9e15621e2f8c448fa9d0c84116952dd1806f3e2243f509d7f3bd85db4afb4` |
