# Plan de trabajo vivo — OpenFodder modernizado para Windows

**Versión del plan:** 2.17 · **Actualización:** 25 de octubre de 2026, Europe/Madrid.
**Responsable técnico:** asistente, con ejecución y verificación en cada sesión del chat.  
**Responsable de validación de usuario:** Miguel.  
**Estado del incremento actual:** validación de identidad/geometría de destinos implementada y validada en CI Windows/Linux sobre `40d67a0`; 97 aceptaciones y 627 rechazos; [informe](H4_1_DESTINOS_PRESENTACION.md).

**Último estado verificado del motor:** H2.6 aceptado y base clásica intacta. Nuevo incremento H4: frame de misión ya compuesto con recursos propios y prueba integrada de coordinadoras misión↔pausa 0/1/5. 240 escenarios y 672 capturas retenidas; backing persistente de pausa conservado independientemente de la presentación. [Alcance y resultados](H4_1_FRAME_MISION.md). Release local, 6 CTests, H3 original 11.361 estados y 29/29 replays PASS; CI Windows/Linux aprobada; no confundir estas pruebas con capas independientes, GPU o replay completo 0/1/N. H4 sigue abierto.

**Entrada para nuevos equipos:** [guía de relevo](README.md), [matriz PC/Amiga](DIFERENCIAS_PC_AMIGA.md) e [informes conservados en Git](evidence/40d67a0-reports.json).

## 1. Objetivo y alcance

Modernizar Cannon Fodder para Windows conservando su jugabilidad: controles, reglas, tiempos, dificultad, colisiones, comportamiento de enemigos y objetivos. Renovaremos personajes, vehículos, edificios, terreno, elementos, efectos e interfaz, y haremos más suave el desplazamiento de cámara y entidades.

La base será OpenFodder, C++ y SDL3. La primera meta será una misión de muestra completa y jugable con presentación moderna; después extenderemos ese resultado al alcance acordado del primer Cannon Fodder. La modernización completa de Cannon Fodder 2 queda fuera de la primera versión, aunque no debemos romper deliberadamente su funcionamiento existente.

**Este documento es el seguimiento operativo.** El análisis técnico se conserva en [PLAN_MODERNIZACION_ES.md](PLAN_MODERNIZACION_ES.md), los resultados iniciales en [RESULTADOS.md](RESULTADOS.md) y la prueba de usuario en [PRIMER_ARRANQUE_WINDOWS.md](PRIMER_ARRANQUE_WINDOWS.md).

## 2. Panel de situación

