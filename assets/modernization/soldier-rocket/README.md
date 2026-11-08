# Lanzacohetes: direcciones 0, 1, 2, 3, 4, 5 y 7 del jugador

Bloque interno A3 del plan 2.74: **veintiún maestros**, frames 0/1/2 conservados por las rutas nativas. Estilo C — Pintado moderado e identidad C01. La dirección 6 y la aceptación jugando de Miguel siguen PENDIENTES.

[Prompts y referencias](generation.json), [hashes, recortes, colocación y claves](manifest.json). El [visor publicado](../../../docs/modernization/reviews/rocket.html) y el [contacto anterior](../../../docs/modernization/evidence/soldier-rocket-contact.png) son históricos. La preparación genera un visor local con las siete direcciones actuales; no se publica material nativo comercial.

## Selección y producción

El selector directo mantiene frame 0; los llamadores de ratón/objetivo con `field_43` pueden restaurar 0, 1 o 2. No se inventa un ciclo de retroceso ni un cuarto frame. [Contrato original y límites](../../../docs/modernization/ROCKET_SELECTION.md).

Los originales se generaron con `image_gen` y alfa real. D5 recupera exactamente `r5-f0.png`, `r5-f1.png` y `r5-f2.png` del commit local `3f23207`, sin regeneración, reflejo ni repintado. Conserva los recortes, colocación, prompts y doce claves del respaldo; no incorpora D6. Recorte, escala y anclaje usan los constructores existentes. No hay fogonazo, humo o proyectil incorporado al cuerpo: esas entidades y sus relojes siguen en el motor.

Revisión interna de D5 favorable frente a C01, marcha D5, tres maestros, seis derivados y cuatro grupos nativos PC/Amiga. Las paletas Amiga capturadas solo permiten evaluar silueta. Los recortes no excluyen píxeles de alfa ≥16; el lienzo derivado tiene 16×14 celdas a 8×/12× y conserva el encaje vertical existente, con alfa en sus bordes superior/inferior. No se atribuye margen transparente al derivado. Aceptación jugando PENDIENTE.

## Activos, claves y pruebas

El combinado contiene **77 poses, 154 activos 8×/12× y 306 vinculaciones**. Los 148 activos y 294 vínculos de D4 conservan exactamente descriptores, PNG, RGBA y claves; C01 intacto. Las 84 claves de cohete se reconstruyen desde cuatro grupos reales PC/Amiga, sin atribuirlas a observaciones de replay. Las dos claves ordinarias Amiga de marcha D6 ausentes siguen pendientes y excluidas.

`check_rocket_art.py` recorre el método real `WindowHD::TryRenderMissionHD` con SDL software: 63 casos (siete direcciones × tres llamadores × tres frames iniciales), 22 intervalos por secuencia, dos soldados con rutas/fases independientes, recorte, solapamiento y oclusión. En ambas densidades y cuatro grupos: **11.088 intervalos / 22.176 cuerpos por modo**, controlado y reconstruido real. Tres rechazos transaccionales por tipo/estado/paleta sin vincular. El selector mantiene 2.703 aserciones y 576 muestras.

La expectativa SDL reutiliza el compositor CPU previamente probado y la geometría del selector está simulada; no constituyen un oráculo anatómico independiente ni cobertura del manejador completo/campaña/GPU/CD32. Se conserva `soldier_rocket_original_selection` y se amplía `soldier_rocket_art`. Source, selección, simulación, lanzador y referencias H3 intactos. H3 D3 ya válido (11 fases/11.361 estados) no repetido por este cambio artístico.

Pruebas y límites D5: [evidencia específica](../../../docs/modernization/evidence/soldier-rocket-d5-validation.json). Windows LLVM23 x86/x64 ASan/UBSan y Linux Clang18 ASan/UBSan/LSan: ambos modos PASS sin hallazgos ni advertencias de ejecución. Binarios/runtime reutilizados de D3 por hash; controles positivos D3 no repetidos. Windows usa `detect_leaks=0`; Linux `detect_leaks=1`. Publicación y CI D5: consultar la evidencia específica y el control operativo del plan; no atribuir CI anterior al lote nuevo. Las comprobaciones D3 siguen disponibles en [evidencia D3](../../../docs/modernization/evidence/soldier-rocket-d3-validation.json) y [diagnóstico](../../../docs/modernization/evidence/soldier-rocket-d3-sanitizer-escalation.md).

## Reproducción

Preparar y compilar conforme a [DESARROLLO.md](../../../docs/modernization/DESARROLLO.md). Ejecutar los dos CTests de cohete. Para un diagnóstico local con recursos reales, crear directorios de salida nuevos:

```bash
python tools/modernization/prepare_aim_native.py --group 7 --snapshots /ruta/snapshots-pc --snapshots /ruta/snapshots-amiga --out /ruta/nueva/cohetes --rekey /ruta/openfodder_aim_reference --renderer /ruta/openfodder_native_walk_renderer
python tools/modernization/check_rocket_art.py --exe /ruta/openfodder_external_asset_tests --selector-exe /ruta/openfodder_rocket_selector_tests --c01-builder /ruta/openfodder_art_builder --batch-builder /ruta/openfodder_batch_builder --asset-builder /ruta/openfodder_ordered_asset_builder --native-rocket /ruta/cohetes --native-grenade /ruta/granadas --native-aim /ruta/apuntado --native-walk /ruta/snapshots-pc --native-walk /ruta/snapshots-amiga --out /ruta/nueva/validacion
```

