# H4.1 — Capas y destinos indexados propios

23-10-2026. Código `793e347cd9f118da1c9ec6a84f88caf3257b74c2`. Comparación contra `ff15219680b289abf207fdc23fc436a9f390e649`. PR #1 permanece en borrador sin fusionar. Base clásica H2.6 conservada.

## Decisión y API

[SurfaceLayers.hpp](../../Source/Utils/SurfaceLayers.hpp) añade `SurfaceLayer<Pixel>`: copia privada compartida const de píxeles y geometría/stride por valor. `MakeLayerTarget` crea un vector mutable **independiente** a partir de esa captura. `CompositeLayer` escribe solo ese destino, en el orden de invocación, sin consultar el motor. Índices y palabras RGB tienen tipos distintos; no se convierten implícitamente. El stride se expresa en elementos del tipo de píxel.

`cSurface::CaptureIndexedLayer`, `CaptureRGBLayer` y `CaptureIndexedState` son lecturas sin efectos. La última retiene además paleta actual, objetivo y efectiva para reproducir el contrato de copia de reclutamiento. No conserva superficie, textura, renderer ni punteros a memoria externa. Destruir o modificar productor/destino originales no afecta a una captura retenida. Copiar un destino copia su vector; copiar una captura comparte solo sus píxeles privados inmutables. Cada nueva presentación debe empezar con un destino nuevo desde la captura, sin acumular accidentalmente restos de la pasada anterior.

Los destinos indexados propios pueden recibir los núcleos existentes mediante `target.pixels.data()` y su stride, mientras el propietario permanezca vivo y su vector no se redimensione durante la llamada. Los adaptadores del motor mantienen sus destinos clásicos y publican el resultado de composición en el punto anterior. Esto resuelve la propiedad de las operaciones genéricas de copia/mezcla; no conecta todavía todos los comandos a un estado de presentación completo.

## Tres contratos, sin unificarlos como alfa

| Operación clásica | Fuente y destino | Regla conservada | Efectos conservados |
|---|---|---|---|
| copyFrom | Índices; origen debe cubrir al menos el tamaño del destino | Copia opaca, también cero; tamaño del destino | Copia paleta actual, objetivo y efectiva. No copia saved, adjusting, loaded flag, SDL ni textura |
| mergeFrom | Índices; mínimo de tamaños | Cero no escribe, los demás bytes sí, incluido 255 | No cambia ninguna paleta, saved, adjusting, SDL ni textura |
| mergeSurfaceBuffer | Palabras uint32 de SDL; mínimo de extensiones `height*pitch` | Palabra cero no escribe, cualquier otra sí; **incluye padding** | Una SDL_UpdateTexture al final si hay textura; no cambia índices, saved ni paletas |

Las mezclas son lineales: no alinean filas de anchos distintos, no escalan, no recortan por coordenadas y no interpretan alfa. `0xFF000000` es no cero y por tanto escribe, aunque represente negro en su formato. Cambiarlo por «RGB negro transparente» o mezclar índices antes de aplicar las paletas de cada capa rompería el contrato de pausa.

`copyFrom` deja de exigir que el núcleo lea más allá de una fuente corta: la función genérica compone el mínimo de tamaños y conserva la cola del destino. Las llamadas clásicas válidas siguen proporcionando fuente suficiente; la prueba de equivalencia se limita a ese dominio, porque la copia original con fuente corta tiene lectura fuera de límites. No se afirma equivalencia de entradas inválidas.

Los contratos de RGB requieren palabras de 32 bits y pitch divisible por cuatro, como las superficies indexadas convertidas de los llamadores actuales. No se extienden a PNG de 24 bits ni a conversiones de formato arbitrarias. `CaptureIndexedLayer` captura el almacenamiento indexado existente: tras LoadPng las dimensiones SDL pueden diferir de ese buffer; no usarlo como una representación indexada del PNG. La carga/propiedad STB sigue fuera de este bloque.

## Rutas inspeccionadas y orden

| Ruta | Secuencia y responsabilidad que permanece clásica | Captura disponible / pendiente |
|---|---|---|
| Pausa, Fodder.cpp::Phase_Paused | Fade del fondo si adjusting → draw fondo → draw texto con su paleta → mezcla RGB → RenderAt/FrameEnd → eventos | Mezcla ahora usa capturas RGB y destino propio; coordinadora intacta |
| Reclutamiento, Recruits.cpp | Copia inicial; callback dibuja camión/soldados/sidebar, home-away PC, cursor y fade antes de copyFrom | Copia indexada con tres paletas retenidas; callback y bloqueos intactos |
| mergeFrom | No se han encontrado llamadores actuales en Source | Adaptador y núcleo probados; no se presenta como ruta ejercitada por replays |
| Minimapa, MapRuntime.cpp y Phase_Map_Overview_Show | Preparación de tiles centrados; PaletteSetOverview → Save → SetImage → contador/parpadeo con draw o Restore → Video_Sleep; Restore final → SetImageOriginal | Superficie compuesta capturable; contador, entrada, atlas/tile builder y restauraciones siguen clásicos |
| Ventana | RenderAt recorta desde 16/16; RenderShrunk toma dimensiones completas; FrameEnd en coordinadora | Sin cambios; no se incluye renderer ni textura en las capturas |
| GUI/16/Alt/Offset y escenas | Siguen escribiendo por sus adaptadores/registros clásicos | Pueden producir la capa compuesta; sus comandos individuales aún no son todos independientes |

