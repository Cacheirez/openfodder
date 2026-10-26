# Piloto visual — alcance de trabajo

26-10-2026. H6.1 parcial: [primera muestra B01 presentada](H6_1_MUESTRA_B01.md), 2D ilustrado limpio, revisada para reducir ruido del terreno. Todavía no hay conceptos aprobados ni recursos HD integrados. Faltan A/C comparables y comprobación a escala real.

## Decisión de secuencia

El diseño conceptual puede comenzar mientras se completa el contrato semántico de H4.2/H4.4. No requiere cerrar todas las escenas, toda CD32 ni la interpolación a 144 Hz. La integración de una muestra sí requiere identidad y generación de entidad, posición/cámara coherentes, anclaje y correspondencia con el recurso clásico. Las escrituras de píxeles actuales no sustituyen esos datos.

Se mantiene la campaña CD32 como destino del proyecto. Para una prueba técnica reproducible se usan las primeras fases públicas PC/Amiga; esto no sustituye la posterior comprobación privada con CD32. Los recursos comerciales no se publican.

## Una misma muestra para comparar

Preparar tres conceptos del mismo soldado en la misma pose y perspectiva cenital oblicua clásica, sobre un fragmento pequeño de jungla: suelo, borde de vegetación, árbol/obstáculo y sombra. Añadir una copia a tamaño de juego para comprobar legibilidad. Misma cámara, encuadre y silueta lógica en las tres muestras; evitar que una presentación más vistosa falsee la comparación.

| Dirección candidata | Qué probar | Riesgo que comprobar |
|---|---|---|
| Píxel refinado | Siluetas nítidas y continuidad visual con el clásico | Confundir más resolución con más detalle útil |
| 2D ilustrado limpio | Formas simples, luz y sombras moderadas, color legible | Exceso de suavizado o aspecto de pegatina |
| 2D pintado moderado | Textura y volumen contenidos | Ruido visual al reducir el soldado a tamaño jugable |

Recomendación inicial de trabajo: 2D ilustrado limpio; es una propuesta, no una decisión atribuida a Miguel. La elección corresponde a Miguel viendo las muestras. Comparar 2×/4× como hipótesis; no fijar 4× como obligación.

## Límites del primer recurso integrado

Un soldado, una pose inicial y un fragmento de terreno; retorno automático al original para todo lo demás. Conservar campo visible, coordenadas, caja lógica, colisiones, selección, disparos y tiempos de animación. El atlas final seguirá las direcciones/fotogramas del inventario real: no inventar ahora un número uniforme de direcciones.

Separar cuerpo y sombra solo si el contrato de recursos lo soporta; fijar anclaje de pies, margen transparente, escala visual y procedencia. La imagen conceptual no es un sprite listo para el juego. La primera integración verificará que el anclaje no salta al cambiar de recurso, que el ratón sigue apuntando al mundo correcto y que H3 se conserva.

## Tres entregas concretas

1. Comparativa visual de las tres direcciones, sin integración: H6.1; Miguel elige H6.2.
2. Captura semántica mínima de cámara y un sprite, con identidad/generación y continuidad temporal: H4.2/H4.4. Primero reproducir el original; después sustituir una pose.
3. Escena jugable acotada con sustitución individual y retorno al original; comprobar pausa/reanudación y selección. Solo entonces ampliar animaciones, vehículos, edificios y terreno.

Estas entregas son criterios de avance, no una estimación de días. H5.1 comienza con una medida comparativa del proceso completo; aún faltan tiempos por frame, CPU/memoria y Windows/GPU. No presentar los tiempos de CI ni de replays acelerados como FPS del juego.

## Alcance de catálogo aclarado

El [censo CD32](CD32_CENSO_SPRITES.md) cubre todas las fases iniciales. Antes de producción, clasificar tipos y estados de las fases avanzadas; añadir el helicóptero ocupable como prueba compuesta tras el soldado. No inferir que todos los gráficos o capacidades están representados por los replays de demos.
