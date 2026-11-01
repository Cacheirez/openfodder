# Entrega A — inventario y lote inicial

Estado: inventario terminado; cinco recursos nuevos pendientes de producción e integración. No hay nuevo ZIP ni cambios del motor. C01 conserva la aceptación de Miguel.

Elegimos **Amiga The One m1p2 (Find Grenades)**. m1p1 no prepara la hoja 7 del primer jugador y no permite reutilizar C01 en ese recorrido. m1p2 ejercita los seis fotogramas seleccionados con más presencia de la hoja 7 que m1p3. La prueba lógica conserva el orden de las tres fases de campaña.

| Fase | Llamadas de preparación | Ticks distintos | Llamadas con claves del lote |
|---|---:|---:|---:|
| m1p1 | 593 | 149 | 52 |
| m1p2 | 6129 | 1534 | 2044 |
| m1p3 | 6840 | 1711 | 2520 |

Los contadores incluyen preparaciones repetidas dentro de un tick. Solo observan el primer jugador vivo; no representan todos los soldados, frames presentados ni porcentaje de cobertura HD. La captura ocurre antes de las comprobaciones finales de oclusión/publicación.

## Lote acotado

[Manifiesto del lote](../../assets/modernization/soldier-pilot-batch.json): hojas 2 (Face Left) y 7 (Face Right + Forward), frames 0, 1 y 2. Se reutiliza C01 en 7/0; faltan cinco imágenes. Tablas Amiga verificadas: offsets 12/14/16 y 562/564/566, segmento eGFX_IN_GAME, cuerpo 16×14, modificadores 0/0. Los anclajes del arte nuevo requieren comprobación visual; no se dan por aceptados al copiar dimensiones.

Usar el frame capturado del motor y sus contadores originales. El índice de frame no distingue por sí solo reposo y marcha. No introducir un reloj de animación independiente. Mantener estilo C, originales, sombras clásicas, orden, oclusiones y retorno clásico en claves o condiciones no cubiertas. 12× es variante provisional de trabajo; 8× permanece disponible.

## Evidencia reproducible

- [Inventario completo](evidence/soldier-pilot-inventory.json), con claves y geometría por fase.
- [Procedencia y hashes](evidence/soldier-pilot-build.json).
- [Log y trazas íntegros comprimidos](evidence/soldier-pilot-traces.json.gz), archivo compartido v1, reconstrucción exacta verificada.
- H3: **PASS, tres fases y 3405 estados**, contra selección de Amiga The One del reference-gameplay-v1.json original, sin regenerar referencias.

La herramienta build_soldier_inventory_probe.py emite una copia diagnóstica de Sprite_Core.cpp: no modifica Source. Se compila esa copia en un ejecutable local separado y se ejecuta la campaña con las opciones registradas en la procedencia. analyze_soldier_inventory.py resume el log mediante --log y --out. archive_replay_evidence.py conserva los archivos originales después del ensayo. El ejecutable diagnóstico no es el paquete Windows.

## Siguiente trabajo

Producir las cinco imágenes coherentes con C01, preparar sus derivados y comprobar juntos anclaje y ciclo. Generalizar después la selección a estas seis claves conservando los controles de contraste y retorno. Añadir contadores de sustitución efectiva y tiempos mínimos en esa integración. Antes del nuevo ZIP: H3, CI pertinente y prueba visible a velocidad normal. Esto no cierra H7 ni promete cobertura completa del recorrido.
