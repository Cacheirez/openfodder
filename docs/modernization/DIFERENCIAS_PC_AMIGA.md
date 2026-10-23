# Diferencias PC/Amiga y contratos de compatibilidad

Revisión: 23-10-2026, motor `ff15219680b289abf207fdc23fc436a9f390e649`. Registro de diferencias **comprobadas en las rutas analizadas**, no catálogo exhaustivo de todas las versiones del juego. PC/Amiga identifica el formato/backend de los datos; ambos se ejecutan en el anfitrión Windows o Linux. CD32 es la fuente comercial prioritaria, no un tercer sistema operativo del motor.

## Matriz de dibujo

| Contrato | PC | Amiga | Evidencia / decisión |
|---|---|---|---|
| Sprite 8 | Dos índices de cuatro bits por byte, primero nibble alto; fila fuente de 160 bytes | Bits separados por planos; cada byte expande ocho píxeles; distancia de planos `height * 40` | [SpriteRaster.hpp](../../Source/Utils/SpriteRaster.hpp); 29.160 casos, conservar formato |
| Transparencia del sprite | Nibble cero no escribe; índice no cero OR paleta | Resultado cero de planos no escribe; no cero OR paleta | No sustituir por copia opaca |
| Registros antes de rasterizar | Columnas `columns >> 1`; salto fuente `160 - columnsRaster`; salto destino con conversión a uint16 | Columnas `(columns - 1) * 2`; salto fuente `(width >> 3) - columnsRaster`; salto destino `targetWidth - columnsRaster * 8` | Conservar unidades y conversiones; no equiparar columnas entre formatos |
| Paleta por fila | El núcleo PC admite tabla por Y | La ruta Amiga8 no la usa | Contrato del rasterizador; el comando de sprite retenido actual no solicita esa tabla |
| Recorte/visibilidad | Reglas PC | Reglas Amiga8/16 diferentes | [SpriteDrawState.hpp](../../Source/Utils/SpriteDrawState.hpp), 306.432 casos; no normalizar fórmulas sin comparación original |
| Resolución de sprite | GetSpriteData conserva paleta de tabla | GetSpriteData puede sustituir paleta, seleccionar cabecera y escribir dimensiones | Orden obligatorio: paleta de tabla → accessor → captura de paleta/layout efectivos |
| Propiedad original | Hojas en vectores compartidos mutables | Además cabecera activa mutable y buffers preprocesados | Copia privada inmutable; un shared_ptr const de un vector con alias mutable no basta |
| Terreno: IDs del mapa | LE16, máscara 0x1FF; ID > 0x1DF pasa a cero | LE16, máscara 0x1FF; ID > 0x1C0 pasa a cero | Valores límite distintos deliberadamente conservados |
| Atlas de terreno | Base/sub: IDs 0–239 / 240–479, 20 tiles por fila; offset local `(id/20)*5120+(id%20)*16`; stride 320 | Atlas concatenado, offset `id*128`, cuatro planos de palabras big-endian | [TerrainDraw.hpp](../../Source/Utils/TerrainDraw.hpp); 7.680 casos |
| Fondo del terreno | Copia incluso el índice cero; conserva lo no escrito del destino | Limpia destino completo y expande planos mediante OR | No tratar el cero del terreno como transparencia de sprite |
| Efectos de terreno | Captura → raster → Save | clearBuffer → captura → raster → Save | clearBuffer limpia también fondo guardado y SDL; no repetir efectos desde el núcleo puro |
| Recorte de terreno inicial | Fuente avanza `startY*320`, copia desde `startX` al comienzo del destino | Fuente empieza `id*128 + startY*2`; consume `16-startY` filas por plano **sin saltar el resto del plano**; desplaza bits por startX y escribe en `tile.x + x` para x desde startX | Peculiaridad reproducida, no corregida. Véase fórmula abajo |
| Tiles extra / borde | Bucles inclusivos hasta rows+1 y columns+1 | Igual número de iteraciones; salida del mapa usa break en el bucle interno | Capturar también margen extra; no reinterpretar como solo viewport visible |

En el primer tile Amiga, con `sy=startY`, la palabra de la fila r del plano p se lee desde `id*128 + 2*sy + 2*(p*(16-sy)+(r-sy))`. No reemplazarla automáticamente por `id*128 + p*32 + 2*r`: para sy distinto de cero no es equivalente al código clásico. El índice destino horizontal incluye startX, mientras el siguiente tile avanza solo `16-startX`. Ambas peculiaridades están preservadas por la prueba contra cuerpos originales.

## Selección de recursos de sprites

Fuente: `GetSpriteData` y `GetSpriteResourceStorage` en [PC](../../Source/PC/Graphics_PC.cpp) y [Amiga](../../Source/Amiga/Graphics_Amiga.cpp). Esta tabla describe la ruta de resolución, no toda la GUI.

