# Herido prolongado / daño con override 0x21/F0

21-11-2026. Producido dentro de PROTAGONISTAS-COMPLETOS, con criterio artístico delegado por Miguel. Inspección interna y exportación comprobadas; no declara aceptación visual/jugable global de Miguel. El lanzador anterior sigue intacto; se integra en el candidato v3 aislado.

Maestro original inmutable `source.png`, generado con image_gen integrado y transparencia. Referencias: pose nativa reconstruida de la hoja completa, C01 y el maestro 0x29/F0 para identidad/paleta; F1 reutiliza además el nuevo F0. Nativos privados en el atlas local `player-catalog-verified/native/`. No se reflejó arte ni se generó una hoja de poses. Las cajas nativas y los hashes figuran en `manifest.json`. Exportación exacta con los constructores existentes; 16×14 lógico, 8×/12×. Sangre y sombra permanecen comandos independientes, sin sombra de suelo añadida al cuerpo.

64 casos Window/SDL por plataforma para la dirección completa: PC/Amiga, F0/F1, animación 1/10, 8×/12×, dos actores, altura/recorte/oclusión de cero, alias de color no usado, negativos y recuperación SDL. PASS Windows ASan/UBSan y Linux ASan/UBSan/LSan. H3 de R2 sigue válido: no cambia código de simulación ni referencias.

## Prompt

```text
Create ONE transparent OpenFodder protagonist sprite master, native sheet 0x21 frame0: prolonged wounded/bleeding Die5 and damage override, same fixed native pose in both uses. Reference1 is the EXACT original pose/silhouette/orientation; references2 and3 supply approved C01 moderately painted identity, olive green helmet and uniform, tan straps/pouches, brown boots, restrained painted facets and steep overhead oblique camera, NOT their poses. Follow reference1: compact whole standing wounded soldier, helmet high near centre, torso below, visibly unsteady bent knees, arms close to torso/waist. Preserve that native pose rather than turning this into a normal walk or lying corpse. Same helmet/body scale and olive palette as C01. Native bright red marks become small irregular subdued dark red fabric scuffs, no red belt/stripe/badge/glow and no exposed wound or gore. Avoid adding a long protruding weapon, accessory, environment or new action. Genuine transparent alpha, single whole figure centered with generous square transparent padding, clean complete silhouette and all limbs. No cast ground shadow (the native independent shadow command is retained), no ground, scene, text, framing, mirrored art, multiple poses or sprite sheet.
```
