# D3 — diagnóstico Windows: x64 resuelto, x86 acotado

**7 de noviembre de 2026.** HEAD `12740d002755e2bc6bdcb7aa19ebcb285f7c9ed6`, PR #1 abierta/borrador/sin fusionar. Sin commit/publicación, sin cambiar Source, referencias ni maestros. No se ha activado otro modelo ni subagentes.

## Validación posterior a JSON completada — sin limitación de interceptación x86

**PASS:** Windows LLVM23 x86 y x64 ASan/UBSan, matriz controlada y real; Linux Clang18 ASan/UBSan/LSan con `detect_leaks=1`, ambos modos. Cada modo completa 7.920 intervalos/15.840 cuerpos, 360 secuencias, tres rechazos transaccionales y selector 2.703/576. Sin hallazgos ni advertencias de runtime; 142 activos RGBA/descriptores y 282 vínculos exactos. H3 recompilado: 11 fases/11.361 estados PASS contra las referencias existentes.

El paquete binario LLVM23 no incluía ASan i386. Se construyó el runtime oficial desde `llvm-project-23.1.5.src.tar.xz`, SHA-256 `fb50b1eac93ddeb3aa8dab4cfe324dff74f4a9c2bdee6160c9e36188f8d06a6e`, coincidente con digest del release. CMake/Ninja, clang-cl23 con target i686 y entorno vcvars x86; `COMPILER_RT_DEFAULT_TARGET_ONLY=ON`, sanitizador asan, sin tests/XRay/libFuzzer/profile/memprof. Fuente y build permanecen fuera de Git. Configuración exacta en `asan23-i386-build/CMakeCache.txt`; configuración y build logs conservados. `stl_asan.lib` i386 se compiló /MD desde la fuente oficial instalada, ambas anotaciones true. El runtime nuevo se añadió solo a la copia portable local de LLVM23, sin cambiar Visual Studio ni el sistema.

Controles positivos del runtime nuevo: container-overflow ASan e integer-overflow UBSan detectados, exit 1, sin advertencia de interceptación. La matriz Clang19 anterior también terminó pero emitía advertencia; queda como antecedente, sustituida por esta pasada LLVM23 sin advertencia. No se excluyeron comprobaciones ni se usó el reporter diagnóstico en la validación. Fugas comprobadas en Linux; no se afirma LSan Windows.

Recuperación: `build_post_json_windows.ps1`, `post_json_linux.sh`, `run_post_json_x64.ps1`, `run_asan23_x86.ps1`, `asan23-i386-build`, `asan23-x86`, salidas `validation-d3-asan23-x86-*`, `validation-d3-post-json-x64-*`, trabajo Linux `/root/openfodder-d3-linux/post-json-*`, `post-json-h3`, y resumen `post-json-validation-results.json` con hashes. No repetir estas pruebas salvo regresión.

Las limitaciones de sanitización aquí diagnosticadas quedan resueltas para la matriz local. Permanecen commit/publicación/CI nueva, compilación completa de producción/audio/GPU/CD32/campaña y aceptación jugando. No se cierra D3 ni se abre D4, no se ha publicado nada.

## Integración autorizada — matriz x86 UBSan PASS

Integradas en `Source/Utils/json.hpp` las referencias de callback y las dos sobrecargas de asignación revisadas: copia con temporal y movimiento con temporal local antes del swap. Autorización explícita del usuario para esta excepción al límite de Source de D3. No se ha cambiado simulación ni referencias. El header cambia firmas: recompilar consumidores, sin afirmar compatibilidad binaria con objetos previos.

Fixture y selector recompilados para **i686, LLVM23, /MD, O1, UBSan completo en modo trampa** contra Source integrado. Matrices controlada y real **PASS 7.920 intervalos/15.840 cuerpos por modo**, 360 secuencias, tres rechazos transaccionales y selector 2.703 aserciones/576 muestras. Sin advertencias ni hallazgos; 142 activos/descriptores RGBA y 282 vínculos exactos. No se utilizó reporter personalizado, exclusión de alignment ni /NODEFAULTLIB para estos resultados.

Test persistente `tools/modernization/test_json_alignment.cpp`: copia/movimiento/autoasignación, valores anidados, callback, roundtrip y error de entrada; UBSan i686 y x64 O2 PASS. Control positivo con mismos flags i686 detecta overflow (`0xC000001D`). Este PASS es **UBSan, no ASan**: LLVM23 carece de runtime ASan i386. La cobertura ASan x86 y la validación amplia posterior a cambiar JSON permanecen pendientes; los PASS previos Linux/x64/H3 corresponden al Source anterior.

