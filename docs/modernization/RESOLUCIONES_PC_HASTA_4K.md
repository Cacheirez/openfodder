# Presentación PC multirresolución — 4:3 y 16:9 hasta 4K

27-10-2026. Requisito solicitado por Miguel. Documento de alcance y aceptación: **pendiente de implementación y validación**. No modifica el motor ni acredita soporte actual. Se conservan modo clásico, base aceptada, mejoras anteriores, referencias H3 y PR sin fusionar.

## Objetivo y límites

Soportar ventanas redimensionables y pantalla completa en resoluciones habituales de PC, con soporte explícito de 4:3 y 16:9 hasta **3840×2160 (4K UHD)**. Separar tamaño lógico del mundo, resolución interna de composición, densidad de los recursos y píxeles físicos de salida. El límite de esta entrega es 3840 de ancho y 2160 de alto; no incluye DCI 4096×2160 ni 5K/8K.

La lista siguiente es una matriz mínima de aceptación, no una lista cerrada de tamaños permitidos ni una clasificación estadística de popularidad. Enumerar los modos reales de cada monitor, admitir tamaños intermedios de ventana y conservar las frecuencias disponibles sin inventar modos que la pantalla no admite. En ventana se probarán los tamaños que quepan en el escritorio; los restantes se verifican mediante destinos de render automatizados. Un test de render no acredita un monitor físico.

| Formato | Resoluciones de la matriz mínima |
|---|---|
| 4:3 — compatibilidad | 640×480, 800×600, 1024×768, 1152×864, 1280×960, 1400×1050, 1600×1200 |
| 4:3 — alta resolución | 1920×1440, 2048×1536, 2560×1920, 2880×2160 |
| 16:9 | 1280×720, 1600×900, 1920×1080, 2560×1440, 3200×1800, 3840×2160 |
| Aproximación habitual a 16:9 | 1366×768; tratar su relación exacta, sin asumir divisibilidad por 16/9 |

2880×2160 es el cuadro 4:3 que cabe en una salida de 2160 líneas; **no se denomina 4K UHD**. En un monitor UHD se podrá presentar el encuadre 4:3 centrado sin deformarlo. El render también debe admitir tamaños de ventana no listados dentro del intervalo, incluidas dimensiones impares. Mínimo previsto: 640×480; bajo ese mínimo, limitar tamaño o aplicar un modo de compatibilidad explícito y probado, sin dejar controles inaccesibles.

Otros formatos detectados (por ejemplo 5:4, 16:10 o ultrapanorámico) conservarán una presentación proporcionada mediante el encuadre compatible; la adaptación nativa específica de esos formatos no forma parte de la aceptación de este incremento.

## Encuadre: resolución no equivale a mostrar más mapa

1. **Encuadre clásico compatible:** disponible en todas las resoluciones. Conserva el campo visible y la geometría lógica; centra la imagen en el área disponible con bandas si hacen falta. No recorta ni estira el juego para llenar la pantalla. Es la referencia de regresión y el retorno ante un modo moderno no soportado.
2. **Presentación moderna 4:3 y 16:9:** objetivo del plan, con composición e interfaz adaptadas al formato. La adaptación 16:9 no se considerará completa si solo se amplía el framebuffer clásico. Preparar viewport panorámico nativo, manteniendo disponible el encuadre clásico. Antes de habilitar la ampliación lateral del mundo, aislar la visibilidad de presentación de la lógica heredada (`mWasDrawn`, activación, IA y efectos), contrastar H3 y validar bordes/cámara/selección. La visión adicional puede cambiar la información táctica del jugador: identificar ese comportamiento como modo panorámico y revisarlo con Miguel, sin atribuirle equivalencia perceptiva con el clásico.
3. **No modificar simulación para llenar pantalla:** ninguna resolución cambia velocidades, alcance, colisiones, timers o RNG. No sustituir las dimensiones lógicas usadas por gameplay por las del monitor. La ampliación de viewport es un trabajo de presentación con puertas propias, no una autorización para cambiar reglas.
4. **Corrección de aspecto explícita:** revisar relación de píxel/presentación por backend PC/Amiga y por escena. Una matriz heredada, como 320×200, no debe confundirse automáticamente con su proporción visual objetivo. Mantener la opción clásica aceptada y documentar la transformación antes de aplicar la escala de salida.

## Arquitectura y recursos gráficos

- Dibujar terreno, sprites, sombras y efectos en un destino moderno con resolución suficiente, antes de la reducción final. No reducir el arte nuevo al framebuffer clásico y después ampliarlo a 4K como solución HD.
- Mantener coordenadas, pivotes, cajas y tiempos en unidades lógicas. Definir una transformación explícita mundo → cámara → viewport → píxeles de salida, con su inversa para el ratón.
- Conservar fuentes maestras de alta resolución del estilo C. Establecer densidad uniforme y coherente por familia de recursos, sin redibujar cada sprite para 720p/1080p/1440p/4K.
- Evaluar 2×/4× y densidades mayores si 4K las necesita. 4× no es un techo ni una decisión cerrada. Elegir después de observar el tamaño real del sprite y del terreno en el viewport de destino.
- Generar variantes de resolución, filtrado y mipmaps cuando mejoren reducción, memoria o estabilidad. Evitar halos de alpha, costuras y contaminación entre regiones del atlas mediante márgenes y tratamiento de transparencias verificados.
- Terreno compuesto por tiles/atlas con equivalencia de tamaños lógicos y uniones estables; no crear un fondo completo por resolución de monitor. Escenas ilustradas estáticas tendrán reglas propias de ajuste, bandas y zonas seguras, sin recortar información.
- Interfaz y texto con escala independiente del mundo: HUD, menús, reclutas, briefing, pausa, minimapa y cursor legibles desde 640×480 hasta UHD. No ampliar ciegamente toda la interfaz con el mismo factor que el mapa.
- Gestionar presupuesto de memoria/texturas, tamaño máximo de textura del dispositivo, recreación de destinos y liberación tras cambios. Si no es viable una calidad, ofrecer calidad inferior explícita conservando la resolución de salida y la geometría; registrar el fallback y no presentarlo como calidad nativa equivalente.

