# Piloto 0x2D/F1 — daño/muerte hacia atrás y a la derecha

17-11-2026. Estilo C — Pintado moderado. **Valoración visual favorable de Miguel (17-11-2026), F0/F1.** No incorporado al lanzador de juego; continuidad del conjunto pendiente.

`source.png` es la copia inmutable del maestro generado mediante la herramienta integrada `image_gen`, con alfa real. Maestro F0 provisional de esta dirección y referencia nativa local `death-2d-native/f1-native.png`. No se refleja arte. Los gráficos nativos se conservan fuera de Git. [Contexto, pruebas y anclajes](../../../docs/modernization/DEMO_A1_DANO_2D.md).

Los derivados tienen celda lógica de 16×14, a 8× (128×112) y 12× (192×168). Se exportan con `build_soldier_batch.cpp` y `build_ordered_soldier_asset.cpp`, sin retocar los píxeles del maestro. La colocación sigue el bbox nativo: [4, 1, 15, 12]. No contiene sombra proyectada; las sombras tipo 22 se mantienen como comandos nativos separados. `manifest.json` registra claves, hashes y estado.

## Prompt

```text
Use case: identity-preserve. Asset: exactly one transparent RGBA OpenFodder player hit/death pose 0x2D/F1. Image 1 is the new F0 master: preserve the same character, exact dark olive/tan/brown palette, helmet size and shape, equipment, proportions, moderate hand-painted Style C and steep overhead camera. Image 2 is the exact native SECOND pose: follow its silhouette and body-part arrangement rather than repeating F0. The hit animation shifts the helmet a little down and screen-right, the torso recoils and turns a little more toward the right edge, the front forearm/hand reaches further screen-right at chest level, and the bent legs shuffle toward the lower-left. Keep the body compact and visibly unbalanced by impact, not a regular running stride, not a prone corpse. Rear-right/northeast three-quarter facing; only a narrow right-side face/profile. Compact dark rifle held with the moving forearm close across the chest/right side as indicated by the grey/orange native marks, no long protruding barrel. Keep the restrained tiny dark red fabric mark on the left upper back/shoulder, flat and not luminous. Preserve the same soldier identity and head/body scale so the two frames read as one animation, while making the native frame-one limb and torso change clear. One isolated complete soldier with both boots inside a compact native footprint, square canvas and generous genuine transparent padding. No ground, cast shadow, glowing pixels, blood splash, scene, frame, text or extra object; do not mirror.
```
