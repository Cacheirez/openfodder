# Relevo técnico — empezar aquí

Última revisión: 23-10-2026. Este índice organiza el conocimiento para continuar **sin depender del chat**. La fuente operativa es [PLAN_TRABAJO.md](PLAN_TRABAJO.md); los informes fechados son evidencia histórica y no sustituyen su estado actual.

## Estado y referencias de recuperación

- Repositorio: https://github.com/Cacheirez/openfodder. Rama `modernization/windows-foundation`, PR #1 en borrador y **sin fusionar**.
- Código más reciente validado: `ff15219680b289abf207fdc23fc436a9f390e649`. Los commits documentales posteriores no cambian ese motor. Verificar HEAD/PR al retomar; no asumir que esta fecha es la última.
- Base clásica recuperable: rama `baseline/classic-h2.6-2026-10-22`, commit `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`. No moverla ni reescribir su historia. Para inspeccionarla sin alterar la rama activa: `git worktree add --detach ../openfodder-classic 5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`.
- H2.6 aceptada por pruebas automáticas y validación manual de Miguel con CD32. H4.1 está en curso: efectos separados, geometría/recorte por valor, raster PC/Amiga8, recursos propios de sprites, terreno visible, HUD lateral compuesto, cursor y conversión con paleta efectiva/destino RGB propio. No hay todavía frame completo, interpolación ni arte HD.
- Próximo bloque: composiciones y destinos indexados restantes (capas, GUI, minimapa y escenas). No cambiar cadencia hasta completar y probar el estado de presentación 0/1/N.

## Orden de lectura y mapa de conocimiento

| Necesidad | Documento o fuente |
|---|---|
| Objetivo, alcance y tarea activa | [Plan vivo](PLAN_TRABAJO.md) |
| Diseño inicial y razones de arquitectura | [Plan de modernización](PLAN_MODERNIZACION_ES.md); sus pasos de arranque son históricos |
| Diferencias verificadas PC/Amiga y lagunas | [Matriz de contratos](DIFERENCIAS_PC_AMIGA.md) |
| Base aceptada y prueba CD32 | [Aceptación H2.6](H2_6_ACEPTACION_BASE_CLASICA.md) |
| Errores de memoria, enteros, RNC, audio/hilos | Informes H2_* de esta carpeta, especialmente [UBSan](H2_3_UBSAN_CLEAN_2026-10-21.md) y [LSan/TSan](H2_LEAK_THREAD_DIAGNOSTICOS.md) |
| Simulación y visibilidad lógica | [H3](H3_VALIDACION_2026-10-21.md), [contrato mWasDrawn](H3_6_CONTRATO_VISIBILIDAD.md), Source/GameplayTrace.cpp |
| Efectos de dibujo y extracción de núcleos | [Efectos H4.1](H4_1_EFECTOS_DIBUJO.md) |
| Rutas aún acopladas y mutaciones de recursos | [Inventario H4.1](H4_1_RUTAS_Y_RECURSOS.md), con sus seguimientos finales |
| Recursos de sprites y fallo/corrección de rendimiento | [Recursos estables](H4_1_RECURSOS_ESTABLES.md) |
| Tiles/atlas, fórmulas y efectos de fondo | [Terreno estable](H4_1_TERRENO_ESTABLE.md) |
| HUD lateral/cursor, decisiones y momentos originales | [HUD y cursor estables](H4_1_HUD_CURSOR_ESTABLES.md) |
| Paleta efectiva, destinos RGB y efectos de superficie | [Paleta y destinos](H4_1_PALETA_DESTINOS.md) |
| Evidencia compacta de la última revisión | [Informes conservados](evidence/ff15219-reports.json) |

## Invariantes que condicionan cualquier implementación

1. Preservar reglas, RNG, orden de actualizaciones y tiempos lógicos. `mWasDrawn` influye en la jugabilidad; no convertirlo en visibilidad HD ni recalcularlo a la frecuencia del monitor.
2. Retirada de sprites, armas, temporizador comercial y consumo de solicitudes de cursor se ejecutan en sus coordinadoras originales. Los núcleos reutilizables solo dibujan; no reejecutan esos efectos.
3. Capturar juntos bytes privados, geometría, formato y paleta/layout efectivos. No retener entidades, cabeceras activas o superficies del motor en futuros comandos.
4. `FrozenSpriteResources::ReadOnlyBatch` solo es válido mientras no se escriban ni sustituyan imágenes fuente dentro de la pasada. Revisa otra vez el contenido en la siguiente. `TerrainAtlasCache` compara una vez por atlas/captura. Ambos requieren serialización del productor; no son publicación concurrente segura.
5. Mantener Save/Restore, limpieza, fades y llamadas SDL en su orden; completar el frame antes de introducir hilos/cadencias nuevas. PC/Amiga no son formatos intercambiables.
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

