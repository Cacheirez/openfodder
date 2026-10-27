# H5.5 — primera integración de pantalla y ratón en misión

27-10-2026 · Plan 2.36. Implementación opcional, aceptación parcial. Conserva base clásica, mejoras, recursos originales, C01, referencias H3 y PR sin fusionar.

## Cierre de la CI anterior

El motor C01 `1bcf69c21a38f26cac14f5092dc7ef087dfdbfa5` termina con Windows y Linux completos aprobados:

- [Windows 40463857888](https://github.com/Cacheirez/openfodder/actions/runs/40463857888).
- [Linux 40463857883](https://github.com/Cacheirez/openfodder/actions/runs/40463857883).
- [Evidencia con cierre posterior a la observación inicial](H6_3_CI_1bcf69c.json), campo `closure`. Incluye todos los pasos y conclusiones, no solo la prueba artística.

Linux supera los recorridos de memoria y concurrencia declarados por el workflow (ASan/UBSan/LSan/TSan). No convertir los recorridos de publicación H4 en una afirmación de sanitizadores dedicados a todas las sustituciones artísticas C01. La CI del incremento nuevo es independiente.

## Activación y alcance exacto

```text
OPENFODDER_MISSION_SCREEN_TRANSFORM=1
openfodder --window --alternate-mouse
```

La opción `mouse-locked` guardada debe estar desactivada. El resto de opciones de C01/publicación puede mantenerse. Por defecto sigue la ruta clásica. Primer adaptador: misión PC/Amiga, ventana y ratón absoluto alternativo. El encuadre, rectángulo de dibujo, recorte y campo visible existentes no cambian. No constituye todavía ventana libre bien ajustada, panorámico, compositor HD ni aceptación 4K.

`Video_SurfaceRender` transmite a `RenderAt` el booleano de elegibilidad de misión ya calculado: fase activa, sin pausa/overview/interrupt, superficie principal no cargada como imagen, recorte normal y sin shrink. Las otras llamadas usan `false` por defecto. No se alteran productores, cadencia, cámara, simulación ni el contraste de C01.

## Dibujo y entrada compartidos

`ScreenTransform` conserva por valor tamaño de ventana, salida física y los rectángulos fuente/destino realmente enviados a SDL. La fuente incluye (16,16) de almacenamiento. Su proyección de origen y extremo debe reproducir el rectángulo clásico exactamente; una discrepancia es error, no retorno silencioso.

El snapshot solo se prepara tras un `SDL_RenderTexture` correcto y se publica tras un `SDL_RenderPresent` correcto. El ratón usa el último snapshot presentado, nunca el que aún se está dibujando. Un mutex protege los nuevos valores compartidos; no implica que todos los buffers heredados estén preparados para concurrencia.

La inversa convierte ventana → salida física → canvas, conserva la cuantización por suelo y entrega el mismo dominio de cursor que antes: `floor(canvas.x)-32`, `floor(canvas.y)+4`. Los cálculos posteriores de panel, hotspot, selección, cámara y mundo siguen en sus funciones originales. No se aplica dos veces el recorte de almacenamiento, ni se equipara un anclaje de sprite con un punto de selección.

Se contrasta el dominio completo de PC 320×200 y Amiga 320×225 a escala 2: 544.000 coordenadas de ventana. En el área cubierta, el resultado coincide exactamente con la división entera clásica. También se comprueba una relación ventana/salida 1:2. Los eventos existentes siguen llegando como coordenadas enteras; preservar subpíxeles de los eventos SDL es trabajo posterior.

El snapshot de este incremento es de **pantalla/canvas**. No introduce cámara visual interpolada ni cambia el momento lógico de una orden. La captura temporal completa de cámara/mundo y su conversión inversa permanecen abiertas en H5.5.

## Invalidación y retorno

- Bandas, exterior y bordes derecho/inferior quedan fuera del hit-test. No se ajustan al borde del mapa. Se conservan las posiciones previas del cursor y se anulan botones de juego para esa entrada.
- Una pulsación iniciada fuera no se convierte en orden al volver dentro manteniendo el botón: hay que soltarlo. HUD y mapa continúan separados por la lógica original después de convertir al dominio de cursor clásico.
- Cambios de tamaño, píxeles físicos, monitor o pérdida de foco invalidan el snapshot. Antes de usarlo se vuelven a comprobar tamaños reales; si no coinciden se bloquea la entrada hasta tener geometría válida. La pérdida de foco bloquea también la entrada del modo opcional.
- Fallo de dibujo/presentación: no se publica una transformación nueva. No reutilizar coordenadas de un frame fallido.
- Renderer con target, escala, viewport, clip o presentación lógica no compatibles: conservar dibujo e interpretación clásicos conjuntamente. No compensar a ciegas una segunda transformación SDL.
- Pausa, minimapa, otras escenas, fullscreen, ratón relativo/bloqueado y navegador conservan el adaptador clásico. `RenderShrunk` invalida el snapshot. El navegador no adopta este ciclo de publicación.

Con alta densidad se invierte el **rectángulo que ya dibuja el motor**, no un nuevo ajuste a toda la salida. Por eso esta integración corrige la correspondencia con lo mostrado, pero no acredita aún el diseño multirresolución completo.

## Pruebas

Local aprobado:

- `check_screen_transform_integration.py`: cuerpos reales de RenderAt, RenderShrunk, FrameEnd, MapMissionMouse, invalidación y bloque de ratón alternativo; dobles SDL. ASan/UBSan, 544.000 puntos PC/Amiga, origen de almacenamiento, DPI, bandas, pulsación retenida, foco, tamaños cambiados, presentación pendiente/fallida y retornos. La prueba exige que el resto de `Mouse.cpp` siga idéntico al commit anterior. LSan local desactivado; sin afirmación de GPU o interacción manual real.
- `check_screen_transform_contract.py`: cinco pruebas del modelo racional y 300 combinaciones.
- `check_mission_presentation.py`: 240 programaciones, 672 frames retenidos, pausa/reanudación y equivalencia con cuerpos anteriores.
- `check_mission_recording.py`: ocho configuraciones, 192 escenarios / 384 transiciones; huella `15155017350506417091` conservada.
- 30 tests Python y contrato de visibilidad H3 aprobados.

Añadido a CI: fixture bajo ASan/UBSan en Linux y replay con `--screen-probe --first-phase` en Windows/Linux. El replay activa ventana/ratón alternativo, exige el marcador `SCREEN_TRANSFORM: presented mission and verified mouse inverse` en cada campaña y conserva los 301 estados H3 de las primeras fases PC/Amiga. El marcador solo se emite tras presentar un snapshot válido y comprobar la inversa; no basta ejecutar con una variable activada.

Los replays usan entradas canónicas grabadas: no simulan clics físicos de usuario. La cobertura de clics reales sigue siendo la fixture con dobles y la prueba manual pendiente. No declarar verde el nuevo motor a partir del cierre de C01.

## Primera CI del adaptador y corrección de la puerta HUD

`fb4a997`: compilación y replay activo H5.5 aprobados en **Windows y Linux**. Linux conserva los 301 estados H3 de las primeras fases PC/Amiga. [Evidencia parcial](H5_5_CI_fb4a997.json). No es un cierre global: Linux falla después en una comprobación histórica que exigía identidad completa de `Mouse.cpp`; Windows seguía ejecutándose al registrar el informe.

Corrección acotada: `screen_mouse_contract.py` permite retirar **solo el bloque literal aprobado** del nuevo adaptador para comparar el resto del fichero con el original. La puerta conserva la igualdad de todas las demás decisiones/operaciones del cursor y de `GUI_Element.cpp`; la fixture nueva usa la misma normalización y prueba el adaptador real. No se cambia el motor para resolver ese fallo. En la prueba HUD local se desactiva LSan por la limitación `/proc`/ptrace ya conocida; no se atribuye cobertura local de fugas.

## Siguiente paso

Revisar la nueva CI y validar en Windows dibujo/ratón, pausa, cambios de foco y tamaño. Después sustituir la política de destino heredada por el ajuste multirresolución del contrato, con opciones y recuperación. Incorporar ratón relativo/warp y las escenas restantes antes de aceptar H5.5/H5.9. Densidad HD aún sin fijar.
