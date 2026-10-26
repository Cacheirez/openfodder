# Relevo técnico — empezar aquí

Última revisión: 27-10-2026. Este índice organiza el conocimiento para continuar **sin depender del chat**. La fuente operativa es [PLAN_TRABAJO.md](PLAN_TRABAJO.md), versión 2.32; el [plan anterior completo](PLAN_TRABAJO_HISTORICO_HASTA_2_19.md) queda como histórico. La publicación opcional desde órdenes está implementada; `acfc099a` está aprobado en Windows/Linux con TSan activo acotado. La [programación 0/1/5 de misión](H4_6_PLANIFICACION_MISION.md) está validada en bd2b3d2. La fixture conjunta de misión/pausa y sustitución de recursos pasa localmente. La siguiente [sonda SDL del motor completo](H4_6_PAUSA_MOTOR.md) está implementada: matriz 0/1/5 local PASS acotada; CI Windows/Linux aprobada; anomalía local inicial pendiente; los informes fechados son evidencia histórica y no sustituyen su estado actual.

Incremento vigente: [sustitución individual de pose](H4_4_POSE_INDIVIDUAL.md), con retorno al clásico, gráficos originales y contraste obligatorio. Pruebas locales y CI Windows/Linux de 46c180be aprobadas, incluidos los sanitizadores declarados. [Evidencia del cierre automático del piloto](H4_4_VALIDACION_46c180be.json); H4 global sigue abierto. Captura anterior: [soldado semántico](H4_2_SOLDADO_SEMANTICO.md), Windows d28d99f9 aprobado, Linux pendiente.

Comparativa visual: [H6.1 A01/B01/C01](H6_1_COMPARATIVA_ABC.md), tres conceptos presentados, no integrados. Recomendación B01; elección H6.2 pendiente de Miguel y comprobación a escala real pendiente.

Incremento de catálogo anterior: [capacidades de helicópteros y vehículos](CD32_CAPACIDADES_VEHICULOS.md), revisión estática parcial y escenarios verificables. Captura mínima del soldado ya implementada; después del piloto visual, helicóptero compuesto. No esperar al catálogo exhaustivo.

Contexto de catálogo: [censo CD32 y contrato de tipos/capacidades](CD32_CENSO_SPRITES.md); continuar después con  [medición inicial H5.1](H5_1_MEDICION_INICIAL.md) y [piloto visual H6](H6_PILOTO_VISUAL.md). Diseñar conceptos no exige cerrar todas las escenas; integrar sprites nuevos exige antes su contrato semántico.

## Estado y referencias de recuperación

- Repositorio: https://github.com/Cacheirez/openfodder. Rama `modernization/windows-foundation`, PR #1 en borrador y **sin fusionar**.
- Código más reciente con CI aprobada: `9aaaf448bf5383f8441f1a26f1df2fe4cb611bbb` (misión 0/1/5, pausa SDL acotada; incidencia local de observabilidad abierta). Los commits documentales posteriores no cambian ese motor. Verificar HEAD/PR al retomar; no asumir que esta fecha es la última.
- Base clásica recuperable: rama `baseline/classic-h2.6-2026-10-22`, commit `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`. No moverla ni reescribir su historia. Para inspeccionarla sin alterar la rama activa: `git worktree add --detach ../openfodder-classic 5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`.
- H2.6 aceptada por pruebas automáticas y validación manual de Miguel con CD32. H4.1 está en curso: efectos separados, geometría/recorte por valor, raster PC/Amiga8, recursos propios de sprites, terreno visible, HUD lateral compuesto, cursor, conversión con paleta efectiva y copias/mezclas con destinos indexados/RGB propios y productores GUI/minimapa/escenas retenidos. La pausa y el frame de misión ya compuesto tienen estado propio y pruebas focalizadas 0/1/5. Faltan capas movibles independientemente, transiciones interactivas del motor completo, interpolación y arte HD. La ruta de misión ya tiene 0/1/5 con H3 original.
- Frame anterior: [frame de misión compuesto y transición a pausa](H4_1_FRAME_MISION.md). 240 escenarios 0/1/5 y 672 capturas retenidas con dobles; efecto de backing persistente de pausa separado. No equivale todavía a capas independientes ni pruebas 0/1/N del motor completo. Consultar resultados del informe antes de aceptar la revisión.

- Incremento validado anterior: [identidad y geometría de destinos](H4_1_DESTINOS_PRESENTACION.md), 97 casos válidos y 627 rechazos sin escritura. CI Windows/Linux, H3 original y 29/29 replays aprobados. Incluye inspección de los destinos reales para preparar capas independientes sin mezclar mSurfaceFinal con mSurface.

- Compositor previo: [compositor de capas de misión](H4_1_CAPAS_MISION.md), 192 escenarios/384 salidas retenidas PASS local. En esa revisión aún no estaba conectado a productores reales; la continuación siguiente aporta esa conexión diagnóstica. CI Windows/Linux aprobada en `ba2ef207`; [evidencia](evidence/ba2ef207-reports.json).

- Incremento anterior: [registro de productores reales y contraste](H4_1_REGISTRO_PRODUCTORES.md), modo diagnóstico optativo. Publicación clásica conservada; 24 escenarios de integración 0/1/5 PASS local. CI Windows/Linux aprobada; replay con registro y vídeo software: 8 fases PC y 3 Amiga, cero omisiones.