Usar directorio nuevo para este ejemplo; no volver a clonar sobre Run/Tests existente. Para reproducir exactamente el motor validado, hacer checkout detached de `ff15219` **antes** de inicializar submódulos. En clones superficiales, obtener los commits originales que cada script declara en `BASELINE` antes de ejecutar equivalencia (`git fetch --no-tags origin <SHA>`). Conservar historia completa o un git bundle del repositorio y de los submódulos para un relevo sin red; no hacer squash que elimine las fuentes de comparación.

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

Esperado: 29/29 fases públicas, cero omisiones, retorno 0; H3 7.956 estados PC + 3.405 Amiga = 11.361. H3 son muestras lógicas de 11 fases, no todos los estados de todas las campañas. La prueba manual H2.6 no acredita visualmente cada cambio H4 posterior.

En Linux ejecutar también los siete scripts `check_final_timer_equivalence.py`, `check_sprite_draw_equivalence.py`, `check_sprite_raster_equivalence.py`, `check_sprite_resource_equivalence.py`, `check_terrain_equivalence.py`, `check_hud_cursor_equivalence.py` y `check_surface_draw_equivalence.py` de tools/modernization. Esperado respectivamente: 184.320, 306.432, 29.160, 10.944, 7.680, (2.304 cursor + 288 HUD) y 27.648 casos de superficie. Usan GCC y fuentes originales de Git. El workflow añade pruebas Python/contratos y compilaciones del motor ASan/UBSan, LSan y TSan; reproducir sus flags y variables, no solo un build Release. No ignorar un timeout o un fallo de infraestructura como si fuese PASS.

## Custodia y continuidad de la evidencia

Los artefactos de evidencia de la última CI caducan el **22-11-2026**. Sus enlaces y SHA-256 constan en el informe de paleta/destinos; los JSON de resultados y SHA de dependencias se conservan ahora en `evidence/ff15219-reports.json`. Este archivo no contiene trazas completas, logs completos ni ejecutables y no permite reconstruir los ZIP a partir de sus hashes.

Antes del relevo, el custodio debe archivar los ZIP de Linux/Windows de las ejecuciones 39995798623/39995798688, el paquete Windows y el código/historia/submódulos en almacenamiento duradero de la organización. Si ya caducaron, repetir pruebas sobre el commit exacto y registrar una nueva procedencia; no atribuir el resultado nuevo al artefacto desaparecido. Los enlaces Actions por sí solos no son archivo permanente.

Datos CD32: obtener de Miguel la copia privada autorizada y su manifiesto SHA-256. Los originales y manifiestos privados no están en GitHub; no depender de rutas temporales del asistente ni publicar esos archivos. Verificación privada previa: 276 archivos, 72 MAP, 72 SPT; RNC probado aisladamente, no 72 fases automatizadas. La versión exacta del binario probado manualmente no se registró mediante VERSION.txt: es una limitación conocida. Si no se conserva la copia privada, la parte CD32 del relevo está pendiente; las demos públicas siguen siendo reproducibles.

## Criterio de cierre de futuros bloques

Cada entrega debe actualizar el plan vivo, la matriz de diferencias y el informe del bloque con: commit base/final, funciones y efectos, decisión y alternativas descartadas relevantes, excepciones PC/Amiga/versión, fuentes y propietarios, límites/precondiciones, pruebas reproducibles y resultados reales, fallos encontrados y resueltos, cobertura pendiente y siguiente paso. Guardar resultados compactos en Git y evidencias voluminosas fuera del repositorio. Separar siempre «inspeccionado», «probado automáticamente», «validado manualmente» y «pendiente».

Esta guía se apoya en la evidencia del motor `ff15219`; las rutas aún no auditadas se documentarán al analizarlas.
