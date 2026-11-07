# H4.1 — Productores GUI, minimapa y escenas

24-10-2026. Código/pruebas `d35e2675ffbbc79f8bf21eb961d78c06d74abd14` (motor introducido en `fa720cd`). Base de comparación `793e347cd9f118da1c9ec6a84f88caf3257b74c2`. PR #1 en borrador sin fusionar; baseline clásica intacta.

## Frontera elegida

[IndexedProducer.hpp](../../Source/Utils/IndexedProducer.hpp) retiene operaciones de píxel ya decodificadas: offset de destino, valor de índice y operación (sobrescritura u OR). El vector posee todos sus datos, se copia/mueve por valor y no conserva punteros a fuentes, cabeceras, paletas por fila, entidades ni superficies. `RasterizeIndexedProducer` solo aplica esas operaciones al destino suministrado.

Es una alternativa a retener cada formato fuente: las decisiones de formato, planos y paleta efectiva se resuelven durante la captura. Los recursos se leen exclusivamente en esa llamada; después pueden cambiar o destruirse. El resultado es un parche de píxeles, **no una imagen completa ni una paleta RGB**. Se necesita el destino inicial correcto y la captura RGB del mismo estado para componer una presentación coherente. Los offsets incluyen el stride capturado; no reutilizar con otra geometría.

Las coordinadoras clásicas conservan selección/accessors, clipping, registros, temporizadores y callbacks. La captura es pura respecto al motor; los adaptadores publican registros y escriben destino en su fase original. No llamar otra vez a la coordinadora GUI o de escena al repetir una presentación.

## Rutas adaptadas y particularidades

| Ruta | Captura / comportamiento conservado |
|---|---|
| GUI_Frame_8 y otras llamadas Video_Draw_8_Prepared | Datos de píxel propios, con paleta por fila PC resuelta al capturar; Amiga la ignora como antes. GUI_Element.cpp queda idéntico: accessor antes del clipping, LastHeight y coordenadas originales |
| GUI_Frame_16 / PC16 | Índices de 8 bits, cero transparente; fuente salta ColumnsMax-columns, destino width-columns. No usar el formato PC de nibbles de la ruta 8 |
| Amiga16 | Calcula salto fuente antes de dividir columnas entre dos; conserva el resultado con columnas impares, paleta y distancia entre planos height*40. Paleta por fila ignorada |
| Amiga Alt | Mantiene las comprobaciones de fila y X (incluido `X <= width`), y su avance de destino particular cuando una fila no se dibuja. No se convierte en un clipping nuevo |
| Amiga Offset | Giro horizontal dentro de width-32, base destino +16, fuente de 40 bytes/fila; máximo de cinco planos. No escribe registros de saltos/columnas |
| Minimapa PC | Copia 16×16 opaca, fuente stride 320; incluye cero |
| Minimapa Amiga | Cuatro planos BE16, OR sobre destino, offset de tile con conversión uint16; conserva el guard de fin del atlas y su avance |
| Capas helicóptero PC | Captura de las escrituras de los bucles masked/opaque, rotación de cuatro planos y retorno parcial por fin de fuente en masked; excepción de desplazamiento 320 explicada abajo |
| Helicóptero Amiga | Selección, número de frame, filas extra y clipping permanecen en Mission_Intro_DrawHelicopter; su Alt y las capas Offset producen órdenes propias |
| Service_Draw Amiga | Conserva elección Service/RankFont y GetHeader, paleta cero y registros; captura el bucle planar con stride fuente 40 |
| Load_And_Draw_Image PC | Captura la desintercalación de cuatro planos de bytes (320×200), incluyendo ceros. clearBuffer y PaletteLoad permanecen antes/después respectivamente; pBackColor sigue ignorado como en el original |
| Load_And_Draw_Image Amiga | Código intacto: carga/RAW/preprocesado, paleta y clearBuffer siguen clásicos; la ruta 16 captura antes de que la imagen local desaparezca y mBMHD_Current se ponga a cero |

