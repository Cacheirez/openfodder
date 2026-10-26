# H6.1 — primera muestra B01: 2D ilustrado limpio

26-10-2026. Propuesta conceptual presentada a Miguel en el chat del proyecto. No integrada en el motor, no aprobada como estilo final y no equivalente a un atlas utilizable.

## Qué se ha preparado

Una lámina con el soldado ampliado, el mismo motivo en un fragmento de jungla y una reducción orientativa. Se ha generado con la herramienta integrada imagegen, sin usar recursos comerciales como entrada. La primera versión resultó demasiado texturada; la segunda simplifica el suelo y las masas de vegetación para reducir el ruido visual. La segunda versión es la muestra B01 de revisión.

La imagen se conserva como imagen generada en la conversación; este documento conserva el brief, los prompts y el dictamen. No se añade al paquete ejecutable ni se referencia como recurso del juego.

## Lectura de la muestra

- Silueta compacta, casco oliva y arma oscura reconocibles.
- Sendero claro y vegetación agrupada separan mejor al soldado del fondo.
- La reducción permite una primera valoración visual, pero no es una captura del motor ni una comprobación de tamaño nativo, 2× o 4×.
- Quedan detalles y volumen en el uniforme; no representa todavía una especificación cerrada de paleta, sombreado o número de tonos.
- La proporción del casco y la inclinación de cámara deben compararse con el sprite original antes de adaptar un recurso. No se afirma correspondencia exacta entre las vistas generadas.
- La sombra dibujada es conceptual. Cuerpo, sombra, margen transparente y anclaje deberán definirse por separado según el contrato real.

## Estado del plan

H6.1 está parcialmente realizado: primera dirección B presentada. Faltan las variantes A (píxel refinado) y C (pintado moderado), comparables en pose y encuadre, y una prueba controlada a escala del juego. H6.2 sigue pendiente: Miguel elige tras revisar las muestras. No se ha tomado una elección de estilo en su nombre.

El piloto de sustitución actual utiliza exclusivamente gráficos originales y exige igualdad visual. Integrar arte nuevo requerirá un contrato distinto para las diferencias visuales autorizadas, conservando H3, posición/anclaje y fallback clásico. No se debe desactivar el contraste global para insertar esta lámina.

## Prompt de generación

```text
Use case: stylized-concept.
Create ONE professional game art direction concept sheet, landscape, for a careful modernization of the classic Cannon Fodder game. This is a visual proposal, NOT an engine screenshot and NOT a production sprite atlas.
Direction B: clean illustrated 2D. Original newly drawn artwork, no copied game assets. Preserve a small readable olive-uniform infantry soldier silhouette, oversized simple round green helmet, minimal face, dark boots, compact dark rifle held across chest pointed diagonally toward lower right. Relaxed ready stance, one single pose, feet together enough for a compact game footprint. View from steep overhead, classic near-top-down oblique 2D game view, NO horizon, NO isometric diamond, NO front-facing portrait, NO cinematic perspective. Character should feel modest and functional, not mascot or chibi toy. Flat crisp shapes with two or three restrained shading tones, subtle small contact shadow, no heavy black outline, no glossy 3D materials, no hyperrealistic military details.
Design a beautiful but restrained review sheet on warm offwhite background with dark forest-green typography and thin dividers.
Left half: a large isolated inspection drawing of that soldier, the same overhead view/pose as in the scene. Below it small clear Spanish caption 'Soldado · vista ampliada'.
Right half: a square compact jungle floor fragment seen with the EXACT same camera: subdued olive grass, a small earth path passing diagonally, dense fern border at upper edge, one compact broad-leaf tree canopy at upper left and one small grey rock. Same soldier at center-right standing on the path, only about 1/12 the tile width; silhouette readable against ground. Environment quieter and lower contrast than the soldier. No other soldiers, enemies, vehicles, interface or explosion. Beneath the tile, repeat a small reduced preview of the SAME scene composition with a plain caption 'Reducción orientativa'. Do not invent pixel measurements, scale ratios or a claim of actual game size.
Header exact Spanish text: 'H6.1 · PRIMERA PROPUESTA'
Subheading exact: 'B — 2D ilustrado limpio'
Footer exact text: 'Concepto visual · No integrado en el motor'
Keep layout spacious, refined and pragmatic. The sheet should make it easy to assess silhouette, readability, color hierarchy and restrained shadow, rather than showcase illustrative detail. No logos, no watermarks, no paragraphs.
```

## Ajuste tras revisión visual

```text
Refine this exact game concept sheet. Keep all Spanish text, layout, character identity, pose, camera, footprint and scene object positions unchanged. Make only the rendering style noticeably cleaner and flatter: eliminate camouflage patterns, painterly flecks and faceted texture from the soldier; use solid olive clothing with two restrained shadow tones, a simple smooth helmet, matte dark boots and rifle. Simplify the jungle floor very strongly into broad quiet olive grass areas and a clean tan path, with at most a few separated grass tufts; simplify foliage into larger grouped leaf silhouettes with less tiny detail. Maintain the muted forest palette but give the small soldier clearer value separation against the ground. No thick outline, no glossy 3D or sticker halo. Update both the main scene and reduced preview to match these simplifications. This is still a concept visual, not an engine screenshot or scale validation.
```

## Siguiente paso

Revisar la dirección B con Miguel y completar la comparativa acordada. Después, preparar un único recurso con transparencia y anclaje medidos contra el original, sin ampliar todavía el catálogo de animación o vehículos.
