# Contraste nativo de marcha — 5 de noviembre de 2026

Bloque A1/A3 del plan 2.74. Resuelve la carencia de píxeles/paletas tras el censo de hashes: verifica los fotogramas nativos y prueba las vinculaciones diagonales con los recursos reales, sin reasignar las claves a recursos sintéticos. **No completa las otras 21 poses artísticas ni la sustitución del soldado.**

## Resultado

- Replays públicos PC Format y Amiga The One: 112 instantáneas únicas de cuerpo, 56 por plataforma. Incluyen las 24 claves ordinarias de marcha por plataforma, dos recursos por plataforma y estados que reutilizan esas hojas. No son 112 imágenes nuevas ni cobertura de CD32.
- Cada instantánea conserva recurso inmutable y paleta RGB efectiva. La reconstrucción comprueba SHA-256 del recurso y recalcula la clave completa antes de rasterizar con el núcleo original existente. No se reconstruye una imagen a partir del nombre de la hoja ni se aprueba un hash por coincidencia nominal.
- Las 13 vinculaciones diagonales anteriores se reprodujeron con sus bytes y paletas reales. **12 son marcha ordinaria; la restante es `Slide1` (`mAnimState=0x32`)**, que reutiliza 7/2 en un recurso PC. Se clasifica y prueba aparte, conservando su estado original; no se suma como otra clave de marcha.
- Método real Window/SDL con ASan/UBSan: cuatro grupos reales de recurso/paleta con ciclo 0–1–2–1, más Slide1 separado, a 8×/12×. 34 intervalos, 68 cuerpos, 26 combinaciones clave/densidad. Dos soldados, agua y oclusión. C01 idéntico byte a byte. Las claves se recalculan de los recursos reales; no se sustituyen por claves de fixture.
- Revisión visual interna de las 24 claves nativas y del ciclo diagonal frente a sus originales. Orientación, tres índices y alternancia general se contrastan; el estilo C y C01 se conservan. No implica reproducción píxel a píxel de la anatomía, aprobación de las otras cinco poses ni aceptación de Miguel. Paletas/recursos probados limitados a estas demos.

[Informe, hashes y límites](evidence/soldier-native-walk-validation.json). Las 13 vinculaciones siguen siendo candidatas artísticas; su identidad y publicación aislada quedan verificadas. El intervalo de campaña completo sigue retornando coherentemente al clásico si faltan otras claves. El lanzador no cambia y no se entrega ZIP.

## Reproducción local

Los PNG nativos, bytes originales, instantáneas de paleta y HTML comparativo **no se suben a GitHub**, tampoco si se repite el proceso con datos comerciales. Guardarlos fuera del árbol versionado. Solo publicar el informe de hashes y las trazas de diagnóstico sin píxeles. El ejecutable de diagnóstico no se distribuye.

1. Preparar las dependencias y demos fijadas de [DESARROLLO.md](DESARROLLO.md). Conservar los headers C01/piloto generados por los constructores existentes. `build_walk_native_probe.py --project /ruta/nueva/proyecto --headers /ruta/headers` emite un CMake separado y una copia diagnóstica de WindowHD; no modifica `Source`. Compilar ese proyecto con SDL3 release-3.4.0 mediante `cmake -S /ruta/nueva/proyecto -B /ruta/nueva/build -DSDL3_DIR=/ruta/SDL3` y `cmake --build /ruta/nueva/build --parallel 4`. Este ejecutable local usa `OPENFODDER_NO_MIXER`; no acredita audio ni un paquete jugable.
2. Crear un directorio vacío para instantáneas. Ejecutar el script existente `check_mission_publication_replays.py` con `--exe` apuntando al diagnóstico, `--data Run`, `--out` nuevo, `--soldier-probe --screen-probe --pause-probe --ordered-manifest tools/modernization/ordered-empty-assets.json`. Definir `SDL_VIDEODRIVER=dummy`, `SDL_RENDER_DRIVER=software`, `SDL_AUDIODRIVER=dummy` y `OPENFODDER_NATIVE_WALK_OUT` con la ruta absoluta del directorio de instantáneas. Preferir almacenamiento temporal en memoria para trazas grandes; esperar al retorno del proceso y verificar íntegramente H3.
3. Preparar el arte mediante `prepare_walk_art_review.py` y los tres constructores existentes, en otro directorio nuevo. Compilar el target `openfodder_native_walk_renderer` y el ejecutable de fixtures `openfodder_external_asset_tests` con los cambios de este bloque. `soldier_native_walk_snapshot` comprueba píxeles conocidos PC/Amiga y 12 casos negativos sin datos del juego.
4. Ejecutar `review_native_walk.py --snapshots /ruta/instantaneas --art /ruta/arte --renderer /ruta/openfodder_native_walk_renderer --window-exe /ruta/openfodder_external_asset_tests --out /ruta/nueva/revision`. Genera las imágenes locales, `native-comparison.html`, la entrada de prueba, el log SDL y `public-report.json`. El HTML permite inspeccionar cada clave y su candidato HD cuando existe; el visor previo sigue disponible para el ciclo ilustrativo. Ninguno sustituye un recorrido continuo del juego.

El exportador limita 512 claves y recursos de 1 MiB, deduplica claves y valida los ficheros de salida. El renderer rechaza recurso/clave alterados y rutas inválidas. El exportador se inyecta únicamente en la copia diagnóstica y no cambia reglas, frames, tiempos ni selección de recursos.

## Continuación vigente

Las otras 21 claves artísticas ya están preparadas y revisadas internamente en `39c29f1`; [fuentes y límites del lote de 24](../../assets/modernization/soldier-walk24/README.md). No repetir su producción. Continuar con reposo/apuntado y demás estados/enemigos, variantes y transiciones según [CONTINUIDAD.md](CONTINUIDAD.md). Este informe conserva el alcance técnico del contraste diagonal; no acredita aceptación artística ni cobertura completa.
