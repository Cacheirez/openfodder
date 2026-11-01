> **OBSOLETO COMO PLAN DE EJECUCIÓN.** Sustituido por [PLAN_TRABAJO.md](PLAN_TRABAJO.md). Se conserva únicamente como histórico; sus tareas pendientes no determinan el trabajo vigente.

# Bitácora del plan 2.28–2.69

Estado histórico. La tarea vigente está en [PLAN_TRABAJO.md](PLAN_TRABAJO.md). Se conservan los incrementos íntegros, con sus resultados y pendientes de cada fecha.

## Incremento 2.69 — C01 aceptado y medición integrada

Miguel acepta explícitamente detalle, posición e integración al abrir C01_12.html. [Alcance y ensayo](H6_COSTE_HD_INTEGRADO.md): comparación visual aceptada, sin extrapolar a todas las animaciones o GPU. Se mide el motor completo con SDL software en clásico, publicación, HD 8× y HD 12×, campaña Amiga completa y H3 por ejecución. Motor y paquete 3ee12e9 conservados; ensayo tmpfs completo PASS: 16 recorridos/48 fases con H3, cuatro calentamientos y tres muestras por modo. Medianas de campaña: clásico 19,924 s; publicación 49,621 s; HD 8× 76,816 s; HD 12× 76,551 s. Sin diferencia concluyente entre densidades. Intento previo de escritura local rechazado y conservado; siguiente paso, perfilado por bloque, no reducir calidad ni prometer FPS. No se fija densidad ni se produce arte adicional.

## Incremento 2.68 — diagnóstico, prueba visible y paquete cerrados

[Validación 3ee12e9](VALIDACION_3ee12e9.md): Windows 41288644622, Linux 41288644597 y comparador 41288644598 completos PASS. Prueba visible C01 en ambas plataformas y densidades: ocho fases PC y 7.956 estados H3 originales por ejecución; exportaciones idénticas entre Windows/Linux/local. Regresión HD: 11 fases, 22 pausas y 11.361 estados por ejecución. ZIP 13077821521 verificado: 300 archivos, ejecutable coincidente, comparaciones y ocho grabaciones PC públicas, lanzador automático y diagnóstico. Se corrige el include MSVC del intento 7d27b59; no cambia H3 ni composición. Pendientes aceptación visual Windows/GPU y coste integrado; PR borrador sin fusionar.

## Incremento 2.67 — diagnóstico y prueba visible C01

Miguel confirma funcionamiento correcto sin diferencia visual; ambos logs carecen de SOLDIER_HD_SDL. [Diagnóstico y prueba](H6_C01_DIAGNOSTICO_VISIBLE.md): motivos acotados por proceso, exportación optativa del primer parche publicado y comparación del mismo instante con clásico. El paquete incluirá HTML/BMP verificados y PROBAR_C01_VISIBLE.cmd con ocho grabaciones PC públicas. No se fuerza la sustitución ni se desactivan guards. Arrancar directamente en m2p1 muestra C01 pero no reproduce el H3 de campaña; se usa PC completo sin regenerar referencias. Nueva CI/paquete pendientes.

## Incremento 2.66 — CI y paquete HD SDL cerrados

[Validación a05e656](VALIDACION_a05e656.md): Windows 41197313659, Linux 41197313403 y comparador 41197313475 completos PASS. Informes HD 8×/12× en ambos sistemas: 11 fases, 22 pausas/reanudaciones y 11.361 estados H3 originales por ejecución; publicación HD real en PC/Amiga. ZIP Windows 13041734254 inspeccionado: 281 archivos, 29 demos sin omisiones, ejecutable coincidente con los informes, dos lanzadores HD y VERSION con árbol idéntico al commit probado. Escalado/transiciones/fallos automatizados aprobados; Windows/GPU físico y coste integrado pendientes. PR en borrador, sin fusionar.

## Incremento 2.65 — presupuesto de CI Windows

4856a8f resuelve la sonda: local 8×/12× y paso HD Linux PASS. Windows supera 8× completo y PC 12×, pero el job cancela Amiga 12× al cumplir 35 minutos (41194788492). Se amplía a 60 minutos, manteniendo las 11 fases y cinco presentaciones de 12×. Nueva CI y paquete pendientes; no se atribuye PASS a la ejecución cancelada. [Evidencia](evidence/hd-sdl-replay-fix-2026-10-31.json).

