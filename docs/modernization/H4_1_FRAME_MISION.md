# H4.1 — Frame de misión compuesto y transición a pausa

24-10-2026. Código `049439d56126e95b56eebd183e4f42610d8b6821`. Base `bae84bf2ff48821a96bdccc7900ce67ce090c0f9`; motor anterior `a133afb8188a26f51e703b7a81576cf1b9264f67`. PR #1 en borrador, sin fusionar. Base clásica `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8` intacta.

## Incremento y frontera elegida

`MissionPresentation` conserva la **imagen completa ya compuesta** de terreno, sprites, HUD y cursor, con índices privados, paleta RGB efectiva, geometría y backing RGB. Reutiliza `PresentationSurface` y sus núcleos; no retiene motor, entidades, recursos vivos ni handles SDL. Cada rasterización devuelve un vector propio.

La captura se hace en `Video_SurfaceRender`, justo donde antes se convertían los índices. No se captura al terminar `Interrupt_Redraw`: `Mission_Sprites_Handle` también dibuja sprites en el paso principal y `Phase_Cycle` puede avanzar el fade antes de presentar. Capturar antes perdería esas escrituras o usaría una paleta anterior. Ambas cadencias y todas sus coordinadoras permanecen intactas.

Este incremento ensambla el resultado completo clásico, **no una lista de capas o comandos movibles independientemente**. No permite aún interpolar terreno/sprites ni sustituirlos individualmente por arte HD. La alternativa de trasladar todos los productores a una llamada por tick se descarta porque alteraría la visibilidad y el calendario de efectos. Tampoco se vuelve a llamar a productores al repetir una captura.

Ruta integrada: misión activa, sin pausa/overview/callback, superficie principal, skip clásico 16/16, sin reducción y sin PNG. Las demás combinaciones mantienen `draw` anterior. El runtime sigue presentando una vez; las planificaciones 0/1/5 se inyectan exclusivamente en el harness, sin añadir una opción de usuario ni cambiar tiempos.

## Orden y publicación

1. Interrupción original: tick de replay, entrada/cámara y efectos, terreno/Save, sprites, HUD, cursor; señales originales.
2. Paso principal original: preparación/efectos y escrituras adicionales; fade en su momento anterior.
3. `Video_SurfaceRender`: guarda de vídeo y selección de destino, captura completa → núcleo puro → `ApplyPresentation` → RenderAt → FrameEnd.
4. `Video_Sleep`: Restore, sincronización, Cycle y eventos conservan sus posiciones. El camino de replay conserva también su Restore.
5. Entrada/iteración/salida de pausa mantienen preparación, fades, eventos, restauración de paleta y redibujado de terreno/sprites/HUD.

`ApplyPresentation` continúa siendo un sink inmediato: requiere igual geometría/pitch. Una captura antigua se puede rasterizar después de destruir su origen, pero no se puede aplicar a una nueva superficie arbitraria. No se introduce cola, hilo, generación global, nueva cadencia ni protocolo de sincronización. La captura usa la serialización existente de los llamadores; este trabajo no demuestra seguridad de todos los callbacks.

## Dependencia descubierta al probar la transición

El primer ensayo integrado falló con padding de tres palabras, N=0 y primera imagen de misión al volver de pausa: para ancho inicial 80/alto 64, grupo 10, palabra 7472, se obtenía 7486 en lugar de 7503. Los índices y el estado observado coincidían; el backing RGB no. No se ha debilitado la comparación ni excluido el padding.

La composición de pausa actualiza bytes RGB que sobreviven a la conversión posterior. En superficies indexadas son el padding final situado fuera de las `width*height` palabras empaquetadas y fuera del ancho visible por fila. En una imagen RGB cargada, todos sus bytes son backing persistente. Si esa actualización solo ocurre al publicar, omitir la presentación altera la siguiente captura.

Se extrae `CommitPauseBacking`: después de capturar y antes de la presentación opcional, copia exclusivamente esos bytes persistentes desde la composición original por palabra RGB no cero. `PresentationPixelAt` calcula el valor de la capa de texto después de su conversión, respetando skips, cero/255, tamaño y padding. No avanza fades, cambia índices/paletas/Save, sube texturas ni consume entrada. En superficies indexadas sin padding no recorre ningún píxel. La captura ya obtenida sigue siendo independiente e inmutable.

Es un **efecto de producción**, no un núcleo de presentación para repetir N veces. Con una presentación, la imagen final coincide con el código anterior. Con cero, se conserva la parte del backing que condicionará capturas posteriores. El resto del buffer RGB/texture es salida y puede permanecer sin publicar. No equivale a demostrar que todos los buffers visuales sean idénticos cuando no se presenta.

## Pruebas y cobertura exacta

`check_mission_presentation.py` extrae los cuerpos reales anterior/actual de `Interrupt_Redraw`, `Video_Sleep`, `Video_SurfaceRender` y `Phase_Paused`; usa métodos y declaración reales de `cSurface`. Compara el archivo Fodder.cpp completo normalizando **solo** los dos cambios autorizados. Las guardas anteriores siguen protegiendo los productores, sus momentos, el RNG y los llamadores de Save/Restore/fade.

240 escenarios: dos anchos, dos altos, dos paddings, diez modos y tres frecuencias (0/1/5). Incluyen ruta ordinaria, callback, overview, misión inactiva, vídeo desactivado, superficie marcada RGB, destino alternativo, vista reducida, skip cero y diferencia entre los dos flags de vídeo. La ruta ordinaria y el modo con cursor desactivado recorren misión → seis iteraciones de pausa → reanudación → sustitución posterior de recursos.