## Opciones y cambios en ejecución

Selector de monitor, resolución y modo ventana/pantalla completa sin bordes; pantalla completa exclusiva solo con modos admitidos y verificados. Preferencia nativa del escritorio como arranque moderno, con un ajuste compatible seguro si no se puede crear el destino. No cambiar la frecuencia del monitor salvo elección explícita.

Aplicar cambios con confirmación temporizada (15 segundos) y retorno a la configuración anterior si no se confirma, falla el modo o se pierde la pantalla. Persistir opciones únicamente tras éxito; arranque recuperable si el monitor guardado ya no existe.

Responder a redimensionado, maximización, Alt+Tab, minimización, cambio de monitor y cambio de DPI. Distinguir tamaño de ventana en coordenadas de ventana y tamaño real en píxeles. Probar escalado de Windows 100/125/150/175/200/300 %. Recalcular viewport, cursor y ratón sin desplazamientos, saltos de anclaje ni reutilización de destinos obsoletos.

## Tareas y orden

| ID del plan | Entrega pendiente |
|---|---|
| H4.2–H4.5 | Contrato de geometría/destinos que soporte cambio de resolución y RGB moderno, conservando capturas coherentes y el oráculo clásico |
| H5.5 | Transformaciones e inversa de entrada; coordenadas en bandas, HUD y viewport; no emitir órdenes de mundo desde bandas |
| H5.6 | Opciones de monitor, modo, resolución, escala de interfaz y calidad, persistencia y recuperación |
| H5.9 | Presentación multirresolución 4:3/16:9 hasta UHD, con matriz de modos y ventana redimensionable |
| H5.10 | Viewport panorámico e interfaz nativos; independencia de visibilidad lógica y revisión explícita del encuadre |
| H6.3–H6.6 | Densidades de arte, atlas, alpha, filtros, márgenes, fuentes y pruebas visuales 720p/1080p/1440p/4K |
| H7.9 | Primera misión moderna completa validada en ambos formatos y extremos de la matriz |
| H9.3–H9.5 | Matriz automatizada, pruebas Windows/GPU/DPI/monitores, coste y recuperación |

Secuencia: definir transformaciones y política de encuadre → soporte de destinos/opciones → prueba de una pose y fragmento de terreno a varias densidades → compositor HD y viewport nativo → atlas/producción por lotes. Confirmar por separado la CI pendiente del piloto C01; su recurso 16×14 no cierra este requisito.

Avance 2.47: transformaciones, misión en ventana, bandas/cursor y mapa general implementados; CI y aceptación física de esas rutas registradas en el plan. Prueba manual comunicada en UHD/300 %. Pausa ajustada implementada con CI propia pendiente. Opciones, otras escenas, entrada relativa y soporte global siguen pendientes; no se considera implementado todo este documento.

## Criterios de aceptación

- Todos los tamaños enumerados y varios intermedios/impares producen frames válidos, sin estiramientos accidentales, cortes de HUD, costuras, accesos fuera de límites ni anclajes que cambien con la resolución.
- Replays deterministas conservan H3 original con entradas canónicas de mundo equivalentes. Se prueban además las transformaciones de entradas físicas: no reutilizar sin adaptación una grabación de coordenadas de pantalla entre resoluciones distintas.
- Cambiar de modo, DPI o monitor no conserva escenas/destinos obsoletos ni consume simulación extra. Pausa/reanudación, minimapa, selección y disparo funcionan en las posiciones mostradas.
- Probar por render automatizado toda la matriz; registrar por separado qué combinaciones han sido observadas en Windows/GPU reales. No marcar todas como manualmente aprobadas por emular un destino 4K.
- Objetivo inicial de fluidez: 60 Hz hasta UHD en el equipo de referencia, sujeto a medición de CPU/GPU, memoria y percentiles p95/p99. 120/144 Hz se evalúan donde el monitor lo permita, sin cambiar el ritmo lógico. No prometer FPS por aprobar replays acelerados.
- El modo clásico y todas las mejoras anteriores siguen disponibles. Sin regenerar referencias, mover la base clásica ni fusionar el PR.

## Referencias técnicas de implementación

Documentación oficial consultada el 27-10-2026; verificar contra SDL fijado por el proyecto al implementar, sin actualizar dependencias por iniciativa propia:

- [Tamaño real en píxeles](https://wiki.libsdl.org/SDL3/SDL_GetWindowSizeInPixels).
- [Tamaño de ventana y diferencias con alta densidad](https://wiki.libsdl.org/SDL3/SDL_GetWindowSize).
- [Modo de pantalla completa y eventos de cambio](https://wiki.libsdl.org/SDL3/SDL_SetWindowFullscreenMode).
- [Enumeración de modos en SDL3](https://wiki.libsdl.org/SDL3/README-migration).
