# H2.3 — Lecturas sin alineación y desplazamientos negativos (21-10-2026)

**Estado técnico:** los **17 avisos UBSan** remanentes se han corregido en las rutas ensayadas. Linux: **29/29 replays, 0 avisos UBSan, 0 errores AddressSanitizer, retorno 0**. Windows x64: compilación, 29 replays y H3 PASS. **H2.3 integral permanece abierta** por falta de pruebas de fugas (`detect_leaks=0`), cobertura limitada de campañas y rutas no ensayadas.

## Hallazgo y corrección: alineación (2/2)

El método `readLE<T>` en `Source/stdafx.hpp:92` realizaba un `reinterpret_cast` implícito de bytes a un puntero `T*` y desreferenciaba una dirección a veces no alineada. Eso provocaba dos `runtime error: load of misaligned address` al leer `unsigned int`.

- `Source/Utils/EndianIO.hpp`: carga de byte a byte en little-endian con preservación exacta de los bits para tipos enteros con signo o sin signo. Evita el acceso desalineado y no asume el endianness del anfitrión.
- `writeLEWord` ahora usa una escritura de dos bytes, también independiente de la alineación.
- `test_endian_io.cpp` comprueba **262.144** combinaciones de valores y offsets, más casos de 32 bits y negativos. GCC y Clang + ASan/UBSan: PASS.

Código: [a930a72](https://github.com/Cacheirez/openfodder/commit/a930a725db2c23877763b0044803b3bd7d57f3ac).

## Hallazgo y corrección: RNG (4/4)

En `Source/Utils/pseudorand.hpp`, los desplazamientos a la izquierda de `Data2`, `Data4` y otros registros podían operar con valores negativos; en C++ eso es comportamiento indefinido. Para preservar la reproducción determinista:

- Se construyen registros de 32 bits con desplazamientos de **palabras sin signo** y la extensión de signo explícita del término bajo.
- El desplazamiento de estado de 16 bits usa `wrapShiftLeft16`, que conserva el patrón binario tras el truncamiento a 16 bits.
- `test_rng_bit_exact.cpp` fija un digest FNV de **262.144 llamadas** y verifica el estado interno completo de cuatro palabras. Se obtuvo la huella comparando la implementación clásica bajo GCC y Clang en O0/O2. No actualizarla al modificar el RNG.

Código: [0f930da](https://github.com/Cacheirez/openfodder/commit/0f930da0a67e5bc10764a5a3bb689ebdf6691264); ajuste de orden de parámetros de la prueba [93c6a83](https://github.com/Cacheirez/openfodder/commit/93c6a832c66d34e50f109e16bc764952dd8ff9db).

## Otros desplazamientos negativos (11/11 observados)

`Source/Utils/SignedBits.hpp` define `wrapShiftLeft16`, `wrapShiftLeft32` y `packWords32`, usando bits sin signo y copia definida de la representación binaria. Se reemplazaron los lugares registrados por UBSan en:

- `Source/Camera.cpp`: combinación de componentes de 32 bits en el límite de la cámara.
- `Source/Map/MapRuntime.cpp`: desplazamiento de coordenadas hacia el espacio gráfico.
- `Source/Sprites/Sprite_Core.cpp`: direcciones, coordenadas fraccionarias y empaquetado de posiciones.
- `Source/Sprites/Sprite_Helicopter.cpp`: ajuste de dirección.
- `Source/Sprites/Sprite_Vehicle.cpp`: campo de posición fija y velocidad.
  
`test_signed_bits.cpp` comprueba **196.706** transformaciones de bits/valores límite de 16 y 32 bits con GCC y Clang bajo ASan/UBSan, PASS.

Código: [0acb947](https://github.com/Cacheirez/openfodder/commit/0acb947d73e668ec4baa5d4c0e5100cdf598f46b).

## Evidencias integradas

- [Linux Actions 39629941582](https://github.com/Cacheirez/openfodder/actions/runs/39629941582), artefacto [OpenFodder-Linux-H3-evidence](https://github.com/Cacheirez/openfodder/actions/runs/39629941582/artifacts/12358742901).
  - Los seis tests de CTest pasan tanto en compilación normal como bajo ASan/UBSan.
  - Campañas demo PC Format y Amiga The One, comparación y baseline H3 **11.361 estados sin diferencias**.
  - Motor completo: **29 fases PASS, sin errores `ERROR: AddressSanitizer`, sin `runtime error:` de UBSan**, `returncode=0`. El ZIP de evidencia fue descargado y verificado con CRC correcto; `report.json` y `engine.log` inspeccionados.
- [Windows Actions 39629941637](https://github.com/Cacheirez/openfodder/actions/runs/39629941637): compilación x64, seis pruebas CTest, **29 replays**, H3 doble ejecución y comparación baseline, **SUCCESS**.
- [Linux previo 39629089130](https://github.com/Cacheirez/openfodder/actions/runs/39629089130): tras endian/RNG y antes del resto de desplazamientos, UBSan bajó **17→11**; mismo baseline H3.
- Se preservó `tools/modernization/reference-gameplay-v1.json` sin rebaselinar.

**No equivale a ausencia general de comportamiento indefinido:** UBSan solo observa rutas ejecutadas, LeakSanitizer permanece desactivado y no hay cobertura de todas las 72 fases comerciales CD32. Se conservan también H2.1 (atribución histórica de fallo RNC) y H2.4 (revisión integral de sincronización).

## Endurecimiento del criterio CI

`tools/modernization/check_ubsan_indices.py` deja de limitarse a índices: **cualquier `runtime error:` UBSan o `ERROR: AddressSanitizer` falla la ejecución**, además de fases ausentes/errores. Se elimina `continue-on-error: true` del paso del motor instrumentado. `test_ubsan_index_gate.py` incorpora el rechazo de avisos UBSan de alineación/desplazamiento.

La compuerta de CI nueva debe validarse en su propio commit posterior al código ya comprobado; no atribuir a ese cambio meramente documental una prueba aún no terminada.

**Continuidad:** estudiar LeakSanitizer en un ejecutor compatible, H2.4 y el alcance de campañas antes de declarar H2.6. No iniciar H4 hasta la decisión explícita de estabilidad.
