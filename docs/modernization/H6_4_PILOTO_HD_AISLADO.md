# H6.4 — contrato y piloto aislado de composición C01 HD

29-10-2026, plan 2.58. Implementado en `Source/Utils/SoldierArtHD.hpp`, sin conexión a SDL ni activación en el juego. No confundir con el comparador HTML ni con el piloto nativo 16×14 existente. Dirección C conservada. Miguel ha revisado ambas densidades en las resoluciones/fondos del comparador: ambas le parecen bien, con preferencia por mayor detalle si memoria y rendimiento lo permiten. Esto orienta hacia 12×, pero no fija aún la densidad definitiva ni acredita rendimiento del motor.

## Contrato

Entrada: secuencia propia `MissionLayerSequence`, identidad de destino, estabilidad de paleta y recurso RGBA inmutable de cuadro 16d×14d. Candidatos d=8 y d=12; d=1 se admite exclusivamente como oráculo de equivalencia con `ComposeSoldierArt`. No hay punteros a entidades vivas, llamadas SDL, RNG, modificación de visibilidad o pasos de simulación.

Salida: `SoldierArtHDResult` con identidad, densidad efectiva, origen lógico, escena y estado explícito. En éxito, destino RGB privado empaquetado a densidad d. En retorno clásico, destino nativo exacto y densidad 1, nunca un frame parcial. El consumidor futuro debe respetar la densidad efectiva; no puede interpretar un fallback nativo como HD.

Se reutiliza la política conservadora revisada de `SoldierArt.hpp`: una sola pose compatible de hoja 7/frame 0, PC o Amiga. Se elimina solo ese cuerpo de una copia de comandos usando alfa nativo cero, recuperando el fondo verdadero; se amplía el fondo clásico y se mezcla la derivación HD, con promedio premultiplicado durante la preparación y alfa recto al componer. El anclaje lógico sigue siendo el original; pies en (8,14), cuerpo en (3,0)-(13,14), cámara/altura procedentes del comando actual.

No se reordenan comandos por su rol. Los destinos permanecen independientes. Cualquier comando posterior que pueda tocar el cuerpo conserva el clásico: escrituras incluso del mismo color, cero u OR, otro soldado, HUD, Terrain/Clear/Save/Restore. Los recortes no soportados, cuerpos repetidos y paleta inestable también vuelven al clásico. **Este incremento conserva oclusiones mediante fallback; todavía no dibuja un cuerpo HD parcialmente oculto.** El recorte clásico permanece íntegro; no se inventa geometría para un cuerpo cortado.

El primer piloto rechaza backing con pitch distinto de ancho: no transforma silenciosamente el comportamiento histórico packed/pitched. Identidades desconocidas o comandos mal formados siguen siendo errores del contrato de MissionLayers; no se ocultan como retornos artísticos. La entrada exige extensiones ya válidas para los núcleos retenidos.

## Recursos y memoria

`build_soldier_art.cpp fuente.png salida.hpp [1|8|12]` deriva directamente del PNG original. La llamada antigua produce exactamente el mismo header nativo, byte a byte. CMake genera los derivados en su directorio de compilación; fuente, receta y pruebas quedan en Git. No se modifican ni regeneran los originales, H3 o gráficos comerciales.

| Elemento | 8× | 12× |
|---|---:|---:|
| Pose RGBA 16×14 | 57.344 bytes (56 KiB) | 129.024 bytes (126 KiB) |
| Salida RGB 352×272 del ensayo de límite | 24.510.464 bytes | 55.148.544 bytes |

12× supone 2,25 veces los texels de 8×. El compositor comprueba un presupuesto configurable de **64 MiB para la salida HD**, con divisiones previas para evitar desbordamientos. El presupuesto no incluye escena, referencias clásicas, temporales, recurso ni asignador; no es un límite de memoria total del proceso. Tampoco garantiza que una reserva no falle por memoria insuficiente del sistema.

Esta implementación CPU recompone referencias y escala el fondo completo. Es un piloto de corrección, no una arquitectura final optimizada ni una promesa de 60 Hz. Antes de integración: decidir destino físico o atlas/caché, reducir copias, medir CPU/GPU y p95/p99 por frame y memoria en escenarios representativos. No aumentar el canvas de todo el juego a 12× por asumir que toda textura necesita esa densidad.

## Verificación reproducible

```
python tools/modernization/check_soldier_art_hd.py
python tools/modernization/check_soldier_art.py
```

Prueba nueva C++ también en CTest (`soldier_art_hd_isolated`) de Windows/Linux. Linux añade ejecución ASan/UBSan. Prueba local: 132 casos de retorno, PC/Amiga, desplazamiento de anclaje, densidades 1/8/12, igualdad del resultado 1× con el compositor nativo, detalle HD distinto de ampliar 16×14, alfa 0/128/255 contra ecuación independiente, píxeles exteriores intactos, cursor temprano, escritura posterior incluso de igual color, OR, Save/Restore/Clear, cuerpo duplicado, destino distinto, pitch, recurso ausente/incompatible y presupuesto. Repeticiones 0/1/5 conservan la escena retenida; **no son nuevos replays de la simulación completa**. El destino 352×272 a 12× se comprueba explícitamente.

Regresión nativa: 64 casos existentes de C01 con adaptadores reales conservados. PNG fuente contrastado por SHA-256. No se afirma inspección visual SDL, GPU o Windows físico. CI propia y paquete se registran aparte; no atribuirles el PASS de 30ba0ec.

## Siguiente

Validar físicamente la corrección de Save (causa reproducida/corregida en 2.59), después integrar opcionalmente el destino HD en una publicación de misión conservando el contraste clásico y la identidad temporal. Ampliar oclusiones solo con un contrato de escrituras verificable; no superponer a ciegas una textura al final. Medir costes antes de fijar 12×. Cursor, atlas de animaciones y terrenos siguen pendientes.