Reproducción en la carpeta local habitual: `run_integrated_x86.ps1`, `integrated-x86/{fixture.exe,selector.exe,json_regression.exe}`, logs de compilación, salidas `validation-d3-integrated-x86-controlled` y `validation-d3-integrated-x86-real`, `integrated-x86-results.json` con hashes. Compilar el test con `clang --driver-mode=cl --target=i686-pc-windows-msvc /MD /EHsc /std:c++17 -O2 -fsanitize=undefined -fsanitize-trap=all -I Source tools/modernization/test_json_alignment.cpp` desde la raíz.

Sin commit/publicación, sin cierre D3 ni D4. No hace falta escalado adicional para esta integración.

## Corrección aislada del paso por valor — mínimo JSON PASS

La copia `x86-candidate-v2/json.hpp` conserva los callbacks por referencia del candidato anterior y sustituye `operator=(basic_json other)` por dos sobrecargas: copia desde `const basic_json&` y movimiento desde `basic_json&&`. Ambas preparan un temporal local antes del intercambio original; se conserva el tratamiento del origen movido y la autoasignación. La copia puede lanzar como antes durante la construcción del parámetro; la sobrecarga de movimiento conserva la condición noexcept original. Es un cambio de firmas en un header de terceros: requiere revisión de integración y recompilar sus consumidores; estos resultados no acreditan compatibilidad ABI con binarios previos.

**PASS LLVM23 UBSan-trap completo**: mínimo JSON i686 O1 exit 0; pruebas focalizadas i686/x64 O1/O2 exit 0, con asserts activos. Verificados copia independiente, movimiento y origen null, autoasignaciones, valores anidados, roundtrip y excepción de entrada inválida. Control positivo nuevo, mismos flags: overflow termina con `0xC000001D`. No se ha suprimido alignment ni usado el reporter personalizado para estos PASS. ASan x86 y la matriz WindowHD/SDL siguen pendientes.

Recuperación en la carpeta local habitual: `prepare_x86_assignment.py`, `json_alignment_candidate_v2.cpp`, `json_assignment_checks.cpp`, `x86-candidate-v2/json.hpp`, `x86-candidate-v2/assignment.patch`, `x86-assignment-results.json`, logs `win23/json-v2-*.log` y `win23/json-checks-*-*.log`. El parche de asignación es incremental sobre el candidato de callbacks, no sobre Source original. Source intacto, sin commit/publicación. Siguiente paso: revisar la integración conjunta antes de validar la matriz; no abrir D4.

## Localización posterior — comprobación concreta encontrada

La variante JSON con callbacks por referencia falla en **`x86-candidate/json.hpp:5485:35`**, expresión `*object_element = BasicJsonType(std::forward<Value>(v));`. El reporter recibe tipo `nlohmann::basic_json<>`, kind=5 (llamada de método), alineación exigida 8 y dirección módulo 8 igual a 4; termina con exit 86. La asignación declara `operator=(basic_json other)` por valor en la línea 18661. La IR original O1/UBSan-trap conserva ubicaciones de la línea 5485 y bloques `inalloca` de basic_json con align4. El siguiente punto de investigación es ese paso por valor, no ampliar a ciegas el cambio de callbacks.

Método diagnóstico: LLVM23 conserva `-fsanitize=undefined`; `-fsanitize-trap=all -fno-sanitize-trap=alignment -fno-sanitize-recover=all` dirige alineación a un reporter explícito que imprime la metadata y aborta. Se excluyeron únicamente `clang_rt.ubsan_standalone.lib` y `clang_rt.ubsan_standalone_cxx.lib` ausentes para enlazar ese reemplazo diagnóstico. No se presenta como runtime de validación ni PASS. Cambiar reporting puede variar la disposición de pila: esto localiza un fallo concreto de la variante instrumentada, no equivale a capturar con depurador la instrucción de trampa del binario anterior.

Fuentes/log/IR y resultado: `x86-candidate/alignment_reporter.cpp`, `win23/json-report-run.log`, `win23/json-candidate-trap.ll`, `x86-exact-location.json` en la carpeta local de recuperación. Parche sin ampliar; Source intacto; matriz pendiente. El diagnóstico solicitado queda listo para volver al modelo habitual.

