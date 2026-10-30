# Relevo técnico — empezar aquí

**Estado vigente 30-10-2026 · plan 2.61:** `3d82ff2` tiene CI Windows/Linux/comparador completa PASS y [paquete verificado](https://github.com/Cacheirez/openfodder/actions/runs/41017089830/artifacts/12961100516). [Cierre y evidencia](VALIDACION_3d82ff2.md). [Costes HD medidos](H6_COSTE_HD_AISLADO.md): evitar integrar tal cual el escalado completo CPU; 12× sigue candidato de textura y 8× parametrizado. Save pendiente de aceptación física; HD aún aislado, densidad final abierta.

**Histórico 2.60 (superado por el cierre 2.61):** CI Windows d2e05e8 falló por falta de `<string>` en el generador HD (MSVC std::to_string). Include corregido; nueva CI/paquete pendientes. No usar d2e05e8 como paquete aprobado. [Evidencia](evidence/windows-d2e05e8-build-failure.json).

**Estado anterior: 29-10-2026 · plan 2.60.** Este repositorio contiene el relevo operativo, las decisiones, el código, las pruebas y los originales visuales. No hace falta recuperar el chat para continuar el desarrollo. Los datos comerciales privados y los ZIP/logs completos caducables de Actions tienen las limitaciones indicadas abajo.

## Leer en este orden

1. [Estado de continuidad y siguiente incremento](CONTINUIDAD.md).
2. [Plan vivo completo](PLAN_TRABAJO.md), especialmente tarea activa y H4–H10. Sus incrementos fechados son bitácora, no estados pendientes acumulativos.
3. [Inventario de escenas y criterio FIT](H5_9_INVENTARIO_ESCENAS.md), [opciones](H5_6_OPCIONES_PRESENTACION.md) y [evidencia del motor vigente](VALIDACION_30ba0ec.json).
4. [Galería original del soldado y jungla](../../assets/modernization/concepts/README.md), [pose C01 y anclajes](H6_3_POSE_C01.md), [densidad 8×/12×](H6_DENSIDAD_EVALUACION.md).
5. [Auditoría de continuidad y mapa de todos los documentos](AUDITORIA_CONTINUIDAD_2026-10-28.md). [Prompt listo para otro hilo](PROMPT_NUEVO_HILO.md).

Incremento vigente: [contrato y piloto HD aislado](H6_4_PILOTO_HD_AISLADO.md) implementado, sin integración SDL; [Save: glifo inválido reproducido y corregido](H5_6_INCIDENCIA_SAVE.md), prueba real PC/Amiga añadida; aceptación física pendiente. Alternancia aceptada. Ambas densidades revisadas visualmente; preferencia por alta condicionada a coste. CI y paquete nuevos no heredan resultados de 30ba0ec.

Relevo revisado: [cierre documental del 29-10](RELEVO_2026-10-29.md).

## Referencias vigentes

- Repositorio: https://github.com/Cacheirez/openfodder; rama `modernization/windows-foundation`; [PR #1](https://github.com/Cacheirez/openfodder/pull/1) abierto, borrador y **sin fusionar**.
- Referencia anterior verificada: `30ba0eccc752cf693b56f1f120842b51f3fd937e`, con arreglo de clics a1c8856 y comparador independiente. No confundir HEAD documental, motor y merge temporal de CI.
- Windows [40800994744](https://github.com/Cacheirez/openfodder/actions/runs/40800994744), Linux [40800994727](https://github.com/Cacheirez/openfodder/actions/runs/40800994727) y navegador [40800994726](https://github.com/Cacheirez/openfodder/actions/runs/40800994726): PASS completo. [Paquete corregido verificado](https://github.com/Cacheirez/openfodder/actions/runs/40800994744/artifacts/12866468476), [evidencia final](VALIDACION_30ba0ec.json).
- FIT común en ventana/maximizada/F11, con ratón alternativo desbloqueado. Geometría lógica y campo visible conservados. CLASSIC sigue disponible y es el valor por defecto.
- Escenas aceptadas («Probar escenas está ok»). Alternancia del menú aceptada; Save corregido en código, pendiente de aceptación física. Miguel autoriza adelantar tareas independientes: [comparador técnico C 8×/12×](../../assets/modernization/density-review/README.md) verificado; comparación visual revisada, densidad final pendiente de coste. No volver a elegir A/B/C: Miguel eligió C.
- Base clásica: `baseline/classic-h2.6-2026-10-22` → `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`; no mover ni reescribir. Inspección aislada: `git worktree add --detach ../openfodder-classic 5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`.

## Cómo interpretar los informes

Los informes H2/H3/H4 y los incrementos fechados describen la implementación y evidencia de su revisión. Un «pendiente» histórico puede estar resuelto en CONTINUIDAD/plan/evidencia posterior. No borrar fallos históricos ni reabrirlos sin evidencia nueva. Las casillas abiertas pueden ser hitos parcialmente implementados: leer su avance. No declarar H4/H5/H6 completos por un piloto.

## Invariantes que condicionan cualquier implementación

1. Preservar reglas, RNG, orden de actualizaciones y tiempos lógicos. `mWasDrawn` influye en la jugabilidad; no convertirlo en visibilidad HD ni recalcularlo a la frecuencia del monitor.
2. Retirada de sprites, armas, temporizador comercial y consumo de solicitudes de cursor se ejecutan en sus coordinadoras originales. Los núcleos reutilizables solo dibujan; no reejecutan esos efectos.
3. Capturar juntos bytes privados, geometría, formato y paleta/layout efectivos. No retener entidades, cabeceras activas o superficies del motor en futuros comandos.
4. `FrozenSpriteResources::ReadOnlyBatch` solo es válido mientras no se escriban ni sustituyan imágenes fuente dentro de la pasada. Revisa otra vez el contenido en la siguiente. `TerrainAtlasCache` compara una vez por atlas/captura. Ambos requieren serialización del productor; no son publicación concurrente segura.
5. Mantener Save/Restore, limpieza y fades en su orden; documentar cualquier cambio de publicación SDL (la pausa sube ahora los resultados finales); completar el frame antes de introducir hilos/cadencias nuevas. PC/Amiga no son formatos intercambiables.
6. No actualizar referencias H3 para hacer pasar un cambio. Investigar el primer estado divergente; separar cualquier cambio intencional de comportamiento y documentar su aceptación.

## Recuperar y reproducir

Requisitos: Git con historial, C++14, CMake, Python 3; Windows con VS 2022 C++ x64, Linux con GCC/Ninja. Las recetas completas y las opciones vigentes están en [.github/workflows/windows-build.yml](../../.github/workflows/windows-build.yml), [linux-build.yml](../../.github/workflows/linux-build.yml) y CMakeLists.txt. Linux necesita además las bibliotecas de desarrollo listadas allí. No confundir compilación headless de análisis con paquete jugable.

```bash
git clone https://github.com/Cacheirez/openfodder.git
cd openfodder
git switch modernization/windows-foundation
git submodule update --init --recursive
git clone https://github.com/OpenFodder/tests.git Run/Tests
git -C Run/Tests checkout c7722ef1a37c1e04ff28c6fedf9d3bdff197dc86
```

Usar directorio nuevo para este ejemplo; no volver a clonar sobre Run/Tests existente. Para reproducir exactamente el motor validado, hacer checkout detached de `30ba0eccc752cf693b56f1f120842b51f3fd937e` **antes** de inicializar submódulos. En clones superficiales, obtener los commits originales que cada script declara en `BASELINE` antes de ejecutar equivalencia (`git fetch --no-tags origin <SHA>`). Conservar historia completa o un git bundle del repositorio y de los submódulos para un relevo sin red; no hacer squash que elimine las fuentes de comparación.

Pins: Run `070a6086c62164e859fc3274b75b5f536fa9d902`, Scripts `dad04730860bcdd1189aa8562860e379b0f5d783`, tests SHA anterior; SDL release-3.4.0, SDL_mixer `3045b35335113e5e5ba258858cb403d8803bfbeb`. Linux registra SHA efectivos en los artefactos. Las imágenes de Actions/paquetes del sistema no están congeladas: no se promete binario reproducible bit a bit. H2.5 describe un mixer Linux flotante **histórico**, corregido en H2.6.

Windows, desde Developer PowerShell:

```powershell
cmake -S . -B build-win -G "Visual Studio 17 2022" -A x64 -DOPENFODDER_ENABLE_FFMPEG=OFF
cmake --build build-win --config Release --parallel 4
ctest --test-dir build-win -C Release --output-on-failure
```

Linux, después de instalar SDL3/mixer conforme al workflow:

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DOPENFODDER_AUTO_FFMPEG=OFF
cmake --build build --parallel 4
ctest --test-dir build --output-on-failure
```

En Linux, exportar `SDL_VIDEODRIVER=dummy` y `SDL_AUDIODRIVER=dummy` para las siguientes pruebas. En Windows sustituir `build/openfodder` por `Run/openfodder.exe`. Cada directorio de informes debe ser nuevo:

```bash
python tools/modernization/audit_replays.py --exe build/openfodder --data Run --out reports/replays --timeout 600 --baseline tools/modernization/reference-completion.json
python tools/modernization/verify_gameplay_determinism.py --exe build/openfodder --data Run --campaign "PC Format" --out reports/pc --timeout 600
python tools/modernization/verify_gameplay_determinism.py --exe build/openfodder --data Run --campaign "Amiga The One" --out reports/amiga --timeout 600
python tools/modernization/check_gameplay_baseline.py --baseline tools/modernization/reference-gameplay-v1.json --traces reports/pc/run1/traces reports/amiga/run1/traces
```

Esperado: 29/29 fases públicas, cero omisiones, retorno 0; H3 7.956 estados PC + 3.405 Amiga = 11.361. H3 son muestras lógicas de 11 fases, no todos los estados de todas las campañas. La prueba manual H2.6 no acredita visualmente cada cambio H4 posterior. La preparación del minimapa se omite explícitamente en unit testing: no atribuirle cobertura de los replays. Su constructor ahora tiene comparación sintética propia contra el cuerpo original, sin validación visual comercial.

En Linux ejecutar también los diez scripts `check_final_timer_equivalence.py`, `check_sprite_draw_equivalence.py`, `check_sprite_raster_equivalence.py`, `check_sprite_resource_equivalence.py`, `check_terrain_equivalence.py`, `check_hud_cursor_equivalence.py`, `check_surface_draw_equivalence.py`, `check_surface_layers_equivalence.py`, `check_indexed_producer_equivalence.py` y `check_pause_presentation.py` de tools/modernization. Esperado respectivamente: 184.320, 306.432, 29.160, 10.944, 7.680, (2.304 cursor + 288 HUD), 27.648 de superficie, 2.944 de capas, (1.536 raster + 1.964 escenas + 1.024 tiles + 72 constructores) y 144 planificaciones de pausa. Usan GCC y fuentes originales de Git. El workflow añade pruebas Python/contratos y compilaciones del motor ASan/UBSan, LSan y TSan; reproducir sus flags y variables, no solo un build Release. No ignorar un timeout o un fallo de infraestructura como si fuese PASS.

## Custodia y límites del relevo

Los cuatro PNG conceptuales y la pose C01 están en Git con SHA-256, además de prompts, manifiestos, código generador y header nativo. No dependen de enlaces de imágenes del chat; no deben regenerarse para sustituir originales perdidos. Las láminas son conceptos, no capturas ni atlas utilizables. Fondos finales, animaciones, cursor nuevo todavía no existen; hay un visor técnico 8×/12× separado del motor, revisado visualmente; el piloto HD aislado todavía no está integrado en SDL.

Los JSON de validación y resúmenes están en Git; **los logs/trazas completos y los binarios de Actions no están archivados todos de forma permanente en GitHub**. El paquete y evidencia Windows de 30ba0ec caducan el 28-11-2026. Si desaparecen, reconstruir/probar el commit exacto con los workflows y registrar nuevos hashes; un hash no reconstruye el ZIP ni garantiza binarios idénticos. No hace falta disponer de los ZIP antiguos para editar y reconstruir el proyecto. C1 conserva la deuda de archivo completo.

CD32: los datos originales privados no están en GitHub y no deben publicarse. Las demos públicas y sus grabaciones fijadas permiten continuar las pruebas automatizadas. La inspección previa de 72 fases CD32 no equivale a 72 replays aprobados. Pedir los datos privados únicamente si una tarea concreta los requiere; no bloquear el desarrollo público por su ausencia.

En cada incremento actualizar CONTINUIDAD, plan y evidencia afectada. Registrar motor probado, CI, paquete/hash, aceptación manual exacta, límites y siguiente paso. Conservar los originales artísticos nuevos en Git con manifiesto y galería. Los mensajes al usuario terminan siempre con **Hecho**, **Situación del plan** y **Próximos pasos**.