## Incremento 2.64 — pausa por fase en replays restaurados

CI 75a91ff compiló y superó las pruebas SDL, pero falló al exigir 16 pausas en PC: la sonda buscaba ticks absolutos 8/16 y siete fases PC/Amiga restauran relojes posteriores. Ahora cuenta pasos elegibles dentro de cada fase sin modificar relojes de simulación. Se conserva la campaña completa, se refuerza la puerta para exigir pasos 8/16 en cada fase y se incluyen informes HD en el artefacto Linux. 31 tests Python PASS; replays locales completos 8×/12× PASS (11 fases, 22 pausas y 11.361 estados por ejecución), nueva CI en validación. No se cambian referencias H3.

## Incremento 2.63 — SDL opcional con recuperación clásica

[Contrato y evidencia](H6_HD_SDL_OPCIONAL.md). Texturas temporales de fondo nativo y parche HD, misma transformación de pantalla, validación de escena/destino y vuelta a clásico ante error. Escala entera contra oráculo completo; fraccionaria conserva exactamente exterior clásico SDL, sin exigir idéntico muestreo interior. Pruebas software y método real local PASS; CI nueva y paquete pendientes. Se cierra CI 832895d en las tres plataformas. Opciones aceptadas; sin cambios de simulación, H3 u originales.

## Incremento 2.62 — composición eficiente y opciones aceptadas

[Contrato y pruebas](H6_COMPOSICION_HD_POR_CAPAS.md): fondo nativo más parche HD precompuesto; equivalencia exacta con el compositor completo en pruebas PC/Amiga 1×/8×/12× y guards de retorno clásico. Implementación aislada, aún sin SDL ni nueva oclusión parcial. No cambia motor activo, H3 ni originales. Miguel confirma que las opciones guardan y mantienen valores; REVERT/caducidad no se atribuyen como pruebas manuales separadas. CI nueva pendiente.

## Incremento 2.61 — coste HD medido antes de integración

[Ensayo reproducible](H6_COSTE_HD_AISLADO.md), 108 procesos/21.600 muestras. Escalado completo CPU 12× no es una ruta adecuada para el objetivo de 60 Hz en este entorno: Amiga compleja mediana 39,398 ms frente a 11,126 ms a 8×. Mantener calidad 12× como candidata de recurso, desacoplar densidad de textura y destino de composición antes de integrar. No se fija densidad ni se modifica el motor. MSVC corregido en 3d82ff2; CI Windows/Linux/comparador completa PASS y paquete verificado, [cierre](VALIDACION_3d82ff2.md). Save pendiente de aceptación física.

## Incremento 2.60 — portabilidad del generador HD y medición en curso

La CI Windows de d2e05e8 (40903703370) falla al compilar el generador: std::to_string requiere `<string>` explícito en MSVC. Se añade ese include sin alterar píxeles, algoritmo ni motor. El PASS Linux no sustituye Windows; la CI de la nueva revisión y su paquete quedan pendientes. [Registro del fallo](evidence/windows-d2e05e8-build-failure.json). Medición CPU/memoria aislada 8×/12× en preparación, sin integrar HD ni fijar densidad.

## Incremento 2.59 — causa de Save reproducida y corregida

[Diagnóstico](H5_6_INCIDENCIA_SAVE.md): `?` se transforma en frame 54, pero las fuentes Briefing PC/Amiga solo tienen 37. `Sprite_Get_Sheet` devuelve nullptr y GUI_Draw_Frame_8 lo desreferencia. Fixture nueva de funciones reales y tablas reales reproduce fallo UBSan antes del cambio; después pasa con `KEEP CHANGES 15`, durante cuenta atrás 0..15 y botones. Integrada en CTest y Linux ASan/UBSan. Regresiones de transacción y fades conservadas. No se modifican fuentes, tablas o raster, ni se atribuye prueba física Windows. Se conserva el registro diagnóstico por si el entorno muestra otra causa. CI/paquete propios pendientes, PR sigue borrador.

## Incremento 2.58 — composición HD aislada y nueva incidencia Save

