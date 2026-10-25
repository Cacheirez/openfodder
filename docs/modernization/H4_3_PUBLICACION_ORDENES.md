# H4.3 — Presentación opcional desde órdenes verificadas

25-10-2026. Continúa el registro de `b34373b0` y el plan 2.20. PR #1 sin fusionar; base clásica conservada.

## Comportamiento

`OPENFODDER_PRESENT_MISSION_LAYERS=1` activa el registro y la publicación de misión desde sus órdenes, incluso si `OPENFODDER_AUDIT_MISSION_LAYERS` no está activado. Sin la nueva variable se mantiene la publicación clásica; la variable anterior sigue permitiendo auditoría sin sustituir la publicación.

Los productores clásicos siguen ejecutándose una vez y proporcionan el oráculo. En el punto original de conversión, el compositor toma la paleta efectiva, verifica índices, fondo guardado y RGB de los dos destinos, y entrega a `ApplyPresentation` exactamente el resultado RGB verificado de `mSurface`. No se vuelve a capturar el clásico para la nueva publicación ni se mezcla `mSurfaceFinal` con el destino visible. La comprobación de interrupción permanece activa, aunque no haya presentación.

La nueva opción está desactivada por defecto, no añade hilos, no cambia cadencias, RNG, reglas, goldens H3 ni recursos gráficos. Es un paso de integración, no la eliminación del productor clásico ni una optimización de rendimiento.

## Elegibilidad y fallos

Se mantiene la restricción del punto de misión: sin pausa, overview, callback, imagen cargada, shrink ni destino alternativo. Las demás rutas continúan clásicas. El registro se renueva por intervalo y se descarta en pausa como antes.

Antes de publicar se comprueban identidad, dimensiones indexadas y geometría/formato/extensión del destino RGB. Si falta el intervalo o el destino ya no es compatible, se descarta el registro asociado a los destinos recibidos y se permite la publicación clásica. El primer retorno emite `MISSION_LAYER_PRESENT: classic fallback (missing or incompatible interval)`.

Una divergencia dentro de un intervalo compatible lanza error: no se atrapa para esconderla mediante fallback. Tampoco se ignora un rechazo de `ApplyPresentation` posterior al contraste. El primer éxito emite `MISSION_LAYER_PRESENT: published verified orders`. Se conservan los locks y los puntos serializados del motor; esto no autoriza llamadas concurrentes arbitrarias a las superficies.

## Pruebas

La fixture ejecuta los cuerpos actuales con la opción apagada/encendida: 24 escenarios y 48 presentaciones programadas por modo; PC/Amiga, padding, 0/1/5, dos destinos, sprites/paleta tardíos, recursos liberados, Clear/Save/Restore, reinicio y detección de escrituras omitidas. Ahora invoca el productor preparado además del resuelto. Comprueba los píxeles recibidos por la ventana, no solo el resultado de una llamada aislada al compositor. Añade rechazo de destino sustituido, retorno clásico sin registro y nueva publicación tras reiniciar el intervalo. Las llamadas adicionales de fallback/reentrada se comprueban aparte del contador de 48.

Se mantienen las pruebas históricas diferenciales de misión/pausa (240/672), pausa (144) y destinos (97 aceptaciones/627 rechazos). `audit_contract.py` normaliza únicamente el bloque opcional exacto hacia la publicación anterior; el test de registro sigue ejecutando el bloque nuevo y comprobando que los productores/coordinadoras restantes no cambien.

`check_mission_publication_replays.py` ejecuta PC Format y Amiga The One con vídeo software y publicación activa, exige las marcas de publicación y contraste, cero omisiones y 8+3 fases; compara las trazas con los 11.361 estados de H3 original. Conserva hashes de ejecutable/fixtures/configuración, logs, trazas y reportes. La CI ejecuta este control con el motor normal, ASan/UBSan/LSan y TSan. Un resultado pendiente no se considera aprobado.

## Reproducción

```bash
python3 tools/modernization/check_mission_recording.py
SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy \
python3 tools/modernization/check_mission_publication_replays.py \
  --exe build/openfodder --data Run --out reports/h4-publication
```

Para activar manualmente la opción en PowerShell, dentro de una carpeta de juego comprobada:

```powershell
$env:OPENFODDER_PRESENT_MISSION_LAYERS = '1'
.\openfodder.exe
Remove-Item Env:OPENFODDER_PRESENT_MISSION_LAYERS
```

La variable afecta a procesos iniciados desde esa consola; al quitarla, los siguientes arranques vuelven al modo predeterminado. No se solicita todavía una nueva aceptación manual de este incremento.

## Estado y continuación

Pruebas focalizadas locales ASan/UBSan: PASS; LSan local desactivado por la restricción de `/proc`, CI conserva fugas activadas. 13 pruebas Python: PASS. Compilación/replays completos y sanitizadores con la nueva publicación: pendientes de la CI de este incremento hasta registrar sus resultados.

H4.3 sigue parcial y H4 abierto: falta 0/1/N del motor completo, transición misión↔pausa interactiva con la nueva ruta, más escenas/cargas, mediciones comparables de coste/retención y Windows/GPU real. Los replays nuevos usan la cadencia heredada; no se presentan como 0/1/N integral. La batería focalizada de pausa conserva sus dobles y no prueba por sí sola la transición interactiva del motor. Tampoco hay prueba nueva de las 72 fases CD32.

Siguiente paso tras validar este incremento: introducir programación de presentación de prueba 0/1/N en el motor, preservando la producción y las coordinadoras, comparar estados H3 y ampliar la transición de pausa. Después, estados semánticos de cámara/entidades para H5. No activar por defecto ni introducir interpolación/arte antes de las puertas del plan.
