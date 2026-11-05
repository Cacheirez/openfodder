# Estado operativo — relevo del 5 de noviembre de 2026

**Plan vigente 2.74, sin cambios de alcance ni orden. A1/A2/A3/A4 y A/H7 abiertos.** La alternancia del ejecutable de Miguel sigue sin resolverse como producto; el lanzador no cambia y no hay ZIP nuevo.

## Rama y commits

- Repositorio `Cacheirez/openfodder`, rama `modernization/windows-foundation`. PR #1 comprobada abierta, borrador y sin fusionar.
- Último bloque artístico publicado: `39c29f10edeb972418bb10885fb051d47b2af3f6`.
- Corrección posterior de portabilidad: `b92100982ede0b6d6c18e0cd0072aed8d637f1c4`, fija LF en los dos JSON de marcha comprobados por hash; no cambia Source, arte, claves ni referencias.
- El commit que contiene este relevo es documental y posterior a esos cambios. Obtener su SHA con `git log -1 --format=%H -- docs/modernization/CONTINUIDAD.md`; comprobar también HEAD remoto antes de continuar. No confundir un commit documental con una nueva validación del motor.

## Trabajo completado y evidencia

- A1/A2: captura de todos los slots, composición ordenada de varios cuerpos, resolución por contenido de recurso/paleta efectiva, manifiestos v2 de activos externos verificados y censo transaccional de publicación SDL. Implementado y probado; faltan cobertura/rutas y transiciones para cerrar estos bloques. Contrato: [SOLDADOS_COBERTURA_COMPLETA.md](SOLDADOS_COBERTURA_COMPLETA.md).
- Contraste nativo: 112 instantáneas PC/Amiga de demos públicas; reconstrucción con recurso y paleta reales. 13 vinculaciones diagonales probadas: 12 de marcha y una Slide1 separada. [Reproducción y límites](NATIVE_WALK_REVIEW.md), [evidencia](evidence/soldier-native-walk-validation.json).
- A3: **24 poses artísticas de marcha del jugador preparadas y revisadas internamente**, 48 derivados 8×/12×; 18 maestros nuevos, tres anteriores reutilizados en su diagonal correcta y tres del ciclo C01 conservados. C01 y sus derivados idénticos. [Fuentes, prompts, selección y visor](../../assets/modernization/soldier-walk24/README.md).
- Manifiesto de marcha ordinaria con **94 claves reales observadas: 48 PC + 46 Amiga**. Las 112 instantáneas incluyen estados no ordinarios; no equivalen a 96 vinculaciones de marcha. Slide1 conserva el manifiesto diagonal separado.
- Falta observar 6/0 y 6/2 en el recurso Amiga `3e0bf624…`; sus imágenes modernas existen y se probaron con otros recursos. No inventar las dos claves ausentes ni vincular por compartir hoja.

## Pruebas realizadas y resultados

Resultados anteriores reutilizados, sin repetir H3 ni el censo durante este relevo:

