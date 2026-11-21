# Nado hacia delante y a la izquierda · 0x19

Dos poses provisionales en estilo C, generadas con ImageGen integrado a partir del ciclo derecho, C01 y la silueta local de esta dirección. El arte nuevo se distribuye bajo GPL-3.0-or-later. La forma y la continuidad se valorarán jugando con las seis direcciones.

Recorte compartido `[87, 358, 1216, 838)` y colocación `[1, 3, 15, 13)` en la celda 16×14. Se retiró la estela difusa del primer borrador con una edición de ImageGen. Se usó el camino existente de `build_soldier_batch.cpp` y `build_ordered_soldier_asset.cpp`. Cada manifiesto vincula solo la clave de M1P2 confirmada al reconstruir la fila original. El original nativo queda local.

## Prompts

F0

```text
Use case: stylized-concept. Create one RGBA game sprite, OpenFodder style C soldier swimming towards the bottom-left (southwest), genuine front three-quarter view with nose pointing down-left and water streaming towards the upper-right; crown center in left half of the sprite, 19/F0. Reference 1 is the exact native silhouette and facing direction. Reference 2 is the provisional modern swimmer, use its C style, helmet size, waterline and subtle wake as identity and technique reference. Reference 3 is C01 with the approved olive palette and equipment. Keep the same steep oblique strategy-game camera. Redraw the soldier in the exact new orientation from reference 1 as a three-dimensional turn, without mirroring the image or reusing the right-facing artwork. Helmet, mask of face where visible, shoulder(s) and a hand above the surface, torso and boots submerged, slight stroke extending as shown by the native reference. Put the crown and leading shoulder in the same parts of the game cell as reference 1. Soft broken grey-green wake stays low and narrow, fading to transparency with gaps. Head size and color remain continuous with the modern reference. One isolated character. No solid water backdrop, river landscape, floating island, rifle, legs, ground, shadow or text. Genuine transparent background and padding.

Ajuste: Use case: precise-object-edit. Keep the OpenFodder southwest swimmer body and olive helmet exactly as in this transparent sprite. Remove absolutely all of the large translucent grey water sheet, spray halo behind the helmet, perimeter speckle, luminous outlines and cyan/green fringe. Keep only a narrow muted green-grey foam crease directly touching the body at the waterline and three small completely separate trailing ripples to the upper right. Everything else, including the area behind the head and both sides of the character, must be fully transparent alpha zero. Keep the helmet, face, hand, orientation, overall scale, and C painterly material unchanged. Leave enough margin to contain the whole body and tiny wake. Transparent game sprite, no backdrop or terrain.
```

F1

```text
Use case: identity-preserve. Edit reference 1 (the new OpenFodder swimmer down-left (southwest), front three-quarter, with only narrow touch foam and separate trailing ripples, no translucent water sheet F0) into 19/F1. Reference 2 is the exact second native frame. Keep the crown, helmet, olive palette, face or back view, body anchor, shoulder size, viewing angle, and waterline exactly where they are on the same canvas. The torso stays submerged. Only bring the leading hand closer to the body and change the subtle broken water ripples to the second stroke as indicated by the native silhouette. No redrawing the character, camera shift, scale change, terrain, solid backdrop, feet, rifle, text, or cast shadow. Genuine transparency including between small grey-green wake shapes. Match the two-frame cycle with contact alignment.
```
