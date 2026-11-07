# Alcance completo H0–H10

Requisitos del proyecto conservados al limpiar la documentación el 02-11-2026. El orden y la tarea activa están únicamente en [PLAN_TRABAJO.md](PLAN_TRABAJO.md). Los avances fechados de esta lista son antecedentes técnicos, no instrucciones de siguiente paso. H7.3 exige ahora la sustitución completa definida en [SOLDADOS_COBERTURA_COMPLETA.md](SOLDADOS_COBERTURA_COMPLETA.md); el lote f72d6e7 no cumple ese cierre.

## H0. Auditoría y preparación — completado

- [x] **H0.1 — Asistente:** inspeccionar temporización, cámara, superficies, sprites, entrada y pruebas existentes.
- [x] **H0.2 — Asistente:** fijar las revisiones auditadas de motor, datos, scripts y grabaciones.
- [x] **H0.3 — Asistente:** compilar la referencia Linux y ejecutar las 29 fases demo disponibles.
- [x] **H0.4 — Asistente:** preparar el control de replays y comprobar sus ocho casos de prueba.
- [x] **H0.5 — Asistente:** reproducir el fallo de lectura de pistas del mapa y preparar un parche con ocho casos de borde.
- [x] **H0.6 — Asistente:** comprobar que las 29 fases completan tras ese parche; registrar el segundo fallo ASan en descompresión Amiga.
- [x] **H0.7 — Miguel / asistente:** conectar GitHub, verificar el repositorio y crear la rama y el PR #1.
- [x] **H0.8 — Asistente:** preparar el workflow Windows, la comparación de resultados y el empaquetado de las siete demos.

**Evidencia:** PR #1 e informe inicial conservado en el historial Git anterior a la limpieza (df933bf). No usar el paquete inicial como referencia vigente. La cobertura es de demos; no equivale a toda la campaña comercial.

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

- [ ] **H6.1 — Asistente:** conservar las muestras comparables del mismo soldado y fragmento de escenario, claramente identificadas como conceptos. **Parcial:** [tres direcciones A01/B01/C01 presentadas](H6_1_COMPARATIVA_ABC.md), con pose/escenario similares. Detalle, posición e integración de C01 aceptados en el HTML; falta comprobar el nuevo lote animado y su escena. Las láminas no son recursos integrados; C sí está aprobada como dirección y tiene una pose experimental aparte.
- [x] **H6.2 — Miguel:** dirección elegida: **C — Pintado moderado**, por su toque Nintendo. A descartado; B no elegido. La aprobación del estilo no equivale a aceptar el recurso integrado.
- [ ] **H6.3 — Asistente:** definir resolución de recursos, paleta, proporciones, contornos, sombras y nivel de detalle. Evaluar 2×/4× y densidades mayores cuando lo requiera UHD, sin multiplicar el tamaño lógico. Conservar maestros HD y derivar variantes automáticamente; fijar densidad tras probar 720p/1080p/1440p/4K con terreno y sprites juntos.
- [ ] **H6.4 — Asistente:** definir el manifiesto de atlas: ID, región, escala, anclaje de pies, dirección y fotograma. Atlas significa una imagen que agrupa varios sprites. Añadir densidad, variantes, márgenes para filtrado y límites de textura; no crear un atlas manual por resolución de monitor.
- [ ] **H6.5 — Asistente:** preparar carga, validación y sustitución individual de recursos, con retorno automático al original cuando falte uno nuevo. **Parcial:** pose C01 incorporada en compilación, sustitución acotada y fallback comprobados; cargador/atlas HD generales pendientes.
- [ ] **H6.6 — Asistente:** validar transparencias, márgenes, unión de tiles, pivotes, ciclos de animación y consistencia entre direcciones.
- [ ] **H6.7 — Asistente:** registrar procedencia y condiciones de uso de cada recurso; separar recursos propios de los originales. **Hecho para el piloto:** manifiestos, prompts, hashes y PNG originales C01 y A/B/C en assets/modernization; mantenerlo para futuros recursos.

**Aceptación:** muestra aprobada y recursos reproducibles que el motor pueda cargar correctamente. No producir cientos de imágenes antes de comprobar cómo funcionan juntas dentro del juego.

## H7. Primera misión moderna completa

**Fase de regresión pública:** Amiga The One m1p2. El soldado completo requiere casos adicionales para direcciones, estados, enemigos y oclusiones; esta fase sola no acredita H7.3.

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

