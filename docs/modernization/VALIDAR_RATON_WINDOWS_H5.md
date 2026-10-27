# Validación interactiva Windows — pantalla y ratón H5.5

Pendiente de ejecución por Miguel. La CI Windows y el replay automático no sustituyen esta comprobación con pantalla y ratón físicos. No ampliar el ajuste multirresolución antes de revisar el resultado.

## Preparación

1. Descargar `OpenFodder-Windows-x64-demos` de una ejecución Windows **completada en verde** cuyo commit figure en el informe de validación. Es el ZIP de **Artifacts**, no el ZIP del código de la rama.
2. Extraerlo entero en una carpeta nueva. No copiar configuraciones ni partidas de otra instalación. Así `mouse-locked` empieza desactivado. Mantener `VERSION.txt` para identificar el motor.
3. En paquetes que incluyen esta guía, ejecutar **PROBAR_RATON_H5.cmd**. Arranca en ventana y ratón alternativo absoluto, con la transformación nueva activada. Las variables solo duran en ese proceso. No cambia ajustes de Windows ni instala nada.
4. Elegir la demo **PC Format**; repetir después con **Amiga The One**. No hace falta aportar ni copiar datos CD32.

El test utiliza gráficos clásicos para centrar la comparación en las posiciones. C01 y todas las mejoras siguen en el motor; no se eliminan. No se evalúa aquí la calidad artística ni una densidad HD.

## Comprobación de 5–10 minutos

| Acción | Resultado esperado |
|---|---|
| Mover el cursor despacio por el centro y cerca de los cuatro bordes del mapa | Sin saltos al entrar en misión; el punto señalado se mantiene coherente con la orden. El soldado puede seguir una ruta distinta por obstáculos. |
| Seleccionar soldados y ordenar desplazamientos a puntos despejados | La selección y el destino coinciden con el cursor; sin desplazamiento constante horizontal/vertical. |
| Usar el panel lateral y volver al mapa | El panel responde en su zona; sus clics no se convierten en órdenes sobre el terreno. |
| Pulsar `P` y volver a pulsarlo | Pausa y reanudación correctas; sin salto de cursor ni orden inesperada al volver. |
| Hacer Alt+Tab y regresar | Recupera el control y el punto señalado; sin disparo ni movimiento por una pulsación mantenida fuera. |
| Cambiar tamaño con `+`/`−` (preferiblemente teclado numérico) | Correspondencia ratón/dibujo conservada en las escalas que admite el motor; sin orden inesperada durante el cambio. No se prueba aún arrastre libre del borde de ventana. |
| Si hay bandas visibles, iniciar una pulsación en la banda y entrar al mapa sin soltar | No debe convertirse en una orden; soltar y pulsar de nuevo dentro. Si no aparecen bandas, marcar este caso «no probado». |
| Pulsar F11 para fullscreen y volver con F11 | Regreso correcto a ventana. Fullscreen usa el adaptador clásico: no cuenta como aceptación del nuevo modo. |

No pulsar F12 durante esta comparación: conmuta el bloqueo de ratón y deja fuera del alcance del adaptador opcional. Si se pulsó por error, cerrar el juego y comprobar `mouse-locked=false` en `openfodder.ini` antes de repetir. No interpretar un caso que estaba fuera de alcance como aprobado.

Para comparar, cerrar el juego y ejecutar **COMPARAR_RATON_CLASICO.cmd** en la misma demo y escala. Ambos usan ratón absoluto; solo cambia la transformación H5.5. No se espera una diferencia visual en ventana normal. Si algo falla, indicar si sucede en ambos lanzadores o solo con H5.

Anotar la resolución de escritorio y escala de Windows que se usan habitualmente (por ejemplo, 1920×1080 y 125 %). No es necesario cambiar el sistema ni disponer de un monitor 4K para esta primera aceptación.

## Qué devolver

```text
VERSION.txt:
Demo(s):
Resolución de escritorio / escala de Windows:
Selección y destino: bien / problema
Panel: bien / problema
Pausa y Alt+Tab: bien / problema
Cambio +/−: bien / problema
Bandas: bien / problema / no probado
F11 y vuelta: bien / problema / no probado
Comparación clásica: igual / solo falla H5 / fallan ambos
Detalle del problema y pasos:
```

Si hay un problema, adjuntar `H5_RATON.log` y, si se comparó, `H5_RATON_CLASICO.log`, junto con `VERSION.txt`. Una captura o vídeo corto ayuda a identificar un desplazamiento. Los logs no certifican por sí solos que cada clic haya sido correcto ni que todas las rutas del adaptador se hayan activado.

## Límites de aceptación

Esta prueba cubre interacción de las demos y el equipo indicado. No cierra CD32 completo, ratón relativo, interpolación de cámara, panorámico, otras escenas o toda la matriz 4K. El requisito de conservar base clásica y mejoras sigue vigente; el PR permanece sin fusionar.
