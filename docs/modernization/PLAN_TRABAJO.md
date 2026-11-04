# Plan de trabajo vigente — OpenFodder

**Versión 2.74 · 2 de noviembre de 2026.** Responsable técnico: asistente. Decisiones y valoración de juego: Miguel. Este es el único plan de ejecución; [alcance completo H0–H10](ALCANCE_H0_H10.md).

## Dónde estamos

El candidato f72d6e7 compila, pasa CI y conserva H3, pero Miguel observa alternancia de soldado moderno/clásico. **Entrega A no aceptada como soldado completo.** Se retira el criterio de avanzar al escenario tras aceptar solo seis poses. Se requiere reproducir las direcciones, secuencias y estados originales con sustitución continua de todos los soldados del alcance.

[Diagnóstico, catálogo y criterios de salida](SOLDADOS_COBERTURA_COMPLETA.md). El inventario estático está hecho para las tablas CF1 PC/Amiga: marcha de ocho direcciones y tres frames por dirección, otras familias y rutas especiales localizadas. Falta completar cobertura dinámica/variantes y la implementación general.

## Orden de trabajo

| Paso | Trabajo | Cierre |
|---|---|---|
| **A1 — activo** | Matriz completa de soldados: todas las claves originales, entidades, estados, recursos/paletas y escenarios. Diagnóstico por entidad/estado y motivo. Casos para oclusiones, agua, bordes y transiciones. | Inventario trazable y puerta que detecte cualquier cuerpo clásico no previsto; no basta publicar una clave una vez. |
| **A2** | Captura de todos los soldados y composición de múltiples cuerpos en el orden original, con recorte/oclusiones correctos. | Casos normales soportados sin volver al clásico; referencia clásica y simulación conservadas. No desactivar guards para saltarse el problema. |
| **A3** | Ciclo de marcha completo de 24 claves del jugador; después todos los demás estados, enemigos y variantes del catálogo. Derivados/manifiestos reproducibles. Puede avanzar junto con A2 cuando los contratos estén fijados. | Poses coherentes y selección exacta del frame original; todas las familias del alcance cubiertas. Las 24 claves son un paso interno, no soldado completo. |
| **A4** | H3, pruebas de render, CI Windows/Linux, paquete y recorrido continuo a velocidad normal. | Ningún cuerpo clásico intercalado en condiciones normales dentro del alcance; validación visual de Miguel. Recuperación segura y coherente ante errores reales. |
| **B** | Escena coherente: terreno, vegetación, edificios/objetos/efectos, interfaz y cursor completo con punto activo conservado. | Recursos del recorrido cubiertos, composición y legibilidad comprobadas. |
| **C** | Interpolación de cámara/entidades, discontinuidades, ratón e independencia 0/1/N; completar la fase. | Misión completa con presentación nueva y suave; objetivo 60 Hz sujeto a medición real. Cierre H7 solo con su definición completa. |
| **D** | Extensión a CF1/CD32, variantes, pantallas y vehículos; matriz Windows, pulido y entrega. | H8–H10 completos según el alcance final. |

## Avance de ejecución A1/A2 — sin cambiar el plan 2.74

Captura ampliada a todos los slots visibles, con tipo, persona, dirección de apuntado, vehículo/destrucción y recursos propios. Matriz de 637 claves y plantilla exacta de las 24 de marcha por bando/formato en `evidence/soldier-coverage-matrix.json`. Traza opcional `OPENFODDER_SOLDIER_COVERAGE=1` después del contraste clásico; su analizador mantiene `PENDING` porque observar no demuestra publicación HD.

`OrderedSoldierArt.hpp` es un compositor CPU interno de múltiples cuerpos: mantiene orden y celdas HD disjuntas, aplica agua/recortes, oclusiones incluso de igual color y Save/Restore/Clear. Pruebas sintéticas PC/Amiga a 1×/8×/12×. **A1/A2 siguen abiertos**: faltan variantes/rutas dinámicas, integración SDL/transiciones y arte completo. No se entrega otro piloto parcial ni se cierra A/H7.

El contrato de activos externos v2 está implementado como paso A3 junto a A2: geometría variable, SHA-256, derivados RGBA 8×/12× y vinculaciones explícitas sin compilar cada pose. Una prueba sintética recorre las 24 claves PC/Amiga en 128 intervalos SDL; no son 24 imágenes artísticas terminadas. [Estado y siguiente bloque de arte](CONTINUIDAD.md).

Contraste nativo del 5 de noviembre: 24 claves ordinarias por plataforma recuperadas de recursos reales; 13 vinculaciones diagonales verificadas sin reasignación sintética (12 de marcha y una Slide1 separada), 34 intervalos SDL/68 cuerpos y H3 original completo PASS. [Reproducción y límites](NATIVE_WALK_REVIEW.md). Pendientes las otras 21 claves artísticas y demás estados; A3 no se cierra por estas pruebas.

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
