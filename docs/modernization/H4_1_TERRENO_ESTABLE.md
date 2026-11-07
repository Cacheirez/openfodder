# H4.1 — Terreno visible y atlas con propiedad estable

23 de octubre de 2026. Revisión de código: `7eeb6f777cc2ddfd9c615a2a94eef69bd3625c41`. Continúa [H4_1_RECURSOS_ESTABLES.md](H4_1_RECURSOS_ESTABLES.md). PR #1 en borrador, sin fusionar; base clásica H2.6 conservada.

## Implementación y alcance

`CaptureVisibleTerrain` produce un `TerrainDraw` con formato PC/Amiga, comandos por valor (tile normalizado, posición de destino y recortes X/Y) y atlas propietarios. Incluye las filas/columnas extra del bucle original, no solo el rectángulo aparente de la ventana. No guarda punteros al mapa, motor, cabeceras ni superficies. La cámara queda resuelta en los tiles seleccionados y su geometría.

PC conserva copias privadas de los dos atlas base/sub; el offset de cada tile reproduce la tabla construida por `Tile_Prepare_Gfx`. Amiga conserva una copia del atlas concatenado y preparado `mBlkData`. `TerrainAtlasCache` compara contenidos una vez por atlas y captura, detectando cambios dentro del mismo vector; comparte la copia inmutable si coincide. Si cambian los bytes, los comandos anteriores conservan su versión. No hay alias mutable a esas copias. El caché pertenece al productor y requiere la serialización clásica; no incorpora un protocolo de publicación entre hilos.

`PrepareTerrain` lee el mapa y devuelve datos por valor. La lectura usa índices con signo para evitar formar punteros anteriores al buffer. Conserva el comportamiento de omitir filas anteriores al mapa y detener las lecturas al alcanzar su final; los mapas válidos contienen palabras completas. El límite de ID sigue siendo 0x1DF en PC y 0x1C0 en Amiga; IDs superiores se convierten en tile 0.

`RasterizeTerrain` consume exclusivamente esos datos y el destino. PC copia filas indexadas de 16 píxeles con stride 320. Amiga conserva la expansión de cuatro planos, incluido el avance y la posición de destino peculiares del primer tile recortado. No se corrigen esas peculiaridades visuales en este cambio. Los atlas truncados no se leen fuera de su extensión; esta protección no atribuye equivalencia al comportamiento indefinido del código anterior sobre recursos malformados. El destino debe poder contener el rectángulo clásico y los recortes deben estar entre 0 y 15.

Los adaptadores `MapTiles_Draw` mantienen sus llamadas y cadencia:

- PC: capturar → rasterizar → `Save`, una vez.
- Amiga: `clearBuffer` → capturar → rasterizar → `Save`, una vez.

`clearBuffer` sigue limpiando píxeles, fondo guardado y superficie SDL en su punto clásico. El núcleo Amiga también inicializa los píxeles del destino para que una presentación repetida sea independiente de su contenido anterior; no llama a SDL, `Save` ni al motor. `Save` permanece después del terreno y antes de los sprites. La guarda de vídeo de `Interrupt_Redraw` no se modifica.

Se trata del terreno indexado de `MapTiles_Draw`. Las paletas RGB, fades, minimapa/overview, `Map_Tile_Draw`, HUD/cursor y otras escenas siguen sus rutas clásicas. No se publica aún un frame completo ni se aumenta la frecuencia de ejecución. Los datos privados CD32 no se publican ni se modifican.

## Equivalencia y vida útil

`check_terrain_equivalence.py` extrae de `ff82fb60` los cuerpos reales PC/Amiga de `MapTiles_Draw` y la preparación de la tabla PC; los compara con los adaptadores y capturadores nuevos. La superficie de prueba registra limpieza y guardado, y conserva el fondo; no reproduce SDL.

7.680 casos cubren ambos formatos, los 256 pares de recorte (0–15), tres tamaños de vista y cinco posiciones del mapa, incluidos su final y una fila parcial. Los atlas y mapas sintéticos contienen patrones variados, ambos bancos PC, atributos e IDs de los 512 valores posibles. Se comparan todos los píxeles, el fondo guardado, el orden/número de efectos y los registros de cámara. La captura por sí sola no modifica la superficie. El núcleo se repite tres veces y conserva el resultado.

Las pruebas adicionales retienen comandos, editan mapa y atlas, redimensionan buffers, destruyen el productor y copian/mueven el comando. Verifican la reutilización de copias sin cambios, nuevas copias al modificar bytes, dibujo retenido idéntico y liberación tras el último propietario. Una prueba aparte cubre el origen negativo del mapa sin ejecutar aritmética de punteros inválida del original.

La prueba se ejecuta en CI con ASan/UBSan y detección de fugas activa. H3 y los replays verifican simulación y finalización; no sustituyen esta comparación de píxeles ni una validación visual completa de CD32.

## Resultados

Compilación Release local y 6/6 CTests aprobados. Los 7.680 casos focalizados pasan con ASan/UBSan (`detect_leaks=0` local; CI exige `detect_leaks=1`). H3 conserva 11.361 estados del baseline original, PC 7.956 y Amiga 3.405. Los 29 replays locales terminan sin omisiones y con retorno 0 (40,855 s; observación local, no benchmark). SHA-256 del ejecutable: `6b23b3c36957e96411a9bd1b0af6de6fadb4c942906b80cb5e0485f828e1a581`.

CI: [Windows 39919649274](https://github.com/Cacheirez/openfodder/actions/runs/39919649274) aprobada; [Linux 39919649308](https://github.com/Cacheirez/openfodder/actions/runs/39919649308) aprobada sobre el mismo código `7eeb6f7`.

Windows: H3 original 11.361 estados y 29/29 replays, cero omisiones, retorno 0 (20,062 s). ZIP de evidencia `12486123605` descargado, CRC correcto e informes internos verificados. SHA-256 coincidente con GitHub: `04dc479848924c5618c6e97751afec4fb6ae4ccd1721f646f69d5bd3fa071601`.

Linux: 7.680 casos de terreno con ASan/UBSan y fugas activas aprobados; también pasan 10.944 casos de recursos de sprites, 29.160 de rasterización, 306.432 de recorte y 184.320 transiciones de temporizador. H3 original: 11.361 estados.

| Diagnóstico del motor Linux | Fases | Omisiones / retorno | Tiempo observado |
|---|---|---|---|
| ASan/UBSan | 29/29 | 0 / 0 | 30,772 s |
| LSan | 29/29 | 0 / 0 | 30,822 s |
| TSan | 29/29 | 0 / 0 | 209,160 s |

Sin diagnósticos en los logs examinados; no se modifican los límites ni las referencias de las pruebas. ZIP Linux `12487286837` descargado, CRC correcto e informes internos verificados; SHA-256 coincidente con GitHub: `6127b72ff5c93329299dda4ea3115947dd05ecf1270c3c5c4969b34ef3aa6077`. Los tiempos no constituyen un benchmark controlado. La captura añade comparación lineal de atlas y memoria para copias retenidas; no se declara neutralidad de rendimiento.

Base recuperable verificada: `baseline/classic-h2.6-2026-10-22` → `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`, intacta. PR #1 abierto en borrador y sin fusionar. No se atribuye una nueva prueba manual CD32 a esta revisión.

## Próximo bloque

Capturar HUD y cursor con datos y recursos propios, conservando decisiones, consumo de banderas y efectos en sus coordinadoras clásicas. Después completar las rutas restantes y verificar el estado de presentación completo antes de cambiar la cadencia.