[Contrato y piloto HD](H6_4_PILOTO_HD_AISLADO.md): destino privado 8×/12×, equivalencia nativa 1×, anclaje y orden conservados mediante guards clásicos; fallback completo ante oclusión/recorte/pitch no soportados. Derivados reproducibles desde el PNG original, sin alterar el header nativo. 132 casos de retorno y comprobaciones alfa/detalle/destinos/0-1-5/presupuesto PASS local ASan/UBSan. CTest Windows/Linux añadido. No es HD integrado en el juego ni prueba de rendimiento/GPU.

Miguel acepta ambas densidades del comparador, con preferencia por más detalle si el coste lo permite; no se fija densidad final. Confirma alternancia correcta, pero [Save cierra antes de KEEP/REVERT](H5_6_INCIDENCIA_SAVE.md). La fixture actual pasa, no reproduce el fallo real. Se añade registro optativo y se habilita en el lanzador de opciones; **no se declara corregido**. Escenas aceptadas y cursor pendiente. Regresiones locales: C01 nativo 64 casos, opciones y 30 tests Python PASS. CI propia/paquete se registrarán tras publicar, sin heredar el verde de 30ba0ec.

## Incremento 2.57 — relevo a un nuevo hilo

Revisión de continuidad solicitada por Miguel. [Cierre del relevo](RELEVO_2026-10-29.md): CI 30ba0ec reconfirmada, originales visuales contrastados con sus manifiestos, enlaces locales y JSON revisados. Se corrige la receta que aún apuntaba al motor e18b05b. README, estado, plan y prompt sincronizados; informes históricos conservados como evidencia fechada.

Siguiente tarea autónoma explícita: contrato y piloto aislado de composición HD de una pose C01, parametrizado 8×/12×, conservando orden, destinos, oclusión, recorte, anclaje y fallback. No se ha implementado todavía. Opciones y elección de densidad siguen pendientes de Miguel, sin bloquear esta preparación. Cambio solo documental: no altera motor, recursos, H3 ni paquete validado.

## Incremento 2.56 — cierre automático de opciones y visor

[Validación 30ba0ec](VALIDACION_30ba0ec.json): Windows 40800994744, Linux 40800994727 y navegador 40800994726 completos PASS. Paquete 12866468476 verificado por SHA-256, ejecutable/PRUEBAS.json y árbol de VERSION temporal; 279 entradas, 29 fases sin omisiones, siete CTest. Incluye pulsación única a1c8856. El intento Windows anterior fue cancelado por la política del workflow al publicar otra revisión; no fue un PASS completo.

Comparador autónomo final verificado byte a byte contra Git; capturas DPR 1/3 inspeccionadas. Modelo reproduce C01 nativo y compara 8×/12× a huella física igual. No hay elección de densidad ni composición HD del juego todavía. Trabajo independiente de la aceptación del menú completado; próxima preparación técnica posible: contrato/destino HD conservando orden/oclusiones y fallback. La prueba manual de opciones puede esperar a Miguel. Esta revisión solo registra resultados, sin cambiar motor ni herramienta.

## Incremento 2.55 — preparación independiente de densidades

Miguel autoriza continuar sin esperar a su validación de opciones. [Visor autónomo C01](../../assets/modernization/density-review/README.md): mismo maestro, promedio premultiplicado, recorte/caja/anclaje y tamaño físico para 8×/12×; salidas 4:3/16:9, PC/Amiga, DPR compensado y ampliación de inspección separada. No genera nuevos dibujos ni toca Source. Equivalencia exacta 1× con header nativo y 96 combinaciones geométricas PASS. Builder verifica SHA del original y genera HTML autónomo reproducible. Primera CI específica f842b3d aprobada: modelo, bundle y navegador/capturas; [evidencia](H6_DENSIDAD_VALIDACION_f842b3d.json). Ajuste de inspección posterior (2× por defecto y scroll completo a 4×) vuelve a comprobarse en su CI. La instalación local de Chromium no pudo completarse por descarga incompleta, por lo que no se afirma inspección visual local.

Esto adelanta preparación y evaluación técnica; no elige densidad ni da por aceptadas opciones. Opciones a1c8856 requieren su paquete y prueba manual. Después de revisar resultados del comparador, decidir densidad y diseñar composición HD antes de animaciones masivas; el motor sigue componiendo C01 a 16×14.

## Incremento 2.54 — escenas aceptadas y clic único en opciones

