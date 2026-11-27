# H5.9 — pausa con la geometría de misión

Incremento 2.47, 28-10-2026. Tras aceptar mapa y bordes, extender el ajuste opcional a la pausa de misión en ventana. No habilitado por defecto; requiere los mismos flags SCREEN_TRANSFORM/FIT y ratón absoluto desbloqueado.

RenderAt reconoce la pausa solo para la superficie principal de una misión activa, sin overview, callback de otra escena ni imagen cargada. Reutiliza cálculo de destino físico, recorte y aspecto ya validados. Mantiene tamaño/centrado al pausar y responde al redimensionamiento/DPI durante pausa. F11, modos incompatibles y escenas restantes conservan ruta clásica. No se modifica Phase_Paused ni las funciones de simulación, paleta, recursos o composición.

No se publica una inversa de entrada de misión para una imagen pausada. Al reanudar, se bloquea la entrada del adaptador hasta presentar un frame de misión válido con dimensiones actuales, evitando órdenes con geometría vieja. Fallos de dibujo/presentación siguen invalidando el snapshot. No se altera la lógica de botones ni se considera resuelta toda la entrada relativa/interpolada.

## Pruebas

Fixture con métodos reales y dobles SDL, ASan/UBSan sin LSan local: 72 transiciones misión/pausa/redimensionamiento/reanudación, seis salidas hasta UHD y una impar, DPI 100/125/150/175/200/300 %, PC/Amiga. Comprueba destino idéntico antes de redimensionar, nuevo ajuste al cambiar tamaño, bloqueo hasta publicación de misión, exclusiones, F11 y fallos de dibujo/presentación. Siguen pasando 544.000 coordenadas clásicas, 228 ajustes de misión y 216 casos de overview.

Fixture del bucle real de pausa: 144 programaciones, 0/1/5 presentaciones, fades, reanudación, recursos, generaciones y destinos independientes. Regresiones: 2.944 casos de capas y 1.536 raster/1.964 escenas/1.024 tiles/72 minimapas. El código de pausa anterior y las referencias H3 permanecen intactos.

La sonda temprana Windows/Linux combina ahora screen-probe y pause-probe en las primeras fases PC/Amiga, exige marcador del ajuste de pausa y compara H3 original. Es input canónico con eventos SDL de pausa; no prueba ratón físico/GPU. Nueva CI pendiente al publicar.

## Próximo paso

Cerrar la CI y verificar el nuevo paquete. En Windows: maximizar, pausar con P, comprobar tamaño/centrado, restaurar/maximizar mientras está pausado y reanudar; comprobar cursor y órdenes. No reutilizar 6e98fda como evidencia de esta nueva conducta. Tras validar esta transición, avanzar al mínimo de opciones de presentación H5.6 antes de fijar densidad artística. Base clásica, mejoras, C01 y plan de rediseño del cursor conservados; PR sin fusionar.
