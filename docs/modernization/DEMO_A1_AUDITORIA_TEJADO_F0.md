# A.1 — auditoría nativa del tejado 0x91/F0

12 de noviembre de 2026. Entrada `731d96a9dd7f88e115c05f62718c9ff3949fb382`. Prueba manual `interactive-check-02`, Amiga The One, misión 1, fase 2 (Find Grenades). [Evidencia de la sesión](evidence/demo-a1-interactive.json).

## Impacto registrado

Se verificaron tamaño y SHA-256 del `engine.log` cerrado y se cruzaron los comandos con el contador `missing` de cada resultado transaccional. Los 4.456 intentos corresponden a 4.456 pares únicos de escena e intervalo. Hubo 92 publicaciones y 4.364 rechazos. Cada clave cuenta como máximo una vez por intento.

El tejado tipo **15 / 0x91 / F0**, clave **`5fc9fc6b277ef4b4f27f2552b6a212827b18f31e8e3dc4c6979cb98c4e64d9f7`**, es el faltante más frecuente después de F4. Afectó a **1.758 intentos**. El siguiente de la clasificación afectó a 1.755. El tejado aparece en la escena 186, densidad 12, ranura 16 y generación 157, entre los intentos 365 y 3879 (intervalos 364 y 3878).

- **3** intentos con el tejado como único faltante (3875, 3877 y 3879).
- **1.732** con el tejado, F4 y al menos otro faltante.
- **23** con el tejado y otro faltante, sin F4.

Al descontar F4 del listado histórico, solo esos tres intentos quedarían sin faltantes al cubrir también el tejado. La publicación HD efectiva en esos intervalos queda PENDIENTE. La clave falta en las 322 vinculaciones del manifiesto exacto de la sesión, cuyo SHA-256 se cotejó con la evidencia.

## Procedencia comprobada

