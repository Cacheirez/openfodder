# H4.1 — Identidad y geometría de los destinos de presentación

24-10-2026. Base `a6c4b07a9dd53eff1016303f559e7c0ea5243a8d`; motor anterior `049439d56126e95b56eebd183e4f42610d8b6821`. PR #1 en borrador sin fusionar y base clásica `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8` conservada.

## Decisión y alcance

Antes de ampliar las capas de misión se cierra la precondición del sink identificada en [el informe del frame](H4_1_FRAME_MISION.md): `ApplyPresentation` hacía memcpy del tamaño del resultado sin verificar el destino. Una captura retenida podía rasterizarse correctamente y, aun así, publicarse en una superficie distinta o incompatible.

Cada `cSurface` recibe una identidad de almacenamiento privada: un `shared_ptr<const PresentationDestination>` cuyo objeto está vacío. No contiene ni retiene la superficie, el motor, SDL o una textura. Las capturas conservan esa identidad junto a sus datos privados; `PresentationTarget` la transmite al resultado de rasterización. Mientras una captura antigua exista, su identidad no puede reutilizarse para una nueva superficie aunque el allocator reutilice exactamente la dirección de `cSurface`.

La identidad se renueva cuando `LoadPng` sustituye con éxito `mSDLSurface`, incluso si mantiene dimensiones. No se renueva al cambiar píxeles, paleta, fade, Save/Restore ni al rasterizar: identifica el almacenamiento de destino, **no la versión del contenido ni una fase del juego**. Volver a presentar una captura antigua sobre el mismo almacenamiento sigue siendo una operación permitida.

No se añade cola ni hilo, no se amplía la cadencia y no se modifica Fodder.cpp. Las llamadas actuales siguen siendo inmediatas y válidas. La separación de capas independientes continúa pendiente; este incremento aporta la comprobación de destino que necesitará esa separación.

## Contrato nuevo del sink

`bool cSurface::ApplyPresentation(const PresentationTarget&)` devuelve false sin escribir ni subir texturas cuando:

- Falta identidad o pertenece a otro almacenamiento/superficie.
- No hay superficie/píxeles SDL válidos, o sus dimensiones/pitch no son positivos.
- El formato no usa palabras de cuatro bytes, o pitch no es divisible por cuatro.
- Ancho, alto o stride no coinciden exactamente, o stride es menor que el ancho visible.
- El vector no contiene exactamente `stride*height` palabras. La comprobación usa división/resto para evitar multiplicaciones desbordadas.

Con entrada compatible conserva memcpy y una actualización de textura si existe. No modifica índices, fondo guardado, paletas ni estado de fade. No recorta silenciosamente un frame incompatible para hacerlo caber.

`CommitPauseBacking` usa la misma comprobación para el destino de fondo antes de aplicar el efecto de producción descubierto en la transición. Devuelve bool y no sube texturas. La capa de texto continúa siendo una fuente retenida, no tiene que pertenecer al mismo destino que el fondo.

Los llamadores inmediatos existentes no necesitan una rama de recuperación porque capturan y aplican sobre la misma superficie sin sustituirla entre ambos pasos. Una futura cola debe comprobar el bool y decidir explícitamente descartar o reconstruir; esa política **no está implementada**. Esto tampoco sustituye el bloqueo necesario para impedir modificaciones concurrentes entre comprobación y copia.

Los kernels puros siguen permitiendo rasterizar capturas antiguas o sin destino vinculado, pero el sink solo acepta resultados vinculados a su almacenamiento. Las fuentes/geometrías capturadas deben seguir cumpliendo las precondiciones de rasterización; no se convierte esta validación de destino en un validador universal de escenas arbitrarias.

## Pruebas

`check_presentation_destination.py` compila los métodos reales de cSurface y el cuerpo real de `LoadPng` con SDL/STB controlados, C++14 y ASan/UBSan. Normaliza exactamente los tres métodos de presentación modificados, el nuevo matcher y la renovación de identidad en LoadPng; exige que todo el resto de Surface.cpp permanezca igual a `049439d`.

97 publicaciones/commits de backing válidos y 627 rechazos. Casos: tres anchos, dos altos, dos paddings, fuentes indexadas/RGB, textura presente/ausente; identidad distinta con igual geometría; ancho/alto/stride alterados; vector corto/largo; identidad ausente; dimensión cero; metadatos máximos size_t; pitch no divisible por cuatro y formato de tres bytes. Se comprueban píxeles, estado lógico de superficie y ausencia de SDL_UpdateTexture al rechazar.

También se destruye una superficie y se construye otra en **la misma dirección** mediante placement new. La captura vieja sigue produciendo sus píxeles y se rechaza en la nueva superficie. Se ejecuta `LoadPng` real con un decoder de prueba: reemplazo RGBA de igual tamaño invalida el resultado anterior; el resultado nuevo se acepta; un segundo reemplazo cambia dimensiones y formato, e invalida otra vez el resultado anterior. Las capturas antiguas sobreviven y la identidad se libera tras el último propietario.

La suite no valida el decoder STB ni la GPU reales. No se captura una imagen de 24 bits como si fuera una capa de palabras RGB: ese formato queda fuera de la API de captura existente. No se cambian aquí el ownership ni los fallos históricos del loader PNG.

Las suites previas de pausa (144 escenarios) y misión (240 escenarios, 672 capturas) continúan comparando el comportamiento anterior con recursos destruidos/sustituidos y 0/1/5. Se adapta el harness a las firmas bool y al formato SDL simulado; no se reducen sus casos, referencias ni comparaciones. Se añade paso obligatorio Linux CI con detect_leaks=1.

## Reproducción y resultados

```bash
python3 tools/modernization/check_presentation_destination.py
python3 tools/modernization/check_pause_presentation.py
python3 tools/modernization/check_mission_presentation.py
```

Local: 97 aceptaciones/627 rechazos, 144 escenarios de pausa, 240 de misión/672 capturas y todas las equivalencias anteriores PASS con ASan/UBSan, detect_leaks=0. También 13 pruebas Python, contrato de visibilidad y 1.309 descriptores de sprites PASS. [Evidencia local](evidence/destination-local-2026-10-24.json). Compilación completa/H3/replays CI pendientes al escribir esta primera revisión; no se atribuye al nuevo motor la validación H3 anterior.

El entorno local de esta sesión conserva el checkout pero perdió CMake y las dependencias SDL temporales. No se presenta el binario conservado de la sesión anterior como una compilación del nuevo código. La compilación completa y H3/replays de este incremento se verificarán en CI Windows/Linux.

## Coste, diferencias y continuación

Una pequeña asignación de identidad por construcción/reemplazo de almacenamiento y una referencia compartida por captura/resultado; comparaciones constantes antes de publicar. No se copian píxeles adicionales por esta identidad. No se ha medido rendimiento comparativo.

El contrato es común a PC/Amiga después de sus productores específicos. No cambia formatos indexados, planos, recortes ni orden de paletas. Tampoco se cambia la mezcla de pausa por palabra RGB no cero ni la preservación del backing.

Siguiente: separar las órdenes/capas de misión conservando las escrituras de ambos ritmos clásicos; ampliar pruebas del motor con vídeo real y cobertura de otras escenas/cargas/minimapa. La política de publicación asíncrona, el decoder PNG real, GPU y validación visual comercial siguen pendientes. H4 global continúa abierto.