Miguel confirma «Probar escenas está ok» y comunica que CLASSIC/FIT y ON/OFF cambian y vuelven inmediatamente. [Incidencia y reproducción](H5_6_INCIDENCIA_CLIC_REPETIDO.md): el bucle reenviaba el estado mantenido del botón; el limitador permitía repetir cada 90 ms. Ahora consume una sola pulsación con Mouse_Button_Left_Toggled, conservando ratón, dispatcher GUI y productores clásicos. La fixture extrae también el bloque real del bucle y las funciones reales de botones/GUI: falla antes del cambio y pasa después, incluidos clics sostenidos, soltar/repulsar, arrastre desde fuera y SAVE/KEEP separados. Se mantienen las pruebas de transacción, persistencia y fallos SDL. Nuevo motor necesita CI/paquete propios; el ZIP e18b05b aún tiene el defecto. No repetir todo el recorrido de escenas ni avanzar a densidad antes de cerrar opciones.

## Incremento 2.53 — auditoría documental y conservación de bocetos

Corregidos índice de relevo, tabla del motor vigente y avances H5/H6 que seguían anclados a revisiones anteriores. [Auditoría e inventario documental](AUDITORIA_CONTINUIDAD_2026-10-28.md). Archivados en Git los cuatro PNG originales B inicial/B refinada/A/C, sin recodificar, con manifiesto SHA-256 y [galería](../../assets/modernization/concepts/README.md). Fuente transparente C01 contrastada con su manifiesto y original recuperado. No se genera arte nuevo ni se altera el motor. [Estado autónomo](CONTINUIDAD.md) recoge aceptaciones manuales, límites, flags, siguiente incremento y formato obligatorio de mensajes. Logs/trazas/binarios caducables y datos comerciales privados conservan sus exclusiones explícitas.


## Incremento 2.52 — CI y paquete de escenas verificados

