# Ciclo de nado a la derecha, 0x1E/F0 y F1

Dos maestros provisionales del jugador en estilo C, generados con ImageGen integrado el 17 de noviembre de 2026. F0 usa C01 con verde A, el soldado de caída lateral y la pose nativa local. F1 parte de F0 y de la segunda pose nativa. El arte nuevo se distribuye bajo GPL-3.0-or-later.

Los dos maestros son RGBA 1341×1173. SHA-256 de [F0](source.png) `20fd4a9b96d2409123adbd8eb0b35e9a69c09ad457dedd63a644e6972f68aa1b`. SHA-256 de [F1](../demo-a1-player-swim-1e-f1/source.png) `90513721fb838ba6ed3176d162b543fbde7b32c1ee984fcd31c05d8dbc875157`.

Los dos frames comparten el recorte `[130, 330, 1238, 748)` y la colocación `[1, 3, 16, 11)` en la celda 16×14. Se fija la misma transformación para estabilizar el casco y la línea de agua, con un ligero cambio del brazo y de la estela. Se usa `build_soldier_batch.cpp` con colocación `1 15 8` y un traslado de tres filas hacia arriba. Los derivados PNG y RGBA se contrastan con `build_ordered_soldier_asset.cpp`. Cada manifiesto aporta un vínculo de M1P2, con geometría nativa de dos columnas y 14 filas y offsets 1696 (F0) y 1698 (F1).

Este ciclo sirve para revisar proporciones y línea de agua. La integración jugable del nado se programa cuando esté preparado el conjunto de direcciones que mejora la continuidad en los censos.

## Prompts de generación

F0

```text
Use case: stylized-concept. Make one top-down oblique transparent RGBA game sprite of the OpenFodder olive soldier swimming to screen-right, sheet 0x1E/F0. Reference 1 is its exact native silhouette and pose; reference 2 is C01 Style C palette and helmet; reference 3 is the accepted fall soldier's identity in profile-related motion. Show the SAME soldier wading/swimming across a natural dark river, side view toward EAST with helmet, profile, one shoulder and one forearm emerging above the water, body and boots fully submerged and hidden. Match native composition: crown and face in right half, shoulder lower, arm extended low toward the right edge at the waterline, tiny trailing broken ripples toward the left. Head stays upright with eye/face pointing horizontally right, no diving. Painterly moderate C with broad clean shapes, olive uniform and green helmet, quiet muted green-grey and cream hints for the narrow wake blending into transparent edges; leave the river itself transparent. Upper half and corners transparent. No solid water patch, straight hard waterline, ground shadow, rifle, background, text, arena or island. One figure only. It must read at 16×14: body submerged, helmet about five native pixels across, lower waterline held below the chin. Real alpha, generous transparent margins.
```

F1

```text
Use case: identity-preserve. Edit reference 1, the new OpenFodder swimming-right 0x1E/F0 master, into 0x1E/F1. Reference 2 is the target native second frame. Keep same olive helmet, face, crown angle, profile and proportions with no shift or rescale of head relative to the canvas. Keep the soldier facing exactly right, same elevated oblique game camera, identical painterly treatment and colors, same overall sprite size and waterline. Change only the stroke and surrounding ripple: emerging forearm and hand pull back close under the chin/right shoulder and sit mostly below the waterline, with a subtly different broken wake trailing left and a little splash near the right edge. The reach is shorter than F0 without moving the body. Preserve true transparent RGBA margins, no new terrain, river backdrop, rifle, island, text, borders or ground shadow. Output one isolated sprite only.
```
