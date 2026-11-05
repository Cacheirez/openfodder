# Estado operativo — 5 de noviembre de 2026

**Plan vigente 2.74, sin cambios de alcance ni orden. A1/A2/A3/A4 y A/H7 abiertos.** La alternancia del ejecutable de Miguel sigue sin resolverse como producto; el lanzador no cambia y no hay ZIP nuevo.

## Rama y commits

- Repositorio `Cacheirez/openfodder`, rama `modernization/windows-foundation`. PR #1 comprobada abierta, borrador y sin fusionar.
- Marcha publicada: `39c29f10edeb972418bb10885fb051d47b2af3f6`. Este avance añade reposo/apuntado sobre `b617168`; su commit se obtiene del historial de este documento.
- Corrección posterior de portabilidad: `b92100982ede0b6d6c18e0cd0072aed8d637f1c4`, fija LF en los dos JSON de marcha comprobados por hash; no cambia Source, arte, claves ni referencias.
- El commit que contiene este relevo es documental y posterior a esos cambios. Obtener su SHA con `git log -1 --format=%H -- docs/modernization/CONTINUIDAD.md`; comprobar también HEAD remoto antes de continuar. No confundir un commit documental con una nueva validación del motor.

## Trabajo completado y evidencia

- A1/A2: captura de todos los slots, composición ordenada de varios cuerpos, resolución por contenido de recurso/paleta efectiva, manifiestos v2 de activos externos verificados y censo transaccional de publicación SDL. Implementado y probado; faltan cobertura/rutas y transiciones para cerrar estos bloques. Contrato: [SOLDADOS_COBERTURA_COMPLETA.md](SOLDADOS_COBERTURA_COMPLETA.md).
- Contraste nativo: 112 instantáneas PC/Amiga de demos públicas; reconstrucción con recurso y paleta reales. 13 vinculaciones diagonales probadas: 12 de marcha y una Slide1 separada. [Reproducción y límites](NATIVE_WALK_REVIEW.md), [evidencia](evidence/soldier-native-walk-validation.json).
- A3: **24 poses artísticas de marcha y ocho nuevas de apuntado bajo preparadas y revisadas internamente**. La marcha conserva sus 48 derivados 8×/12×; 18 maestros nuevos, tres anteriores reutilizados en su diagonal correcta y tres del ciclo C01 conservados. C01 y sus derivados idénticos. [Fuentes, prompts, selección y visor](../../assets/modernization/soldier-walk24/README.md).
- Manifiesto de marcha ordinaria con **94 claves reales observadas: 48 PC + 46 Amiga**. Las 112 instantáneas incluyen estados no ordinarios; no equivalen a 96 vinculaciones de marcha. Slide1 conserva el manifiesto diagonal separado.
- Falta observar 6/0 y 6/2 en el recurso Amiga `3e0bf624…`; sus imágenes modernas existen y se probaron con otros recursos. No inventar las dos claves ausentes ni vincular por compartir hoja.

## Pruebas realizadas y resultados

Resultados anteriores reutilizados, sin repetir H3 ni el censo durante este relevo:

- [Lote de marcha 39c29f1](evidence/soldier-walk24-validation.json): ASan/UBSan y método real Window/SDL PASS. Recursos controlados: 256 intervalos/512 cuerpos; claves reales sin reasignación sintética: 236/472 y 188 combinaciones clave/densidad. Tres grupos completos recorren ocho direcciones en 0–1–2–1; las 22 claves del cuarto grupo se prueban individualmente. Dos soldados, agua, oclusión y rechazos de enemigos/estados/paletas sin vincular.
- Regresiones del ciclo diagonal (32 intervalos/64 cuerpos), activos externos (128/256), nueve tests Python y reglas del piloto: PASS según el informe publicado.
- H3 local con el nuevo manifiesto: **11 fases, 11.361 estados originales (7.956 PC + 3.405 Amiga) y 22 pausas/reanudaciones PASS**. Trazas íntegras en memoria; compilación local sin mixer. **Cero publicación HD ordenada de campaña** por estados/entidades sin arte. Acredita simulación/guards, no cobertura visual ni audio.
- CI real de `39c29f1`, consultada el 5 de noviembre: [Linux PR 41944510127](https://github.com/Cacheirez/openfodder/actions/runs/41944510127) y [comparador 41944510090](https://github.com/Cacheirez/openfodder/actions/runs/41944510090) PASS. [Windows PR 41944510095](https://github.com/Cacheirez/openfodder/actions/runs/41944510095) FAIL, igual que push 41944503184. Compila; 20/21 CTests pasan. Falla únicamente `soldier_walk24_art`: `ValueError: native evidence changed; inspect bindings`. Pasos posteriores de replay/H3 y paquete omitidos; no atribuirles PASS.
- Causa reproducida: `core.autocrlf=true` convertía el JSON nativo a CRLF, distinto del SHA-256 fijado con LF. `b92100982ede0b6d6c18e0cd0072aed8d637f1c4` conserva bytes LF mediante `.gitattributes`, manteniendo la comprobación exacta. Verificación focalizada de checkout con `git -c core.autocrlf=true cat-file --filters HEAD:ruta`: ambos archivos idénticos byte a byte y hash original válido; CRLF reproduce el desacuerdo. No se han cambiado hashes para ocultarlo.
- CTest no estaba disponible en PATH durante el relevo. Un primer intento directo usó un nombre de ejecutable inexistente y no ejecutó SDL; se corrigió al binario local existente. El intento con el binario correcto terminó con error de LeakSanitizer: no puede abrir `/proc/102/task` y no funciona bajo ptrace. No se declara PASS nuevo de SDL ni sanitizadores; no se desactiva la protección para obtener un verde. [Evidencia focalizada de relevo](evidence/handoff-20261105.json). Actualización posterior: el CTest Windows de `577c702` ya pasa; ver el estado de CI siguiente. El límite local de LeakSanitizer no equivale a un fallo del motor.

## Contraste del plan con código — 5 de noviembre

- HEAD auditado `577c702`; PR #1 abierta, borrador y sin fusionar. Plan 2.74 conserva alcance/orden; su resumen ya distingue implementación y cierre de A1–A4.
- `WindowHD.cpp` carga el manifiesto ordenado y rechaza el intervalo completo ante cualquier clave ausente. `PROBAR_SOLDADO_ANIMADO.cmd` sigue en el lote antiguo de seis claves. Los 24 maestros y sus hashes están íntegros; el manifiesto tiene 94 vinculaciones únicas de marcha ordinaria, sin reposo/apuntado en esa revisión base. No hay cambios de Source desde el lote artístico `39c29f1`.
- CI de `577c702`: compilación y CTest Windows [42019722132](https://github.com/Cacheirez/openfodder/actions/runs/42019722132) PASS; el anterior fallo de hash ha superado su puerta de prueba. Compilación/CTest Linux [42019722430](https://github.com/Cacheirez/openfodder/actions/runs/42019722430) PASS; comparador [42019722401](https://github.com/Cacheirez/openfodder/actions/runs/42019722401) PASS. Windows/Linux completos aún en curso al consultar; los runs Windows de `b921009` fueron cancelados, no fallidos ni aprobados.
- No se repiten H3, censo ni generaciones concluidas. [Evidencia de contraste](evidence/plan-status-20261105.json). Ese diagnóstico de base queda ampliado por el bloque de reposo/apuntado siguiente; consultar la tarea técnica vigente al final.

## Reposo/apuntado implementado — 5 de noviembre

- Ocho maestros de apuntado bajo, 16 derivados y manifiesto combinado de 64 activos/126 claves. [Fuentes, prompts, visor y reproducción](../../assets/modernization/soldier-aim/README.md). Marcha y C01 exactos respecto a la evidencia publicada.
- La quietud normal reutiliza el frame de marcha que el original conserva. El apuntado permitido por el objetivo selecciona `0x30`, hojas `0x10–0x17`, frame 0. `0x40` se usa en una ruta especial de caída; la indicación previa de tratarlo como reposo normal queda descartada. Las funciones originales no se modifican.
- Selección real extraída y contrastada con la base clásica: 152 aserciones y 80 muestras de transición, incluidas restricciones de agua, líder/seguidor y modos de escuadrón. Cálculo espacial simulado en la fixture, no una interacción completa de campaña.
- Dos soldados con direcciones y fases independientes, solapamiento, recorte y oclusión posterior: 640 intervalos/1.280 cuerpos controlados, 600/1.200 con recursos reales a 8×/12×; tres rechazos transaccionales por modo. Tres grupos reales cubren ocho direcciones; el cuarto omite dos pares por las dos claves de marcha Amiga aún no observadas.
- 32 claves de apuntado reconstruidas desde bytes/paletas reales y metadatos originales; 11 coinciden con el censo previo y 21 no se presentan como observaciones de replay. Originales y paletas permanecen locales. [Informe sin píxeles](evidence/soldier-aim-native-references.json).
- [Validación, hashes y alcance de sanitizadores](evidence/soldier-aim-validation.json). No se repite H3 completo al no cambiar Source, lógica, tiempos ni referencias. La marcha anterior pasa su regresión. Aceptación visual, cobertura completa/GPU/CD32 y CI del nuevo commit pendientes al publicar. Sin ZIP ni cambio de lanzador.

## Pendientes y bloqueos

- Aceptación artística de Miguel **PENDIENTE**: la revisión interna y la CI no la sustituyen. La última observación de Miguel rechaza la alternancia moderno/clásico en `PROBAR_SOLDADO_ANIMADO.cmd`; no volver a ofrecer el mismo piloto parcial como terminado.
- Otros estados del jugador (posturas del modo de escuadrón 0, granadas, agua/daño/muerte), enemigos y variantes; las 24 poses no son el soldado completo.
- Dos variantes Amiga ordinarias no observadas; rutas/transiciones excluidas, GPU, densidad final, CD32 y campaña continua sin retornos normales por falta de arte. Datos comerciales, bytes nativos y paletas permanecen fuera de Git.
- Primer intento antiguo de H3 con JSONL incompleto descartado; la repetición canónica íntegra ya está acreditada. No reutilizar el intento truncado ni repetir la investigación sin regresión.

## Decisiones y recuperación de cambios locales

- Se mantiene estilo C — Pintado moderado, maestro C01 y contadores originales. Solo C01 tiene aceptación del usuario; los restantes maestros siguen candidatos. 12× de trabajo y 8× alternativa, pendientes GPU/densidad final.
- No regenerar los siete ciclos publicados ni reimplementar carga/censo/resolver salvo regresión demostrada. Las vinculaciones requieren identidad real y estado correcto; observar una clave no acredita publicación ni aceptación.
- Checkout activo de relevo: `/workspace/scratch/a4e0bfdd2e06/openfodder`. No contiene cambios funcionales pendientes aparte de los commits identificados.
- El checkout antiguo `c81d19f0fca7/openfodder`, basado en `db8a910`, conserva CMake, seis herramientas y arte experimental sin publicar. Está **sustituido** por `3e8592c`, `36e2cf8` y `39c29f1`; contiene las poses 3/2 y 5/2 rechazadas. No aplicarlo sobre HEAD ni atribuir sus resultados al lote vigente.
- Recuperación duradera: archivo **OpenFodder_recuperacion_local_20261105.zip**, guardado junto a los archivos del usuario. ZIP verificado: 71 entradas y CRC íntegros antes/después de guardar. SHA-256 `05ad629a90694b2c52a55ed49f82f739e6ef6caac6f34a68567d8e4e32e7ef31`. Incluye `RECUPERAR.txt`, SHA base, parche binario y archivos no versionados para reconstruirlo en checkout separado. Incluye también las salidas/fixtures C01 y temporales duktape del checkout antiguo `aa523e15d6d8`; no son desarrollo nuevo entregado. Los originales locales se conservan. Esta copia es archivo de recuperación, no publicación en la rama ni lote aceptado.

## Siguiente tarea técnica concreta

1. Comprobar CI real del nuevo HEAD; no atribuirle los resultados de commits anteriores.
2. Continuar A3 con las **otras posturas normales del jugador: modo de escuadrón 0, tabla en offset `0x18`**. Contrastar selección, frames y referencias antes de asumir que el comentario `Death-3` describe todas sus rutas. Después, granadas y demás armas/estados.
3. Reutilizar marcha/apuntado y pruebas ya concluidas. Completar las dos variantes ordinarias Amiga y transiciones, otros estados/enemigos y recorrido completo antes de cerrar A3/A/H7 o cambiar el lanzador.

## Inicio del próximo hilo

Se puede utilizar directamente [PROMPT_NUEVO_HILO.md](PROMPT_NUEVO_HILO.md), con GitHub conectado y sin adjuntos obligatorios. El archivo de recuperación solo hace falta para investigar el intento antiguo, no para continuar el trabajo publicado. [DESARROLLO.md](DESARROLLO.md) contiene preparación y compilación; [PLAN_TRABAJO.md](PLAN_TRABAJO.md) conserva el alcance vigente.
