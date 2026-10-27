# Contrato de transformaciones de pantalla

27-10-2026 · Contrato inicial 2.35; avance 2.36 · H5.5/H5.9 parciales. Especificación y modelo matemático verificable; [primera conexión opcional a misión](H5_5_TRANSFORMACION_MISION.md) implementada para el rectángulo clásico y ratón absoluto. El resto del contrato sigue pendiente. No cierra soporte 4K, interpolación ni panorámico. Continúan el clásico, C01 y todas las mejoras anteriores.

## Qué hay actualmente

- `Source/Window.cpp`, `RenderAt`: recorta la fuente desde (16,16), con tamaño `mScreenSize`. En ventana usa resolución original × multiplicador. En pantalla completa sin escala entera calcula ancho a partir de alto × 4/3 y centra usando el modo del monitor. No hay una transformación compartida con entrada.
- `RenderShrunk` usa toda la fuente desde (0,0); no se le puede aplicar automáticamente el recorte de misión.
- `Source/Versions.hpp`: pantalla principal PC 320×200, Amiga 320×225; segunda pantalla Amiga 320×260. El contrato debe acompañar a cada escena, no asumir 320×200 universal.
- `Source/Mouse.cpp`: escala entera de `GetScale()`, ajustes de ratón (-32,+4), entrada relativa, captura/liberación y warp. Hay cálculos posteriores de mundo, cámara y selección; no se deben duplicar estos ajustes en la transformación genérica.
- `Source/Utils/SpriteDrawState.hpp`: posición de destino previa al recorte `x=modX+spriteX-mapX+xBias`, `y=modY+spriteY-rows-height-mapY`. Son coordenadas de almacenamiento, no directamente de ventana. El piloto C01 usa ese destino real y conserva su cuadro lógico 16×14.

## Espacios y contrato de datos

| Espacio | Unidad y origen | Responsable |
|---|---|---|
| Mundo | Unidades lógicas del mapa; posición/altura y cámara separadas | Simulación, inmutable al presentar |
| Canvas de escena | Coordenadas lógicas de la composición, origen visible (0,0) | Adaptador de escena |
| Almacenamiento | Texeles de fuente; incluye padding/recorte | Recurso y destino capturados |
| Salida | Píxeles físicos del área cliente/destino de render | Presentación |
| Ventana | Coordenadas locales que recibe el ratón/warp | Adaptador SDL |
| Interfaz | Unidades propias; rectángulos de interacción explícitos | Layout de HUD/menús |

Cada frame presentado retiene un `ScreenTransformSnapshot`: ID/generación de escena y geometría, dimensiones de ventana W, salida física P, canvas L, corrección de aspecto a, rectángulo D de destino, rectángulo fuente R, cámara visual C y rectángulos de mundo/interfaz. Dibujo, cursor, selección y warp deben consumir **la misma versión**. No leer cámara actual o tamaños globales distintos para invertir un frame ya mostrado. Render-target interno HD y tamaño de salida son datos separados.

Valores no finitos, dimensiones no positivas, recurso incompatible o generación caducada invalidan el contrato. Durante minimización/salida cero no se divide ni se envían órdenes; se conserva una configuración recuperable. Se mantiene el render clásico como retorno de presentación; el retorno no justifica interpretar un clic con geometría obsoleta.

## Fórmulas de presentación y ratón

Todas las operaciones son continuas hasta el adaptador final; no usar divisiones enteras intermedias. Coordenadas de bordes; los centros de píxel se muestrean en (i+0,5,j+0,5). Rectángulos de interacción semiabiertos: izquierda/arriba incluidos, derecha/abajo excluidos.

Para canvas L=(Lw,Lh), corrección de aspecto a=(ax,ay)>0 y salida P=(Pw,Ph):

```text
k = min(Pw/(Lw*ax), Ph/(Lh*ay))
sx = k*ax; sy = k*ay
Dw = Lw*sx; Dh = Lh*sy
Dx = (Pw-Dw)/2; Dy = (Ph-Dh)/2
salida(canvas) = (Dx + canvas.x*sx, Dy + canvas.y*sy)
canvas(salida) = ((salida.x-Dx)/sx, (salida.y-Dy)/sy)
salida(ventana) = (ventana.x*Pw/Ww, ventana.y*Ph/Wh)
ventana(salida) = (salida.x*Ww/Pw, salida.y*Wh/Ph)
```

El DPI nominal no sustituye las relaciones P/W medidas, que pueden diferir entre ejes por redondeo. Usar el tamaño real del destino que recibe el render. Antes de integrar, comprobar las unidades del renderer SDL y sus posibles escalas/presentación lógica; no aplicar doble conversión. Las coordenadas globales de escritorio no entran aquí.

Primero comprobar si el punto físico está en D; las bandas no producen órdenes de mundo. Dentro de D, dar prioridad al HUD/menús y comprobar después el rectángulo interactivo del mapa. No convertir un clic en una banda en un clic en el borde mediante clamp. Para arrastrar/capturar fuera del área, definir política separada de cancelación/scroll, sin inventar una selección válida.

La escala entera de píxel clásico es una política adicional, **a=1 y k entero**, no el redondeo de sx/sy de cualquier modo. Si no cabe k≥1 se requiere fallback explícito. Conservar la política clásica existente mientras se valida el adaptador; no cambiar silenciosamente su aspecto.

## Aspecto y ejemplos de referencia

