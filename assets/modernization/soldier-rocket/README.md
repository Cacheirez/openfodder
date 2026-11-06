# Lanzacohetes: direcciones 0 y 7 del jugador

Bloque interno A3 del plan 2.74: **seis maestros de las direcciones 0 y 7**, frames 0/1/2 conservados por las rutas nativas. Estilo C — Pintado moderado, identidad C01 y sus activos exactos conservados. Las direcciones 1–6 y la prueba jugable de Miguel siguen pendientes.

[Prompts y referencias](generation.json), [hashes, recortes, colocación y claves](manifest.json), [visor moderno](../../../docs/modernization/reviews/rocket.html), [contacto a 8×/12×](../../../docs/modernization/evidence/soldier-rocket-contact.png), [validación](../../../docs/modernization/evidence/soldier-rocket-art-validation.json).

## Selección y producción

El selector directo mantiene frame 0; los llamadores de ratón/objetivo con `field_43` pueden restaurar 0, 1 o 2. No se anima una secuencia de retroceso 0–1–2 ni se inventa un cuarto frame por su presencia en una tabla. [Contrato original y límites](../../../docs/modernization/ROCKET_SELECTION.md).

Los PNG se generaron con `image_gen`, con alfa real y referencias propias del proyecto: C01 para el primer cuerpo; ese cuerpo y las piernas de los frames de marcha correspondientes para los otros dos. Las imágenes originales quedan intactas. Recorte, escala y anclaje se aplican con los constructores existentes; no se reflejan ni repintan maestros mediante scripts. No hay fogonazo, humo o proyectil incorporado al cuerpo: conserva esas entidades y sus relojes el motor.

La revisión interna compara casco, equipo, orientación del tubo, iluminación, volumen y piernas con C01 y las poses nativas. Miguel ha expresado una valoración artística favorable provisional del trabajo anterior, pendiente de probarlo jugando; no se atribuye aceptación jugable a este lote.

## Activos, claves y pruebas

El combinado contiene **124 activos 8×/12× y 246 vinculaciones**: los 112 activos y 222 vínculos anteriores mantienen sus descriptores/bytes exactos, contrastados también con el resultado guardado de granadas. Las **24 claves nuevas** se reconstruyen desde cuatro grupos reales de recurso/paleta PC/Amiga y tres frames de las direcciones 0 y 7. No se atribuyen a observación de replay. Las dos claves ordinarias Amiga ausentes de la dirección 6 siguen pendientes; no se necesitan ni se inventan para este recorrido de direcciones 0 y 7.

`check_rocket_art.py` ejecuta las muestras de los selectores originales en el método real `WindowHD::TryRenderMissionHD` con SDL software. Usa dieciocho casos (dos direcciones × tres llamadores × tres frames iniciales), preámbulo de marcha/apuntado, retención y regreso; 22 intervalos por secuencia. Dos soldados se presentan con rutas/fases independientes, solapamiento, recorte y oclusión posterior. A ambas densidades y en cuatro grupos: **3.168 intervalos / 6.336 cuerpos por modo**, controlado y con recursos reales. Tres casos de tipo/estado/paleta no vinculados rechazan todo el intervalo. C01 se contrasta exactamente.

La expectativa SDL reutiliza el compositor CPU previamente probado: acredita integración/publicación, no una segunda evaluación anatómica independiente. La fixture del selector simula geometría; el preámbulo/final reutiliza las familias ya verificadas. No ejecuta el manejador completo del jugador ni demuestra cobertura de campaña, GPU, CD32 o aceptación de Miguel. El informe precisa los resultados de sanitizadores y sus límites.

CTest añade `soldier_rocket_art`; se conserva `soldier_rocket_original_selection`. La modificación del emparejamiento se prueba en este bloque con dos direcciones independientes; no cambia la herramienta compartida de granadas. No cambia Source, el lanzador, los relojes ni las referencias H3; no se repite H3 completo ni se entrega ZIP nuevo.

## Reproducción

Preparar y compilar conforme a [DESARROLLO.md](../../../docs/modernization/DESARROLLO.md). Ejecutar los dos CTests de cohete. Para un diagnóstico local con recursos reales, crear directorios de salida nuevos:

```bash
python tools/modernization/prepare_aim_native.py --group 7 --snapshots /ruta/snapshots-pc --snapshots /ruta/snapshots-amiga --out /ruta/nueva/cohetes --rekey /ruta/openfodder_aim_reference --renderer /ruta/openfodder_native_walk_renderer
python tools/modernization/check_rocket_art.py --exe /ruta/openfodder_external_asset_tests --selector-exe /ruta/openfodder_rocket_selector_tests --c01-builder /ruta/openfodder_art_builder --batch-builder /ruta/openfodder_batch_builder --asset-builder /ruta/openfodder_ordered_asset_builder --native-rocket /ruta/cohetes --native-grenade /ruta/granadas --native-aim /ruta/apuntado --native-walk /ruta/snapshots-pc --native-walk /ruta/snapshots-amiga --out /ruta/nueva/validacion
```

No publicar los bytes, paletas ni rasters de los recursos originales. El helper puede reconstruir más entradas de la tabla para inspección; solo las 24 claves revisadas de este manifiesto se vinculan. El visor ilustra retención de frame, no la duración real de una llamada del motor.

Siguiente bloque: ampliar las otras siete direcciones, conservando el contrato de selección y el primer conjunto revisado. El recorrido completo en el juego sigue abierto.

## Microbloque A3-ROCKET-D0 — 6 de noviembre

Dirección 0 recuperada byte a byte del commit local `3f23207`, sin regenerar arte ni incorporar las direcciones 1–6. El manifiesto conserva exactamente las tres descripciones de maestros, doce claves y seis derivados de dirección 7. [Evidencia específica](../../../docs/modernization/evidence/soldier-rocket-d0-validation.json). Los enlaces de validación/contacto de la primera dirección son históricos; el visor incluye ahora 0 y 7.

Los mismos comandos anteriores reproducen el lote 0/7 y ambos CTests; el selector de pareja usa desplazamiento 10 entre 18 secuencias para cruzar direcciones y variar ruta/frame. Pruebas controlada y reconstruida real: 3.168 intervalos y 6.336 cuerpos cada una, 8×/12×, tres rechazos transaccionales. Los datos reales siguen siendo privados. La siguiente tarea se consulta exclusivamente en el control operativo de PLAN_TRABAJO.md.
