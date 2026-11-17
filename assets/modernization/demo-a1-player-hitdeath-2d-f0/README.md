# Piloto 0x2D/F0 — daño/muerte hacia atrás y a la derecha

17-11-2026. Estilo C — Pintado moderado. **PROVISIONAL, pendiente de aceptación visual de Miguel.** No incorporado al lanzador de juego ni aceptado como solución parcial de continuidad.

`source.png` es la copia inmutable del maestro generado mediante la herramienta integrada `image_gen`, con alfa real. Referencia nativa local `death-2d-native/f0-native.png`; [maestro de marcha de la misma dirección](../soldier-walk24/uniform-a/s5-f0-verde-a.png); [C01 verde A](../soldier-c01/uniform-sample/c01-verde-a-12x.png). Los gráficos nativos se conservan fuera de Git. [Contexto, pruebas y anclajes](../../../docs/modernization/DEMO_A1_DANO_2D.md).

Los derivados tienen celda lógica de 16×14, a 8× (128×112) y 12× (192×168). Se exportan con `build_soldier_batch.cpp` y `build_ordered_soldier_asset.cpp`, sin retocar los píxeles del maestro. La colocación sigue el bbox nativo: [3, 0, 13, 12]. No contiene sombra proyectada; las sombras tipo 22 se mantienen como comandos nativos separados. `manifest.json` registra claves, hashes y estado.

## Prompt

```text
Use case: style-transfer / identity-preserve. Asset: ONE transparent RGBA game-sprite master, OpenFodder player hit/death animation 0x2D/F0, rear-right (northeast) direction. Image 1 is the exact native pose and silhouette reference, NOT a style reference. Convert that specific pose into the moderate hand-painted Style C of images 2 and 3. Image 2 is the approved same soldier from the required rear-right orientation, with the correct dark olive uniform, helmet, tan webbing, boots and compact dark rifle; image 3 is accepted C01 character proportions and painting style. The native character is recoiling/staggering from a hit, not walking and not lying flat. Preserve native silhouette and relative positions: helmet crown at top centre, a narrow visible face/profile on the right side of the helmet, torso angled down-left from the helmet, one compact forearm/hand extending screen-right at mid-body, bent legs running diagonally down-left under the hips. Keep a compact rifle against the front/right of the torso following the grey/orange native weapon/hand marks, with no long protruding barrel. Preserve the small restrained red hit accent on the left upper torso at the position in image 1; no additional blood splashes or effects, no exposed wounds. Same steep overhead oblique strategy-game camera, grounded solid anatomy and continuous body scale, broad readable painted facets with tidy alpha edges. Reconstruct the native pose in three dimensions, without mirroring or reusing a walk stance. One complete isolated soldier, generous genuine transparent padding on a square canvas, no ground, floor, terrain, cast shadow, glow, text, frame or extra object. Keep all equipment and both boots within the compact native silhouette. This is frame zero only; do not make a sprite sheet.
```

## Corrección del primer intento

El primer intento añadió brillo al impacto. El maestro final aplica esta corrección; no se presenta el intento anterior como aceptado.

```text
Use case: precise-object-edit. Edit this exact transparent OpenFodder hit-pose sprite. Change ONLY the red hit mark: replace the two luminous/glowing red points and their glow halos on the upper-left back/shoulder with one small, flat, dark red fabric stain in the same location, with no emitted light or glow. Keep the entire soldier pose, silhouette, orientation, helmet, equipment, face, rifle, proportions, dark olive palette, moderate hand-painted shading, all body pixels outside the tiny red-mark area, generous padding, square composition and genuine alpha transparency unchanged. Do not enlarge the stain, add blood effects or redraw any anatomy. No cast shadow or backdrop.
```
