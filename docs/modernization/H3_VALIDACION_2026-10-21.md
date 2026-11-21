# H3 — Validación de equivalencia lógica: primeras 11 fases (21-10-2026)

**Estado:** H3.1–H3.5 verificados para las dos campañas de demostración indicadas. H3.6 tiene cobertura inicial de `mWasDrawn`, pero el ensayo de independencia del dibujo corresponde a H4 y no se ha realizado. H2 (RNC) sigue pendiente. **No hay gráficos HD ni cambios de simulación.**

## Revisión exacta y ejecuciones

- Código instrumentado: `cc5e337ddf8533a1a0377de987948d150760f272`.
- [Windows — run 39593037606](https://github.com/Cacheirez/openfodder/actions/runs/39593037606): **SUCCESS**, compilación x64, 29 fases demo, 0 omitidas, traza duplicada de PC Format y Amiga The One.
- [Linux — run 39593037449](https://github.com/Cacheirez/openfodder/actions/runs/39593037449): **SUCCESS**, compilación nativa y trazas duplicadas con los mismos replays.
- [Evidencias Windows](https://github.com/Cacheirez/openfodder/actions/runs/39593037606/artifacts/12343940168), [evidencias Linux](https://github.com/Cacheirez/openfodder/actions/runs/39593037449/artifacts/12342920918). Artefactos con caducidad; el manifiesto compacto de huellas permanece en `tools/modernization/reference-gameplay-v1.json`.
- Tests fijados en commit `c7722ef1a37c1e04ff28c6fedf9d3bdff197dc86` y SHA-256 del manifiesto de 29 ficheros `.ofd`: `3208f5f28ba2a155094cfe4df77f5a3a13d06b0aaa70fba9028720973ca8b0fd`.

## H3.1 — Determinismo observado

| Campaña | Fases distintas | Muestras de estado por ejecución | Windows A/B | Linux A/B | Comparación Windows ↔ Linux |
|---|---:|---:|---|---|---|
| PC Format | 8 | 7956 | PASS | PASS | PASS |
| Amiga The One | 3 | 3405 | PASS | PASS | PASS |
| **Total** | **11** | **11361** | **PASS** | **PASS** | **PASS** |

Se han inspeccionado los ZIP de evidencia: para las 11 fases, el par run1/run2 es idéntico byte a byte en cada plataforma. En la comparación cruzada los registros de estado de Windows y Linux son idénticos después de normalizar **solo** CRLF/LF, sin eliminar ni transformar datos lógicos. Las cabeceras mantienen los distintos valores `platform`. Los mismos 11 nombres/fases están presentes; todas tienen sprites activos en el registro.

La huella SHA-256 canónica de los ticks (sin la cabecera y con fin de línea LF) de cada fase se conserva en `tools/modernization/reference-gameplay-v1.json`. Esto permite comprobar el estado lógico **registrado**, no prueba cobertura de las 72 fases CD32 ni todos los estados internos posibles.

## H3.2 — Inventario de campos identificado y registrado

- **Metadatos:** campaña, misión/fase, plataforma de ejecución y plataforma de recursos, cuatro semillas de grabación, identificadores SHA-256 de grabaciones/parámetros, punto de muestreo.
- **Reglas y progreso:** diez objetivos, éxito/abandono, bajas, reclutas disponibles, soldados asignados (ID, rango, selección, bajas), tick de motor y tick de grabación.
- **Munición y controles:** granadas y cohetes por escuadra, arma seleccionada, escuadra activa, posición/botones del ratón, cámara y destino de mapa.
- **Temporización:** tiempo final de misión, temporizador de finalización, selección de escuadra, cadencia de disparo, pasos y entrada a vehículos, espera de acciones y armas por sprite.
- **Objetos:** lista ordenada de sprites activos con índice, tipo, posición entera/fraccionaria, dirección, animación, destino, destrucción, estado de terreno, agua, vehículo, sombra y `mWasDrawn`; cola de tiles pendientes de destrucción.
- **RNG:** las cuatro palabras del estado actual de `mRandom.getSeeds()`, sin consumir números adicionales.

**Cobertura no demostrada:** todas las casillas de la matriz de tiles (la cola de destrucción sí se registra), relaciones por punteros entre entidades (no serializar direcciones; se deberán traducir a índices estables cuando se necesiten), todos los subciclos de `Interrupt_Redraw` y cualquier campo aún no identificado con influencia lógica. `sSprite` no ofrece un contador genérico de vida o munición; no se han inventado `mHealth` ni `mAmmo`.

## H3.3–H3.4 — Instrumentación y capacidad de detectar errores

- `Source/GameplayTrace.cpp` registra JSONL opcional desde `Phase_Cycle()`, solo con la variable `OPENFODDER_TRACE_DIR` y ejecución de pruebas. Mantiene la ruta de producción sin escritura de trazas.
- `compare_gameplay_traces.py` valida metadatos, presencia y orden de ticks, ranuras de sprites, tipos y primera diferencia.
- `verify_gameplay_determinism.py` ejecuta dos veces con el mismo binario, grabaciones, configuración y semillas.
- Sobre **copias analíticas de trazas realmente producidas**, el comparador detectó: `tick 0 / state.game.kills_home / 0→1` y `tick 0 / state.sprites[0].was_drawn / 1→2`, tanto en Windows como en Linux.

**Limitación de la prueba de mutación:** la divergencia intencionada se creó en el archivo de prueba, no modificando la lógica del videojuego. Demuestra que el comparador y la cobertura de campos detectan alteraciones, no que haya un fallo real de jugabilidad.

## H3.5 — Política de plataformas

Guardar referencias diferenciadas para Windows-x64 y Linux-x64 con `platform`, `resource_platform`, código y datos fijados. El comparador regular **rechaza** metadatos de plataforma distintos; el cotejo cruzado efectuado en esta sesión fue un análisis separado de los 11 pares de líneas de estados, sin tolerancias ni sustitución de referencias específicas por plataforma.

## H3.6 — Visibilidad lógica y `mWasDrawn`

`Source/Sprites/Sprite_Core.cpp` asigna `mWasDrawn` durante `Sprite_Draw_Frame`, según `Sprite_OnScreen_Check`. El análisis inicial del proyecto identificó consumidores en comportamientos de civiles y efectos, por lo que no se tratará como una propiedad meramente estética.

1. La traza de cada sprite activo contiene el indicador y la prueba de mutación específica lo comprueba.
2. La futura ruta gráfica moderna será de solo lectura y no escribirá `mWasDrawn` en cada fotograma adicional.
3. Antes de dar por cerrado el desacoplamiento H4 hay que auditar todos los consumidores y contrastar **cero, uno y varios** dibujos entre ticks lógicos, incluida la pausa, borde de cámara y actualización de visibilidad.

**H3.6 sigue abierta para completar esa auditoría de consumidores.** El registro y detector están listos; la independencia futura del renderizado NO se ha demostrado.

## Cierre y continuidad

La referencia lógica es reproducible sobre los escenarios comprobados. Se conserva el renderizado clásico, el PR #1 como borrador, el paquete Windows previamente validado y el riesgo RNC registrado en H2.1. No fusionar ni empezar la sustitución de gráficos basándose solo en estos indicadores.

**Siguiente:** terminar revisión de los consumidores de `mWasDrawn` y de sincronización H2.4; continuar estabilización H2.1–H2.3 antes de iniciar integración de H4, manteniendo H6 (arte conceptual) independiente.
