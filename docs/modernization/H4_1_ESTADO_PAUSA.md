# H4.1 — Estado de presentación de la pausa

24-10-2026. Código `a133afb8188a26f51e703b7a81576cf1b9264f67`; referencia anterior `d35e2675ffbbc79f8bf21eb961d78c06d74abd14`. PR #1 en borrador sin fusionar. La rama clásica `baseline/classic-h2.6-2026-10-22` permanece en `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`.

## Alcance y decisión

Primera escena ensamblada: pausa, con fondo y texto superpuesto. `PausePresentation` contiene ambos destinos de origen, sus geometrías/strides, índices y tablas RGB efectivas, además de los bytes RGB necesarios para superficies ya cargadas y padding. No retiene punteros a entidades, cSurface, SDL, cabeceras ni recursos del motor. Cada captura representa una generación completa y autónoma; no necesita un contador global de generaciones.

Se elige pausa porque delimita la composición y permite aislar los efectos de fade, entrada y salida sin modificar el paso de misión. No se cambia la frecuencia de ejecución ni se añade una cola/hilo de presentación. El runtime sigue presentando una vez por iteración.

## Orden de ejecución

`cFodder::Phase_Paused` conserva su cuerpo salvo el bloque de conversión/mezcla:

1. `Draw_Phase_Paused` prepara una vez texto, recursos, paletas y registros, como antes. Su dibujo inicial y la selección/restauración de imagen y sheet siguen intactos.
2. En cada iteración, comprobar `isPaletteAdjusting` y ejecutar el fade original si corresponde.
3. Capturar fondo y texto con `cSurface::CapturePresentation`. Es una lectura sin efectos; la tabla capturada es la RGB aplicada, no la paleta objetivo del fade.
4. `RasterizePausePresentation` produce dos destinos privados y compone texto sobre fondo. Esta operación puede omitirse o repetirse sin acceso al motor.
5. `ApplyPresentation` copia los resultados a los buffers RGB/texture del adaptador; `RenderAt`, `FrameEnd`, `Cycle`, eventos y delay siguen en su lugar.
6. Al salir: `PaletteSet`, `palette_SetFromNew`, `surfaceSetToPalette`, reset de `mPhase_Aborted`, terreno, sprites y sidebar conservan su orden original.

La publicación SDL se reduce de las subidas intermedias fondo/texto/fondo compuesto a una subida de cada resultado final. Ningún RenderAt se situaba entre las subidas anteriores. La cantidad de actualizaciones de textura no se declara idéntica; los píxeles presentados y los efectos lógicos sí se comparan. No mover el fade al rasterizador ni repetir la preparación del texto al repetir la presentación.

## Contratos de píxel y propiedad

| Elemento | Contrato conservado |
|---|---|
| Fondo y texto indexados | Cada capa usa su propia paleta RGB efectiva y skip inicial 16/16 |
| Índice cero y 255 | Conversión original: cero deja destino negro; 255 no tiene entrada en la tabla de 255 colores y queda negro |
| Mezcla de pausa | Omite la palabra RGB cero, no el índice cero ni el alfa; incluye padding y usa mínimo de tamaños |
| Destino con pitch | Primero borrar ancho visible de cada fila; después copiar width*height palabras empaquetadas, reproduciendo el recorrido clásico incluso con padding |
| Imagen cargada | `CaptureDraw` vacío; se retienen los píxeles RGB existentes, como draw que no convierte PNG |
| Captura retenida | Vectores privados const compartidos entre copias del estado; tabla/geométrica por valor; no aliases mutables al motor |
| Salida | Dos vectores mutables independientes, sin alias con el estado ni otras rasterizaciones |

PC y Amiga llegan a esta composición después de sus productores específicos: no se reinterpretan planos Amiga como índices PC. La escena común conserva las paletas ya resueltas. El camino RGB cargado se prueba sintéticamente; no equivale a validar el decoder PNG real ni un renderer/GPU.

`ApplyPresentation` es un sink de presentación, no parte del núcleo puro. Requiere el mismo tamaño/pitch que el destino capturado; el bucle lo aplica inmediatamente antes de procesar eventos. Una captura antigua se puede rasterizar tras sustituir/destruir sus fuentes, pero no se debe copiar su resultado a un cSurface nuevo de geometría distinta. Para una futura cola de publicación hay que validar generaciones/geometrías o crear un destino SDL propio; no reutilizar a ciegas ese adaptador.

## Pruebas y límites

`python tools/modernization/check_pause_presentation.py` compila con C++14 y ASan/UBSan cuerpos reales de Phase_Paused anterior/actual y métodos actuales de cSurface. El módulo `pause_contract.py` fija la única sustitución permitida; las suites anteriores siguen comparando el resto de Fodder.cpp completo, incluidos todos los llamadores de fade/Save/Restore. No se ha quitado el archivo de sus guardas.