**Precondiciones:** recursos y destinos con extensiones clásicas válidas; planos en el rango soportado; mapa con palabras completas y dimensiones compatibles. No se añaden validaciones universales de archivos o clipping seguro a rutas históricas. La prueba Alt usa almacenamiento con margen para comparar también sus desplazamientos peculiares; no afirma que X==width sea seguro con cualquier destino real.

## Constructor del minimapa

`CaptureOverviewPlan` copia IDs enmascarados con 0x1FF y posiciones centradas, usando la interpretación nativa de palabra del original. El cálculo de offsets conserva la diferencia entre dividir por dos cada dimensión y dividir su diferencia: no simplificar para tamaños impares.

`Map_Overview_Prepare` mantiene guarda unit-testing, eliminación/creación de superficie y clearBuffer. Publica left/top y captura las operaciones de tiles en orden; después aplica el conjunto al destino limpio. `CaptureOverviewTile` no escribe registros ni superficie. El origen del mapa y los atlas solo se leen durante la captura.

La fase de visualización del minimapa permanece sin cambios: paleta → Save → SetImage → contador/parpadeo y Restore → Video_Sleep → Restore final/SetImageOriginal. Los replays aún omiten la preparación del minimapa; la nueva prueba ejecuta el **cuerpo original y el actual** con recursos sintéticos y compara guardas, centrado, superficie y píxeles. No atribuirle validación visual comercial ni de toda la interacción.

## Corrección encontrada: seam PC de 320

La prueba ASan contra el cuerpo original reprodujo una lectura de `data[-1]` en HeliIntroBlit_OpaqueAlignedX con pCx=320: el primer tramo tiene cero grupos y el código decrementa Ds antes del segundo. Masked comparte ese esquema. Los llamadores calculan 320 menos el desplazamiento circular, por lo que ese límite puede alcanzarse.

Ambas capturas PC normalizan **solo pCx==320 a cero**. Es el mismo punto del ciclo de 320 píxeles; no se cambia la velocidad ni la posición lógica de las capas. Para 0–319 se compara contra el original en la misma posición. Para 320 se compara expresamente contra la ruta original válida de cero. No se afirma equivalencia de píxeles con la lectura indeterminada original. No se actualizan referencias H3 para aceptar este cambio.

## Efectos de escenas que no se repiten

Fodder.cpp, GUI_Element.cpp, Recruits.cpp y Window.cpp quedan idénticos. Se comprueban también los cuerpos Briefing_Intro_Helicopter_Play, Mission_Intro_DrawHelicopter y Recruit_Sprite_Draw de ambos backends. El escalado de reclutas **modifica el recurso HillSprites** y, en PC, sus registros de construcción: se conserva como producción de recurso en el punto original, no como instrucción de presentación repetible. Las capturas posteriores usan valores propios; nunca repetir ese preprocesado por cada frame presentado.

Callbacks, RNG, avances de escena, fades, Save/Restore, carga de imágenes y generación de recursos continúan en sus coordinadoras. Este bloque no declara que todos los efectos de escenas sean render puro ni los mueve a otro hilo. La GUI lateral compuesta conserva sus capturas previas.

## Pruebas

[check_indexed_producer_equivalence.py](../../tools/modernization/check_indexed_producer_equivalence.py): cuerpos originales y adaptadores actuales con motor/superficies sintéticos y ASan/UBSan. Compara todos los píxeles y registros relevantes, guardas de constructor, centrado, clear y selección de paleta en las rutas ejercitadas.

- 1.536 raster: PC16/Amiga16/Alt/Offset, planos 1/4/5/8, columnas pares/impares, filas vacías y bordes; Offset conserva límite de cinco planos.
- 1.964 escenas: todas las posiciones 0–320 de las dos capas PC, fuentes cortas masked, Service Amiga y carga PC; 320 usa la referencia explícita anterior.
- 1.024 tiles: 512 IDs en cada backend.
- 72 constructores de minimapa: dimensiones pares/impares, ambos formatos, guarda unit testing y datos truncados a palabras completas.
- Retención tras mutar/destruir fuentes, copia y repetición de operaciones; comparación de decisiones/llamadores que permanecen idénticos.

