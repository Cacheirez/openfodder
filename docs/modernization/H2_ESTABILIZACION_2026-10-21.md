# H2 — Estabilización defensiva del motor (21 de octubre de 2026)

**Estado:** trabajo de estabilización en curso; aún NO es una base declarada libre de errores de memoria. H3.6 auditado y cerrado, H4 sin comenzar.

## H2.1–H2.2 — Contrato de recursos RNC y corrección

Se comprobó una debilidad en el contrato anterior: `rnc_unpack(void*,void*)` no conoce tamaños reales. `Resources.cpp` controla la cabecera externa, pero la rutina interna original podía efectuar lecturas anticipadas más allá del último byte. Se había registrado un hallazgo de AddressSanitizer en `lword/bit_advance` durante replays Amiga.

**Cambio implementado (desactivable por reversión de commit):**

- `Source/Amiga/dernc_bounded.cpp` ofrece `rnc_unpack_bounded(input,input_capacity,output,output_capacity)` con límites físicos y escritura acotada. No reserva relleno adicional. Solo la lectura anticipada del bitstream admite una extensión virtual a cero cuando faltan bytes especulativos; no se inventan literales y se siguen comprobando CRC de entrada/salida y longitudes.
- `Source/Amiga/dernc.hpp` define el nuevo contrato sin modificar la firma legacy.
- `Source/Resources.cpp` utiliza la rutina comprobada con los tamaños reales de los vectores.
- `Source/Amiga/Resource_Amiga_File.cpp` delega la carga en `fileDeRNC` en vez de invocar una segunda descompresión sin comprobación de retorno.
- La función legacy sigue en la base por compatibilidad de código, pero **las rutas del juego identificadas ya no la invocan**. No afirmar que API legacy es segura.

**Pruebas realizadas:**

- En entorno local aislado, **60** recursos RNC de demos válidos, y **714** casos de límites/cabecera/CRC rechazados, con AddressSanitizer y UndefinedBehaviorSanitizer.
- En GitHub Actions Linux: **88** recursos RNC de los datos públicos y **1047** entradas inválidas rechazadas, con ASan y UBSan (ejecución [39599528660](https://github.com/Cacheirez/openfodder/actions/runs/39599528660), PASS).
- Compilación y 29 replays demo Windows: [39599528686](https://github.com/Cacheirez/openfodder/actions/runs/39599528686), PASS.
- Los 11 replays con trazas H3 reproducibles en Windows/Linux. Además, los **11361 estados** registrados son exactamente iguales a las capturas **previas al cambio** en ambas plataformas. La comparación se hizo sobre archivos de evidencia descargados.
- Se incorporó el verificador `tools/modernization/check_gameplay_baseline.py` como requisito CI de Windows y Linux, para que una regresión futura no pueda pasar solo por ser determinista consigo misma.

**Límite:** H2.1 original pedía atribuir la lectura fuera de límites a un recurso mínimo con sus longitudes exactas. Esa atribución completa no está documentada; la corrección se ha validado con el conjunto de recursos y regresiones indicados. No marcar H2.1 como plenamente cerrado hasta documentar el caso concreto o justificar la sustitución completa del componente.

## H2.3 — Suite completa con sanitizador

Pendiente una ejecución ASan del **motor completo** sobre todas las rutas de replays disponibles después de incorporar el lector acotado. La batería aislada de RNC no sustituye a esta prueba. El detector de fugas permanece sin validar (en pruebas localizadas: `detect_leaks=0`; ASan y UBSan siguen activados).

## H2.4 — Coordinación entre hilos

`Source/Start.cpp` crea el hilo `Interrupt_Sim` y espera su finalización por `join`. En `Fodder.cpp` el hilo consulta el progreso mediante `mVideo_Ticked`, `mVideo_Done` y `mExit`, mientras `mPhase_InterruptTicks` se incrementa y se pone a cero en hilos diferentes. El tipo `volatile` de algunas señales **no** proporciona sincronización en C++.

Se cambiaron **esas cuatro señales concretas** a `std::atomic` con inicialización explícita, conservando el mutex `mSurfaceMtx` y el orden del ciclo. El código está sujeto a compilación y comparación de los hashes H3 en una nueva ejecución de Windows/Linux.

**No se afirma ausencia universal de carreras**: cámara, `mSprites`, entrada, superficies y visibilidad siguen compartiendo coordinaciones del motor clásico. H4 exigirá copias de presentación coherentes y de solo lectura; no trasladar libremente llamadas SDL al hilo de simulación.

## H2.5 / H2.6 — Referencias y decisión de integración

Los 11.361 estados de referencia se han contrastado entre Windows y Linux para PC Format y Amiga The One. Las 72 fases CD32 siguen sin replays propios; los datos comerciales se mantienen fuera del repositorio y de la CI.

La PR #1 debe permanecer en borrador hasta completar las pruebas pendientes. Conservar la base clásica y no declarar este H2 cerrado solo porque la CI normal esté verde.

## Evidencias y siguientes acciones

- [Contrato H3.6](H3_6_CONTRATO_VISIBILIDAD.md)
- [Validación H3](H3_VALIDACION_2026-10-21.md)
- [Huellas lógicas originales](../../tools/modernization/reference-gameplay-v1.json)
- Próximo paso H2: ejecutar/verificar regresión CI tras cambio atómico, realizar diagnóstico ASan del motor completo, inspeccionar fallos restantes y registrar limitaciones; después decidir H2.6.
