# Auditoría técnica de sombras — OpenFodder

17 de noviembre de 2026. Fuente auditada: `cd4da48b6a2923f181407cd5fdba3f64657d4c2a`, rama `modernization/windows-foundation`. PR #1 consultada: abierta, borrador, sin fusionar y con ese mismo HEAD. Encargo de Miguel: inspección, pruebas focalizadas y documentación; **sin cambios del motor, arte ni nuevas fases**. Plan 2.74 vigente. La siguiente tarea operativa continúa siendo la captura manual de daño con `Probar-P1-Impacto.ps1`.

## Resultado ejecutivo y nivel de certeza

1. **VERIFICADO EN CÓDIGO:** no existe un sistema único de proyección de sombras. Hay sprites independientes de tipos 3, 22 y 35, auxiliares de vehículos/helicópteros y gráficos que pueden llevar sus detalles oscuros incorporados. El nombre `Player_Shadow` no restringe el tipo 22 al protagonista: también sirve a enemigos mediante la animación compartida.
2. **PROBADO TÉCNICAMENTE:** el compositor ordenado conserva las escrituras de `0x97/F1` entre cuerpos HD, con recorte y recuperación completa; el híbrido conserva F0 con procedencia nativa comprobada en su experimento acotado. Esto acredita operaciones concretas, **no conservación global ni aceptación visual**.
3. **Laguna observada en un replay real conservado:** tipo 3/`0x7E` F0–F3 y tipo 35/`0x8D/F1` quedan sin resolver. Provocan retorno íntegro al clásico; no se ha demostrado pérdida de esas sombras en una publicación parcial. Limita la continuidad HD y no debe esconderse como recurso transparente.
4. **PENDIENTE DE COMPROBACIÓN:** equivalencia de las sombras incorporadas a los sprites sustituidos, vínculo inequívoco cuerpo/sombra en registros, vuelo provocado por granada con trayectoria completa y CD32 comercial. No hay base para afirmar que todos los sprites HD actuales preservan la sombra original.
5. **PENDIENTE DE ACEPTACIÓN VISUAL:** coherencia entre cuerpos HD y sombras clásicas, especialmente al despegar, caer, morir y entrar en agua. Las recomendaciones de este informe no autorizan implementaciones.

## A. Mapa de código, datos y dibujo

Los enlaces señalan ficheros y líneas del HEAD auditado; los números pueden desplazarse con cambios posteriores.

