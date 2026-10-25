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

`check_mission_publication_replays.py` ejecuta PC Format y Amiga The One con vídeo software y publicación activa, exige las marcas de publicación y contraste, cero omisiones y 8+3 fases; compara las trazas con los 11.361 estados de H3 original. Conserva hashes de ejecutable/fixtures/configuración, logs, trazas y reportes. La CI ejecuta las 11 fases con el motor normal y ASan/UBSan/LSan. TSan usa `--first-phase`: dos fases explícitas (PC m1p1 y Amiga m1p1), 301 estados del mismo H3 original. La suite TSan headless habitual sigue exigiendo sus 29 fases. Un resultado pendiente no se considera aprobado.

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

Pruebas focalizadas locales ASan/UBSan: PASS; LSan local desactivado por la restricción de `/proc`, CI conserva fugas activadas. 15 pruebas Python: PASS. El motor `1e1f93d3` pasó Windows, publicación real 11/11 y H3 original, y ASan/UBSan/LSan con publicación activa; Linux falló en TSan activo por timeout. La revisión `acfc099a` mantiene la publicación y refuerza/acota la prueba como se describe abajo; su CI está pendiente hasta registrar resultados.

H4.3 sigue parcial y H4 abierto: falta 0/1/N del motor completo, transición misión↔pausa interactiva con la nueva ruta, más escenas/cargas, mediciones comparables de coste/retención y Windows/GPU real. Los replays nuevos usan la cadencia heredada; no se presentan como 0/1/N integral. La batería focalizada de pausa conserva sus dobles y no prueba por sí sola la transición interactiva del motor. Tampoco hay prueba nueva de las 72 fases CD32.

Siguiente paso tras validar este incremento: introducir programación de presentación de prueba 0/1/N en el motor, preservando la producción y las coordinadoras, comparar estados H3 y ampliar la transición de pausa. Después, estados semánticos de cámara/entidades para H5. No activar por defecto ni introducir interpolación/arte antes de las puertas del plan.

## Diagnóstico del primer intento y alcance de la corrección

`1e1f93d3`: [Windows 40201830489](https://github.com/Cacheirez/openfodder/actions/runs/40201830489) aprobado; [Linux 40201830487](https://github.com/Cacheirez/openfodder/actions/runs/40201830487) **FAIL**, exclusivamente en publicación activa con TSan. [Informes íntegros y límites](evidence/1e1f93d3-reports.json).

- Publicación normal: PC 8 fases/61,905 s; Amiga 3 fases/53,786 s. H3 original: 11.361 estados iguales.
- Publicación ASan/UBSan/LSan: PC 8 fases/694,409 s; Amiga 3 fases/347,246 s. H3 original igual. Todos los engine.log del artefacto inspeccionados sin avisos de los sanitizadores buscados.
- TSan habitual sin vídeo: 29 fases/152,639 s, PASS. TSan con publicación activa agotó 1.200 s en PC; Amiga no llegó a ejecutarse. El log stdout estaba almacenado en buffer: el informe contó cero fases completadas, pero las trazas completas de PC m1p1, m2p1 y m2p2 coinciden con sus 152+787+1.270 estados originales. m3p1 quedó incompleta; sus 1.276 estados completos coinciden con el prefijo de la publicación normal. Esto prueba avance, no éxito de la campaña ni ausencia universal de carreras.

No se amplió el timeout ni se desactivó TSan. En `acfc099a`, el ejecutor de pruebas permite `OPENFODDER_TEST_FIRST_PHASE=1` exclusivamente para terminar después de la primera fase completada en el modo de diagnóstico; no modifica la simulación, el contenido de esa fase ni los controles del juego normal. El runner activa esa variable solo con `--first-phase`, registra el alcance parcial y compara exactamente los dos nombres y hashes seleccionados del fichero H3 original. El selector se guarda en el informe; no se reescribe ningún golden del repositorio. Las demás invocaciones mantienen la cobertura completa.

El control nuevo rechaza diagnósticos ASan/UBSan/LSan/TSan aunque el proceso termine con código cero. Dos pruebas Python comprueban los avisos recuperables y las marcas válidas; además, UBSan se configura para detener la ejecución ante el primer error.

Los tiempos muestran un coste elevado bajo instrumentación; no son una medición controlada de rendimiento de juego. H5.1 permanece pendiente y no se activa la opción por defecto. Ampliar TSan activo a más fases queda como cobertura pendiente, no como una suite completa aprobada.

## Conservación de evidencias

Los ZIP completos de Windows y Linux de `b34373b0` están conservados en `OPENFODDER_EVIDENCIAS_b34373b0.zip`, con [manifiesto SHA-256](evidence/b34373b0-archive.json). También se conserva `OPENFODDER_EVIDENCIAS_1e1f93d3.zip`: incluye el intento fallido de TSan, logs y trazas parciales, además de las pruebas aprobadas. Ninguno contiene datos comerciales. C1 sigue abierta para referencias anteriores y siguientes revisiones.

## Revisión en curso

`acfc099a43d02d55bf44426b6c05a2f0330cf889`: [Linux 40225314495](https://github.com/Cacheirez/openfodder/actions/runs/40225314495), [Windows 40225314591](https://github.com/Cacheirez/openfodder/actions/runs/40225314591). Windows aprobado e inspeccionado: 6 CTests, 29 fases sin omisiones, H3 original de 11.361 estados. Linux sigue pendiente, observado aún en instalación de dependencias; no se hereda un aprobado global del intento anterior. [Evidencia](evidence/acfc099a-reports.json). Cambios frente a `1e1f93d3`: control de sanitizadores y alcance explícito de la prueba, sin cambios en el compositor ni en la publicación.

## Cierre de la validación de acfc099a

Linux 40225314495 y Windows 40225314591 aprobados. Archivo Linux comprobado por SHA-256 e integridad; todos los informes PASS y logs sin diagnósticos de sanitizador. Publicación normal: PC 34,761 s/8 fases y Amiga 31,707 s/3 fases; publicación ASan/UBSan/LSan: 398,944 s y 198,676 s, con 11.361 estados originales. TSan activo acotado: PC m1p1 30,817 s, Amiga m1p1 37,479 s, 301 estados originales. Los 29 replays headless TSan siguen aprobados. [Evidencia completa resumida](evidence/acfc099a-reports.json). Esta decisión sustituye el estado pendiente anterior, sin borrar el intento fallido 1e1f93d3.

Se acepta el incremento opcional en este alcance y se continúa con [programación 0/1/5 de misión](H4_6_PLANIFICACION_MISION.md). No es cierre global de H4 ni validación de TSan sobre toda la campaña con vídeo.
