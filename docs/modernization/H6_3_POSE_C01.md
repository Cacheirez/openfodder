# H6.3 — primera pose C01 transparente y prueba de anclaje

27-10-2026. Miguel elige C — Pintado moderado, con preferencia explícita sobre A/B. H6.2 queda cerrado. H6.3 sigue parcial: implementación experimental, CI nueva y valoración visual en juego pendientes. Motor clásico por defecto, PR sin fusionar.

## Recurso y correspondencia

Se ha generado una pose aislada RGBA a partir del concepto C01: uniforme oliva, casco, rifle y botas, sin escenario ni sombra incorporada. El motor conserva su sombra clásica. Fuente original y manifiesto: `assets/modernization/soldier-c01/`. La imagen no incorpora gráficos comerciales.

Objetivo verificable: hoja 7, frame 0, soldado normal Player, dirección de la hoja «derecha y hacia delante». Las tablas PC `stru_330FC[0]` y Amiga `stru_8C4A8[0]` declaran cuadro 16×14, modX=modY=0, offsets 2248/562. El raster Amiga usa dos columnas que producen 16 píxeles. La prueba comprueba los valores contra las tablas reales, sin modificarlas.

El generador C++ `build_soldier_art.cpp` decodifica el PNG, excluye la franja casi transparente inferior a alpha 16 y obtiene un cuerpo RGBA nativo mediante promedio de área y colores premultiplicados. El cuadro lógico sigue siendo 16×14; cuerpo en caja (3,0)-(13,14), referencia de pies (8,14), y origen lógico heredado (0,14). La cuantización a diez columnas de contenido es una aproximación de proporciones a esta resolución, no una escala HD definitiva. El anclaje usa la geometría actual del comando, incluida cámara/altura; no mantiene coordenadas del instante de captura. Se comprueba que no salta al sustituir.

Esta pose es una adaptación visual inicial: no se afirma coincidencia anatómica perfecta con el original. El detalle pintado se pierde en buena parte a 16×14; el PNG grande se conserva para una integración HD posterior. No se amplían el campo visible, colisiones ni dimensiones lógicas.

## Integración acotada

Activación opcional: `OPENFODDER_CAPTURE_SOLDIER=1`, `OPENFODDER_PRESENT_MISSION_LAYERS=1`, `OPENFODDER_SOLDIER_ART=1`. No necesita activar la sustitución indexada anterior. Los datos nativos se compilan en `SoldierArtPixels.hpp`: no hay carga externa durante la presentación.

Primero se ejecuta el contraste clásico completo existente: índices, Save/Restore y RGB. Después, el adaptador busca una sola operación Soldier compatible y del destino que se va a presentar. Retira únicamente ese cuerpo de una copia privada de la secuencia, recompone su fondo y mezcla la pose RGBA. Así las zonas transparentes muestran el fondo verdadero, no restos del cuerpo anterior. Solo se permite diferencia dentro del cuadro 16×14; una diferencia fuera del cuadro lanza error. El motor no recibe los índices ni los RGB modificados como estado de simulación.

La política de orden es conservadora: si cualquier operación posterior puede tocar el cuadro —incluidos cursor, otros sprites, HUD o escrituras de cero/OR— se conserva el clásico. Terrain/Clear/Save/Restore posteriores en ese destino también hacen fallback. No se añade la pose por encima de un obstáculo. Como máximo se sustituye una operación del primer soldado capturado, nunca otra dirección o frame para aumentar artificialmente la cobertura.

Otros retornos: recorte, tamaño o anclaje incompatible, animación especial, recurso original distinto, destino no válido, pausa/overview fuera del registro, fundido en curso y paleta negra. La fuente incorporada es inmutable y verificable; el compositor también admite recurso ausente para probar el fallback. Las discrepancias del contraste clásico siguen siendo errores, no motivos para ocultar divergencias.

## Pruebas y alcance

- Fixture de los métodos reales Begin/Record/Verify/Present de Surface, con SDL y recursos originales sintéticos: ASan/UBSan, PC/Amiga, cámara desplazada, pitch con padding, transparencia, huella lógica 0/1/5, pausa/invalidez, recurso retenido y rechazo de escrituras ajenas. Incluye 64 casos de retorno y comprobación de igualdad fuera del cuadro.
- Reproducción determinista del header RGBA a partir del PNG, y verificación de metadata original.
- Puerta Python exige al menos una sustitución efectiva en el recorrido declarado. Cada informe cuenta escenas realmente sustituidas por campaña. **No se exige ni se atribuye cobertura por fase:** una pose concreta puede no aparecer o estar siempre tapada.
- Runner `--art-probe` añadido al motor completo Windows/Linux con las once fases H3 originales. Esta CI nueva está pendiente; no se atribuye el verde del motor previo 46c180be a este cambio.
- Se conservan todas las rutas y pruebas anteriores. Sin aceptación manual Windows/GPU, sin prueba completa CD32 y sin validación HD. LSan/TSan nuevos para la ruta artística no se declaran aprobados: la fixture local usa ASan/UBSan con detect_leaks=0.

```bash
python3 tools/modernization/check_soldier_art.py
SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy \
python3 tools/modernization/check_mission_publication_replays.py \
  --exe build/openfodder --data Run --out reports/h6-art-full --art-probe
```

Siguiente: confirmar CI y revisar una captura del motor a tamaño real. Después fijar escala visual y ampliar el compositor RGB para oclusiones, en lugar de ampliar ahora las animaciones.
