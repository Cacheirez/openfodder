# Plan de trabajo — Cannon Fodder modernizado para Windows

**Versión 2.70 · Revisión: 1 de noviembre de 2026.**
Responsable técnico: asistente. Validación de juego y decisiones visuales: Miguel.
**Tarea activa: entrega A — preparar un soldado animado visible en una fase pública, con perfilado acotado y validación por entrega.**

Estado operativo: [CONTINUIDAD.md](CONTINUIDAD.md). [Prompt nuevo hilo](PROMPT_NUEVO_HILO.md). La ruta operativa siguiente determina el orden. Los incrementos anteriores están en la bitácora enlazada; sus pendientes no reabren tareas aceptadas.

## Ruta operativa 2.70 — acelerar hacia una muestra jugable

Revisión solicitada por Miguel el 01-11-2026. Cambia la secuencia y la política de trabajo; no modifica el motor, los workflows ni el paquete validado. Los IDs H0–H10 y el objetivo completo se conservan. Esta ruta prevalece sobre las próximas tareas de informes históricos.

### Diagnóstico

La base ya permite un piloto: C elegida, C01 aceptado, compositor/SDL opcionales, retorno clásico, H3 y paquete Windows comprobados. Los incrementos recientes han priorizado diagnóstico, medición y cierres sucesivos sobre cambios visibles. Esas pruebas han sido útiles, pero continuar con la misma granularidad retrasaría innecesariamente la muestra.

Hay dependencias demasiado amplias: inventariar todas las fases antes de ampliar un soldado, esperar a cerrar la densidad definitiva o H4/H5 globales antes de preparar H7. También se duplican estados entre documentos y el plan mezcla una extensa bitácora con trabajo vigente. Se eliminan esas dependencias para el piloto, conservándolas donde correspondan a cobertura final.

### Próximas entregas, por orden

| Entrega | Trabajo acotado | Resultado y criterio de salida |
|---|---|---|
| **A — soldado visiblemente animado** (H4.2/H4.4, H5.1, H6.4–6.6, H7.1/H7.3) | Inventariar primero Amiga The One m1p1 como candidata; confirmar sus estados y grabación. Integrar un pequeño lote coherente de reposo/marcha y las direcciones de un recorrido definido, con manifiesto/anclajes y tiempos originales. Añadir contadores y tiempos mínimos a la ruta real. | Nuevo ZIP con una diferencia perceptible jugando a velocidad normal, sin tener que localizar un único frame. Estados no cubiertos vuelven al clásico y quedan enumerados. H3 y validación de paquete aprobados. Es muestra parcial, no soldado ni H7 completos. |
| **B — escena de muestra coherente** (H6, H7.2/H7.4/H7.6) | Completar el lote de estados necesarios para el recorrido, añadir un conjunto pequeño de terreno/vegetación y cursor con punto activo conservado. Probarlos juntos antes de producir más recursos. | Recorrido de una fase con personajes y entorno renovados, cobertura explícita y comparador. Una valoración del conjunto por Miguel; no una aprobación por sprite. |
| **C — movimiento suave y fase completa** (H4 temporal, H5.2–5.5, H7.7–7.9) | Capturas anterior/actual coherentes; piloto de cámara y soldado, reinicio ante discontinuidades, inversa de ratón y comprobación 0/1/N. Completar los recursos que falten en la fase. | Fase jugable con suavidad, presentación coherente y controles correctos. Objetivo 60 Hz sujeto a medidas reales; solo cerrar H7 cuando cumpla su definición completa. |
| **D — extensión y pulido** (H8–H10) | Tras la muestra, ampliar por lotes a CF1/CD32 y completar matriz, opciones y entrega. | Conservar el alcance final; no convertir los retornos clásicos del piloto en cobertura terminada. |

**Estamos antes de A. Siguiente acción concreta:** inventario acotado de m1p1 y definición del pequeño lote de animación, junto con la instrumentación mínima. Si esa fase no ejercita el lote, elegir otra fase pública ya grabada y registrar la razón; no forzar una pose ni cambiar la referencia lógica para mostrar HD. El orden de campaña necesario para H3 se conserva aunque la demostración visual se centre en una fase.

La preparación de recursos y su manifiesto puede avanzar mientras corre CI o se mide la ruta existente; la integración espera a sus contratos concretos. No implica delegación ni creación de subagentes. La interpolación no bloquea mostrar primero animación HD a ritmo clásico, pero sigue siendo requisito del objetivo final.

### Límites que evitan otra cadena de preparación

- **Perfilado acotado:** una instrumentación de captura/contraste/composición/SDL y contadores de sustitución/retorno; una comparación válida. Optimizar solo un cuello de botella demostrado y comprobar antes/después. Ampliar la investigación solo ante un defecto concreto, una regresión o un presupuesto de frame incumplido en la carga pertinente. No repetir el ensayo completo de densidades sin una hipótesis nueva.
- **Calidad provisional:** usar 12× como variante de trabajo del piloto, con 8× disponible y maestros originales conservados. Es reversible, no selección definitiva ni activación HD por defecto. La medición 2.69 no justifica rebajar calidad ni afirmar que una densidad sea más rápida. La decisión final de densidad deja de bloquear el pequeño lote artístico.
- **GPU en una entrega útil:** incluir diagnóstico de frame/renderer en el próximo paquete funcional. Recoger su coste en Windows junto con la revisión visual; no encadenar paquetes solo para métricas ni esperar GPU para inventariar/preparar recursos. No afirmar 60 Hz basándose en tiempos de campaña.
- **Aceptar por lote:** estilo, detalle/posición/integración C01 y guardado/persistencia están aceptados. Pedir nueva revisión solo por la animación/escena nueva o una incidencia reproducible.
- **Posponer para después del piloto:** cobertura comercial completa, helicóptero compuesto, todas las pantallas, monitor/exclusiva/opciones avanzadas, 120/144 Hz, panorámico nativo y producción masiva. Siguen en H4–H10, sin bloquear A/B. Mantener las rutas clásicas de escenas no afectadas.

### Validación proporcional, sin perder las barreras

| Cambio o momento | Comprobación requerida |
|---|---|
| Documentación y planificación | Enlaces, coherencia y diferencias; sin recompilar ni repetir replays. |
| Herramienta de análisis | Tests de su puerta, ejecución real pertinente y procedencia del informe. No cambiar el motor para obtener cifras favorables. |
| Iteración C++/recursos del piloto | Compilación temprana, incluida MSVC si cambia C++; tests de la ruta afectada, contraste/orden/oclusiones/anclaje y H3 del recorrido pertinente. Exigir publicación HD efectiva cuando se mida HD. Usar la campaña completa si el arranque directo no reproduce H3. |
| Candidato a paquete para Miguel | CI Windows/Linux completa que corresponda al código agrupado, replays y sanitizadores existentes, hash de ejecutable/informes/ZIP y recorrido visible. Conservar la cobertura final actual; agrupar cambios coherentes y corregir fallos antes de entregar. |
| Cambio transversal o dependencia incierta | Ampliar inmediatamente la regresión. Nunca saltar un fallo ni marcar una selección parcial como CI global aprobada. |