- Incremento validado: [publicación opcional desde órdenes](H4_3_PUBLICACION_ORDENES.md). La opción activa obligatoriamente el contraste. `1e1f93d3` pasó publicación normal/ASan con H3, pero TSan activo agotó 1.200 s. `acfc099a` acota esa prueba explícitamente y endurece el control: Windows/Linux aprobados en su alcance; el scheduler H4.6 está validado en bd2b3d2; la nueva prueba conjunta misión/pausa tiene CI pendiente.

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
| Copia/mezcla de capas y destinos indexados | [Capas y destinos](H4_1_CAPAS_DESTINOS_INDEXADOS.md) |
| Productores GUI, minimapa, escenas y corrección de seam PC | [Productores retenidos](H4_1_PRODUCTORES_GUI_ESCENAS.md) |
| Estado de pausa, planificación 0/1/5 y límites | [Informe de pausa](H4_1_ESTADO_PAUSA.md) |
| Evidencia compacta de la última revisión | [Informes conservados](evidence/b34373b0-reports.json) |

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

Usar directorio nuevo para este ejemplo; no volver a clonar sobre Run/Tests existente. Para reproducir exactamente el motor validado, hacer checkout detached de `b34373b0` **antes** de inicializar submódulos. En clones superficiales, obtener los commits originales que cada script declara en `BASELINE` antes de ejecutar equivalencia (`git fetch --no-tags origin <SHA>`). Conservar historia completa o un git bundle del repositorio y de los submódulos para un relevo sin red; no hacer squash que elimine las fuentes de comparación.

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

## Custodia y continuidad de la evidencia

Los artefactos de evidencia de la última CI caducan el **23-11-2026**. Sus enlaces y SHA-256 constan en el informe de pausa; los JSON de resultados y SHA de dependencias se conservan ahora en `evidence/a133afb-reports.json`. Este archivo no contiene trazas completas, logs completos ni ejecutables y no permite reconstruir los ZIP a partir de sus hashes.

Antes del relevo, el custodio debe archivar los ZIP de Linux/Windows de las ejecuciones 40082228491/40082228351, el paquete Windows y el código/historia/submódulos en almacenamiento duradero de la organización. Si ya caducaron, repetir pruebas sobre el commit exacto y registrar una nueva procedencia; no atribuir el resultado nuevo al artefacto desaparecido. Los enlaces Actions por sí solos no son archivo permanente.

Datos CD32: obtener de Miguel la copia privada autorizada y su manifiesto SHA-256. Los originales y manifiestos privados no están en GitHub; no depender de rutas temporales del asistente ni publicar esos archivos. Verificación privada previa: 276 archivos, 72 MAP, 72 SPT; RNC probado aisladamente, no 72 fases automatizadas. La versión exacta del binario probado manualmente no se registró mediante VERSION.txt: es una limitación conocida. Si no se conserva la copia privada, la parte CD32 del relevo está pendiente; las demos públicas siguen siendo reproducibles.

## Criterio de cierre de futuros bloques

Cada entrega debe actualizar el plan vivo, la matriz de diferencias y el informe del bloque con: commit base/final, funciones y efectos, decisión y alternativas descartadas relevantes, excepciones PC/Amiga/versión, fuentes y propietarios, límites/precondiciones, pruebas reproducibles y resultados reales, fallos encontrados y resueltos, cobertura pendiente y siguiente paso. Guardar resultados compactos en Git y evidencias voluminosas fuera del repositorio. Separar siempre «inspeccionado», «probado automáticamente», «validado manualmente» y «pendiente».

Esta guía se apoya en la evidencia del motor `049439d`; las rutas aún no auditadas se documentarán al analizarlas.

La suite `python tools/modernization/check_pause_presentation.py` compara 144 planificaciones 0/1/5 con recursos destruidos/sustituidos. Usa dobles de SDL/entrada y no demuestra por sí sola la transición completa de misión a pausa ni validación visual comercial.

La nueva suite `check_mission_presentation.py` compara coordinadoras reales con productores/SDL sintéticos; la suite de pausa refuerza la comparación de capturas retenidas contra la secuencia original. El siguiente bloque conserva la separación por capas, otras escenas, publicación diferida y validación visual como pendientes.

Último incremento verificado: Windows 40095813348 y Linux 40095813181 aprobados; H3 original y 29/29 replays, con ASan/UBSan, LSan y TSan Linux. [Informe y evidencias](H4_1_FRAME_MISION.md). Los ZIP nuevos caducan también el 23-11-2026; su archivo duradero externo sigue pendiente.

## Seguimiento — destinos de presentación

[Identidad y geometría del destino](H4_1_DESTINOS_PRESENTACION.md): publicación rechaza superficies sustituidas, identidades distintas, tamaños/strides/extensiones incompatibles y formatos fuera del contrato de palabras RGB. Capturas antiguas siguen rasterizándose; un destino nuevo de igual tamaño no hereda su identidad. Se conserva cadencia y producción clásica. Consultar el informe para pruebas y estado de CI; separación de capas y publicación asíncrona siguen pendientes.

Validación actual: `acfc099a` aprobado; el informe H4.3 conserva el fallo histórico y su resolución. La programación H4.6 no programa aún el bucle interactivo de pausa ni todas las escenas.
