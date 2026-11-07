# H5.9 — aceptación de bordes y escalado del mapa general

Fecha: 28-10-2026.

Miguel confirma corregido el problema del cursor y aprobados los puntos 4 y 5: cruce de ambos límites y bloqueo de órdenes desde bandas. Configuración comunicada anteriormente: 3840×2160 al 300 %. Se cierra esa incidencia en el alcance observado del paquete 1447abb; no equivale a aceptar todas las escenas o modos.

Nueva incidencia: «a pantalla completa, al pinchar el mapa, el mapa no escala, se queda pequeño en la esquina superior izquierda». Pendiente distinguir pantalla completa F11 de ventana maximizada y confirmar que se trata del mapa general abierto desde el panel. No se conoce la edición/campaña usada para esta observación.

Inspección del código 1447abb: Phase_Map_Overview_Show llama a Video_Sleep(mSurfaceMapOverview, true), que acaba en RenderShrunk. Esa ruta usa GetWindowSize() para el destino, no la salida física actual, y en ventana fija origen (0,0). El ajuste opcional existente solo cubre misión y excluye overview. Esto explica plausiblemente el mapa pequeño arriba a la izquierda en ventana maximizada; no demuestra todavía el caso F11. En fullscreen hay además otra rama de centrado basada en el modo de pantalla.

Siguiente incremento: ajustar explícitamente el mapa general con destino centrado y proporciones conservadas, diferenciando ventana maximizada/F11 y píxeles físicos/DPI. Mantener pausa, marcador de escuadrón, salida con clic y regreso a misión. No ampliar el ajuste genéricamente a todos los usos de RenderShrunk. Conservar la ruta clásica y las referencias H3. No se ha modificado el motor en este registro.

Requisito artístico: el cursor del juego se rediseñará junto con personajes, objetos y fondos, siguiendo C — Pintado moderado. Inventariar variantes y estados, definir punto activo de clic, escala visual independiente del área de interacción, legibilidad/contraste en todos los fondos y DPI; validar selección y apuntado. Mantener cursor original como retorno. El puntero del sistema mostrado en bandas no constituye el nuevo diseño artístico.

## Aclaración y corrección — incremento 2.45

Miguel confirma: «lo del mapa ocurre con la ventana maximizada, con F11 va todo perfecto». Se acota la incidencia al mapa general en ventana maximizada.

RenderShrunk ajusta ahora únicamente la superficie del mapa general activo cuando están habilitados SCREEN_TRANSFORM y SCREEN_FIT, en ventana con ratón absoluto desbloqueado. El destino usa el tamaño físico de salida del renderer y se centra, con escala uniforme sobre el rectángulo clásico: se conserva el aspecto visual anterior del mapa, no se redefine a partir de su almacenamiento cuadrado. La fuente se mantiene completa. F11, flags desactivados, otros usos de RenderShrunk y estados SDL no soportados conservan su destino clásico.

La ruta del mapa no publica una transformación de ratón de misión: conserva su comportamiento de cerrar con un clic, sin coordenadas de selección del mundo. No cambian pausa, marcador, Save/Restore ni retorno a misión. Las pruebas de esos efectos de juego no se sustituyen por las fixtures de geometría.

Pruebas locales con métodos reales y dobles SDL, ASan/UBSan sin LSan local: 216 casos de overview (seis salidas hasta UHD incluida una impar, seis DPI hasta 300 %, PC/Amiga y tres tamaños de fuente). Verifican destino, centrado, fuente completa, ausencia de snapshot de misión y retorno a la inversa de misión; además trece exclusiones/estados y F11. Continúan pasando 544.000 coordenadas clásicas y 228 casos de ajuste de misión. Regresiones de capas y productores indexados conservadas.

CI nueva y aceptación física pendientes al publicar. La overview está deshabilitada en las demos no personalizadas fuera de debug: no atribuir cobertura automática de esta escena a los replays normales. Repetir con la edición en que Miguel ya abrió el mapa, maximizando al 300 %, cerrando el mapa y comprobando selección/órdenes; contrastar F11, que ya funcionaba. PR sin fusionar, base clásica, H3, C01 y cursor aceptado conservados.

## Paquete verificado — incremento 2.46

Windows 40634973004 completo PASS para 6e98fda. ZIP descargado y comprobado: hash, versión/árbol, integridad, tres lanzadores y guía. [Evidencia](H5_9_VALIDACION_6e98fda.json). El commit temporal 7c596ea tiene árbol idéntico al código de rama y no fusiona el PR. Linux supera las pruebas específicas del mapa pero continúa su CI global al registrar. Pendiente observación física en el equipo de Miguel: mapa maximizado → cierre con clic → selección y órdenes en misión, con contraste F11. No se atribuye esa observación a la CI ni al asistente.

## Aceptación manual y cierre Linux — 28-10-2026

Miguel confirma: «perfecto, el mapa se queda centrado, se cierra y vuelve a misión. Todo funciona bien». Se acepta la secuencia observada del mapa en la configuración comunicada. Linux 40634973034 ha terminado completo PASS, al igual que Windows 40634973004. Evidencia actualizada en H5_9_VALIDACION_6e98fda.json. Incidencias de mapa y bordes cerradas en su alcance; no se requiere repetirlas para una revisión documental. Siguiente incremento: mantener el ajuste de misión durante pausa/reanudación, conservando simulación y ruta clásica.