- [Lote de marcha 39c29f1](evidence/soldier-walk24-validation.json): ASan/UBSan y método real Window/SDL PASS. Recursos controlados: 256 intervalos/512 cuerpos; claves reales sin reasignación sintética: 236/472 y 188 combinaciones clave/densidad. Tres grupos completos recorren ocho direcciones en 0–1–2–1; las 22 claves del cuarto grupo se prueban individualmente. Dos soldados, agua, oclusión y rechazos de enemigos/estados/paletas sin vincular.
- Regresiones del ciclo diagonal (32 intervalos/64 cuerpos), activos externos (128/256), nueve tests Python y reglas del piloto: PASS según el informe publicado.
- H3 local con el nuevo manifiesto: **11 fases, 11.361 estados originales (7.956 PC + 3.405 Amiga) y 22 pausas/reanudaciones PASS**. Trazas íntegras en memoria; compilación local sin mixer. **Cero publicación HD ordenada de campaña** por estados/entidades sin arte. Acredita simulación/guards, no cobertura visual ni audio.
- CI real de `39c29f1`, consultada el 5 de noviembre: [Linux PR 41944510127](https://github.com/Cacheirez/openfodder/actions/runs/41944510127) y [comparador 41944510090](https://github.com/Cacheirez/openfodder/actions/runs/41944510090) PASS. [Windows PR 41944510095](https://github.com/Cacheirez/openfodder/actions/runs/41944510095) FAIL, igual que push 41944503184. Compila; 20/21 CTests pasan. Falla únicamente `soldier_walk24_art`: `ValueError: native evidence changed; inspect bindings`. Pasos posteriores de replay/H3 y paquete omitidos; no atribuirles PASS.
- Causa reproducida: `core.autocrlf=true` convertía el JSON nativo a CRLF, distinto del SHA-256 fijado con LF. `b92100982ede0b6d6c18e0cd0072aed8d637f1c4` conserva bytes LF mediante `.gitattributes`, manteniendo la comprobación exacta. Verificación focalizada de checkout con `git -c core.autocrlf=true cat-file --filters HEAD:ruta`: ambos archivos idénticos byte a byte y hash original válido; CRLF reproduce el desacuerdo. No se han cambiado hashes para ocultarlo.
- CTest no estaba disponible en PATH durante el relevo. Un primer intento directo usó un nombre de ejecutable inexistente y no ejecutó SDL; se corrigió al binario local existente. El intento con el binario correcto terminó con error de LeakSanitizer: no puede abrir `/proc/102/task` y no funciona bajo ptrace. No se declara PASS nuevo de SDL ni sanitizadores; no se desactiva la protección para obtener un verde. [Evidencia focalizada de relevo](evidence/handoff-20261105.json). La CI Windows posterior debe comprobarse en vivo; no se declara verde por la corrección local.

## Pendientes y bloqueos

- Aceptación artística de Miguel **PENDIENTE**: la revisión interna y la CI no la sustituyen. La última observación de Miguel rechaza la alternancia moderno/clásico en `PROBAR_SOLDADO_ANIMADO.cmd`; no volver a ofrecer el mismo piloto parcial como terminado.
- Otros estados del jugador (reposo/apuntado, granadas, agua/daño/muerte), enemigos y variantes; las 24 poses no son el soldado completo.
- Dos variantes Amiga ordinarias no observadas; rutas/transiciones excluidas, GPU, densidad final, CD32 y campaña continua sin retornos normales por falta de arte. Datos comerciales, bytes nativos y paletas permanecen fuera de Git.
- Primer intento antiguo de H3 con JSONL incompleto descartado; la repetición canónica íntegra ya está acreditada. No reutilizar el intento truncado ni repetir la investigación sin regresión.

## Decisiones y recuperación de cambios locales

- Se mantiene estilo C — Pintado moderado, maestro C01 y contadores originales. Solo C01 tiene aceptación del usuario; los restantes maestros siguen candidatos. 12× de trabajo y 8× alternativa, pendientes GPU/densidad final.
- No regenerar los siete ciclos publicados ni reimplementar carga/censo/resolver salvo regresión demostrada. Las vinculaciones requieren identidad real y estado correcto; observar una clave no acredita publicación ni aceptación.
- Checkout activo de relevo: `/workspace/scratch/a4e0bfdd2e06/openfodder`. No contiene cambios funcionales pendientes aparte de los commits identificados.
- El checkout antiguo `c81d19f0fca7/openfodder`, basado en `db8a910`, conserva CMake, seis herramientas y arte experimental sin publicar. Está **sustituido** por `3e8592c`, `36e2cf8` y `39c29f1`; contiene las poses 3/2 y 5/2 rechazadas. No aplicarlo sobre HEAD ni atribuir sus resultados al lote vigente.
- Recuperación duradera: archivo **OpenFodder_recuperacion_local_20261105.zip**, guardado junto a los archivos del usuario. ZIP verificado: 71 entradas y CRC íntegros antes/después de guardar. SHA-256 `05ad629a90694b2c52a55ed49f82f739e6ef6caac6f34a68567d8e4e32e7ef31`. Incluye `RECUPERAR.txt`, SHA base, parche binario y archivos no versionados para reconstruirlo en checkout separado. Incluye también las salidas/fixtures C01 y temporales duktape del checkout antiguo `aa523e15d6d8`; no son desarrollo nuevo entregado. Los originales locales se conservan. Esta copia es archivo de recuperación, no publicación en la rama ni lote aceptado.

## Siguiente tarea técnica concreta

1. Comprobar HEAD/PR y CI posteriores a `b92100982ede0b6d6c18e0cd0072aed8d637f1c4`. Si Windows sigue fallando, leer el fallo nuevo y resolver esa regresión antes de ampliar arte; no repetir pruebas ya verdes sin motivo.
2. Continuar A3 con **reposo/apuntado del jugador**: contrastar selección original, estado, hoja/frame y dirección de apuntado independiente; recuperar solo las referencias reales que falten, preparar vinculaciones explícitas y arte, y probar un ciclo acotado marcha → reposo/apuntado → marcha en Window/SDL con dos soldados y oclusión, 8×/12×. Reutilizar maestros únicamente donde la correspondencia esté probada. Criterio de salida: selección exacta, publicaciones/rechazos trazables y regresiones focalizadas, sin cambiar lógica ni lanzador.
3. Después, familias de granadas/agua/daño/muerte y enemigos; resolver las dos variantes ordinarias y transiciones. No cerrar A3/A/H7 ni entregar ZIP hasta cobertura y validación pertinentes.

## Inicio del próximo hilo

Se puede utilizar directamente [PROMPT_NUEVO_HILO.md](PROMPT_NUEVO_HILO.md), con GitHub conectado y sin adjuntos obligatorios. El archivo de recuperación solo hace falta para investigar el intento antiguo, no para continuar el trabajo publicado. [DESARROLLO.md](DESARROLLO.md) contiene preparación y compilación; [PLAN_TRABAJO.md](PLAN_TRABAJO.md) conserva el alcance vigente.
