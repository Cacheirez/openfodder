# H2.3 — Índices seguros de seguidores y Huffman PC (21-10-2026)

**Conclusión:** los seis avisos de índices fuera de rango inicialmente registrados en `Sprite_Core.cpp` y `Resource_PC_CD.cpp` desaparecen del análisis ASan/UBSan del motor completo después de **29 fases**. La comprobación de jugabilidad conserva las **11.361 muestras** originales en Linux y Windows. **H2.3 global sigue abierta** por otros 17 avisos UBSan, detección de fugas no realizada y cobertura pendiente de la campaña comercial.

## Diagnóstico desde los logs (antes del parche)

En el artefacto original `H2_sprite_frames_ASan_Linux_evidence.zip` (run Linux 39615453699), UBSan señalaba:
- `Sprite_Core.cpp:2036, 2167, 2170`: índice **9** fuera de `sSprite *[9]`.
- `PC/Resource_PC_CD.cpp:509, 526, 537`: índices **627, 694, 940** fuera de `short int[627]`.
- Los otros 17 errores: 15 desplazamientos negativos y dos accesos desalineados.

### Seguimiento de sprites

`field_5E_Squad` es un cursor de búsqueda que avanza de 0 hasta aproximadamente 30. `mSquad_0_Sprites[9]` a `mSquad_4_Sprites[9]` representan **cinco grupos consecutivos de nueve entradas**: el acceso original cruzaba los límites de C++ para alcanzar la siguiente escuadra. La primera solución, que descartaba los valores mayores que 8, fue una regresión: falló la séptima fase de PC Format. Se corrigió mediante `gameFlattenedIndex`, que convierte el cursor en índice de escuadra y posición, y consulta `mSquads[grupo][posición]` sin desbordar los arrays. Conserva exactamente el comportamiento de los índices clásicos del 0 al 30. Se comprueban los accesos tanto al elegir seguidor como al fijar su objetivo.

### Tablas Huffman de recursos PC

Los nodos internos son `2*314-1=627` y las hojas `314`, con **941 posiciones lógicas** de padres. En el código heredado hay dos arrays de memoria separados: `word_26DBE[627]` alberga padres de nodos, y `word_272A4[314]` los de hojas. El array `word_279FE[627]` contiene las frecuencias ordinarias, mientras `word_27EE4` es el centinela `freq[627]=0xffff`. El acceso previo fuera de rango dependía de la adyacencia accidental de estos miembros. El parche `Huffman_Parent` y `Huffman_Frequency` conserva explícitamente dicha relación sin leer ni escribir fuera de los arrays.

La primera tentativa, que aumentaba físicamente los arrays, rompió la decodificación PC; **se descartó**. Se preservó la evidencia de la ejecución fallida y se repitieron los replays sin modificar las referencias H3.

La inicialización mediante `memset` usa ahora `sizeof` de cada array, corrigiendo además una longitud de un byte superior al tamaño de `byte_27EE6`.

## Pruebas y resultados

- **Código verificado:** [e096180](https://github.com/Cacheirez/openfodder/commit/e09618072f996bd3ac455baa20b9c450ef8a07bf).
- [Linux run 39624063027](https://github.com/Cacheirez/openfodder/actions/runs/39624063027): compila, CTest (3 pruebas, incluida `squad_huffman_index_layout`), RNC acotado, H3 PC/Amiga, baseline original, **ASan/UBSan 29/29 fases, 0 omisiones, retorno 0**. `engine.log`: **cero avisos `runtime error: index ... out of bounds`** y cero errores fatales de AddressSanitizer.
- [Windows run 39624062742](https://github.com/Cacheirez/openfodder/actions/runs/39624062742): compilación x64, tests de límites, 29 replays y comprobación del baseline H3, **SUCCESS**.
- Prueba aislada local bajo GCC y Clang, `-fsanitize=address,undefined`: **1.077 casos** de índices de escuadras y posiciones Huffman, PASS.
- Se conservan los hashes de `tools/modernization/reference-gameplay-v1.json`, sin regenerarlos ni ignorar campos.

**Quedan 17 errores UBSan de naturaleza distinta:** 15 desplazamientos de bits negativos en RNG, cámara, mapa y sprites; 2 lecturas desalineadas en `Source/stdafx.hpp:92`. La suite principal del motor usa `ASAN_OPTIONS=detect_leaks=0`, por lo que todavía no acredita ausencia de fugas.

## Nueva barrera de CI

`tools/modernization/check_ubsan_indices.py` y sus pruebas sintéticas convierten la auditoría en criterio de rechazo de GitHub Actions: deben completarse 29 fases y no aparecer un ASan fatal ni un UBSan de índice fuera de rango. Se mantienen explícitos los avisos restantes, **sin silenciarlos ni considerarlos resueltos**. La ejecución de este nuevo paso debe verificarse en su propio commit.

**Próximo paso:** tratar con pruebas de equivalencia los desplazamientos negativos y lecturas desalineadas; cerrar H2.1/H2.4 y documentar cobertura adicional antes de aceptar H2.6. Los datos CD32 comerciales se mantienen privados.
