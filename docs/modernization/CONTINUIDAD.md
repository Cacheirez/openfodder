# Estado operativo — 5 de noviembre de 2026

**Plan vigente 2.74. A3 activo; A1/A2/A3/A4 y A/H7 abiertos.** La alternancia del piloto de Miguel no está resuelta ni aceptada como producto completo. El lanzador sigue usando el lote antiguo; no hay ZIP nuevo de soldados completos.

## Rama y avance publicado

- `Cacheirez/openfodder`, rama `modernization/windows-foundation`; PR #1 abierta, borrador y sin fusionar.
- Último commit de implementación verificado: **`8d09a28dd24573789619ce71af94649451d51ca8`**, posturas normales y 24 poses de granada, sobre `1e1f021845457a9209b20eafa9ad6700f9748c2f` (arreglo del fetch clásico). Los cambios del bloque están publicados en esa rama.
- Este relevo modifica únicamente documentación y añade la comprobación remota de CI. Su commit se identifica con `git log -1 --format=%H -- docs/modernization/CONTINUIDAD.md`; no confundirlo con el commit de implementación anterior. Verificar siempre HEAD remoto y CI viva.
- Source del motor, jugabilidad, relojes, RNG y referencias originales no cambian. Base clásica `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`; H3 previo conserva 11 fases / 11.361 estados (7.956 PC + 3.405 Amiga) y 22 pausas/reanudaciones. No se repite H3 completo en este bloque de arte/herramientas.

## Completado y límites

- A1/A2: inventario, captura de todos los slots, compositor ordenado, resolución por recurso/paleta, activos externos v2 y censo transaccional SDL implementados. Siguen pendientes cobertura/rutas, transiciones y GPU. [Contrato de cobertura](SOLDADOS_COBERTURA_COMPLETA.md).
- A3: **24 poses de marcha, ocho de apuntado bajo y 24 de lanzamiento de granada**, preparadas y revisadas internamente. 112 activos 8×/12× y 222 vinculaciones. Los 64 activos previos de marcha/apuntado, incluido C01, conservan sus bytes. [Fuentes, prompts, visor y reproducción de granadas](../../assets/modernization/soldier-grenade/README.md).
- Quietud y disparo normal reutilizan los frames que selecciona el original; apuntado bajo usa la tabla `0x30`. La tabla `0x40` mantiene su alcance especial, no se presenta como reposo normal.
- **Modo de escuadrón 0:** revisión de las diez referencias de `word_3BED5`; solo cinco escrituras, todas inicializan a 2. No se ha localizado una ruta normal CF1 que lo active. Sus ramas de animación, parada y salida se prueban sin producir un lote ficticio de posturas normales. No es una prueba contra alteraciones externas de memoria/estado. [Auditoría](evidence/soldier-normal-postures-audit.json).
- Granada: ocho direcciones × tres claves, selección original **0,0,1,1,2,2** y retorno a la postura original. No se modifica la creación, trayectoria ni reloj del proyectil separado. El primer ciclo se verificó antes de ampliar las otras siete direcciones. Se rechazó `g5-f1.png` por invertir el rifle; solo `g5-f1-v2.png` se vincula en su lugar.
- Claves: marcha 94 observadas; apuntado 32 reconstruidas (11 coinciden con el censo previo); granada 96 reconstruidas (34 coinciden). Las restantes reconstrucciones usan tablas/bytes/paletas reales verificados, no se atribuyen a observación de replay. Datos originales, paletas y comparaciones nativas quedan locales.

## Validación del bloque

[Informe, hashes y alcance de sanitizadores](evidence/soldier-grenade-validation.json).

- Selectores extraídos de las fuentes actuales y contrastados con la base clásica: **272 aserciones y 168 muestras** en ocho direcciones; incluye posturas, disparo/cooldown, modo 0 y lanzamiento. Geometría/dirección al objetivo simuladas en la fixture; no acredita interacción completa de campaña. Aserciones conservadas en Release.
- Método real WindowHD/SDL, dos soldados con fases/direcciones independientes, solapamiento, recorte y oclusión, 8×/12×: **1.344 intervalos/2.688 cuerpos controlados y 1.260/2.520 con recursos reales**. Tres rechazos transaccionales por modo: tipo, estado y paleta sin vincular. La expectativa SDL reutiliza el compositor CPU previamente probado; no es un oráculo anatómico independiente.
- Tres grupos reales recorren ocho direcciones; en el cuarto se omiten dos pares porque siguen faltando dos claves ordinarias Amiga de marcha. No se inventan. Las 24 poses nuevas de granada sí existen.
- Compatibilidad del helper ampliado a más familias: conserva la clave anterior de apuntado cuando se omite el frame. Comparación de los 64 activos previos exacta. Nuevos CTests: `soldier_grenade_original_selection` y `soldier_grenade_art`.
- No equiparar estas publicaciones aisladas a publicación HD de una campaña completa. Aceptación visual nueva de Miguel, GPU y CD32 **PENDIENTES**. Consultar el informe para resultados locales ASan/UBSan y la limitación de LSan; no atribuir ausencia de fugas si no se ha medido.

