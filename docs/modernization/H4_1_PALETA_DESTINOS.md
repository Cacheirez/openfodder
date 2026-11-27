# H4.1 — Paleta efectiva y destinos propios de conversión

23-10-2026. Código `ff15219680b289abf207fdc23fc436a9f390e649`. Comparación contra `c6af094c49641018b6dea6dc77cbe731a7ea0218`. PR #1 en borrador, sin fusionar; base H2.6 intacta.

## Frontera y propiedad

`cSurface::CaptureDraw` captura el buffer indexado completo en una copia privada e inmutable, las 255 entradas de `mPaletteSDL` por valor, dimensiones y skips. Es una lectura sin avances de fade, Save/Restore, llamadas SDL ni publicación de registros. No conserva cSurface, SDL_Surface, SDL_Texture ni punteros a buffers vivos.

[SurfaceDraw.hpp](../../Source/Utils/SurfaceDraw.hpp) define el comando `SurfaceDraw` y `SurfaceDrawTarget`, propietario exclusivo de su vector XRGB8888. `RasterizeSurface` devuelve un destino nuevo en cada llamada; copiarlo copia sus píxeles, moverlo transfiere propiedad. Los comandos comparten solo el buffer privado const; sus colores y geometría se copian por valor. Destruir/modificar la superficie productora no invalida los datos retenidos. Ninguna de estas operaciones publica automáticamente datos entre hilos.

El destino resuelto aquí es **la salida de conversión indexada a RGB**. Los rasterizadores de sprites/terreno/HUD siguen componiendo en sus destinos indexados clásicos. No se afirma haber construido un plan completo de composición ni haber migrado ventanas, overlays, PNG, minimapa o escenas a un presentador independiente.

## Paleta realmente visible

Capturar `mPalette` o `mPaletteNew` sería incorrecto: `surfaceSetToPaletteNew` aplica la paleta de destino directamente, mientras que `palette_SetFromNew` copia la paleta lógica sin aplicar inmediatamente la tabla SDL. Se conserva `mPaletteSDL`, ya mapeada mediante SDL para XRGB8888. No hay nuevo remapeo RGB, redondeo o interpretación artística.

| Contrato | Comportamiento conservado |
|---|---|
| PC | Canales de recursos cargados como bytes; conversión existente desplaza cada canal 2 bits antes de SDL_MapRGB |
| Amiga | Nibbles de 4 bits se expanden primero mediante desplazamiento de 2 bits al cargar; conversión de superficie aplica el desplazamiento existente adicional |
| Paleta efectiva | 255 colores, tabla SDL aplicada; distinta de actual/objetivo cuando las rutas clásicas lo requieren |
| Índice 0 | No escribe color; destino previamente negro |
| Índice 255 | Fuera de las 255 entradas, produce negro; no ampliar silenciosamente a 256 colores |
| Fade | Algoritmo original con componentes/diferencias int8, desplazamientos y retorno `!mPaletteAdjusting`; no se normaliza ni se reejecuta desde la captura |
| Save/Restore | Solo copian el buffer indexado; no guardan ni restauran paletas, SDL ni textura |
| clearBuffer | Sigue limpiando buffer vivo, guardado y SDL; no se sustituye por limpiar solo el destino nuevo |

La tabla `mPaletteSDL` se inicializa ahora a cero. Antes quedaba indeterminada hasta aplicar una paleta; copiar toda la tabla para retenerla exigiría leer entradas no inicializadas. Esto define el estado previo a la primera aplicación como negro, coherente con los buffers iniciales. No se atribuye equivalencia a lecturas indeterminadas anteriores; la equivalencia de paletas aplicadas se prueba contra el cuerpo original.

## Orden original

`cSurface::draw` mantiene la guarda PNG al principio. Después captura, llama a `clearSDLSurface(0)` en la fase original, convierte en un destino propio, copia sus píxeles a SDL y actualiza la textura una vez si existe. No se trasladan fades ni Save/Restore a este adaptador. Todas las funciones que llaman a Save/Restore/fade permanecen iguales a la base.

`Video_SurfaceRender` mantiene vídeo desactivado → selección de superficie → draw → RenderAt/RenderShrunk → FrameEnd. En pausa se mantienen fade de fondo → draw de fondo → draw de texto con su paleta → mergeSurfaceBuffer → RenderAt/FrameEnd. La captura individual no representa por sí sola esta composición final. El Restore comentado en Video_SurfaceRender continúa comentado.

