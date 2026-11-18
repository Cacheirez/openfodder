# SOMBRAS-HD-PILOTO — marcha frontal 0x00/F1

18-11-2026. Una sola clave nativa, dos densidades. **Muestra provisional técnicamente comprobada; pendiente de valoración visual de Miguel.** Sin activación en el lanzador normal, sin motor nuevo ni extensión a otras poses.

`shadow-source.png` es el maestro RGBA inmutable generado con `image_gen` integrado. Referencias: raster nativo frontal y derivado HD actual, ambos locales; no se redibuja el cuerpo. El maestro es solo la pintura de sombra. `compose.cpp` es una herramienta de autoría offline que combina cuerpo existente sobre esa sombra y limita los cambios a la máscara nativa de esta pose. No forma parte del motor. `window-cases.inc` contiene las pruebas focalizadas, utilizando el fixture real de Window/SDL existente.

Los PNG/RGBA finales de 128×112 y 192×168 viajan como **un solo activo del mismo comando corporal nativo**. Ningún píxel opaco del cuerpo ni ninguno fuera de la máscara cambia. `manifest.json` conserva hashes, máscara, recorte explícito del maestro, cuerpos originales por densidad, prompt y resultados. No generalizar esta máscara ni este offset a otras poses.

[Informe y reproducción](../../../docs/modernization/SOMBRAS_HD_PILOTO.md). Las referencias nativas y la comparativa sobre fondo del juego permanecen locales, fuera de Git.

## Prompt exacto

```text
Generate ONLY one painted ground-contact SHADOW PLATE for a moderate painted overhead tactical game sprite. Reference1 is exact native frontal soldier with its dark shadow visible below/right; reference2 is the HD body, for scale/context ONLY and must NOT be redrawn. Output NO SOLDIER, no body, boots, gun, objects or ground. Only an isolated flattened irregular shadow silhouette, about 7 units wide by 3 units high, skewed to right: upper edge widest, left edge starts a little to the left of centre; rounded right edge, narrower short lower tip towards right. Match the dark patch under the native feet in reference1, not a generic symmetrical ellipse. Soft restrained hand-painted olive-black translucent contact shadow, denser central contact and slightly softened perimeter, no glow, blur cloud or directional long drop shadow. Single compact shape in centre of square truly transparent canvas with generous padding, no checkerboard pixels. Native mask and placement will be applied by the deterministic game asset builder; this is only the shadow paint master. It will be composited behind the unchanged HD body in the SAME native sprite command.
```
