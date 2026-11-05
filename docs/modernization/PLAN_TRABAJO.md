# Plan de trabajo vigente — OpenFodder

**Versión 2.74 · 2 de noviembre de 2026.** Responsable técnico: asistente. Decisiones y valoración de juego: Miguel. Este es el único plan de ejecución; [alcance completo H0–H10](ALCANCE_H0_H10.md).

## Dónde estamos

Estado contrastado con código y activos de `577c702` el **5 de noviembre de 2026**. Se conserva la versión 2.74: esta revisión actualiza avance y criterios operativos, sin cambiar alcance ni orden.

**Estamos desarrollando A3, con A1/A2 implementados parcialmente y pendientes de cobertura completa.** El piloto `PROBAR_SOLDADO_ANIMADO.cmd` sigue activando el lote antiguo de seis claves; no activa el manifiesto de marcha de 24 poses. La alternancia observada por Miguel continúa sin aceptación ni solución entregada como producto.

| Bloque | Implementado y comprobado | Falta para cerrarlo |
|---|---|---|
| A1 | Catálogo estático PC/Amiga, captura de todos los slots, claves por recurso/paleta y censo transaccional de publicación. | Variantes/rutas y escenarios completos, incluidas dos claves ordinarias Amiga no observadas y transiciones. |
| A2 | Compositor ordenado de múltiples cuerpos, recortes/oclusiones, publicación SDL y recuperación de la vista completa; integración por manifiesto en `WindowHD`. | Cobertura normal sin retornos por arte ausente, transiciones y validación GPU/escenas reales. |
| **A3 — bloque de desarrollo actual** | 24 poses de marcha del jugador, derivados 8×/12× y 94 vinculaciones reales; revisión interna y pruebas aisladas de publicación. | Reposo/apuntado, demás estados, enemigos/variantes y aceptación artística. No equivale a soldados completos. |
| A4 | H3 y pruebas focalizadas ya ejecutadas para los bloques anteriores; CTests Windows/Linux actuales PASS. | CI completa en curso, cobertura global, paquete nuevo y recorrido continuo aceptado por Miguel. |
| B/C/D | Hay infraestructura previa documentada en H0–H10. | No se inicia un nuevo bloque de escenario, interpolación o extensión como sustituto del cierre de soldados. |

[Diagnóstico, catálogo y criterios de salida](SOLDADOS_COBERTURA_COMPLETA.md). La ruta ordenada rechaza todo el intervalo si falta una clave: tener el arte de marcha no elimina los retornos de campaña mientras falten otros estados/entidades. El último H3 local conserva 11.361 estados originales, pero no publicó HD ordenado de campaña.

