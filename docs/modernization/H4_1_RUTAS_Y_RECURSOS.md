# H4.1 — Rutas pendientes y vida útil de recursos

Auditoría de código del 22-10-2026 sobre `a5a5cc42fee914a9c219c06985538d158a7e3f10` (motor `691cb0de`). Revisión estática previa al estado completo de presentación. No modifica el motor, los recursos del juego ni los momentos de ejecución. PR #1 en borrador, sin fusionar; base H2.6 conservada en `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`.

## 1. Resultado y decisión

El núcleo `RasterizeSprite8` ya puede consumir valores explícitos y escribir solo el destino. **Todavía no puede publicarse un frame completo independiente del motor**: la resolución de imágenes tiene efectos, faltan propietarios inmutables y varias rutas consumen registros, buffers y callbacks activos.

El siguiente bloque debe resolver conjuntamente **recurso, paleta efectiva y descripción de planos**, con un propietario estable, antes de extender comandos o añadir interpolación. Primero debe verificarse la diferencia de orden de paleta descrita abajo. No aumentar la frecuencia de las coordinadoras clásicas ni retirar sus escrituras por considerarlas meramente temporales.

## 2. Inventario de rutas

Los nombres identifican funciones concretas de la revisión auditada. «Pendiente» significa que la ruta no es reutilizable como presentación aislada; no implica que falle actualmente.

| Ruta y fuentes | Dependencias / efectos observados | Datos necesarios para separarla |
|---|---|---|
| Sprites: `Sprites_Draw`, `Sprite_PrepareLegacyFrame`, `Video_Draw_8_Prepared` ([Sprite_Core.cpp](../../Source/Sprites/Sprite_Core.cpp), [Graphics.cpp](../../Source/Graphics.cpp), [Fodder.cpp](../../Source/Fodder.cpp)) | Listas con punteros a entidades, retirada diferida, visibilidad y registros clásicos. El núcleo final ya está separado; la resolución todavía usa el backend activo | Orden de dibujo copiado, geometría y paleta efectiva por comando, recurso propietario y layout capturados juntos. Nunca guardar `sSprite*` |
| Terreno: `MapTiles_Draw`, `Map_Tile_Draw`, `MapOverview_Render_Tiles` ([PC](../../Source/PC/Graphics_PC.cpp), [Amiga](../../Source/Amiga/Graphics_Amiga.cpp)) | Lee mapa mutable, cámara, dimensiones globales y tiles. PC usa punteros `mTile_Gfx_Ptrs`; Amiga `mBlkData`. MapTiles_Draw guarda el fondo mediante `Save`; Amiga también limpia el destino | IDs de tiles visibles y cámara por valor, atlas propietario, reglas PC/Amiga, destino y fondo propios. Conservar el orden terreno → sprites |
| GUI/texto: `GUI_Draw_Frame_8/16` ([GUI_Element.cpp](../../Source/GUI_Element.cpp)) | Resolución con efectos y recorte global; Frame_8 actualiza `mGUI_Draw_LastHeight`. Frame_16 fija `mVideo_Draw_ColumnsMax` | Comandos 8/16 explícitos; altura lógica de texto actualizada una vez en su llamador. No trasladarla al render repetible |
| HUD: `GUI_Sidebar_*`, `Sidebar_Copy_*` ([GUI_Element.cpp](../../Source/GUI_Element.cpp), [Graphics.cpp](../../Source/Graphics.cpp)) | Estado de armas/munición y refresco, buffers sidebar mutables, registros de fuente/destino. Copy_ScreenBuffer avanza además el puntero pasado por referencia | Capturar el HUD ya resuelto o comandos propios; propietario del buffer y rectángulos. Mantener decisiones de armas y consumo de banderas en su punto clásico |
| Cursor: `Mouse_DrawCursor`, backends PC/Amiga | Solicitud de cursor ya separada, pero posición/tipo, PSTUFF, paleta y registros siguen activos. Amiga selecciona paleta especial según versión | Tipo, posición, recurso y paleta resueltos por tick; no volver a consumir solicitudes desde el presentador |
| Otros rasterizadores: `Video_Draw_16`, `Video_Draw_8_Alt`, `Video_Draw_16_Offset`, `DrawPixel`, `DrawPixels_8/16` | PC16 usa ColumnsMax y escribe saltos; Amiga16 transforma columnas y usa cabecera activa. Alt tiene sus propias comprobaciones de coordenadas; Offset envuelve horizontalmente. Los helpers de planos leen cabecera activa | Núcleos por formato con strides/planos/offsets explícitos y pruebas específicas; no asumir equivalencia con RasterizeSprite8 |
| Reclutamiento/servicio/briefing: `Recruit_Sprite_Draw`, `Recruit_Draw_HomeAway`, `Service_Draw`, `HeliIntro_BlitMaskedAlignedX`, `HeliIntroBlit_OpaqueAlignedX`, `Mission_Intro_DrawHelicopter` | Buffers temporales, imágenes especiales, columnas en unidades diferentes, callbacks, animaciones y paletas. Helicóptero Amiga usa Clip(true) y Video_Draw_8_Alt | Comandos y recursos por escena; separar avances de animación de su dibujo sin cambiar orden ni cadencia |
| Pausa/minimapa: `Phase_Paused` y rutas de overview ([Fodder.cpp](../../Source/Fodder.cpp), [MapRuntime.cpp](../../Source/Map/MapRuntime.cpp)) | Mezcla de superficies, paletas atenuadas y restauración. El minimapa se elimina y recrea; el mapa subyacente cambia | Modo de presentación explícito, contenido y paleta coherentes, recursos propios del modo; no retener el puntero de overview |
| Presentación final: `cSurface::draw/Save/Restore/copyFrom`, fades; `Video_SurfaceRender`, `Video_Sleep`, `cWindow` ([Surface.cpp](../../Source/Surface.cpp), [Window.cpp](../../Source/Window.cpp)) | Conversión indexada→RGB, textura SDL y destino mutable; Save/Restore escriben buffers; fade avanza paleta. Video_Sleep mezcla espera, eventos y restauración | Destinos propiedad del presentador y paleta resuelta del mismo tick. Fades, esperas, eventos y ticks no se repiten por cada presentación |

