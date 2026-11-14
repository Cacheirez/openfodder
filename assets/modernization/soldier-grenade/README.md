# Posturas normales y lanzamiento de granada

Bloque interno A3 del plan 2.74: **24 maestros seleccionados de lanzamiento, ocho direcciones × tres frames**, derivados 8×/12× y transición desde marcha/reposo/apuntado al lanzamiento y de vuelta. Estilo C, identidad C01 y lógica original conservados. Revisión interna; **aceptación visual de Miguel pendiente**. [Prompts y procedencia](generation.json), [fuentes/recortes/vinculaciones](manifest.json), [visor moderno](../../../docs/modernization/reviews/grenade.html) y [hoja de revisión](../../../docs/modernization/evidence/soldier-grenade-contact.png).

## Qué se ha comprobado de las posturas

El modo de escuadrón procede de `word_3BED5`. En las fuentes CF1 revisadas solo hay cinco escrituras de inicialización, todas a 2; no se ha localizado una ruta normal que lo cambie a 0. Se conservan y prueban la rama 0, su parada y salida, sin promover la tabla comentada `Death-3` a una nueva animación normal. [Auditoría de las diez referencias y límite de la conclusión](../../../docs/modernization/evidence/soldier-normal-postures-audit.json). No demuestra que una alteración externa de memoria/estado sea imposible.

Marcha, quietud con frame conservado, disparo y apuntado de los modos efectivos reutilizan las familias ya preparadas. El disparo conserva las reglas originales de frame y cooldown; no se añaden poses genéricas ni un reloj nuevo. El cuerpo bajo de apuntado sigue en la tabla `0x30`; la tabla `0x40` mantiene su clasificación de ruta especial, no reposo normal. El resto de armas, agua, daños/muerte, enemigos y transiciones sigue pendiente.

`check_grenade_selection.py` reutiliza la extracción de los tres selectores originales, exige igualdad con la base clásica `5e6a4f…` y añade el bloque real de parada del modo 0. Ejecuta **272 aserciones y emite 168 muestras** de las ocho direcciones. Los cálculos espaciales de dirección se simulan en la fixture: no equivale a una interacción completa de campaña. Las aserciones se conservan en Release/NDEBUG.

## Secuencia de granada

La rama `mFiredWeaponType == 1` usa offset `0x28`, hojas `0x08–0x0F`. Entra en frame 0 y reinicia el tick antiguo; después selecciona **0,0,1,1,2,2** y vuelve a la postura que decide el motor. Se comprueba que no publica el índice 3, limpia los campos originales al terminar y mantiene la prioridad de agua/apuntado. La rutina original permanece sin modificar.

Las poses representan preparación, brazo armado con granada y suelta con mano vacía. El proyectil separado, su creación, trayectoria y reloj no se sustituyen ni se acreditan visualmente con estos cuerpos. No hay granada voladora pintada dentro del soldado.

## Producción y revisión

Primero se preparó y revisó la dirección 7: escala/equipo frente a C01 y ciclo completo en el método real WindowHD/SDL, 168 intervalos controlados y 168 con recursos reales, dos soldados y oclusión a ambas densidades. Después se ampliaron las otras siete direcciones.

Los PNG son generaciones independientes con alfa real, sin reflejar luces ni retocar maestros mediante scripts. Se detectó un giro brusco del rifle en `g5-f1.png`; queda **rechazado y sin vinculación**. La variante seleccionada `g5-f1-v2.png` conserva rifle, mano de soporte y apoyo de la preparación. El original rechazado se conserva solo como evidencia de la decisión. [Prompts exactos](generation.json).

El manifiesto fija recorte y colocación de cada pose en el marco nativo 16×14; las derivaciones se realizan con los constructores existentes. El visor usa un ritmo ilustrativo, no el reloj del juego. Los **64 activos anteriores** (48 de marcha y 16 de apuntado) mantienen sus descriptores y hashes exactos, incluido C01.

## Vinculaciones y verificación

96 claves de granada se reconstruyen desde cuatro grupos reales de recurso/paleta PC/Amiga y los metadatos originales. **34 coinciden con el censo previo; las otras 62 no se presentan como observaciones de replay.** El helper verifica recursos y recalcula la clave de cada frame. Su ampliación conserva el frame 0 por defecto de las referencias de apuntado. [Informe público sin píxeles/paletas](../../../docs/modernization/evidence/soldier-grenade-native-references.json). Originales y hojas nativas permanecen locales; no se usan recursos comerciales CD32.

El lote combinado contiene **112 activos y 222 vinculaciones**. `check_grenade_art.py` recorre la selección original en el método real `WindowHD::TryRenderMissionHD` con SDL software: dos soldados con fases/direcciones independientes, solapamiento, recorte y oclusión posterior a 8×/12×. Comprueba C01 y rechazo de todo el intervalo cuando un cuerpo tiene tipo/estado/paleta sin vincular. La expectativa de salida reutiliza el compositor CPU ya probado: acredita integración/publicación, no un segundo oráculo anatómico independiente.

- Controlado: 64 secuencias, **1.344 intervalos / 2.688 cuerpos**.
- Recursos reales: 60 secuencias, **1.260 intervalos / 2.520 cuerpos**. Tres grupos cubren ocho direcciones; el cuarto omite dos pares por las dos claves ordinarias Amiga de marcha aún no observadas. Las 24 poses de granada existen; no se inventan las marchas ausentes.
- Tres rechazos transaccionales por modo; la cobertura general conserva `PENDING`.

[Resultados, hashes y sanitizadores](../../../docs/modernization/evidence/soldier-grenade-validation.json). CTest añade `soldier_grenade_original_selection` y `soldier_grenade_art`. No se repite H3 completo: Source del motor, relojes, reglas y referencias no cambian. La CI completa del nuevo commit, GPU/CD32, campaña sin retornos normales y aceptación de Miguel se comprueban por separado. El lanzador sigue igual; no hay ZIP nuevo de soldados completos.

## Reproducción

Preparar/compilar conforme a [DESARROLLO.md](../../../docs/modernization/DESARROLLO.md). El workflow trae la referencia clásica antes de generar las fixtures. Ejecutar los nuevos CTests; el artístico recibe el selector y los tres constructores. Para referencias reales locales:

```bash
python tools/modernization/prepare_aim_native.py --group 5 --snapshots /ruta/instantaneas --out /ruta/nueva/granadas --rekey /ruta/openfodder_aim_reference --renderer /ruta/openfodder_native_walk_renderer
python tools/modernization/check_grenade_art.py --exe /ruta/openfodder_external_asset_tests --selector-exe /ruta/openfodder_grenade_selector_tests --c01-builder /ruta/openfodder_art_builder --batch-builder /ruta/openfodder_batch_builder --asset-builder /ruta/openfodder_ordered_asset_builder --native-grenade /ruta/granadas --native-aim /ruta/apuntado --native-walk /ruta/instantaneas --out /ruta/nueva/validacion
```

Los directorios de salida deben ser nuevos. Las referencias de apuntado se obtienen con el mismo helper en su grupo 6 por defecto. Se pueden repetir los argumentos de instantáneas si están separadas. No publicar bytes/paletas ni comparaciones nativas.
