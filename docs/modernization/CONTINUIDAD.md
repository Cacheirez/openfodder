# Estado operativo — 4 de noviembre de 2026

**Plan 2.74. Tarea activa: sustitución completa de soldados.** Leer [plan](PLAN_TRABAJO.md) y [revisión de cobertura](SOLDADOS_COBERTURA_COMPLETA.md). A1/A2 tienen un primer bloque implementado: captura de todos los slots y compositor ordenado interno. Los seis frames actuales no cumplen el objetivo. La ruta ordenada se conecta por manifiesto explícito; el lanzador del piloto no cambia.

## Última observación de Miguel

Probó `PROBAR_SOLDADO_ANIMADO.cmd`: el nuevo soldado aparece intercalado con el antiguo. Pide sustituirlo en todos los casos, revisar todos los sprites y reproducir las ocho direcciones y el movimiento original. **No interpretar esta prueba como aceptación del lote.** No volver a pedirle validar la misma muestra parcial antes de corregirla.

## Estado comprobado

- Repositorio: https://github.com/Cacheirez/openfodder · rama `modernization/windows-foundation` · PR #1 abierto, borrador, sin fusionar.
- Último código/ZIP probado: `f72d6e792c359cec2f53d006d167738c2104bc66`. CI Windows 41359306896, Linux 41359307009 y comparador 41359306892 PASS. ZIP 13106475504: 303 archivos; 29 fases públicas sin omisiones; lote publica seis claves y conserva 3405 estados H3 Amiga. [Verificación y hashes](evidence/soldier-batch-package.json).
- Ese PASS es técnico, no cobertura visual completa. Solo dos orientaciones, primer jugador, un parche y retornos conservadores. [Diagnóstico de los cuatro límites](SOLDADOS_COBERTURA_COMPLETA.md#por-qué-se-intercala-el-clásico).
- Inventario estático nuevo: PC jugador 158 claves, Amiga jugador 159, enemigos 160 por formato; 71 hojas por bando. Marcha: 24 claves por bando. No confundir entradas de tablas con imágenes únicas por producir o estados ya probados. Rutas especiales/civiles/efectos clasificados aparte.
- El bloque posterior A1/A2 amplía la captura real (todos los sprites visibles, incluido el slot auxiliar), conserva apuntado/persona/vehículo/destrucción y añade traza por comando. `OrderedSoldierArt.hpp` compone múltiples cuerpos con recortes y oclusiones, conectado ahora a SDL mediante manifiesto explícito para desarrollo. No hay un ZIP posterior que corrija la mezcla.
- Matriz reproducible: [soldier-coverage-matrix.json](evidence/soldier-coverage-matrix.json); 637 claves estáticas y 96 entradas de marcha (24 × 2 bandos × 2 formatos). No son 637 imágenes distintas. Observación de captura ≠ publicación HD. [Detalle de implementación y límites](SOLDADOS_COBERTURA_COMPLETA.md#bloque-interno-a1a2).

## Validación del bloque interno A1/A2

[Informe con hashes](evidence/soldier-a1a2-validation.json): compositor 144 escenarios y captura ASan/UBSan PASS; 4 tests de matriz PASS. Replay real de 11 fases con contraste y 11.361 estados H3 originales PASS (build local Linux sin mixer). 532.749 comandos únicos capturados; 277 claves ordinarias observadas, no publicadas en HD. CI de `45ad790` comprobada: Windows 41498165115, Linux 41498165124 y comparador 41498165156 PASS; no hay nuevo paquete entregado. Primer intento de trazas truncado, descartado; repetición íntegra en almacenamiento temporal local.

## Siguiente bloque A2: publicación SDL interna

`OrderedSoldierSDL.hpp` publica el resultado ordenado como fondo nativo y franjas HD disjuntas. Carga todas las texturas antes de dibujar, recorta contra la vista y recupera la vista clásica completa ante un fallo parcial. Rechaza cobertura incompleta. Pruebas locales SDL software: 348 casos PC/Amiga a 8×/12× con ASan/UBSan, más los 144 casos CPU. [Evidencia](evidence/soldier-ordered-sdl-validation.json). Añadido a CTest Windows/Linux. **Conectado a `WindowHD` mediante `OPENFODDER_SOLDIER_ORDERED_MANIFEST`**. Resolución por contenido del recurso y paleta RGB efectiva; desconocidos bloquean todo el intervalo. Faltan vinculaciones/arte completos, transiciones y GPU/recorrido visual. No hay nuevo ZIP ni corrección visual entregada.

## Integración por recurso/paleta — 3 de noviembre

CI de `060c0b1`: Windows 41533396790 y comparador 41533396822 PASS. Linux 41533397215 compiló y pasó 15 CTests, pero falló en el inventario estricto de llamadas SDL, que no incluía las cuatro del adaptador. Inventario corregido; no atribuir PASS a los pasos omitidos.

La ruta ordenada de `WindowHD` mantiene el contraste clásico y los guards de escena/pausa/renderer. Resuelve claves estables antes de componer y no cae al piloto si faltan vinculaciones. La recuperación conserva toda la vista. El código local del intento anterior se perdió antes de publicarse; se reconstruyó desde el hilo y se repiten sus pruebas. No reutilizar resultados H3 perdidos. [Contrato](SOLDADOS_COBERTURA_COMPLETA.md#resolución-de-variantes-e-integración-windowhd). Código publicado: `615a90d`. [Evidencia](evidence/soldier-ordered-integration.json): 15 CTests, 37 tests Python e integración/pantalla ASan/UBSan PASS; H3 completo 11 fases / 11.361 estados y 22 transiciones de pausa PASS. Se descartó una traza truncada en el workspace y se repitió íntegro en almacenamiento temporal local. 635 claves PC y 508 Amiga conservadas en `evidence/soldier-ordered-variants.json.gz`, observadas, no aprobadas. El replay usó manifiesto vacío: valida rechazo y simulación, no publicación HD de campaña. CI Windows 41623136653 y Linux 41623137007 en ejecución al registrar; comparador 41623136723 PASS. Consultar estado vivo antes de afirmar CI completa.

## Censo de publicación ordenada — 4 de noviembre

A1 incorpora `OPENFODDER_ORDERED_COVERAGE=1` y `ordered_soldier_coverage.py`: resultado transaccional por intervalo/comando, variante y entidad, con deduplicación de presentaciones. Sustituir una clave en el resolver no cuenta como publicación hasta completar SDL. Errores, recuperación clásica, recursos faltantes y censo interrumpido quedan separados; logs incoherentes/truncados se rechazan. [Contrato](SOLDADOS_COBERTURA_COMPLETA.md#evidencia-transaccional-de-publicación-ordenada--4-de-noviembre) y [evidencia](evidence/soldier-ordered-coverage-validation.json).

Pruebas del método real a 8×/12×: 21 intentos, 8 publicaciones, 4 rechazos por variante, 2 recuperaciones clásicas, 2 fallos de recuperación, 2 intervalos sin cuerpo, 2 censos interrumpidos y 1 manifiesto inválido; ASan/UBSan PASS. 41 tests Python y captura/contrato de pantalla ASan/UBSan PASS. Replays iniciales PC/Amiga con cinco presentaciones: 301 estados H3 originales PASS; 45.785 registros corresponden a 9.157 comandos únicos, cero publicaciones con manifiesto vacío. CTest añade comprobación con diagnóstico desactivado/activado. H3 completo PASS: 11 fases, 11.361 estados originales (7.956 PC + 3.405 Amiga) y 22 transiciones de pausa; compilación local sin mixer. CI del nuevo commit pendiente al publicar; no heredar el verde anterior.

**No corrige todavía la alternancia del ejecutable de Miguel.** No añade poses ni cambia el lanzador. A1/A2/A3 siguen abiertos; guards previos, arte completo, GPU y aceptación visual/CD32 pendientes. No repetir la instrumentación ya cubierta: utilizarla para comprobar vinculaciones/arte y continuar con el resolver más allá de los seis activos, una secuencia completa de 24 claves y las rutas/transiciones aún pendientes.

## Decisiones que se conservan

Estilo **C — Pintado moderado**; C01 aceptado en detalle, posición e integración del comparador. Guardado/persistencia y recorrido común de escenas aceptados. No repetir elección A/B/C ni esas pruebas sin una regresión concreta. Cinco maestros adicionales generados, provisionales. 12× de trabajo y 8× alternativa; GPU/densidad final pendientes.

Objetivo: CF1 modernizado, CD32 principal, presentación suave y nueva sin alterar jugabilidad ni campo lógico. Equipo de prueba de Miguel: Windows 11, 3840×2160, escala 300 %. Base clásica `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`, no mover ni reescribir. H3 original: 11 fases y 11361 estados (7956 PC + 3405 Amiga). Mantener contraste independiente, orden, anclaje, sombras y recortes. Datos comerciales privados fuera de GitHub.

## Para continuar

1. Comprobar HEAD, PR y CI reales. HEAD documental puede ser posterior al código validado.
2. Resolver las rutas/variantes aún pendientes de la matriz, incluida captura en transiciones excluidas; no convertir conteos de captura en aceptación visual.
3. Completar vinculaciones explícitas por recurso/paleta y las 24 poses originales, después los demás estados/entidades censados. La ruta ordenada está conectada por manifiesto; faltan transiciones/GPU y cobertura antes de cambiar el lanzador. Entregar ZIP solo tras cobertura y pruebas pertinentes.
4. Registrar aceptación visual exacta y límites; no cerrar A/H7 por CI verde.

Recuperación y compilación: [DESARROLLO.md](DESARROLLO.md). Relevo: [PROMPT_NUEVO_HILO.md](PROMPT_NUEVO_HILO.md). Mensajes al usuario: terminar con `Hecho:`, `Situación del plan:` y `Próximos pasos:`. Sin subagentes salvo autorización expresa.