**Mejora de CI a implementar, aún no aplicada:** empezar por evitar duplicados de eventos y cachear dependencias fijadas. Los workflows Windows/Linux declaran push y pull_request; comprobar qué ejecuciones duplican el mismo código antes de consolidar eventos. Windows agrupa por github.ref, por lo que push y PR pueden quedar en grupos distintos; Linux no tiene grupo de concurrencia. Linux recompila SDL/mixer en cada ejecución. Usar claves de caché por plataforma, compilador, flags y SHA de dependencias; un fallo de caché debe reconstruir. Cancelar solo revisiones sustituidas, nunca la única validación necesaria del candidato.

Separar feedback rápido y validación completa del candidato si lo anterior no basta. No borrar escenarios o sanitizadores para conseguir un verde temprano. Si se dividen jobs, aislar datos/salidas por job y conservar la trazabilidad del ejecutable. Esta reorganización es un ajuste acotado de infraestructura, no un nuevo proyecto previo a A. Hasta implementarla, los workflows actuales siguen siendo la referencia; el cambio de política no demuestra una reducción de duración.

### Gestión de avance

Agrupar implementación, pruebas y documentación de una entrega coherente; no convertir cada medición, include o cierre en una nueva espera manual. Un registro de evidencia por entrega y actualización breve de tarea activa/continuidad. README y prompt sirven de índice, sin copiar toda la historia. Leer al retomar el estado y esta ruta, y después los contratos afectados; no releer toda la bitácora salvo que una dependencia lo requiera.

Medir dos cosas: tiempo hasta feedback de compilación/tests y tiempo hasta un ZIP con cambio visible. Comparar antes/después de los ajustes CI; no prometer una reducción porcentual o fecha sin ese dato. El ahorro esperado procede de menos trabajo bloqueante y ejecuciones redundantes, no de menos protección de la simulación.

**Siempre:** H3 original, reglas/RNG/tiempos/colisiones/campo lógico, contraste obligatorio, orden/oclusiones/anclaje, retorno clásico y originales artísticos preservados. Clásico por defecto; PR abierto, borrador, sin fusionar. Un fallo reproducible se corrige antes de seguir con su ruta afectada.

## Incremento 2.70 — revisión de prioridades

Ruta A–D incorporada y bloqueos del piloto acotados. Aceptación C01 y medición 2.69 conservadas. Historial 2.28–2.69 trasladado íntegro a [la bitácora](PLAN_TRABAJO_HISTORICO_2_28_A_2_69.md). Revisión documental: no es implementación de animaciones, optimización de motor ni de CI. El paquete vigente sigue siendo 3ee12e9.

## 1. Dictamen de la revisión

El objetivo y la arquitectura general siguen siendo válidos. Hemos avanzado bastante más que el inventario que todavía indicaban algunas casillas: existen capturas propias, composición ordenada, validación de destinos y registro conectado a productores reales. Sin embargo, reconstruir el mismo frame no equivale aún a poder presentar con otra frecuencia ni a interpolar entidades por separado. **H4 sigue abierto. Los conceptos H6.1 ya existen, C está elegida y su pose mínima está integrada experimentalmente. El siguiente avance visible es un pequeño lote animado; la densidad definitiva se decidirá con la muestra, sin bloquearla. Guardado/persistencia y C01 ya aceptados.**

Cambios respecto al plan anterior:

- Consolidar el estado vigente y trasladar las notas de sesiones anteriores al [histórico v2.19](PLAN_TRABAJO_HISTORICO_HASTA_2_19.md). Se conservan todos los IDs H0–H10, los fallos históricos y sus resoluciones.
- Reconocer como hechos el frame compuesto de misión, la transición a pausa en pruebas focalizadas, las capas ordenadas y el registro de productores. No repetir esas extracciones; ampliar su integración y cobertura.
- Concretar H4.3: activación opcional, frame válido, política de retorno al clásico, detección de divergencias y destinos independientes.
- Ampliar la aceptación de H4.6 con 0/1/N en el motor completo y sanitizadores con la nueva ruta activa. La ruta de misión ya conserva H3 con 0/1/5; falta ampliar transiciones y escenas.
- Adelantar la medición de H5.1 a H4 y explicitar la información semántica que necesitará la interpolación: identidad de entidad, generación, posición, cámara y tiempos coherentes.
- Dar por confirmada CD32 como campaña principal en H8.1. Su cobertura automática completa sigue pendiente.
- Añadir tareas transversales de conservación de evidencias y reproducción. Los informes compactos están en Git; los ZIP completos de Actions caducan.

**No se necesita ahora:** reescribir el motor, actualizar SDL por iniciativa propia, crear otro hilo de renderizado, producir arte en masa ni volver a aceptar H2.6. La ampliación panorámica del viewport queda planificada en H5.10 y requiere aislar primero la visibilidad lógica; no se incorpora al piloto C01 actual. La escala gráfica 4× es una hipótesis que evaluaremos, no un requisito cerrado. Tampoco se exige terminar todas las pantallas del juego antes de probar un piloto acotado, siempre que las demás conserven su ruta clásica y las transiciones estén verificadas.

### Ajuste de secuencia del 26-10-2026

La CI de la sonda de pausa está aprobada en Windows/Linux. Se deja la anomalía local de observabilidad como incidencia acotada: no se borra, pero no bloquea preparar conceptos visuales ni una captura semántica experimental. Evitar ampliar indefinidamente las baterías de escenas antes de mostrar un piloto. Siguiente trabajo técnico: medir coste, capturar cámara/identidad/posición de un sprite y reproducirlo con el recurso original; en paralelo de planificación (sin delegación), preparar tres conceptos comparables. Véase [alcance del piloto](H6_PILOTO_VISUAL.md).

## 2. Objetivo, alcance y reglas

Modernizar Cannon Fodder para Windows sobre OpenFodder, C++ y SDL3: cámara y movimiento suaves, presentación renovada de personajes, vehículos, edificios, terreno, efectos e interfaz. Mantener reglas, controles, dificultad, colisiones, tiempos, RNG y todas las correcciones ya incorporadas. Presentación PC en 4:3 y 16:9 hasta 3840×2160, según la [matriz de resoluciones](RESOLUCIONES_PC_HASTA_4K.md), con modo clásico preservado. Primero una misión completa de muestra; después el alcance acordado de Cannon Fodder 1, con CD32 como campaña principal. Cannon Fodder 2 no se moderniza en esta primera entrega, pero se conserva su compatibilidad existente.

