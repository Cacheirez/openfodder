# Estado operativo — inicio rápido (14 de noviembre de 2026)

## Arranque rápido — leer solo esta sección al empezar una sesión

- **Hito activo:** enemigos completos hasta revisión jugando, AUTORIZADO/en curso. Rama `modernization/windows-foundation`; PR#1 abierta, borrador y sin fusionar; sin subagentes/modelos nuevos. Protagonistas aceptados y congelados.
- **Código validado:** `76db816`; Source idéntico. **Arte publicado:** `4dbe7b69`,105poses/210derivados E01/v2; primeras dos reacciones de daño y primera reacción inicial integradas. Identidad aprobada, aceptación global jugando PENDIENTE.
- **E3.S PASS técnico:** candidatos `enemy-swim-proportions-technical-v2/8x` y `12x`,244 activos y13.521.408/30.423.168 bytes;679 contratos,140 modernos,469 cuerpos sin arte,66 no-write y4 marcadores nativos. Natación sin suelo añadido;25 grupos/43 poses terrestres con propietarios5/36. [Evidencia](evidence/enemy-swim-integration-v1.json).
- **E3.CI PASS técnico sobre76db816:** Windows push45687322096, Linux PR45687335306 y H645687334996;87 pruebas Python locales y sanitizadores focalizados Windows/Linux PASS. Windows duplicado de PR cancelado por60min; no es fallo del juego y no se repite el PASS completo equivalente. Linux push duplicado45687322051: PASS, consultado el26-11. No afirmar que todos los checks de PR están verdes. [Cierre](evidence/enemy-ci-20261125-76db816.json).
- **E3.VI comprobado:** natación16poses corregida e integrada, escalaX/Y0,974–1,033; originales intactos. Candidatos `enemy-swim-proportions-technical-v2`:244activos,13.521.408/30.423.168bytes,140contratos modernos.679dibujos por densidad/plataforma y sanitizadores Windows/Linux PASS; Source idéntico a CI76db816, sin repetir CI/H3 por arte inactivo. [Evidencia](evidence/enemy-swim-proportions-integration-v2.json).
- **Avance E01/v2:** E3.R23 comprobado;111poses/222derivados disponibles. Daño inicial2B/F0,F1 con maestro enemigo reutilizado y contratos/formatos propios; sin generación redundante ni alias nativo. Integración y aceptación jugando pendientes. [Último bloque](evidence/enemy-initial-damage2-d3.json).
- **E3.DA2 comprobado:** ajuste proporcional/ancla nativa por frame en3/3 primeros pares de daño; fuentes y derivados previos conservados, sin suelo añadido ni cambios de simulación. [Evidencia](evidence/enemy-damage-native-anchor-d2.json).
- **E3.DI PASS técnico:** daño62..69/F0,F1 integrado en candidatos nuevos `enemy-damage-technical-v1/8x` y `12x`;260activos,14.438.912/32.487.552bytes;679contratos,204modernos (198cuerpos/6sombras),405cuerpos sin arte,66no-write y4marcadores. 679dibujos por densidad/plataforma y sanitizadores Windows/Linux PASS; daño sin suelo añadido. [Evidencia](evidence/enemy-damage-integration-v1.json).
- **E3.D2I PASS técnico:** segunda reacción14poses propias integrada,64 reutilizado por la fuente, sin6C. Candidatos `enemy-damage2-technical-v1/8x` y `12x`:274activos,15.241.728/34.293.888bytes;679contratos,260modernos (254cuerpos/6sombras),349cuerpos sin arte,66no-write y4marcadores.679dibujos por densidad/plataforma y sanitizadores Windows/Linux PASS; sin suelo añadido al daño. [Evidencia](evidence/enemy-damage2-integration-v1.json).
- **E3.RA comprobado:** mismo controlador/acción/dirección/frame20↔62 y procedencia E01 verificados; maestro reutilizable, sin alias nativo.20/F0 PC/Amiga y20/F1 soloAmiga: PC no declara ese frame. Exportación propia pendiente. [Auditoría](evidence/enemy-initial-master-reuse-audit-v1.json).
- **E3.RI PASS técnico:** daño inicial20..27 integrado:31contratos reales (Amiga16/PC15), sin20/F1PC. Candidatos `enemy-initial-damage-technical-v1/8x` y `12x`:290activos,16.159.232/36.358.272bytes;679contratos,291modernos (285cuerpos/6sombras),318cuerpos sin arte,66no-write y4marcadores.679dibujos por densidad/plataforma y sanitizadores Windows/Linux PASS; sin suelo añadido. [Evidencia](evidence/enemy-initial-damage-integration-v1.json).
- **Siguiente tarea única:** E3.R24 — verificar y exportar segunda reacción inicial2C/F0,F1 de tipo5/persona0, dirección4, reutilizando maestros E01 de6E con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones. Dirección2 ya cubierta por22; no crear2A.
- **Recuperación:** `C:/Users/migue/.codex/visualizations/2026/11/19/01a1f3ca-14cf-76a1-a9ab-bf2ff6bf17c3`; candidatos anteriores `enemy-aim-technical-v1`, `enemy-rocket-technical-v1`, `enemy-swim-technical-v1`, registros de CI y fuentes generadas preservados. Maestros/prompts/evidencia en Git; no ejecutable final enemigo entregado.
- **ImageGen operativo en poses independientes:**32 nuevas desde reanudación;4B/F0 queda pendiente con registro aislado, sin reintento ni cambio de herramienta/modelo. Soporte no es requisito para otros recursos.
- **Garantías:** simulación/IA/RNG/colisiones/reloj/dirección/frame/H3 y modo clásico intactos;64MiB y fallback real mantenidos. ZIP ajeno y todos los lanzadores previos intactos. Sin B, nuevos escenarios, civiles/vehículos, scroll ni16:9.


