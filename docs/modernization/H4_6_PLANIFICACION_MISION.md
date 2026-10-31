# H4.6 — Programación 0/1/5 de presentación de misión en el motor

25-10-2026. Continúa la publicación opcional aceptada en `acfc099a`, con Windows/Linux aprobados y TSan activo acotado a PC/Amiga m1p1 (301 estados). PR #1 en borrador, sin fusionar; base clásica intacta.

## Contrato implementado

En modo de pruebas (`mUnitTesting`), con `OPENFODDER_PRESENT_MISSION_LAYERS=1`, `OPENFODDER_TEST_MISSION_PRESENTATIONS` admite exactamente `0`, `1` o `5`. Ausente equivale a una presentación; otros valores producen error cuando se evalúa el control. Fuera de pruebas o sin la publicación opcional, se ignora y se conserva una presentación.

Solo se programa la ruta elegible de misión dentro de `Video_SurfaceRender`: sin pausa/overview/callback, destino principal, formato indexado y parámetros de recorte habituales. Cada llamada ejecuta cero, una o cinco veces el bloque completo: conversión/composición, aplicación/subida, RenderAt y FrameEnd. No se limita a repetir un cálculo sobre un vector privado. Con cero se verifica igualmente el registro en el punto tardío de paleta, además del contraste de interrupción.

Los productores, la simulación, `Save/Restore`, los eventos, `mVideo_Ticked/mVideo_Done`, los bloqueos y las esperas siguen fuera de ese bucle y en sus puntos originales. No se introduce un hilo, no se multiplica la frecuencia lógica y no se cambia la entrada de los replays. El modo clásico y los gráficos se conservan.

Esto prueba distintas cantidades de presentaciones **por llamada de misión** con el motor completo; no introduce un reloj de render independiente, interpolación ni una garantía sobre cualquier frecuencia/escena. Las pantallas no elegibles y el bucle interactivo de pausa siguen presentándose normalmente.

## Pruebas

`check_mission_recording.py` compila los cuerpos reales con hooks y scheduler activos. Ejecuta 24 escenarios por configuración: clásico (variable 5 ignorada), opcional 0, 1 y 5. Las llamadas programadas producen respectivamente 48, 0, 48 y 240 presentaciones; las verificaciones adicionales de fallback y guardas se contabilizan aparte. Comprueba el número real de FrameEnd/RenderAt, todos los píxeles, invariancia lógica, recursos destruidos y la detección de una escritura omitida en el modo cero. Las guardas de pausa, overview, fuera de misión, juego normal y recorte alternativo conservan una presentación.

Las pruebas históricas normalizan únicamente la función programada exacta hacia la función anterior, y después los hooks ya inventariados. El test de registro ejecuta la función nueva completa; las restantes coordinadoras/productores siguen protegidas por comparación con su referencia histórica. Se mantienen las pruebas diferenciales de misión/pausa 240/672 y pausa 144.

`check_mission_publication_replays.py --presentations N` fija el entorno, registra N en el hash de configuración y exige la marca del scheduler. N=0 exige contraste activo y ausencia de la marca de publicación; N>0 exige publicación y contraste. En todos los casos se exigen los nombres/cantidad de fases y sus huellas originales, sin rebaselinar. El runner elimina una variable de scheduling heredada si no se le pide explícitamente.

La CI mantiene la ejecución normal (una presentación) y añade cero/cinco sobre las 11 fases públicas: 8 PC Format y 3 Amiga The One, 11.361 estados por política. Se conservan ASan/UBSan/LSan con publicación activa y TSan de dos fases a una presentación, además de los 29 replays sanitizados habituales. No se atribuye a los sanitizadores una batería completa 0/1/5 que no ejecutan.

## Reproducción

```bash
python3 tools/modernization/check_mission_recording.py
SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy \
python3 tools/modernization/check_mission_publication_replays.py \
  --exe build/openfodder --data Run --out reports/h4-schedule-0 --presentations 0
```

Repetir con `--presentations 1` y `5`, usando directorios nuevos. Los reports y trazas declaran su configuración. No usar `--first-phase` para presentar una prueba como las 11 fases completas.

## Estado y trabajo restante

Local: fixture activa PASS bajo ASan/UBSan; pruebas históricas de misión y pausa PASS; 15 pruebas Python PASS. Motor `bd2b3d2`: CI Windows [40229859350](https://github.com/Cacheirez/openfodder/actions/runs/40229859350) y Linux [40229859389](https://github.com/Cacheirez/openfodder/actions/runs/40229859389) PASS, inspeccionadas el 26-10-2026. Las políticas 0/1/5 conservan los 11.361 estados H3 originales en 11 fases. Publicación activa ASan/UBSan/LSan: 11 fases; TSan: dos fases/301 estados. [Informes y hashes](evidence/bd2b3d2-reports.json). Los ZIP completos se conservan también en `OPENFODDER_EVIDENCIAS_bd2b3d2.zip`, fuera de la caducidad de Actions.

H4 permanece abierto. Siguiente: ampliar misión↔pausa con la ruta de órdenes y la programación real, recursos/superficies sustituidos y entradas/salidas de escenas. La batería de pausa histórica usa dobles: no equivale a una pausa interactiva real del motor. También siguen pendientes coste/retención medidos, Windows/GPU manual y estados semánticos de cámara/entidades para interpolación. No activar la opción por defecto.


## Ampliación del 26-10-2026: bucle de pausa unido a misión

La fixture de registro ahora ejecuta también el cuerpo real de `Phase_Paused`, sin normalizar sus hooks. Cada una de las 24 combinaciones PC/Amiga, padding, llamadas y semillas recorre dos transiciones misión→pausa→misión. En cada pausa se sustituyen y destruyen las tres superficies, primero con igual geometría y después cambiando su ancho, junto con sprites, atlas y panel. Se retiene el frame anterior y se comprueba que sigue siendo reproducible; al regresar, el intervalo nuevo usa los destinos y recursos actuales.

Se verifican tres presentaciones/eventos de pausa por transición, un único restablecimiento de paleta y redibujado final, invalidación del registro durante pausa, reapertura al volver y conteo 0/1/5 al presentar la misión reanudada. La huella de índices, backing, paletas y efectos coincide entre clásico y los tres modos opcionales: `15155017350506417091`, 48 transiciones por configuración, 192 en total. PASS local bajo ASan/UBSan; CI de esta ampliación pendiente. Esta huella compara variantes de la fixture, no sustituye a H3 ni se añade como golden del juego.

No cambia código del motor. `Draw_Phase_Paused`, entrada, selección de recursos y SDL siguen siendo dobles; no se afirma haber probado una pausa interactiva completa, GPU o una nueva cadencia dentro de pausa. El próximo incremento debe cubrir esa interacción en el motor completo antes de extender el scheduler a más escenas.