1. Mantener el modo clásico y la base recuperable; no mover ni reescribir su rama.
2. No aumentar la frecuencia lógica para conseguir más imágenes por segundo. Preservar visibilidad lógica y `mWasDrawn`, orden de actualizaciones y efectos de coordinadoras.
3. Conservar las coordenadas lógicas y el encuadre clásico como referencia. La presentación panorámica nativa H5.10 tendrá contrato explícito y no modificará visibilidad lógica, colisiones, armas ni límites de entidades. Cambiar resolución no autoriza estirar ni recortar el juego.
4. Presentar desde datos coherentes y propios, sin consumir RNG ni ejecutar otra vez efectos del juego. Los efectos cosméticos tendrán presupuesto y aleatoriedad separados.
5. Mantener las referencias H3 originales; una divergencia no se resuelve regenerando sus huellas para obtener verde.
6. Conservar los datos comerciales, partidas y credenciales fuera de Git y de los paquetes públicos.
7. Distinguir compilación, replays, igualdad lógica, igualdad de imagen, sanitizadores y prueba manual. Ninguna de ellas sustituye a todas las demás.
8. **PR #1 abierto, en borrador y sin fusionar.** La aceptación futura de una entrega no autoriza por sí sola a fusionarlo.

## 3. Estado comprobado y alcance de la evidencia

