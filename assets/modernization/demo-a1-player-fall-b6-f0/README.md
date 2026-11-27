# Caída lateral derecha del jugador, 0xB6/F0

Maestro provisional en estilo C, generado con ImageGen integrado el 17 de noviembre de 2026. Usa la caída aceptada `0xB0/F0`, el maestro de marcha lateral con el verde oliva elegido por Miguel y la silueta nativa local de esta dirección. El arte nuevo se distribuye bajo GPL-3.0-or-later.

`source.png` es RGBA 1341×1173 y tiene SHA-256 `cad297049c2c286a8422263ccc0a4d9ec07c0ff14e43913345bfdea89d6b0a65`. Recorte de alfa ≥16 `[384, 129, 892, 973)`. El contrato de Amiga The One es 16×14, segmento 0, offset 2820, dos columnas, 14 filas y modificadores 0/0. La silueta nativa ocupa `[5, 1, 13, 12)`.

La figura derivada ocupa `[6, 2, 12, 12)`. Conserva la proporción estrecha del perfil y la altura nativa de los pies. Se usa `build_soldier_batch.cpp` con el recorte indicado, colocación `6 6 10` y traslado de dos filas nativas hacia arriba. `build_ordered_soldier_asset.cpp` exporta el RGBA exacto de cada PNG. El manifiesto liga las dos densidades a una sola clave observada en la partida anterior de M1P2. Aceptación visual y jugable pendiente.

## Prompt de generación

```text
Use case: stylized-concept. Create one transparent RGBA OpenFodder sprite, falling player 0xB6/F0, right-facing side profile. Reference 1 is the native pose silhouette and direction; reference 2 is the accepted forward-facing fall design; reference 3 shows the soldier's true right-facing profile in normal walking. Use the same helmet, olive fabric, tan straps and painterly C style as the two modern references. Rotate the body fully screen-right with the nose and both toes pointing horizontally right, not southeast. Steep overhead oblique view with the crown of the helmet visible, profile of the face under its brim. Single compact in-air drop, arm flexed slightly forwards and down in a bracing gesture, opposite arm partly occluded, knees and boots tucked close under the hips, no running stride. Match the small vertical silhouette of the pixel input and the body size of the accepted fall; preserve screen-right directional readability in a 16×14 game cell. One full figure with generous genuinely transparent padding, no ground, shadow, scene, effects, text, protruding rifle or extra equipment. Natural solid hand-painted game character, broad brush texture, crisp alpha.
```
