# Reposo y apuntado — ocho direcciones

Bloque interno A3 del plan 2.74. Ocho maestros nuevos de postura baja de apuntado, estilo C y equipo de C01. **Revisión artística interna, aceptación de Miguel pendiente.** No cambia el lanzador ni entrega soldados completos. [Prompts exactos y procedencia](generation.json), [recortes/colocación y claves](manifest.json), [visor de transición](../../../docs/modernization/reviews/aim.html), [hoja de revisión](../../../docs/modernization/evidence/soldier-aim-contact.png).

## Selección original comprobada

No hay una única familia de «reposo/apuntado». `Sprite_Handle_Troop_Direct_TowardMouse` puede conservar el frame de marcha al detenerse; se reutiliza la marcha existente. Cuando el objetivo/estado lo permite, `Sprite_Handle_Troop_Animation` selecciona el offset `0x30`, hojas `0x10–0x17`, frame 0: la familia baja etiquetada `Prone`. La conservación de frame se acota para no introducir un índice inexistente. Las restricciones de agua, movimiento del líder y seguimiento se mantienen.

El offset `0x40` (hojas `0xB0–0xB7`) de `Sprite_Update_Direction_Anim` pertenece a una ruta especial de caída y **no se activa como reposo normal**. El modo de escuadrón `word_3AA1D=0` selecciona otra familia `0x18` y sigue pendiente de arte. No sustituir estas ramas por una postura genérica ni modificar los selectores.

`check_aim_selection.py` extrae las tres funciones actuales, exige igualdad con la base clásica `5e6a4f…` y las ejecuta en una fixture con geometría/dirección al objetivo simuladas. Comprueba 152 aserciones en ocho direcciones y emite 80 muestras de marcha → reposo con frame conservado → apuntado bajo → marcha. El cálculo espacial completo y una interacción de campaña no quedan acreditados por esta fixture.

## Arte y derivación

Los ocho PNG maestros son salidas independientes de `image_gen` con transparencia real; referencias C01, pose de apuntado frontal y equipo de espalda. Las referencias nativas solo guían postura/orientación y quedan locales. Los maestros no se retocan ni se reflejan con scripts.

La primera derivación hacía demasiado grandes algunos cascos laterales. Se corrigió la colocación explícita en `manifest.json`: altura de contenido 10 u 11 unidades dentro del mismo marco nativo 16×14, anclada abajo. `build_soldier_batch.cpp` admite esas alturas; su caso anterior de altura 14 produce los mismos bytes. No cambia tamaño lógico ni selección de frames. Revisión interna de ocho transiciones y comparación de casco/equipo/anclaje realizadas sobre los derivados.

`prepare_aim_art.py` reutiliza `prepare_walk24.py`, añade 16 derivados y combina 64 activos con 126 vinculaciones. **Los 48 activos de marcha coinciden con sus hashes publicados; C01 permanece exacto.** No se regeneran maestros de marcha.

## Referencias reales y límites

`prepare_aim_native.py` y `rekey_aim_reference.cpp` reconstruyen 32 claves desde cuatro grupos reales recurso/paleta de las demos PC/Amiga, usando metadatos de las hojas originales; verifican el hash del recurso, recalculan claves y rasterizan con el núcleo existente. **11 coinciden con el censo previo; 21 son reconstrucciones desde tablas/bytes verificados, no observaciones de replay.** No extrapolan a otro recurso, bioma o CD32. [Evidencia pública sin píxeles/paletas](../../../docs/modernization/evidence/soldier-aim-native-references.json). Datos originales y HTML comparativo nativo permanecen locales.

## Prueba de transición

`check_aim_art.py` ejecuta el método real `WindowHD::TryRenderMissionHD` en SDL software, a 8×/12×, dos soldados con direcciones y fases desplazadas entre sí, solapamiento, recorte del segundo y una oclusión posterior. Compara salida exacta, conserva C01 y comprueba rechazo transaccional si falta una clave de cualquiera de los cuerpos. La expectativa SDL reutiliza el compositor CPU ya probado: esta prueba verifica integración/publicación, no un segundo oráculo independiente de anatomía o raster.

- Controlado, tablas originales y vinculaciones de prueba explícitas: 64 secuencias, 640 intervalos y 1.280 cuerpos publicados.
- Recursos reales: 60 secuencias, 600 intervalos y 1.200 cuerpos. Tres grupos recorren las ocho direcciones; en el cuarto se omiten dos pares de direcciones porque las dos claves ordinarias Amiga de marcha siguen sin observarse. No se inventan.
- Tres rechazos completos: segundo cuerpo enemigo, animación no cubierta y paleta desconocida. No hay publicación parcial.

CTest añade `soldier_aim_original_selection` y `soldier_aim_art` Windows/Linux. [Resultados y alcance de sanitizadores](../../../docs/modernization/evidence/soldier-aim-validation.json). No se repite H3 completo: Source del motor, reglas, relojes y referencias siguen sin cambios. La campaña completa sin retornos normales por falta de arte, otros estados, GPU/CD32 y aceptación visual permanecen pendientes.

## Reproducción

Compilar los targets de CMake; el CTest artístico recibe el ejecutable de selección y los tres constructores existentes. Para referencias reales locales, compilar `openfodder_aim_reference` y `openfodder_native_walk_renderer`, y ejecutar:

```bash
python tools/modernization/prepare_aim_native.py --snapshots /ruta/instantaneas --out /ruta/nueva/referencias --rekey /ruta/openfodder_aim_reference --renderer /ruta/openfodder_native_walk_renderer
python tools/modernization/check_aim_art.py --exe /ruta/openfodder_external_asset_tests --selector-exe /ruta/openfodder_aim_selector_tests --c01-builder /ruta/openfodder_art_builder --batch-builder /ruta/openfodder_batch_builder --asset-builder /ruta/openfodder_ordered_asset_builder --native-aim /ruta/referencias --native-walk /ruta/instantaneas --out /ruta/nueva/validacion
```

Los directorios de salida deben ser nuevos. Se pueden repetir `--snapshots` y `--native-walk` si los recursos están separados. No subir recursos originales, paletas ni capturas nativas a Git.
