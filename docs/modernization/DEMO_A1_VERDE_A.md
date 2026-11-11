# A.1 — verde A en las 80 poses

El 12 de noviembre de 2026 se aplicó en un solo lote el verde oliva A a las 68 poses pendientes. El candidato contiene 24 poses de marcha, 8 de apuntado, 24 de granada y 24 de lanzacohetes. Los 12 maestros de marcha ya ajustados se conservan.

La transformación aplica los factores RGB `(0.77, 0.90, 0.83)` ponderados por la máscara cromática del uniforme. Los recortes se toman de cada maestro aprobado. Las máscaras delimitan las granadas en mano y el tubo del lanzacohetes para proteger sus tonos oliva. Los manifiestos conservan las rutas y hashes de los originales y registran por separado los nuevos maestros y sus hashes RGBA.

## Comprobaciones

- Frente a `edcba828e536049164d5424c71a378bf103e178c`, los 160 activos conservan sus dimensiones, anclajes y canal alfa byte a byte. Solo cambia el RGB de los 136 derivados esperados. Las 318 vinculaciones conservan claves, destinos y orden.
- La reconstrucción del candidato con los builders existentes verifica los hashes RGBA a 8×/12×. SHA-256 de `candidate-manifest.json`: `a68128301e073a714c46e4eee49e92158ff29584a53efcd420156f883b27902d` (Windows).
- Revisión visual interna de las 80 poses a ambas densidades mediante láminas antes/después. Se cotejaron los frames y las direcciones de cada familia, junto a los verdes ya aprobados de marcha 4–7.
- SDL Windows x64 por software: marcha controlada 256 intervalos, marcha nativa 236, apuntado nativo 600, granada nativa 1.260 y lanzacohetes 12.672 controlados y 11.880 con recursos nativos. Ambas densidades, dos cuerpos, recortes y oclusiones en marcha, transiciones y tres rechazos por pasada. Los casos nativos combinan marcha observada con claves de las demás familias reconstruidas desde sus recursos.
- Aceptación jugando, GPU, CD32 y cobertura completa de campaña **PENDIENTES**. El recorrido nativo de lanzacohetes omite 18 parejas de secuencias por dos claves de marcha Amiga ausentes. Se conserva la evidencia previa de H3 y sanitizadores. El piloto y el lanzador conservan su configuración.

## Reproducción y recuperación

Con Pillow 11.3.0 y los builders de la rama:

```powershell
python -B tools/modernization/prepare_uniform_a.py --out <directorio-nuevo> --c01-builder <art-builder> --batch-builder <batch-builder> --asset-builder <ordered-asset-builder>
python -B tools/modernization/prepare_rocket_art.py --out <candidato-nuevo> --c01-builder <art-builder> --batch-builder <batch-builder> --asset-builder <ordered-asset-builder>
```

El primer comando reproduce los 68 PNG añadidos y comprueba los hashes anotados. Para marcha 4–7 se conservan los [comandos específicos y resultados anteriores](../../assets/modernization/soldier-walk24/uniform-a/README.md). Para recuperar la apariencia anterior del candidato se puede reconstruir desde `edcba82` en un checkout independiente.

Evidencia local en `C:/Users/migue/.codex/visualizations/2026/11/11/01a1ccf2-ba36-78a2-8403-b24f50437a5c`: láminas `{familia}-{0,4}-{8,12}x.png`, comparación de los 160 activos en `comparacion.json` y resultados SDL en `qa-*/validation.json`.