| Campo | Estado comprobado el 25 de octubre de 2026 |
|---|---|
| Repositorio | [Cacheirez/openfodder](https://github.com/Cacheirez/openfodder) |
| Rama de trabajo | `modernization/windows-foundation` |
| Propuesta de cambios | [PR #1, borrador sin fusionar](https://github.com/Cacheirez/openfodder/pull/1) |
| Revisión de código de la propuesta | `40d67a0c0c1d12e246d9da22ff53434ed9930846`: identidad/geometría de destinos, sobre frame compuesto y backing de pausa |
| Compilación Windows observada | [40120465262](https://github.com/Cacheirez/openfodder/actions/runs/40120465262): aprobada |
| Pasos Windows ya comprobados | Compilación, 6 CTests, contrato de visibilidad, H3 PC/Amiga y baseline original PASS |
| Ejecutable Windows y 29 replays | Paquete demos publicado por CI; 29/29 fases, cero omisiones, 23,938 s |
| Referencia local Linux | `049439d`: H3 original 11.361 estados, 29/29 fases sin omisiones |
| Pruebas focalizadas | 97 destinos aceptados y 627 rechazados; 240 escenarios misión/pausa, 672 capturas retenidas; 144 escenarios de pausa 0/1/5; 1.536 raster nuevos, 1.964 escenas, 1.024 tiles, 72 constructores; 2.944 de capas; 27.648 de paleta/superficie; 2.304 cursor y 288 HUD; 7.680 casos de terreno; 10.944 casos de resolución/propiedad; 29.160 de rasterización; 306.432 de recorte; 184.320 transiciones del temporizador |
| Memoria | [Linux 40120465254](https://github.com/Cacheirez/openfodder/actions/runs/40120465254): aprobada |
| Prueba manual Windows | Confirmada por Miguel: demo y campaña CD32 jugables; controles, sonido, pausa, F11 y Alt+Tab correctos |
| Gráficos nuevos / scroll nuevo | Pendientes; ningún cambio en la simulación clásica |
| Tarea activa | **H4.1: capas independientes y cobertura del motor completo tras validar frame compuesto y transición misión↔pausa**. [Implementación y límites](H4_1_FRAME_MISION.md); luego capas independientes y cobertura real pendiente. |
| Siguiente intervención de Miguel | Conservar la carpeta probada; sin nueva instalación necesaria ahora |

El estado de Actions es una observación, no un seguimiento permanente. Antes de aceptar un cambio del motor, comprobar las ejecuciones de su revisión de código vigente. Los commits exclusivos de documentación no sustituyen ni invalidan automáticamente la prueba de la revisión de código precedente.

## 3. Cómo seguiremos el plan en el chat

- `[x]` significa completado con evidencia disponible. `[ ]` significa pendiente, aunque haya trabajo iniciado.
- Cada tarea tiene un ID estable, como **H3.2**. Usaremos esos IDs al conversar y en los cambios del proyecto.
- Al empezar una sesión leeremos la última versión de este archivo en GitHub, el estado de la rama/PR y las pruebas relevantes. No dependeremos solo de la memoria del chat.
- Trabajaremos en una tarea activa o en un lote pequeño que tenga sentido verificar junto.
- Al terminar actualizaremos este mismo archivo: casillas, panel de situación, evidencia, bloqueos, decisiones y siguiente acción. No crearemos un plan distinto por sesión.
- Si una prueba falla, el hito sigue abierto. Registraremos el primer fallo y lo resolveremos o delimitaremos explícitamente antes de avanzar.
- Si falta una decisión artística, puedo seguir con las tareas técnicas independientes. Pediré decisiones concretas, con ejemplos, cuando afecten al resultado.
- La documentación se actualizará separada del código cuando sea posible, evitando reconstrucciones innecesarias por simples cambios de estado.
- Los trabajos se realizan durante las sesiones; este plan no crea avisos, tareas programadas ni actividad autónoma entre mensajes.

**Mensaje suficiente para retomar:** «Seguimos con el plan de OpenFodder; revisa la tarea activa y continúa». Si has hecho una prueba, añade la versión y lo que observaste.

**Formato de cierre de cada sesión:** tarea trabajada → cambio realizado → pruebas y resultados → límite o bloqueo → siguiente paso. Siempre en español y explicando los conceptos nuevos antes de utilizarlos.

## 4. Reglas que protegerán el proyecto

1. Conservar una referencia clásica reproducible y una forma de desactivar las mejoras visuales.
2. No aumentar la velocidad de la simulación para conseguir más imágenes por segundo.
3. No ampliar inicialmente el mundo visible: la visibilidad y el campo de visión pueden influir en comportamiento y dificultad.
4. No alterar colisiones, alcance de armas, velocidad de soldados, temporizadores ni límites de entidades como consecuencia de un recurso gráfico nuevo.
5. Hacer el renderizado adicional de solo lectura. Auditar antes los efectos del dibujo clásico, incluido `mWasDrawn`.
6. Separar la aleatoriedad y el presupuesto de los efectos cosméticos de los del juego.
7. Introducir cambios pequeños y reversibles, con evidencia suficiente. No fusionar automáticamente un borrador por tener un indicador verde.
8. Mantener datos comerciales, partidas y credenciales fuera del repositorio y de los paquetes públicos. Las primeras pruebas usan las demos suministradas por el proyecto.
9. Distinguir «compila», «completa replays», «pasa el detector de memoria» y «se juega correctamente en Windows». Son validaciones diferentes.

## 5. Ruta de hitos

| Hito | Entrega | Depende de | Estado |
|---|---|---|---|
| H0 | Auditoría, referencia y repositorio | — | Completado para el alcance inicial |
| H1 | Primera compilación Windows y arranque verificado | H0 | Completado |
| H2 | Base estabilizada y defectos conocidos delimitados | H1; investigación local puede avanzar antes | Base aceptada en H2.6; H2.1 histórico delimitado y cobertura limitada |
| H3 | Comparación reproducible de jugabilidad | H2 | H3.1–H3.6 completadas en el alcance demo, con pruebas de integración pendientes de H4 |
| H4 | Dibujo separado de la simulación | H3 | H4.1 iniciado: inventario; extracción e independencia pendientes |
| H5 | Cámara y movimiento suaves con gráficos originales | H4 | Pendiente |
| H6 | Dirección artística y recursos de muestra | H1; diseño independiente de H2–H5 | Pendiente |
| H7 | Misión completa con gráficos modernos | H5 y H6 | Pendiente |
| H8 | Cobertura gráfica del alcance de Cannon Fodder 1 | H7 y datos necesarios disponibles | Pendiente |
| H9 | Pulido, regresión y rendimiento Windows | H8; mediciones desde H5 | Pendiente |
| H10 | Versión candidata y paquete final | H9 | Pendiente |

No fijamos fechas de entrega sin medir H4 y el esfuerzo artístico. La estimación se revisará al cerrar H2, H5 y H7. No se considerará acabado el proyecto al completar solo la misión de muestra.

**Actualización de control (21-10-2026):** prueba de los 29 replays Linux con ThreadSanitizer y LeakSanitizer validada mediante `report.json` y `engine.log` dentro del ZIP de evidencias; ambos detectores mostraron **cero hallazgos, 29 fases aprobadas, cero omisiones y retorno 0**. La comprobación de LSan ya es obligatoria en CI; TSan todavía conserva `continue-on-error: true`, por lo que debe revisarse el informe hasta endurecer su puerta. La cobertura real de audio SDL, ventanas interactivas y 72 fases CD32 no está demostrada. Se conserva H3 como barrera de regresión.

**Matriz de referencias y cobertura:** [H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md](H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md). La auditoría H2.5 ha terminado; las versiones flotantes y diferencias de reproducción son riesgos registrados, no defectos de jugabilidad probados.

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

## H2. Estabilización de la base

**H2.5 cerrado (21-10-2026):** [inventario de referencias, versiones y cobertura](H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md). C++14, OpenFodder 1.5.4, SDL3 3.4.0; SDL3_mixer 3.1.0 fijado por commit en Windows, 3.3.0 observado pero sin SHA en Linux; FFmpeg y XMP configurados de forma distinta. Completan 29/29 fases públicas en ambas plataformas, pero H3 registra solo 11 fases/11.361 estados, LSan/TSan solo Linux headless y no hay cobertura total CD32. El cierre documental **no cierra H2.6**.

**Resultado más reciente (21-10-2026):** las 29 fases públicas pasan ASan/UBSan, LeakSanitizer y ThreadSanitizer en [Linux 39641851896](https://github.com/Cacheirez/openfodder/actions/runs/39641851896); también [Windows 39641852057](https://github.com/Cacheirez/openfodder/actions/runs/39641852057) pasa compilación, 29 replays y referencia H3. Las pérdidas de `scandir()` y objetos Duktape `cPosition`, y las carreras de temporización/callback/preparación de fase se corrigieron sin rebaselinar H3. Este resultado **complementa y reemplaza operativamente** los diagnósticos históricos de 23/17 avisos que aparecen más abajo. La cobertura solo abarca rutas ejecutadas. Informe detallado: [H2_LEAK_THREAD_DIAGNOSTICOS.md](H2_LEAK_THREAD_DIAGNOSTICOS.md).


**Actualización 21-10-2026:** [H2_ESTABILIZACION_2026-10-21.md](H2_ESTABILIZACION_2026-10-21.md). H2.2 dispone de lector RNC acotado: 88 recursos RNC y 1.047 casos inválidos probados con ASan/UBSan en Linux, 29 replays Windows y equivalencia de 11.361 estados previos/posteriores al cambio en ambas plataformas. **H2.3: corregidos los bloqueos de tablas de direcciones y fotogramas; la nueva ejecución ASan Linux llega a 29 fases, pero hay 23 avisos UBSan pendientes. Consultar [informe de protección de fotogramas](H2_3_PROTECCION_FOTOGRAMAS_2026-10-21.md).** La atribución del recurso mínimo del fallo original (H2.1), ASan del motor completo (H2.3), sincronización integral (H2.4) y aceptación H2.6 quedan abiertos.


- [ ] **H2.1 — Asistente:** aislar el acceso fuera de límites en `Source/Amiga/dernc.cpp`, con un recurso mínimo que lo reproduzca y longitudes de entrada/salida identificadas.
- [x] **H2.2 — Asistente:** corregir la causa y probar truncamientos/límites del descompresor; no ocultar el fallo desactivando el detector ni añadiendo relleno sin justificar.
- [x] **H2.3 — Asistente:** ejecutar ASan/UBSan y LeakSanitizer sobre los 29 replays públicos con cero hallazgos. **Alcance demo cerrado; campañas privadas y flujos interactivos no cubiertos.**
- [x] **H2.4 — Asistente:** proteger música Amiga, callback, temporización y transiciones de fase; confirmar ThreadSanitizer sin carreras en 29/29 replays públicos y H3 inalterado. **Auditoría demo terminada; todavía no implica cobertura general de audio real, ventanas, menús ni H4.**
- [x] **H2.5 — Asistente:** inventariar versiones reales y referencias fijadas por plataforma, documentar diferencias de SDL_mixer/XMP/FFmpeg, cobertura 29/11 fases y huecos de CD32/audio. **Cerrado como auditoría** en [H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md](H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md); la versión Linux de SDL_mixer sigue sin SHA fijado y se trata en H2.6.
- [x] **H2.6 — Asistente / Miguel:** base clásica aceptada el 22-10-2026 en la cobertura documentada, CI de `5c564b19` aprobada y validación CD32 de Miguel. Referencia recuperable `baseline/classic-h2.6-2026-10-22` → `5e6a4f38`; PR sin fusionar. [Decisión y exclusiones](H2_6_ACEPTACION_BASE_CLASICA.md).

**Aceptación:** las rutas incluidas en la primera versión no tienen fallos de memoria reproducibles pendientes sin resolver o delimitar; los replays y el arranque siguen funcionando. Si existe una exclusión, debe figurar con su impacto y no presentarse la suite completa como aprobada.

**Límite actual:** LeakSanitizer no pudo operar en el entorno local inicial; las pruebas posteriores desactivaron solo la detección de fugas. Añadir una comprobación de fugas donde sea viable, sin confundir su ausencia con un resultado favorable.

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

## H4. Separar presentación y simulación

- [ ] **H4.1 — Asistente:** documentar qué funciones de dibujo modifican estado, y trasladar o preservar esos efectos en el paso lógico correspondiente. **Primera extracción implementada:** [efectos principales, pruebas y límites](H4_1_EFECTOS_DIBUJO.md); 11.361 estados H3 preservados localmente y en CI Windows/Linux. La pausa ya tiene estado propio y prueba 0/1/5; faltan ensamblado y pruebas del frame de misión/transiciones. No equivale a independencia global 0/1/N.
- [ ] **H4.2 — Asistente:** introducir estados de presentación coherentes y de solo lectura para cámara, sprites, terreno, paletas e interfaz.
- [ ] **H4.3 — Asistente:** crear rutas clásica y moderna seleccionables, manteniendo inicialmente las imágenes originales.
- [ ] **H4.4 — Asistente:** separar capas de terreno, entidades, efectos, panel y cursor; conservar orden, recortes, fundidos y visibilidad lógica.
- [ ] **H4.5 — Asistente:** asegurar el uso correcto del hilo de ventana/SDL y la entrega de estados entre hilos, sin leer estructuras parcialmente actualizadas.
- [ ] **H4.6 — Asistente:** ejecutar dibujo cero, una y varias veces entre pasos lógicos y comparar las trazas; probar cargas, cambios de fase, minimapa y pausa.

**Aceptación:** dibujar más veces no altera las reglas ni consume aleatoriedad del motor; la imagen clásica sigue siendo una referencia utilizable. No introducir todavía arte nuevo que dificulte comparar resultados.

## H5. Scroll y movimiento suaves

- [ ] **H5.1 — Asistente:** medir el ritmo real de simulación y presentación antes del cambio; conservar los ritmos clásicos.
- [ ] **H5.2 — Asistente:** interpolar la cámara con posiciones fraccionarias, manteniendo márgenes suficientes de dibujo y límites del mapa.
- [ ] **H5.3 — Asistente:** interpolar entidades según su propio ritmo de actualización. No confundir suavizar posición con cambiar la duración de sus animaciones.
- [ ] **H5.4 — Asistente:** reiniciar interpolación ante carga, salto de cámara, pausa, muerte/reaparición y reutilización de identificadores de sprites.
- [ ] **H5.5 — Asistente:** resolver y probar la correspondencia ratón → ventana → cámara visual → mundo. Medir el retraso visual de interpolación y su efecto al apuntar.
- [ ] **H5.6 — Asistente:** añadir opciones de presentación —clásico/moderno, sincronización y límite de FPS cuando proceda— sin que cambien la velocidad de juego.
- [ ] **H5.7 — Asistente / Miguel:** validar a 60 Hz: desplazamientos lentos/rápidos, diagonales, esquinas, seguimiento, selección y disparos junto al panel.
- [ ] **H5.8 — Asistente / Miguel:** medir 120/144 Hz si el monitor lo permite, después de cerrar 60 Hz. Registrar lo no probado.

**Aceptación:** mismo estado lógico en replays, ausencia de huecos o temblores en bordes, panel estable y clics coherentes con lo mostrado. A 60 Hz el presupuesto por fotograma es 16,67 ms; evaluar intervalos y percentiles, no solo una media de FPS. Los objetivos de mayor frecuencia son secundarios hasta que 60 Hz esté resuelto.

## H6. Dirección artística y cadena de recursos

- [ ] **H6.1 — Asistente:** presentar unas pocas muestras comparables del mismo soldado y fragmento de escenario, claramente identificadas como conceptos.
- [ ] **H6.2 — Miguel:** elegir la dirección visual. Propuesta inicial: 2D ilustrado, perspectiva original, siluetas claras y colores legibles; pendiente de aprobación visual.
- [ ] **H6.3 — Asistente:** definir resolución de recursos, paleta, proporciones, contornos, sombras y nivel de detalle. Empezar evaluando recursos 4× sin multiplicar el tamaño lógico del mundo.
- [ ] **H6.4 — Asistente:** definir el manifiesto de atlas: ID, región, escala, anclaje de pies, dirección y fotograma. Atlas significa una imagen que agrupa varios sprites.
- [ ] **H6.5 — Asistente:** preparar carga, validación y sustitución individual de recursos, con retorno automático al original cuando falte uno nuevo.
- [ ] **H6.6 — Asistente:** validar transparencias, márgenes, unión de tiles, pivotes, ciclos de animación y consistencia entre direcciones.
- [ ] **H6.7 — Asistente:** registrar procedencia y condiciones de uso de cada recurso; separar recursos propios de los originales.

**Aceptación:** muestra aprobada y recursos reproducibles que el motor pueda cargar correctamente. No producir cientos de imágenes antes de comprobar cómo funcionan juntas dentro del juego.

## H7. Primera misión moderna completa

**Escenario inicial propuesto:** una fase pequeña de jungla de Cannon Fodder 1 disponible como demo —por ejemplo Amiga The One—, a confirmar al cerrar H1. Usar datos Amiga no impide ejecutar el juego en Windows.

- [ ] **H7.1 — Asistente:** inventariar todos los recursos realmente utilizados por la fase elegida y fijar su grabación de referencia.
- [ ] **H7.2 — Asistente:** sustituir suelo, caminos, agua, vegetación y obstáculos que aparezcan en esa fase.
- [ ] **H7.3 — Asistente:** completar soldados y enemigos con todas las direcciones y estados usados: desplazamiento, disparo, daño y muerte.
- [ ] **H7.4 — Asistente:** completar edificios, objetos interactivos, proyectiles, explosiones y las variantes destruidas necesarias.
- [ ] **H7.5 — Asistente:** incorporar sombras y efectos cosméticos sin gastar plazas de sprites ni aleatoriedad de la simulación.
- [ ] **H7.6 — Asistente:** renovar lo imprescindible de panel, selección, cursor y textos, sin perder información ni alterar zonas de clic.
- [ ] **H7.7 — Asistente:** verificar recortes por agua, superposiciones, anclajes y congruencia entre aspecto y colisiones; comparar replays y rendimiento.
- [ ] **H7.8 — Miguel:** jugar la fase y valorar legibilidad, estilo y respuesta. Registrar cambios solicitados por separado de errores funcionales.

**Aceptación:** una fase se puede completar de principio a fin con cámara suave y presentación nueva coherente; sus recursos necesarios están cubiertos y la jugabilidad verificada. No basta una captura atractiva ni una demostración aislada de scroll.

## H8. Extender el resultado a Cannon Fodder 1

- [ ] **H8.1 — Asistente / Miguel:** confirmar la edición y campaña principal que se quiere cubrir. Para la campaña comercial completa harán falta los datos correspondientes disponibles legítimamente para las pruebas, sin publicarlos en GitHub.
- [ ] **H8.2 — Asistente:** generar un inventario real de recursos y variantes de esa edición: biomas, tropas, civiles, vehículos, edificios, armas, interfaz y pantallas auxiliares.
- [ ] **H8.3 — Asistente:** crear una matriz de cobertura por conjunto de recursos, con estados pendiente/provisional/final y escenarios que los ejercitan.
- [ ] **H8.4 — Asistente:** completar escenarios por lotes coherentes y verificar uniones, destrucción, animaciones y colores de cada lote.
- [ ] **H8.5 — Asistente:** completar vehículos, civiles, elementos especiales y efectos que no aparezcan en la primera fase.
- [ ] **H8.6 — Asistente:** cubrir menús, briefing, reclutas, servicio, mapa y textos incluidos en el alcance; conservar variantes clásicas donde se acuerde explícitamente.
- [ ] **H8.7 — Asistente:** detectar recursos faltantes automáticamente y ejecutar regresión con los nuevos escenarios disponibles.
- [ ] **H8.8 — Miguel:** validar muestras representativas de cada lote sin tener que repetir manualmente todas las pruebas automatizadas.

**Aceptación:** la matriz del alcance acordado no contiene recursos provisionales o ausencias ocultas. El fallback permite jugar durante el desarrollo, pero no sirve para declarar modernización completa de un recurso todavía original.

## H9. Pulido y validación final Windows

- [ ] **H9.1 — Asistente:** ejecutar las referencias lógicas disponibles con ambas rutas de presentación y los límites de FPS soportados.
- [ ] **H9.2 — Asistente:** revisar errores de memoria, cargas y liberación de texturas, cambios de fase y sesiones largas en los entornos disponibles.
- [ ] **H9.3 — Asistente / Miguel:** probar ventana/pantalla completa, pausa, Alt+Tab, ratón, minimapa, guardado/carga y escalado Windows 100/125/150 % cuando sea viable.
- [ ] **H9.4 — Asistente / Miguel:** medir rendimiento en el PC de Miguel, registrar resolución/Hz/configuración y corregir cuellos de botella demostrados.
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

## 6. Decisiones pendientes

| ID | Decisión | Propuesta inicial | Momento necesario |
|---|---|---|---|
| D1 | Estilo gráfico | 2D ilustrado fiel a siluetas y perspectiva | H6.2 |
| D2 | Edición/campaña principal | Cannon Fodder 1; demos primero | H7.1 y H8.1 |
| D3 | Campo de visión y panorámico | Conservar área lógica; adaptar presentación sin revelar más mapa | H4–H5 |
| D4 | Monitor y objetivo de refresco | 60 Hz primero; 120/144 si procede | H5.7 |
| D5 | Cobertura de pantallas auxiliares | Inventariar y acordar, sin olvidarlas al cerrar alcance | H8.2 |

Ninguna decisión artística es necesaria para resolver ahora la compilación Windows.

## 7. Riesgos y bloqueos conocidos

| ID | Riesgo o bloqueo | Tratamiento |
|---|---|---|
| R1 | Lectura fuera de límites en descompresión RNC | H2.1–H2.3; fallo reproducido, no cerrado |
| R2 | Dibujo con efectos sobre la lógica | H3.6 y H4; preservar visibilidad lógica y secuencia de actualizaciones |
| R3 | Interpolación con retraso y desajuste al apuntar | Medir y probar transformación de coordenadas en H5.5 |
| R4 | Diferencias entre plataformas o ejecuciones | Establecer determinismo antes de usar hashes como garantía |
| R5 | Arte inconsistente o incompleto | Muestra dentro del juego antes de producción masiva; matriz de recursos |
| R6 | Ampliar la vista cambia dificultad/comportamiento | Mantener área lógica original en la primera versión |
| R7 | Cobertura de pruebas de campaña completa | Datos CD32 recibidos y verificados; faltan replays de sus 72 fases |
| R8 | CI verde interpretada como validación total | Separar pruebas lógicas, memoria, gráficos, audio y prueba manual |

## 8. Registro de evidencias

| Evidencia | Resultado confirmado | No demuestra |
|---|---|---|
| Auditoría Linux inicial | 29 fases completadas antes/después del parche | Toda la campaña comercial, identidad por tick o Windows |
| Herramienta de auditoría | 8 pruebas superadas | Jugabilidad completa |
| Casos de borde de mapa | 8 casos sobre el cuerpo real con ASan/UBSan | Ausencia de fallos en otros componentes |
| ASan completo tras parche | 11 fases antes del fallo RNC | Suite de memoria aprobada |
| ASan, PC Format | 8 fases completadas | Todas las rutas Amiga; estas 8 ya forman parte de las 29 |
| Actions Windows, ejecución 39489706846 | Compilación aprobada; ZIP inspeccionado; PRUEBAS.json PASS, 29 fases, cero omisiones | Prueba visual/audio en el PC de Miguel o ausencia de fallos de memoria |
| H3 en Windows, ejecución 39593037606 | 11 fases, 11.361 muestras de estado iguales en dos pasadas por campaña; 29 replays anteriores PASS; comparador detecta divergencias en bajas y `mWasDrawn` | Cobertura de toda CD32 o independencia de renderizado |
| H3 en Linux, ejecución 39593037449 | 11 fases, 11.361 muestras; identidad byte a byte de run1/run2; comparación cruzada Windows/Linux exacta en estados tras normalizar saltos de línea | Ausencia de problemas de memoria o igualdad de estados no registrados |
| Huellas canónicas de H3 | `tools/modernization/reference-gameplay-v1.json`, 11 huellas SHA256 lógicas, asociadas a commits y datos | Validez indefinida para futuras versiones sin rebaselinar |
| Lector RNC acotado + 60 fixtures locales | ASan/UBSan PASS, 714 variantes inválidas rechazadas | ASan integral y CD32 |
| Lector RNC acotado Linux CI 39599528660 | 88 recursos RNC válidos; 1.047 variantes inválidas; ASan/UBSan PASS; H3 PASS | Ausencia de errores en todos los componentes |
| RNC + H3 Windows CI 39599528686 | 29 fases PASS, H3 PASS; mismo estado lógico anterior en 11.361 muestras | Campaña CD32 completa y ASan integral |
| Datos CD32 recibidos el 21 de octubre | CRC ZIP correcto; 266/266 archivos requeridos con MD5 coincidente; 72 pares MAP/SPT | Campaña completada jugando: intento local omitió 72 fases por falta de replays |
| Prueba manual de Miguel, 21 de octubre | Demo funcional; campaña Cannon Fodder reconocida tras añadir Amiga_CD y jugable; responde afirmativamente a todas las comprobaciones solicitadas | No acredita completar las 72 fases, sesiones largas ni ausencia de defectos de memoria |

Añadir evidencia futura con: tarea, commit, entorno, prueba, resultado y enlace al registro. No borrar resultados fallidos históricos cuando se corrija un problema.

**Seguimiento H2.3, alineación y aritmética definida (21-10-2026):** [H2_3_UBSAN_CLEAN_2026-10-21.md](H2_3_UBSAN_CLEAN_2026-10-21.md). Cambio en `readLE`, RNG y cálculos de cámara/sprites/mapa/vehículos. Las 29 fases disponibles pasan ASan/UBSan **sin avisos**, y las 11.361 muestras de H3 siguen idénticas en Linux/Windows. Nuevo control CI obligatorio de cero fallos de sanitizador, sin `continue-on-error`. Pendientes: LeakSanitizer, CD32 completo, H2.1 y H2.4.

**Seguimiento H2.3, índices de sprites y Huffman (21-10-2026):** [H2_3_INDICES_SPRITES_HUFFMAN_2026-10-21.md](H2_3_INDICES_SPRITES_HUFFMAN_2026-10-21.md). Linux: 29/29 fases con ASan, **0 errores fatales, 0 índices UBSan** (antes 6); 17 avisos UBSan adicionales pendientes. Windows: compilación, 29 replays y baseline H3 PASS. La primera tentativa con arrays físicos mayores rompió la decodificación y se revirtió; el resultado final preserva el mapeo de tablas heredado. Se incorpora un nuevo gate de CI para impedir que reaparezcan índices fuera de rango.

**Seguimiento H2.3, protección de fotogramas (21-10-2026):** [H2_3_PROTECCION_FOTOGRAMAS_2026-10-21.md](H2_3_PROTECCION_FOTOGRAMAS_2026-10-21.md). Nuevas longitudes de animación de origen: 15 tablas (1.309 entradas) y protección de tipo/fotograma. La compilación Linux, pruebas de límites, auditoría RNC y baseline H3 (11.361 estados) pasan; **la prueba completa ASan Linux termina 29/29 fases, sin fatal**, pero UBSan informa 23 condiciones indefinidas (6 índices, 15 desplazamientos y 2 accesos desalineados). Este resultado **no** cierra H2.3. Windows CI está en cola a la fecha de esta revisión.

**Seguimiento H2.3, corrección de direcciones (21-10-2026):** [H2_3_CORRECCION_DIRECCIONES_2026-10-21.md](H2_3_CORRECCION_DIRECCIONES_2026-10-21.md). La tabla 32×32 ya se consulta con un índice físicamente válido. 1.063.217 casos de aritmética de índices superan las pruebas aisladas; Linux (CTests y RNC) y Windows (compilación, CTests y 29 replays) conservan el baseline H3 de 11.361 estados. La suite ASan del motor completo vuelve a registrar **FAIL tras 11 fases**, ahora por una lectura en `Sprite_Draw_Frame` (`Source/Sprites/Sprite_Core.cpp:85`) de datos de animación Amiga. El primer error anterior de direcciones no vuelve a aparecer en este registro. `continue-on-error: true` en H2.3 hace que el workflow no falle; consultar siempre su `report.json`.

**Diagnóstico adicional H2.3 (21-10-2026):** [H2_3_DIAGNOSTICO_ASAN_2026-10-21.md](H2_3_DIAGNOSTICO_ASAN_2026-10-21.md). El workflow Linux aparece verde, pero la etapa ASan del motor completo está en `continue-on-error` y su propio informe registra `FAIL`. No aceptar H2.3 hasta corregir y repetir la suite.

## 9. Bitácora y siguiente sesión

| Fecha | Trabajo | Resultado / siguiente acción |
|---|---|---|
| 2026-10-20 | Auditoría inicial, parche de límites y pruebas Linux | Referencia preparada; RNC pendiente |
| 2026-10-20 | Conexión GitHub, rama y PR #1 | Automatización Windows iniciada |
| 2026-10-20 | Creación de este plan v1.0 | Tarea activa H1.1; consultar resultado Windows y actuar según el primer fallo o éxito |
| 2026-10-21 | H3.1–H3.5: emisor, comparador, 2 pasadas por campaña en Windows/Linux | 11.361 muestras idénticas por plataforma y entre plataformas; H3.6 auditada posteriormente; detalles en H3_VALIDACION_2026-10-21.md |
| 2026-10-21 | H3.6 cerrada; H2.2 lector acotado y pruebas | RNC validado Linux/Windows; H2.1/H2.3/H2.4 pendientes; ver H2_ESTABILIZACION_2026-10-21.md |
| 2026-10-21 | H2.3: índice seguro de tabla de direcciones, regresión y ASan/UBSan | Direcciones verificadas; siguiente fallo ASan en Sprite_Core.cpp:85. H2.3 sigue abierta; ver H2_3_CORRECCION_DIRECCIONES_2026-10-21.md |
| 2026-10-21 | H2.3: metadatos de tamaños de sprites + acceso acotado | Linux: 29 fases ASan sin fatal; UBSan 23 avisos pendientes. Windows CI pendiente en aquel corte; detalles H2_3_PROTECCION_FOTOGRAMAS_2026-10-21.md |
| 2026-10-21 | H2.3: índice plano de seguidores y tablas Huffman segmentadas, 1.077 tests de límites | Linux y Windows: 29 fases, H3 11.361 estados intactos, 6 avisos de índice eliminados; 17 UBSan no relacionados pendientes; informe H2_3_INDICES_SPRITES_HUFFMAN_2026-10-21.md |
| 2026-10-21 | H2.3: endian seguro, RNG idéntico y corrección de desplazamientos negativos | 29/29 fases, 0 ASan y 0 UBSan Linux, baseline H3 inalterado Linux y Windows; 262.144 RNG, 262.144 endian y 196.706 test de bits; compuerta CI estricta. H2.3 cobertura global pendiente. |
| 2026-10-21 | H2.3/H2.4: LSan/TSan y mutex de audio/transición | Linux 39641851896: 29/29 ASan/UBSan, 29/29 LSan y 29/29 TSan, cero avisos; Windows 39641852057 y H3 11.361 muestras PASS. Siguiente paso H2.5 y decisión H2.6. |
| 2026-10-21 | H2.5: inventario CMake, toolchains, SDL3/SDL3_mixer, Run/Scripts/tests y matriz de cobertura | Auditoría terminada; SDL3_mixer Linux sin revisión fija; 29 fases CI vs 11 trazadas; FFmpeg/XMP y audio real/CD32 fuera de equivalencia. H2.6 pasa a ser tarea activa. |

**Checklist para retomar (versión 1.8):**

1. Confirmar HEAD de PR #1 y los últimos resultados de Windows/Linux; el PR debe seguir en borrador.
2. **H2.5 COMPLETADO:** consultar [matriz técnica](H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md). La discrepancia y revisión flotante de SDL3_mixer en Linux son riesgo concreto a decidir/corregir en H2.6.
3. Endurecer ThreadSanitizer en CI al comprobar la batería 29/29; mantener las pruebas H3 como puerta obligatoria.
4. **H2.1:** documentar la limitación del caso mínimo RNC original, o delimitar explícitamente el riesgo residual del API heredada antes de aceptar H2.6.
5. **H2.6:** producir la ficha de aceptación de base clásica con evidencias, límites y una decisión expresa antes de iniciar H4.

**Primera acción del siguiente bloque:** H2.6, ficha de aceptación con las limitaciones H2.5 (especialmente congelación de SDL3_mixer Linux) y decisión sobre RNC H2.1. H4 no está iniciado. No subir recursos CD32 privados a GitHub.

### Actualización del 21 de octubre de 2026

- H1.1–H1.3 completados. Artefacto: https://github.com/Cacheirez/openfodder/actions/runs/39489706846/artifacts/12294654792 . SHA256: `caf4eeaedd1ae857295230a099ecdcb78d99b4749a7a6ceca1a76d6896f22207`.
- VERSION.txt del paquete: `4e7afb99abeda79de044fbf196b667711c4a4687`, revisión de integración usada por Actions para el PR; la rama de origen usa `1c0b42368c5ae44fb462933bde3db520560e231c`.
- Inspeccionados ejecutable, SDL3.dll, SDL3_mixer.dll, scripts, campañas, siete directorios demo, licencias, lanzador e informe. Sin datos comerciales ni partidas en el ZIP.
- Datos comerciales CD32 incorporados solamente al entorno local privado de pruebas. H8.1 tiene los datos disponibles; la cobertura completa sigue pendiente.
- Prueba de Miguel completada: confirma demo funcional y campaña CD32 reconocida y jugable, con todas las comprobaciones solicitadas satisfactorias. No comunica errores. H1.4–H1.6 cerrados por este reporte; no se exige una captura adicional.
- Se conserva el paquete indicado como referencia de la prueba por continuidad de las instrucciones; Miguel no ha enviado una lectura independiente de VERSION.txt. Duración y demo exacta no detalladas.
- H2.1 pasa a ser la tarea activa. El fallo RNC sigue pendiente aunque no se haya manifestado en esta prueba manual.


## Revisión vigente — 22 de octubre de 2026

Esta sección sustituye operativamente los pendientes históricos de dependencia flotante/TSan no bloqueante del texto anterior; se conserva el historial.

- Rama al retomar: `df99c678`; PR #1 abierto, borrador, sin fusionar.
- **H2.6 avanzado, todavía abierto:** [ficha de aceptación](H2_6_ACEPTACION_BASE_CLASICA.md).
- Cambio CI `5c564b1943e30a2504452e8ad51832a687b8988a`: SDL3_mixer Linux fijado a la revisión Windows, SHA efectivos archivados, TSan obligatorio y Ubuntu 24.04 explícito. Sin cambios del motor ni de H3.
- Nuevas ejecuciones [Linux 39735380183](https://github.com/Cacheirez/openfodder/actions/runs/39735380183) y [Windows 39735380194](https://github.com/Cacheirez/openfodder/actions/runs/39735380194): **en curso al registrar esta actualización**, no aprobadas todavía.
- Local: 13 tests Python PASS; YAML válido y diff limpio.
- ZIP privado CD32: CRC correcto, 276 archivos, 72 pares MAP/SPT; lector RNC real probado con ASan/UBSan: **41 recursos válidos y 488 variantes inválidas rechazadas**, retorno 0, sin avisos. No es una ejecución del motor completo ni de las 72 fases. Recursos originales intactos y fuera de GitHub.
- Se conserva la prueba manual satisfactoria que Miguel denomina «H6», incluida CD32. Versión exacta no atribuida; H6 artístico formal continúa pendiente.
- H2.1 sigue como atribución histórica no resuelta; la carga actual llama al lector acotado. Audio físico, interacción y campaña CD32 completa siguen fuera de la cobertura automatizada.
- **Siguiente acción:** revisar resultados e informes de estas ejecuciones, resolver fallos si aparecen y decidir H2.6 antes de iniciar H4. No se solicita repetir ahora la prueba manual.

## Cierre H2.6 e inicio H4.1 — 22 de octubre de 2026

Esta decisión sustituye operativamente el estado «pendiente de CI» de la revisión previa, conservada como historial.

- H2.6 aceptado para iniciar la separación de presentación, con exclusiones expresas en su ficha: H2.1 histórico, cobertura CD32 de 72 fases incompleta, interacción/audio real y backends distintos.
- Miguel confirma expresamente el motor probado con sus archivos originales CD32 y valida H2.6; no se le solicita repetirlo.
- Windows 39735380194 y Linux 39735380183 aprobados para `5c564b19`. Informes internos comprobados; H3 de 11.361 estados preservado.
- Base recuperable: `baseline/classic-h2.6-2026-10-22`, commit `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`; solo documentación adicional respecto al commit probado. No se moverá esa rama para incorporar H4.
- H4.1 iniciado: además de visibilidad, se identifican retirada de entidades, cambios de arma y temporizador comercial en HUD, consumo de cursor, registros de recorte y callbacks con estado. El código del motor no se ha cambiado en este bloque.
- Próximo cambio: separar retirada/preparación de sprites manteniendo los puntos de llamada originales; después verificar H3 sin modificar referencias. No adelantar 60 FPS ni H4.2–H4.6 como terminados.
- PR #1 se mantiene abierto en borrador, sin fusionar.

## Implementación H4.1 — 22 de octubre de 2026

- Código `4e4d57efc408d4a4f404b5f4f2ed7844fde261c3`: extracción de retirada diferida, visibilidad, selección de arma, temporizador comercial y solicitud del cursor. Se conservan los puntos, guardas y orden de llamada.
- Linux local: 6 CTests, 13 tests Python, H3 de 11 fases/11.361 estados y 29 replays sin omisiones, todos PASS. No se cambia el baseline.
- Temporizador comercial: 184.320 transiciones equivalentes al cuerpo original H2.6, con UBSan y registro de llamadas gráficas; se añade esta prueba a CI Linux. No sustituye la campaña comercial completa.
- [Linux 39772995975](https://github.com/Cacheirez/openfodder/actions/runs/39772995975) y [Windows 39772996056](https://github.com/Cacheirez/openfodder/actions/runs/39772996056): ambos completados con éxito; resultados finales abajo.
- La base clásica recuperable continúa en `5e6a4f38`; PR #1 sigue sin fusionar.
- Próximo bloque técnico tras comprobar CI: encapsular registros de recorte/dibujo y revisar efectos restantes antes de publicar estados inmutables. Las coordinadoras clásicas siguen teniendo estado; todavía no deben invocarse para dibujar 0/1/N veces por tick.

### Resultado final del bloque H4.1

Código `4e4d57ef`: primera extracción aceptada. Windows 39772996056 y Linux 39772995975 completos y satisfactorios. H3: 11.361 estados del baseline original; replays: 29/29, cero omisiones; Linux ASan/UBSan, LSan y TSan: 29/29 cada uno, sin hallazgos en los logs examinados. Prueba comercial aislada: 184.320 transiciones equivalentes. ZIP e informes internos verificados; huellas y límites en H4_1_EFECTOS_DIBUJO.md.

H4.1 permanece en curso por los registros de dibujo/efectos restantes. Siguiente cambio: encapsular preparación/recorte en datos propios para avanzar hacia estados inmutables, manteniendo coordinadoras clásicas y H3 original. No aumentar todavía la frecuencia de llamadas a las funciones clásicas. Base `baseline/classic-h2.6-2026-10-22` intacta; PR en borrador, sin fusionar.

## Preparación y recorte sin modificar el motor — 22 de octubre de 2026

Código `73de45aa12542c33e72a79fcbf2e10c0a5526d37`: entradas y resultados propios en SpriteDrawState.hpp, cálculos puros y adaptación a los registros clásicos en el mismo punto de ejecución. 306.432 casos PC/Amiga equivalentes al código anterior, 6 CTests y 13 tests Python aprobados localmente. H3 original: 11.361 estados conservados; 29 replays aprobados sin omisiones. CI Windows 39817991168 y Linux 39817991165 aprobadas: H3 original intacto en ambas plataformas, 29/29 replays Windows y 29/29 en cada sanitizador Linux, sin diagnósticos observados. ZIP e informes internos comprobados. Detalles y límites en [H4_1_EFECTOS_DIBUJO.md, sección 7](H4_1_EFECTOS_DIBUJO.md#7-preparación-y-recorte-por-valor--22-10-2026).

Siguiente trabajo: adaptar el rasterizador para consumir estos datos explícitamente. El adaptador clásico todavía escribe en el motor y los recursos son prestados; no se declara seguro dibujar el frame completo 0/1/N veces ni publicar snapshots entre hilos. H4.1 sigue abierta, PR sin fusionar y baseline clásica intacta.

## Rasterizador con entradas explícitas — 22 de octubre de 2026

Código `691cb0dedd657cd99cab165cbce7ff26fa2bd537`: núcleo RasterizeSprite8 PC/Amiga que escribe únicamente píxeles en el destino. La ruta de sprites transmite directamente la preparación; los adaptadores conservan las tres escrituras clásicas previas al dibujo. Prueba focalizada: 29.160 casos de igualdad de píxeles/registros, transparencia, paletas y repetición; ejecutada bajo ASan/UBSan e incorporada a CI Linux. H3 local original intacto (11.361 estados), 29/29 replays sin omisiones, 6 CTests y 13 tests Python aprobados.

CI Windows 39820699876 y Linux 39820699877 aprobadas. H3 original intacto en ambas plataformas; 29/29 replays Windows y 29/29 en cada sanitizador Linux, cero omisiones y sin diagnósticos observados. Prueba de 29.160 casos de píxeles/registros aprobada en CI. ZIP e informes internos verificados. Detalles en [H4_1_EFECTOS_DIBUJO.md](H4_1_EFECTOS_DIBUJO.md), sección 8. H4.1 sigue abierta: quedan otras rutas de dibujo, vida útil de recursos y pruebas 0/1/N del frame completo. El siguiente bloque es inventariar esas rutas/recursos antes de construir el estado de presentación. No modificar la frecuencia de llamada de los adaptadores clásicos. PR sin fusionar y baseline clásica conservada.

## Auditoría de rutas y recursos — 22 de octubre de 2026

Revisión de `a5a5cc42` completada: [H4_1_RUTAS_Y_RECURSOS.md](H4_1_RUTAS_Y_RECURSOS.md). Inventario de terreno, GUI/HUD, cursor, rasterizadores restantes, escenas, superficies/paletas y callbacks; propietarios, mutaciones y fronteras de cambio de fase/versión identificados. No se modifica el motor ni se construye todavía el estado completo.

Hallazgo prioritario: GetSpriteData Amiga cambia paleta y cabecera. La preparación encapsulada altera el orden de paleta respecto a a2f63090 para segmentos donde el accessor la sustituye; no hay reproducción visual de misión y las pruebas anteriores no cubren esa resolución. Debe comprobarse/corregirse el contrato antes de extenderlo. Mantener shared_ptr no garantiza inmutabilidad de los bytes.

Siguiente bloque: resolvedor explícito que reúna recurso propietario, offset/extensión, layout y paleta efectiva, preservando efectos y orden clásicos; prueba de resolución y retención de recursos antes de avanzar a comandos de terreno/HUD y al frame completo. H4.1 sigue abierta. Última CI del motor sigue siendo 691cb0de; esta auditoría documental no ejecuta H3 de nuevo ni amplía su cobertura. PR en borrador sin fusionar y baseline H2.6 intacta.

## Resolución conjunta con propiedad estable — 23 de octubre de 2026

Código `ff82fb6049def3d784bc09a3a3c2d7fc685f4ea5`: propietario privado e inmutable, offset/extensión, layout y paleta efectiva reunidos; orden clásico de paleta Amiga restaurado. 10.944 casos comparados con preparación/accessors originales, más pruebas de mutación, recarga, destrucción y liberación del último propietario. [Implementación, evidencia y límites](H4_1_RECURSOS_ESTABLES.md).

CI Windows 39866081138 y Linux 39866081648 aprobadas: H3 original 11.361 estados en ambas plataformas; Windows 29/29 replays; Linux ASan/UBSan, LSan y TSan 29/29, sin diagnósticos. ZIP e informes verificados. El primer intento agotó el límite de TSan; la corrección valida los bytes una vez por segmento y pasada de dibujo, preservando los efectos de cada llamada. TSan final: 104,453 s con el límite original de 600 s. La prueba focalizada con fugas pasa en CI; el entorno local impidió ejecutar LSan. H4.1 sigue abierta: falta terreno/HUD y demás rutas del frame. No aumentar todavía la frecuencia ni publicar el motor entre hilos. PR en borrador sin fusionar, base H2.6 intacta.


## Terreno visible con atlas estables — 23 de octubre de 2026

Código `7eeb6f777cc2ddfd9c615a2a94eef69bd3625c41`: `TerrainDraw` retiene tiles/geometría por valor y copias privadas de atlas PC/Amiga. `MapTiles_Draw` conserva limpieza y guardado en su punto clásico; rasterización repetible sin consultar el motor. 7.680 comparaciones contra los cuerpos originales cubren recortes, ambos bancos PC, planos Amiga, bordes y efectos. Pruebas de retención, mutación, destrucción y liberación aprobadas.

Local: Release, 6/6 CTests, H3 11.361 estados originales y 29/29 replays. CI Windows 39919649274 y Linux 39919649308 aprobadas: H3 original 11.361 estados en ambas; Windows 29/29 replays; Linux ASan/UBSan, LSan y TSan 29/29, cero omisiones y sin diagnósticos. ZIP e informes internos verificados. Detalles: [H4_1_TERRENO_ESTABLE.md](H4_1_TERRENO_ESTABLE.md). H4.1 sigue abierta; el siguiente bloque es HUD/cursor, manteniendo las coordinadoras clásicas y sin construir todavía el frame completo. PR en borrador, sin fusionar; base H2.6 recuperable.


## Continuidad documental — 23 de octubre de 2026

Añadidos índice/guía de relevo, matriz de diferencias PC/Amiga comprobadas y campos pendientes de análisis, instrucciones de reproducción/recuperación y custodia de datos privados. Documentos iniciales marcados como históricos. Informes JSON de la CI de `7eeb6f7` conservados en Git; los ZIP completos siguen sujetos a caducidad y requieren archivo duradero externo. La guía identifica esta obligación pendiente y no afirma que esté completada. No cambia el motor; no se repiten pruebas ni se amplía su cobertura.


## HUD lateral y cursor retenidos — 23 de octubre de 2026

Código `c6af094c49641018b6dea6dc77cbe731a7ea0218`: captura del sidebar compuesto y cursor con bytes privados, geometría y paleta/layout efectivos. Decisiones, composición, consumo de solicitud y registros siguen en sus puntos clásicos. Se documentan las diferencias startY/destino PC-Amiga y paleta/offset del cursor en [H4_1_HUD_CURSOR_ESTABLES.md](H4_1_HUD_CURSOR_ESTABLES.md). Local: 2.304 casos de cursor, 288 de HUD, 6 CTests, H3 original 11.361 estados y 29 replays. CI Windows 39956418210 y Linux 39956418211 aprobadas: H3 original en ambas, Windows 29/29 replays y Linux ASan/UBSan, LSan y TSan 29/29, sin diagnósticos en los registros examinados. ZIP e informes verificados y resultados compactos conservados en Git. H4.1 sigue abierta; el siguiente bloque es RGB/fades y propiedad de destinos, antes del frame completo. PR sin fusionar y base H2.6 intacta.


## Paleta efectiva y salida RGB propia — 23 de octubre de 2026

Código `ff15219680b289abf207fdc23fc436a9f390e649`: [contrato y límites](H4_1_PALETA_DESTINOS.md). Captura de índices privados y tabla SDL efectiva; conversión a vector de destino propio. Fades y Save/Restore conservan cuerpos y llamadores originales. Tabla efectiva inicializada a negro antes de su primera aplicación para evitar copiar entradas indeterminadas. No se declara propiedad de todas las composiciones ni frame completo. Local: 27.648 casos, 6 CTests, H3 original 11.361 estados y 29/29 replays aprobados. CI Windows 39995798688 y Linux 39995798623 aprobadas; H3 original en ambas, Windows 29/29 replays y Linux ASan/UBSan, LSan y TSan 29/29. Informes compactos conservados en Git.


## Capas y destinos indexados — 23 de octubre de 2026

Código `793e347cd9f118da1c9ec6a84f88caf3257b74c2`: capturas privadas, destinos independientes y operaciones de copia/mezcla indexada/RGB. Conserva los tres contratos y el orden en pausa/reclutamiento, sin mover fades, Save/Restore, callbacks ni bloqueos. Auditoría del minimapa documenta que se omite en unit testing. [Informe y límites](H4_1_CAPAS_DESTINOS_INDEXADOS.md). Local: 2.944 casos nuevos, 27.648 de superficie, 6 CTests, H3 original y 29 replays aprobados. CI Windows 40003012479 y Linux 40003012470 aprobadas: H3 original en ambas, Windows 29/29 replays y Linux ASan/UBSan, LSan y TSan 29/29. Evidencia compacta conservada en Git y ZIP verificados.


## Productores GUI/minimapa/escenas — 24 de octubre de 2026

`d35e2675ffbbc79f8bf21eb961d78c06d74abd14`: operaciones de píxel propias para GUI8, PC16, Amiga16/Alt/Offset, tiles/constructor de minimapa, capas de helicóptero PC, Service Amiga y carga de imágenes PC. Se conservan coordinadoras/accessors/registros; preprocesado de reclutas sigue siendo un efecto de producción de recursos, no se repite al presentar. Detectada por ASan lectura original data[-1] en seam PC 320: normalizado a cero y probado contra esa referencia válida, sin atribuir equivalencia a UB. [Informe detallado](H4_1_PRODUCTORES_GUI_ESCENAS.md). Local: 1.536 + 1.964 + 1.024 + 72 casos nuevos, suites previas, 6 CTests, H3 original y 29 replays aprobados. CI Windows/Linux aprobada; H3 original intacto en ambas plataformas y 29/29 replays con los sanitizadores Linux.


## 24-10-2026 — Primera escena de presentación: pausa

`a133afb`: fondo y texto con geometría, índices/paletas y backing RGB propios; rasterización sin acceso al motor. Se conserva el orden de fade, eventos y reanudación. 144 escenarios 0/1/5 comparan bucle original/actual con cambio de dimensiones y destrucción de recursos. [Informe, costes y límites](H4_1_ESTADO_PAUSA.md). Local H3 original y 29 replays PASS; CI Windows/Linux aprobada; H3 original y 29/29 replays preservados, sanitizadores Linux sin diagnósticos. No es el cierre global H4.1.

## 24-10-2026 — Frame compuesto de misión y regresión de transición

[Informe](H4_1_FRAME_MISION.md): captura en el punto de conversión final para incluir escrituras del paso principal y paleta efectiva. 240 escenarios 0/1/5, 672 capturas retenidas; se encontró y extrajo el efecto de backing persistente de pausa que alteraba el padding al omitir la presentación. La suite de pausa conserva sus 144 escenarios y añade comparación de capturas contra el original. Coordinadoras reales con productores/SDL controlados; no es un cierre global H4. No se cambia cadencia, referencias H3 ni base clásica. Resultados completos en el informe.

Cierre del incremento `049439d`: CI Windows/Linux aprobada, ZIP/informes verificados; H3 original 11.361 estados, 29 replays y sanitizadores sin diagnósticos. PR en borrador sin fusionar. La tarea siguiente es separación por capas, pruebas del motor completo 0/1/N, otras escenas y publicación/geometría; H4 global sigue abierto.

## Seguimiento — destinos de presentación

[Identidad y geometría del destino](H4_1_DESTINOS_PRESENTACION.md): publicación rechaza superficies sustituidas, identidades distintas, tamaños/strides/extensiones incompatibles y formatos fuera del contrato de palabras RGB. Capturas antiguas siguen rasterizándose; un destino nuevo de igual tamaño no hereda su identidad. Se conserva cadencia y producción clásica. Consultar el informe para pruebas y estado de CI; separación de capas y publicación asíncrona siguen pendientes.
