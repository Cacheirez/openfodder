# Caída del jugador hacia delante y derecha, 0xB7/F0

Maestro provisional en estilo C, generado con ImageGen integrado el 17 de noviembre de 2026. Referencias de la generación: la caída aprobada `0xB0/F0`, C01 con verde A y la silueta nativa local de la dirección. Se distribuye el arte nuevo bajo GPL-3.0-or-later.

`source.png` es RGBA 1341×1173 y tiene SHA-256 `299944e4895e42164815ae601dcf370348949627c38fb912ec0176b3203b58b7`. Recorte de alfa ≥16 `[327, 219, 1024, 942)`. El contrato de Amiga The One es 16×14, segmento 0, offset 2822, dos columnas, 14 filas y modificadores 0/0. La silueta original ocupa `[5, 1, 12, 12)`.

La figura derivada conserva el tamaño 9×9 del piloto y termina en y=12, como la referencia nativa. Se usa `build_soldier_batch.cpp` con el recorte indicado, colocación `4 9 9` y traslado de dos filas nativas hacia arriba. `build_ordered_soldier_asset.cpp` exporta el RGBA exacto de cada PNG. El manifiesto liga las dos densidades a una sola clave de M1P2 observada tanto en el último registro de Miguel como en el del soldado flotante. Aceptación visual y jugable de la variante pendiente.

## Prompt de generación

```text
Use case: stylized-concept. Create exactly one transparent RGBA game sprite master for OpenFodder player falling pose 0xB7/F0. Reference 1 is the native pose and direction. Reference 2 is the accepted 0xB0 falling soldier, use its proportions, scale, olive helmet, tan straps, boot shape, no visible rifle, and painterly Style C. Reference 3 shows the same model from the intended southeast facing direction, use its direction and green olive palette, not its walk pose. Rotate the body, face and boots together to face toward the lower right of the screen as in the native silhouette, turning the three-quarter body volume rather than mirroring or simply tilting. Show helmet crown high and face partly hidden. Same compact pose falling in midair, arms slightly opened and braced close to torso, boots tucked directly beneath hips, with gentle diagonal asymmetry like the native sprite. Preserve the size and weight of the same person. Steep overhead oblique strategy-game camera, moderate hand-painted broad strokes, clean silhouette. Real alpha, generous transparent margin. No background, no ground contact or shadow, no effects, no text, no new gear, no extra objects, no weapons pointing out. Frame is one pose only.
```
