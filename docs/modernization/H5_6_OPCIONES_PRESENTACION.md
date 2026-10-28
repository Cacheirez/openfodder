# H5.6 — opciones de presentación y confirmación

Incremento 2.49, 28-10-2026. Pausa de 63c4d6f aceptada por Miguel: «funciona la pausa perfectamente». Windows y Linux de ese paquete PASS. La CI de este incremento es nueva y sigue pendiente al publicar.

## Comportamiento implementado

El menú existente ofrece Presentation: CLASSIC / FIT. Es presentación, independiente del arte C01. Clásico sigue siendo el valor predeterminado. FIT ajusta misión, pausa, mapa general y ahora briefing/reclutamiento, con aspecto original y bandas. Requiere ventana y ratón alternativo desbloqueado; el menú lo indica. F11 mantiene el camino clásico.

Los cambios del menú se editan en una copia. SAVE prueba cambios de presentación o modo de ratón y pide KEEP/REVERT durante 15 segundos de reloj monotónico; Escape o expiración restauran. El candidato no se escribe antes de KEEP. Se rechaza confirmar si la ventana ha cambiado mientras se probaba (por ejemplo, F11 o resize). DEFAULTS también queda pendiente de SAVE. Cambiar plataforma se aplica al cerrar tras guardar, evitando modificar gráficos a mitad de una prueba de ventana.

La transacción captura estado real de ventana (modo, tamaño, posición, maximización, resizable, escalas internas y ratón relativo), comprueba respuestas SDL y el estado resultante después de sincronizar. Invalida las coordenadas publicadas al aplicar/restaurar. Ante un fallo restaura; si también falla la restauración, muestra RESTORE FAILED, conserva el snapshot para reintentar e impide guardar. Los métodos históricos de F11 no se sustituyen.

INI: `presentation=classic|fit` en `[openfodder]`, ausente/desconocido → clásico. Se preservan secciones desconocidas. Guardado a `openfodder.ini.pending` y reemplazo mediante SDL_RenamePath, comprobando errores de escritura; un fallo no trunca el último archivo confirmado. No es una garantía ante corte de alimentación. Flags SCREEN_TRANSFORM/FIT existentes siguen siendo overrides explícitos (incluido 0); no se modifican desde el menú. PROBAR_OPCIONES_H5.cmd limpia esos dos overrides y respeta las preferencias del INI sin forzar ventana/ratón. El lanzador anterior de resoluciones continúa aislando el ajuste.

La densidad de píxel de la ventana se solicita en su creación cuando FIT está activo. Tras guardar FIT por primera vez, reiniciar permite crear la ventana con esa propiedad; cambiarla en vivo no recrea el renderer ni las texturas.

## Briefing y reclutamiento

Las capturas de Miguel muestran briefing textual y colina de reclutamiento. Se reconocen mediante sus flags existentes y las superficies exactas (mSurface / mSurfaceRecruit). Se reutilizan el recorte original y el rectángulo de dibujo físico. Se publica la inversa solo después de presentar, con identidad de escena para rechazar coordenadas de otra pantalla. Se mantiene la entrega del cursor del sistema en bandas y se suprimen clics sostenidos desde ellas. Las pantallas de cargar/guardar con otra superficie, imágenes externas, vídeo y demás escenas no se incluyen automáticamente.

## Validación

- Compilación sintáctica de los tres .cpp modificados contra cabeceras SDL 3.4.0, sin mixer local.
- Métodos reales de menú, INI y ventana extraídos, ASan/UBSan: edición/defaults sin escritura, INI antiguo/inválido/round trip/overrides, 14999/15000 ms y wraparound, KEEP tardío, cancelar/Escape, fallo de cada solicitud SDL, solicitud denegada, fallo de guardado, fallo y reintento de restauración, cambio externo, fullscreen/maximizado y posición.
- La misma fixture se compila mediante CMake/CTest en Windows/Linux cuando Python está disponible (en ambas CI); las aserciones permanecen activas también en Release.
- Métodos reales de render/present/mouse: 544.000 coordenadas clásicas, 228 ajustes de misión, 216 mapas, 72 transiciones de pausa y 144 ajustes briefing/reclutamiento. Prueba también preferencia INI sin flags, puntos de botones y cambio de escena.
- Regresiones locales: 144 programaciones de pausa, 2.944 casos de capas; 1.536 raster, 1.964 escenas, 1.024 tiles y 72 minimapas.

Son dobles SDL y pruebas de código, no prueba física de GPU/ratón. Las demos que saltan briefing/reclutamiento no prueban automáticamente esas pantallas en ejecución real. Sigue pendiente verificar el paquete nuevo y probar en Windows UHD/300 % las pantallas reportadas y el menú.

## Siguiente

Validar el paquete nuevo: opciones (guardar, dejar caducar, cancelar, reiniciar) y reclutamiento/briefing maximizado → misión. Después comparar muestras C a densidad suficiente, incluido cursor. Monitores, modos enumerados, exclusiva, interfaz independiente, sincronización y límite de FPS siguen pendientes de cortes posteriores H5.6; no se anuncian como implementados.

Referencias de API: [SDL_SyncWindow](https://wiki.libsdl.org/SDL3/SDL_SyncWindow), [SDL_SetWindowFullscreen](https://wiki.libsdl.org/SDL3/SDL_SetWindowFullscreen), [SDL_RenamePath](https://wiki.libsdl.org/SDL3/SDL_RenamePath).

## Verificación posterior — revisión 2.50

Windows 40713267240 completo PASS; el paquete verificado contiene la corrección de ambas escenas. [Evidencia y descarga](H5_6_VALIDACION_551eaf7.json). Linux falló en un control que todavía exigía igualdad de todo OptionsMenu.cpp con la versión anterior a H5.6. Se actualiza mediante huellas exactas y verificación de las dos llamadas explícitas a fade, sin cambiar motor ni H3. 27.648 casos de superficie y transacciones de opciones PASS localmente. Cierre de la nueva CI global y prueba física de Windows pendientes; el paquete Windows 551eaf7 sigue siendo válido para probar estas funciones.
