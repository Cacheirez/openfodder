# H4.6 — Sonda acotada de pausa en el motor completo

26-10-2026. Continúa la fixture conjunta `cb0013e6`. No activa la presentación nueva por defecto; PR #1 en borrador, sin fusionar, base clásica intacta.

## Recorrido implementado

`--pause-probe` del runner fija `OPENFODDER_TEST_MISSION_PAUSE=1`. Solo funciona con pruebas, reproducción de demos y vídeo activo; se excluye grabación. Sin la opción, el runner elimina su efecto fijándola a cero. El hook reside en el punto de eventos del replay bajo el bloqueo existente de superficies. La lógica normal, el bucle de pausa y la ruta SDL no se reescriben.

En los ticks lógicos 8 y 16 de cada fase, la sonda envía pulsación/liberación de P a la cola SDL, pasa por `Window::Cycle` y `eventsProcess`, y comprueba la entrada en pausa. Otra pulsación/liberación queda preparada para la primera iteración de `Phase_Paused`. Se ejecutan los productores reales del texto, selección de recursos, fade, backing, aplicación de superficies, RenderAt/FrameEnd, eventos y redibujado al salir.

Durante la sonda se seleccionan temporalmente los eventos SDL en lugar de los del replay, restaurando el indicador con RAII. El bloqueo impide que el hilo de interrupción avance durante esta intervención de prueba. No se escribe el fichero de demo ni se inyecta una asignación directa a `mPhase_Paused`. Se comprueban reloj lógico, tick del replay y cuatro semillas RNG antes/después, invalidación del registro durante pausa y registro nuevo contrastado al volver. El runner exige exactamente dos pares únicos de entrada/salida por fase; un proceso con código cero sin cobertura sigue fallando.

## Alcance y reproducción

```bash
SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy \
python3 tools/modernization/check_mission_publication_replays.py \
  --exe build/openfodder --data Run --out reports/h4-pause-1 \
  --presentations 1 --pause-probe --first-phase
```

Repetir con 0 y 5 y directorios distintos. Son PC Format m1p1 y Amiga The One m1p1: dos fases, cuatro transiciones por política y 301 estados H3 originales. El scheduler sigue afectando solo a misión; cada pausa ejecuta una iteración real. No equivale a mantener una pausa larga, entrada humana, GPU, sustitución comercial de recursos durante pausa, concurrencia libre o toda CD32.

## Estado

Compilación local del motor completo con GCC/C++14 y dependencias SDL existentes: PASS. Control sin sonda: 301 estados H3 originales. Matriz normal 0/1/5: PASS, cuatro transiciones por política y H3 intacto. ASan/UBSan 0/1/5: PASS, cuatro transiciones por política y los mismos 301 estados H3. LSan no se ha ejecutado localmente. Pruebas focalizadas de registro y transición (192), pausa (144), misión (240/672), visibilidad y 16 pruebas Python: PASS.

CI añadida: matriz normal 0/1/5, ASan/UBSan/LSan y TSan a una presentación, siempre con dos fases explícitas. Se conservan las pruebas previas de 11 fases y 29 replays. CI propia pendiente.

El primer ejecutable local produjo una ejecución Amiga con código cero, una sola transición registrada y sin avisos de finalización: el gate la rechazó correctamente. Sus 149 estados trazados sí coincidían con el control. No se ha reproducido tras recompilar ni en la matriz posterior; no se atribuye una causa ni se declara corregida. Se conserva ese FAIL junto con los PASS posteriores en [evidencia local](evidence/pause-probe-local-2026-10-26.json). La aceptación de esta ampliación queda pendiente de CI y de resolver o delimitar esta anomalía de observabilidad.

Siguiente: revisar resultados de CI y la anomalía inicial; después ampliar duración/eventos de pausa y escenas. La sustitución/destrucción de recursos sigue acreditada por la fixture conjunta, no por esta sonda SDL.


## Resultado de CI — revisión del 26-10-2026

`9aaaf448`: [Windows 40250030288](https://github.com/Cacheirez/openfodder/actions/runs/40250030288) y [Linux 40250030293](https://github.com/Cacheirez/openfodder/actions/runs/40250030293) aprobados. Inspeccionados los pasos y el log Linux: matriz de pausa 0/1/5, ASan/UBSan/LSan y TSan a una presentación, todos con 301 estados originales; pruebas de 11 fases conservadas. [Resumen de CI](evidence/9aaaf448-ci-summary.json). No se reproduce en esta CI la anomalía local inicial; su causa sigue abierta y no se declara corregida. Esta aceptación es del alcance acotado, no de H4 completo.

Se avanza ahora con H5.1 y el [piloto visual](H6_PILOTO_VISUAL.md), manteniendo las validaciones como puertas de cada integración.
