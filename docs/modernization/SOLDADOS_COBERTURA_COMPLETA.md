# Sustitución completa de soldados — revisión del 02-11-2026

## Decisión de Miguel

El lote f72d6e7 aparece intercalado con el soldado antiguo. Esa mezcla no es aceptable como resultado final. Hay que reproducir los sprites, direcciones, estados y secuencias del original con arte moderno, no mantener una selección parcial durante el juego normal. La entrega A sigue abierta. CI verde demuestra sus pruebas técnicas, no aceptación visual ni cobertura completa.

## Lo que realmente hace el original

La marcha tiene **8 direcciones × 3 fotogramas = 24 claves por bando** en PC y Amiga. Dos extremos de zancada y una pose intermedia permiten representar el movimiento, pero las imágenes deben asignarse tras contrastar las poses originales: no basta generar dos pies alternos y ponerles índices arbitrarios. El ciclo del contador es 0–1–2–1; la fase inicial, el contador utilizado y las excepciones los decide el motor. Mantener también sus poses quietas y de disparo.

`Sprite_Handle_Troop_Animation` selecciona según `mFaceDirection` y el estado; la dirección de apuntado puede diferir del desplazamiento o del joystick. `Sprite_Frame_Modifier_Update` conserva los contadores originales: uno se actualiza cada cuatro llamadas y el rápido cada dos. No trasladar esos ticks a FPS del monitor ni añadir un reloj artístico.

El mapeo de las ocho direcciones es: 0 delante, 1 delante/izquierda, 2 izquierda, 3 izquierda/atrás, 4 atrás, 5 atrás/derecha, 6 derecha, 7 derecha/delante. Son las etiquetas de las tablas, no una reinterpretación de los controles.

## Inventario comprobado en código

Herramienta reproducible: `python tools/modernization/inventory_soldier_catalog.py --out docs/modernization/evidence/soldier-catalog.json`. [Catálogo con offsets, segmentos, geometría, arrays, referencias y hashes](evidence/soldier-catalog.json). Usa las tablas CF1 PC/Amiga, valida sus longitudes reales y recorre las tablas humana/enemiga.

| Familia de la tabla | Direcciones | Fotogramas por dirección |
|---|---:|---|
| Marcha | 8 | 3 |
| Lanzar granada | 8 | 3 |
| Cuerpo a tierra | 8 | 1 |
| Nadar | 8 | 2 |
| Muerte, grupo 1 | 8 | Generalmente 2; jugador PC primera dirección 1, última dirección enemiga 3 |
| Muerte, grupo 2 | 8 | 2; comparte una hoja con el grupo anterior |
| Grupo etiquetado `Death-3` | 8 | 3; también lo seleccionan otras ramas del código: no clasificar por el comentario solamente |
| Lanzacohetes | 8 | Generalmente 3, una dirección tiene 4 |
| Arma en reposo/apuntado | 8 | 1 |

Tras eliminar la hoja compartida, cada bando referencia **71 hojas**. Jugador: **158 claves hoja/frame en PC y 159 en Amiga**; enemigo: **160 en cada formato**. No sumarlos como encargos artísticos: hay equivalencias entre plataformas, alias, paletas y recursos que pueden compartirse. Son entradas definidas, no una prueba de que todas se ejecuten en cada edición o fase.

El catálogo incluye también los metadatos de 18 hojas adicionales por formato: cuerpos especiales, elementos asociados, marcadores y las hojas 0x2A/0x6C declaradas pero omitidas por los alias de las tablas de animación. No encargar esas dos como estados alcanzables sin comprobar la ruta.

La herramienta registra además 80 asignaciones literales de hoja en Troop/Core/Civilian con función y clasificación. La inspección distingue:

- Cuerpos/estados especiales: cadáver flotante 0x9E; hojas 0x38/0x7A; final de misión 0x41/0x38/0x9F; deslizamiento 0xA4/0xA7; entrada en vehículo 0xCC. Verificar frames, altura y recortes en cada manejador.
- Elementos asociados: sombras 0x8D/0x97, rangos/bonificaciones 0x95/0xE5/0xE6. No fundirlos en el cuerpo sin conservar su orden y condiciones.
- 0x7C actúa como ocultación/marcador en varias rutas; no inventar un soldado visible para él.
- Civiles y rehenes tienen familia propia (incluida la espera 0xDC y rutas D0/D6/D7/D8/D9/DA/DD); mantenerlos en la matriz general, sin asumir que comparten el soldado armado.
- El barrido también encuentra árboles, puertas, aves y otros efectos. Están clasificados aparte, no incluidos artificialmente en la cuenta del soldado.

**Límite del inventario:** no extrae arte comercial, no resuelve por sí solo variantes de recursos/paleta de cada bioma, ni constituye cobertura dinámica de CD32. La fase pública m1p2 sirve para regresión, pero no puede demostrar todos los estados. CF2 queda fuera del objetivo CF1; no modificarlo accidentalmente.

## Por qué se intercala el clásico

Hay limitaciones independientes, comprobables en el código de f72d6e7:

1. `SoldierArtEligible`: solo hojas 2/7 y frames 0/1/2, tipo jugador, animación 0, cuerpo 16×14 sin recorte de agua. Faltan 18 claves solo en la marcha del jugador y todos los demás estados.
2. `CaptureSoldierSemantic`: captura únicamente el primer jugador presente; excluye otros soldados, enemigos y rutas de vehículo/destrucción.
3. `ComposeSoldierArt`: sustituye como máximo un comando. Superposición posterior, repetición del actor o recorte causan retorno clásico.
4. `TryRenderMissionHD`: otras condiciones de pausa, mapa, paleta, destino o renderer también retornan al clásico. Las transiciones necesitan tratamiento coherente, no solo más PNG.

El log aportado por Miguel confirma `later-layer-overlap` y `no-eligible-batch-key`, además de `palette-transition` y `black-palette`; registra únicamente las seis claves del piloto. No incluye tiempos por frame, así que no permite asignar cada alternancia visual a una línea concreta.

## Implementación que sigue

1. Completar la matriz estática con rutas especiales y variantes efectivas de recurso/paleta; crear casos sintéticos y recorridos que ejerciten cada estado. Registrar por entidad, clave, recurso y motivo: intentos, sustituciones, faltantes, recortes y errores. La puerta actual «se publicaron seis claves alguna vez» es insuficiente.
2. Ampliar captura a todos los soldados previstos, conservando identidad/generación y bytes propios; procesar cada comando relevante en su posición original. Sustituir el parche único por composición ordenada capaz de varios cuerpos, oclusiones y recortes de agua/bordes. Mantener la referencia clásica independiente. **No quitar las protecciones para hacer aparecer HD encima de obstáculos.**
3. Preparar primero un ciclo completo de 24 claves del jugador y su prueba de giro en ocho direcciones; revisar que manos/arma/casco, volumen, iluminación, pies y altura sean coherentes. El ciclo debe sustituir claves originales, no repetir una pose quieta ni inferir el frame a partir de la entrada de usuario. Después completar todos los estados, aliados/enemigos y variantes censadas antes de declarar al soldado terminado.
4. Conservar el estilo C y el maestro C01, pero tratar el lote de cinco imágenes como provisional. Ajustar sus poses si no corresponden al frame original. El tamaño 16×14, animación 0 y los offsets del piloto no pueden ser requisitos globales.
5. Verificar H3, orden, recortes, agua, superposiciones, múltiples soldados, disparo, granadas, muerte, vehículo, pausa, cambios de fase y retorno tras un error. Validar ambas densidades y el paquete Windows completo.

## Criterio de salida

En funcionamiento normal, **ningún cuerpo clásico intercalado** entre poses modernas dentro del alcance de soldados acordado, incluyendo todos los soldados presentes, sus direcciones y estados. Los contadores deben demostrar cobertura por estado/entidad y ausencia de retornos por falta de arte o por oclusiones normales; un caso no ejercitado se marca pendiente, nunca PASS. Revisar una escena continua además de la galería.

