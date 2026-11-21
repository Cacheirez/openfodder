# H2.3 — Corrección de índices de dirección y nuevo diagnóstico ASan/UBSan

**Fecha:** 21 de octubre de 2026 · **Código examinado:** `696e0a4f7ae7fe5961cedc1f75aadafd5c1c419f`.
**Estado:** corrección de tabla de direcciones verificada para el alcance de pruebas; **H2.3 global abierta** por un nuevo defecto de sprites. Se mantiene la rama `modernization/windows-foundation` y PR #1 en borrador.

## Causa y corrección

`Source/MapData.cpp` contiene `mMap_DirectionsBetweenPoints` con **1024 entradas** distribuidas como una matriz **32 × 32**. `Direction_Between_Points` en `Source/Fodder.cpp` examinaba inicialmente solo los bits 9 a 0 de la distancia absoluta; para distancias mayores, el valor ensamblado `(y << 5) | x` podía superar 1023. `Direction_Between_Points_LUT` en `Source/Camera.cpp` usa la misma tabla y también normalizaba mediante operaciones con `int16` que podían desbordarse antes de calcular el índice.

La función auxiliar pura `Source/Utils/DirectionLUT.hpp`, `directionLutNormalize`, determina el bit más significativo sobre magnitudes enteras ampliadas (`int32` de diferencia con magnitud calculada usando `int64`), desplaza ambos ejes lo necesario para limitar `x,y` a 0–31 y construye un índice entre 0 y 1023. Se aplica en **ambas** rutas de consulta. No cambia el cálculo posterior de cuadrantes ni las tablas de direcciones ni `mWasDrawn`. `MapData.cpp` declara una comprobación estática de tamaño de la tabla.

## Pruebas de límites

- `tools/modernization/test_direction_lut.cpp` prueba de forma exhaustiva **1.048.576 pares** de magnitudes de 0 a 1023 contra la normalización previa y otros **14.641** conjuntos de coordenadas extremas de 16 bits: **1.063.217 casos**. También comprueba el vector cero, el último índice y la diferencia máxima de 65.535 entre coordenadas.
- La misma prueba sintética local pasó con **GCC y Clang**, `-fsanitize=address,undefined`.
- Se añadió un target independiente `openfodder_direction_tests` mediante CMake/CTest. `ctest` pasó en Linux normal, Windows x64 Release y Linux ASan/UBSan.
- [Windows Actions 39608816475](https://github.com/Cacheirez/openfodder/actions/runs/39608816475): compilación, test de límites, **29 replays demo**, dos dobles replays H3 y comparación con las **11.361 huellas** anteriores, PASS.
- [Linux Actions 39608816538](https://github.com/Cacheirez/openfodder/actions/runs/39608816538): compilación, CTest, auditoría RNC acotada, doble replay H3 y comprobación del baseline anterior, PASS.
- No se actualizaron ni regeneraron huellas de referencia H3: se usaron las **anteriores a los cambios H2**.

Estas pruebas acreditan la normalización de índices y el comportamiento en las fases ensayadas, no la ausencia de defectos en todo el motor.

## ASan/UBSan del motor completo tras corregir direcciones

La suite se ejecutó nuevamente en Linux mediante `build-h2-asan` (ASan + UBSan, `ASAN_OPTIONS=detect_leaks=0`) y su informe **es FAIL**, aunque el workflow exterior muestre SUCCESS por `continue-on-error: true`.

El primer bloqueo anterior `Source/Fodder.cpp:2863`, `Direction_Between_Points`, **no aparece** en este registro. Tras **11 fases completadas**, el siguiente fallo fatal es:

- **`AddressSanitizer: global-buffer-overflow`, lectura de 2 bytes** en `cFodder::Sprite_Draw_Frame`, `Source/Sprites/Sprite_Core.cpp:85`.
- Traza de llamada: `Sprite_Draw_Frame` → `Sprites_Draw` → `Mission_Sprites_Handle` → `Phase_Cycle` → `Phase_Loop`, durante **Amiga Power Alien Levels**.
- El informe sitúa la lectura junto a estructuras `stru_8E238` y `stru_8E248` de `Source/Amiga/SpriteData_Amiga.hpp`. **La causa exacta del índice o fotograma inválido no está aún determinada**; la llamada `Sprite_Get_Sheet(pSpriteType,pFrame)` debe auditarse antes de elegir la corrección.
- UBSan también informa de accesos con **índice 9** a arrays de **nueve punteros** en `Source/Sprites/Sprite_Core.cpp:2020, 2151, 2154` y varios **desplazamientos de bits de valores negativos** en RNG, cámara, sprites y mapa. Son incidencias independientes que no deben corregirse sin pruebas de equivalencia.

**Evidencia primaria:** [artefactos Linux 39608816538](https://github.com/Cacheirez/openfodder/actions/runs/39608816538) → `OpenFodder-Linux-H3-evidence` → `h2-engine-asan/engine.log` y `report.json`. El informe registra `phases_passed=11`, `returncode=1` y `verdict=FAIL`.

## Próxima intervención acotada

1. Auditar `Sprite_Get_Sheet`, las longitudes reales por tipo/fotograma y los llamadores, incluyendo los recursos de Amiga Power Alien Levels, **sin publicarlos**.
2. Introducir protección comprobable del acceso a datos de sprites preservando resultados para animaciones válidas.
3. Añadir tests focalizados y repetir las dos CI y la prueba completa ASan/UBSan, registrando el siguiente primer fallo si apareciese.
4. Después, revisar los avisos UBSan y la sincronización H2.4 por separado.

**No declarar H2 finalizada; no comenzar aún la sustitución gráfica H4.**
