# H4.1 — Composición ordenada de capas de misión

25-10-2026. Trabajo sobre `a9877f1fd0653099fa97221aa7d527e5ad44b966`. PR #1 en borrador y sin fusionar. Base clásica sin cambios.

## Implementación y alcance exacto

`MissionLayers.hpp` introduce una representación retenida de las capas de misión. Cada orden conserva una identidad de destino, su procedencia (terreno, sprite, sidebar, cursor o superficie) y una operación. La secuencia se reproduce en su orden de inserción: la procedencia nunca es un criterio de ordenación.

Las operaciones son terreno retenido, escrituras indexadas decodificadas, sidebar retenido, Clear, Save y Restore. Las escrituras indexadas conservan asignaciones de cero, asignaciones iguales al color anterior y operaciones OR. No se deduce cobertura comparando imágenes. Sprites y cursor pueden usar `CaptureSprite8Producer`, que conserva valores decodificados sin punteros a recursos activos.

Cada destino conserva índices iniciales y guardados independientes, backing RGB y la paleta efectiva de presentación. Clear reproduce los índices actuales/guardados y el borrado visible del backing RGB, conservando padding. Save/Restore trabajan exclusivamente sobre copias privadas durante la composición: no llaman al motor ni consumen eventos. La salida incluye tanto la imagen final como el fondo guardado de cada destino. `RasterizeMissionLayers` convierte únicamente el destino solicitado, sin mezclar automáticamente otros destinos del mismo tamaño.

Las identidades ausentes, desconocidas o duplicadas y la geometría incompatible del fondo guardado se rechazan con `invalid_argument`. Como los kernels originales, las órdenes requieren geometría y extensiones válidas previamente recortadas. No es un parser de escenas arbitrarias ni una API concurrente. La validación del sink sigue siendo obligatoria antes de publicar.

**Este incremento implementa y prueba el compositor, pero todavía no conecta el registro de órdenes a los productores del motor.** `Interrupt_Redraw`, Graphics, Surface y la captura compuesta de `Video_SurfaceRender` permanecen sin cambios. La misión jugable aún utiliza el frame compuesto anterior. No se declara completada la separación de capas en producción.

## Pruebas

`python3 tools/modernization/check_mission_layers.py`: 192 combinaciones, 384 salidas retenidas, C++14 con ASan/UBSan. Matriz: terreno PC/Amiga, dos anchos, padding 0/3, Restore inicial opcional, Clear opcional, reanudación y 0/1/5 presentaciones. Dos destinos independientes de la misma geometría reciben órdenes intercaladas.

Se comparan los índices finales y guardados con un recorrido de referencia que aplica inmediatamente los kernels existentes; la conversión final compara todos los bytes y metadatos con `RasterizePresentationSurface`. Sprites reales decodificados, HUD, cursor anterior/posterior al terreno, cambios de paleta posteriores a las órdenes, liberación de fuentes, reutilización de capturas, modificación de salidas privadas, composición de pausa y retorno a misión. Casos específicos comprueban que invertir escrituras cambia la salida y que repetir una escritura del mismo color no elimina su cobertura.

La prueba de composición de pausa usa los kernels retenidos: no es una transición del motor completo. Las pruebas existentes de 144 escenarios de pausa y 240 escenarios de coordinadoras misión/pausa, con 672 capturas y reemplazo de recursos, siguen siendo la evidencia de esa integración previa. No hay cambios a sus referencias ni a los goldens H3.

Se añade un paso obligatorio de CI Linux con `detect_leaks=1`. El resultado local usa `detect_leaks=0`. No se presenta una compilación del motor local nuevo: este entorno no dispone actualmente de CMake/dependencias SDL.

## Conexión pendiente con el motor

1. Registrar cada operación en el adaptador que conoce su destino real. El registro debe conservar las órdenes de `mSurfaceFinal` sin añadirlas a `mSurface`.
2. Conservar las dos llamadas posibles al cursor y todos los efectos lógicos en sus coordinadoras. Retener solo las órdenes ya preparadas, sin repetir selección de recursos, visibilidad, registros ni consumo de solicitudes.
3. Registrar también Clear/Save/Restore, establecer la fuente inicial y delimitar la vida del registro. Capturar la paleta efectiva en el punto actual de conversión.
4. Auditar cualquier escritura por puntero directo que pueda escapar al registro. Comparar primero la composición de órdenes con el frame compuesto vigente; no activar un registro incompleto ni rellenar sus huecos con máscaras deducidas por diferencias de píxeles.
5. Ampliar los dobles de coordinadoras para verificar el registro real y ejecutar H3/replays/CI. Después ampliar vídeo real y otras escenas.

No se añaden cadencias, hilos, interpolación ni arte HD. El compositor copia destinos y fondos guardados y almacena órdenes decodificadas; aún no se ha medido ni optimizado su coste. La integración deberá limitar memoria y vida del registro entre presentaciones, incluyendo N=0.

## CI verificada

Revisión `ba2ef207a65fba5a1996f42cbb5517405750f122`: [Linux 40140490722](https://github.com/Cacheirez/openfodder/actions/runs/40140490722) y [Windows 40140490643](https://github.com/Cacheirez/openfodder/actions/runs/40140490643) aprobadas. Compilación, 6 CTests, todas las equivalencias anteriores, nuevo compositor 192/384, H3 original 11.361 estados y 29/29 fases sin omisiones PASS; ASan/UBSan, LSan y TSan sin hallazgos. La prueba nueva se compila en Linux; la compilación Windows sigue validando el motor existente, que aún no incluye este header.

[Evidencia conservada](evidence/ba2ef207-reports.json): metadatos, comprobaciones de jobs e informes originales. Descargados ambos ZIP, comprobados tamaño/SHA-256 e integridad; 9 report.json PASS y 12 engine.log sin diagnósticos de sanitizadores. Los ZIP/trazas completos caducan el 23-11-2026 UTC; no se afirma conservación externa permanente.

## Continuación 25-10-2026

El [registro de productores reales](H4_1_REGISTRO_PRODUCTORES.md) conecta este compositor como oráculo diagnóstico en el motor. La publicación continúa siendo clásica; el informe nuevo contiene el alcance y las pruebas vigentes. La falta de conexión descrita arriba corresponde a la revisión inicial de este documento.