Además de la ruta de misión de `Interrupt_Redraw`, hay callbacks en `CampaignSelect.cpp`, `OptionsMenu.cpp`, `Recruits.cpp`, `Service.cpp`, `Fodder.cpp` y `Start_Emscripten.cpp`. No publicar estas lambdas: capturan el motor y algunas ejecutan cambios de escena, interfaz o paleta. La revisión no demuestra cobertura de todos los modos editor/bot/Emscripten.

## 3. Propiedad y operaciones que invalidan una vista

| Recurso | Propietario actual y evidencias | Riesgo para un estado retenido / decisión |
|---|---|---|
| Imágenes y hojas | `sImage::mData`, `tSharedBuffer = shared_ptr<vector<uint8>>` en [stdafx.hpp](../../Source/stdafx.hpp); imágenes alojadas en cGraphics | Copiar sImage comparte bytes mutables. Mantener shared_ptr evita liberar el vector, pero no evita escritura, resize o erase. Crear una versión congelada o copia privada; `shared_ptr<const vector>` solo no elimina otros alias mutables |
| Fuente de sprite | `sSpriteSheet::GetGraphicsPtr` ([SpriteSheet.cpp](../../Source/SpriteSheet.cpp)) devuelve `GetSpriteData(segment) + offset`; SpriteDrawState conserva un puntero prestado | No incluye propietario ni extensión. Registrar identidad/generación del recurso y offset validado; resolver puntero desde su propietario al consumirlo |
| Cabecera Amiga | `mBMHD_Current` apunta al miembro de un sImage; `GetHeader` inicializa su caché de dimensiones/planos | Se cambia al resolver otro segmento. RECRUIT/HILL cambian altura a 0x100/0x101. Copiar layout por valor en la misma resolución; no capturar solo el puntero |
| Imágenes locales | `Load_And_Draw_Image` usa un `sImage Decoded` local y deja `mBMHD_Current` a cero tras dibujar; también en Amiga2 | El puntero de cabecera no sobrevive a la función. Un comando diferido requiere propietario de datos y copia del layout antes de salir |
| Cargas/preprocesado | `Map_Load_Resources` y Load_* sustituyen imágenes; Load_Hill_Data Amiga hace resize; Load_Sprite_Font Amiga hace erase; PC Load_Hill_Data escribe ceros en los bytes | Publicar solo después de completar transformaciones. No modificar una versión que ya consume un frame; crear otra generación |
| Tiles PC | mTile_BaseBlk/mTile_SubBlk pertenecen al motor; `Tile_Prepare_Gfx` construye una tabla de punteros interiores | Conservar propietarios de ambos atlas y offsets; no retener la tabla de punteros actual al cambiar de tileset |
| Tiles Amiga | mBlkData, vector del backend, se redimensiona y rellena en `Tile_Prepare_Gfx` | Congelar la versión resultante; regenerar sin alterar versiones retenidas |
| Mapa | mMap comparte datos de mMapLoaded en MapRuntime; `MapTile_Set` y `Map_Destroy_Tiles` escriben sus bytes | Copiar los IDs/atributos visibles requeridos o versionar el mapa. Retener shared_ptr no congela destrucción de edificios/terreno |
| Sidebar y temporales | Buffers del motor; `mImageTemporary` se reserva en cGraphics y se utiliza en Recruits | Copiar contenido necesario al capturar o producir comandos; nunca prestar memoria que se reutiliza en la siguiente escena |
| Superficies y textura | cSurface posee arrays new[], SDL_Surface y SDL_Texture; destructor los libera. Backend mSurface/mImageOriginal son punteros; SetImage cambia destino activo | El presentador debe poseer sus destinos. No guardar cSurface* dentro de comandos de simulación ni reutilizar una textura tras destruir su renderer |
| Paletas | sImage contiene colores; cGraphics/cSurface mantienen paletas activas, objetivo y convertidas; fade y copyFrom las cambian | Capturar paleta efectiva por valor junto a los píxeles/comandos del mismo estado. No recalcular un fade al presentar otra vez |
| Metadatos de frames | Tablas estáticas, pero SetActiveSpriteSheet cambia tabla/conteos activos | Copiar el descriptor necesario después de validar índice; no conservar «índice + tabla actual» como resolución diferida |

