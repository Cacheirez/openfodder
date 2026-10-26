# H4.4 — sustitución individual de pose con retorno al clásico

26-10-2026. Incremento sobre `d28d99f9`. Clásico por defecto; PR #1 abierto, en borrador y sin fusionar. Base clásica y referencias H3 sin cambios.

## Comportamiento

Con `OPENFODDER_CAPTURE_SOLDIER=1`, `OPENFODDER_REPLACE_SOLDIER_POSE=1` y auditoría/publicación de misión, el productor selecciona la primera pose compatible del soldado capturado. La decodifica una vez a una imagen indexada propia e inmutable con los gráficos originales. El índice cero es transparente; los demás conservan la paleta indexada y reciben el RGB efectivo de la escena, incluidos fades. No se generan ni publican imágenes comerciales.

La selección se conserva entre intervalos de producción de una misión. La clave exige escena, slot, generación, tipo, hoja, frame, animación, dirección, segmento, anclajes, dimensiones, paleta y versión/propiedad del recurso. La posición, cámara y altura se toman del comando actual: una pose válida puede moverse sin quedar pegada a la posición donde se capturó. El tick no selecciona una animación nueva ni ejecuta simulación.

La pausa o una escena no elegible descartan el registro y la selección; la reentrada selecciona de nuevo. Un cambio de escena también descarta la selección. Una generación o recurso incompatible dentro de la misma escena produce retorno al clásico, sin reasignar silenciosamente la pose a otro soldado. Una escena retenida antigua puede seguir componiéndose privadamente, pero no recupera autorización de publicación tras invalidarse su destino.

El compositor sustituye solo la operación Soldier compatible, en su orden y destino originales, mediante blit transparente de la imagen indexada. Las capas posteriores siguen pudiendo ocultarla. Los demás comandos conservan el raster clásico. La sustitución no modifica los buffers indexados del motor ni sus fondos guardados: compone en buffers privados y publica el resultado contrastado.

## Retorno y límites deliberados

La ruta opcional devuelve un fallo de compatibilidad **antes de escribir** si falta la pose, cambia la clave, se recorta su geometría, falta espacio de destino o los datos de la imagen son incompatibles. Esa operación se rasteriza entonces con su recurso clásico retenido. No se pierde el soldado ni se superponen las dos versiones.

Este piloto solo acepta geometría PC/Amiga8 completa y el mismo tamaño/anclaje del original, con dimensiones acotadas al área clásica. Comprueba extensión del recurso antes de decodificarlo. No implementa arte externo, escalado, interpolación, sombras, insignias, atlas nuevos ni el catálogo completo CD32. El siguiente paso visual necesitará decidir el recurso nuevo y un contrato explícito para diferencias de imagen autorizadas.

El contraste original sigue siendo obligatorio y se ejecuta primero. Después se comparan la composición sustituida, los fondos guardados y el RGB con el original. Como el piloto usa el mismo arte, toda diferencia es un error: **no se captura la excepción para ocultarla como fallback**. Las pruebas inyectan una pose con píxeles alterados para demostrar que la ruta sí dibuja y que el contraste rechaza su corrupción.

## Reproducción

```bash
python3 tools/modernization/check_soldier_pose.py
python3 tools/modernization/check_mission_recording.py
python3 -m unittest discover -s tools/modernization -p 'test_*.py'

SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy \
python3 tools/modernization/check_mission_publication_replays.py \
  --exe build/openfodder --data Run --out reports/h4-pose-full --pose-probe
```

`--pose-probe` activa también la captura y exige una marca `SOLDIER_POSE: verified replacement scene=…` por fase. La mera finalización o el fallback permanente no satisfacen esa puerta. Sin la opción, el runner desactiva explícitamente la sustitución. Para la matriz acotada añadir `--presentations 0|1|5 --pause-probe --first-phase`.

Linux CI añade once fases con H3 original y pausa 0/1/5 acotada. Windows añade pausa 0/1/5 acotada. Los recorridos acotados de sanitizadores incluyen la sustitución. Se mantienen los recorridos anteriores de captura sin sustitución. Son pruebas de vídeo software, no aceptación manual de Windows/GPU o campaña CD32.

## Evidencia de este incremento

- `check_soldier_pose.py`: PASS local, 46 casos PC/Amiga con ASan/UBSan. Incluye movimiento/cámara/altura, anclajes, transparencia, cambio real de píxeles, fallos sin escritura parcial, recursos retenidos y orden de capas. Además rechaza recursos truncados y prueba el compositor con sustitución y fallback.
- `check_mission_recording.py`: PASS local, ocho configuraciones (sustitución apagada/encendida, clásico y publicación 0/1/5), 192 escenarios y 384 transiciones. La huella lógica sigue siendo `15155017350506417091` en todas. Ejecuta productores y coordinadores reales con dobles de SDL/simulación; incluye pausa, liberación de recursos, destinos reemplazados y rechazo de una pose corrupta.
- 29 pruebas Python PASS, incluida la puerta que rechaza cobertura de sustitución ausente o duplicada.
- Contrato de visibilidad y referencias de capacidades CD32: PASS; ninguna referencia H3 regenerada.
- ASan/UBSan locales con `detect_leaks=0` por la limitación local de LSan previamente documentada. CI mantiene LSan y TSan; no se atribuyen a estas fixtures resultados de motor completo.
- CI del padre `d28d99f9`: Windows [40374586200](https://github.com/Cacheirez/openfodder/actions/runs/40374586200) completed/success. Linux [40374585563](https://github.com/Cacheirez/openfodder/actions/runs/40374585563) seguía en instalación de dependencias al consultar; no se declara aprobado. Su log aún no estaba disponible (404 del servicio de logs).
- CI del código de este incremento: pendiente de publicación/ejecución. No hay build completo local nuevo: las dependencias SDL temporales de la sesión anterior ya no están disponibles. La aceptación del motor y H3 depende de su CI.

H4 permanece abierto. Tras aprobar la CI, siguiente entrega: muestra visual de una pose con anclaje explícito y selección de concepto H6.1, conservando la salida clásica.
