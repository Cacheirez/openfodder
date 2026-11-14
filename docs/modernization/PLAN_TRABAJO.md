# Plan de trabajo vigente — OpenFodder

**Versión 2.74 · 2 de noviembre de 2026.** Responsable técnico: asistente. Decisiones y valoración de juego: Miguel. Este es el único plan de ejecución; [alcance completo H0–H10](ALCANCE_H0_H10.md).

## Control operativo — siguiente paso (lectura inicial obligatoria)

**Única autoridad sobre el trabajo inmediato.** Plan 2.74 y alcance final H0–H10 conservados. **Cambio de estrategia autorizado por Miguel el 14 de noviembre de 2026:** no seguir priorizando una por una las claves residuales del enfoque «todo o nada». La entrega B (lanzador/paquete provisional), la generación masiva de nuevas familias y los hitos posteriores **NO están autorizados**.

- **Hito técnico completado:** `A.1-HYBRID-P1` — prototipo acotado, opt-in, de composición híbrida. Miguel probó ambos modos y observó alternancia de los soldados entre HD y clásico. **Continuidad jugable NO ACEPTADA.**
- **Último resultado comprobado (estrategia estricta):** en la sesión manual de 334 vínculos del 14-11 hubo **4.664/10.987 publicaciones HD (42,45 %)**, **6.263 retornos por faltantes**, 60 interrupciones y 18,074 s de racha máxima; **NO ACEPTADA** por Miguel. En 5.312 retornos faltaban varias claves; una sola clave nueva resolvería como máximo 140. La corrección posterior del recorte Amiga8 pasó pruebas focalizadas: replay público **1.894/4.554 publicaciones**, 2.660 faltantes y cero interrupciones, con H3 de la fase conservado. Esto **no acredita una nueva aceptación jugando**. [Evidencia](DEMO_A1_CONTINUIDAD_334.md).
- **Último microbloque técnico:** `A.1-HYBRID-P1.1` integra el árbol Amiga8 0x90/F0 sin enlace de manifiesto cuando coincide su contrato nativo. Activación adicional con `OPENFODDER_SOLDIER_ORDERED_HYBRID=1` sobre la ruta ordenada. SDL software y sanitizadores focalizados comprobados a 8×/12×. [Evidencia](DEMO_A1_HYBRID_P1.md).
- **Cierre P1.2:** CTest y H3 Windows/Linux, CI completa Windows y pasos pertinentes de ASan/UBSan/LSan en Linux comprobados sobre `fc51fb3`. En Amiga The One M1P2, el híbrido aumenta de 1.368 a 1.894 publicaciones HD con el mismo manifiesto de 333 vínculos y conserva los 1.546 estados de la fase. [Evidencia](DEMO_A1_HYBRID_P1.md).
- **Revisión manual de P1:** 42 publicaciones híbridas con al menos dos soldados HD y el árbol clásico. Se identificaron 21 transiciones HD→clásico en híbrido y 24 en estricto, siempre con al menos un mismo soldado todavía presente y por variantes ausentes de otros elementos. [Evidencia](DEMO_A1_HYBRID_P1.md#revisión-manual-de-p1).
- **Ampliación autorizada por Miguel:** validar la insignia tipo 21, hoja `0x95/F2`, como dibujo clásico provisional sin vínculo en modo híbrido. Autorizados los pasos técnicos necesarios hasta la próxima revisión jugable.
- **Ampliación comprobada:** `4133a63` conserva `0x95/F2` cuando cumple el contrato nativo. CI Windows completa y H3/ASan/UBSan/LSan pertinentes en Linux comprobados. [Evidencia](DEMO_A1_HYBRID_P1.md#ampliación-de-la-insignia-0x95f2).
- **Siguiente tarea única:** Miguel vuelve a jugar Amiga The One M1P2 con el híbrido y valora la continuidad de los soldados. [Comando y registro](DEMO_A1_HYBRID_P1.md#próxima-prueba-jugable).
- **Contrato provisional:** (a) HD válido → reemplazar; (b) recurso clásico completo, verificable y todavía sin HD → dibujo clásico **provisional** en el orden original; (c) geometría/bytes/identidad inválidos, error SDL, presupuesto agotado u otro fallo real → protección y recuperación clásica coherente, sin publicación parcial corrupta. No promover indiscriminadamente cuerpos desconocidos a «aceptados»; registrar por entidad/estado las representaciones clásicas y posibles cambios de aspecto del mismo actor.
- **Criterio de salida P1:** evidencia reproducible con **al menos dos soldados HD y un objeto o enemigo clásico válido**, oclusiones en ambos sentidos, escrituras de cero y mismo color, transparencias, recortes/bordes, Save/Restore si interviene; pruebas negativas de recurso inválido y fallo SDL con recuperación íntegra. Probar regresiones de modo clásico y estricto, ASan/UBSan y H3/CI pertinentes, sin declarar PASS no observado. GPU, CD32, audio, campaña y aceptación jugando quedan **PENDIENTES** si no se ejercitan. No basta con contadores de cobertura.
- **Límites:** sin nuevas imágenes, sin alterar IA, simulación, RNG, reloj ni referencias H3; modo híbrido no activado por defecto y modo clásico recuperable; sin iniciar B, escena completa, scroll o viewport 16:9. Tras cada microbloque validado, publicar commit/evidencias y relevo. Aplicar límites de reintentos de `AGENTS.md` y detenerse al llegar a la próxima revisión jugable.
- **Hitos posteriores propuestos, NO autorizados aún:** (2) demostración jugable y modernización progresiva de terreno, objetos, enemigos, interfaz/cursor; (3) scroll/interpolación visual a 60 Hz conservando tiempo lógico; (4) viewport **16:9 real** con cámara, ratón, HUD y visibilidad lógica separados. CD32 permanece como edición objetivo. [Criterios finales de soldados](SOLDADOS_COBERTURA_COMPLETA.md) · [Alcance H0–H10](ALCANCE_H0_H10.md).

**Vigencia:** toda referencia a «próxima clave», «completar variantes antes de avanzar», «siguiente cohete» u órdenes secuenciales que aparezca **más abajo** es **histórica**, no una tarea vigente. El control operativo de arriba manda.

## Ajuste del verde del uniforme — comprobado

Petición expresa de Miguel del 8 de noviembre de 2026: mantiene su conformidad con el diseño de los soldados, pero considera excesiva la diferencia entre el verde nuevo y el clásico. **Objetivo:** un uniforme más oscuro y más verde, conservando estilo C — Pintado moderado, diseños, siluetas, detalles, poses y animaciones. Miguel eligió el verde oliva más oscuro de la opción A el 11 de noviembre. La aceptación jugando y la resolución de la alternancia siguen PENDIENTES.

Trabajo dentro de A, iniciado después de la auditoría del rango. Se conserva el plan 2.74 y sus garantías. B, activación y paquete quedan fuera de alcance. Cada etapa tiene su propio cierre.

1. **Preparar la muestra — COMPROBADA.** C01, marcha 7/0, dos verdes más oscuros a 8×/12×. Comparación estática del clásico, el actual, A y B sobre una captura de PC Format. Maestro original conservado. [Máscara, comprobaciones, hashes y láminas locales](../../assets/modernization/soldier-c01/uniform-sample/README.md).
2. **Validar la muestra con Miguel — COMPROBADA.** Elección visual expresa de la opción A sobre la muestra estática. Las comprobaciones técnicas de dimensiones, alfa, anclaje y regiones de control corresponden a la etapa 1.
3. **Aplicar la opción A al lote y validarla — COMPROBADA.** 80 poses y 160 activos con hashes reproducibles a 8×/12×. Comparativas internas de las cuatro familias y pruebas focalizadas de composición SDL, con recortes, oclusiones, transiciones y rechazos. Geometría, alfa, anclajes y claves nativas comprobados. [Resultados y límites](DEMO_A1_VERDE_A.md).

**Criterio de cierre de este ajuste:** tono elegido y autorizado para todo el lote por Miguel, aplicación trazable a las 80 poses y verificaciones técnicas y visuales internas registradas. Mantener recuperación de los originales. La cobertura global, la continuidad jugable y la aceptación de la alternancia tienen sus propios criterios.

Los microbloques del verde pueden avanzar con la aceptación jugando pendiente. La prueba en juego sigue siendo necesaria para la aceptación global del piloto.

## Situación histórica anterior — 5 de noviembre (no operativa)

Estado base contrastado con `b617168`, ampliado por el bloque de reposo/apuntado descrito abajo, el **5 de noviembre de 2026**. Se conserva la versión 2.74: esta revisión actualiza avance y criterios operativos, sin cambiar alcance ni orden.

**Estamos desarrollando A3, con A1/A2 implementados parcialmente y pendientes de cobertura completa.** El piloto `PROBAR_SOLDADO_ANIMADO.cmd` sigue activando el lote antiguo de seis claves; no activa el manifiesto de marcha de 24 poses. La alternancia observada por Miguel continúa sin aceptación ni solución entregada como producto.

| Bloque | Implementado y comprobado | Falta para cerrarlo |
|---|---|---|
| A1 | Catálogo estático PC/Amiga, captura de todos los slots, claves por recurso/paleta y censo transaccional de publicación. | Variantes/rutas y escenarios completos, incluidas dos claves ordinarias Amiga no observadas y transiciones. |
| A2 | Compositor ordenado de múltiples cuerpos, recortes/oclusiones, publicación SDL y recuperación de la vista completa; integración por manifiesto en `WindowHD`. | Cobertura normal sin retornos por arte ausente, transiciones y validación GPU/escenas reales. |
| **A3 — bloque de desarrollo actual** | 24 poses de marcha, ocho de apuntado bajo, 24 de granada y tres de cohete (dirección 7); 118 activos 8×/12× y 234 vinculaciones. Posturas y disparo normal verificados en los selectores originales; transiciones aisladas probadas. | Lanzacohetes, agua, daño/muerte, enemigos/variantes, cobertura de campaña y aceptación artística. Modo 0 interno auditado, sin activación normal localizada. No equivale a soldados completos. |
| A4 | H3 previo y pruebas focalizadas de los lotes. Compilación/CTests del arreglo de referencia clásica verificados por commit. | Cobertura global, paquete nuevo y recorrido continuo aceptado por Miguel. CI completa de `8d09a28` PASS; no cierra A4. |
| B/C/D | Hay infraestructura previa documentada en H0–H10. | No se inicia un nuevo bloque de escenario, interpolación o extensión como sustituto del cierre de soldados. |

[Diagnóstico, catálogo y criterios de salida](SOLDADOS_COBERTURA_COMPLETA.md). La ruta ordenada rechaza todo el intervalo si falta una clave: tener el arte de marcha no elimina los retornos de campaña mientras falten otros estados/entidades. El último H3 local conserva 11.361 estados originales, pero no publicó HD ordenado de campaña.

CI completa de implementación `8d09a28`: Windows [42034593717](https://github.com/Cacheirez/openfodder/actions/runs/42034593717), Linux [42034593370](https://github.com/Cacheirez/openfodder/actions/runs/42034593370) y revisión de densidades [42034593520](https://github.com/Cacheirez/openfodder/actions/runs/42034593520), todas PASS. El fallo de referencia clásica ausente está resuelto. [Estado y límites del relevo](CONTINUIDAD.md), [comprobación remota](evidence/handoff-20261105.json).

## Avance A3: reposo/apuntado y transición — 5 de noviembre

Implementado el lote bajo de apuntado en ocho direcciones y su derivación reproducible, conservando los 48 derivados de marcha exactos. [Fuentes y reproducción](../../assets/modernization/soldier-aim/README.md), [evidencia](evidence/soldier-aim-validation.json).

Corregida la interpretación previa de la selección: `0x30` es la familia baja `Prone` (hojas `0x10–0x17`, frame 0) seleccionada por objetivo/condiciones; la quietud normal puede conservar frames de marcha. `0x40` pertenece a una ruta especial de caída y no se promueve a reposo normal. Las tres funciones selectoras permanecen idénticas a la base clásica. El modo de escuadrón 0 selecciona otra familia; la auditoría posterior descrita abajo no localiza activación normal CF1, por lo que no se promueve arte para esa rama interna.

Prueba de 152 aserciones/80 muestras originales, más transición con dos soldados independientes y oclusión en WindowHD/SDL: 640 intervalos controlados y 600 con recursos reales, 8×/12×. Las claves bajas son 32 reconstrucciones desde tablas/bytes verificados: 11 coinciden con el censo previo, 21 no se atribuyen a observación de replay. No hay aceptación visual de Miguel ni publicación HD completa de campaña. No se cambia el lanzador ni se entrega ZIP.

## Avance A3: posturas normales y granadas — 5 de noviembre

El modo de escuadrón 0 queda auditado y probado como rama interna: solo se localizan cinco escrituras de inicialización a 2, sin un cambio normal a 0. No se generan ni se promueven como posturas normales las hojas comentadas `Death-3` sin una ruta efectiva. Es una conclusión de revisión de fuentes, no una garantía sobre estados manipulados externamente. [Auditoría](evidence/soldier-normal-postures-audit.json).

Marcha, quietud y disparo normal reutilizan las familias anteriores, conservando frame/cooldown. Granadas añade 24 poses (ocho direcciones × tres), 48 derivados y 96 claves reconstruidas desde bytes reales; 34 coinciden con el censo previo y 62 no se atribuyen a observación de replay. El combinado tiene 112 activos/222 claves. Los 64 activos anteriores siguen exactos. [Contrato, selección y reproducción](../../assets/modernization/soldier-grenade/README.md), [evidencia](evidence/soldier-grenade-validation.json).

Las funciones originales mantienen la secuencia de lanzamiento 0,0,1,1,2,2 y su retorno nativo; 272 aserciones y 168 muestras. La prueba WindowHD/SDL usa dos soldados independientes y oclusión a 8×/12×: 1.344 intervalos controlados y 1.260 con recursos reales. El proyectil queda separado. No acredita campaña HD completa ni aceptación visual; A3 sigue abierto.

El arreglo `1e1f021` trae la referencia clásica antes de compilar; queda verificado por la CI completa de `8d09a28` indicada arriba.

## Siguiente bloque verificable — histórico de noviembre, sustituido por el control operativo

**A3: lanzamiento de cohetes del jugador.** Selección en offset `0x38` y retorno ya contrastados: entrada directa en frame 0; los llamadores con restauración conservan 0/1/2. [Contrato y evidencia](ROCKET_SELECTION.md). Dirección 7 ya preparada (tres poses), con transición en WindowHD/SDL a 8×/12× y dos soldados/oclusiones. [Fuentes y pruebas](../../assets/modernization/soldier-rocket/README.md). Ampliar ahora las siete direcciones restantes sin rehacer las familias previas. La cuarta entrada de una dirección no se selecciona en las rutas normales probadas, sin afirmar inalcanzabilidad universal. Después, agua, daño/muerte y enemigos. Reutilizar marcha, apuntado, granadas y diagnóstico sin regenerarlos salvo regresión. Mantener pendientes las variantes Amiga no observadas, transiciones, GPU/CD32 y cobertura continua; clasificar por separado proyectiles y otros elementos asociados.

## Orden de trabajo original — referencia histórica, no secuencia operativa vigente

| Paso | Trabajo | Cierre |
|---|---|---|
| **A1 — abierto** | Matriz completa de soldados: todas las claves originales, entidades, estados, recursos/paletas y escenarios. Diagnóstico por entidad/estado y motivo. Casos para oclusiones, agua, bordes y transiciones. | Inventario trazable y puerta que detecte cualquier cuerpo clásico no previsto; no basta publicar una clave una vez. |
| **A2** | Captura de todos los soldados y composición de múltiples cuerpos en el orden original, con recorte/oclusiones correctos. | Casos normales soportados sin volver al clásico; referencia clásica y simulación conservadas. No desactivar guards para saltarse el problema. |
| **A3 — activo** | Ciclo de marcha completo de 24 claves del jugador; después todos los demás estados, enemigos y variantes del catálogo. Derivados/manifiestos reproducibles. Puede avanzar junto con A2 cuando los contratos estén fijados. | Poses coherentes y selección exacta del frame original; todas las familias del alcance cubiertas. Las 24 claves son un paso interno, no soldado completo. |
| **A4** | H3, pruebas de render, CI Windows/Linux, paquete y recorrido continuo a velocidad normal. | Ningún cuerpo clásico intercalado en condiciones normales dentro del alcance; validación visual de Miguel. Recuperación segura y coherente ante errores reales. |
| **B** | Escena coherente: terreno, vegetación, edificios/objetos/efectos, interfaz y cursor completo con punto activo conservado. | Recursos del recorrido cubiertos, composición y legibilidad comprobadas. |
| **C** | Interpolación de cámara/entidades, discontinuidades, ratón e independencia 0/1/N; completar la fase. | Misión completa con presentación nueva y suave; objetivo 60 Hz sujeto a medición real. Cierre H7 solo con su definición completa. |
| **D** | Extensión a CF1/CD32, variantes, pantallas y vehículos; matriz Windows, pulido y entrega. | H8–H10 completos según el alcance final. |

## Avance de ejecución A1/A2 — sin cambiar el plan 2.74

Captura ampliada a todos los slots visibles, con tipo, persona, dirección de apuntado, vehículo/destrucción y recursos propios. Matriz de 637 claves y plantilla exacta de las 24 de marcha por bando/formato en `evidence/soldier-coverage-matrix.json`. Traza opcional `OPENFODDER_SOLDIER_COVERAGE=1` después del contraste clásico; su analizador mantiene `PENDING` porque observar no demuestra publicación HD.

`OrderedSoldierArt.hpp` es un compositor CPU interno de múltiples cuerpos: mantiene orden y celdas HD disjuntas, aplica agua/recortes, oclusiones incluso de igual color y Save/Restore/Clear. Pruebas sintéticas PC/Amiga a 1×/8×/12×. **A1/A2 siguen abiertos**: faltan variantes/rutas dinámicas, transiciones y arte completo; la integración SDL por manifiesto ya está implementada. No se entrega otro piloto parcial ni se cierra A/H7.

El contrato de activos externos v2 está implementado como paso A3 junto a A2: geometría variable, SHA-256, derivados RGBA 8×/12× y vinculaciones explícitas sin compilar cada pose. Una prueba sintética recorre las 24 claves PC/Amiga en 128 intervalos SDL; no son 24 imágenes artísticas terminadas. [Estado y siguiente bloque de arte](CONTINUIDAD.md).

Contraste nativo del 5 de noviembre: 24 claves ordinarias por plataforma recuperadas de recursos reales; 13 vinculaciones diagonales verificadas sin reasignación sintética (12 de marcha y una Slide1 separada), 34 intervalos SDL/68 cuerpos y H3 original completo PASS. [Reproducción y límites](NATIVE_WALK_REVIEW.md). Las otras 21 claves artísticas se prepararon en el lote posterior descrito a continuación; siguen pendientes los demás estados y A3 no se cierra por estas pruebas.

Lote artístico posterior: las **24 claves de marcha del jugador están preparadas y revisadas internamente** (18 maestros nuevos, tres anteriores reutilizados en su diagonal y ciclo C01 conservado). [Fuentes, visor y límites](../../assets/modernization/soldier-walk24/README.md). Publicación SDL probada con las 94 claves ordinarias realmente observadas; dos variantes Amiga no observadas quedan explícitas. Pendientes aceptación artística, otros estados/enemigos y cobertura completa. No cierra A3 ni corrige todavía el lanzador como producto.

## Reglas de implementación

- Preservar reglas, RNG, tiempos lógicos, colisiones, orden y campo visible. No cambiar huellas H3 para ocultar divergencias ni acelerar la simulación para animar arte.
- La dirección visual y el frame los decide el motor, no un reloj nuevo ni la lectura directa del joystick. Mantener apuntado independiente de desplazamiento.
- Estilo C — Pintado moderado y maestro C01 conservados. El lote de cinco poses sigue provisional; no suponer que la aprobación de C01 acepta toda la animación.
- 12× es variante provisional de trabajo, con 8× disponible; densidad final y rendimiento GPU pendientes. No bloquear la corrección de cobertura con otra cadena de estudios de densidad.
- Clásico disponible por elección y recuperación ante errores. En funcionamiento normal, la ausencia de arte o una oclusión normal no cuentan como soldado moderno terminado.
- No producir cientos de imágenes antes de verificar una secuencia completa y su composición. Agrupar cambios útiles, pruebas y evidencia por entrega.
- Datos comerciales y partidas privadas fuera de GitHub. Demos públicas para el trabajo inicial; CD32 se valida por separado cuando la tarea concreta requiera sus datos.
- PR #1 abierto, borrador y sin fusionar. No delegar a subagentes salvo autorización expresa.

## Validación y eficiencia

Documentación: coherencia/enlaces. Catálogos: reproducibilidad, fuentes y longitudes reales. Implementación: tests focalizados de rutas afectadas, H3 y sanitizadores pertinentes; antes de entregar ejecutable, CI completa Windows/Linux, informes ligados al hash y ZIP verificado. Registrar pruebas no ejecutadas como pendientes.

Medir contadores de cobertura y coste por bloque en la ruta real. Optimizar un cuello demostrado, sin encadenar estudios que sustituyan al avance visual. La reducción de duplicados y caché de dependencias en CI sigue pendiente; no eliminar pruebas para acelerar un verde.

Conservar evidencia útil y maestros en Git; los binarios de Actions caducan. Actualizar [CONTINUIDAD.md](CONTINUIDAD.md) y la evidencia afectada, sin copiar el mismo estado a cada informe histórico. [Índice documental](README.md).
