# H2.3 — Diagnóstico del motor completo con ASan/UBSan (21-10-2026)

**Estado: fallo reproducible; H2.3 sigue abierta.** Revisión `6255b658622dc80d8036d0a243492a8c0d7783ee`; [GitHub Actions Linux 39601962016](https://github.com/Cacheirez/openfodder/actions/runs/39601962016), evidencia `OpenFodder-Linux-H3-evidence`, `h2-engine-asan/engine.log` y `report.json`.

## Hallazgo nuevo, distinto de RNC

La suite ASan/UBSan del motor completo finaliza con `FAIL`, `returncode=1` y **11 fases completadas** antes de abortar. El primer error fatal registrado es:

- **ASan: `global-buffer-overflow` de lectura de 2 bytes**, `Source/Fodder.cpp:2863`, en `cFodder::Direction_Between_Points`, al indexar `mMap_DirectionsBetweenPoints[pData4]`.
- Ruta de llamada: `Camera_PanTarget_AdjustToward_SquadLeader` → `Camera_Handle` → `Phase_Loop_Interrupt` → hilo `Interrupt_Sim`.
- Ocurre después de completar los replays de Cannon Fodder Plus, Amiga The One y Amiga Action; el log empieza la campaña *Amiga Power Alien Levels*, pero todavía no completa su primera fase.
- **No atribuirlo al RNC**: aparece en el cálculo de direcciones de cámara tras instalar el nuevo lector comprimido acotado.

ASan también informa de varios comportamientos indefinidos de desplazamiento a la izquierda de valores negativos en `Source/Sprites/Sprite_Helicopter.cpp:44`, `Source/Camera.cpp:304`, `Source/Utils/pseudorand.hpp:102`, `Source/Map/MapRuntime.cpp:1158`, `Source/Sprites/Sprite_Core.cpp:460/472` y `Source/Sprites/Sprite_Vehicle.cpp:244`. Son incidencias independientes; no corregirlas ciegamente, porque los cambios en aritmética pueden alterar lógica y RNG.

## Plan defensivo de corrección

1. Revisar y documentar dimensiones reales de `mMap_DirectionsBetweenPoints`, dominio permitido y cómo se calcula `pData4`. Usar casos representativos de juego y registros no sensibles; no generar material de explotación.
2. Definir explícitamente el caso de puntos coincidentes, las magnitudes altas y los límites de índice antes de proponer una corrección de comportamiento.
3. Añadir comprobaciones y pruebas de invariantes matemáticos de dirección; comparar los resultados con la referencia clásica para entradas válidas.
4. Repetir la suite completa ASan/UBSan sin alterar el comparador lógico preestabilización de 11.361 muestras; inspeccionar y documentar el siguiente primer error real si existiese.
5. Separar errores ASan de avisos UBSan. La detección de fugas sigue pendiente: se ejecutó `ASAN_OPTIONS=detect_leaks=0`.

**Precaución CI:** en `.github/workflows/linux-build.yml`, el paso diagnóstico H2.3 tiene `continue-on-error: true`. Por ello la ejecución del workflow puede aparecer `SUCCESS` aunque `reports/h2-engine-asan/report.json` indique `FAIL`. El resultado del paso no debe considerarse aprobación de H2.3. Conservarlo como diagnóstico informativo hasta corregir las incidencias, pero comunicar explícitamente FAIL.

## Estado H3.6 y H2.4

H3.6 se cerró para su alcance de **auditoría** (14 referencias de `mWasDrawn` en nueve ficheros, contrato de visibilidad y `check_visibility_contract.py` integrado en CI). La independencia visual 0/1/N fotogramas es H4, no H3.6.

H2.4 cambió a `std::atomic` cuatro señales de control del hilo. En la ejecución 39601962016, compilación Linux, H3, controles de visibilidad y comparación con baseline pasan; Windows [39601961997](https://github.com/Cacheirez/openfodder/actions/runs/39601961997) también termina SUCCESS. Esto verifica la regresión disponible, **no** demuestra ausencia de todas las carreras de datos.

H2.1 (identificación exacta del recurso RNC que disparó el error original), H2.3 (ASan completo), H2.4 (revisión integral de sincronización) y H2.6 (aceptación) siguen abiertos. Ningún cambio de jugabilidad o renderizado se introduce con este documento.