La suite anterior de raster (29.160) sigue comparando Video_Draw_8_Prepared, ahora con captura propia; HUD/cursor (2.304+288), capas (2.944) y superficie (27.648) permanecen. Los guards documentales por archivo se ajustan a las funciones realmente cambiadas: las nuevas pruebas comparan esos productores, y fade/Save/Restore siguen exigiendo sus llamadores intactos. No se eliminan casos ni instrumentación para hacer pasar el cambio.

La prueba es de datos/efectos, no de SDL/GPU/audio ni validación manual CD32. No mide todo el comportamiento de interacción de escenas. Los PNG conservan su ruta propia; no son un formato indexado nuevo.

## Coste y continuación

Las órdenes decodificadas ocupan más memoria que los datos comprimidos/planos; el minimapa completo puede generar muchas operaciones. No se presenta como optimización. No hay caché de alias mutable ni publicación concurrente. Antes de habilitar escenas/mapas mayores o nuevas cadencias se debe medir y, si hace falta, compactar comandos sin cambiar sus resultados.

Siguiente bloque: ensamblar por escena la lista ordenada de destinos, capas, paletas y generaciones, manteniendo aparte los efectos originales. Empezar con una ruta concreta y comprobar 0/1/N presentaciones, pausa y transición de recursos antes de declarar el estado completo para todas las escenas. Permanecen fuera de ese cierre PNG/renderer y validación visual de escenas comerciales.

## Resultados

Local: Release, 6/6 CTests, contrato de visibilidad, H3 original 11.361 estados y 29/29 replays, cero omisiones, retorno 0, 16,557 s. SHA-256 binario `51e3ce553a8bde4ee1520e938fabe546ac588bb2fba2bc6e4539a82806f29550`. Suites focalizadas locales con detect_leaks=0; CI requiere detect_leaks=1.

CI [Windows 40049116756](https://github.com/Cacheirez/openfodder/actions/runs/40049116756) y [Linux 40049116792](https://github.com/Cacheirez/openfodder/actions/runs/40049116792): ambas aprobadas. La revisión inicial fa720cd no incluía el ajuste del guard por archivo; d35e267 conserva el motor y compara las funciones de efectos sin excluir ningún llamador.


- Windows: 29/29 replays, cero omisiones, 23,688 s; H3 PC 7.956 + Amiga 3.405 y comparación original 11.361 estados PASS.
- Linux: todas las suites focalizadas PASS, incluida la nueva suite 1.536 raster + 1.964 escenas + 1.024 tiles + 72 constructores. H3 PC/Amiga y original PASS.
- Motor completo Linux: 29/29 fases en ASan/UBSan (36,232 s), LSan (36,284 s) y TSan (148,227 s), sin omisiones ni diagnósticos en los registros examinados. Instrumentación y límites de tiempo conservados.
- ZIP verificados por tamaño, SHA-256 y CRC; informes internos PASS. Escaneados 7 logs Linux y 5 Windows. [JSON originales y dependencias conservados en Git](evidence/d35e267-reports.json).

| Evidencia | Artefacto | SHA-256 | Caducidad UTC |
|---|---|---|---|
| Linux | 12542324925 | `359d650414bcd068d3f591f563df8961f4bcfdd876416e51c0b1d8cf786690ee` | 2026-11-23 01:28:22 |
| Windows | 12542324465 | `9943aaa788257fc6409a3d37bbd1abc7b76b795740ab52228ecebac3ebad35c6` | 2026-11-23 01:25:04 |

El JSON compacto no conserva trazas/logs completos ni binarios. El archivo duradero externo de los ZIP completos continúa pendiente; véase la guía de relevo. Esta validación automatizada usa demos públicas y fixtures sintéticos; no equivale a una nueva validación visual completa con datos comerciales CD32.
