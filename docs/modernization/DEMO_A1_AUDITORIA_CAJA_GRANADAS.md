# A.1 — auditoría nativa de la caja de granadas 0xC2/F0

12 de noviembre de 2026. Entrada `885417794b2813799672cd85efef10e25db8719d`. Prueba manual `interactive-check-02`, Amiga The One, misión 1, fase 2 (Find Grenades). [Evidencia de la sesión](evidence/demo-a1-interactive.json).

## Recuento frente al candidato de 324 claves

Se cotejaron los SHA-256 del log cerrado y de ambos manifiestos. Se cruzaron los comandos de densidad 12 con los resultados de **4.456** intentos, cada uno con un par único de escena e intervalo. Las 322 vinculaciones del manifiesto de la sesión son idénticas en el candidato, que añade dos conservaciones exactas (insignia F4 y tejado F0). Cada clave se cuenta una vez por intento. [Candidato de partida](DEMO_A1_AUDITORIA_TEJADO_F0.md#integración-del-candidato).

| Faltantes distintos por intento | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Intentos | 2.222 | 2.054 | 108 | 6 | 15 | 21 | 21 | 3 | 6 |

Quedan **42 claves residuales**. La primera según el criterio de faltante único y frecuencia total es `c967c720f08747d3eae8abb253c3ed16d3684ca547ca65df3627d275f9c3e6e5`. Aparece en **1.755 intentos**, en todos ellos como único faltante. La segunda suma 275 como único faltante y 359 en total. La caja se observó en la escena 186, ranura 23, generación 164, entre los intentos 365 y 3873.

Cubrir esa clave elevaría de **2.222 (49,87 %)** a **3.977 (89,25 %)** los intentos del registro histórico con todas las claves cubiertas y dejaría 479 con faltantes. Es una proyección sobre el registro. La sesión original publicó 92 intervalos HD y la publicación efectiva con el candidato ampliado sigue PENDIENTE.

## Procedencia comprobada

- El tipo 37 es `eSprite_GrenadeBox`. Su manejador selecciona la hoja `0xC2` y otorga cuatro granadas al recoger la caja. En Amiga The One, `0xC2` dirige a `stru_8E308`, con una sola fila F0, segmento `eGFX_IN_GAME2` (1), offset **2578**, dos columnas de tabla, 13 filas y modificadores (0, 0). [Tipo](../../Source/Sprites.hpp#L58) · [Manejador](../../Source/Sprites/Sprite_Projectiles.cpp#L731) · [Tabla](../../Source/Amiga/SpriteData_Amiga.hpp#L980).
- Se verificó el recurso Amiga8 de **320 × 256, cuatro planos**, con SHA-256 `3dd8d73e4700b42f081f25b25b547b5bd76c9124580ecbd5e01729527e9d8f11`, y el índice efectivo 0 tanto para el recurso como para el dibujo. Se reprodujo primero la clave de la insignia 0x95/F0. Con el mismo recurso y paleta efectiva, la fila de la caja y los valores 0 de persona, animación, vehículo y destrucción pendiente reproducen la clave del log. Cambiar la persona a −1 o usar el offset de la insignia cambia el hash. El snapshot es una reconstrucción sin tick de la sesión manual. [Origen del recurso y la paleta](DEMO_A1_AUDITORIA_TEJADO_F0.md#procedencia-comprobada).
- El renderizador nativo de Windows x64 recalculó la clave con el motor y generó un raster de **16 × 13**, con 102 píxeles de alfa distinto de cero y SHA-256 RGBA `fe65a387e79d0fc034c567c96473bb301381c53dee10dbb40d6ebb169774df4b`. [Verificación de clave](../../tools/modernization/native_walk_snapshot.hpp#L25) · [Renderizador](../../tools/modernization/render_walk_native.cpp).

## Integración y comprobación

El preparador con `--with-grenade-box` añade la clave exacta de la caja como `keep-associated` al verde A con F4 y tejado. El registro admite el tipo 37, hoja 0xC2/F0, en Amiga8 con sprite y recurso válidos y fuera de los estados de vehículo y destrucción pendiente. Se cotejaron los 160 activos por SHA-256 y las 324 vinculaciones previas en orden. El candidato tiene **325 vínculos (318 reemplazos y siete conservaciones)** y SHA-256 `5a7197d0f21b62d15c4be4cc44c379aa84455c35b436b584dbb3e389fee26cfc` en Windows. Las dos variantes anteriores del preparador reproducen sus manifiestos byte a byte. [Registro](../../Source/Utils/OrderedSoldierRegistry.hpp) · [Preparador](../../tools/modernization/prepare_demo_a1_manifest.py).

SDL 3.4.0 por software en Windows x64 con Clang 23.1.5, ASan y UBSan dio **PASS a 8× y 12×**. La escena controlada contiene cinco cuerpos de claves nativas, F4, el tejado y la caja. Las 102 escrituras de la caja cubren celdas HD previas, el último cuerpo compone encima de 53 y quedan 49 visibles. El cuadro SDL coincide píxel a píxel con la composición esperada. El intervalo simulado tras la recogida retira el comando de la caja y conserva HD con los cinco cuerpos. Dos faltantes inducidos por densidad (caja o cuerpo) producen un cuadro clásico íntegro y recuperan HD al restaurar la clave. Regresiones F4 y tejado PASS a ambas densidades.

Una prueba aparte ejecutó el manejador real y las funciones de distancia y destrucción del motor en Windows x64. A distancia la caja conserva la hoja 0xC2 y el inventario queda en tres granadas. Al acercarse el jefe de escuadra, el inventario sube a siete, se marcan ambos contadores para refresco y la caja pasa a tipo nulo con destrucción pendiente.

**PENDIENTES:** aceptación jugando, recorrido integrado de recogida en el juego, publicación efectiva durante la sesión manual, GPU, audio, CD32, LSan y cobertura restante. La proyección histórica de 3.977 intervalos con claves cubiertas sigue siendo un recuento de cobertura. No se entrega ejecutable.

## Recuperación local

Directorio local `C:/Users/migue/.codex/visualizations/2026/11/12/01a1d0b9-bfaa-75a1-95f3-71a1660c5d96`. Desde allí, ejecutar `python -B verify_grenade_box.py <repo> <a1> <roof-candidate/candidate-manifest.json> <renderer.exe>`. Usar el árbol `a1` de [Continuidad](CONTINUIDAD.md), el manifiesto de 324 claves de la [integración del tejado](DEMO_A1_AUDITORIA_TEJADO_F0.md#integración-del-candidato) y el [renderizador de F4](DEMO_A1_AUDITORIA_RANGO_F4.md#recuperación-local). El log se lee desde la ruta de la evidencia de la sesión.

Evidencia de integración en `C:/Users/migue/.codex/visualizations/2026/11/12/01a1d0c7-c4fc-7a61-bfe3-2ae6d4edbb75`. Generar `box-candidate` con `python -B tools/modernization/prepare_demo_a1_manifest.py --base <verde-A>/qa-rocket-native/art/candidate-manifest.json --out <directorio-evidencia>/box-candidate --with-grenade-box`. En el directorio de evidencia, ejecutar `python -B prepare_box_input.py <evidencia-del-tejado> <auditoría-de-la-caja> <directorio-evidencia>`, luego `run_box.ps1 <checkout>` y `run_pickup.ps1 <checkout>`. La prueba del manejador recompila sus fuentes del checkout y enlaza con los objetos restantes del `native_probe` conservado en `<a1>/build`.

- `fixture-run.log` SHA-256 `ac8d33606e54af8876843bb6cda99d4c6b2861ae016053bdcfbcd81afbcdb0b7`.
- `pickup-run.log` SHA-256 `6bced472c3eaa1881720c0be9e7d12de273fed564c56099eaa1a713818f7d9c8`.

| Fichero local | SHA-256 |
| --- | --- |
| `verify_grenade_box.py` | `59f63110987a729e50c289fcf0d6b874adbbd7794cd02796f320c27ab77187d8` |
| `grenade-box-derived.json` | `77ea661d9831c9e0e487dcc9103962f301687cbb2fc826013924c1accaf0f445` |
| `grenade-box-verification.json` | `82432948ea542b0ed123182500ea07846fc8ee959f295c3ff17ed22ea96261fc` |
