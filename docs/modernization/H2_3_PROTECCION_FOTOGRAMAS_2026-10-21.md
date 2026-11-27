# H2.3 — Protección de tablas de fotogramas (21 de octubre de 2026)

**Estado:** corrección focalizada integrada y validada en Linux. H2.3 global **continúa abierta** por avisos UBSan y cobertura/fugas pendientes. La rama y PR #1 siguen en borrador. No se ha cambiado el arte HD ni el renderizador moderno.

## Diagnóstico y cambio aplicado

En `Source/Sprites/Sprite_Core.cpp`, `Sprite_Get_Sheet` devolvía `&mSprite_SheetPtr[tipo][fotograma]` sin conocer ninguna de las dos dimensiones. La ejecución anterior detuvo ASan por una lectura `global-buffer-overflow` en `Sprite_Draw_Frame` línea 85 después de 11 fases, junto a arrays `stru_8E238`/`stru_8E248` de Amiga.

Se han inventariado las **590 declaraciones de arrays de fotogramas** (293 Amiga y 297 PC), **15 tablas de selección** (8 Amiga y 7 PC), con **1.309 referencias a secuencias** (768 Amiga y 541 PC). No se detectaron discrepancias entre tamaños de arrays explícitos y sus inicializadores; no se han añadido límites arbitrarios.

- `Source/Amiga/SpriteData_Amiga.hpp` y `Source/PC/SpriteData_PC.hpp` contienen tablas `*_FrameCounts` cuyos elementos son `sizeof(array)/sizeof(array[0])` y llevan `static_assert` del tamaño de cada grupo.
- `SetActiveSpriteSheetPtr` registra la tabla de selección, los tamaños reales de fotograma y la cantidad de tipos mediante la plantilla que verifica en compilación que ambos arrays coinciden.
- `Source/Amiga/Graphics_Amiga2.cpp` usa el helper `SetActiveCF2SpriteSheet` de su clase base para activar la tabla CF2 sin tamaños duplicados ni límites fijos.
- `Sprite_Get_Sheet` valida tanto `tipo` como `fotograma`, devuelve `nullptr` si están fuera de rango y muestra un máximo de 24 avisos. `Sprite_Draw_Frame` no desreferencia el resultado inválido y asigna `mWasDrawn=0`; el dibujo válido sigue el código clásico sin cambios. El código de overlays Amiga omite un fotograma inválido.
- `check_visibility_contract.py` y el contrato H3.6 se actualizaron de 14 a **15 apariciones** documentadas de `mWasDrawn`. La independencia futura del dibujo de alta frecuencia sigue siendo H4.

**Código:** [commit de protección 6306abc](https://github.com/Cacheirez/openfodder/commit/6306abcecd7fdc615d416cfedb22aa78f32eb57c), [tests/CI 768343f](https://github.com/Cacheirez/openfodder/commit/768343f7f271b522465ff7d515b707bffedc920f), [ruta CF2 f956596](https://github.com/Cacheirez/openfodder/commit/f95659607cdeb74a6d0a8396667a8b305297dbda).

## Evidencia de pruebas

**GitHub Actions Linux** [run 39615453699](https://github.com/Cacheirez/openfodder/actions/runs/39615453699). Comprobaciones terminadas correctamente:

- Compilación nativa Linux, test de límites de fotogramas y prueba independiente de tabla de direcciones.
- Auditoría estática de los 590 arrays y 1.309 referencias, con la ruta CF2 incluida.
- Auditoría H3.6 de visibilidad, suite RNC acotada con sanitizadores y replays H3.
- PC Format y Amiga The One generan los **11.361 estados** de la referencia fijada previamente: no se reescribió la referencia.
- Motor completo `build-h2-asan`, compilado con AddressSanitizer + UndefinedBehaviorSanitizer, `ASAN_OPTIONS=detect_leaks=0`. `h2-engine-asan/report.json`: **29 fases completadas, cero omitidas, returncode 0, verdict PASS**. El `engine.log` no contiene `ERROR: AddressSanitizer` ni un error fatal de lectura como el anterior.

El registro ASan identificó dos referencias inválidas de animación durante las pruebas, ahora rechazadas antes del acceso: **tipo 124/fotograma 13** (8 fotogramas disponibles) y **tipo 185/fotograma 1** (1 disponible). El log limita los avisos a 24; no son 24 instancias necesariamente distintas.

**Importante:** el veredicto `PASS` del script de replays certifica finalización correcta y ausencia de fatal; **no certifica ausencia de errores UBSan**. En el mismo `engine.log` hay **23 líneas `runtime error:`**, desglosadas en 6 índices fuera de límites, 15 desplazamientos a la izquierda de valores negativos y 2 lecturas desalineadas de enteros. Ejemplos: `Sprite_Core.cpp` con índice 9 en array de nueve punteros, `PC/Resource_PC_CD.cpp` con índice 694/940/627 en array de 627, `Utils/pseudorand.hpp`, cámara y mapa para desplazamientos de valores negativos, y `stdafx.hpp:92` para lecturas desalineadas.

Por lo tanto **H2.3 permanece abierta**. La suite integral todavía no es limpia bajo UBSan y no se ha activado el detector de fugas. Es necesario separar la corrección de las siguientes anomalías de los cambios de animación.

**Windows** [run 39615453561](https://github.com/Cacheirez/openfodder/actions/runs/39615453561): en cola de GitHub Actions durante esta revisión. No afirmar compilación ni replays Windows verificados para la revisión CF2 hasta que termine esta ejecución.

## Siguiente hito

1. Inspeccionar los accesos de índice 9 de `Source/Sprites/Sprite_Core.cpp` y los índices de `Source/PC/Resource_PC_CD.cpp`, con pruebas focalizadas y sin modificar valores de referencia válidos.
2. Corregir las operaciones de desplazamiento negativo y alineación con equivalencia aritmética comprobada.
3. Endurecer el indicador de CI para que un `runtime error:` de UBSan no quede presentado como suite integral libre de defectos aunque el proceso finalice con código 0; reportar por separado ASan, UBSan y LeakSanitizer.
4. Repetir CI Windows y Linux y conservar la referencia H3 existente. Completar H2.1/H2.4 antes de aceptar H2.6; mantener H4 aún pendiente.