## Registro detallado conservado — 5 de noviembre de 2026

**Plan vigente 2.74. A3 activo; A1/A2/A3/A4 y A/H7 abiertos.** La alternancia del piloto de Miguel no está resuelta ni aceptada como producto completo. El lanzador sigue usando el lote antiguo; no hay ZIP nuevo de soldados completos.

## Rama y avance publicado

- `Cacheirez/openfodder`, rama `modernization/windows-foundation`; PR #1 abierta, borrador y sin fusionar.
- Último lote artístico publicado verificado: **`8d09a28dd24573789619ce71af94649451d51ca8`**, posturas normales y 24 poses de granada, sobre `1e1f021845457a9209b20eafa9ad6700f9748c2f` (arreglo del fetch clásico). Los cambios del bloque están publicados en esa rama.
- La selección del lanzacohetes se publicó en `31d82972453f5caa0b37a5a9d1fced0390f0dad3`; el bloque actual añade tres poses de su dirección 7 y su transición en WindowHD/SDL. El commit del estado operativo actual se identifica con `git log -1 --format=%H -- docs/modernization/CONTINUIDAD.md`; no confundirlo con el commit del último lote artístico anterior. Verificar siempre HEAD remoto y CI viva.
- Source del motor, jugabilidad, relojes, RNG y referencias originales no cambian. Base clásica `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`; H3 previo conserva 11 fases / 11.361 estados (7.956 PC + 3.405 Amiga) y 22 pausas/reanudaciones. No se repite H3 completo en este bloque de arte/herramientas.

## Completado y límites

- A1/A2: inventario, captura de todos los slots, compositor ordenado, resolución por recurso/paleta, activos externos v2 y censo transaccional SDL implementados. Siguen pendientes cobertura/rutas, transiciones y GPU. [Contrato de cobertura](SOLDADOS_COBERTURA_COMPLETA.md).
- A3: **24 poses de marcha, ocho de apuntado bajo y 24 de lanzamiento de granada**, preparadas y revisadas internamente. 112 activos 8×/12× y 222 vinculaciones en esas tres familias; el primer lote de cohete descrito abajo eleva el combinado a 118 activos y 234 vínculos. Los 64 activos previos de marcha/apuntado, incluido C01, conservan sus bytes. [Fuentes, prompts, visor y reproducción de granadas](../../assets/modernization/soldier-grenade/README.md).
- Quietud y disparo normal reutilizan los frames que selecciona el original; apuntado bajo usa la tabla `0x30`. La tabla `0x40` mantiene su alcance especial, no se presenta como reposo normal.
- **Modo de escuadrón 0:** revisión de las diez referencias de `word_3BED5`; solo cinco escrituras, todas inicializan a 2. No se ha localizado una ruta normal CF1 que lo active. Sus ramas de animación, parada y salida se prueban sin producir un lote ficticio de posturas normales. No es una prueba contra alteraciones externas de memoria/estado. [Auditoría](evidence/soldier-normal-postures-audit.json).
- Granada: ocho direcciones × tres claves, selección original **0,0,1,1,2,2** y retorno a la postura original. No se modifica la creación, trayectoria ni reloj del proyectil separado. El primer ciclo se verificó antes de ampliar las otras siete direcciones. Se rechazó `g5-f1.png` por invertir el rifle; solo `g5-f1-v2.png` se vincula en su lugar.
- Claves: marcha 94 observadas; apuntado 32 reconstruidas (11 coinciden con el censo previo); granada 96 reconstruidas (34 coinciden). Las restantes reconstrucciones usan tablas/bytes/paletas reales verificados, no se atribuyen a observación de replay. Datos originales, paletas y comparaciones nativas quedan locales.

## Validación del bloque