CI consultada de `577c702`: Windows [42019722132](https://github.com/Cacheirez/openfodder/actions/runs/42019722132) y Linux [42019722430](https://github.com/Cacheirez/openfodder/actions/runs/42019722430) han superado compilación/CTest; los workflows completos siguen en curso. Comparador [42019722401](https://github.com/Cacheirez/openfodder/actions/runs/42019722401) PASS. El fallo anterior de hash por CRLF no se reproduce en el CTest Windows posterior a `b921009`; no atribuir PASS a pasos aún pendientes. [Comprobación de estado](evidence/plan-status-20261105.json).

## Siguiente bloque verificable

**A3: reposo/apuntado del jugador y transición marcha → reposo/apuntado → marcha.** Contrastar la rama de `Sprite_Handle_Troop_Animation` que selecciona la tabla en offset `0x30`, frame 0, y sus condiciones: dirección `mFaceDirection`, objetivo de arma, movimiento y agua. No asumir que toda quietud/disparo usa la misma familia.

Reutilizar el censo y los maestros existentes cuando su correspondencia esté probada; recuperar solo referencias faltantes. Añadir vinculaciones explícitas y arte para las ocho direcciones de esta familia, con sus variantes observadas. Salida: prueba acotada Window/SDL con dos soldados, oclusión y 8×/12×, selección original intacta y censo de publicaciones/rechazos. Seguir la CI activa; resolver cualquier fallo nuevo pertinente antes de ampliar la entrega. Después, demás estados/enemigos y variantes pendientes. No regenerar la marcha ya publicada ni cambiar todavía el lanzador.

## Orden de trabajo

| Paso | Trabajo | Cierre |
|---|---|---|
| **A1 — abierto** | Matriz completa de soldados: todas las claves originales, entidades, estados, recursos/paletas y escenarios. Diagnóstico por entidad/estado y motivo. Casos para oclusiones, agua, bordes y transiciones. | Inventario trazable y puerta que detecte cualquier cuerpo clásico no previsto; no basta publicar una clave una vez. |
| **A2** | Captura de todos los soldados y composición de múltiples cuerpos en el orden original, con recorte/oclusiones correctos. | Casos normales soportados sin volver al clásico; referencia clásica y simulación conservadas. No desactivar guards para saltarse el problema. |
| **A3 — activo** | Ciclo de marcha completo de 24 claves del jugador; después todos los demás estados, enemigos y variantes del catálogo. Derivados/manifiestos reproducibles. Puede avanzar junto con A2 cuando los contratos estén fijados. | Poses coherentes y selección exacta del frame original; todas las familias del alcance cubiertas. Las 24 claves son un paso interno, no soldado completo. |
| **A4** | H3, pruebas de render, CI Windows/Linux, paquete y recorrido continuo a velocidad normal. | Ningún cuerpo clásico intercalado en condiciones normales dentro del alcance; validación visual de Miguel. Recuperación segura y coherente ante errores reales. |
| **B** | Escena coherente: terreno, vegetación, edificios/objetos/efectos, interfaz y cursor completo con punto activo conservado. | Recursos del recorrido cubiertos, composición y legibilidad comprobadas. |
| **C** | Interpolación de cámara/entidades, discontinuidades, ratón e independencia 0/1/N; completar la fase. | Misión completa con presentación nueva y suave; objetivo 60 Hz sujeto a medición real. Cierre H7 solo con su definición completa. |
| **D** | Extensión a CF1/CD32, variantes, pantallas y vehículos; matriz Windows, pulido y entrega. | H8–H10 completos según el alcance final. |

## Avance de ejecución A1/A2 — sin cambiar el plan 2.74

Captura ampliada a todos los slots visibles, con tipo, persona, dirección de apuntado, vehículo/destrucción y recursos propios. Matriz de 637 claves y plantilla exacta de las 24 de marcha por bando/formato en `evidence/soldier-coverage-matrix.json`. Traza opcional `OPENFODDER_SOLDIER_COVERAGE=1` después del contraste clásico; su analizador mantiene `PENDING` porque observar no demuestra publicación HD.

`OrderedSoldierArt.hpp` es un compositor CPU interno de múltiples cuerpos: mantiene orden y celdas HD disjuntas, aplica agua/recortes, oclusiones incluso de igual color y Save/Restore/Clear. Pruebas sintéticas PC/Amiga a 1×/8×/12×. **A1/A2 siguen abiertos**: faltan variantes/rutas dinámicas, transiciones y arte completo; la integración SDL por manifiesto ya está implementada. No se entrega otro piloto parcial ni se cierra A/H7.

El contrato de activos externos v2 está implementado como paso A3 junto a A2: geometría variable, SHA-256, derivados RGBA 8×/12× y vinculaciones explícitas sin compilar cada pose. Una prueba sintética recorre las 24 claves PC/Amiga en 128 intervalos SDL; no son 24 imágenes artísticas terminadas. [Estado y siguiente bloque de arte](CONTINUIDAD.md).

Contraste nativo del 5 de noviembre: 24 claves ordinarias por plataforma recuperadas de recursos reales; 13 vinculaciones diagonales verificadas sin reasignación sintética (12 de marcha y una Slide1 separada), 34 intervalos SDL/68 cuerpos y H3 original completo PASS. [Reproducción y límites](NATIVE_WALK_REVIEW.md). Las otras 21 claves artísticas se prepararon en el lote posterior descrito a continuación; siguen pendientes los demás estados y A3 no se cierra por estas pruebas.

Lote artístico posterior: las **24 claves de marcha del jugador están preparadas y revisadas internamente** (18 maestros nuevos, tres anteriores reutilizados en su diagonal y ciclo C01 conservado). [Fuentes, visor y límites](../../assets/modernization/soldier-walk24/README.md). Publicación SDL probada con las 94 claves ordinarias realmente observadas; dos variantes Amiga no observadas quedan explícitas. Pendientes aceptación artística, otros estados/enemigos y cobertura completa. No cierra A3 ni corrige todavía el lanzador como producto.

## Reglas de implementación

- Preservar reglas, RNG, tiempos lógicos, colisiones, orden y campo visible. No cambiar huellas H3 para ocultar divergencias ni acelerar la simulación para animar arte.
- La dirección visual y el frame los decide el motor, no un reloj nuevo ni la lectura directa del joystick. Mantener apuntado independiente de desplazamiento.
- Estilo C — Pintado moderado y maestro C01 conservados. El lote de cinco poses sigue provisional; no suponer que la aprobación de C01 acepta toda la animación.
- 12× es variante provisional de trabajo, con 8× disponible; densidad final y rendimiento GPU pendientes. No bloquear la corrección de cobertura con otra cadena de estudios de densidad.
- Clásico disponible por elección y recuperación ante errores. En funcionamiento normal, la ausencia de arte o una oclusión normal no cuentan como soldado moderno terminado.
- No producir cientos de imágenes antes de verificar una secuencia completa y su composición. Agrupar cambios útiles, pruebas y evidencia por entrega.
- Datos comerciales y partidas privadas fuera de GitHub. Demos públicas para el trabajo inicial; CD32 se valida por separado cuando la tarea concreta requiera sus datos.
- PR #1 abierto, borrador y sin fusionar. No delegar a subagentes salvo autorización expresa.

## Validación y eficiencia

Documentación: coherencia/enlaces. Catálogos: reproducibilidad, fuentes y longitudes reales. Implementación: tests focalizados de rutas afectadas, H3 y sanitizadores pertinentes; antes de entregar ejecutable, CI completa Windows/Linux, informes ligados al hash y ZIP verificado. Registrar pruebas no ejecutadas como pendientes.

Medir contadores de cobertura y coste por bloque en la ruta real. Optimizar un cuello demostrado, sin encadenar estudios que sustituyan al avance visual. La reducción de duplicados y caché de dependencias en CI sigue pendiente; no eliminar pruebas para acelerar un verde.

Conservar evidencia útil y maestros en Git; los binarios de Actions caducan. Actualizar [CONTINUIDAD.md](CONTINUIDAD.md) y la evidencia afectada, sin copiar el mismo estado a cada informe histórico. [Índice documental](README.md).