El modo clásico sigue disponible por elección. Ante fallo real de carga, recurso inválido o error SDL, conservar recuperación segura, registrada y coherente; no confundirla con aceptar una cobertura incompleta como producto terminado. No hace falta ocultar esa protección para cumplir el objetivo visual.

Esta revisión cambia alcance y pruebas; **no corrige todavía el ejecutable f72d6e7 ni genera el resto de imágenes**. La siguiente implementación debe resolver conjuntamente cobertura y composición antes de entregar otra muestra como soldado completo.

## Bloque interno A1/A2

- Captura: todos los dibujos visibles de `mSprites` y `mSprite_Spare`; el nombre histórico `Soldier` de la operación incluye ahora efectos/civiles y otras entidades para no perder su procedencia. Clasificar después, sin excluir enemigos, agua, vehículo o destrucción en el productor. Conserva `mFaceDirection` además de movimiento, persona, escena/slot/generación y recurso propio. Pausa/mapa/fuera de misión siguen excluidos y pendientes de integración.
- Traza: `OPENFODDER_CAPTURE_SOLDIER=1`, publicación de capas y `OPENFODDER_SOLDIER_COVERAGE=1` emiten `SOLDIER_CAPTURE` por comando después del contraste clásico. Incluye clave, recurso/generación/layout/paleta, estado, apuntado, recorte y orden. La generación solo identifica una versión local al proceso; no demuestra equivalencia entre biomas o ejecuciones. Puede producir logs grandes; usar solo en diagnósticos acotados.
- Matriz: `python tools/modernization/soldier_coverage.py --out informe.json [--log engine.log]`. `--require-complete` devuelve 1 mientras no haya evidencia completa; un log vacío o seis claves publicadas nunca pasan. Distingue cuerpos conocidos, tipo inesperado con hoja de cuerpo, civiles/rehenes, asociados, marcador y otras entidades por clasificar. Variantes CD32 y escenarios no probados quedan pendientes.
- Compositor interno: `ComposeOrderedSoldierArt` resuelve cada comando en su posición; no selecciona una única entidad ni modifica el reloj. Sustituye el cuerpo completo por celdas HD precompuestas y elimina las celdas afectadas por escrituras posteriores, incluidas las del mismo color, cero y OR. Guarda/restaura índices y celdas juntos. El presupuesto cuenta celdas activas y guardadas; un exceso genera error, nunca salida parcial. La referencia clásica independiente sigue ejecutándose antes.
- Recorte: dimensiones variables del recurso original y coordenadas de muestra derivadas de `sourceOffset`, columnas/filas ya preparadas y `rowsToSkip`. No estira el trozo visible ni reinterpreta el joystick. Geometrías inválidas, formatos/pitch no admitidos o activos inconsistentes fallan explícitamente. Los tests cubren agua, arriba/abajo y laterales PC; laterales Amiga reales siguen pendientes.
- Resolución artística: el llamador debe verificar recurso/variante completo y clasificar explícitamente lo que conserva clásico. Un recurso faltante se registra como `Missing`; no puede satisfacer `complete()`. Ese método comprueba únicamente el intervalo interno, **no aceptación global ni publicación SDL**. Los tests usan colores sintéticos, no arte nuevo aceptado.

**Límite del bloque CPU inicial:** no sustituía `ComposeSoldierArtHDLayers` ni `TryRenderMissionHD`; la integración posterior por manifiesto se describe abajo. Los guards del piloto permanecen. Falta resolver arte por recurso/paleta, conectar la salida y recuperación SDL, cubrir transiciones y ejecutar la secuencia continua completa. No representa un ejecutable con la mezcla corregida. El alcance H0–H10 se conserva.

## Adaptador SDL ordenado (interno)

`OrderedSoldierSDL.hpp` consume el resultado del compositor, agrupa celdas contiguas por fila y carga el fondo y todas las franjas visibles antes de escribir en el renderer. Conserva huecos de oclusión y recorta cada franja contra la vista. Los extremos de destino se redondean de forma compartida: redondear posición y alto por separado dejaba rendijas en SDL software a escala fraccionaria. No equivale a certificar muestreo idéntico a un lienzo HD expandido a todas las escalas.

