# H5.9 — cursor en bordes, UHD y escala del 300 %

Reporte de Miguel, 27-10-2026: «el cursor se paraliza momentáneamente, unas décimas de segundo, al pasar por los bordes, especialmente el izquierdo. Mi resolución es 3840x2160 y la escala del 300%. Por lo demás, bien».

Resultado manual: favorable en general, con incidencia abierta. Resolución indicada de escritorio: 3840×2160; escala Windows: 300 %. No se conoce aún el tamaño efectivo de la ventana/salida SDL ni la demo, y no se atribuye una reproducción física al asistente. Código del paquete entregado: 45de47a4 (asociación contextual).

## Inspección y reproducción acotada

La matriz anterior llegaba al 200 % de DPI. Se amplía al 300 %: 228 combinaciones de tamaño/backend/DPI en la fixture de métodos reales y 360 combinaciones en el modelo racional. Ambas pasan localmente, con ASan/UBSan en la fixture. LSan permanece desactivado localmente por la limitación ya documentada.

Se añade un barrido de ida/vuelta de los bordes laterales con salida UHD y ventana lógica 1280×720, para PC y Amiga. El adaptador retiene la posición anterior del cursor mientras el punto está en una banda y actualiza en la primera muestra dentro de la imagen, sin temporizador en esa rama. Este comportamiento es reproducible con dobles SDL; no mide latencia física ni demuestra que explique la percepción comunicada.

La espera clásica de recaptura de 150 ms está después del retorno de ratón alternativo; no se ejecuta en el modo absoluto del lanzador entregado. No se cambia ese temporizador sin comprobar que el usuario esté usando otra ruta. También existe un límite clásico distinto en el lado izquierdo con panel reducido, que debe distinguirse del cruce hacia las bandas.

Hipótesis principal: al cruzar una banda, el cursor dibujado se queda en su última posición mientras el puntero del sistema sigue oculto. Falta confirmar si ocurre fuera de la imagen, dentro de ella o al salir de la ventana. No se declara causa confirmada ni corrección aplicada.

## Siguiente paso

Miguel: precisar si la pausa aparece al entrar en la banda negra/salir de la ventana o todavía dentro de la imagen jugable. Según esa observación, revisar la presentación del cursor fuera del área o instrumentar la ruta interior. Mantener bloqueadas las órdenes originadas en bandas. No ampliar escenas hasta resolver y volver a validar la incidencia.

Este incremento añade pruebas y documentación; no modifica motor, referencias H3, arte ni base clásica. CI del motor 45de47a4 sigue cerrada; los tests ampliados requieren su nueva ejecución CI. PR abierto y sin fusionar.

## Aclaración y corrección — incremento 2.42

Miguel precisa que solo ocurre al maximizar, al tocar los límites izquierdo y derecho de la imagen del juego; en ventana sin maximizar no ocurre. Esto acota la incidencia a la transición entre imagen y bandas del ajuste. La aceptación física de la corrección sigue pendiente.

Corrección implementada: distinguir `Band` de una geometría inválida. En bandas, mostrar el puntero del sistema y suprimir únicamente los píxeles del cursor del juego, manteniendo sus decisiones, selección, preparación y registros originales. Al reentrar, recuperar el cursor del juego sin temporizador de recaptura. La visibilidad del sistema se actualiza en FrameEnd, en el hilo de presentación; el estado compartido de banda es atómico. Pausa, demos grabadas, fullscreen y otros modos conservan su alcance clásico. Los clics en bandas siguen bloqueados, incluida la pulsación mantenida al reentrar.

Pruebas locales PASS con ASan/UBSan (LSan local desactivado): 544.000 coordenadas y 228 combinaciones; barrido lateral UHD/300 % en ambos sentidos con visibilidad del sistema; 2.304 casos de cursor y 288 HUD, más comprobación PC/Amiga de que ocultar píxeles conserva todos los registros; 10.944 casos de preparación/recursos; 192 escenarios de productores, 384 transiciones con digest original `15155017350506417091`. La captura del cursor se prueba sin eliminar su marca de procedencia; el guard de productores admite solo las dos líneas nuevas verificadas funcionalmente.

Nueva CI pendiente al publicar. No reutilizar el paquete 45de47a4 como si contuviera este arreglo. Tras CI verde, repetir maximización y cruces laterales al 300 %, confirmando que aparece el puntero Windows en la banda y vuelve el cursor del juego dentro. No ampliar escenas hasta esa comprobación.
