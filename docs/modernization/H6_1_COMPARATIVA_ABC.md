# H6.1 — comparación A01 / B01 / C01

27-10-2026. Tres propuestas conceptuales presentadas en el chat. Actualización: Miguel ha elegido C — Pintado moderado, con diferencia; A descartado. H6.2 cerrado. La integración sigue siendo experimental. Imágenes generadas con imagegen; A01 y C01 usan la lámina B01 refinada como referencia. Sin imágenes comerciales de entrada.

| Propuesta | Lo observado | Ventaja propuesta | Riesgo a comprobar |
|---|---|---|---|
| A01 — Píxel refinado | Bordes escalonados y grupos de píxeles visibles; carácter retro más marcado | Continuidad estética con la tradición del juego | No es un atlas pixel-perfect: falta retícula coherente y escala nativa |
| B01 — 2D ilustrado limpio | Superficies más uniformes y suelo menos texturado | Equilibrio entre renovación y claridad | Puede parecer demasiado suave o de juguete; revisar proporciones del casco |
| C01 — Pintado moderado | Pinceladas en casco, suelo y vegetación; volumen más orgánico | Más calidez y carácter pictórico | El detalle puede perderse al reducir o competir con los actores |

## Dictamen de revisión inicial (superado por la elección C)

Recomendación del asistente: B01 como punto de partida, por el equilibrio observado entre claridad y renovación. A01 es la alternativa si Miguel prioriza continuidad retro. C01 es preferible si el acabado pictórico resulta prioritario, condicionado a conservar legibilidad. Son juicios visuales, no mediciones ni resultados de rendimiento.

Las tres láminas mantienen aproximadamente pose, cámara, distribución y colores de referencia, pero no son imágenes idénticas salvo por el estilo: hay pequeñas variaciones de contorno y detalle. Las miniaturas son orientativas generadas, no reducciones instrumentadas ni capturas del motor. No comparar su atractivo ampliado como si demostrara legibilidad en juego.

Se han presentado las tres direcciones acordadas. H6.1 continúa parcial hasta comprobar a escala real la dirección que se elija. La recomendación inicial B del asistente queda superada por la elección explícita C de Miguel. H4 conserva su estado y el código validado 46c180be; este incremento solo registra trabajo visual.

## Condiciones del siguiente paso

La dirección C ya fue elegida y la pose descrita en H6_3_POSE_C01.md ya está implementada. El criterio aplicado fue preparar un único recurso con transparencia, anclaje y proporciones medidos contra el original. Probarlo sobre fondos claros/oscuros y en un encuadre real, con sombra separada cuando corresponda. Conservar fallback clásico y H3; la integración de arte distinto necesita un contrato explícito de diferencias visuales autorizadas.

## Prompt A01

```text
Use case: style-transfer. Create candidate A01 by changing ONLY the art rendering style of the attached B01 game concept sheet to refined pixel art. Preserve EXACT same sheet layout, Spanish captions except subheading, same soldier identity, overhead oblique view, helmet/body proportions, rifle aimed lower-right, pose, foot positions and shadow extent. Preserve the SAME jungle tile map: tree at upper-left, fern border, rock lower-left, diagonal tan path and soldier at center-right; preserve relative sizes and camera. All three soldier depictions must use the same pixel-art treatment. Replace subheading with exact text 'A — Píxel refinado'. Keep header 'H6.1 · PRIMERA PROPUESTA', labels 'Soldado · vista ampliada' and 'Reducción orientativa', footer 'Concepto visual · No integrado en el motor'.
Rendering: authentic deliberate hand-crafted 2D sprite pixel art, clearly visible square pixel clusters, hard pixel edges without anti-aliasing or fuzzy shading. The enlarged isolated soldier must look like a small sprite enlarged with nearest-neighbor, roughly 48 pixels high before enlargement; not an HD illustration with a pixel filter. Restrained olive green, khaki, brown, dark charcoal palette; 3 tonal steps per material, readable compact silhouette and minimal facial marks. Jungle uses chunky organized pixel clusters with quieter floor and grouped foliage, not detailed noise. Keep page typography smooth and professional; pixel treatment applies to artwork only. No new objects, no cinematic perspective, no UI, no grid overlay, no invented actual game scale claims. This is a comparative concept, not exported production art.
```

## Prompt C01

```text
Use case: style-transfer. Create candidate C01 by changing ONLY the art rendering style of the attached B01 game concept sheet to restrained hand-painted 2D game art. Preserve EXACT same sheet layout, Spanish captions except subheading, same soldier identity, overhead oblique view, helmet/body proportions, rifle aimed lower-right, pose, foot positions and shadow extent. Preserve the SAME jungle tile map: tree at upper-left, fern border, rock lower-left, diagonal tan path and soldier at center-right; preserve relative sizes and camera. All three soldier depictions must use the same painted treatment. Replace subheading with exact text 'C — Pintado moderado'. Keep header 'H6.1 · PRIMERA PROPUESTA', labels 'Soldado · vista ampliada' and 'Reducción orientativa', footer 'Concepto visual · No integrado en el motor'.
Rendering: modest hand-painted gouache-like 2D game artwork, gently varied surface tones, broad controlled brushstrokes, soft but readable volume, slightly organic edge transitions. This must be visibly more tactile and painted than clean illustrated B01, but remain low-noise and legible when small, no photorealism, no cinematic lighting, no 3D render. Keep compact helmet, body and rifle silhouette. Jungle uses broad painterly leaf and ground shapes rather than many tiny speckles; the floor remains quiet. Same muted olive/khaki/dark charcoal color hierarchy. No thick outline, no extra props, no background expansion, no UI. Keep page typography smooth and professional. Do not invent scale measurements or claim actual game size. This is a comparative visual concept, not production art.
```

B01 y sus prompts: [primera muestra](H6_1_MUESTRA_B01.md). Los cuatro PNG originales se conservan en la [galería del repositorio](../../assets/modernization/concepts/README.md), con SHA-256 y sin recodificar; no se añaden al paquete ejecutable.
