# Diagnóstico HD y prueba visible C01

01-11-2026 · plan 2.67. Implementado; nueva CI y paquete pendientes.

Miguel confirma funcionamiento general correcto con a05e656, pero no ve diferencia. Sus dos logs registran captura semántica/publicación de capas y carecen de `SOLDIER_HD_SDL`. Eso confirma ausencia de publicación HD registrada, no su causa. [Evidencia de los logs](evidence/c01-user-logs-2026-11-01.json).

## Diagnóstico optativo

`OPENFODDER_HD_DIAGNOSTICS=1` habilita `SOLDIER_HD_REASON`. Los lanzadores 8×/12× lo activan. Cada motivo aparece una sola vez por proceso (máximo 40), sin inundar el log en cada frame. Un motivo puede ser transitorio; solo el marcador `SOLDIER_HD_SDL` confirma sustitución publicada.

| Motivo | Significado |
|---|---|
| no-eligible-c01 | Ningún comando del destino coincide con la pose C01 admitida |
| repeated-actor | El actor ya se dibujó antes en ese intervalo |
| body-clipped / viewport-body-clipped | Cuerpo recortado en superficie o viewport |
| later-layer-overlap | Una orden posterior puede tocar el cuerpo; se preserva el clásico |
| palette-transition / black-palette | Paleta en transición o negra |
| paused / map-overview / scene-callback / outside-mission / loaded-image | Escena no apta para sustitución HD |
| missing-audit-interval / stale-scene / not-mission-surface | Falta registro actual o no corresponde a la escena/superficie |
| renderer-target / renderer-clip / renderer-scale / renderer-logical-presentation | Estado SDL no soportado por el piloto |
| native-art-enabled / publication-disabled | Conflicto con piloto nativo o publicación desactivada |
| missing-asset / unsupported-density / unsupported-pitch / patch-budget / allocation-failed | Recurso, formato, presupuesto o memoria |
| sdl-error-classic-recovered / sdl-error-recovery-failed | Fallo SDL; distingue recuperación clásica de fallo de recuperación, acompañado del error SDL disponible |

Si varios candidatos C01 son rechazados en un intervalo, el compositor informa del último candidato rechazado. No es una estadística ni implica que todos los actores fallen por esa causa. No se omiten las comprobaciones de contraste ni se modifica la simulación.

## Comparación visible

`OPENFODDER_HD_COMPARE=1` guarda, solo después de una publicación HD correcta, `C01_8.html` o `C01_12.html` y tres BMP: escena clásica, fondo sin el cuerpo seleccionado y parche HD precompuesto. Una exportación como máximo por densidad y proceso. Un fallo de escritura se registra sin hacer fallar un dibujo correcto.

El HTML recorta la vista con el Src real usado por SDL (sin mostrar el relleno de la superficie), permite alternar clásico/HD sobre el mismo fondo, marca el anclaje y muestra ambos cuerpos ampliados. Usa exactamente el mismo instante; no genera arte ni fuerza poses. Es una comparación de los píxeles compuestos, no una captura del escalado final de la GPU ni una medida de FPS.

El paquete incluirá las dos comparaciones generadas y verificadas por CI. Abrir `C01_12.html` o `C01_8.html` permite ver el cambio inmediatamente; conservar sus BMP al lado.

`PROBAR_C01_VISIBLE.cmd` reproduce automáticamente PC Format completo con HD 12× y abre la comparación al terminar solo si el log confirma una exportación nueva. Puede tardar varios minutos. Conserva `C01_PRUEBA.log` si falla. Se incluyen únicamente las ocho grabaciones públicas PC fijadas por el proyecto, sin partidas privadas. Es una prueba automática, no exige encontrar una pose jugando.

## Validación y límites

El intento de arrancar directamente en misión 2/fase 1 sí publicó C01, pero su traza no coincidió con el H3 de campaña completa (787 estados con hash distinto). No se regeneró la referencia. La prueba selecciona ahora las ocho fases PC originales y compara todos sus estados contra el H3 existente, para ambas densidades. El recorrido completo conserva la inicialización previa de campaña.

`check_c01_visible.py` exige finalización de las ocho fases, publicación HD, exportación de HTML/BMP, dimensiones correctas del parche, ausencia de errores/sanitizadores y H3 original. El empaquetador contrasta el hash del ejecutable con el informe de comparación y los hashes de cada captura. Las pruebas de Window real verifican motivos de rechazo y los guards anteriores; el fallo de escritura se probó desde un directorio no escribible y conservó el dibujo correcto.

Sigue siendo una pose C01. No cambia el tamaño del soldado, no añade animaciones ni oclusión parcial. La diferencia entre el soldado clásico y C01 debe verse claramente ampliada; la diferencia entre densidades 8× y 12× puede ser pequeña al tamaño de juego. No se vuelve a pedir elegir A/B/C ni repetir las opciones ya aceptadas.

Pruebas locales: [evidencia](evidence/c01-diagnostic-local-2026-11-01.json). Recorrido estándar PC completo PASS en ambas densidades, 7.956 estados originales por ejecución; 31 tests Python y pruebas SDL/Window con ASan/UBSan PASS. No se declara render HTML en navegador: la descarga del binario de pruebas falló; sintaxis JavaScript y BMP inspeccionados. Recorte final Src en revalidación y nueva CI/paquete pendientes.

Corrección de portabilidad: Windows 41288036788 (7d27b59) falló al compilar la fixture por falta del include explícito `<string>` para std::to_string. Añadido; también `<exception>` para el catch del exportador. No cambia composición ni guardas. Recorte final local PASS en ambas densidades; JavaScript generado ejecutado con Skia Canvas (BMP, recorte, zoom y alternancia), vista inspeccionada; no equivale a navegador DOM/GPU. Nueva CI pendiente.
