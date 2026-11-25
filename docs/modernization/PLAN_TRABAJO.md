# Plan de trabajo vigente — OpenFodder

**Versión 2.74 · 2 de noviembre de 2026.** Responsable técnico: asistente. Decisiones y valoración de juego: Miguel. Este es el único plan de ejecución; [alcance completo H0–H10](ALCANCE_H0_H10.md).

## Control operativo — siguiente paso (lectura inicial obligatoria)

**Única autoridad sobre el trabajo inmediato.** Plan 2.74 vigente; rama `modernization/windows-foundation`, PR #1 abierta, borrador y sin fusionar. Nunca modificar `master`, usar subagentes ni cambiar de modelo sin permiso.

- **Hito activo AUTORIZADO:** enemigos completos hasta revisión jugando. Miguel autoriza priorizar ahora integración técnica con recursos existentes, dejando el arte bloqueado pendiente; el lote parcial no es revisión final. Protagonistas COMPLETADOS y ACEPTADOS, candidato/lanzadores congelados conservados. [Aceptación](evidence/player-acceptance-20261122.json).
- **Cobertura de fuente E1/E3.T1:** 965 contratos PC/Amiga, 679 producidos y 286 solo declarados; máscaras de persona incluyen daño previo a IA. [Tabla](evidence/enemy-native-table-v1.json). Las filas declaradas no activan arte; recursos vacíos de demo requieren firma cero por recurso, sin inventar ausencia universal ni añadir las 53 referencias antiguas.
- **Arte E01 aprobado:** casco/uniforme gris verdoso, cuello rojo teja y barba corta. Lote técnico inicial: 27 poses/54 derivados (marcha y granada frontal); biblioteca gráfica posterior en «Avance E01/v2». Versión verde anterior conservada. [Identidad](evidence/enemy-identity-approved-v2.json). **E2.G1 sigue BLOQUEADO** por rechazo ImageGen 4B/F0, sin reintentos/cambio de herramienta o modelo. [Recuperación](evidence/enemy-generation-blocked-4b-f0.json).
- **Criterio de sombras:** mismo apoyo relativo que protagonistas, proyección fija abajo-derecha/luz arriba-izquierda, independiente de orientación. Estados de agua/altura/daño y sombras independientes mantienen su semántica; ausencias nativas documentadas. Cubrir todas las poses/transiciones producidas antes de aceptación final. [Requisito](evidence/enemy-shadow-coverage-requirement.json).
- **Integración E3.T2–T3 comprobada:** catálogo enemigo opt-in, 679 contratos firmados; candidatos 8×/12× con 54 cuerpos modernos por formato agregado, seis sombras modernas, 66 no-write, cuatro marcadores nativos y **549 contratos corporales sin arte**. [Integración](evidence/enemy-catalog-integration-v1.json), [candidatos](evidence/enemy-technical-candidates-v1.json). Faltantes válidos conservan clásico durante desarrollo; datos/geometría/propiedad inválidos rechazan con recuperación.
- **Último bloque E3.T4 comprobado:** nueve grupos de sombra de suelo para 27 poses, 54 derivados; apoyo y proyección cualificados, colocación estable por dirección y bytes de cuerpo/pintura intactos. Validación nativa 679 estados por densidad Windows/Linux PASS, ASan/UBSan y LSan Linux; ocho pruebas de contacto/densidad PASS. [Evidencia](evidence/enemy-ground-contact-integration-v1.json). No acredita aceptación visual de Miguel.
- **Presupuesto y pruebas:** carga de densidad explícita, preflight 64 MiB intacto; candidatos 204 activos y 11.227.648/25.262.208 bytes. Catálogo/despacho 18.284 casos y captura enemiga 2.073 por sistema PASS; controles protagonistas conservados. **Replay/H3 locales y CI completa del código14025f9 PASS**; aceptación visual/jugable enemiga PENDIENTE.
- **E3.T5 COMPLETADO técnicamente:** H3 Windows/Linux 11 fases/11.361 estados y M1P2 técnico 1.546 estados intactos, 4.635 publicaciones HD; enemigo 5: 1.673 modernos/5.022 clásicos por arte pendiente, sin errores de datos. CI completa Windows/Linux/H6 PASS sobre 14025f9, consultada el 25-11; 85 pruebas Python. [Replay](evidence/enemy-technical-replay-v1.json), [cierre de CI](evidence/enemy-technical-ci-20261125.json). La integración técnica priorizada está comprobada; el hito artístico completo sigue abierto.
- **E2.G1.R — revisión preparada, NO enviada:** comprobado rechazo de salida concreto, no bloqueo general de cuenta/servicio demostrado. ImageGen no ofrece aquí acción de revisión/desbloqueo. Informe de soporte reproducible con petición d0b0ba1a-05a9-416c-aa3c-3c603d2441aa conservado localmente, sin imágenes ni recursos comerciales adjuntos. Sin nueva generación ni elusión. [Vía oficial y entrega](evidence/enemy-imagegen-review-request-20261125.json).
- **Cambio de orden autorizado por Miguel:** continuar con otras poses del inventario sin la imagen4B/F0 rechazada. Esa operación conserva su registro y queda pendiente; soporte no es requisito para tareas artísticas independientes. No ocultar contenido para eludir filtros ni cambiar herramienta/modelo. Una generación de otra pose no demuestra revisión ni resolución del rechazo anterior.
- **Avance E01/v2:** E2.R7 comprobado; registro disponible 43 poses/86 activos, siempre separados de la versión1 conservada. PASS contratos nativos, hashes, alfa/cajas y RGBA/PNG; revisión interna favorable. Integración y aceptación jugando PENDIENTES. [Último bloque](evidence/enemy-v2-rocket-d7.json).
- **Producción reanudada:** otras poses ImageGen funcionan;4B/F0 sigue pendiente, sin soporte obligatorio para trabajo independiente. Biblioteca35 poses/70 derivados integrada en candidatos nuevos `enemy-aim-technical-v1`, anteriores congelados intactos.
- **E3.A comprobado:** 35 poses; candidatos8×/12×,220 activos,12.145.152/27.326.592 bytes;92 contratos modernos,517 cuerpos sin arte. Propietarios5/36 separados reutilizando píxeles; transición de apuntado0/51 y exclusión por altura verificadas. Sanitizadores focalizados Windows/Linux y679 dibujos nativos por densidad PASS; CI del código nuevo y revisión jugando PENDIENTES. [Evidencia](evidence/enemy-aim-integration-v1.json).
- **E3.R comprobado:** ocho poses de lanzacohetes tipo36/F2 integradas;43 poses disponibles. Candidatos privados `enemy-rocket-technical-v1`:228 activos,12.603.904/28.358.784 bytes;108 contratos modernos,501 cuerpos sin arte.679 dibujos por densidad/plataforma y sanitizadores Windows/Linux PASS. Sombras de suelo102, independientes6; CI nueva y revisión jugando PENDIENTES. [Evidencia](evidence/enemy-rocket-integration-v1.json).
- **Siguiente tarea única:** E2.S0 — modernizar natación enemiga5A/F0,F1, dirección0, con identidad E01/v2 y referencias nativas. Preservar agua y ausencia de sombra de suelo; no reintentar4B/F0.
- **Recuperación:** candidatos y logs privados en `C:/Users/migue/.codex/visualizations/2026/11/19/01a1f3ca-14cf-76a1-a9ab-bf2ff6bf17c3/enemy-technical-ground-v1`; fuentes/hashes/prompts y evidencias en Git. ZIP ajeno y lanzadores anteriores intactos; sin ejecutable de revisión final enemigo.
- **Límites:** IA, simulación, RNG, colisiones, reloj, dirección/frame, H3 y modo clásico independientes. B, escenarios/civiles en general/vehículos, scroll y 16:9 requieren autorización distinta. CD32 comercial, GPU/audio y campaña completa no se dan por ejercitados.

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