El minimapa se omite explícitamente cuando `mParams->mUnitTesting` está activo. Además las demos normales lo deshabilitan salvo excepciones de debug/custom. Por ello **H3/replays no validan visualmente su constructor ni su parpadeo**. Se conserva su código byte a byte; la captura genérica admite el buffer resultante, pero la separación de sus decisiones/tile builder requiere pruebas propias posteriores.

## Diferencias PC/Amiga

Los núcleos de mezcla de superficies son comunes. Sus fuentes no lo son: cada capa retiene sus colores efectivos tras la selección del backend. Amiga PaletteSetOverview aplica directamente la paleta objetivo; PC usa paletteSet con aplicación inmediata. En reclutamiento home-away se dibuja solo en PC en ese callback. Ninguna de estas decisiones se mueve al compositor. El orden pausa/reclutamiento y la exclusión del minimapa en pruebas quedan comprobados por guards sobre archivos originales, no por suponer equivalencia entre backends.

## Pruebas y límites

[check_surface_layers_equivalence.py](../../tools/modernization/check_surface_layers_equivalence.py) usa la declaración real de cSurface, cuerpos originales/actuales y almacenamiento SDL sintético con padding y centinelas. Compara 2.944 combinaciones de tamaños fuente/destino, padding, textura y operación; excluye fuentes cortas en copia opaca original. Verifica todos los píxeles y paletas, buffers guardados, flags y número de actualizaciones. Añade mezclas consigo misma, orden observable A→B frente B→A, repetición, destinos independientes, mutación/redimensionado/destrucción y liberación del último propietario.

Fodder.cpp, Recruits.cpp, MapRuntime.cpp, Window.cpp y ambos backends se comparan byte a byte con la base. draw, Save, Restore y fade siguen iguales. La antigua suite de superficie deja de exigir que copyFrom tenga idéntico cuerpo, porque ahora lo compara esta nueva suite; sus 27.648 casos de conversión permanecen. Hubo que añadir el nuevo include al harness anterior al incorporar la declaración de estado indexado; no se redujo su matriz.

Los recursos de prueba son sintéticos y el sink SDL contabiliza actualizaciones: no se atribuye equivalencia GPU, audio, PNG ni validación visual CD32. Nuevas copias/asignaciones tienen coste; no se afirma neutralidad de rendimiento ni se introduce publicación entre hilos. El productor debe permanecer serializado durante la captura, conforme a los bloqueos existentes. No es un protocolo nuevo de sincronización.

Local: Release, 6/6 CTests y contrato de visibilidad aprobados. 2.944 casos de capas y 27.648 de conversión de superficies con ASan/UBSan (`detect_leaks=0` local). H3 original 7.956 PC + 3.405 Amiga = 11.361 estados; 29/29 replays, cero omisiones, retorno 0, 16,044 s. Ejecutable SHA-256 `fd933647965731c56372f5e8a874e4164014177c0b4cd42efbf67cdb15babb1a`.

CI [Windows 40003012479](https://github.com/Cacheirez/openfodder/actions/runs/40003012479) y [Linux 40003012470](https://github.com/Cacheirez/openfodder/actions/runs/40003012470): aprobadas. H3 original de 11.361 estados en ambas; Windows 6/6 CTests y 29/29 replays, cero omisiones, retorno 0, 18,234 s. Linux 6/6 CTests, todas las suites focalizadas y ASan/UBSan, LSan y TSan con 29/29 cada uno, cero omisiones y sin diagnósticos en los logs examinados. Pasadas Linux: 35,189 s, 35,494 s y 143,989 s respectivamente, límite original de 600 s; tiempos informativos, no benchmark.

### Evidencia conservada

[Informes JSON originales, SHA de dependencias y examen de logs](evidence/793e347-reports.json) conservados en Git. Verificados tamaño, CRC y SHA-256 de los dos ZIP y examinados sus 12 logs; logs de jobs confirman el baseline H3 y las suites focalizadas.

| Plataforma | Artefacto | SHA-256 ZIP |
|---|---|---|
| Linux | 12522838801 | `8bed46e3240f9b209423f992855fcbe19696b3d1aaeca520f8d404439da66af5` |
| Windows | 12523062556 | `e9812df21d2bdfcf3512654c35cae92de701ca273e120fe1038531ee997231d6` |

Caducidad 22-11-2026. El archivo duradero externo de ZIP completos, trazas, logs y binarios sigue pendiente conforme a la [guía de relevo](README.md); estos JSON no los sustituyen. No se han publicado archivos comerciales CD32.

## Continuación

Falta separar y probar los productores específicos aún acoplados (GUI/16/Alt/Offset, constructor del minimapa y escenas), decidir la lista ordenada de destinos/capas por escena y sus generaciones. Después podrá construirse el estado completo y verificar 0/1/N presentaciones por tick, sin repetir decisiones ni efectos. No aumentar cadencia ni mover callbacks entre hilos en este bloque.