La falta de recursos impide la publicación parcial. Cualquier fallo de dibujo restaura toda la vista desde la textura clásica independiente, desactivando temporalmente su mezcla; un fallo de recuperación devuelve error. Ninguna textura sobrevive a la llamada. Pruebas: comparación exacta con lienzo HD a escala entera y recorte atravesando cuerpos, agua, superposición, oclusión del mismo color, todas las llamadas SDL fallables, restauración de mezcla, recurso faltante, datos inválidos y reentrada. SDL software y ASan/UBSan; LSan no disponible bajo ptrace local.

La integración posterior por manifiesto conecta desde `TryRenderMissionHD`; siguen pendientes las vinculaciones completas, poses, transiciones y GPU/recorrido visual. Este adaptador no cambia la ruta del piloto ni elimina sus guards. [Informe](evidence/soldier-ordered-sdl-validation.json).

## Resolución de variantes e integración WindowHD

`SoldierVariant.hpp` calcula SHA-256 sobre formato, segmento, offset, dimensiones/planos, tipo/persona, hoja/frame/animación, vehículo/destrucción, geometría original, bytes de la pose completa sin recorte y los 255 colores RGB efectivos de presentación. No usa punteros ni generaciones de proceso. Posición, slot, escena, reloj y recortes no cambian la clave. Los colores no usados también cuentan: decisión conservadora que evita extrapolar equivalencias sin revisar. El diagnóstico emite hashes, no bytes gráficos privados.

`OrderedSoldierRegistry.hpp` carga vinculaciones explícitas; rechaza versión/clave/decisión inválidas, duplicados, más de 8192 entradas o ficheros mayores de 8 MiB. Se carga una vez por ruta: reiniciar para aplicar ediciones. Observar una clave no crea ni aprueba su vinculación. El formato inicial permite las seis poses existentes; extenderlo para el resto del arte sigue pendiente.

```json
{"version":1,"bindings":[
  {"key":"<SHA-256 de 64 caracteres observado y revisado>","decision":"replace-pilot","sheet":7,"frame":0}
]}
```

El marcador del ejemplo no es una clave válida. `replace-pilot` exige jugador, pose 16×14, hoja/frame del activo, sin vehículo/destrucción y los offsets originales soportados; admite todos los slots y recortes del compositor. `keep-associated` solo permite claves exactas de marcador 0x7C o tipos/hojas asociados expresamente enumerados. No permite ignorar cuerpos o civiles desconocidos.

Activación interna: captura/publicación de misión, densidad HD 8/12 y `OPENFODDER_SOLDIER_ORDERED_MANIFEST` con ruta al JSON. `OPENFODDER_ORDERED_KEYS=1` registra claves únicas, máximo 8192 por proceso; `OPENFODDER_HD_DIAGNOSTICS=1` registra motivos. El manifiesto vacío `tools/modernization/ordered-empty-bindings.json` prueba el rechazo y no sustituye soldados. El lanzador de Miguel no se modifica ni se entrega como corregido.

El método real verifica el contraste clásico independiente, resuelve todos los comandos del destino y rechaza faltantes antes de la composición CPU o carga GPU. Si el intervalo tiene recursos suficientes, compone y publica en orden. Un fallo de carga no reutiliza otro manifiesto; esta rama nunca cae al piloto. Continúan los guards de pausa, mapa, paleta y renderer, pendientes de tratamiento posterior.

Las pruebas del método real incluyen vectores SHA-256, identidad estable con movimiento/agua/generación, sensibilidad a bytes/paleta/persona/offset, límites del recurso, duplicados, intento de conservar un cuerpo, varios soldados, agua, oclusión, faltantes y reentrada. Comparación exacta con lienzo HD expandido a escala entera. El runner `check_mission_publication_replays.py --ordered-manifest ...` comprueba ruta y H3, manteniendo cobertura artística `PENDING`; CI añade las primeras fases PC/Amiga con pausa. Un PASS de rechazo por manifiesto vacío no es una prueba de publicación HD real ni cobertura completa.