`cResources::fileGet` obtiene un buffer de FileRead y puede descomprimirlo; no proporciona un contrato de caché inmutable. El cambio de versión en Fodder sustituye recursos/backend y recarga fuentes, hill y PSTUFF. La selección de fase sustituye mapa y atlas. Estas son fronteras de generación; los datos privados CD32 no necesitan copiarse al repositorio para establecerlas.

## 4. Hallazgo prioritario: orden y paleta efectiva

`GetSpriteData` no es una lectura pura en Amiga: escribe `mVideo_Draw_PaletteIndex`, cambia mBMHD_Current y, en segmentos de briefing, fija columnas/filas. `GetHeader` también puede inicializar campos. En PC el accessor devuelve los bytes sin esos efectos.

Hay una diferencia de contrato introducida al encapsular preparación:

- En `a2f63090`, Sprite_PrepareLegacyFrame escribe primero la paleta de la tabla y después llama a GetGraphicsPtr. Amiga puede sustituir esa paleta.
- En el código auditado se llama primero a GetGraphicsPtr y después se toma `SheetData->mPalleteIndex & 0xFF` para el comando y se publica su resultado.
- Ejemplo por inspección: una entrada FONT de SpriteData_Amiga.hpp contiene 10240 (byte bajo 0); GetSpriteData(eGFX_FONT) selecciona 0xF0. El contrato antiguo produciría 0xF0 y la preparación actual produciría 0 si se usa esa entrada en la ruta de sprites. RECRUIT/HILL seleccionan 0xD0.