## Seguimiento x86 — dos hipótesis comprobadas, corrección aún pendiente

Local `12740d0`; PR remota `a8268ff`, abierta/borrador/sin fusionar. El avance remoto solo cambia AGENTS.md (recomendación de hilo nuevo tras cierre). No se ha mezclado con los cambios locales.

1. LLVM23 i686, `-O1 -fsanitize=undefined -fsanitize-trap=all`, añadiendo `-mstackrealign -mstack-alignment=16`: compila, el mínimo original sigue terminando en `0xC000001D`.
2. Variante aislada pasando callbacks por referencia constante: el mínimo `std::function` pasa; el mínimo JSON con copia privada del header y las firmas de callback adaptadas sigue terminando en `0xC000001D`. **No es una corrección válida para integrar.** No se afirma que la trampa restante tenga la misma localización: falta localizarla.

Los builds y ejecuciones se completaron fuera del sandbox; el fallo no corresponde a permisos. No se desactivaron checks ni se alteró Source. No se ejecutó la matriz porque el mínimo JSON aún falla. Resultados en `x86-followup-results.json`, fuentes `function_alignment_candidate.cpp`, `json_alignment_candidate.cpp`, copia `x86-candidate/json.hpp`, diff `x86-candidate/json-reference.patch` y logs `win23/*candidate-*.log`, `function-realign-*.log`, en la carpeta local indicada abajo.

**Propuesta Astra Medio, sin activar**, conforme a AGENTS.md tras dos hipótesis sin resolver el bloqueo. Pregunta: ¿en qué comprobación exacta de la variante JSON x86 cae UBSan-trap, y qué corrección de generación ABI o de paso/almacenamiento de callbacks elimina todas las desalineaciones sin suprimir checks? Comparar el mínimo std::function corregido (exit 0) con JSON corregido (0xC000001D), localizar la trampa antes de ampliar el parche. No ejecutar la matriz ni modificar Source hasta disponer de una corrección demostrada y compatible con los límites del plan.

## Resultado x64 comprobado