No publicar los bytes, paletas ni rasters de los recursos originales. El helper puede reconstruir más entradas de la tabla para inspección; solo las 84 claves revisadas de este manifiesto se vinculan. El visor ilustra retención de frame, no la duración real de una llamada del motor.

El siguiente microbloque se consulta exclusivamente en el control operativo de PLAN_TRABAJO.md. El recorrido completo en el juego sigue abierto.

## Microbloque A3-ROCKET-D0 — 6 de noviembre

Dirección 0 recuperada byte a byte del commit local `3f23207`, sin regenerar arte ni incorporar las direcciones 1–6. El manifiesto conserva exactamente las tres descripciones de maestros, doce claves y seis derivados de dirección 7. [Evidencia específica](../../../docs/modernization/evidence/soldier-rocket-d0-validation.json). Los enlaces de validación/contacto de la primera dirección son históricos; el visor de aquel bloque incluía 0 y 7.

En el commit `b54e19f`, los comandos anteriores reproducen el lote 0/7 y ambos CTests; el selector de pareja usa desplazamiento 10 entre 18 secuencias para cruzar direcciones y variar ruta/frame. Pruebas controlada y reconstruida real: 3.168 intervalos y 6.336 cuerpos cada una, 8×/12×, tres rechazos transaccionales. Los datos reales siguen siendo privados. La siguiente tarea se consulta exclusivamente en el control operativo de PLAN_TRABAJO.md.

## Microbloque A3-ROCKET-D1 — 6 de noviembre

Solo dirección 1 recuperada del commit local `3f23207`: tres maestros, seis derivados 8×/12× y doce claves reconstruidas. Las direcciones 2–6 permanecen en el respaldo; no se incorporan. [Evidencia D1](../../../docs/modernization/evidence/soldier-rocket-d1-validation.json).

En `fa413e0`, el mismo comando reproduce la matriz 0/1/7 de 27 secuencias: 4.752 intervalos y 9.504 cuerpos por modo, dos soldados con direcciones/rutas/fases independientes, recorte/oclusión y tres rechazos transaccionales. El desplazamiento 10 cambia de dirección y de caso en los tres grupos de nueve. Se comparan los 124 activos/246 vínculos de D0 con el nuevo resultado. No cambia código C++ ni selección: se reutiliza la fixture de D0; ASan/UBSan de D0 no se atribuye a D1. H3, campaña, GPU/CD32, LSan y aceptación jugando siguen pendientes de sus validaciones pertinentes.

## Microbloque A3-ROCKET-D2 — 6 de noviembre

Solo dirección 2 recuperada exacta desde `3f23207`: tres maestros, seis derivados 8×/12× y doce claves reconstruidas. Direcciones 3–6 excluidas. [Evidencia D2](../../../docs/modernization/evidence/soldier-rocket-d2-validation.json). Se comparan los 130 activos/258 vínculos de D1 con el nuevo resultado por descriptor, bytes y clave.

La CI Linux de D1 (`42212495681`, job `127874305751`) falló en `soldier_rocket_art` durante la pasada ASan/UBSan: el watchdog fijo de 240 segundos expiró. Windows y densidades de ese SHA finalizaron correctamente. Se conserva la matriz completa y se escala únicamente el límite finito a `max(240, expected_intervals // 8)`: 792 segundos para los 6.336 intervalos actuales. No cambia código C++, aserciones, selección, reloj ni recuperación del producto.

Reproducir con los comandos anteriores; para sanitizadores usar el ejecutable de la misma fixture compilado con `-fsanitize=address,undefined -fno-omit-frame-pointer`. La prueba local establece `ASAN_OPTIONS=detect_leaks=0`; LSan queda PENDIENTE. La CI completa del cierre y aceptación jugando se consultan por separado.

Cierre D2: ASan/UBSan local PASS en la matriz controlada completa (6.336 intervalos), con `detect_leaks=0`; salida y hash del ejecutable contrastados. LSan y CI remota completa D2 PENDIENTES.

## Microbloque A3-ROCKET-D5 — 8 de noviembre

Solo dirección 5 recuperada exacta de `3f23207`: tres maestros con alfa, seis derivados 8×/12× y doce claves reconstruidas. D6 permanece excluida. Se conservan los 148 activos y 294 vínculos D4 por descriptor, PNG, RGBA y clave, en ambas plataformas. [Evidencia D5](../../../docs/modernization/evidence/soldier-rocket-d5-validation.json).

Windows LLVM23 x86/x64 ASan/UBSan y Linux Clang18 ASan/UBSan/LSan, controlado y real: 11.088 intervalos/22.176 cuerpos y tres rechazos por modo. Selector: 2.703 aserciones/576 muestras. Se reutilizan los binarios exactos validados de D3; Source, selección, simulación, referencias H3 y lanzador intactos. Revisión interna favorable; aceptación jugando PENDIENTE. La siguiente tarea se consulta exclusivamente en el control operativo del plan.
