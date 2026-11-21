# Daño/muerte 0x22/F1

Preparado el 17-11-2026 dentro del hito autorizado. Modelo C01 y diseño de daño 0x2D valorado favorablemente por Miguel; **esta dirección queda pendiente de revisión visual/jugable agrupada**. No activada en el lanzador normal.

Maestro inmutable `source.png`, RGBA, generado mediante `image_gen` integrado. Referencias: C01 verde A, maestro necesario de la dirección y los dos nativos locales `death-22-native/`. Las referencias nativas no se versionan. Derivados exactos con los constructores existentes, 16×14 lógico, 8×/12×. No incluye sombra proyectada: conserva comandos nativos independientes. [Avance y evidencia](../../../docs/modernization/DEMO_A1_DANO_DIRECCIONES.md).

## Prompts

f1

```text
Use case: identity-preserve. Make exactly one transparent RGBA OpenFodder player hit/death 0x22/F1 sprite. Image 1 is the new left-facing F0 master: preserve identity, helmet and head/body scale, dark olive uniform, tan webbing, brown boots, tiny irregular dark red upper-chest scuff, moderate painted facets and steep overhead camera. Image 2 is the exact native SECOND pose, whose silhouette and limb arrangement must drive this edit. The soldier has fallen/recoiled further backwards toward screen-right: helmet/head at upper-right, face still toward screen-left, torso and hips forming a strong diagonal down-left, knees and boots extending to lower-left. Compact raised arms bend toward the front/left of the chest as in the native; he is losing balance, not walking, aiming or lying flat. Make the change from F0 clearly visible, keep all limbs anatomically attached and compact. No rifle or weapon, no red bands or badges, no glowing pixels, exposed wounds or blood effects. One complete isolated soldier with genuine transparent padding on a square canvas; no ground, cast shadow, backdrop, text, frame or extra poses. Do not mirror or change style.
```

correctionF1

```text
Use case: precise-object-edit / identity-preserve. Correct only the lower-body pose of image 1 (0x22/F1). Its legs are too straight and stretched: bend both knees more, tuck the boots closer to the hips, and make the total body footprint more compact, following image 3's native second-frame silhouette. The soldier still recoils/falls backwards to screen-right, face points screen-left, helmet stays at the upper-right and boots toward lower-left. Image 2 is F0 and establishes the same character/head scale: preserve the absolute helmet/head size and all upper-body identity from image 1, without shrinking the whole figure. Keep face, hands, helmet, torso, olive/tan palette, tiny chest scuff, painting style, camera and alpha unchanged apart from natural hip/knee attachment adjustments. No weapon, red armband, badge, ground, cast shadow, text, glow or added effects. One sprite, same transparent square canvas and generous padding.
```

**Valoración posterior (18-11-2026):** Miguel aprueba esta dirección en la revisión agrupada. No equivale a aceptación jugando ni activa el candidato.