La conversión conserva el recorrido empaquetado del original, skips por defecto 16/16, límite de fuente y limpieza previa. Sus precondiciones son las de superficies indexadas clásicas: dimensiones/buffers compatibles y skips no negativos dentro de dimensiones. No se extiende a pitch arbitrario, tamaños corruptos o un destino PNG. Los PNG devuelven captura vacía y draw sigue sin convertirlos. No se han revisado ni corregido aquí propiedad de memoria STB, composición PNG o ciclo de vida de texturas externas.

## Coste y límites

Cada captura copia el buffer indexado y 255 colores; cada conversión crea un vector RGB y lo copia a SDL. Es una frontera de propiedad explícita con coste adicional, no una optimización. No se aplica caché a un buffer mutable ni se reutiliza un destino entre capturas que puedan seguir retenidas. Cualquier optimización futura debe conservar esa independencia y medirse por separado.

## Verificación

[check_surface_draw_equivalence.py](../../tools/modernization/check_surface_draw_equivalence.py) extrae los cuerpos originales y actuales de Surface.cpp. Ejecuta las funciones reales de paleta/fade/Save/Restore con superficies SDL sintéticas XRGB, y compara el draw original con el adaptador nuevo. Comprueba estáticamente que esos cuerpos y todos sus archivos llamadores permanecen iguales a la base.

- 27.648 casos: 4 anchos × 3 alturas × 3 skips X × 3 skips Y × 8 modos × textura presente/ausente × 16 pasos.
- Modos de paleta actual/objetivo/efectiva divergentes, dimming, negro, clearBuffer, guarda PNG; índices 0 y 255, márgenes y centinelas de destino.
- Todos los píxeles, paletas, estado adjusting, buffers vivo/guardado, número de clear y actualizaciones de textura coinciden.
- Captura sin mutaciones y tres conversiones repetidas; destinos independientes; cambio/redimensionado/destrucción de fuentes; copia/movimiento y liberación tras el último propietario.
- ASan/UBSan en prueba focalizada; CI exige detect_leaks=1. El stub SDL verifica la frontera de datos y llamadas, no el driver GPU. La integración SDL real se compila en Windows/Linux; H3 y replays cubren el motor en modo de prueba, no una nueva validación visual CD32.

Local: Release y 6/6 CTests aprobados; contrato de visibilidad 15 referencias/9 archivos intacto; prueba focalizada 27.648 casos con ASan/UBSan (detect_leaks=0 local). H3 original: 7.956 estados PC + 3.405 Amiga = 11.361; 29/29 replays, cero omisiones, retorno 0, 15,967 s. SHA-256 del ejecutable local: `7566aeb79a3b332e59168604a47467d274ed67a33450f50c41623067f5b52851`.

CI [Windows 39995798688](https://github.com/Cacheirez/openfodder/actions/runs/39995798688) y [Linux 39995798623](https://github.com/Cacheirez/openfodder/actions/runs/39995798623): aprobadas. 6/6 CTests y H3 original (11.361 estados) en ambas plataformas. Windows 29/29 replays, 22,469 s; Linux ASan/UBSan 36,651 s, LSan 36,849 s y TSan 154,460 s, cada uno 29/29, cero omisiones, retorno 0 y sin diagnósticos en los registros examinados. Tiempos informativos, no benchmark; límite de 600 s e instrumentación intactos.

### Evidencia conservada

[Informes originales JSON y SHA de dependencias](evidence/ff15219-reports.json) conservados en Git. Comprobados CRC, tamaño y SHA-256 de ambos ZIP, y los 12 logs contenidos en ellos. Los logs de los jobs confirman también el baseline H3 original y los 27.648 casos focalizados con fugas activas.

| Plataforma | Artefacto | SHA-256 ZIP |
|---|---|---|
| Linux | 12520656497 | `730e1dc9d4ddf3838214ca507a3184879e82b1e3def771a5d2aaefb3cd998057` |
| Windows | 12520965264 | `df5f957de98c03690ac1a2080eca74f91e1d0c29c071d37761f9653f08ea2461` |

Caducidad: 22-11-2026. Los JSON no sustituyen ZIP/trazas/logs/binarios completos; mantener el archivo externo pendiente indicado en la [guía de relevo](README.md). La primera descarga local del ZIP Linux llegó incompleta y fue rechazada por tamaño; la segunda coincide con los 7.754.409 bytes y el hash de Actions. No fue un fallo del motor.

## Siguiente paso

Auditar y capturar las composiciones restantes (overlays, rutas GUI/16/Alt/Offset, minimapa y escenas), con destinos indexados identificados y orden explícito; después construir el estado completo y probar 0/1/N presentaciones entre ticks. Mantener cadencia y jugabilidad originales hasta completar ese contrato.