Esto es una diferencia comprobada de orden en el código, **no una reproducción de un defecto visual en una misión**. GUI_Draw_Frame_8/16 mantiene su propio orden clásico y no debe confundirse con Sprite_PrepareLegacyFrame. La ruta normal in-game Amiga selecciona 0. Hace falta enumerar los segmentos realmente alcanzados por sprites y probar el resolvedor en ellos y en los casos de paleta especial antes de ampliar su uso.

Los 29.160 casos del rasterizador empiezan con una paleta ya suministrada; no prueban esta resolución. Los 306.432 casos de recorte tampoco. H3/replays son headless. Sus resultados siguen siendo válidos para su cobertura, pero **no cierran esta diferencia ni prueban equivalencia visual completa**. No construir el snapshot suponiendo que basta copiar la paleta de la tabla.

## 5. Contrato propuesto para el siguiente bloque (no implementado)

1. Resolver en el punto clásico un descriptor que reúna propietario de bytes congelados, tamaño, offset del segmento/frame, formato, layout y paleta efectiva. Conservar aparte los efectos del accessor en el adaptador y comprobar el orden respecto a preparación y recorte. El render no debe llamar GetGraphicsPtr/GetSpriteData.
2. Dar identidad y generación a los recursos. Completar carga/descompresión/preprocesado antes de publicar; si el original debe seguir mutando, copiar una versión privada. Retener la versión antigua hasta liberar el último estado que la usa. No asumir que un const aplicado a un alias vuelve inmutable el buffer.
3. Capturar por valor la cámara, orden de comandos, tiles visibles, HUD/cursor y paletas. No guardar entidades, cabeceras, buffers sidebar o callbacks vivos. Capturar el layout junto a la fuente, antes de resolver otra imagen.
4. Dar los buffers de destino al presentador. Mantener inicialmente un único hilo de presentación y la cadencia clásica. Una publicación entre hilos requerirá una entrega sincronizada del estado completo; el contador atómico de cadencia existente no es ese mecanismo.
5. Cambiar escena/fase mediante una generación nueva coherente. Un estado debe ser íntegramente de una generación, aunque todavía exista un consumidor de la anterior. No decidir ahora descartar estados que puedan corresponder a transiciones visibles.

`mSurfaceMtx` protege Interrupt_Redraw y varias operaciones de presentación; `mSpriteMtx` protege las listas en Sprites_Draw. No se ha demostrado que todas las cargas, sustituciones y escrituras de callbacks compartan un único protocolo de bloqueo. No ampliar el alcance de hilos hasta auditar las rutas de publicación y transición. TSan previo valida las rutas ejercitadas, no todas las escenas.

## 6. Orden de implementación y criterios de aceptación

| Orden | Trabajo | Evidencia necesaria |
|---|---|---|
| 1 | Resolvedor explícito de recurso/layout/paleta, con compatibilidad del orden clásico | Prueba con cuerpos originales que incluya efectos de GetSpriteData, paletas PC/Amiga y segmentos especiales; caso inválido y vídeo desactivado |
| 2 | Propiedad estable e inmutabilidad verificable | Retener estado A, cargar/sustituir/mutar recurso B y volver a dibujar A idéntico; comprobar fuente/offset/layout y liberación al desaparecer el último propietario |
| 3 | Terreno y HUD/cursor; luego 16/Alt/Offset y escenas restantes | Comparaciones de píxeles y escrituras clásicas para cada ruta; mapas modificados, bordes, transparencia, paletas y destino alternativo |
| 4 | Estado completo y presentación 0/1/N | Igual simulación, recursos y paletas coherentes, pausa/menús/minimapa/cambio de fase, destrucción/reutilización de sprites; H3 original, replays y sanitizadores |

Para sprites el núcleo repetible ya existe; falta conectar una resolución estable. No es necesario reescribir todos los rasterizadores antes de empezar ese primer bloque. La validación manual CD32 de H2.6 sigue aceptada; este documento no la repite ni la convierte en prueba de cambios posteriores.

## 7. Verificación de esta auditoría

