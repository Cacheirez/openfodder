# Microbloque A — viabilidad de la demostración provisional

8 de noviembre de 2026. Base `43bd54a`; plan 2.74 conservado. Alternativa 1 aprobada por Miguel. **Resultado: no listo para microbloque B.** No se modifica el motor, la simulación, el arte, el lanzador ni el paquete de entrega. [Evidencia compacta](evidence/demo-a-feasibility.json).

## Recorrido y resultado real

Se reutilizó el ejecutable del artefacto Windows D6 existente, run `42469760932`, artefacto `13613699909`, y el manifiesto combinado exacto: 80 poses, 160 activos, 318 vinculaciones `replace-art`. Los manifiestos de los modos controlado/real son idénticos. El ejecutable coincide con el SHA-256 de `PRUEBAS.json` del paquete. No se compiló ni preparó un paquete nuevo.

Se ejecutaron inputs públicos existentes, sin editarlos, mediante `--unit-test --campaign "Amiga The One" --mission 1 --phase 2` y `OPENFODDER_TEST_FIRST_PHASE=1`; publicación/captura/cobertura ordenada activadas, SDL software/dummy a 12×. Sin override de presentaciones ni pausa artificial. La reproducción diagnóstica no espera el reloj de pared: los segundos indicados son ticks de demo / 50 Hz, no una prueba interactiva a velocidad normal. Se completó el replay disponible para no truncar la evidencia; el candidato inicial se analizó en sus primeros 30 segundos nominales.

| Recorrido existente | Soldados iniciales | Intentos ordenados | HD publicado | Retorno por clave ausente | H3 independiente |
|---|---:|---:|---:|---:|---|
| Amiga The One m1p2 | 5 | 4.554 | 0 | 4.554 | 1.546 muestras exactas |
| Única alternativa: Amiga The One m1p1 | 2 | 363 | 0 | 363 | 149 muestras exactas |

En m1p2, los primeros 30 segundos contienen 499 muestras lógicas con los cinco jugadores marcados como dibujados y movimiento desde el grupo inicial alrededor de (824,73) hacia (278,317). No se fuerzan ocho direcciones. El replay completo alcanza tick 4.640 (92,8 s nominales), pero no ofrece ningún intervalo publicado: **racha HD observada: cero**.

El replay de m1p1 dura solo 9 s nominales y tiene enemigos marcados como dibujados desde el comienzo. No mejora la cobertura ni proporciona el recorrido de 30–60 s. No se evaluaron otras fases ni se alargó o alteró ese replay.

## Bloqueos comprobados

1. **El combinado solo contiene `replace-art`; no clasifica los elementos asociados.** En el primer intento m1p2, el censo es completo: siete comandos, cinco cuerpos resueltos para sustitución, dos faltantes. Los faltantes son rango `type=21/sheet=0x95/frame=0` y ave `type=19/sheet=0x98/frame=0`. La transacción se rechaza entera: cinco decisiones `replace` no son cinco cuerpos HD publicados.
2. El resolver actual admite `keep-associated` para rango, ciertas sombras y marcador 0x7C, con claves explícitas; el manifiesto D6 no las incluye. **No admite el ave:** añadirle una fila `keep-associated` sin revisar el resolver seguiría dando `Missing`. `Sprites.hpp` identifica el tipo 19 como `Bird2_Left`; su manejador selecciona 0x98 y alterna dos frames. No es un cuerpo de soldado ni exige inventar arte humano.
3. **El recorrido grabado pronto entra en combate.** La traza marca el primer enemigo dibujado en tick 203 (~4,06 s nominales). En toda m1p2 se observan 83 claves enemigas ausentes y 29 claves ausentes de tipo jugador, además de proyectiles, vegetación, elementos asociados y cuerpos especiales. Las 18.035 decisiones de sustitución del jugador (24 claves distintas) quedan sin publicar; el resto de la escena impide la transacción. Corregir rango/ave permitiría resolver el primer bloqueo, pero no acredita 30 s continuos del replay completo.
4. **Transiciones separadas:** se registran `palette-transition` y `black-palette` antes de la puerta ordenada. El diagnóstico comunica cada motivo una vez; no mide su duración ni los cuenta como intentos ordenados. No se puede interpretar la ausencia de transacciones como publicación. Pausa/mapa/reanudación y cambio de fase no se ejercitan con sondas en este bloque.

