# H6 — evaluación inicial de densidad del arte C

**Actualización 2.58:** ambas densidades revisadas por Miguel; preferencia por alta condicionada al coste. [Piloto HD aislado implementado](H6_4_PILOTO_HD_AISLADO.md), sin conexión SDL; falta medir antes de fijar densidad.

28-10-2026. Evaluación geométrica, no aceptación visual ni decisión definitiva. C — Pintado moderado se conserva; el cursor también forma parte del rediseño. No producir animaciones todavía. Actualización 29-10: Miguel autoriza avanzar en tareas independientes mientras prueba opciones; escenas aceptadas. Preparación técnica y comparación instrumental permitidas, elección visual pendiente.

La geometría lógica permanece 320×200 PC / 320×225 Amiga. El ajuste usa `min(ancho físico/320, alto físico/alto lógico)`. La escala Windows del 300 % no se vuelve a multiplicar: el renderer ya informa píxeles físicos. Los recursos se eligen por densidad, no por cada resolución de monitor; un maestro puede generar niveles de detalle compartidos por fondos y sprites. La resolución nativa de dibujo y la ventana son conceptos distintos.

Ejemplo PC con la pose de cuadro lógico 16×14 de C01:

| Salida física | Escala máxima con aspecto original | Pose en pantalla, antes de cuantizar |
|---|---:|---:|
| 640×480 (4:3) | 2× | 32×28 |
| 1280×960 (4:3) | 4× | 64×56 |
| 1600×1200 (4:3) | 5× | 80×70 |
| 1920×1440 (4:3) | 6× | 96×84 |
| 2880×2160 (4:3) | 9× | 144×126 |
| 1280×720 (16:9) | 3,6× | 57,6×50,4 |
| 1920×1080 (16:9) | 5,4× | 86,4×75,6 |
| 2560×1440 (16:9) | 7,2× | 115,2×100,8 |
| 3840×2160 (16:9) | 10,8× | 172,8×151,2 |

En Amiga a UHD la escala es 9,6× y el cuadro 153,6×134,4. Maximizar una ventana deja menos área útil que pantalla completa; calcular siempre con la salida real.

| Densidad de recurso | Pose 16×14 | RGBA por cuadro, sin compresión/mips | Ampliación adicional en UHD PC |
|---|---:|---:|---:|
| 2× | 32×28 | 3.584 bytes | 5,4× |
| 4× | 64×56 | 14.336 bytes | 2,7× |
| 8× | 128×112 | 57.344 bytes | 1,35× |
| 12× | 192×168 | 129.024 bytes | reducción a 0,9× |

Conclusión técnica provisional: 2×/4× no garantizan conservar detalle pintado en UHD. Comparar una pose maestra a 8× y 12× sobre el mismo fondo, a 1080p/1440p/UHD, antes de elegir. Una fuente mayor no obliga a mantener todos los frames a esa densidad: pueden generarse niveles de detalle y atlas según tamaño en pantalla. La tabla no estima la memoria total de un juego: faltan número de frames, atlas, padding, mips y recursos simultáneos.

C01 actual se reduce a 16×14 y se compone en la superficie nativa. Aumentar solo el PNG no producirá detalle HD: hace falta un destino de presentación de mayor resolución conservando geometría, orden, recorte y anclajes lógicos. Mantener el retorno clásico por recurso no disponible o no compatible. El cursor requiere su propio hotspot, estados y comprobación sobre fondos claros/oscuros, sin cambiar la precisión del ratón.

Próxima comparación visual: misma pose, mismo encuadre y escala lógica, tres salidas físicas; revisar silueta, rostro/rifle, bordes alfa, pies/sombra, oclusión y estabilidad al moverse. Para fondos, comenzar por un recorte/tile de referencia a densidad equivalente, no redibujar todavía todos los mapas. No se han generado nuevas imágenes en esta evaluación.

## Avance 2.55 — comparación técnica autónoma

[Visor 8×/12× y reproducción](../../assets/modernization/density-review/README.md). Carga el original sin modificarlo y prepara ambas densidades en memoria con el promedio premultiplicado del piloto. Modelo 1× contrastado exactamente con los 224 píxeles del header nativo; 96 combinaciones de salida/plataforma/DPR y pruebas alfa/anclaje aprobadas localmente. HTML autónomo generado de forma reproducible; no requiere instalar herramientas para abrirlo.

CI independiente añade prueba de navegador y capturas, pendiente al publicar. La instalación local de Chromium falló al recibir un archivo de descarga incompleto; no se declara inspección visual local. La selección definitiva de densidad y la valoración visual son de Miguel; avanzar esta herramienta no las sustituye. Fondos neutros de prueba, no jungla de producción. Mantener arte original y cuadro lógico; ninguna modificación de Source ni del piloto integrado.

**Primera CI cerrada:** f842b3d, run 40800565963 PASS completo, incluido navegador Linux DPR 1/3. [Evidencia y artefacto verificado](H6_DENSIDAD_VALIDACION_f842b3d.json). HTML idéntico al de Git, capturas inspeccionadas. Se ajusta la inspección por defecto a 2× y el desplazamiento horizontal para que a 4× no queden bordes inaccesibles; nueva comprobación de navegador añadida. No atribuir el resultado de navegador a Windows/SDL ni a aprobación de densidad.

**Cierre 29-10, plan 2.56:** revisión 30ba0ec, Windows/Linux/navegador completos PASS; paquete corregido y visor verificados. [Evidencia final](VALIDACION_30ba0ec.json). Las menciones de CI pendiente anteriores describen el estado al publicar. Aceptación manual de opciones y elección visual de densidad siguen pendientes.