La mezcla la introduce **el driver de Clang**, no SDL ni `stl_asan.lib`. `fixture.obj` contiene `/DEFAULTLIB:msvcrt.lib`, `RuntimeLibrary=MD_DynamicRelease` y anotaciones string/vector activas; `stl_asan.lib` también pide MSVCRT. Sin embargo, `clang -### -fms-runtime-lib=dll -shared-libasan -fsanitize=address,undefined fixture.obj` añade `-defaultlib:libcmt` y `asan_static_runtime_thunk`. El código del [driver MSVC de LLVM](https://clang.llvm.org/doxygen/MSVC_8cpp_source.html) distingue el thunk mediante `/MD` o `_DLL` explícito; el comportamiento de la instalación se verificó con `-###`, no se dedujo solo de la documentación.

Solución local verificada, reutilizando **exactamente el mismo objeto**:

```text
clang.exe --driver-mode=cl /MD -fsanitize=address,undefined -fno-sanitize-recover=all fixture.obj ../sdl/SDL3-3.4.0/lib/x64/SDL3.lib /Fe:openfodder_external_asset_sanitized.exe /link /LIBPATH:.
```

Selecciona CRT dinámico y `asan_dynamic_runtime_thunk`; enlace sin errores. No se usa `/NODEFAULTLIB`, `/FORCE`, exclusiones de sanitizadores ni se desactivan anotaciones.

- WindowHD/SDL controlado y real: **PASS 7.920 intervalos/15.840 cuerpos por modo**, 360 secuencias y tres rechazos transaccionales; sin hallazgos ni advertencias de runtime.
- Selector: **2.703 aserciones/576 muestras**. Selector recompilado con `/MD`: salida completa idéntica al selector instrumentado empleado en ambas matrices.
- Controles positivos con `/MD`: ASan detecta container-overflow y UBSan overflow de entero; ambos salen con 1, sin advertencia de interceptación.
- **142 activos RGBA/descriptores y 282 vínculos exactos** frente a la salida validada previa. Linux ASan/UBSan/LSan permanece válido, sin repetirlo.

## Diagnóstico x86 y límite que permanece

`function_alignment_repro.cpp` reduce el caso a `std::function<bool(int)>` pasado por valor a un constructor tras un puntero. No incluye JSON, SDL ni OpenFodder. LLVM23 sin sanitizar observa alineación declarada 8 pero dirección del parámetro módulo 8 igual a 4. En `-O1` con UBSan-trap termina con `0xC000001D`; el mismo caso x64 pasa. El caso x86 `-O0` pasa por disposición incidental distinta y **no constituye una solución**.

La IR local `function_alignment.ll` muestra un bloque de argumentos empaquetado `inalloca`, alineado a 4, y una llamada al constructor de `std::function` con puntero declarado `align 8`; UBSan comprueba esos 8 bytes. Esto aísla una incompatibilidad de expectativas entre el ABI x86 de MSVC, la STL y la instrumentación de Clang. La [documentación de inalloca](https://llvm.org/docs/InAlloca.html) explica ese paso de objetos; [Microsoft/STL #1533](https://github.com/microsoft/STL/issues/1533) describe un problema relacionado de alineación x86 y compatibilidad binaria, **sin afirmar que sea exactamente este caso**.

No hay base para atribuirlo al arte o selección D3, ni para etiquetarlo como falso positivo inocuo. La corrección de herramientas/ABI x86 y una matriz x86 sanitizada válida siguen **PENDIENTES**. No se cambió la firma del parser ni se suprimió `alignment`. Un intento adicional UBSan-only con Clang19 no enlazó por símbolos auxiliares del runtime; se conserva el log y no se reclama resultado.

## Recuperación reproducible

Carpeta local: `C:/Users/migue/.codex/visualizations/2026/11/06/01a1b328-fed4-7e22-8351-edd56f133b83/openfodder-d3-crops`.

- `link_windows23_md.ps1`: enlace coherente de la fixture y compilación del selector `/MD`.
- `run_windows23_sanitizers.ps1`: matrices realizadas, parámetros y recursos locales. Las carpetas de salida deben ser nuevas; el comprobador rechaza sobrescribirlas.
- `windows23-sanitizer-results.json`: hashes, contadores y controles; copia resumida en `soldier-rocket-d3-validation.json`.
- `win23/driver-before.log`, `driver-md.log`, `fixture-md-link.log`, `selector-md-result.json`, `canary-md-*.log` y carpetas `validation-d3-win23-controlled`/`validation-d3-win23-real`.
- Mínimo x86: `function_alignment_repro.cpp`; compilar con `clang --driver-mode=cl --target=i686-pc-windows-msvc /MD /EHsc /std:c++17 -O1 -fsanitize=undefined -fsanitize-trap=all`. IR con `-S -emit-llvm` en modo GNU. No necesita runtime ASan i386.

**Situación:** diagnóstico x64 resuelto y validado; diagnóstico x86 reducido, corrección pendiente. D3 permanece local, sin cierre ni D4. La propuesta anterior de Astra no se ha activado; no se solicita escalado adicional para repetir este diagnóstico.

## Antecedentes conservados — estado anterior, superado en x64

# D3 — diagnóstico pendiente de herramientas Windows

Estado: **escalado propuesto a Astra Medio; no activado**. No cambiar Source, simulación, referencias ni maestros. No desactivar comprobaciones para obtener PASS.

## Caso y resultados

- HEAD base: `12740d002755e2bc6bdcb7aa19ebcb285f7c9ed6`; rama `modernization/windows-foundation`, candidato D3 local sin commit/publicación.
- Esperado: fixture y selector Windows x64 con ASan/UBSan completos, sin advertencia de interceptación; diagnóstico del fallo JSON x86 sin ocultarlo.
- Linux x64 Ubuntu 24.04, Clang 18.1.3 y SDL 3.4.0: **PASS ASan/UBSan/LSan** en las matrices controlada y real, 7.920 intervalos/15.840 cuerpos por modo, sin hallazgos ni advertencias. `detect_leaks=1`, controles positivos de los tres sanitizadores detectan errores deliberados. Todos los 142 activos/282 vínculos coinciden con Windows. Este resultado no depende del runtime Windows.
- Windows Clang 19.1.5 x64: matrices completas PASS con advertencia `interception_win: unhandled instruction`. Los controles positivos detectan desbordamientos de vector y enteros; la advertencia se conserva como límite de cobertura.
- LLVM oficial portable **23.1.5**, archivo verificado con el digest del release: SHA-256 `62fdada7f6fa2b73856486dfbbdba3d2c1882991621615bcb55c60207611c6d4`. Sus controles positivos x64 enlazados con CRT/ASan dinámicos detectan los fallos **sin advertencia de interceptación**; el selector instrumentado compila. La fixture completa aún no enlaza correctamente.

## Hipótesis y entorno comprobados

1. Sustituir el runtime antiguo por LLVM 23 portable, con `-fms-runtime-lib=dll -shared-libasan`: el caso mínimo funciona; LLD falla en la fixture con símbolos `malloc/free` duplicados entre el thunk estático de ASan y UCRT.
2. Usar el enlazador de Visual Studio con el mismo objeto instrumentado: cambia a 16 importaciones UCRT sin resolver. Añadir UCRT explícita produce duplicados entre `libucrt.lib` y `ucrt.lib`. No se ha forzado un enlace que ignore errores ni se han desactivado anotaciones/checks.

Compilaciones ejecutadas fuera del sandbox; no se atribuyen estos errores a permisos. VS 2022 Community, MSVC 14.44.35207 y Windows SDK instalado. La instalación carecía de `stl_asan.lib` x64: se construyó localmente desde el `crt/src/stl/asan.cpp` oficial instalado, con ambas anotaciones `true`; para el caso dinámico se compiló con `/MD`. No se modificó esa fuente ni Visual Studio.

El caso JSON x86 falla con Clang 19 ASan/UBSan en `Source/Utils/json.hpp:16691` por constructor `std::function` desalineado. LLVM 23 x86 con UBSan en modo trampa también termina con `0xC000001D`; un control de overflow confirma que el modo trampa está activo. No se afirma una localización exacta de la trampa nueva. El paquete portable no incluye runtime ASan i386. No hay PASS de sanitización Windows x86.

## Reproducción local

Carpeta: `C:/Users/migue/.codex/visualizations/2026/11/06/01a1b328-fed4-7e22-8351-edd56f133b83/openfodder-d3-crops`.

- Linux reproducible: `build_linux_sanitizers.sh`, `run_linux_sanitizers.sh`, `linux_sanitizer_canary.cpp`, `linux-sanitizer-results.json`, `linux-environment.txt`. Distribución WSL `OpenFodderD3`, trabajo `/root/openfodder-d3-linux`; disco en `linux-wsl`. Conservar los recursos nativos fuera de Git.
- Windows: `win23/fixture.obj`, `fixture-object-build.log`, `fixture-build.log`, `fixture-link.log`, `fixture-link-ucrt.log`; controles `canary-address.log`, `canary-undefined.log`, `json_alignment_x86.exe` y `ubsan_canary_x86.exe`. Compiler/runtime portable en `llvm23/clang+llvm-23.1.5-x86_64-pc-windows-msvc`.
- Fuentes mínimas: `sanitizer_canary.cpp`, `json_alignment_repro.cpp`. Esta última solo incluye `Utils/json.hpp`, crea un `std::istringstream` con `{"x":1}` y lo lee en un `nlohmann::json`; no usa SDL ni D3.
- Objeto de fixture compilado con `-std=c++17 -O1 -g -fms-runtime-lib=dll -shared-libasan -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer -DOPENFODDER_EXTERNAL_ASSET_FIXTURE`, includes Source/tools, headers C01/piloto y SDL 3.4.0.
- Desde Developer Command Prompt x64, en `win23`, enlazar con el mismo clang, `fixture.obj`, `../sdl/SDL3-3.4.0/lib/x64/SDL3.lib`, `-L .`, flags CRT/sanitizadores anteriores y `-fuse-ld=link`; las variantes y errores están en los logs indicados.

Docker no pudo arrancar por un error de acceso a `dockerInference`; no se restableció ni se modificó su configuración. Se utilizó WSL independiente para no bloquear LSan.

## Pregunta concreta para Astra

¿Qué directiva u objeto introduce el CRT estático/thunk de ASan en la fixture de LLVM 23 x64 compilada para `/MD`, y cuál es el enlace coherente con este SDK que mantiene ASan/UBSan y las anotaciones de contenedor activas? Por separado, ¿el caso JSON x86 es un problema de ABI/alineación del compilador con este STL, y qué prueba mínima permite resolverlo sin cambiar la selección de juego ni suprimir comprobaciones?

`AGENTS.md` exige, tras dos hipótesis técnicas sin progreso, descartar entorno/permisos, preparar un caso reproducible y **proponer, no activar, Astra Bajo/Medio**. El informe no autoriza un cambio de modelo ni subagentes. Volver al modelo habitual tras el diagnóstico.