[Evidencia e18b05b](H5_9_VALIDACION_e18b05b.json): Windows 40760804335 y Linux 40760804513 completos PASS, incluidos los diagnósticos declarados y las regresiones H3/C01. Siete CTest Windows, incluida transacción de opciones; 29 fases sin omisiones. [ZIP 12849036551](https://github.com/Cacheirez/openfodder/actions/runs/40760804335/artifacts/12849036551) verificado por SHA256 y hash del ejecutable, 279 entradas, nuevo PROBAR_ESCENAS_H5.cmd y PROBAR_OPCIONES_H5.cmd. VERSION identifica el merge temporal de prueba b87c5e1, con árbol idéntico a e18b05b; el PR sigue sin fusionar.

Pendiente prueba física de escenas comunes, Heroes in Victory y opciones en Windows UHD/300 %. Recorrido: introducciones → reclutamiento/briefing → misión → pausa/mapa → servicio/ascensos → siguiente misión, alternando maximizar/F11; después persistencia, KEEP/REVERT y retorno CLASSIC. No marcar finales o ediciones no visitadas como aceptados. Comparación 8×/12× tras esta aceptación. Este incremento solo registra evidencia y guía; no cambia motor ni paquete.

## Incremento 2.51 — inventario de escenas y FIT común en ventana/F11

Miguel acepta las dos ventanas previas y comunica Heroes in Victory sin ajustar. [Inventario completo y criterio](H5_9_INVENTARIO_ESCENAS.md): política central en RenderAt/RenderShrunk para no excluir servicio, menús, cargar/guardar, opciones, créditos, intros o finales. FIT ahora conserva el aspecto también en F11; CLASSIC permanece original. Vídeo conserva aspecto propio y clic para saltar; ya no hereda una inversa GUI anterior. Nuevo lanzador PROBAR_ESCENAS_H5.cmd sin --skipintro.

864 combinaciones nuevas de GUI/F11/imágenes y auditoría de todas las rutas SDL PASS local; regresiones de misión, mapa, pausa, briefing/reclutamiento, superficies y opciones PASS. Windows y Linux de 263f897 completos PASS (runs 40717230013 y 40717229801); Linux incluye diagnósticos ASan/UBSan/LSan y TSan declarados. Esta ampliación necesita su propia CI y prueba visual. No confundir el paquete anterior con uno que contenga Heroes/F11 común. Base clásica, mejoras, C01, H3 y PR en borrador sin fusionar conservados.

## Incremento 2.50 — paquete Windows verificado y control Linux ajustado

[Evidencia](H5_6_VALIDACION_551eaf7.json). Windows 40713267240 completo PASS, siete CTest incluida la transacción de opciones, ZIP 12828685981 verificado por SHA256, ejecutable coincidente con PRUEBAS.json, 29 fases sin omisiones, 278 entradas y guía 2.49. Incluye las correcciones de briefing/reclutamiento y ambos lanzadores. VERSION.txt es el merge temporal de prueba del PR, con árbol idéntico a 551eaf7; no implica fusión.

Linux 40713267277 falla en una igualdad de archivo completo del menú contra la base anterior a H5.6. Se incorpora una excepción exacta por huellas de ambas versiones, verificando también las dos llamadas directas a fade en su método y condiciones; el resto de comparaciones permanece intacto. No cambia el motor, las referencias H3 ni el contenido jugable del ZIP. Prueba local del control corregido: 27.648 casos de superficie PASS; rechaza mutaciones no revisadas. Nueva CI global pendiente. Prueba física de opciones e introducciones en Windows pendiente de Miguel; densidad visual después.

## Incremento 2.49 — pausa aceptada, opciones y pantallas previas

Miguel confirma «funciona la pausa perfectamente» y aporta capturas de briefing y reclutamiento que no se ajustan al maximizar. Se extiende el ajuste solo a esas parejas escena/superficie, con inversa de ratón de la imagen presentada e identidad de escena; diálogos y F11 conservan ruta clásica. Se evita desmaximizar una ventana ajustada cuando cambia la resolución lógica.

[Opciones H5.6](H5_6_OPCIONES_PRESENTACION.md): edición diferida, CLASSIC/FIT, confirmación de 15 segundos, cancelación/restauración y guardado mediante archivo temporal. Nuevo lanzador sin overrides de presentación. Pruebas locales de métodos reales y SDL simulado PASS; 144 casos de intro, regresiones de misión/pausa/mapa y capas PASS. Nueva CI pendiente; no atribuirle el verde del paquete de pausa 63c4d6f. [Densidad: evaluación inicial](H6_DENSIDAD_EVALUACION.md), sin nueva producción de arte. Base clásica, C01, todas las mejoras y H3 conservados; PR en borrador sin fusionar.

## Incremento 2.48 — paquete de pausa verificado y opciones preparadas

[Evidencia de pausa](H5_9_VALIDACION_63c4d6f.json): Windows 40667967583 PASS, ZIP 12807892335 verificado por SHA256, 277 entradas, guía actualizada, 29 fases y sonda de pausa PC/Amiga con 301 estados H3. VERSION.txt identifica el merge temporal de prueba con árbol idéntico a 63c4d6f. Linux global 40667967516 también completado PASS, incluida pausa ThreadSanitizer. Pendiente maximizar → P → restaurar/maximizar → P → órdenes en Windows UHD/300 %. [Primer corte de opciones H5.6](H5_6_OPCIONES_PRESENTACION.md) preparado, implementación tras validar pausa; densidad artística sin fijar. Revisión documental, sin cambios de motor.

## Incremento 2.47 — mapa aceptado y pausa ajustada

Miguel confirma mapa centrado, cierre y regreso a misión correctos; Linux 40634973034 completo PASS. [Evidencia de cierre](H5_9_VALIDACION_6e98fda.json). Se continúa H5.5/H5.9 con [pausa ajustada](H5_9_PAUSA_AJUSTADA.md): mantiene el destino de misión, admite resize/DPI y no reutiliza coordenadas pausadas al reanudar. 72 transiciones locales nuevas y regresiones de pausa/cursores/mapa/capas PASS; sonda CI ampliada a pausa real y H3. Validación del nuevo código pendiente. Después de aceptar pausa, avanzar a opciones mínimas H5.6 y evaluación de densidad del arte C; no ampliar escenas indefinidamente. Base clásica, mejoras y PR sin fusionar conservados.


## Incremento 2.46 — paquete del mapa verificado

[Estado y evidencia](H5_9_VALIDACION_6e98fda.json). Windows 40634973004 completo PASS. [ZIP verificado](https://github.com/Cacheirez/openfodder/actions/runs/40634973004/artifacts/12793692851): hash contrastado, 277 entradas, tres lanzadores, guía y 29 fases aprobadas sin omisiones. VERSION.txt 7c596ea identifica el commit temporal de prueba del PR, con árbol idéntico a 6e98fda; no implica fusión. Validación física del mapa pendiente en la edición que permite abrirlo; las demos de release no bastan. Linux global sigue en curso al registrar. Esta revisión es documental; no amplía escenas ni cambia código, H3 o arte.


## Incremento 2.45 — mapa centrado y ajustado a la ventana

[Aclaración, implementación y límites](H5_9_MAPA_GENERAL_Y_ACEPTACION_BORDES.md). Corrección limitada a la superficie del mapa general activo en el modo opcional de ajuste en ventana. Usa salida física, conserva aspecto clásico y fuente completa; F11 y demás rutas intactos. Fixture real: 216 casos de overview hasta UHD/300 %, exclusiones y retorno a misión, además de las regresiones de cursor existentes. CI y aceptación física nuevas pendientes; las demos de release no validan automáticamente la overview. Base clásica, mejoras y PR sin fusionar conservados.


## Incremento 2.44 — bordes aceptados, mapa pendiente y cursor artístico

Miguel confirma corregida la incidencia y aprobados los puntos 4 y 5. [Registro y nueva incidencia](H5_9_MAPA_GENERAL_Y_ACEPTACION_BORDES.md): el mapa aparece pequeño arriba a la izquierda al abrirlo a pantalla completa. Localizada la ruta RenderShrunk, que conserva tamaño heredado y origen (0,0) en ventana; falta confirmar el modo de pantalla concreto. El cursor se incluye en H6/H7 con estados, punto activo y legibilidad a distintas escalas. Sin cambios de motor en esta revisión. Base clásica, mejoras y PR sin fusionar conservados.


## Incremento 2.43 — cierre de CI y paquete corregido verificado

[Evidencia de 1447abb](H5_9_VALIDACION_1447abb.json): Windows 40588401900 y Linux 40588409211 completos PASS, incluidos los recorridos de sanitizadores declarados. [ZIP corregido](https://github.com/Cacheirez/openfodder/actions/runs/40588401900/artifacts/12774266903): VERSION.txt idéntico al commit, SHA-256 contrastado, 277 entradas, tres lanzadores y guía; 29 fases aprobadas sin omisiones. Extraer en carpeta nueva y ejecutar `PROBAR_RESOLUCIONES_H5.cmd`. Pendiente repetir maximización y cruces de ambos bordes al 300 % en el Windows de Miguel. Revisión documental: base clásica, mejoras, H3 y PR sin fusionar conservados.


## Incremento 2.42 — cursor continuo al cruzar bandas

[Aclaración y corrección](H5_9_INCIDENCIA_BORDES_300.md). Miguel confirma que solo ocurre maximizado al tocar los límites laterales de la imagen. Se muestra el puntero Windows en bandas y se ocultan únicamente los píxeles del cursor retenido; las decisiones y registros clásicos se conservan. Pruebas locales de geometría/entrada, cursor/HUD, recursos y productores PASS ASan/UBSan. Nueva CI y validación física pendientes. Base clásica, H3, C01 y mejoras conservadas; PR sin fusionar.


## Incremento 2.41 — incidencia manual y cobertura DPI 300 %

[Reporte, análisis y límites](H5_9_INCIDENCIA_BORDES_300.md). Ampliadas las pruebas a 228 combinaciones reales con dobles SDL y 360 racionales, aprobadas localmente. Barrido UHD/300 % reproduce retención del cursor en bandas y actualización inmediata en la primera muestra interior. Falta precisar dónde observa Miguel la pausa antes de atribuirle esa causa. No se cambia el motor ni se declara arreglado. CI anterior Windows/Linux aprobada; nueva ejecución de tests pendiente. PR sin fusionar.


## Incremento 2.40 — cierre de CI y entrega del ajuste Windows

Código `45de47a4` aprobado completamente en Windows 40542788013 y Linux 40542787684, incluidos los recorridos de sanitizadores declarados. [Evidencia y verificación del paquete](H5_9_CIERRE_CI_45de47a4.json). ZIP: 277 entradas, tres lanzadores CRLF, guía y 29 fases aprobadas sin omisiones. [Descarga para Miguel](https://github.com/Cacheirez/openfodder/actions/runs/40542788013/artifacts/12753080638): ejecutar `PROBAR_RESOLUCIONES_H5.cmd` y comprobar redimensionamiento, bandas, selección y órdenes. Aceptación física del nuevo ajuste pendiente; no se extrapola la aceptación del piloto anterior. Esta revisión solo documenta resultados; conserva código, arte, referencias H3 y PR sin fusionar.


## Incremento 2.39 — ajuste de misión a ventanas hasta UHD

[Implementación y pruebas](H5_9_AJUSTE_VENTANAS.md). Nuevo lanzador `PROBAR_RESOLUCIONES_H5.cmd`, ventana redimensionable y densidad de salida física. Se conserva el encuadre y aspecto de píxel aceptado, sin mostrar más mapa ni fijar densidad de arte. Pruebas locales del método real con 190 combinaciones de tamaño/backend/DPI, además de 544.000 coordenadas clásicas. CI nueva pendiente; aceptación manual anterior no se extrapola al ajuste. Base clásica, C01 y H3 conservados, PR sin fusionar.


## Incremento 2.38 — aceptación manual general en Windows

Miguel confirma el 27-10-2026: «funciona perfectamente, no noto diferencias con respecto a Open Fodder original.» Se registra como aceptación general del piloto presentado, sin incidencias observadas. [Alcance y siguiente incremento](H5_5_ACEPTACION_MANUAL_WINDOWS.md). No se solicitará repetir la prueba general; la matriz de resoluciones/DPI y casos no desglosados se comprobará al ampliar el ajuste. H5.5/H5.9 siguen parciales, arte C y base clásica conservados; PR abierto y sin fusionar.


## Incremento 2.37 — cierre automático y paquete Windows de validación

**Cierre automático:** `c8c54ab99bd4438e324108d07c08a516ba993ad4` aprobado en [Windows 40523807564](https://github.com/Cacheirez/openfodder/actions/runs/40523807564) y [Linux 40523793992](https://github.com/Cacheirez/openfodder/actions/runs/40523793992). [Evidencia completa y verificación del ZIP](H5_5_CIERRE_CI_c8c54ab.json). Las incidencias históricas de los guards descritas abajo están resueltas. Pendiente únicamente la aceptación interactiva de este incremento; H5.5/H5.9 globales siguen abiertos.

[Estado 4e8e211](H5_5_VALIDACION_4e8e211.json): Windows completo PASS; Linux supera HUD y falla después en la identidad histórica de Window.cpp. Las dos puertas afectadas ahora exigen hashes exactos de la versión clásica y del adaptador revisado, cuya conducta prueba la fixture real. No se altera Source ni H3. Corregida además la dependencia de un commit no descargado en la fixture nueva: usa la referencia de ratón ya descargada por CI. Local: 2.944 casos de capas, 1.536 raster, 1.964 escenas, 1.024 tiles, 72 minimapas y 544.000 coordenadas, PASS ASan/UBSan sin LSan local. Paquete Windows añade lanzadores H5/clásico y [guía manual](VALIDAR_RATON_WINDOWS_H5.md); observación de Miguel pendiente.

## Incremento 2.36 — integración de pantalla en misión

CI global C01 1bcf69c cerrada: Windows/Linux completos aprobados, evidencia `closure` en [informe](H6_3_CI_1bcf69c.json). [Integración opcional](H5_5_TRANSFORMACION_MISION.md): snapshot del rectángulo realmente dibujado y publicado, inversa para ratón absoluto, offsets clásicos, invalidación y retorno. 544.000 coordenadas PC/Amiga contrastadas con métodos reales y dobles SDL; regresiones conservadas. Sonda de replay SDL y compilación aprobadas en Windows/Linux (fb4a997); Linux falla después en una puerta histórica de identidad completa de Mouse.cpp. Se corrige para admitir solo el nuevo adaptador literal y mantener el resto protegido; cierre global nuevo pendiente. No cambia el encuadre ni introduce HD/panorámico.

## Incremento 2.35 — CI C01 y transformaciones

[CI del motor 1bcf69c](H6_3_CI_1bcf69c.json): Windows completo PASS, 11 fases y 11.361 estados H3 originales; sustitución artística en 7 escenas PC y 2 Amiga. Paso C01 Linux PASS; flujo completo Linux aún en ejecución al registrar la evidencia. [Contrato de pantalla](TRANSFORMACIONES_PANTALLA.md): canvas, recorte, aspecto, destino físico, ventana/DPI, cámara, ratón inverso, bandas/HUD y anclajes independientes de densidad. Modelo racional: cinco pruebas locales, 300 combinaciones de geometría, añadido a CI. No modifica el motor ni conecta aún SDL; H5.5/H5.9 siguen parciales.

## Incremento 2.34 — resoluciones PC hasta 4K

Requisito de Miguel incorporado: ventanas y pantalla completa en resoluciones habituales 4:3 y 16:9, hasta 3840×2160. Matriz mínima explícita, tamaños intermedios por detección de monitor, DPI, interfaz, cursor, recuperación de modos y composición HD. Encuadre clásico disponible; viewport panorámico nativo condicionado a independencia de visibilidad lógica y revisión de la información táctica adicional. No se fija 4× como techo del arte. Solo planificación, no soporte ya implementado. [Especificación y aceptación](RESOLUCIONES_PC_HASTA_4K.md).

## Incremento 2.33 — pose C01 RGBA

Elección C confirmada por Miguel. Recurso transparente generado, cuadro nativo 16×14 y anclaje contrastado con tablas PC/Amiga. Sustitución de hoja 7/frame 0, contraste clásico intacto y diferencias RGB autorizadas solo dentro del cuerpo. Fallback ante solapamientos, recortes, fundidos y estados no cubiertos. Pruebas locales y puerta de cobertura; CI del motor nuevo pendiente. [Contrato y límites](H6_3_POSE_C01.md).

## Incremento 2.32 — comparación visual A/B/C

Presentadas las tres direcciones: píxel refinado, 2D ilustrado limpio y pintado moderado. Recomendación de trabajo: B01; elección H6.2 pendiente de Miguel. Son conceptos con pequeñas variaciones de geometría y miniaturas orientativas, no recursos integrados. Falta comprobación a escala real. [Comparación y prompts](H6_1_COMPARATIVA_ABC.md). Código del motor sin cambios.

## Incremento 2.31 — revisión de CI y primera muestra visual

Windows y Linux de 46c180be aprobados, incluidos ASan/UBSan/LSan y los recorridos TSan declarados. Se cierra la validación automática de este incremento, no H4 global ni la aceptación manual GPU/CD32. [Evidencia conservada](H4_4_VALIDACION_46c180be.json). Primera muestra H6.1 B01 generada y refinada: soldado y jungla en 2D ilustrado limpio, con reducción orientativa. No integrada ni aprobada como estilo final; faltan variantes comparables y escala real. [Muestra, revisión y prompts](H6_1_MUESTRA_B01.md).

## Incremento 2.30 — sustitución individual de pose

Selección de una pose original, imagen indexada inmutable, sustitución en el orden de capas original y retorno al clásico ante clave/recorte/recurso incompatibles. Contraste obligatorio también de la ruta sustituida; una divergencia no se oculta como fallback. 46 casos focalizados, ocho configuraciones de productores/pausa con 384 transiciones y29 pruebas Python PASS. Windows y Linux 46c180be aprobados. No es arte nuevo ni interpolación. [Contrato, reproducción y evidencia](H4_4_POSE_INDIVIDUAL.md).

## Incremento 2.29 — soldado semántico

Captura opcional del primer Player junto al productor real: identidad/escena/generación, posición/cámara, anclajes y recurso original retenido. El compositor reproduce desde esa captura con contraste obligatorio; se rechazan geometrías inconsistentes. Pruebas focalizadas y28 pruebas Python PASS. CI anterior d1d30f12 Windows/Linux aprobada; CI de d28d99f9 Windows aprobada, Linux pendiente. No es interpolación ni arte integrado. [Implementación, reproducción y límites](H4_2_SOLDADO_SEMANTICO.md).

## Incremento 2.28 — capacidades de vehículos

[Matriz fundamentada](CD32_CAPACIDADES_VEHICULOS.md): entrada/ocupación/salida, llamada y vuelo, daño condicional, auxiliares y transformaciones dinámicas. Siete escenarios CD32 seleccionados sobre cinco entornos; todos pendientes de ejecución. Manifiesto con fuentes fijadas y comprobador de relaciones/metadata, sin simulación alternativa. Motor, H3 y base clásica intactos. El contrato semántico está propuesto, no implementado; el siguiente incremento reproduce un soldado original sin esperar a catalogar todas las familias.

