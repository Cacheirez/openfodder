# H2.1 defensiva y arranque de H3 — 2026-10-21

> Informe parcial. **No** se ha modificado el motor ni completado H2/H3. Los scripts de comprobación y sus 22 pruebas sintéticas se entregaron en el chat como `OpenFodder_H2_H3_avance_2026-10-21.zip`; su integración en el repositorio y en CI sigue pendiente.

## H2.1: diagnóstico, sin explotación de vulnerabilidades

Se ha revisado el código de la rama:

- `Source/Amiga/dernc.cpp`: `rnc_unpack(void*,void*)` no recibe longitudes físicas ni capacidad de salida. `bitread_init`, `bitread_fix` y `bit_advance` usan lecturas de dos bytes de la entrada; las validaciones de CRC no sustituyen los controles de rango internos.
- `Source/Resources.cpp`: `cResources::fileDeRNC` valida cabecera de 18 bytes, tamaño comprimido declarado, expansión máxima de 64 MiB y longitud devuelta. El tamaño físico no llega hasta `rnc_unpack`.
- `Source/Amiga/Resource_Amiga_File.cpp`: existe otra llamada a `rnc_unpack` basada en la cabecera y sin comprobación de retorno; determinar si esa ruta se utiliza para los escenarios de pruebas antes de modificarla.

**Inspección estática del ZIP de referencia, sin datos comerciales:** 60 recursos RNC de demos declaran una longitud comprimida exactamente coherente con sus archivos; otros 214 recursos inspeccionados no tienen la cabecera RNC-1. Se excluyó `Amiga_CD`. Este resultado NO acredita seguridad en las lecturas de bits ni validez de la descompresión. No se subió al repositorio ningún contenido comercial.

**Pendiente para cerrar H2.1:** reproducir/verificar en esta sesión el defecto ASan ya registrado en `RESULTADOS.md`, identificar el recurso y las longitudes reales de entrada/salida, registrar la ruta y el límite violado. No ocultar el problema con padding arbitrario ni desactivando ASan.

**Orientación H2.2:** un contrato explícito de `input_size`/`output_capacity`, límites de lectura de bits y literales, rechazo controlado de datos inválidos, y regresión con demos y CD32 en entorno privado.

## H3: protección de jugabilidad

Se han diseñado y probado localmente herramientas (Python estándar) para comparar trazas lógicas JSONL. **22 pruebas sintéticas pasan:** detección de divergencia en posición, munición, RNG y primer tick/campo; rechazo de ticks ausentes, duplicados, floats, comparaciones de plataforma/replay distintos y JSON con claves duplicadas.

### Esquema de traza provisional (H3.2)

Un encabezado `kind=meta`, `schema_version=1`, campaña, misión/fase, plataforma, huellas SHA-256 del replay y parámetros, cuatro semillas, muestreo `post-phase-cycle`, y commit informativo. Una línea por ciclo con `kind=tick`, contador creciente y `state.game`, `state.controls`, `state.rng`, `state.sprites`.

- Datos de fase, objetivos y bajas: `Source/GameData.hpp` y `Source/Fodder.hpp`.
- Controles de ratón/escuadra: `Source/Fodder.hpp`.
- RNG: `mRandom.getSeeds()` sin consumir aleatoriedad (`Source/Utils/pseudorand.hpp`).
- Sprites por índice estable, tipo, posiciones enteras/fraccionarias, estado, dirección, temporizadores y visibilidad (`Source/Sprites.hpp`). La vida y munición se deben mapear a sus estructuras reales, **no** asumir miembros inexistentes `mHealth`/`mAmmo` en `sSprite`.
- Nunca serializar punteros, padding de C++, direcciones de memoria, estado gráfico o números flotantes.

### Limitaciones y tareas restantes

1. H3.1 NO completado: los 29 replays que terminan no prueban identidad de estado. Faltan dos trazas reales de la misma grabación.
2. H3.3 parcial: comparador local probado; **falta el emisor del motor**, compatible con `Phase_Cycle` y con el avance parcial en `Interrupt_Redraw`.
3. H3.4 NO completado: la divergencia se detectó sobre fixtures sintéticos, no sobre modificaciones del motor.
4. H3.5 y H3.6 pendientes: referencia por plataforma y conservación de `mWasDrawn`/visibilidad.

**Criterio para avanzar a H4:** una referencia repetible que detecte cambios lógicos, y dibujo clásico desacoplable sin modificar esa referencia. No cambiar velocidades, colisiones, reglas, comportamiento enemigo, temporizadores ni RNG.