Para solicitar un aspecto visual A sobre un canvas L puede usarse ax=A*Lh/Lw, ay=1. Eso define una transformación deliberada, no prueba cuál era el aspecto artístico correcto de todos los recursos. En PC 320×200, A=4/3 da ax=5/6; en Amiga 320×225 da ax=15/16. La corrección por escena/backend sigue pendiente de aceptación visual. Nunca deducir el aspecto visual solo del ancho/alto del archivo.

| Caso matemático | Canvas / aspecto | Salida física | D=(x,y,ancho,alto) | sx,sy |
|---|---|---|---|---|
| PC corregido 4:3 | 320×200 / 4:3 | 1920×1080 | (240,0,1440,1080) | 4,5; 5,4 |
| PC corregido 4:3 UHD | 320×200 / 4:3 | 3840×2160 | (480,0,2880,2160) | 9; 10,8 |
| Amiga corregido 4:3 | 320×225 / 4:3 | 1920×1080 | (240,0,1440,1080) | 4,5; 4,8 |
| PC píxel cuadrado, ajuste fraccional | 320×200 / 8:5 | 1920×1080 | (96,0,1728,1080) | 5,4; 5,4 |

Con ventana 1280×720 y salida 1920×1080 (relación 1,5), su centro (640,360) corresponde al píxel físico (960,540) y al canvas PC (160,100). Un clic de ventana x=100 cae en la banda izquierda; no se manda al mapa. Estos ejemplos son referencias aritméticas, no capturas ni validación de un monitor real.

## Mundo, cámara, recursos y anclajes

Para el viewport moderno, definir explícitamente el origen O del mapa dentro del canvas y la esquina del mundo C representada allí:

```text
canvas_mapa = O + (mundo - C)
mundo = C + (canvas_mapa - O)
```

La cámara C será la del frame mostrado. La conversión no muta la cámara de simulación. Entrada de mundo se encola para el siguiente paso lógico conservando el momento, redondeo y límites del contrato de órdenes. Interpolación y la revisión de apuntado H5.5 siguen abiertas. Al ampliar a 16:9, el layout decide el tamaño lógico del viewport: cambiar P por sí solo no autoriza mostrar más mapa.

Para C01 actual, partir de la posición preparada **antes de recorte**, y trasladar de almacenamiento a canvas restando R.x/R.y (16,16 en `RenderAt`). Después aplicar D y sx/sy. El recorte del sprite cambia el subrectángulo de texeles, nunca su anclaje lógico. No aplicar de nuevo mapX/mapY a una posición ya preparada.

Una fuente artística de tamaño N y cuadro lógico G tiene densidad r=N/G por eje. Si el anclaje del recurso está en texeles b, su anclaje lógico es b/r. Posición final de una muestra: `D + escala * (anclaje_canvas + (texel-b)/r)`. Duplicar N y b preservando G debe dejar exactamente igual el anclaje en pantalla. No fijar r a partir de la resolución del monitor sin evaluar el tamaño mostrado. A 4K, el ejemplo PC usa 9×10,8 píxeles físicos por unidad lógica: un maestro 4× podría requerir ampliación. Esto justifica medir densidad, no elegirla todavía.

En la ruta clásica de ratón hay ajustes (-32,+4), cámara entera y otros offsets de selección. **No se sustituyen por O/C a ciegas**: el adaptador debe caracterizar por separado el punto de clic, hotspot del cursor, anclaje de sprite, HUD y comandos. La identidad visual de un sprite no prueba la equivalencia del punto seleccionado. El modelo adjunto prueba el contrato moderno, no esa equivalencia heredada.

## Interfaz, entrada relativa y cambio de tamaño

- Interfaz con transformación propia dentro de la salida, y orden de hit-test explícito por encima del mapa. El contrato de rectángulos debe compartirlo el dibujo. UI escalable no significa reinterpretar sus zonas clásicas por un factor aproximado.
- Ratón absoluto y warp usan funciones inversas comunes. Ratón relativo conserva por ahora sensibilidad, acumuladores fraccionarios y política de captura existentes. No multiplicar automáticamente sus deltas por P/W: el adaptador tendrá que identificar unidades/configuración SDL y probar captura/liberación. El modelo actual no cubre entrada relativa real.
- Cambiar resolución, DPI o monitor invalida la generación anterior; recalcular todo, publicar un frame coherente y volver a consultar posición antes de aceptar una nueva orden. Vaciar deltas heredados según la política de foco/captura. No avanzar simulación por redimensionar.
- El compositor HD tendrá una transformación canvas → destino interno y otra destino interno → salida. Su producto debe coincidir con la transformación directa anterior; cambiar calidad interna no cambia el punto del mundo seleccionado ni el tamaño lógico.

## Verificación y siguiente integración

`python3 tools/modernization/check_screen_transform_contract.py` ejecuta un modelo de referencia racional sin SDL: matriz de 18 resoluciones del plan, tamaños impares, DPI/ratios no uniformes, ida/vuelta, bandas, separación HUD/mapa, cámara fraccionaria, anclajes a distintas densidades y destinos internos alternativos. No acredita GPU, apariencia ni código C++ de producción.

Avance 2.36: valor C++ y adaptador de misión implementados opcionalmente, rectángulo contrastado con `RenderAt` e inversa absoluta conectada con ajustes clásicos. Pendiente su validación de CI/manual y extender el ajuste de destino al contrato multirresolución. Mantener `RenderShrunk` y demás escenas en su ruta actual hasta disponer de su propio contrato. Después verificar ratón absoluto/relativo y cambios de tamaño con SDL, H3 y pruebas Windows. Solo entonces comparar pose/terreno HD para elegir densidad.
