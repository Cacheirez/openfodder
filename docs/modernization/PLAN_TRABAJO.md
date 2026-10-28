# Plan de trabajo — Cannon Fodder modernizado para Windows

**Versión 2.44 · Revisión: 28 de octubre de 2026.**
Responsable técnico: asistente. Validación de juego y decisiones visuales: Miguel.
**Tarea activa: resolver el escalado del mapa general tras precisar ventana maximizada frente a fullscreen F11. Bordes del cursor aceptados por Miguel; rediseño artístico del cursor incluido expresamente.**

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

## 1. Dictamen de la revisión

El objetivo y la arquitectura general siguen siendo válidos. Hemos avanzado bastante más que el inventario que todavía indicaban algunas casillas: existen capturas propias, composición ordenada, validación de destinos y registro conectado a productores reales. Sin embargo, reconstruir el mismo frame no equivale aún a poder presentar con otra frecuencia ni a interpolar entidades por separado. **H4 sigue abierto. El diseño conceptual H6.1 puede empezar ya; la integración necesita el contrato semántico mínimo, no cerrar todas las escenas.**

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
| Motor candidato | `46c180be3f456175834917646b04815a166c2d75`; Windows/Linux aprobados; este incremento posterior solo modifica documentación |
| Último motor con aceptación global previa | `acfc099a43d02d55bf44426b6c05a2f0330cf889` (alcance descrito en H4.3) |
| Base clásica aceptada | `baseline/classic-h2.6-2026-10-22` → `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8` |
| CI Windows 46c180be | [40377396759](https://github.com/Cacheirez/openfodder/actions/runs/40377396759), éxito |
| CI Linux 46c180be | [40377396760](https://github.com/Cacheirez/openfodder/actions/runs/40377396760), éxito, incluidos los diagnósticos de memoria y concurrencia declarados |
| Publicación desde órdenes | Implementada, opcional y con contraste obligatorio; validada en acfc099a con el alcance de pruebas declarado. H4 global sigue abierto. Clásico por defecto |
| Interpolación / arte | Pendientes |

| Evidencia conservada | Qué acredita | Límite |
|---|---|---|
| H3 original | 11.361 estados: 7.956 PC y 3.405 Amiga, conservados en Windows/Linux | 11 fases, no toda CD32 ni todos los estados posibles |
| Replays habituales | 29/29 fases, cero omisiones; 6 CTests y controles de CI aprobados | Completar no demuestra por sí solo igualdad visual o interacción real |
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
| H5 · Cámara y movimiento suaves | Pendiente; adelantar medición H5.1 | Piloto H4 validado con gráficos originales |
| H6 · Arte y recursos | Pendiente | Conceptos independientes; integración depende del contrato de presentación |
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

- [ ] **H5.1 — Asistente:** medir el ritmo real de simulación y presentación antes del cambio; conservar los ritmos clásicos. **Se adelanta su inicio a H4:** comparar clásico, registro/contraste y publicación nueva en las mismas escenas y condiciones; CPU, tiempos p95/p99, memoria, copias y subidas a GPU cuando esa ruta exista. Herramienta inicial `measure_presentation_cost.py`: compara clásico, auditoría y publicación, calentamiento y orden rotatorio, con H3 obligatorio. [Primera medición](H5_1_MEDICION_INICIAL.md): 24 fases PASS con H3, resultados en tmpfs; dos intentos locales rechazados y conservados. Mide tiempo del proceso completo; p95/p99 por frame, CPU, memoria y GPU siguen pendientes. No inventar un presupuesto ni confundirlo con FPS.
- [ ] **H5.2 — Asistente:** interpolar la cámara con posiciones fraccionarias, manteniendo márgenes suficientes de dibujo y límites del mapa.
- [ ] **H5.3 — Asistente:** interpolar entidades según su propio ritmo de actualización. No confundir suavizar posición con cambiar la duración de sus animaciones.
- [ ] **H5.4 — Asistente:** reiniciar interpolación ante carga, salto de cámara, pausa, muerte/reaparición y reutilización de identificadores de sprites.
- [ ] **H5.5 — Asistente:** resolver y probar la correspondencia ratón → ventana → cámara visual → mundo. Medir el retraso visual de interpolación y su efecto al apuntar. **Avance 2.35:** [contrato y modelo verificable](TRANSFORMACIONES_PANTALLA.md), con inversa, bandas, HUD, cámara y anclajes; **Avance 2.36:** [adaptador de misión](H5_5_TRANSFORMACION_MISION.md) opcional, dibujo y ratón absoluto compartidos; equivalencia local con offsets clásicos comprobada. **Avance 2.38:** CI Windows/Linux cerrada y aceptación manual general de Miguel recibida. Pendientes matriz detallada de resolución/DPI, ratón relativo, cámara interpolada y otros modos/escenas.
- [ ] **H5.6 — Asistente:** opciones de presentación: clásico/moderno, monitor, resolución, ventana/sin bordes y exclusiva si se valida, escala de interfaz, calidad, sincronización y límite de FPS. Detectar modos admitidos, confirmar cambios en 15 segundos y recuperar configuración anterior ante fallo. Persistencia segura sin cambiar velocidad de juego.
- [ ] **H5.7 — Asistente / Miguel:** validar a 60 Hz: desplazamientos lentos/rápidos, diagonales, esquinas, seguimiento, selección y disparos junto al panel.
- [ ] **H5.8 — Asistente / Miguel:** medir 120/144 Hz si el monitor lo permite, después de cerrar 60 Hz. Registrar lo no probado.

- [ ] **H5.9 — Asistente:** soportar la [matriz 4:3/16:9 hasta UHD](RESOLUCIONES_PC_HASTA_4K.md), ventana redimensionable, píxeles físicos separados de coordenadas de ventana, DPI 100/125/150/175/200 % y transformaciones de entrada verificadas.
- [ ] **H5.10 — Asistente / Miguel:** viewport e interfaz modernos nativos 4:3/16:9, sin estirar la imagen clásica. Separar visibilidad de dibujo y lógica antes de mostrar más mapa; conservar encuadre clásico y revisar explícitamente la información táctica del panorámico.

**Aceptación:** mismo estado lógico en replays, ausencia de huecos o temblores en bordes, panel estable y clics coherentes con lo mostrado. A 60 Hz el presupuesto por fotograma es 16,67 ms; evaluar intervalos y percentiles, no solo una media de FPS. Los objetivos de mayor frecuencia son secundarios hasta que 60 Hz esté resuelto.

Antes de ampliar la captura semántica, cruzar tipos de motor + SPT de todas las fases + recursos y estados. El helicóptero controlable será el primer caso compuesto después del soldado; preservar cuerpo/hélice/sombra/ocupantes y altura. El diseño conceptual puede continuar, pero el catálogo de producción no se limita a las demos.

## H6. Dirección artística y cadena de recursos

- [ ] **H6.1 — Asistente:** presentar unas pocas muestras comparables del mismo soldado y fragmento de escenario, claramente identificadas como conceptos. **Parcial:** [tres direcciones A01/B01/C01 presentadas](H6_1_COMPARATIVA_ABC.md), con pose/escenario similares. Falta comprobar a escala real la dirección elegida. Ninguna está integrada ni aprobada.
- [x] **H6.2 — Miguel:** dirección elegida: **C — Pintado moderado**, por su toque Nintendo. A descartado; B no elegido. La aprobación del estilo no equivale a aceptar el recurso integrado.
- [ ] **H6.3 — Asistente:** definir resolución de recursos, paleta, proporciones, contornos, sombras y nivel de detalle. Evaluar 2×/4× y densidades mayores cuando lo requiera UHD, sin multiplicar el tamaño lógico. Conservar maestros HD y derivar variantes automáticamente; fijar densidad tras probar 720p/1080p/1440p/4K con terreno y sprites juntos.
- [ ] **H6.4 — Asistente:** definir el manifiesto de atlas: ID, región, escala, anclaje de pies, dirección y fotograma. Atlas significa una imagen que agrupa varios sprites. Añadir densidad, variantes, márgenes para filtrado y límites de textura; no crear un atlas manual por resolución de monitor.
- [ ] **H6.5 — Asistente:** preparar carga, validación y sustitución individual de recursos, con retorno automático al original cuando falte uno nuevo.
- [ ] **H6.6 — Asistente:** validar transparencias, márgenes, unión de tiles, pivotes, ciclos de animación y consistencia entre direcciones.
- [ ] **H6.7 — Asistente:** registrar procedencia y condiciones de uso de cada recurso; separar recursos propios de los originales.

**Aceptación:** muestra aprobada y recursos reproducibles que el motor pueda cargar correctamente. No producir cientos de imágenes antes de comprobar cómo funcionan juntas dentro del juego.

## H7. Primera misión moderna completa

**Escenario inicial propuesto:** una fase pequeña de jungla de Cannon Fodder 1 disponible como demo —por ejemplo Amiga The One—, a concretar antes de H7.1 y de producir sus recursos. Usar datos Amiga no impide ejecutar el juego en Windows.

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
- [ ] **H9.3 — Asistente / Miguel:** verificar toda la matriz de resoluciones mediante render automatizado y registrar aparte pruebas Windows/GPU reales; ventana/pantalla completa, redimensionado, monitor, pausa, Alt+Tab, ratón, minimapa, guardado/carga y DPI 100/125/150/175/200 %. Probar retorno de configuración inválida.
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

**La publicación opcional ya está implementada.** `1e1f93d3` pasó 11 fases con H3 original tanto en ejecución normal como con ASan/UBSan/LSan, pero TSan activo agotó el tiempo. `acfc099a` refuerza el control de avisos y acota TSan a dos fases explícitas. Windows y Linux están aprobados; TSan activo cubre dos fases explícitas. [Resultados y diagnóstico](H4_3_PUBLICACION_ORDENES.md). La validación acfc099a ya está cerrada en su alcance. La programación 0/1/5 de misión está validada en bd2b3d2; la ampliación conjunta misión↔pausa tiene PASS local y CI propia pendiente; consultar [H4.6](H4_6_PLANIFICACION_MISION.md). Las condiciones siguientes siguen siendo las puertas de aceptación de H4, no una lista de trabajo ya completado.

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
| D1 | Estilo gráfico | Pendiente de muestras comparables y elección de Miguel en H6.2 |
| D2 | Edición y fase piloto | CD32 confirmada como campaña principal; concretar fase demo pequeña antes de H7.1 |
| D3 | Campo de visión | Conservar área lógica original; cualquier ampliación será una decisión posterior explícita |
| D4 | Refresco y equipo | 60 Hz primero; recoger monitor/configuración para H5.7, 120/144 Hz después si procede |
| D5 | Pantallas auxiliares | Inventariar en H8.2 y acordar su cobertura; una excepción clásica debe quedar explícita |

No hay una decisión artística que bloquee el siguiente incremento H4.

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

Al retomar: leer este plan y el [relevo técnico](README.md), comprobar HEAD/PR y las pruebas de la revisión vigente; trabajar en un incremento pequeño; registrar código, pruebas, límites y siguiente paso. Los commits documentales no cambian el motor validado. No repetir pruebas costosas por cambios solo documentales, ni reutilizar un verde antiguo para aceptar código nuevo.

El [plan v2.19 íntegro](PLAN_TRABAJO_HISTORICO_HASTA_2_19.md) conserva la bitácora anterior. Sus «siguientes pasos» son históricos; el siguiente vigente es la sección 6 de este documento. El [diseño inicial](PLAN_MODERNIZACION_ES.md) conserva razones y propuestas, subordinadas al estado verificado aquí.

El proyecto terminará cuando el alcance acordado de Cannon Fodder 1 tenga presentación renovada coherente, cámara y movimiento suaves, jugabilidad conservada según la cobertura documentada, paquete Windows reproducible y validación real de Miguel. Una base estable, un compositor equivalente o una sola misión moderna son hitos intermedios. El PR permanecerá sin fusionar conforme a la instrucción vigente.
