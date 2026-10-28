# H5.9 — aceptación de bordes y escalado del mapa general

Fecha: 28-10-2026.

Miguel confirma corregido el problema del cursor y aprobados los puntos 4 y 5: cruce de ambos límites y bloqueo de órdenes desde bandas. Configuración comunicada anteriormente: 3840×2160 al 300 %. Se cierra esa incidencia en el alcance observado del paquete 1447abb; no equivale a aceptar todas las escenas o modos.

Nueva incidencia: «a pantalla completa, al pinchar el mapa, el mapa no escala, se queda pequeño en la esquina superior izquierda». Pendiente distinguir pantalla completa F11 de ventana maximizada y confirmar que se trata del mapa general abierto desde el panel. No se conoce la edición/campaña usada para esta observación.

Inspección del código 1447abb: Phase_Map_Overview_Show llama a Video_Sleep(mSurfaceMapOverview, true), que acaba en RenderShrunk. Esa ruta usa GetWindowSize() para el destino, no la salida física actual, y en ventana fija origen (0,0). El ajuste opcional existente solo cubre misión y excluye overview. Esto explica plausiblemente el mapa pequeño arriba a la izquierda en ventana maximizada; no demuestra todavía el caso F11. En fullscreen hay además otra rama de centrado basada en el modo de pantalla.

Siguiente incremento: ajustar explícitamente el mapa general con destino centrado y proporciones conservadas, diferenciando ventana maximizada/F11 y píxeles físicos/DPI. Mantener pausa, marcador de escuadrón, salida con clic y regreso a misión. No ampliar el ajuste genéricamente a todos los usos de RenderShrunk. Conservar la ruta clásica y las referencias H3. No se ha modificado el motor en este registro.

Requisito artístico: el cursor del juego se rediseñará junto con personajes, objetos y fondos, siguiendo C — Pintado moderado. Inventariar variantes y estados, definir punto activo de clic, escala visual independiente del área de interacción, legibilidad/contraste en todos los fondos y DPI; validar selección y apuntado. Mantener cursor original como retorno. El puntero del sistema mostrado en bandas no constituye el nuevo diseño artístico.
