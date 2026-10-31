# H6 — publicación SDL opcional de C01 HD

31-10-2026 · plan 2.66. [CI y paquete a05e656 cerrados PASS](VALIDACION_a05e656.md). Prueba física Windows/GPU y densidad definitiva pendientes. Las notas posteriores de CI pendiente son historia de los incrementos 2.63–2.65.

## Activación y alcance

`OPENFODDER_SOLDIER_HD=8` o `12`, junto con `OPENFODDER_PRESENT_MISSION_LAYERS=1` y `OPENFODDER_CAPTURE_SOLDIER=1`. Mantener `OPENFODDER_SOLDIER_ART=0` (el piloto nativo es una ruta diferente). Lanzadores Windows `PROBAR_HD_8X.cmd` y `PROBAR_HD_12X.cmd`, añadidos al empaquetador. Una variable ausente o distinta de 8/12 deja la ruta previa intacta. Clásico por defecto; una sola pose C01, no todas las animaciones ni oclusión parcial.

`Window::RenderAt` llama al adaptador únicamente para una presentación de misión. `WindowHD.cpp` exige superficie de misión actual, escena activa y generación coincidente, captura activa, paleta estable/no negra y estado SDL soportado. Pausa, mapa, callback, imágenes, fundidos, destino ajeno, frame de otra escena, renderer con target/clip/scale/logical presentation no soportados conservan la ruta previa. Verifica nuevamente el intervalo mediante el oráculo clásico; una divergencia propaga el error, no queda oculta como fallback.

La composición genera fondo nativo y parche premezclado. Crea dos texturas temporales XRGB8888, NONE y NEAREST, sube sus píxeles y dibuja ambas con el mismo Src/Dest e inversa de entrada del render actual. El parche se proyecta desde el anclaje lógico sin recalcular cámara ni entidades. Rechaza cuerpos que crucen el recorte visible: se conserva el clásico completo. No modifica la superficie, índices ni textura clásica.

Las texturas se destruyen tras cada llamada: no se conserva un frame GPU entre escenas, resoluciones o renderers. Es una primera integración correcta, **no un caché GPU optimizado**; su coste de creación/subida aún debe medirse. Los recursos derivados 8×/12× se preparan una vez y se comparten como valores inmutables. Sin hilos nuevos ni cambios de simulación.

## Recuperación

Antes del primer dibujo, cualquier fallo de creación/configuración/subida vuelve al dibujo clásico habitual. Si falla después de empezar el dibujo HD, se repinta el rectángulo completo con la textura clásica usando reemplazo NONE y se restaura su modo de mezcla anterior: no se suman colores sobre una imagen parcial. Si también falla ese repintado/restauración, el adaptador devuelve fallo y la entrada de pantalla no se marca válida. No se promete recuperar un dispositivo perdido sin intervención de SDL. Memoria insuficiente en composición/recurso vuelve a clásico; errores del oráculo siguen visibles.

## Escalado: contrato y hallazgo

La igualdad exacta del compositor por capas y el completo se mantiene en su raster lógico HD. En SDL software se comprueba igualdad exacta a escala lógica entera. Con escala fraccionaria, SDL muestrea de forma diferente una textura nativa y una previamente ampliada, incluso en terreno detallado: exigir igualdad con toda la textura HD resultó incorrecto y la primera prueba detectó esa diferencia. No se cambia H3 ni se disimula con tolerancias.

Contrato físico del piloto: mantener exactamente el dibujo **clásico nativo SDL fuera del rectángulo del cuerpo**, incluidas bandas; dentro, usar el detalle HD con NEAREST y la proyección del anclaje común. Las pruebas usan fondo detallado y verifican esa igualdad exterior en 1001×777, 384×216 y 640×480. El muestreo interior puede diferir del compositor de canvas expandido. La apariencia, posibles bordes y comportamiento en GPU requieren aceptación visual posterior. No se promete identidad visual con filtros lineales.

## Pruebas y reproducción