Lectura de funciones, llamadas, campos propietarios y sitios de asignación/mutación en la revisión indicada; contraste del orden de preparación con `a2f63090`. Solo documentación: no se recompila ni se atribuye una nueva ejecución H3 a este commit. Último motor validado: `691cb0de`, Windows 39820699876 y Linux 39820699877. Las limitaciones y el hallazgo de resolución anteriores se añaden a esa evidencia; H4.1 sigue abierta.

## 8. Seguimiento — 23-10-2026

El bloque de resolución/propiedad de sprites se implementa en bd15a8a8: [H4_1_RECURSOS_ESTABLES.md](H4_1_RECURSOS_ESTABLES.md). Restaura el orden de paleta señalado en la sección 4 y captura copia privada, layout y paleta efectiva. La CI de la nueva revisión se documenta allí. El inventario de rutas pendientes y las limitaciones de publicación del frame completo siguen vigentes.


## 9. Terreno visible — 23-10-2026

`MapTiles_Draw` PC/Amiga consume una captura con tiles por valor y atlas privados e inmutables; conserva limpieza/guardado en el adaptador clásico. Código `7eeb6f7`; equivalencia, vida útil y resultados en [H4_1_TERRENO_ESTABLE.md](H4_1_TERRENO_ESTABLE.md). Las rutas de minimapa y tiles individuales, RGB/fades y HUD/cursor continúan pendientes de separación.


## 10. HUD lateral y cursor — 23-10-2026

Captura del sidebar compuesto y del cursor con recursos propietarios en `c6af094`; coordinadoras y efectos clásicos conservados. Véase [H4_1_HUD_CURSOR_ESTABLES.md](H4_1_HUD_CURSOR_ESTABLES.md). No equivale a separar cada función GUI ni las rutas RGB, fades, minimapa o rasterizadores restantes.


## 11. Seguimiento: conversión de superficies retenida

`ff15219` captura índices privados y paleta SDL efectiva por valor; cada conversión devuelve un destino RGB propio. [Contrato de paleta/destinos](H4_1_PALETA_DESTINOS.md) registra casos de paleta lógica/objetivo/aplicada divergentes, PNG excluido, Save/Restore y fades intactos, costes y límites. La composición de pausa sigue fondo → texto → merge; no se presenta una captura individual como frame completo. Próximo bloque: composiciones y destinos indexados restantes.


## 12. Seguimiento: capas y destinos indexados

`793e347` implementa capturas de capas, estado indexado con tres paletas y destinos independientes para copyFrom/mergeFrom/mergeSurfaceBuffer. [Informe](H4_1_CAPAS_DESTINOS_INDEXADOS.md) distingue copia opaca, transparencia por índice y por palabra RGB; mantiene orden de pausa/reclutamiento. Minimapa auditado, con exclusión de unit testing explícita. No se declara frame completo ni separación de todos los productores GUI/16/Alt/Offset/escenas.


## 13. Seguimiento: productores GUI/minimapa/escenas

`d35e267`: [informe](H4_1_PRODUCTORES_GUI_ESCENAS.md). Captura de operaciones decodificadas para las rutas GUI8/16/Alt/Offset, minimapa y productores de escenas indicados, con propiedad por valor. El constructor del minimapa tiene ahora pruebas sintéticas independientes; las decisiones de interacción siguen clásicas. Preprocesado de reclutas mantiene mutación de recursos una vez; no convertirlo en render repetible. Corrección explícita de lectura fuera de límites en seam PC 320. Próximo bloque: ensamblar por escena destinos, paletas y generaciones; frame completo/PNG/renderer/0-1-N aún no cerrados.


## 14. Primera escena ensamblada: pausa

`a133afb`: `PausePresentation` conserva fondo/texto, geometrías y paletas efectivas; `RasterizePausePresentation` devuelve destinos independientes sin consultar el motor. Fade, preparación, entrada y reanudación siguen fuera. Prueba de 144 planificaciones 0/1/5 con generaciones de recursos destruidas y dimensiones cambiadas. [Informe](H4_1_ESTADO_PAUSA.md). La subida SDL usa resultados finales; no se declara igualdad de número de subidas. Falta ensamblar y verificar frame de misión y transición misión↔pausa, además de validación GPU/PNG real/comercial.
