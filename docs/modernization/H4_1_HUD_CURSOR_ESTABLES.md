# H4.1 — HUD lateral y cursor con recursos propios

23-10-2026. Código `c6af094c49641018b6dea6dc77cbe731a7ea0218`; comparación original `7eeb6f777cc2ddfd9c615a2a94eef69bd3625c41`. PR #1 en borrador y sin fusionar, base H2.6 conservada.

## Decisión y frontera de captura

Se retiene el HUD lateral **ya compuesto** en `mSidebar_Screen_Buffer`. No se convierten decisiones de armas, munición, selección, temporizador o refresco en instrucciones que un presentador repita. `GUI_Element.cpp`, `Mouse.cpp`, las copias de sprites al sidebar y `Sidebar_Copy_ScreenBuffer_Common` quedan iguales a la base. Este último sigue avanzando el puntero pasado por referencia en su punto original.

La alternativa de reconstruir cada icono/texto al presentar obligaría a extraer ahora sus decisiones y efectos. Capturar el resultado indexado permite conservarlos y avanzar sin reejecutar composición lógica. Esto no migra toda la GUI: menús, texto directo sobre otras superficies, minimapa y escenas mantienen sus caminos clásicos.

## HUD retenido

[SidebarDraw.hpp](../../Source/Utils/SidebarDraw.hpp) define `SidebarDraw`: copia privada `shared_ptr<const vector<uint8_t>>`, número de filas, offset y stride de destino. `CaptureSidebarDraw` consulta el buffer y dimensiones activas; `CaptureSidebar` copia solo los bytes requeridos. No conserva punteros del motor ni escribe en él. `RasterizeSidebar` escribe exclusivamente el destino; su repetición no consulta flags, armas ni buffers vivos.

Se mantiene la geometría particular del original, incluso si `pSurface` es otro destino: **el ancho y alto usados siguen siendo los de mSurface**, no los del destino alternativo. No reinterpretar esta compatibilidad como adaptación automática de tamaño.

| Parámetro | PC | Amiga |
|---|---|---|
| Ancho copiado | 48 bytes por fila | 48 bytes por fila |
| Filas, con startY válido | `max(height - (17 + startY), 0)` | Igual |
| Offset fuente | 0 | `48 * startY` |
| Offset destino | `16 * activeWidth + 16` | `(16 + startY) * activeWidth + 16` |
| Stride destino | Ancho de la superficie activa | Igual |

En PC startY reduce la cantidad sin desplazar el inicio. En Amiga desplaza ambos inicios. La fila inferior que el original deja sin copiar permanece así. El destino y el buffer fuente deben contener los rangos clásicos; no se añade validación universal de geometrías inválidas. Para los usos soportados startY no es negativo. Un rango vacío no necesita propietario de píxeles. Esta copia añade asignación y bytes por captura; no se afirma neutralidad de coste.

## Cursor retenido sin repetir la selección

`cFodder::Mouse_DrawCursor` conserva exactamente: guarda `mParams->mDisableVideo` → coordenadas → `Mouse_CommitCursorRequest` → llamada al backend si existe. Con vídeo desactivado no consume la solicitud. Con backend nulo y vídeo activado sí mantiene coordenadas y consumo, como antes.

Cada backend expone `Cursor_PrepareLegacyDraw`: **es una coordinadora con efectos**, no una API pura para ejecutar a otra frecuencia. Conserva selección de tabla PSTUFF, escrituras de columnas/filas, cálculo del offset y accessor original. PC fuerza 0xF0 después del accessor; Amiga conserva su selección efectiva. Luego llama a `CaptureCursorDraw`, que lee esos registros y retiene bytes privados mediante el caché existente, junto con geometría, paleta y layout por valor. No llama de nuevo al accessor ni sustituye el puntero clásico de fuente por el de la copia.

`Mouse_DrawCursor` del backend entrega el resultado a `Video_Draw_8_Resolved`; este publica columnas/saltos en el punto de rasterización original. Para presentar repetidamente se debe usar el núcleo `RasterizeSprite8` con el comando retenido, **no volver a llamar a Cursor_PrepareLegacyDraw ni a Video_Draw_8_Resolved** (este último también escribe registros).

| Contrato de cursor | PC | Amiga |
|---|---|---|
| Columnas de preparación | `di->mColumns` | `di->mColumns >> 3` |
| Offset PSTUFF | `Y*160 + (X>>1)`, con conversiones clásicas int16/uint16 | `(Y & 0xFF)*40 + ((X>>3) & -2)`, con conversiones clásicas |
| Paleta | 0xF0 después del accessor | 0xE0 o byte bajo de mCursorPalette en Xmas/NotVeryFestive/AlienLevels |
| Planos | Nibbles PC | Layout de la cabecera seleccionada por el accessor, retenido antes de cualquier cambio posterior |
| Recorte | No se añade recorte al cursor | Tampoco; coordenadas/recursos válidos son precondición clásica |