| Responsabilidad | Fuente y punto de entrada | Hecho comprobado |
|---|---|---|
| Tipos, altura y propietario | [Sprites.hpp](../../Source/Sprites.hpp#L29), [reinicio](../../Source/Sprites.cpp#L801) | Tipos 3, 22 y 35 distintos; `mOwnerSprite`, altura/fracción y `mHasShadow` son estado del motor. `mHasShadow` no es prueba universal de una sombra dibujada. |
| Sombra de soldado | [crear](../../Source/Sprites/Sprite_Troop.cpp#L2084), [actualizar](../../Source/Sprites/Sprite_Troop.cpp#L623) | Sprite separado; propietario y copia de su tipo, altura cero, primer grupo de dibujo. Requiere `mWasDrawn` y slot libre. |
| Activación del soldado | [animación compartida](../../Source/Sprites/Sprite_Troop.cpp#L791), llamadas en líneas 143 y 486 | La creación de línea 851 está tras las salidas de estados especiales y el filtro `mAnimState`/`field_64`: no se ejecuta en toda marcha normal. Otra creación en línea 1557 pertenece a una rama de final de misión. |
| Sombra pequeña de proyectil | [actualizar](../../Source/Sprites/Sprite_Effects.cpp#L105), [granada](../../Source/Sprites/Sprite_Projectiles.cpp#L151) | Tipo 3; sigue al slot anterior, copia X/Y y `mRowsToSkip`. Granadas y varios misiles crean pareja con `0x7E`; altura de la sombra cero, grupo primero. Creaciones: líneas 112, 199, 285, 1453, 1593 y 1753. |
| Sombra genérica | [crear](../../Source/Sprites/Sprite_Effects.cpp#L625), [actualizar](../../Source/Sprites/Sprite_Effects.cpp#L377) | Tipo 35 con propietario, hoja `0x8D`, altura cero y grupo primero. Se destruye si el propietario pasa a explosión o tiene filas omitidas. |
| Objetos lanzados por explosión | [Sprite_Handle_Exploidable](../../Source/Sprites/Sprite_Core.cpp#L1838) | La rama de lanzamiento crea tipo 35 en línea 1922. Arbusto, árbol, tejado, muñeco de nieve y segundo arbusto llaman a esta rutina en líneas 986–1008; no demuestra una sombra independiente en reposo. |
| Vehículos | [Sprite_Shadow_Update_From_Height](../../Source/Sprites/Sprite_Core.cpp#L174), [vehículo](../../Source/Sprites/Sprite_Vehicle.cpp#L1165) | Actualiza `pSprite+1`, hoja `0x8D`; no usa necesariamente tipo 35. También participa en deslizamiento, línea 241 del núcleo. Los wrappers humanos pueden anular auxiliares con tipo Null; no generalizar a todo vehículo/estado. |
| Helicóptero | [auxiliares](../../Source/Sprites/Sprite_Helicopter.cpp#L809), [otra ruta](../../Source/Sprites/Sprite_Helicopter.cpp#L1009), [posición](../../Source/Sprites/Sprite_Core.cpp#L1243) | En la primera ruta el rotor ocupa `+1` y la sombra `+2`; en otra la sombra ocupa `+1`. Son contratos diferentes, no una pareja universal por adyacencia. |
| Orden | [Sprite_Sort_DrawList](../../Source/Sprites/Sprite_Core.cpp#L45) | Primero grupo First, después Second ordenado por Y y después Third; First conserva el recorrido de slots. Una sombra no se coloca automáticamente debajo de cada objeto cercano. |
| Proyección y captura | [adaptador](../../Source/Sprites/Sprite_Core.cpp#L96), [PrepareSpriteDraw](../../Source/Utils/SpriteDrawState.hpp#L209), [semántica](../../Source/Sprites/Sprite_Core.cpp#L2414) | Todos esos sprites pasan por geometría, cámara y recorte nativos. La captura guarda escena/slot/generación, tipo, hoja, frame y geometría; no guarda propietario ni tipo de relación. |
| Raster y secuencia | [Graphics.cpp](../../Source/Graphics.cpp#L240), [Surface.hpp](../../Source/Surface.hpp#L140) | El dibujo resuelto conserva bytes del recurso; se registra como operación Soldier aun cuando sea sombra/efecto. La palabra Soldier no significa cuerpo humano. |
| Resolución y publicación | [registro](../../Source/Utils/OrderedSoldierRegistry.hpp#L181), [contrato nativo](../../Source/Utils/ResolvedSpriteResource.hpp#L98), [WindowHD](../../Source/WindowHD.cpp#L85) | Resolución de cada comando antes de componer; faltante rechaza el intervalo completo. F0 nativo adicional está acotado al experimento de enemigos clásicos de M1P2 Amiga The One. |

### Recursos y ediciones

- `0x97`: Amiga `stru_8DB38`, [línea 762](../../Source/Amiga/SpriteData_Amiga.hpp#L762), F0 offset 2748, 3 filas; F1 offset 2750, 4 filas. Ambos segmento `eGFX_IN_GAME2`, columnas 2, modificadores (0,0): anchura útil Amiga8 de 16 píxeles. PC `stru_3478C`, [línea 1809](../../Source/PC/SpriteData_PC.hpp#L1809): offsets 10992/11000, 16 columnas y 3/4 filas.
- `0x8D`: Amiga `stru_8D8D8`, [línea 704](../../Source/Amiga/SpriteData_Amiga.hpp#L704): offsets 5304/5308/5588, columnas 3/2/2, filas 11/7/5. PC `stru_3452C`, [línea 1737](../../Source/PC/SpriteData_PC.hpp#L1737): offsets 21216/21232/22352, columnas 32/16/16 y las mismas filas. No intercambiar offsets o convenciones de columnas entre backends.
- `0x7E` es la hoja elegida para las sombras pequeñas por los creadores de proyectiles; los frames observados son F0–F3. Su raster y su ciclo requieren validación propia antes de conservarlos en HD.
- **VERIFICADO EN CÓDIGO:** CD32 figura como CF1/Amiga/Retail en [Versions.cpp:93](../../Source/Versions.cpp#L93). [Graphics_Amiga.cpp:441](../../Source/Amiga/Graphics_Amiga.cpp#L441) escoge tabla The One solo para esa demo y la tabla Amiga general para las demás versiones. Las funciones lógicas de sombra examinadas son compartidas; esto no verifica los bytes comerciales ni su apariencia.
- **PENDIENTE DE COMPROBACIÓN:** PC real, otros recursos Amiga y CD32 en juego. La igualdad de tablas o de fórmula no acredita paletas, empaquetado, entorno o campaña equivalentes. Ningún recurso comercial se añade al repositorio.

## B. Inventario por familia y estado

| Familia/estado | Representación confirmada | Límites de la clasificación |
|---|---|---|
| Aliado y enemigo, marcha/reposo/disparo/giro ordinarios | Sprite corporal por selector nativo; no hay creación incondicional de tipo 22 en esta ruta | La traza conserva 6.170 muestras normales de tipo 0 y 14.186 de tipo 5 con `has_shadow=0`. **No significa ausencia de sombra en los píxeles**. La muestra nativa 0/F1 inspeccionada tiene una extensión oscura inferior derecha incorporada al raster; su delimitación artística exacta y conservación HD quedan pendientes. |
| Aliado/enemigo en ramas de daño/muerte | Tipo 22 asociado mediante propietario, hoja `0x97` y frame según altura | Confirmado tanto por código compartido como por etiquetas del propietario en la traza. Hay salidas que evitan su creación; no afirmar que toda herida genera una sombra nueva. |
| Soldado lanzado, rebote y caída | Cuerpo con altura lógica; tipo 22 sigue X/Y con offset según altura, si existe | Trayectoria y eliminación verificadas en código. No se ha aislado en esta auditoría una granada concreta y la pareja completa en vídeo. |
| Soldado sumergido/nadando/muerto flotante | Filas omitidas y hojas propias; tipo 22 se destruye al aparecer `mRowsToSkip` | El cadáver flotante tipo 27/`0x9E` tiene contrato de cuerpo propio; no prueba sombra separada. Agua, estela y detalle oscuro embebido deben distinguirse. |
| Granada y varios misiles | Tipo 3 independiente en slot siguiente; `0x7E`, altura cero | Demostrado para creadores citados; el manejador solo sigue el slot anterior, no calcula iluminación. No extrapolar a la bala ordinaria ni a todos los efectos. |
| Helicóptero | Sombra independiente `0x8D` en auxiliar; rotor separado | Posiciones de auxiliares dependen de la ruta. Falta reproducción práctica de un helicóptero y su sombra en CD32/HD. |
| Vehículo terrestre/deslizamiento | Auxiliar `+1`, `0x8D`, actualizado desde altura cuando interviene esa rutina | Confirmado en ruta común; wrappers y estados pueden anularlo. Sombreado del propio vehículo no queda inventariado visualmente. |
| Árbol/arbusto/tejado/muñeco lanzado | Tipo 35 creado por rutina de objeto explosible | No acredita sombra separada del objeto quieto. Replay contiene tipo 35, pero sin propietario explícito no se identifica qué objeto lo originó. |
| Edificios y objetos estáticos no lanzados | No se ha encontrado un productor universal de sombra separado en las rutas auditadas | **PENDIENTE DE COMPROBACIÓN** por recurso: sombra embebida o ausencia. No etiquetar toda la familia como «sin sombra». |
| Terreno, balas, sangre, humo y demás efectos | Recursos/operaciones propios, sin exigencia universal de sombra | No se ha demostrado sombra para cada familia. Sombras pintadas en tiles quedarían dentro del raster de terreno; falta censo visual de esos recursos. El sombreado de botones GUI es otro dominio. |

La categoría «ausente» solo se puede asignar a un recurso/estado comprobado. La búsqueda por nombres de funciones no demuestra ausencia gráfica. Este inventario agota las rutas explícitas encontradas, no todos los píxeles y familias comerciales.

## C. Posición, vuelo, agua y oclusión

Sea `h=mHeight` del propietario. Son coordenadas lógicas enteras, antes del recorte; los desplazamientos de creación no deben confundirse con los actualizados en ticks posteriores.

| Ruta | Posición actualizada de la sombra | Frame/ocultación |
|---|---|---|
| Tipo 22 | `X=owner.X+(h>>2)+5`, `Y=owner.Y+(h>>2)-3`; altura sombra 0 | `0x97/F1` si `h<=8`, F0 si `h>8`. Se destruye al fallar identidad/copia del tipo del propietario, hoja `0x7C` o filas omitidas. Creación inicial: X+4, `0x8D/F2`. |
| Tipo 35 | Misma fórmula X/Y que tipo 22; altura 0 | `f=(h>>3)+1`; si `f>2`, vuelve a **1**, no a 2. Hoja `0x8D`; propietario invisible `0x7C` propaga invisibilidad. Creación inicial X+14/Y+16, F0. |
| Tipo 3 | X/Y del slot anterior; copia filas omitidas; altura inicial 0 | Hoja/frame preparados por la ruta de proyectil, no por este manejador. |
| Auxiliar común y primera ruta de helicóptero | `X=body.X+(h>>1)+9`, `Y=body.Y+(h>>1)-1` | `0x8D/min(h>>4,2)`; la rutina común usa hoja invisible cuando hay filas omitidas. |
| Otra ruta de helicóptero | `X=body.X+8+(h>>2)`, `Y=body.Y+(h>>2)` | El llamador selecciona hoja/frame; ajustador impone grupo First. |

**Proyección real:** `screenX=modX+X-mapX+xBias`; `rows=rowsNative-rowsToSkip`; `screenY=modY+Y-rows-height-mapY+16`. La diferencia visible cuerpo/sombra incorpora dimensiones, modificadores, altura y recortes. Por eso el −3 lógico no contradice una sombra percibida abajo a la derecha. En `0x97` Amiga F0/F1, con modificador Y cero y sin recorte, la diferencia entre bordes inferiores es `h+(h>>2)-3`; no usar esa cifra como desplazamiento universal de centros o pies. No hay dependencia directa de dirección en el manejador tipo 22, pero el cuerpo cambia de recurso/forma según la dirección.

**Explosión y altura:** [Sprite_Troop.cpp:1021](../../Source/Sprites/Sprite_Troop.cpp#L1021) integra `mHeightFixed` con `mFixedPoint`, rebota al cruzar el suelo, reduce impulso y velocidad; con agua/`field_50` y altura cero omite seis filas. Sí existe altura lógica, con fracción. La sombra de altura cero representa el plano del terreno, pero también se desplaza con X/Y y con h: no queda fija en el punto del lanzamiento. Los objetos explosibles usan otra integración y rebote ([núcleo:1862](../../Source/Sprites/Sprite_Core.cpp#L1862)), con comprobación de agua/borde/drop al aterrizar. No trasladar esa fórmula al soldado ni modificarla para ajustar arte.

**Agua y muerte:** tipo 22 y 35 pueden desaparecer por `mRowsToSkip`; tipo 3 hereda ese recorte. No hay en sus manejadores una proyección que busque una superficie receptora, un obstáculo o una dirección de luz. La interacción con terreno/agua viene de la lógica del propietario, selección de recursos y operaciones de dibujo. El paso a `0x7C`, cambio de tipo y destrucción tienen significado propio; no conservar una sombra por encima de esas decisiones.

**Transparencia, bordes y orden:** conservar exactamente las escrituras del productor nativo (`CaptureSprite8Producer`), no convertir todo índice cero en un alfa arbitrario ni inferir escritura por diferencia de color. Las operaciones posteriores borran las celdas HD que pisan, incluso con cero o el mismo color. Las sombras First preceden normalmente a cuerpos Second; la oclusión depende de la secuencia real, no de una capa inventada «sombras siempre abajo». [OrderedSoldierArt.hpp:63–103](../../Source/Utils/OrderedSoldierArt.hpp#L63) reproduce Pixels/Terrain/Soldier y Save/Restore de índices **y** celdas HD. El fondo se guarda antes de sprites en los dos backends ([PC:308](../../Source/PC/Graphics_PC.cpp#L308), [Amiga:777](../../Source/Amiga/Graphics_Amiga.cpp#L777)).

## D. Compatibilidad clásica, estricta e híbrida

- **Clásica:** utiliza el raster nativo completo y la secuencia original. No depende de que exista arte moderno. Es la recuperación de seguridad, no una aceptación visual de la mezcla.
- **Ordenada estricta:** exige resolución de todos los comandos. Puede conservar una sombra mediante vínculo exacto `keep-associated`; `0x97/F1` ya dispone de ese caso. «Estricto» no implica que todo píxel deba ser HD: hay asociados clásicos explícitos.
- **Híbrida:** añade contratos nativos acotados para determinados faltantes válidos. `0x97/F0` se admite como asociado en el experimento `classicEnemies`, limitado desde `WindowHD` a M1P2 de Amiga The One. F1 no obtiene por ello una exención genérica: depende de su vínculo exacto. Ni tipo 3/`0x7E` ni tipo 35/`0x8D` quedan admitidos universalmente por activar híbrido.
- **Conservación de orden y posición:** la sombra sigue siendo su comando y utiliza su geometría. Un HD posterior puede cubrirla igual que un cuerpo posterior en clásico. Hay PASS de composición, pero la silueta/alfa nuevos pueden ocultar más o menos sombra: requiere comparación visual.
- **Riesgo de eliminación incorporada:** reemplazar un sprite omite su raster clásico completo y mezcla el activo HD dentro del rectángulo nativo. Si la sombra estaba pintada en ese raster y el activo nuevo no la contiene, no hay un comando adicional que la recupere. No se ha cerrado esta comprobación para marcha y resto de poses.
- **Riesgo de duplicado:** un cuerpo HD con sombra pintada junto a tipo 22/3/35 u otro auxiliar conservaría ambas representaciones. Los prompts de algunas caídas/nado ya piden ausencia de sombra; eso no valida automáticamente todos los PNG ni todas las transiciones.
- **Identidad incompleta para diagnóstico:** escena/slot/generación identifica el dibujo, pero no su propietario. La clave de contenido excluye posición, slot, generación y reloj por diseño ([SoldierVariant.hpp:45](../../Source/Utils/SoldierVariant.hpp#L45)); no sirve como identidad de actor. `mAIAggression` del tipo 22 guarda el tipo del dueño, no su slot. No emparejar por cercanía visual ni por clave compartida.
- **Fallos reales:** procedencia inválida, geometría, bytes, presupuesto o SDL deben seguir rechazando con recuperación íntegra; el resultado `missing` tampoco autoriza omitir la sombra y publicar el resto. No se ha observado un fallo nuevo de composición en las pruebas ejecutadas.

## E. Contrato propuesto para modernizar una familia

Propuesta reutilizable, **sin autorización de implementación**:

1. **Declaración por recurso/estado y edición:** clasificar independiente, embebida, auxiliar derivado o ausente con evidencia de bytes/raster y llamadas. Registrar incertidumbre; ni `mHasShadow=0` ni hoja `0x97` bastan para toda una familia.
2. **Relación e identidad:** para una sombra independiente, conservar identidad propia (escena, slot, generación, orden) y documentar propietario con su identidad y rol. Para auxiliares adyacentes, registrar la convención concreta; para embebidas, registrar región y pertenencia al raster. Una eventual ampliación de captura sería solo presentación/diagnóstico y necesita autorización.
3. **Procedencia y ancla:** conservar versión, recurso/hash, segmento, hoja, frame, paleta, geometría y fórmula nativa. Escalar el dibujo con densidad; no introducir desplazamientos a ojo ni alterar altura, colisión, cámara lógica, RNG o tiempo.
4. **Secuencia:** una sombra independiente continúa como comando independiente. Preservar grupos y orden, transparencia, escrituras de cero/igual color, recorte y Save/Restore. No fusionar cuerpo y sombra ni añadirlos sobre una captura clásica final.
5. **Estados:** documentar creación, primer frame, vuelo, umbral de altura, rebote, desaparición/agua, muerte y reutilización/destrucción del slot. No inventar una sombra cuando el original la suprime.
6. **Sustitución:** HD válido para esa clave y densidad → sustituir ese comando; clásico válido sin HD → conservar solo mediante contrato permitido y verificable; error real → recuperar escena completa. Si la sombra es embebida, el activo sustituto debe preservar su función en ese mismo comando o requerir un diseño explícitamente aprobado, sin introducir otro dibujo por conveniencia.
7. **Coherencia estética:** cuerpo, sombra y suelo deben compartir estilo C y lectura de altura/volumen. Cuerpo HD con sombra clásica es provisional y debe constar en diagnóstico; no satisface por sí solo el producto final. Exigir revisión de Miguel de opacidad, bordes, tamaño aparente, apoyo y trayectoria antes de aceptar arte nuevo.
8. **Mínimo técnico antes de ampliar:** raster nativo de referencia; pareja protagonista/enemigo si procede; objeto no humano comprobado; vuelo con al menos despegue/cima/aterrizaje; agua; solapamiento en ambos órdenes y borde; Save/Restore si interviene; faltante/corrupto y error SDL con recuperación completa. Reutilizar fixtures existentes y sanitizadores pertinentes; no ejecutar matrices completas por cada informe.
9. **Aceptación separada:** PASS técnico acredita las operaciones ejercitadas; replay acredita los estados que realmente contiene; aceptación visual/jugable corresponde a Miguel. CD32, GPU y casos no reproducidos se marcan pendientes, sin extrapolar desde la demo Amiga.

No se justifica introducir iluminación, shaders ni un nuevo sistema físico de sombras. La prioridad es comprender los píxeles ya sustituidos y reutilizar los comandos originales.

## F. Evidencias ejecutadas y límites

Resumen y hashes: [evidencia documental](evidence/auditoria-sombras-20261117.json). Carpeta local de recuperación: `C:/Users/migue/.codex/visualizations/2026/11/17/01a1ea7b-b727-78f2-a6ac-a4b32dc39150/`. Solo se publican métricas y documentos, sin recursos originales ni capturas privadas.

| Comprobación | Tipo de evidencia | Resultado y límite |
|---|---|---|
| Mapa, fórmulas, altura, orden y selección PC/Amiga/CD32 | VERIFICADO EN CÓDIGO | HEAD indicado. No es una reproducción de CD32. |
| `0x97/F1` real reconstruido, entre cuerpos HD | PROBADO TÉCNICAMENTE, fixture actual compilado con MSVC C++14 y SDL 3.4.0 software/dummy | PASS 8×/12×: 24 escrituras; una pisa HD anterior, 22 quedan bajo el cuerpo posterior, dos visibles; recorte a 12 escrituras; clave ausente recupera clásico completo. Sin sanitizadores nuevos en esta ejecución. Antecedente sanitizado en [auditoría F1](DEMO_A1_AUDITORIA_SOMBRA_97_F1.md). |
| `0x97/F0`, procedencia, errores y Save/Restore | PROBADO TÉCNICAMENTE, fixture WindowHD actual con `OPENFODDER_TEST_ORDERED_HYBRID=1` | PASS 8×/12×, dos actores HD y asociados clásicos. Los bytes de este caso genérico son controlados: prueba contrato/operaciones, no apariencia nativa del F0. Incluye recuperación SDL y rechazos de procedencia. |
| Protagonista/enemigo normal | Reanálisis de traza de replay público real conservado + inspección de una imagen nativa | 6.170/14.186 muestras con animación 0 y `has_shadow=0`; no demuestra ausencia de sombra embebida. Se inspeccionó `impacto-marcha-0-1-0c5d8496/native-local.png`, 0/F1 con animación 1 y raster equivalente a marcha; no se acepta visualmente la pareja HD. |
| Sombra asociada de aliado/enemigo | Reanálisis de traza real | 587 muestras tipo 22: etiqueta del tipo del propietario 0 en 124 y 5 en 463. Confirma uso de ambos tipos; no identifica el dueño individual. |
| Sombras `0x97` en publicación HD | Reanálisis de log real, cruzando COMMAND y RESULT por intento | F0: 393 comandos keep, 297 en intentos publicados; F1: 1.347 keep, 879 publicados. Son comandos, no actores únicos ni frames lógicos. |
| Objeto no humano con sombra | Código + comandos de replay real conservado | Tipo 3/`0x7E`: 162/12/12/24 comandos missing en F0/F1/F2/F3. Tipo 35/`0x8D/F1`: 17 missing. Ninguno aparece en intento HD publicado. Identidad concreta del objeto tipo 35 y valoración visual pendientes. |
| Soldado despedido por granada | Código de animación/altura y tipo 22 en replay | **PENDIENTE DE COMPROBACIÓN** de causa y trayectoria de la pareja en reproducción visual. La traza existente no exporta altura ni propietario. No atribuir todas las sombras observadas a explosión. |
| Oclusión sombra/cuerpo y terreno | Fixture F1 con escrituras nativas y fixture híbrido con capas controladas | PASS técnico en ambos sentidos y recorte; pendiente escena real representativa validada visualmente. |

El replay no se vuelve a ejecutar: se analiza el log de `impacto-probe-replay/classic-enemies/engine.log`, SHA-256 `37b083aefb9c6c56a6ff1eb11dd76e325312649ffd03d072c0b1dc0ad9d03fe8`, y su traza retenida en la carpeta de trabajo del 16-11 citada en [continuidad del prototipo](DEMO_A1_HYBRID_P1.md#prueba-diagnóstica-de-daño-del-pelotón). Esto no se presenta como replay nuevo de este bloque. H3 completo, CI, GPU, audio, nuevos sanitizadores y campaña comercial **no ejecutados en esta auditoría documental**; no hay cambio del motor que justifique repetir su matriz.

### Recuperación y reproducción focalizada

1. Generar `shadow-fixture.cpp` con `python -B tools/modernization/build_hd_window_fixture.py --emit <carpeta-local>/shadow-fixture.cpp` desde el checkout auditado. Compilar contra Source/tools actuales y SDL3; receta MSVC equivalente en la recuperación de [F1](DEMO_A1_AUDITORIA_SOMBRA_97_F1.md#reproducción-de-la-integración). Usar rutas de salida locales y no modificar fixtures históricos.
2. Compilación con `OPENFODDER_EXTERNAL_ASSET_FIXTURE`, `SDL_VIDEODRIVER=dummy`, `SDL_AUDIODRIVER=dummy` y `OPENFODDER_A1_RANK_F4` apuntando al `enemy-input.json` de la recuperación F1: `shadow-run.log`. Otra compilación sin ese define y con `OPENFODDER_TEST_ORDERED_HYBRID=1`: `hybrid-run.log`. No se necesita reconstruir SDL/LLVM.
3. `audit_shadow_logs.py`, conservado en la carpeta local de esta auditoría, analiza exclusivamente COMMAND/RESULT y la traza JSONL retenida; produce `shadow-replay-summary.json`. Los hashes de script, fixture, ejecutables y logs se incluyen en la evidencia publicada. El JSON no contiene sprites ni bytes gráficos.

**Captura humana pendiente, sin cambiar la siguiente tarea:** usar `Probar-P1-Impacto.ps1` según el plan y facilitar log/carpeta de capturas que muestra el lanzador. Como observación adicional, anotar aliado/enemigo, instante del daño y si hay vuelo; si es posible guardar vídeo local con despegue, punto alto, aterrizaje y paso junto a un obstáculo. Los snapshots de ese diagnóstico se limitan a dibujos de jugador en hojas 0–7: no garantizan capturar la sombra ni la pose aérea. Si faltan esos datos, proponer una captura de pareja acotada, **sin modificar ahora el diagnóstico**. Para CD32 hace falta la instalación privada de Miguel y una comparación clásica/híbrida de la misma situación; no subir datos comerciales. La validación de sombras no reemplaza la captura de las tres claves de impacto.

## G. Próximos pasos y autorización

| Prioridad/ID | Objetivo y resultado esperado | Dependencia | Estado |
|---|---|---|---|
| 1 · IMPACTO-CAPTURA, siguiente operativa vigente | Miguel entrega log/capturas de daño M1P2; permite resolver las tres claves pendientes. Anotar observaciones de sombra si aparecen. | Acción humana con lanzador existente | **AUTORIZADO**, pendiente de Miguel. |
| 2 · SOMBRAS-RASTER, recomendación | Comparar raster clásico/activo HD de una marcha aliada y enemiga, quieto/disparo y caída; delimitar sombras embebidas, pérdida o duplicado antes de crear más familias. Informe de diferencias, sin arte nuevo. | Referencias nativas y activos actuales | **PROPUESTO; REQUIERE APROBACIÓN** como siguiente auditoría acotada. |
| 3 · SOMBRAS-PAREJA, recomendación | Si la captura existente resulta insuficiente, especificar diagnóstico de propietario/rol/altura y caso de vuelo con granada; obtener evidencia inequívoca. | Captura de Miguel y resultado del paso 2 | **PROPUESTO; REQUIERE APROBACIÓN** para cualquier cambio de captura. |
| 4 · SOMBRAS-CONTRATO-NATIVO, recomendación | Auditar claves reales de `0x7E` y `0x8D` por estado/edición y medir continuidad; decidir si merece ampliar conservación clásica verificable. No admitir toda la familia de golpe. | Recursos y propietario identificados; beneficio medido | **PROPUESTO; REQUIERE APROBACIÓN** para implementación. |
| 5 · SOMBRAS-REVISION, recomendación | Revisar con Miguel cuerpo/sombra/suelo, vuelo, agua y oclusión; contrastar CD32 privado cuando esté disponible. Resultado: aceptación o ajustes explícitos por caso. | Parejas comprobadas; revisión humana | **PROPUESTO; REQUIERE APROBACIÓN** para arte o nuevas familias. |

**Siguiente acción única de mayor valor dentro del plan:** obtener la captura de daño de Miguel. No necesita nueva autorización y evita producir variantes sin geometría comprobada. La siguiente recomendación propia de sombras es SOMBRAS-RASTER, porque las sombras embebidas no quedan protegidas por conservar `0x97`; requiere aprobación específica. No iniciar recomendaciones automáticamente. Ampliar matrices o construir otro sistema de sombras antes de esa comparación tendría coste desproporcionado.

**Cierre:** auditoría documental completada con lagunas explícitas; hito de continuidad híbrida sigue pendiente de revisión jugable, no aceptado globalmente. Sin cambios de motor/arte ni referencias; siguiente tarea del plan intacta. Escalado de modelo: NO. Nuevo hilo: no necesario por esta auditoría; decisión de implementación pendiente. La publicación documental no autoriza B, escenarios, scroll, 16:9 ni nueva producción visual.