Las dos claves Amiga D6 F0/F2 pendientes de un grupo siguen pendientes; no se identifican como el primer bloqueo de este recorrido ni se inventan vinculaciones para ellas. No se permite conservar enemigos/cuerpos clásicos para fingir cobertura moderna.

## Cambio mínimo propuesto y siguiente decisión

**Propuesta A.1, pendiente de aprobación:** añadir vínculos completos revisados para el rango mediante el `keep-associated` ya permitido, y admitir de forma estrecha y comprobada la conservación del ave `type=19/sheet=0x98`, con sus dos frames y claves explícitas. Mantener composición/oclusiones originales, rechazo de cualquier clave desconocida y prohibición de exceptuar cuerpos, enemigos o civiles. Primero verificar publicación efectiva del intervalo inicial y que siguen funcionando los rechazos de cuerpos ausentes.

Después habría que volver a evaluar una patrulla de 30–60 s alrededor del punto inicial de m1p2, evitando avanzar por la ruta grabada de combate; **esa trayectoria nueva no se ha grabado ni probado y no se afirma que sea segura o viable**. No se elimina ninguna entidad ni se cambia la IA para conseguirlo. Si requiere otras excepciones de escenario, se presentan con evidencia antes de ampliarlas.

**B permanece bloqueado.** Solo procede activación/paquete provisional tras demostrar un recorrido continuo con varios soldados, sin faltantes ni retornos normales en juego activo, y con transiciones delimitadas. La aceptación jugando, GPU, audio y CD32 siguen pendientes; esta prueba no entrega ni acepta una demo.

## Evidencia reutilizada, CI y recuperación

- No se repiten selectores, sanitizadores D6, controles positivos ni H3 completo. Solo se contrastan las dos trazas nuevas con las entradas inmutables de `reference-gameplay-v1.json`: 1.695 muestras exactas. No se modifica la referencia.
- CI Linux D6 `42469760868`: sigue `in_progress`, sin conclusión global. 47 pasos correctos; pendientes publicación/pausa con sanitizadores, TSan y cierre. No relanzada. Windows/densidades D6 ya PASS. [Ejecución Linux](https://github.com/Cacheirez/openfodder/actions/runs/42469760868).
- Directorio local recuperable: `C:/Users/migue/.codex/visualizations/2026/11/08/01a1baeb-e1ff-7942-98c0-64cf248935d3/demo-feasibility`. Conserva ZIP existente, ejecutable, inputs públicos, logs completos, trazas, resúmenes y scripts `replay_probe.py` / `record_feasibility.py`. Rutas y hashes en la evidencia. No contiene recursos CD32 privados. No se publican binarios ni logs grandes.
- Reproducción: recuperar el artefacto y verificar su digest, reutilizar los inputs públicos existentes de `native-data/Tests/Amiga The One` y el manifiesto indicado en la evidencia. Ejecutar `python -B replay_probe.py "Amiga The One" 1 2 <directorio-nuevo>`; para la única alternativa, `1 1`. El script conserva el entorno y llama al analizador existente `ordered_soldier_coverage.report`. La primera tentativa sin inputs se conserva como descartada (`No test found`, cero cobertura), nunca como PASS.
- WSL devuelve acceso denegado: operación detenida, sin reintentos ni cambios de permisos. Se usa el artefacto Windows existente. No se construyen runtimes ni se amplían pruebas de LLVM.
