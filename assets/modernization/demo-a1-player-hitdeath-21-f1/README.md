# Herido prolongado / daño con override 0x21/F1

21-11-2026. Producido dentro de PROTAGONISTAS-COMPLETOS, con criterio artístico delegado por Miguel. Inspección interna y exportación comprobadas; no declara aceptación visual/jugable global de Miguel. El lanzador anterior sigue intacto; se integra en el candidato v3 aislado.

Maestro original inmutable `source.png`, generado con image_gen integrado y transparencia. Referencias: pose nativa reconstruida de la hoja completa, C01 y el maestro 0x29/F0 para identidad/paleta; F1 reutiliza además el nuevo F0. Nativos privados en el atlas local `player-catalog-verified/native/`. No se reflejó arte ni se generó una hoja de poses. Las cajas nativas y los hashes figuran en `manifest.json`. Exportación exacta con los constructores existentes; 16×14 lógico, 8×/12×. Sangre y sombra permanecen comandos independientes, sin sombra de suelo añadida al cuerpo.

64 casos Window/SDL por plataforma para la dirección completa: PC/Amiga, F0/F1, animación 1/10, 8×/12×, dos actores, altura/recorte/oclusión de cero, alias de color no usado, negativos y recuperación SDL. PASS Windows ASan/UBSan y Linux ASan/UBSan/LSan. H3 de R2 sigue válido: no cambia código de simulación ni referencias.

## Prompt

```text
Create ONE transparent OpenFodder protagonist sprite master, native sheet0x21 frame1, the second frame of the prolonged wounded/bleeding Die5 cycle. Reference1 dictates the EXACT new pose/silhouette/orientation. Reference2 is the matching frame0: preserve the same character, helmet/body proportions, olive fatigues, tan straps/pouches, brown boots, muted small dark red fabric scuffs, moderately painted C01 facets, steep overhead camera. Do NOT repeat frame0. Native frame1 has helmet/head shifted toward the upper-right relative to the body, torso hunched/unbalanced beneath it toward the lower-left, one arm extended a little screen-left beside the waist, legs splayed/bent in the native stagger. Make that small visible wounded sway, not a normal stride or a flat corpse. Whole compact figure, complete limbs; native bright red accents become irregular subdued dark red cloth scuffs, no red band/badge/glow, no gore or exposed wound. No protruding rifle or invented props. Single whole figure centered with generous square transparent padding, true transparent alpha. No cast ground shadow because the engine keeps native shadow as an independent ordered command. No ground, scene, text, mirroring, duplicate poses or sprite sheet.
```
