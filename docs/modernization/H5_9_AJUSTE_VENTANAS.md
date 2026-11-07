# H5.9 — ajuste opcional de misión a ventanas

Activación: `OPENFODDER_MISSION_SCREEN_TRANSFORM=1` y `OPENFODDER_MISSION_SCREEN_FIT=1`, ventana, ratón absoluto alternativo y desbloqueado. El nuevo lanzador configura ese alcance. Sin flags, comportamiento clásico. El piloto anterior permanece disponible con FIT=0.

Se habilita redimensionamiento y salida de alta densidad al crear la ventana opcional. Durante misión, el destino usa la escala uniforme mínima entre ancho y alto físicos disponibles, centrado. Se conservan recorte, encuadre y proporciones de ventana aceptadas (PC 320×200; Amiga 320×225). 4:3 y 16:9 describen la ventana, no una nueva corrección del dibujo. No hay panorámico con más mapa ni arte HD.

El rectángulo se convierte una sola vez a precisión SDL; la inversa retiene exactamente ese destino y el tamaño de ventana/salida. Solo se publica tras dibujo y presentación correctos. Cambios de tamaño/DPI/foco invalidan el snapshot. Las bandas rechazan entradas y pulsaciones retenidas. Estado SDL no soportado retorna como pareja dibujo/entrada al clásico. Se corrige la comprobación exacta antigua que sumaba floats antes de comparar con dobles; el redondeo de tamaños fraccionarios no debe provocar una excepción.

## Validación

Fixture con métodos reales y dobles SDL: 544.000 coordenadas clásicas PC/Amiga, más 190 combinaciones (18 resoluciones hasta 3840×2160 y una ventana impar; DPI 100/125/150/175/200%; dos backends). Comprueba destino contra cálculo independiente, inversa muestreada, bandas, pulsación retenida, invalidación, presentación fallida y retorno. ASan/UBSan local, LSan desactivado por limitación de entorno. El modelo racional independiente sigue aprobado (cinco pruebas). Regresiones ASan/UBSan locales aprobadas: 2.944 casos de capas; 1.536 raster, 1.964 escenas, 1.024 tiles y 72 constructores de minimapa. Los primeros intentos de estas dos regresiones no pudieron ejecutar LSan por restricciones /proc/ptrace; se repitieron con detección de fugas desactivada, sin cambiar la configuración de CI.

La sonda de replay de Windows/Linux activa ahora FIT además de la transformación. CI global inicialmente pendiente al publicar; cerrada después con éxito en Windows 40542788013 y Linux 40542787684 para 45de47a4. [Evidencia completa](H5_9_CIERRE_CI_45de47a4.json). Prueba Windows física del nuevo ajuste todavía pendiente. No se cambian referencias H3. La fixture no acredita GPU, interacción física ni nitidez del recurso ampliado.

## Límites y siguiente paso

Menús, pausa, overview, fullscreen y ratón relativo/bloqueado conservan presentación clásica; pueden cambiar tamaño aparente. No hay selector, persistencia de tamaños arbitrarios, cambio de modo con recuperación de 15 segundos ni interpolación. Estas tareas y la integración de las demás escenas siguen en H5.5/H5.6/H5.9. CI cerrada; comprobar ahora el nuevo lanzador en Windows; conservar el PR abierto y sin fusionar.