[Informe, hashes y alcance de sanitizadores](evidence/soldier-grenade-validation.json).

- Selectores extraídos de las fuentes actuales y contrastados con la base clásica: **272 aserciones y 168 muestras** en ocho direcciones; incluye posturas, disparo/cooldown, modo 0 y lanzamiento. Geometría/dirección al objetivo simuladas en la fixture; no acredita interacción completa de campaña. Aserciones conservadas en Release.
- Método real WindowHD/SDL, dos soldados con fases/direcciones independientes, solapamiento, recorte y oclusión, 8×/12×: **1.344 intervalos/2.688 cuerpos controlados y 1.260/2.520 con recursos reales**. Tres rechazos transaccionales por modo: tipo, estado y paleta sin vincular. La expectativa SDL reutiliza el compositor CPU previamente probado; no es un oráculo anatómico independiente.
- Tres grupos reales recorren ocho direcciones; en el cuarto se omiten dos pares porque siguen faltando dos claves ordinarias Amiga de marcha. No se inventan. Las 24 poses nuevas de granada sí existen.
- Compatibilidad del helper ampliado a más familias: conserva la clave anterior de apuntado cuando se omite el frame. Comparación de los 64 activos previos exacta. Nuevos CTests: `soldier_grenade_original_selection` y `soldier_grenade_art`.
- No equiparar estas publicaciones aisladas a publicación HD de una campaña completa. Aceptación visual nueva de Miguel, GPU y CD32 **PENDIENTES**. Consultar el informe para resultados locales ASan/UBSan y la limitación de LSan; no atribuir ausencia de fugas si no se ha medido.

## CI real comprobada para el relevo

Comprobación remota del 5 de noviembre, ligada a **`8d09a28dd24573789619ce71af94649451d51ca8`**: los tres workflows han terminado con **success**.