| Segmento | PC | Amiga: recurso y paleta efectiva / efectos |
|---|---|---|
| IN_GAME / IN_GAME2 / RANKFONT | Hoja correspondiente, paleta de tabla | Hoja correspondiente, paleta 0, cabecera activa seleccionada |
| FONT | mImageFonts, paleta de tabla | mImageFonts, 0xF0 |
| PSTUFF | mImagePStuff, paleta de tabla | 0xE0; Xmas, NotVeryFestive y AlienLevels usan byte bajo de mCursorPalette |
| RECRUIT | mImageRecruit | mImageHillBackground, 0xD0; altura de cabecera 0x100 |
| HILL | mImageHillSprites | mImageHillSprites, 0xD0; altura 0x101 |
| SERVICE | mImageService | No es un segmento válido de este accessor |
| BRIEFING | No es un segmento válido de este accessor | mImageMissionIntro + 0; 0xA0; columnas 0x28, filas 64 |
| BRIEFING_AMIGA_1 | No válido | mImageMissionIntro + 176*40; 0xB0; columnas 0x28, filas 74 |
| BRIEFING_AMIGA_2 | No válido | mImageMissionIntro + 65*40; 0xC0; columnas 0x28, filas 111 |
| BRIEFING_AMIGA_3 | No válido | mImageMissionIntro + 252*40; 0xD0; columnas 0x28, filas 48 |

Los segmentos válidos Amiga seleccionan cabecera. La consulta adicional del propietario no debe repetir esos efectos. Se captura la cabecera por valor antes de seleccionar otra imagen. La paleta efectiva aquí es el valor utilizado para formar **índices**, no una copia de la paleta RGB completa de la superficie. Los fades/RGB necesitan su propia captura futura.

## Cambios y peculiaridades que no deben confundirse

- Se corrigió el orden de paleta introducido durante la encapsulación: se recuperó el accessor como autoridad final, contrastado con `a2f63090`. No era una justificación para unificar las paletas PC/Amiga.
- Se preservan las particularidades de terreno Amiga indicadas arriba. Una mejora visual posterior debe ser un cambio explícito, separado de la equivalencia clásica.
- La nueva captura rechaza lecturas sin dos bytes disponibles; no se promete equivalencia con accesos fuera de rango del código antiguo sobre archivos malformados.
- H3 verifica estado lógico, no color, audio ni percepción visual. Los fixtures sintéticos de raster verifican píxeles indexados, no toda una sesión SDL/CD32.

## Diferencias aún no cerradas

El inventario [H4_1_RUTAS_Y_RECURSOS.md](H4_1_RUTAS_Y_RECURSOS.md) localiza GUI 8/16, HUD, cursor, 16/Alt/Offset, reclutamiento/servicio/briefing, helicóptero, minimapa, fades y callbacks. HUD lateral compuesto y cursor tienen captura y pruebas propias descritas abajo. El conjunto restante no tiene todavía una matriz exhaustiva ni todas sus pruebas independientes. Tampoco se declara cobertura completa de Amiga2/Cannon Fodder 2, editor, bot, Emscripten, audio por versión ni todas las fases comerciales CD32.

Para cada nueva ruta se debe añadir: función/commit original, campos leídos y escritos, unidades/endian/layout, propietario y mutaciones, regla PC/Amiga, excepciones por versión, prueba diferencial y limitación. Una celda desconocida debe decir «pendiente de analizar», no extrapolarse desde otra ruta.


## HUD lateral y cursor — actualización 23-10-2026

Código `c6af094`: [contratos, fórmulas y pruebas](H4_1_HUD_CURSOR_ESTABLES.md). El sidebar compuesto se retiene con 48 bytes por fila. PC startY solo reduce el número de filas; Amiga desplaza además fuente y destino. Ambas rutas usan dimensiones de la superficie activa incluso con destino alternativo. El cursor PC fuerza paleta 0xF0 tras el accessor; Amiga conserva la paleta efectiva PSTUFF y el layout. Se mantiene la guarda de vídeo antes de consumir solicitudes. Esta actualización cierra la captura de estas rutas; no la composición interna de toda la GUI, RGB/fades ni el frame completo.


## Paleta efectiva y destino RGB — actualización 23-10-2026

Código `ff15219`: [detalle y prueba](H4_1_PALETA_DESTINOS.md). Capturar mPaletteSDL (tabla aplicada), no deducirla de mPalette/mPaletteNew. PC carga canales por byte y Amiga expande nibbles; se mantiene la conversión RGB existente. Son 255 entradas: índice 0 no escribe y 255 produce negro. Save/Restore solo afectan a índices, no a paletas. El destino RGB tiene vector propio; las composiciones de capas y destinos indexados completos siguen pendientes. Inicialización nueva de tabla efectiva a negro antes de aplicar una paleta; se explicita el estado previamente indeterminado.