El caché sigue siendo del productor serializado; no se añade publicación entre hilos. Un cambio de imagen o cabecera no altera un comando retenido. Tanto HUD como cursor producen índices: **no capturan todavía la paleta RGB ni el fade de la superficie**.

## Pruebas y límites

[check_hud_cursor_equivalence.py](../../tools/modernization/check_hud_cursor_equivalence.py) extrae los cuerpos originales y actuales. Comprueba que archivos de decisiones/composición y copias con efectos permanecen iguales a la base. Usa el coordinador real de solicitud de cursor y los accessors reales; las superficies/recursos son sintéticos. El raster de sprites tiene además su suite independiente contra cuerpos originales.

- 2.304 casos de cursor: PC/Amiga, cuatro variantes de versión, ocho descriptores sintéticos, tres solicitudes, vídeo on/off, tres posiciones y backend presente/nulo. Compara todos los píxeles, solicitud/índice actual, fuente original y registros. Incluye una Y de tabla superior a 255 para contrastar el enmascarado Amiga.
- 288 casos de HUD: offsets fuente PC/Amiga, cuatro alturas, tres anchos, seis startY y destino normal/alternativo. Compara todos los píxeles y ausencia de mutaciones al capturar; incluye rangos vacíos.
- Retención: mutar/redimensionar fuentes, cambiar cabecera/imagen, destruir productor, copiar/mover comandos y volver a pintar; weak_ptr verifica liberación al desaparecer el último propietario. Repetir el núcleo tres veces conserva píxeles sin repetir efectos.

Los guards estáticos de la prueba deben revisarse si en el futuro se modifica legítimamente GUI_Element/Mouse; no eliminarlos solo para que pase. H3 complementa esos guards con muestras lógicas, pero no prueba cada combinación de armas o cada pantalla comercial. No se declaran prueba SDL completa, equivalencia acústica, paleta RGB retenida, ni validación visual nueva de CD32.

## Resultados

Local: compilación Release, 6/6 CTests y contrato de visibilidad aprobados; 2.304 cursor + 288 HUD con ASan/UBSan (`detect_leaks=0` local). H3 original: 11.361 estados; 29/29 replays, cero omisiones y retorno 0, 15,976 s (no benchmark). SHA-256 del binario: `c97d39122462359a14932d5483146abd32cc90e42c618e2983fff0ce5d3f3727`.

CI: [Windows 39956418210](https://github.com/Cacheirez/openfodder/actions/runs/39956418210) y [Linux 39956418211](https://github.com/Cacheirez/openfodder/actions/runs/39956418211). Ambas aprobadas: 6/6 CTests y H3 original de 11.361 estados en Windows/Linux; Windows 29/29 replays (22,375 s), Linux ASan/UBSan, LSan y TSan 29/29 cada uno, sin omisiones ni diagnósticos en los registros examinados. La prueba focalizada pasa con fugas activas en Linux CI.

### Evidencia conservada

[Informes JSON originales](evidence/c6af094-reports.json), SHA de dependencias y resultado del examen de los 12 logs de artefactos conservados en Git. ZIP completos comprobados por CRC y SHA-256:

| Plataforma | Artefacto Actions | SHA-256 del ZIP |
|---|---|---|
| Linux | 12502599126 | `bb469c3bf5951f556e7a45cbbb154f25de96f3d5f40a7aeafd11c6d36cf2c205` |
| Windows | 12503191564 | `5a3e9300bd7a11467fa60c6b00fe7513239491b25e742b50d8f91aaccacdffce` |

Caducan el 22-11-2026; archivar ZIP completos y paquete Windows antes del relevo según [README](README.md). Los JSON no contienen todos los logs/trazas/binarios. La primera descarga local del ZIP Linux quedó incompleta y fue rechazada; la segunda tiene los 7.754.414 bytes esperados, CRC válido y hash coincidente con Actions. No fue un fallo del motor.

Tiempos de las pasadas Linux: ASan/UBSan 36,643 s, LSan 36,192 s, TSan 149,501 s, con límite original de 600 s; no son un benchmark comparativo. No se redujeron instrumentación ni compuertas. Los logs de ambos jobs confirman el baseline H3 original, además de las comparaciones entre repeticiones de los JSON.

## Próximo bloque

Capturar la paleta RGB efectiva y aclarar la propiedad de buffers/destinos de presentación, manteniendo avances de fade y Save/Restore en sus coordinadoras clásicas. Completar las rutas GUI/16/Alt/Offset/minimapa y escenas pendientes antes de declarar el frame íntegro y comprobar 0/1/N presentaciones entre ticks.