| Workflow | Ejecución | Resultado |
|---|---|---|
| Windows - modernization foundation | [42034593717](https://github.com/Cacheirez/openfodder/actions/runs/42034593717) | PASS; fetch clásico, build, pruebas, H3 y preparación del paquete de demo existentes |
| linux-build | [42034593370](https://github.com/Cacheirez/openfodder/actions/runs/42034593370) | PASS; build, pruebas, H3 y diagnósticos de sanitizadores existentes |
| H6 - offline density review | [42034593520](https://github.com/Cacheirez/openfodder/actions/runs/42034593520) | PASS |

[Comprobación y alcance](evidence/handoff-20261105.json). Se han consultado los resultados y pasos ya ejecutados; no se han relanzado pruebas ni investigaciones. El fallo anterior por referencia clásica ausente queda resuelto por el fetch previo al build y la CI posterior. Los informes locales conservan el estado que tenían al generarse; esta sección los actualiza para el commit indicado.

Los pasos LSan de la CI Linux existente pasan, pero no sustituyen la medición LSan pendiente de las fixtures locales nuevas de granadas. Los paquetes automáticos de demo conservan el piloto anterior; no son una entrega de soldados completos. La CI de este relevo documental se consulta por separado, sin atribuirle los resultados del commit de implementación.

## Avance A3: selección del lanzacohetes

Selector y llamadores de restauración comprobados contra la base clásica: **2.703 aserciones, 576 muestras, UBSan PASS con NDEBUG y aserciones activas**. La entrada directa mantiene frame 0 durante siete llamadas y retorna en la octava; los llamadores de ratón/objetivo con `field_43` conservan el frame previo 0, 1 o 2. Por ello hacen falta tres poses por dirección para las rutas normales probadas, no una sola imagen fija. Las llamadas del selector no se equiparan a ticks de juego ni a frames de pantalla.

La cuarta entrada declarada en la dirección 5 no se selecciona en esos casos; no se afirma que sea inalcanzable desde cualquier estado. Se prueban giro/reinicio, prioridad del apuntado, retorno al agua y dos soldados intercalados con dirección/frame/tick propios. El primer lote artístico y su publicación SDL acotada se describen a continuación. [Contrato y reproducción](ROCKET_SELECTION.md), [evidencia](evidence/soldier-rocket-selection.json). Nuevo CTest `soldier_rocket_original_selection`; CI del nuevo commit pendiente de publicación. No se repiten las pruebas anteriores ni H3 completo al no cambiar Source ni las referencias.

## Avance A3: primera dirección artística del lanzacohetes

Tres poses nuevas de la dirección 7, frames 0/1/2: **59 poses en total, 118 activos 8×/12× y 234 vinculaciones**. Los 112 activos y 222 vínculos previos permanecen exactos, contrastados con la validación guardada de granadas. C01 intacto. Doce claves reconstruidas desde cuatro grupos reales PC/Amiga; no se atribuyen a observaciones de replay. [Fuentes, prompts, visor y reproducción](../../assets/modernization/soldier-rocket/README.md).

Prueba en el método real WindowHD/SDL: dos soldados con rutas/fases independientes, solapamiento, recorte y oclusión. **1.584 intervalos / 3.168 cuerpos** tanto controlados como con recursos reales a 8×/12×; nueve combinaciones de llamador/frame inicial y tres rechazos transaccionales. La expectativa SDL reutiliza el compositor CPU, no es un oráculo anatómico independiente. CTest nuevo `soldier_rocket_art`; [evidencia y sanitizadores](evidence/soldier-rocket-art-validation.json). La herramienta compartida se contrasta con la prueba focalizada de granadas; no se repiten H3 ni investigaciones concluidas.

Valoración artística de Miguel favorable y provisional, expresamente pendiente de probar el juego. Este bloque no equivale a aceptación jugable, recorrido continuo de campaña ni cobertura de las otras siete direcciones. No hay cambio del lanzador ni ZIP nuevo. ASan/UBSan PASS en la fixture real; LSan pendiente por la limitación de inspección de tareas, con `detect_leaks=0` explícito. La regresión focalizada de granadas pasa (1.344 intervalos). CI del nuevo lote pendiente al publicar. En `31d8297`, Windows y Linux ya superan compilación y CTest; los workflows completos siguen en curso al consultar. Densidades PASS.

## Pendientes y siguiente tarea

1. **Lanzacohetes del jugador:** ampliar las otras siete direcciones y sus vinculaciones, conservando las tres poses y la transición de dirección 7 ya verificadas. Revisar orientación/postura contra las referencias nativas y extender la prueba WindowHD/SDL, con dos soldados, oclusión y 8×/12×. Reutilizar los contratos y maestros existentes; no fabricar un ciclo 0–1–2 ni un cuarto frame que el selector no haya pedido.
2. Después, agua, daño/muerte, enemigos y variantes. Clasificar proyectiles y elementos asociados por separado. No asumir cobertura total por tener 56 poses de tres familias.
3. Completar las dos claves ordinarias Amiga 6/0 y 6/2 del recurso `3e0bf624…`, rutas/transiciones excluidas, GPU/densidad final y CD32. La vista completa sigue recuperándose al clásico si falta cualquier clave necesaria.
4. Mantener estilo C — Pintado moderado; solo C01 tiene aceptación del usuario. 12× de trabajo y 8× alternativa. No repetir selección de estilo, censo completo ni pruebas concluidas sin regresión concreta. No cambiar el lanzador ni cerrar A/H7 hasta cobertura y recorrido continuo pertinentes.

## Recuperación y continuación

**Acceso recuperado y estado comprobado el 5 de noviembre.** El checkout `/workspace/scratch/a4e0bfdd2e06/openfodder` estaba en `8d09a28`, sin modificaciones de archivos seguidos, sin archivos no ignorados pendientes y sin commits locales ausentes de la rama remota. Se actualizó por avance rápido a `67ccf1b`; no fue necesario rescatar cambios de código/arte sin publicar. Esto resuelve la incertidumbre anotada en el relevo anterior. Los directorios ignorados de compilación y capturas nativas se conservan, sin tratarlos como fuentes entregables ni auditar cada temporal.

La CI de `67ccf1b` ha terminado con success: Windows [42062245413](https://github.com/Cacheirez/openfodder/actions/runs/42062245413), Linux [42062245967](https://github.com/Cacheirez/openfodder/actions/runs/42062245967) y densidades [42062245567](https://github.com/Cacheirez/openfodder/actions/runs/42062245567). Son resultados anteriores al nuevo test de lanzacohetes; no se atribuyen al nuevo commit.

Los bytes, paletas y capturas nativas locales no se publican. Para recuperar el trabajo entregado basta la rama de GitHub. Conservar siempre cualquier cambio local antes de limpiar un checkout; el respaldo antiguo descrito abajo no se debe reaplicar sobre HEAD.

El intento antiguo `c81d19f0fca7` sobre `db8a910`, con poses 3/2 y 5/2 rechazadas, quedó sustituido por los bloques posteriores. No aplicarlo sobre HEAD. Recuperación conservada en **OpenFodder_recuperacion_local_20261105.zip**, 71 entradas, SHA-256 `05ad629a90694b2c52a55ed49f82f739e6ef6caac6f34a68567d8e4e32e7ef31`; incluye instrucciones, parches y archivos locales de aquel intento y salidas/temporales antiguos. No se considera trabajo nuevo entregado.

[DESARROLLO.md](DESARROLLO.md) contiene preparación/pruebas. Se puede continuar con [PROMPT_NUEVO_HILO.md](PROMPT_NUEVO_HILO.md), GitHub conectado y sin adjuntos obligatorios.