## CI real comprobada para el relevo

Comprobación remota del 5 de noviembre, ligada a **`8d09a28dd24573789619ce71af94649451d51ca8`**: los tres workflows han terminado con **success**.

| Workflow | Ejecución | Resultado |
|---|---|---|
| Windows - modernization foundation | [42034593717](https://github.com/Cacheirez/openfodder/actions/runs/42034593717) | PASS; fetch clásico, build, pruebas, H3 y preparación del paquete de demo existentes |
| linux-build | [42034593370](https://github.com/Cacheirez/openfodder/actions/runs/42034593370) | PASS; build, pruebas, H3 y diagnósticos de sanitizadores existentes |
| H6 - offline density review | [42034593520](https://github.com/Cacheirez/openfodder/actions/runs/42034593520) | PASS |

[Comprobación y alcance](evidence/handoff-20261105.json). Se han consultado los resultados y pasos ya ejecutados; no se han relanzado pruebas ni investigaciones. El fallo anterior por referencia clásica ausente queda resuelto por el fetch previo al build y la CI posterior. Los informes locales conservan el estado que tenían al generarse; esta sección los actualiza para el commit indicado.

Los pasos LSan de la CI Linux existente pasan, pero no sustituyen la medición LSan pendiente de las fixtures locales nuevas de granadas. Los paquetes automáticos de demo conservan el piloto anterior; no son una entrega de soldados completos. La CI de este relevo documental se consulta por separado, sin atribuirle los resultados del commit de implementación.

## Pendientes y siguiente tarea

1. **Lanzacohetes del jugador:** contrastar selección original en offset `0x38`, frames/direcciones y retorno. La tabla contiene una dirección de cuatro entradas; comprobar uso real antes de encargar cuatro imágenes. Reutilizar contratos, maestros y diagnóstico existentes.
2. Después, agua, daño/muerte, enemigos y variantes. Clasificar proyectiles y elementos asociados por separado. No asumir cobertura total por tener 56 poses de tres familias.
3. Completar las dos claves ordinarias Amiga 6/0 y 6/2 del recurso `3e0bf624…`, rutas/transiciones excluidas, GPU/densidad final y CD32. La vista completa sigue recuperándose al clásico si falta cualquier clave necesaria.
4. Mantener estilo C — Pintado moderado; solo C01 tiene aceptación del usuario. 12× de trabajo y 8× alternativa. No repetir selección de estilo, censo completo ni pruebas concluidas sin regresión concreta. No cambiar el lanzador ni cerrar A/H7 hasta cobertura y recorrido continuo pertinentes.

## Recuperación y continuación

El checkout anterior se documentó en `/workspace/scratch/a4e0bfdd2e06/openfodder`. **En este relevo no hay entorno de ejecución local disponible**: no se ha podido ejecutar `git status`, inspeccionar archivos sin seguimiento ni exportar nuevos parches/bundles. No se certifica que aquel checkout esté limpio ni que cualquier cambio local desconocido esté respaldado. El código/arte y las pruebas revisados aquí son los publicados en GitHub. Los bytes y capturas nativas locales no son entregables públicos.

Si el checkout vuelve a estar disponible, antes de limpiarlo o cambiar de rama:

1. Ejecutar `git status --short --branch`, `git log --oneline origin/modernization/windows-foundation..HEAD` y revisar los archivos sin seguimiento.
2. Guardar `git diff --binary HEAD` como parche, `git bundle create recuperacion.bundle --all` para commits locales y un archivo de los archivos sin seguimiento necesarios, con hashes y SHA de base. Separar datos privados/comerciales.
3. Publicar únicamente cambios válidos en commits coherentes; registrar cualquier resto y su recuperación. No aplicar a ciegas el archivo antiguo descrito abajo.

No se ha creado código local nuevo en este relevo; los cambios documentales se publican mediante GitHub. Una nueva clonación recupera el trabajo publicado, pero no recupera modificaciones desconocidas del checkout anterior.

El intento antiguo `c81d19f0fca7` sobre `db8a910`, con poses 3/2 y 5/2 rechazadas, quedó sustituido por los bloques posteriores. No aplicarlo sobre HEAD. Recuperación conservada en **OpenFodder_recuperacion_local_20261105.zip**, 71 entradas, SHA-256 `05ad629a90694b2c52a55ed49f82f739e6ef6caac6f34a68567d8e4e32e7ef31`; incluye instrucciones, parches y archivos locales de aquel intento y salidas/temporales antiguos. No se considera trabajo nuevo entregado.

[DESARROLLO.md](DESARROLLO.md) contiene preparación/pruebas. Se puede continuar con [PROMPT_NUEVO_HILO.md](PROMPT_NUEVO_HILO.md), GitHub conectado y sin adjuntos obligatorios.
