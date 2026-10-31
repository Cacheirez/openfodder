# H4.1 — Recursos retenidos, paleta efectiva y planos

23 de octubre de 2026. Código: `ff82fb6049def3d784bc09a3a3c2d7fc685f4ea5` (resolución inicial `bd15a8a8` y corrección de coste por pasada). Continúa la auditoría [H4_1_RUTAS_Y_RECURSOS.md](H4_1_RUTAS_Y_RECURSOS.md). PR #1 abierto en borrador, sin fusionar; base clásica conservada.

## Cambio implementado

`ResolveSpriteResource` aplica el orden de la preparación clásica anterior a la encapsulación (`a2f63090`): publica la paleta de la tabla, llama al accessor original del backend y captura la **paleta efectiva** resultante junto al layout de planos. Las selecciones de cabecera, alturas especiales y escrituras de briefing siguen ejecutándose dentro de GetSpriteData. La consulta adicional de propietario no tiene esos efectos.

`ResolvedSpriteResource` reúne una copia inmutable de los bytes, offset del segmento/fotograma, extensión disponible, layout, paleta y número de generación local al caché. `PreparedSpriteDraw` mantiene juntos este propietario y la geometría preparada. La ruta de sprites lo transmite hasta `Video_Draw_8_Resolved`, que ya no consulta la cabecera activa para pintar. Los registros clásicos de fuente siguen apuntando al buffer original: no quedan apuntando a una copia temporal al terminar la llamada.

La diferencia de paleta detectada en la auditoría queda corregida en esta ruta: cuando el accessor Amiga sustituye la paleta de la tabla, se conserva su resultado. FONT usa 0xF0; RECRUIT/HILL, 0xD0; PSTUFF conserva las variantes especiales y la paleta de cursor. PC conserva la paleta de tabla. Se comparan los segmentos válidos de ambos backends con sus accessors originales, no con una tabla nueva de resultados esperados.

## Propiedad e inmutabilidad

El caché del productor construye `shared_ptr<const vector<uint8>>` a partir de una **copia privada**, no de un alias const del vector mutable del motor. Reutiliza esa copia mientras los bytes sean iguales. Si cambian bytes o tamaño, publica otra copia y generación; un comando anterior conserva la suya. La paleta y el layout se copian en cada resolución, aunque los bytes coincidan.

Fuera de una pasada explícita se compara el contenido en cada resolución, porque los cargadores clásicos pueden modificar el vector sin cambiar su dirección. En `Sprites_Draw`, `ReadOnlyBatch` permite comprobar cada segmento una sola vez por pasada; la siguiente pasada vuelve a comparar sus bytes. La paleta, el offset y los planos se siguen resolviendo en **cada llamada**, en su orden original, también con vídeo desactivado. El guard RAII termina el ámbito aunque se abandone por una excepción.

El contrato de ese ámbito exige no escribir ni sustituir los vectores fuente. La revisión del bucle confirma que `Sprite_CommitPendingDestroy` solo cambia campos de sprites y registros auxiliares; `Sprite_PrepareLegacyFrame` selecciona recursos y publica registros; los accessors cambian paleta/cabecera, pero no los bytes; el rasterizador escribe en `cSurface`, que asigna sus buffers por separado. No hay carga de imágenes ni callbacks dentro del bucle. El ámbito queda dentro del bloqueo `mSpriteMtx`; este bloqueo no se presenta como protección universal de los cargadores. Si se añade una escritura de imágenes al bucle, habrá que sacar esa escritura del ámbito o volver a validar el segmento.

Continúa existiendo un coste lineal por segmento y pasada, además de memoria para la última copia de cada segmento y las versiones retenidas. El número de generación identifica versiones de bytes dentro del caché; no es un identificador global de escena ni una garantía de publicación entre hilos.

El caché se usa desde el productor en la secuencia clásica. No protege frente a una escritura concurrente al vector mientras se captura. Los consumidores de comandos ya retenidos no necesitan volver al backend, a sus cabeceras ni a los bytes mutables. La vida útil dura hasta que desaparece el último propietario. Se rechaza un offset de fotograma fuera de la extensión; no se introduce aquí una validación universal de todas las lecturas del rasterizador sobre datos arbitrarios.

## Prueba focalizada

`tools/modernization/check_sprite_resource_equivalence.py` extrae los cuerpos originales de GetSpriteData PC/Amiga y Sprite_PrepareLegacyFrame de `a2f63090`, la resolución/preparación nueva y ambos llamadores Sprite_Draw_Frame. Los compila en un entorno mínimo de imágenes, ventana y motor.

**10.944 casos** (5.472 con captura individual y otros tantos con ámbito de pasada) cubren segmentos PC/Amiga válidos, cuatro variantes de selección de paleta Amiga, paletas de tabla, offsets, sprite visible/fuera de pantalla, fotograma inválido y vídeo activado/desactivado. Compara paleta efectiva, fuente original, geometría, visibilidad, registros y layout. Los llamadores reales se ejecutan para comprobar sus guardas y resultados de dibujo. El stub de dibujo clásico usa el núcleo que cuenta con su propia prueba independiente de equivalencia de píxeles; el dispatcher de recorte también usa el núcleo ya contrastado con los cuerpos originales. No es una ejecución de SDL ni de toda la interfaz.

Pruebas adicionales de retención:

- Resoluciones sin cambios reutilizan propietario y generación.
- Modificar un byte sin cambiar el tamaño produce una versión independiente.
- Cambiar solo los planos captura un layout nuevo sin alterar el retenido.
- Redimensionar, sustituir el recurso y destruir el backend no alteran los píxeles de un comando anterior.
- Resolver otra imagen entre preparar y dibujar no cambia la paleta/layout retenidos.
- Copiar y liberar comandos mantiene el recurso hasta el último propietario, comprobado con weak_ptr.
- Un offset al final del buffer se rechaza.
- Los cambios entre pasadas se detectan; offset, paleta y planos se actualizan dentro de una pasada. La salida normal y por excepción restaura la comprobación de las llamadas individuales.

La prueba se incorpora a Linux CI con ASan, UBSan y detección de fugas activada. Localmente ASan/UBSan aprobaron los casos; LeakSanitizer no pudo inspeccionar `/proc/.../task` en el entorno y terminó con error de infraestructura. Se repitió localmente con `detect_leaks=0`; CI conserva explícitamente `detect_leaks=1` y ha aprobado la prueba completa.

## Regresión y límites

Compilación Release local, 6/6 CTests, 13 tests Python, contrato de visibilidad, 306.432 casos de recorte y 29.160 casos de rasterización aprobados. Las primeras trazas H3 locales de PC y Amiga quedaron incompletas aunque las fases terminaron; se conserva el fallo y se repite la generación en un directorio temporal. La repetición local terminó con PC 7.956 estados, Amiga 3.405 y 11.361 estados coincidentes con el baseline original; 29/29 replays, cero omisiones y retorno 0. No se cambiaron fuentes del motor, referencias ni comparadores para aprobarla. La causa concreta de las trazas truncadas no está demostrada; se conserva como incidencia del primer intento.

Primer intento (`bd15a8a8`): [Windows 39863223248](https://github.com/Cacheirez/openfodder/actions/runs/39863223248) aprobó. [Linux 39863223234](https://github.com/Cacheirez/openfodder/actions/runs/39863223234) aprobó H3, equivalencias y ASan/UBSan/LSan, pero **falló por timeout de TSan a los 600 segundos**, con 17 fases completadas. El log conservado no contiene diagnósticos de TSan antes del corte; esa ejecución incompleta no cuenta como aprobación. La comparación de recursos se repetía para cada sprite y añadía un coste excesivo bajo instrumentación.

Corrección `ff82fb60`: validación de bytes por segmento y pasada read-only, sin saltarse preparación headless, sin desactivar instrumentación ni modificar el timeout o las referencias. Release local: 6/6 CTests, 10.944 casos ASan/UBSan, H3 original 11.361 estados y 29/29 replays (15,51 segundos, cero omisiones, retorno 0). Ese tiempo es una observación local, no un benchmark controlado. Ejecutable SHA-256: `50c42abfb2bdf14805efb12c47b7cb5d487d8ebb06a4b9d2ca28d5da2994309c`.

CI de la corrección: [Windows 39866081138](https://github.com/Cacheirez/openfodder/actions/runs/39866081138) y [Linux 39866081648](https://github.com/Cacheirez/openfodder/actions/runs/39866081648), **completas y satisfactorias** sobre `ff82fb60`.

| Verificación final | Resultado |
|---|---|
| Recursos / recorte / raster / temporizador | 10.944 / 306.432 / 29.160 / 184.320 casos aprobados |
| H3 Linux y Windows | 11.361 estados del baseline original, 7.956 PC y 3.405 Amiga |
| Replays Windows | 29/29, cero omisiones, retorno 0; 27,766 s |
| Motor Linux ASan/UBSan | 29/29, cero omisiones, retorno 0; 23,055 s |
| Motor Linux LSan | 29/29, cero omisiones, retorno 0; 22,805 s |
| Motor Linux TSan | 29/29, cero omisiones, retorno 0; 104,453 s, dentro del límite original de 600 s |

Los logs de los tres sanitizadores no contienen diagnósticos. Se han descargado los ZIP de evidencia, comprobado su CRC y leído los informes internos; las huellas coinciden con los digests de GitHub:

- Linux, artefacto `12464222206`: SHA-256 `50491c43bb628a509f456cf11a8edcdedf34781dd8d359599460ee16fb8509c8`.
- Windows, artefacto `12464357465`: SHA-256 `299d01fa8165ceed98e5db282395f69ec0f088b0f4780fe688e3e178f8c06356`.
- Primer intento Linux fallido, artefacto `12463717387`: SHA-256 `2ae2644030f7c7d48ba4aa6f41cd9c318c2148a61ae1b1ee64dcd1395c9d43ea`; conservado como evidencia del timeout, no como prueba aprobada.

Base recuperable verificada sin cambios: `baseline/classic-h2.6-2026-10-22` → `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`. PR #1 en borrador y sin fusionar. Los datos comerciales CD32 permanecen privados.

Esto resuelve la propiedad de comandos de sprites de esta ruta; no crea aún el estado de presentación completo. GUI, terreno, otros rasterizadores y escenas mantienen sus rutas clásicas. H3/replays siguen verificando simulación headless; los casos focalizados verifican píxeles sintéticos. No se declara validación visual completa CD32, un nuevo protocolo entre hilos ni seguridad 0/1/N del frame completo.

Siguiente bloque: capturar el terreno visible con sus tiles y atlas estables, preservando las escrituras/guardado del fondo en el adaptador; después HUD/cursor y demás rutas. Mantener la frecuencia de ejecución clásica hasta completar esos contratos.