- `Sprite_Handle_BuildingRoof` (tipo 15) selecciona la hoja `0x91` y delega en `Sprite_Handle_Exploidable`. La tabla `mSpriteSheetTypes_InGame_Amiga_TheOne` dirige `0x91` a `stru_8D998`, con una sola fila F0. Segmento `eGFX_IN_GAME2` (1), offset **2744**, 3 columnas de tabla, 12 filas y modificadores (0, 0). [Manejador](../../Source/Sprites/Sprite_Core.cpp#L996) · [Tabla](../../Source/Amiga/SpriteData_Amiga.hpp#L724).
- `eGFX_IN_GAME2` usa `mSpriteSheet_InGame2`, decodificada del LBM `<BaseBaseSet>copt.lbm`. Recurso Amiga8 de 320 × 256, 4 planos, SHA-256 `3dd8d73e4700b42f081f25b25b547b5bd76c9124580ecbd5e01729527e9d8f11`. Los índices efectivos de paleta del recurso y del dibujo son 0. El valor 13480 de la tabla pertenece a otro campo. Los 255 colores efectivos del snapshot de referencia, serializados como palabras de 64 bits little-endian, dan SHA-256 `3c97fa5951d5868eb6e2a30eb0d8217c328b1bc13ae50e300f9c80e24d146ec0`. [Segmento y carga](../../Source/Amiga/Graphics_Amiga.cpp#L83) · [Nombre del recurso](../../Source/Map/MapRuntime.cpp#L233).
- Se reprodujo primero la clave conocida de la insignia 0x95/F0. Con el mismo recurso y paleta, la fila del tejado, persona 0, animación 0, vehículo 0 y destrucción pendiente 0 reproducen la clave del log. Se usaron 20 campos de 64 bits little-endian, 192 bytes de recorte planar y los colores efectivos. Cambiar persona a −1 o reutilizar el offset de la insignia cambia la clave. El snapshot es una reconstrucción y carece de tick de la sesión manual.
- El renderizador nativo existente recalculó la misma clave con el código del motor y obtuvo un raster de **32 × 12**, 189 píxeles con alfa distinto de cero y SHA-256 RGBA `b12b1f987c818f7b2851a289651ecdc62b9b09de932aa94e81b955b3433a50c6`. [Renderizador](../../tools/modernization/render_walk_native.cpp).

## Integración del candidato

La opción `--with-roof` del preparador añade exclusivamente esta clave `keep-associated` al verde A con F4. El registro la admite tras resolver la clave exacta, para Amiga8, tipo 15, hoja 0x91/F0, con recurso válido y fuera de los estados de vehículo y destrucción pendiente. Se cotejaron los 160 activos por SHA-256 y las 323 vinculaciones previas en orden. El candidato resultante tiene **324 vínculos (318 reemplazos y 6 conservaciones)** y SHA-256 `3ea4570d5c55500ae75a0696e4c669e7f17bb2a2672086368907ec38b7faed12` (Windows). [Registro](../../Source/Utils/OrderedSoldierRegistry.hpp) · [Preparador](../../tools/modernization/prepare_demo_a1_manifest.py).

SDL 3.4.0 por software en Windows x64 con Clang 23.1.5, ASan y UBSan dio PASS a **8× y 12×**. La escena controlada usa cinco cuerpos con claves nativas y F4. El recorte superior elimina cinco filas del tejado y conserva exactamente 151 de sus 189 escrituras nativas. En cada densidad, el tejado pisa 58 celdas HD previas y el último cuerpo compone sobre 70 celdas del tejado, con 81 escrituras fuera de esa última capa. La salida SDL coincide píxel a píxel con la composición esperada. Dos faltantes inducidos por densidad (clave del tejado o de un cuerpo) rechazan la publicación antes de dibujar HD, restituyen el cuadro clásico completo y recuperan HD al restaurar la clave. El caso F4 anterior también pasa a ambas densidades y el preparador por defecto reproduce su manifiesto byte a byte. LSan PENDIENTE.

**Aceptación jugando:** sigue vigente la no aceptación de Miguel. GPU, audio, CD32, transiciones de juego y cobertura restante PENDIENTES.

## Recuperación local

Directorio `C:/Users/migue/.codex/visualizations/2026/11/12/01a1cf54-015f-7302-9d44-fcd43311516d`. Contiene `verify_roof_f0.py` (SHA-256 `6999098743fac86ed397103ba698c0753fcfee019848abfae1d122667bbb10f7`), `roof-f0-derived.json` (SHA-256 `aa7a21a4cbef37f0c98297d6b78285dedee1230c269520960dc54317a845307e`), el raster y `roof-f0-verification.json`. Para reproducir, ejecutar `python -B verify_roof_f0.py <repo> <a1> <renderer.exe>` desde ese directorio. Usar el árbol `a1` de [Continuidad](CONTINUIDAD.md) y el [renderizador de la auditoría F4](DEMO_A1_AUDITORIA_RANGO_F4.md#recuperación-local), SHA-256 `1ebfebb0575e4c27681ba8bdc2e53acfce414d06861c6b8bfa4368122dcf48ae`.

Evidencia SDL en `C:/Users/migue/.codex/visualizations/2026/11/12/01a1cfaa-f3cf-77c3-a0e6-90a45e1c3754`. Reconstruir `roof-candidate` con `python -B tools/modernization/prepare_demo_a1_manifest.py --base <verde-A>/qa-rocket-native/art/candidate-manifest.json --out <directorio-evidencia>/roof-candidate --with-roof`. Ejecutar `prepare_roof_input.py <directorio-F4> <roof-f0-derived.json> <directorio-evidencia>` con el [caso F4 anterior](DEMO_A1_AUDITORIA_RANGO_F4.md#comprobación-controlada-de-f4) y luego `run_roof.ps1 <checkout>`. El fixture lee los recursos originales desde los snapshots locales. SHA-256 de `fixture-run.log` `910bee70242e93fd93f5c6dc4c35cb1206363a6d172d7105404fd5dd381d2fb9` y de `f4-regression.log` `8290435193c2b61c86b9a6e6fa08954e893fddcbd7686bb53d66facdf85563a5`.