**144 escenarios de planificación**: 3 anchos × 2 altos × 2 paddings × 4 combinaciones indexado/RGB × 0/1/5 presentaciones. Cada uno recorre seis iteraciones y dos cambios de recursos. Los cambios destruyen ambas superficies y sustituyen dimensiones, bytes, paletas y tipo indexado/RGB. Se comprueban:

- Píxeles del bucle original frente al bucle integrado actual, con una presentación.
- Estado de índices, Save, paletas current/next/effective, indicador de fade, flags de pausa/aborto y llamadas de entrada/eventos/salida idénticos con 0/1/5.
- Cada salida repetida coincide con el frame original correspondiente; ninguna presentación cuando N=0 durante el bucle.
- Capturas de generaciones anteriores copiadas y rasterizadas después de destruir todas las superficies; salida mutable independiente y repetición idéntica.
- Se conserva el paso de reanudación y sus llamadas en el orden original.

Los loaders de recursos, preparación de texto, gráficos de reanudación, entrada, delay y SDL son dobles controlados de prueba. El cuerpo real de `Draw_Phase_Paused` y las restantes coordinadoras se protegen por comparación de código, no se ejecutan en este harness. La traza local observa campos/efectos de pausa; no sustituye H3 del motor completo. Los replays H3 no ejercitan pausa interactiva. Por ello no se atribuye a esta prueba cobertura de toda la misión ni de todas las combinaciones comerciales PC/Amiga/CD32.

## Resultados

Local: 144 escenarios ASan/UBSan PASS; suites de capas 2.944, superficie 27.648 y productores 1.536+1.964+1.024+72 PASS. Release y 6/6 CTests PASS. Contrato de visibilidad PASS. H3 PC 7.956 + Amiga 3.405 y baseline original 11.361 estados PASS. Replays 29/29, cero omisiones, retorno 0, 21,841 s.

SHA-256 binario local: `91bd7362d2cae6aad2883010491405ebba6c3383aacab3ccd06f986d47b6f9d7`.

Las primeras ejecuciones locales de las suites anteriores encontraron la limitación del host para LeakSanitizer (`/proc`/ptrace), no un diagnóstico de fuga. Se repitieron con `detect_leaks=0`; ASan/UBSan siguen activos. La CI mantiene `detect_leaks=1`, instrumentación y límites anteriores.

CI [Linux 40082228491](https://github.com/Cacheirez/openfodder/actions/runs/40082228491) y [Windows 40082228351](https://github.com/Cacheirez/openfodder/actions/runs/40082228351): ambas aprobadas.


- Linux: suite de pausa y todas las equivalencias anteriores PASS con detect_leaks=1. H3 original 11.361 estados PASS. Motor completo 29/29 fases con ASan/UBSan (20,855 s), LSan (20,901 s) y TSan (74,051 s), sin omisiones ni diagnósticos en los logs examinados.
- Windows: compilación, 29/29 replays (24,047 s), H3 PC 7.956 y Amiga 3.405, comparación original 11.361 estados PASS.
- Ambos ZIP de evidencia verificados por tamaño, SHA-256 y CRC. Informes internos PASS; escaneados 7 logs Linux y 5 Windows. [Informes originales, dependencias y líneas de resultado de los jobs conservados en Git](evidence/a133afb-reports.json).

| Evidencia | Artefacto | SHA-256 | Caducidad UTC |
|---|---|---|---|
| Linux | 12555837595 | `11930c50b3332830c394fb53d40bb869687c2396e920b38c2b489e6afa4f90ed` | 2026-11-23 09:37:53 |
| Windows | 12555213147 | `e1a550e1e23c38e1df9584f206e97d15e5aa236386abde71f7ee6c8ac1182ca1` | 2026-11-23 09:37:22 |

El archivo compacto no incluye trazas/logs completos ni ejecutables; el archivo duradero externo de los ZIP sigue pendiente, como explica la guía de relevo.

## Coste y continuación

Se copian índices y backing RGB de ambas capas en cada captura, más las salidas de cada rasterización. Es una separación de propiedad y efectos, no una optimización; no se ha medido la reducción/aumento de coste. Compactar o almacenar solamente padding en la ruta indexada será una optimización posterior con pruebas equivalentes.

Siguiente bloque: ensamblar una captura completa del frame de misión (terreno, sprites, HUD y cursor), tomando la pausa como primer contrato probado. Añadir pruebas 0/1/N del motor en esa ruta, con cambios de recursos y transición misión↔pausa. Todavía no cerrar H4.1 global, introducir interpolación/HD ni cambiar cadencias. Falta validar publicación SDL/GPU, PNG real y escenas comerciales visualmente.
