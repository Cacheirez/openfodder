# Validación interactiva Windows — pantalla y ratón H5.5

El piloto de correspondencia original fue aceptado por Miguel el 27-10-2026. El nuevo ajuste multirresolución requiere una comprobación específica cuando su CI termine; no se considera probado por esa aceptación anterior.

Paquete histórico del piloto anterior (no contiene el nuevo ajuste): [Windows 40523807564 / OpenFodder-Windows-x64-demos](https://github.com/Cacheirez/openfodder/actions/runs/40523807564/artifacts/12743312861). Su `VERSION.txt` es `13461eb7e0f5491b1d107deee4489f2a1e78d6d4`, commit temporal de CI con el mismo árbol que c8c54ab; el PR sigue sin fusionar. Esta guía ya va incluida en ese ZIP.

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

## Nuevo ajuste opcional de ventanas — incremento 2.39

[Descargar el paquete nuevo verificado](https://github.com/Cacheirez/openfodder/actions/runs/40542788013/artifacts/12753080638), con CI Windows/Linux aprobada para `45de47a4`. Extraer en carpeta nueva y ejecutar **PROBAR_RESOLUCIONES_H5.cmd**. `VERSION.txt` contiene `ad490a30678cd927bbc20959c6712760802eb610`: es el commit temporal de prueba de GitHub, cuyo árbol es idéntico al del código validado; no implica fusión del PR. SHA-256 del ZIP: `8868145b186ae5472b505130aee4630513e892243e41f5fa0affb9b0bfbfb659`. Arrastrar bordes o maximizar la ventana durante la misión; probar formas 4:3 y 16:9, el centro, los bordes y el panel. La imagen crece uniformemente y se centra con bandas. Las proporciones son las ya aceptadas en ventana: PC 320:200 y Amiga 320:225; no se aplica una corrección artística nueva a 4:3. Una ventana 16:9 no muestra más mapa.

Repetir pulsación en bandas y entrada sin soltar, pausa/reanudación, Alt+Tab y reducción/ampliación. Pausa, menús, fullscreen y ratón bloqueado/relativo conservan presentación y entrada clásicas; puede verse un cambio de tamaño al entrar en esas escenas. F11 no valida el ajuste nuevo. **COMPARAR_RATON_CLASICO.cmd** vuelve al render clásico al reiniciar, y **PROBAR_RATON_H5.cmd** conserva el piloto anterior sin ajuste. No hace falta cambiar la resolución ni el DPI de Windows; anotar los utilizados. El tamaño 4K se comprueba automáticamente en geometría; no se atribuye una prueba física 4K al usuario.

Log del nuevo lanzador: `H5_RESOLUCIONES.log`. Conservar también `VERSION.txt`. No hay todavía selector de resolución ni aceptación global H5.9.

## Reprueba de bordes — corrección 2.42

El ZIP de 45de47a4 enlazado arriba precede a esta corrección. Usar el [paquete corregido verificado de 1447abb](https://github.com/Cacheirez/openfodder/actions/runs/40588401900/artifacts/12774266903), con CI Windows/Linux completa en verde. Extraer en carpeta nueva. `VERSION.txt` debe contener `1447abb929d75817d36a28b4253490cdebd5e010`. SHA-256: `0c0d8550d246487fbece4084ad158fdc9d4da660d9bb5e0349439dcbc0e9bca0`. Ejecutar `PROBAR_RESOLUCIONES_H5.cmd`, maximizar con la configuración habitual 3840×2160/300 % y cruzar despacio los límites izquierdo y derecho de la imagen. En la banda debe verse el puntero Windows moviéndose; dentro vuelve el cursor del juego. No debe quedar dibujado un cursor inmóvil. Probar también una pulsación iniciada en la banda y mantenida al entrar: no debe dar órdenes hasta soltar y volver a pulsar. Comprobar después restaurar la ventana, pausa/reanudación y Alt+Tab. Esta prueba está pendiente; no se declara resuelta por las fixtures.

## Reprueba del mapa general — corrección 2.45

El paquete 1447abb enlazado arriba contiene el arreglo de bordes, pero no este ajuste del mapa. Usar el [ZIP nuevo verificado](https://github.com/Cacheirez/openfodder/actions/runs/40634973004/artifacts/12793692851), con Windows 40634973004 completo PASS. Extraer en carpeta nueva. VERSION.txt: `7c596ea4861d37c11921083c94b0c8ef5d3e0e4f`, commit temporal de CI con el mismo árbol que 6e98fda; PR sin fusionar. SHA-256: `e7687ac997024a00ca738a96a9533d8f12f37c86249169b1e53378a57be9ed25`. Linux global aún en curso al verificar. Usar `PROBAR_RESOLUCIONES_H5.cmd` y la misma edición en la que se observó el problema; las demos de release pueden tener deshabilitada la overview. Maximizar con 3840×2160/300 %, abrir el mapa desde el panel y comprobar que ocupa el área disponible de forma centrada, conservando su aspecto. Cerrar con un clic y comprobar selección/órdenes en misión y bordes del cursor. Restaurar/maximizar y repetir. Contrastar F11: debe conservar su comportamiento anterior. Registrar edición, VERSION.txt y resultado; no es necesario volver a validar todas las fases.

## Pausa ajustada — incremento 2.47

Mapa y bordes aceptados por Miguel; no se pide repetir toda su validación. El paquete 6e98fda no contiene el nuevo ajuste de pausa. Cuando esté disponible el paquete nuevo aprobado, usar PROBAR_RESOLUCIONES_H5.cmd, maximizar, pulsar P y comprobar que la imagen pausada conserva tamaño/centrado. Restaurar/maximizar mientras está pausado, reanudar con P y probar selección/órdenes y bordes. Mantener 3840×2160/300 % habitual. F11 debe conservar su ruta clásica. Registrar VERSION.txt y cualquier cambio de posición o clic inesperado; la prueba física queda pendiente.