| Elemento | Estado a esta revisión |
|---|---|
| Repositorio y rama | [Cacheirez/openfodder](https://github.com/Cacheirez/openfodder), `modernization/windows-foundation` |
| PR | [#1](https://github.com/Cacheirez/openfodder/pull/1), abierto, borrador, sin fusionar |
| Motor/revisión verificados | `3ee12e978c21b3157521c0e1fb65573bb4c56a26`, diagnóstico y prueba visible C01 con SDL opcional; [evidencia](VALIDACION_3ee12e9.md) |
| Aceptación manual | Parcial por incrementos; [registro vigente](CONTINUIDAD.md). No hay aceptación manual global de e18b05b |
| Base clásica aceptada | `baseline/classic-h2.6-2026-10-22` → `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8` |
| CI Windows 3ee12e9 | [41288644622](https://github.com/Cacheirez/openfodder/actions/runs/41288644622), éxito |
| CI Linux 3ee12e9 | [41288644597](https://github.com/Cacheirez/openfodder/actions/runs/41288644597), éxito, incluidos los diagnósticos declarados |
| Publicación desde órdenes | Implementada, opcional y con contraste obligatorio; validada en acfc099a con el alcance de pruebas declarado. H4 global sigue abierto. Clásico por defecto |
| Interpolación / arte | Interpolación pendiente; C elegida y pose C01 experimental; densidad HD pendiente |

| Evidencia conservada | Qué acredita | Límite |
|---|---|---|
| H3 original | 11.361 estados: 7.956 PC y 3.405 Amiga, conservados en Windows/Linux | 11 fases, no toda CD32 ni todos los estados posibles |
| Replays habituales | 29/29 fases, cero omisiones; 7 CTests Windows y controles de CI aprobados | Completar no demuestra por sí solo igualdad visual o interacción real |
| ASan/UBSan, LSan, TSan del motor | 29/29 fases habituales; publicación activa 11 fases ASan/UBSan/LSan y 2 fases TSan, sin hallazgos en bd2b3d2 | TSan activo limitado a 301 estados; no cubre todas las escenas ni el nuevo scheduler 0/1/5 |
| Frame de misión y pausa | 240 escenarios 0/1/5, 672 capturas retenidas; pausa aislada: 144 escenarios | Pruebas focalizadas con dobles, no motor completo interactivo |
| Destinos | 97 casos aceptados y 627 rechazos sin escritura | Identidad de almacenamiento y geometría; no garantiza frescura temporal del frame |
| Compositor de capas | 192 escenarios, 384 salidas retenidas; destinos y orden conservados | Reconstrucción de operaciones; no entidades ya interpolables |
| Registro de productores | 24 escenarios / 48 presentaciones, planes 0/1/5; contraste de índices, fondo guardado y RGB | La fixture actual invoca los adaptadores preparado y resuelto; recursos y SDL siguen siendo dobles |
| Registro activo en motor real | Vídeo SDL software Linux: PC Format 8 fases y Amiga The One 3; cero omisiones y marcador de contraste comprobado | 0/1/5 en la ruta real de misión: 11.361 estados por política; sin validación GPU ni pausa interactiva |
| Prueba manual de Miguel | Base clásica, demo y CD32 aceptadas; controles, audio, pausa, F11 y Alt+Tab correctos | No se atribuye al motor b34373b0 ni prueba las 72 fases CD32 |

Validación nueva: [H4.3 y su límite TSan](H4_3_PUBLICACION_ORDENES.md), [intento 1e1f93d3](evidence/1e1f93d3-reports.json) y [estado acfc099a](evidence/acfc099a-reports.json). La prueba activa TSan de dos fases está aprobada y no equivale a las 11 fases normales ni a la campaña completa. [H4.6 y evidencia bd2b3d2](H4_6_PLANIFICACION_MISION.md) añaden programación real 0/1/5 de misión.

Fuentes: [registro real y resultados](H4_1_REGISTRO_PRODUCTORES.md), [frame de misión](H4_1_FRAME_MISION.md), [destinos](H4_1_DESTINOS_PRESENTACION.md), [capas](H4_1_CAPAS_MISION.md), [aceptación clásica](H2_6_ACEPTACION_BASE_CLASICA.md) e [informes compactos de b34373b0](evidence/b34373b0-reports.json). Para los núcleos previos —recorte, raster, recursos, terreno, HUD, cursor, paleta y escenas— consultar el [índice técnico](README.md).

## 4. Ruta y dependencias

| Hito | Estado real | Dependencia / próxima entrega |
|---|---|---|
| H0 · Auditoría y preparación | Completado en alcance inicial | Conservar referencias |
| H1 · Windows comprobable | Completado | No repetir aceptación sin un cambio que lo justifique |
| H2 · Estabilización | Base aceptada; H2.1 histórico delimitado | Mantener regresiones y exclusiones |
| H3 · Misma jugabilidad | H3.1–H3.6 completadas en demos | Barrera permanente para H4–H10 |
| H4 · Presentación separada | Avanzado, parcial | Publicación opcional → motor 0/1/N y transiciones → estados aptos para interpolación |
| H5 · Cámara y movimiento suaves | Parcial: medición inicial, transformaciones/FIT y opciones mínimas implementados | Ajuste común y guardado/persistencia aceptados; interpolación pendiente |
| H6 · Arte y recursos | C elegida, bocetos archivados y pose integrada experimentalmente | C01 aceptado y coste inicial medido; pequeño lote animado en entrega A, densidad definitiva y GPU pendientes |
| H7 · Primera misión moderna | Pendiente | H5 y muestra H6 aprobados, fase inventariada |
| H8 · Cobertura de CF1/CD32 | Edición confirmada, producción pendiente | H7 y matriz de recursos/escenarios |
| H9 · Pulido Windows | Pendiente | Regresión continua; cierre tras H8 |
| H10 · Entrega | Pendiente | H9 y aceptación explícita del alcance/publicación |

Se puede comenzar un piloto limitado de H5 cuando la misión elegida supere las puertas H4, aunque otras pantallas sigan clásicas. Esto **no cierra H4 global**. Los conceptos H6 pueden prepararse antes; no conviene producir cientos de recursos hasta probar una muestra dentro del juego. Revisaremos esfuerzo y calendario tras el piloto H4, H5 y H7, sin inventar porcentajes de avance.

## 5. Tareas completas, parciales y pendientes

`[x]` significa completado en el alcance descrito; `[ ]` significa pendiente o parcial, con su progreso explicado. Se mantienen los IDs. Salvo indicación contraria, ejecuta el asistente; Miguel decide estilo y valida juego real.

## H0. Auditoría y preparación — completado

- [x] **H0.1 — Asistente:** inspeccionar temporización, cámara, superficies, sprites, entrada y pruebas existentes.
- [x] **H0.2 — Asistente:** fijar las revisiones auditadas de motor, datos, scripts y grabaciones.
- [x] **H0.3 — Asistente:** compilar la referencia Linux y ejecutar las 29 fases demo disponibles.
- [x] **H0.4 — Asistente:** preparar el control de replays y comprobar sus ocho casos de prueba.
- [x] **H0.5 — Asistente:** reproducir el fallo de lectura de pistas del mapa y preparar un parche con ocho casos de borde.
- [x] **H0.6 — Asistente:** comprobar que las 29 fases completan tras ese parche; registrar el segundo fallo ASan en descompresión Amiga.
- [x] **H0.7 — Miguel / asistente:** conectar GitHub, verificar el repositorio y crear la rama y el PR #1.
- [x] **H0.8 — Asistente:** preparar el workflow Windows, la comparación de resultados y el empaquetado de las siete demos.

**Evidencia:** PR #1, `RESULTADOS.md` y paquete inicial `OpenFodder_Modernizacion_Fase0.zip` entregado en el chat. La cobertura es de demos; no equivale a toda la campaña comercial.

## H1. Primera versión comprobable en Windows — completado

**Objetivo:** que Miguel pueda ejecutar la base clásica sin tener que compilarla personalmente.

- [x] **H1.1 — Asistente:** consultar el resultado de Actions; si falla, leer el primer error real, corregirlo y repetir solo lo necesario. Si sigue activo, identificar el paso sin declarar éxito anticipado.
- [x] **H1.2 — Asistente:** verificar compilación x64 y que las 29 fases completan sin omisiones ni diferencias de nombres/resultados frente a la referencia.
- [x] **H1.3 — Asistente:** verificar el artefacto: ejecutable, DLL, demos, scripts, licencias, instrucciones, `VERSION.txt` y `PRUEBAS.json`; comprobar que no incluye partidas ni datos comerciales.
- [x] **H1.4 — Miguel, guiado por el asistente:** descargar, extraer en una carpeta nueva y abrir `INICIAR.cmd`.
- [x] **H1.5 — Miguel:** probar cinco minutos: movimiento, disparo, desplazamiento, audio, pausa, Alt+Tab y F11. Comunicar versión, demo y cualquier mensaje literal.
- [x] **H1.6 — Asistente:** registrar el resultado manual y corregir los problemas de arranque o empaquetado encontrados.

**Aceptación:** build y replays Windows aprobados, paquete inspeccionado y arranque real confirmado por Miguel. Headless significa «sin ventana»: no sustituye H1.4–H1.5.

**Si falla:** conservar el registro del intento y el primer error; no encadenar instrucciones de instalación al azar ni modificar la jugabilidad para forzar un resultado verde.

## H2. Estabilización de la base — aceptada con exclusiones

- [ ] **H2.1 — Asistente:** atribuir el recurso mínimo del fallo RNC histórico. Deuda documental delimitada, aceptada en H2.6; no hay un fallo reproducido pendiente de la ruta actual en la cobertura ejecutada. Retomar si aparece un caso pertinente, sin bloquear H4 por repetir la investigación histórica.
- [x] **H2.2 — Asistente:** lector RNC acotado y pruebas de truncamientos/límites. Público: 88 recursos válidos y 1.047 variantes inválidas; CD32 privado: 41 y 488, respectivamente.
- [x] **H2.3 — Asistente:** ASan/UBSan y LeakSanitizer sin hallazgos en 29 replays públicos. Campaña completa y todas las rutas interactivas siguen fuera de esa garantía.
- [x] **H2.4 — Asistente:** correcciones de música/callback/temporización/transiciones; TSan sin hallazgos en 29 replays y H3 inalterado. No equivale a una auditoría universal de hilos ni de presentación nueva.
- [x] **H2.5 — Asistente:** inventario de dependencias y cobertura. La discrepancia histórica de mixer se trató en H2.6: SHA fijado en ambas plataformas; TSan obligatorio. No implica equivalencia acústica entre backends ni reproducibilidad binaria absoluta.
- [x] **H2.6 — Asistente / Miguel:** aceptación del 22-10-2026, CI y prueba manual CD32; base clásica recuperable y PR sin fusionar.

**Evidencia y exclusiones:** [aceptación H2.6](H2_6_ACEPTACION_BASE_CLASICA.md). Los avisos UBSan antiguos, el mixer Linux sin fijar y los sanitizadores no bloqueantes pertenecen al histórico; no se mantienen como bloqueos vigentes. Las fugas se comprueban en CI aunque el entorno local no permita ejecutar LSan. No atribuir la prueba manual a un commit exacto que no se registró.

## H3. Proteger la misma jugabilidad

**Actualización de validación:** [H3_VALIDACION_2026-10-21.md](H3_VALIDACION_2026-10-21.md). H3.1–H3.5 verificadas para las 11 fases ensayadas, no toda la campaña CD32. H3.6 auditada y documentada en [H3_6_CONTRATO_VISIBILIDAD.md](H3_6_CONTRATO_VISIBILIDAD.md). La implementación de visibilidad independiente y las pruebas 0/1/N dibujos pertenecen a H4.


**Objetivo:** comprobar más que «la misión llega al final».

- [x] **H3.1 — Asistente:** repetir una grabación con la misma versión, datos, configuración y semilla para establecer si la referencia es determinista. Determinista significa obtener el mismo estado con las mismas entradas.
- [x] **H3.2 — Asistente:** definir los campos a comparar por tick: posiciones y fracciones, vida, munición, selección, proyectiles, temporizadores, objetivos, cambios de mapa y estado del generador aleatorio.
- [x] **H3.3 — Asistente:** implementar una traza o huella canónica sin punteros, direcciones de memoria ni relleno dependiente del compilador.
- [x] **H3.4 — Asistente:** mostrar el primer tick y campo que difiere; probar que una divergencia introducida deliberadamente es detectada.
- [x] **H3.5 — Asistente:** conservar referencias por plataforma si la equivalencia entre Windows y Linux no está demostrada. No ocultar diferencias con tolerancias arbitrarias.
- [x] **H3.6 — Asistente:** registrar el comportamiento lógico relacionado con visibilidad y con `mWasDrawn` para preservarlo al cambiar el dibujo.

**Aceptación:** la herramienta detecta un cambio relevante y la referencia se reproduce bajo condiciones fijadas. Los cambios posteriores deben mantener los campos lógicos acordados o explicar y resolver cualquier divergencia.

## H4. Separar presentación y simulación — parcial

- [ ] **H4.1 — Asistente:** completar la separación/preservación de efectos del dibujo en sus coordinadoras lógicas. **Hecho:** extracción de núcleos, recursos propios, pausa y frame compuesto, productores registrados y contraste diagnóstico. **Falta:** demostrar independencia del motor completo y cubrir coordinaciones/transiciones restantes. No repetir el inventario inicial como si no existiera.
- [ ] **H4.2 — Asistente:** estados coherentes de solo lectura para cámara, sprites, terreno, paletas e interfaz. **Hecho:** capturas propias, destinos validados y piloto de un soldado con escena/slot/generación, posición/cámara y recurso original retenido. **Falta:** generalizar el contrato temporal, vida útil acotada y datos semánticos para H5 al resto de entidades y escenas. La identidad del almacenamiento no es una versión de contenido ni una fecha del frame.
- [ ] **H4.3 — Asistente:** rutas clásica y nueva seleccionables usando imágenes originales. **Hecho:** compositor privado y auditoría opcional `OPENFODDER_AUDIT_MISSION_LAYERS=1`. **Implementado, aceptación parcial:** publicación opcional desde órdenes; conservar referencia clásica, contraste y retorno definido ante ruta no disponible. No activar por defecto hasta superar las puertas de la sección 6.
- [ ] **H4.4 — Asistente:** separar terreno, entidades/efectos, panel y cursor conservando orden, recortes, paleta y visibilidad. **Hecho:** registro ordenado de operaciones reales, incluidos Clear/Save/Restore, destinos independientes y momentos de cursor. **Piloto añadido:** identidad/generación, posición/cámara y sustitución de una pose original con retorno por comando al clásico. **Falta:** generalizar ese modelo y sus tiempos para mover entidades y cámara independientemente; aún no hay interpolación.
- [ ] **H4.5 — Asistente:** comprobar propiedad de datos y uso del hilo de ventana/SDL al publicar. **Hecho:** protección del estado nuevo del registro. **Falta:** verificar el flujo activo completo, coherencia y recursos bajo sanitizadores; esto no prueba que los buffers clásicos sean seguros para acceso concurrente. Conservar inicialmente los hilos existentes; añadir colas o hilos solo si una necesidad medida lo justifica.
- [ ] **H4.6 — Asistente:** comparar estados lógicos con 0/1/N presentaciones entre pasos lógicos. **Hecho:** baterías focalizadas y ruta de misión del motor completo 0/1/5 con H3 original (bd2b3d2). Nueva prueba conjunta de los cuerpos reales de misión/pausa: 192 transiciones con recursos sustituidos, PASS local y CI en 9aaaf448. **Validado en CI:** sonda SDL acotada del motor completo, dos fases/301 estados con 0/1/5 (véase H4_6_PAUSA_MOTOR.md). **Falta:** pausas largas/eventos, sustitución de recursos en interacción completa, carga/cambio de fase, minimapa y entradas/salidas de escenas. Productor preparado y resuelto ya invocados en la fixture; omisión deliberada detectada. Ampliar la cobertura del motor y de las transiciones.

**Aceptación global:** presentar más, menos o ninguna vez no altera reglas, RNG ni efectos lógicos; frames y recursos son coherentes; las rutas soportadas tienen equivalencia comprobada y las restantes mantienen el clásico explícitamente. No declarar cerrado H4 por una imagen idéntica o un replay sin fallos.

## H5. Scroll y movimiento suaves

- [ ] **H5.1 — Asistente:** medir el ritmo real de simulación y presentación antes del cambio; conservar los ritmos clásicos. **Se adelanta su inicio a H4:** comparar clásico, registro/contraste y publicación nueva en las mismas escenas y condiciones; CPU, tiempos p95/p99, memoria, copias y subidas a GPU cuando esa ruta exista. Herramienta inicial `measure_presentation_cost.py`: compara clásico, auditoría y publicación, calentamiento y orden rotatorio, con H3 obligatorio. [Primera medición](H5_1_MEDICION_INICIAL.md): 24 fases PASS con H3, resultados en tmpfs; dos intentos locales rechazados y conservados. Mide tiempo del proceso completo; p95/p99 por frame, CPU, memoria y GPU siguen pendientes. No inventar un presupuesto ni confundirlo con FPS. **Avance 2.69:** [coste integrado HD](H6_COSTE_HD_INTEGRADO.md): tiempo, CPU y RSS del proceso completo con H3; faltan atribución por bloque, percentiles de frame y GPU.
- [ ] **H5.2 — Asistente:** interpolar la cámara con posiciones fraccionarias, manteniendo márgenes suficientes de dibujo y límites del mapa.
- [ ] **H5.3 — Asistente:** interpolar entidades según su propio ritmo de actualización. No confundir suavizar posición con cambiar la duración de sus animaciones.
- [ ] **H5.4 — Asistente:** reiniciar interpolación ante carga, salto de cámara, pausa, muerte/reaparición y reutilización de identificadores de sprites.
- [ ] **H5.5 — Asistente:** resolver y probar la correspondencia ratón → ventana → cámara visual → mundo. Medir el retraso visual de interpolación y su efecto al apuntar. **Avance 2.35:** [contrato y modelo verificable](TRANSFORMACIONES_PANTALLA.md), con inversa, bandas, HUD, cámara y anclajes; **Avance 2.36:** [adaptador de misión](H5_5_TRANSFORMACION_MISION.md) opcional, dibujo y ratón absoluto compartidos; equivalencia local con offsets clásicos comprobada. **Avance 2.38:** CI Windows/Linux cerrada y aceptación manual general de Miguel recibida. Pendientes matriz detallada de resolución/DPI, ratón relativo, cámara interpolada y otros modos/escenas.
- [ ] **H5.6 — Asistente:** opciones de presentación: clásico/moderno, monitor, resolución, ventana/sin bordes y exclusiva si se valida, escala de interfaz, calidad, sincronización y límite de FPS. Detectar modos admitidos, confirmar cambios en 15 segundos y recuperar configuración anterior ante fallo. Persistencia segura sin cambiar velocidad de juego. **Avance 2.49–2.52:** CLASSIC/FIT y transacción SAVE/KEEP/REVERT implementados, CI cerrada; guardado/persistencia aceptados por Miguel el 30-10 (2.62). Monitor/modos/FPS/interfaz independiente siguen pendientes.
- [ ] **H5.7 — Asistente / Miguel:** validar a 60 Hz: desplazamientos lentos/rápidos, diagonales, esquinas, seguimiento, selección y disparos junto al panel.
- [ ] **H5.8 — Asistente / Miguel:** medir 120/144 Hz si el monitor lo permite, después de cerrar 60 Hz. Registrar lo no probado.

- [ ] **H5.9 — Asistente:** soportar la [matriz 4:3/16:9 hasta UHD](RESOLUCIONES_PC_HASTA_4K.md), ventana redimensionable, píxeles físicos separados de coordenadas de ventana, DPI 100/125/150/175/200/300 % y transformaciones de entrada verificadas. **Avance 2.51–2.52:** política FIT común para todas las rutas de escenas y F11; pruebas hasta UHD/300 % y CI aprobadas, recorrido común aceptado por Miguel; matriz exhaustiva pendiente.
- [ ] **H5.10 — Asistente / Miguel:** viewport e interfaz modernos nativos 4:3/16:9, sin estirar la imagen clásica. Separar visibilidad de dibujo y lógica antes de mostrar más mapa; conservar encuadre clásico y revisar explícitamente la información táctica del panorámico.

**Aceptación:** mismo estado lógico en replays, ausencia de huecos o temblores en bordes, panel estable y clics coherentes con lo mostrado. A 60 Hz el presupuesto por fotograma es 16,67 ms; evaluar intervalos y percentiles, no solo una media de FPS. Los objetivos de mayor frecuencia son secundarios hasta que 60 Hz esté resuelto.

Para el piloto, cruzar tipos/SPT/recursos y estados de la fase seleccionada. El catálogo completo se amplía en H8, sin bloquear el pequeño lote del soldado. El helicóptero controlable se mantiene como primer caso compuesto posterior, fuera de la entrega A; preservar cuerpo/hélice/sombra/ocupantes y altura cuando se aborde.

## H6. Dirección artística y cadena de recursos

- [ ] **H6.1 — Asistente:** presentar unas pocas muestras comparables del mismo soldado y fragmento de escenario, claramente identificadas como conceptos. **Parcial:** [tres direcciones A01/B01/C01 presentadas](H6_1_COMPARATIVA_ABC.md), con pose/escenario similares. Detalle, posición e integración de C01 aceptados en el HTML; falta comprobar el nuevo lote animado y su escena. Las láminas no son recursos integrados; C sí está aprobada como dirección y tiene una pose experimental aparte.
- [x] **H6.2 — Miguel:** dirección elegida: **C — Pintado moderado**, por su toque Nintendo. A descartado; B no elegido. La aprobación del estilo no equivale a aceptar el recurso integrado.
- [ ] **H6.3 — Asistente:** definir resolución de recursos, paleta, proporciones, contornos, sombras y nivel de detalle. Evaluar 2×/4× y densidades mayores cuando lo requiera UHD, sin multiplicar el tamaño lógico. Conservar maestros HD y derivar variantes automáticamente; fijar densidad tras probar 720p/1080p/1440p/4K con terreno y sprites juntos.
- [ ] **H6.4 — Asistente:** definir el manifiesto de atlas: ID, región, escala, anclaje de pies, dirección y fotograma. Atlas significa una imagen que agrupa varios sprites. Añadir densidad, variantes, márgenes para filtrado y límites de textura; no crear un atlas manual por resolución de monitor.
- [ ] **H6.5 — Asistente:** preparar carga, validación y sustitución individual de recursos, con retorno automático al original cuando falte uno nuevo. **Parcial:** pose C01 incorporada en compilación, sustitución acotada y fallback comprobados; cargador/atlas HD generales pendientes.
- [ ] **H6.6 — Asistente:** validar transparencias, márgenes, unión de tiles, pivotes, ciclos de animación y consistencia entre direcciones.
- [ ] **H6.7 — Asistente:** registrar procedencia y condiciones de uso de cada recurso; separar recursos propios de los originales. **Hecho para el piloto:** manifiestos, prompts, hashes y PNG originales C01 y A/B/C en assets/modernization; mantenerlo para futuros recursos.

**Aceptación:** muestra aprobada y recursos reproducibles que el motor pueda cargar correctamente. No producir cientos de imágenes antes de comprobar cómo funcionan juntas dentro del juego.

## H7. Primera misión moderna completa

**Candidata de trabajo para A:** Amiga The One m1p1. Confirmar inventario y cobertura del recorrido antes de producir recursos; si no los ejercita, seleccionar otra fase pública grabada y documentarlo. Usar datos Amiga no impide ejecutar el juego en Windows.

- [ ] **H7.1 — Asistente:** inventariar todos los recursos realmente utilizados por la fase elegida y fijar su grabación de referencia.
- [ ] **H7.2 — Asistente:** sustituir suelo, caminos, agua, vegetación y obstáculos que aparezcan en esa fase.
- [ ] **H7.3 — Asistente:** completar soldados y enemigos con todas las direcciones y estados usados: desplazamiento, disparo, daño y muerte.
- [ ] **H7.4 — Asistente:** completar edificios, objetos interactivos, proyectiles, explosiones y las variantes destruidas necesarias.
- [ ] **H7.5 — Asistente:** incorporar sombras y efectos cosméticos sin gastar plazas de sprites ni aleatoriedad de la simulación.
- [ ] **H7.6 — Asistente:** rediseñar panel, selección, cursor y textos, sin perder información ni alterar zonas de clic. **Requisito explícito de Miguel (2.44):** cursor artístico completo en dirección C, con variantes/estados, punto activo conservado, contraste, tamaño visual adaptado a resolución/DPI y retorno al original; no se limita a renovar personajes, objetos y fondos.
- [ ] **H7.7 — Asistente:** verificar recortes por agua, superposiciones, anclajes y congruencia entre aspecto y colisiones; comparar replays y rendimiento.
- [ ] **H7.8 — Miguel:** jugar la fase y valorar legibilidad, estilo y respuesta. Registrar cambios solicitados por separado de errores funcionales.

- [ ] **H7.9 — Asistente / Miguel:** validar la primera misión moderna en 4:3 y 16:9, incluidos los extremos de la matriz y una salida UHD, con interfaz legible y anclajes correctos.

**Aceptación:** una fase se puede completar de principio a fin con cámara suave y presentación nueva coherente; sus recursos necesarios están cubiertos y la jugabilidad verificada. No basta una captura atractiva ni una demostración aislada de scroll.

## H8. Extender el resultado a Cannon Fodder 1

- [x] **H8.1 — Asistente / Miguel:** edición/campaña principal confirmada: Cannon Fodder 1 CD32, con datos originales recibidos y comprobados privadamente. Esto no acredita cobertura ni replays de sus 72 fases. Mantener esos datos fuera de GitHub.
- [ ] **H8.2 — Asistente:** generar un inventario real de recursos y variantes de esa edición: biomas, tropas, civiles, vehículos, edificios, armas, interfaz y pantallas auxiliares.
- [ ] **H8.3 — Asistente:** crear una matriz de cobertura por conjunto de recursos, con estados pendiente/provisional/final y escenarios que los ejercitan. **Avance:** censo CD32 de 72 fases/24 misiones, 72 IDs SPT incluyendo Null, cinco conjuntos de entorno; manejadores localizados. [Censo](CD32_CENSO_SPRITES.md). **Avance 2.28:** [capacidades de vehículos](CD32_CAPACIDADES_VEHICULOS.md), grafo parcial dinámico y escenarios con recursos contrastados. **Pendiente:** otras familias, ejecución/captura de esos estados, tiles y variantes; no confundir presencia estática con prueba jugable.
- [ ] **H8.4 — Asistente:** completar escenarios por lotes coherentes y verificar uniones, destrucción, animaciones y colores de cada lote.
- [ ] **H8.5 — Asistente:** completar vehículos, civiles, elementos especiales y efectos que no aparezcan en la primera fase.
- [ ] **H8.6 — Asistente:** cubrir menús, briefing, reclutas, servicio, mapa y textos incluidos en el alcance; conservar variantes clásicas donde se acuerde explícitamente.
- [ ] **H8.7 — Asistente:** detectar recursos faltantes automáticamente y ejecutar regresión con los nuevos escenarios disponibles.
- [ ] **H8.8 — Miguel:** validar muestras representativas de cada lote sin tener que repetir manualmente todas las pruebas automatizadas.

**Aceptación:** la matriz del alcance acordado no contiene recursos provisionales o ausencias ocultas. El fallback permite jugar durante el desarrollo, pero no sirve para declarar modernización completa de un recurso todavía original.

## H9. Pulido y validación final Windows

- [ ] **H9.1 — Asistente:** ejecutar las referencias lógicas disponibles con ambas rutas de presentación y los límites de FPS soportados.
- [ ] **H9.2 — Asistente:** revisar errores de memoria, cargas y liberación de texturas, cambios de fase y sesiones largas en los entornos disponibles.
- [ ] **H9.3 — Asistente / Miguel:** verificar toda la matriz de resoluciones mediante render automatizado y registrar aparte pruebas Windows/GPU reales; ventana/pantalla completa, redimensionado, monitor, pausa, Alt+Tab, ratón, minimapa, guardado/carga y DPI 100/125/150/175/200/300 %. Probar retorno de configuración inválida.
- [ ] **H9.4 — Asistente / Miguel:** medir rendimiento y memoria en el PC de Miguel a 720p/1080p/1440p/UHD y 4:3 representativos. Objetivo inicial 60 Hz hasta UHD sujeto a medición p95/p99; 120/144 Hz donde sea viable. Registrar GPU/DPI/calidad y corregir cuellos de botella demostrados.
- [ ] **H9.5 — Asistente:** verificar persistencia de opciones, mensajes comprensibles y recuperación ante recurso faltante o inválido.
- [ ] **H9.6 — Asistente / Miguel:** realizar una sesión de juego suficientemente larga para cubrir varias fases y transiciones; anotar duración y cobertura real.

**Aceptación:** no hay errores bloqueantes conocidos en el alcance acordado; las limitaciones menores quedan identificadas y aceptadas. La cobertura y los monitores probados se describen, sin prometer compatibilidad universal.

## H10. Entrega y mantenimiento

- [ ] **H10.1 — Asistente:** preparar una versión candidata con número, commit, configuración de construcción y cambios documentados.
- [ ] **H10.2 — Asistente:** generar un paquete Windows reproducible con dependencias necesarias, licencias e instrucciones de datos y arranque.
- [ ] **H10.3 — Asistente / Miguel:** validar instalación en carpeta limpia, actualización sin perder partidas y retorno a una versión anterior.
- [ ] **H10.4 — Asistente:** revisar que el paquete y el código distribuido contienen los avisos y materiales correspondientes, sin incluir datos comerciales ajenos.
- [ ] **H10.5 — Miguel / asistente:** confirmar la aceptación del resultado y el alcance de la publicación; después etiquetar/publicar la versión cuando esté autorizado.
- [ ] **H10.6 — Asistente:** cerrar la matriz de cobertura y dejar una lista breve de mejoras opcionales posteriores, separada de defectos pendientes.

**Definición de objetivo conseguido:** presentación renovada en todo el alcance acordado de Cannon Fodder 1, cámara y movimiento suaves, reglas conservadas según las pruebas, paquete Windows reproducible y validación de juego real de Miguel. Una base que compila o una sola misión HD no cumplen por sí solas esta definición.

## 6. Publicación opcional: implementación y puertas pendientes

**La publicación opcional ya está implementada.** `1e1f93d3` pasó 11 fases con H3 original tanto en ejecución normal como con ASan/UBSan/LSan, pero TSan activo agotó el tiempo. `acfc099a` refuerza el control de avisos y acota TSan a dos fases explícitas. Windows y Linux están aprobados; TSan activo cubre dos fases explícitas. [Resultados y diagnóstico](H4_3_PUBLICACION_ORDENES.md). La validación acfc099a ya está cerrada en su alcance. La programación 0/1/5 de misión está validada en bd2b3d2; la ampliación conjunta misión↔pausa y la sonda acotada tienen CI aprobada en su alcance; consultar [H4.6](H4_6_PLANIFICACION_MISION.md). Las condiciones siguientes siguen siendo las puertas de aceptación de H4, no una lista de trabajo ya completado.

### 6.1 Implementación mínima y contraste

1. Definir qué frame y destinos son elegibles: captura completa, geometría/identidad compatibles, paleta efectiva, escena y generación vigentes. Conservar por separado `mSurface` y `mSurfaceFinal`; no publicar el segundo como si fuera el primero.
2. Componer desde órdenes propias y activar la publicación mediante una opción desactivada por defecto. Mantener las coordinadoras y efectos lógicos una sola vez y en sus momentos originales.
3. Conservar el resultado clásico como referencia independiente y comparar índices, fondo guardado y RGB, incluidos padding y escrituras que no cambian el color aparente. Una divergencia en un frame elegible debe fallar en pruebas/diagnóstico estricto, sin quedar escondida por el retorno al clásico.
4. Si no hay captura elegible o la escena todavía no está soportada, usar el clásico con motivo observable. Ante sustitución/liberación de destinos, invalidar el frame sin escribir sobre almacenamiento incorrecto; acordar explícitamente la política de presentación durante la transición. No reutilizar silenciosamente una captura de otra fase.
5. Mantener pausa y su fondo persistente con el contrato ya extraído. Probar misión→pausa→misión, paleta tardía, cursor temprano/tardío, superficies de distinto tamaño y recursos modificados o reemplazados con las mismas dimensiones.

### 6.2 Puertas de validación

| Puerta | Condición para aceptar |
|---|---|
| Equivalencia de presentación | Clásico y compositor coinciden en destinos, índices, fondo guardado y RGB; se detecta una divergencia introducida deliberadamente |
| 0/1/N | Motor completo probado con 0, 1 y varias presentaciones —inicialmente N=5— sin alterar trazas lógicas, RNG ni efectos; documentar cómo se programa esa frecuencia |
| Recursos y transiciones | Capturas retenidas siguen siendo propias; destinos obsoletos se rechazan; pausa/carga/fase no reutilizan estados incorrectos |
| Regresión | H3 original intacto, replays públicos sin omisiones y pruebas focalizadas mantenidas; comparar también estados entre políticas de presentación, no solo finalización |
| Memoria y concurrencia | ASan/UBSan, LSan y TSan con la ruta nueva activa en escenarios representativos; registrar exclusiones, sin atribuirle los resultados del recorrido headless habitual |
| Rendimiento | Medición H5.1 comparable con registro apagado, auditoría activa y publicación nueva; limitar retención/copias y resolver regresiones demostradas |
| Windows real | Compilar/empaquetar y comprobar ventana/GPU, pausa, F11, Alt+Tab, cursor y audio con la opción activa; vídeo software Linux no sustituye esta prueba |

Las primeras entregas pueden conservar la opción experimental y desactivada mientras se amplía cobertura. No activar por defecto ni declarar independencia global antes de completar estas puertas. La prueba manual se solicitará cuando exista un paquete concreto; no hace falta reinstalar nada por esta revisión documental.

### 6.3 Después de esa publicación

Completar el contrato semántico de H4.2/H4.4 para cámara y entidades, preservando el orden real; probar generaciones y discontinuidades. Con un piloto validado, iniciar H5 con gráficos originales. Elegir una fase pequeña, inventariarla y aprobar una muestra H6 antes de pasar a producción H7. Extender después por lotes H8 y cerrar validación/entrega H9–H10.

## 7. Tareas transversales incorporadas

- [ ] **C1 — Evidencias duraderas:** conservar ZIP completos, logs y trazas que sustentan aceptaciones, con SHA-256 y relación commit/entorno, en almacenamiento persistente apropiado. Los informes compactos de b34373b0 ya están en Git; los ZIP de esa revisión caducan el **24-11-2026** y hay evidencias anteriores que caducan antes. Los dos ZIP de `b34373b0` ya están archivados con [manifiesto](evidence/b34373b0-archive.json); también se conserva el intento `1e1f93d3`, incluido su TSan fallido. Pendientes referencias anteriores y próximas revisiones; no se programa actividad automática.
- [ ] **C2 — Reproducción:** mantener SHAs efectivos de dependencias/datos públicos, configuración, comandos y paquete probado en cada aceptación. No basta fijar una rama flotante ni prometer compilación bit a bit idéntica. No actualizar dependencias ajenas a la tarea sin motivo.
- [ ] **C3 — Cobertura explícita:** mantener matriz de rutas clásica/nueva, PC/Amiga, escenarios, frecuencia, plataforma y validación automática/manual. Separar demos, CD32 privado, audio físico y GPU. Añadir cobertura comercial progresiva cuando haya grabaciones válidas; no convertir 72 omisiones por falta de replays en 72 aprobaciones.

C1–C3 son obligaciones continuas con entregas verificables; no sustituyen ni renumeran H0–H10.

## 8. Decisiones y riesgos vigentes

| ID | Decisión | Situación / momento |
|---|---|---|
| D1 | Estilo gráfico | C — Pintado moderado elegido en H6.2; densidad HD e integración general pendientes, incluido cursor |
| D2 | Edición y fase piloto | CD32 confirmada como campaña principal; concretar fase demo pequeña antes de H7.1 |
| D3 | Campo de visión | Conservar área lógica original; cualquier ampliación será una decisión posterior explícita |
| D4 | Refresco y equipo | 60 Hz primero; recoger monitor/configuración para H5.7, 120/144 Hz después si procede |
| D5 | Pantallas auxiliares | Inventario H5.9 y FIT común implementados, recorrido común aceptado; matriz exhaustiva y arte moderno pendientes |

La elección C está cerrada. Ambas densidades están revisadas visualmente por Miguel; prefiere mayor detalle si memoria/rendimiento lo permiten. Medir antes de fijar la densidad final.

| ID | Riesgo actual | Tratamiento |
|---|---|---|
| R1 | Caso mínimo RNC histórico sin atribuir | Exclusión aceptada H2.6; lector actual acotado probado. Reabrir si aparece evidencia nueva pertinente |
| R2 | Dibujo aún ligado a efectos lógicos | H4.1/H4.6: preservar coordinadoras y comparar trazas con 0/1/N |
| R3 | Interpolación con retraso o puntería desajustada | H5.4/H5.5: discontinuidades, transformación del ratón y prueba real |
| R4 | Diferencias entre plataformas o configuraciones | Mismas referencias y condiciones documentadas; no tolerancias arbitrarias |
| R5 | Arte incoherente o producción innecesaria | Muestra jugable y manifiesto antes de producción masiva |
| R6 | Vista ampliada que modifica la dificultad | Mantener campo lógico original |
| R7 | Falta de cobertura comercial completa | C3 y H8: CD32 disponible no equivale a 72 fases verificadas |
| R8 | Confundir CI verde con validación total | Matriz de evidencia, sanitizadores activos y Windows real |
| R9 | Capturas obsoletas o retención/copias excesivas | Contrato temporal, invalidación y medición H4/H5.1 |
| R10 | Pérdida de evidencias por caducidad | C1: archivo permanente y manifiesto de integridad |

## 9. Continuidad y criterio de cierre

Al retomar: leer la ruta operativa de este plan, [CONTINUIDAD](CONTINUIDAD.md) y los contratos afectados; comprobar HEAD/PR y las pruebas de la revisión vigente; trabajar en un incremento pequeño; registrar código, pruebas, límites y siguiente paso. Los commits documentales no cambian el motor validado. No repetir pruebas costosas por cambios solo documentales, ni reutilizar un verde antiguo para aceptar código nuevo.

El [plan v2.19 íntegro](PLAN_TRABAJO_HISTORICO_HASTA_2_19.md) conserva la bitácora anterior. Sus «siguientes pasos» son históricos; el siguiente vigente está en la tarea activa y en CONTINUIDAD.md; la sección 6 conserva las puertas globales de H4. El [diseño inicial](PLAN_MODERNIZACION_ES.md) conserva razones y propuestas, subordinadas al estado verificado aquí.

El proyecto terminará cuando el alcance acordado de Cannon Fodder 1 tenga presentación renovada coherente, cámara y movimiento suaves, jugabilidad conservada según la cobertura documentada, paquete Windows reproducible y validación real de Miguel. Una base estable, un compositor equivalente o una sola misión moderna son hitos intermedios. El PR permanecerá sin fusionar conforme a la instrucción vigente.