Se comparan índices, fondo guardado, paletas current/next/effective, fade, banderas, tick de grabación, orden de efectos, señales, entrada/eventos y llamadas a FrameEnd/Cycle. Los productores sintéticos se solapan para detectar cambios de orden; se añaden escrituras y cambios de paleta después de la interrupción para detectar capturas prematuras. Se destruyen/sustituyen superficies y cambian dimensiones/bytes/paletas. Las 672 capturas retenidas se comparan con la imagen anterior exacta después de destruir sus fuentes, y se repiten con destinos independientes. Se comparan **todos** los bytes RGB, incluido padding.

La suite de pausa conserva sus 144 escenarios y ahora compara además las imágenes de todas las capturas retenidas con la secuencia anterior, incluso N=0; comprueba `PresentationPixelAt` frente a la rasterización completa en cada píxel indexado/RGB.

**Límites:** los productores de terreno/sprites/HUD/cursor, selección de recursos, entrada, temporizador y SDL de este harness son dobles controlados. Sus rasterizadores reales conservan las suites diferenciales previas. No se ha ejecutado aquí un replay completo del motor con vídeo real a frecuencias 0/1/5, ni pausa interactiva GPU. H3 del motor es una regresión complementaria headless, no prueba visual ni prueba de todas las transiciones. La sustitución de superficies sintéticas no acredita cargar fases comerciales. No hay nueva validación manual CD32 ni decoder PNG real. La aceptación previa H2.6 de Miguel sigue vigente.

## Reproducción, resultados y coste

```bash
python3 tools/modernization/check_mission_presentation.py
python3 tools/modernization/check_pause_presentation.py
```

Compilan C++14 con ASan/UBSan. Localmente `detect_leaks=0`; CI Linux mantiene `detect_leaks=1`. El workflow añade la suite de misión y obtiene `a133afb` para la comparación original. Las suites anteriores, huellas H3, límites y sanitizadores no se rebajan.

Resultados locales iniciales: 240 escenarios/672 capturas y 144 escenarios de pausa PASS; las nueve equivalencias anteriores PASS; 13 pruebas Python, contrato de visibilidad y 1.309 descriptores de sprites PASS. Release local y 6/6 CTests PASS; H3 PC 7.956 + Amiga 3.405, dos pasadas por campaña y 11.361 estados coincidentes con el baseline original. Replays 29/29, cero omisiones, retorno 0. [Evidencia local](evidence/mission-local-2026-10-24.json). CI [Windows 40095813348](https://github.com/Cacheirez/openfodder/actions/runs/40095813348) y [Linux 40095813181](https://github.com/Cacheirez/openfodder/actions/runs/40095813181) aprobadas sobre `049439d`.

Coste: una copia privada indexada y una copia de backing RGB por captura, más el destino propio. La misión antes capturaba solo índices para convertir; el backing es coste adicional. El efecto de pausa recorre únicamente la cola potencialmente persistente en superficies indexadas, o la imagen entera si es RGB. No se ha medido rendimiento comparativo ni se declara optimización.

## Siguiente bloque

Completar separación en capas/órdenes de misión para interpolación, cobertura de otras escenas/minimapa/cargas y pruebas del motor con presentación real; definir validación de geometría/generación en el sink antes de publicar capturas diferidas. Medir coste y validar imágenes representativas en Windows/CD32. H4.1/H4.6 siguen abiertos globalmente; no comenzar nuevas cadencias ni arte HD con este resultado parcial.

## Cierre de verificación de 049439d

- Windows: 6/6 CTests, H3 original 11.361 estados y 29/29 replays, cero omisiones, retorno 0 (22,312 s).
- Linux: todas las suites focalizadas, incluidos 240 escenarios/672 capturas y 144 escenarios de pausa, con fugas activas; H3 original 11.361 estados; 6/6 CTests.
- Motor Linux: 29/29 replays ASan/UBSan (36,184 s), LSan (36,137 s) y TSan (144,517 s), cero omisiones y sin diagnósticos en los siete engine.log examinados. Windows: cinco engine.log examinados. Los tiempos son observaciones, no un benchmark.
- ZIP de evidencias verificados por tamaño, SHA-256 y CRC; informes internos PASS. [JSON originales, dependencias y líneas de resultado](evidence/049439d-reports.json).

| Plataforma | Artefacto | SHA-256 | Caduca UTC |
|---|---|---|---|
| Linux | 12560388931 | `f710e921952864959a9d97b2062ea37813a234bb39caeb28ea3013652f8c5195` | 2026-11-23 13:04:33 |
| Windows | 12560658748 | `1eb561b5f1e18cabb6b1e7387dce468ba4bf58bc19a424e6106cbe17ac294542` | 2026-11-23 13:00:22 |

La publicación se realizó mediante el conector de GitHub porque Git HTTPS local no tenía credenciales de escritura. El árbol completo publicado `d8ee2225c6127abb1b7a6af299579a18b9dcd40d` coincide exactamente con el commit local probado `964b3d27`. No se sobrescribieron cambios remotos ni se usó force-push. Se conserva ese commit local en una rama auxiliar y la rama activa se sincroniza con el commit publicado. La instalación local de dependencias necesitó cache apt temporal por permisos del contenedor; no se cambió la configuración CI.

El archivo JSON es evidencia compacta: no contiene ZIP/trazas/logs completos ni ejecutables. Su archivo duradero externo sigue pendiente, igual que las evidencias anteriores. La base clásica permanece en `5e6a4f3`; PR #1 abierto en borrador sin fusionar. Se acepta este incremento con los límites anteriores, sin cerrar H4 globalmente.