- `soldier_art_sdl_transaction`: SDL 3.4.0 software real, PC/Amiga y 8×/12×; escala entera, fraccionaria, recorte rechazado, fondo detallado, 160 fallos individuales de creación/configuración/subida/dibujo, vuelta al clásico y reentrada. También 16 fallos de recuperación provocados: devuelve fallo. Sin texturas pendientes al terminar.
- `soldier_hd_window_lifecycle`: extrae el cuerpo **real** de TryRenderMissionHD con entradas de escena controladas y renderer software real; activa/desactiva, pausa/mapa/callback, paleta, escena/destino obsoletos, estado renderer, conflicto con arte nativo y reanudación.
- Integración previa Window/Mouse: 544.000 coordenadas y casos de misión, overview, pausa, GUI, vídeo y DPI aprobados. La puerta de identidad Window admite únicamente el cambio literal de dos líneas que despacha HD, manteniendo el hash del cuerpo previo; H3 no se modifica. Inventario de llamadas SDL ampliado al header nuevo.
- 30 tests Python aprobados. Sintaxis de WindowHD.cpp comprobada contra SDL3 real con OPENFODDER_NO_MIXER (no equivale a build completo del motor).
- Los dos CTest nuevos entran en Windows/Linux. CI añade replays reales con `--hd-probe 8` y `12`, FIT, pausa/reanudación y H3 original; 12× usa cinco presentaciones. Exige marcador de publicación HD: no acepta una ejecución que solo haya vuelto al clásico. Nueva CI pendiente, no atribuirle resultados aún.

Local: SDL tag release-3.4.0, SHA a962f40bbba175e9716557a25d5d7965f134a3d3, compilado estático en scratch. Harness SDL ejecutado ASan/UBSan con LSan local desactivado; la biblioteca SDL local no está instrumentada. CTest reproduce la prueba sin necesidad de entorno gráfico. No es GPU, input físico, audio ni validación comercial CD32.

## CI anterior cerrada

832895d: Windows 41075746093, Linux 41075746384 y comparador 41075746047, todos completed/success. Su paquete no se ha descargado/inspeccionado en este incremento; último paquete inspeccionado sigue siendo 3d82ff2 y no contiene HD SDL. No pedir al usuario probar HD con él.

Siguiente: cerrar CI de la integración, verificar paquete nuevo y prueba visual acotada 8×/12×, transiciones y resolución en Windows. Medir tiempo de frame/subidas GPU antes de fijar densidad o cachear texturas. Guardado/persistencia ya aceptados. PR abierto/borrador/sin fusionar.

## Corrección de CI 2.64

Windows 41095340402 y Linux 41095340185 (75a91ff) fallaron en la sonda de pausa tras completar las ocho fases PC. Los replays restauran mEngineTicks (por ejemplo PC m2p2=788, Amiga m1p2=150), de modo que buscar ticks absolutos 8/16 omitía fases. La sonda usa ahora pasos por fase sin escribir el reloj ni cambiar H3. La puerta exige exactamente dos parejas 8/16 en cada fase. Informes HD añadidos al artefacto Linux; nueva CI y paquete pendientes.

Validación local de la corrección: motor completo sin mixer, SDL software 3.4.0, 8× con una presentación y 12× con cinco; ambas ejecuciones PASS, 11 fases, 22 pausas/reanudaciones y 11.361 estados H3 originales por ejecución. Publicación HD real en PC y Amiga. [Informes](evidence/hd-sdl-replay-fix-2026-10-31.json). No equivale a Windows/GPU ni a audio.

## Presupuesto de CI 2.65

Windows 41194788492 agotó el límite global de 35 minutos durante Amiga 12×. 8× completo (11 fases, 22 pausas, H3) y PC 12× sí pasaron. Linux aprobó el paso HD completo. Se amplía el job Windows a 60 minutos; no se reducen fases ni presentaciones. CI/paquete nuevos pendientes.

## Cierre 2.66

Windows, Linux y comparador a05e656 completos PASS. Informes 8×/12× de ambos sistemas y manifiesto del ZIP conservados en evidence; [cierre y prueba visual acotada](VALIDACION_a05e656.md). No se atribuye prueba física ni rendimiento GPU.
