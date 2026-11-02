# Entrega A — inventario y lote inicial

Estado 2.73 (02-11-2026): cinco maestros nuevos generados e integración SDL opcional implementada. C01 permanece intacto. Pruebas locales y CI Windows/Linux/comparador PASS; ZIP f72d6e7 verificado. La aceptación visual del lote por Miguel sigue pendiente.

Elegimos **Amiga The One m1p2 (Find Grenades)**. m1p1 no prepara la hoja 7 del primer jugador y no permite reutilizar C01 en ese recorrido. m1p2 ejercita los seis fotogramas seleccionados con más presencia de la hoja 7 que m1p3. La prueba lógica conserva el orden de las tres fases de campaña.

| Fase | Llamadas de preparación | Ticks distintos | Llamadas con claves del lote |
|---|---:|---:|---:|
| m1p1 | 593 | 149 | 52 |
| m1p2 | 6129 | 1534 | 2044 |
| m1p3 | 6840 | 1711 | 2520 |

Los contadores incluyen preparaciones repetidas dentro de un tick. Solo observan el primer jugador vivo; no representan todos los soldados, frames presentados ni porcentaje de cobertura HD. La captura ocurre antes de las comprobaciones finales de oclusión/publicación.

## Lote acotado

[Manifiesto del lote](../../assets/modernization/soldier-pilot-batch.json): hojas 2 (Face Left) y 7 (Face Right + Forward), frames 0, 1 y 2. Se reutiliza C01 en 7/0; los cinco maestros nuevos están en assets/modernization/soldier-pilot, con procedencia y hashes. Tablas Amiga verificadas: offsets 12/14/16 y 562/564/566, segmento eGFX_IN_GAME, cuerpo 16×14, modificadores 0/0. Los anclajes del arte nuevo requieren comprobación visual; no se dan por aceptados al copiar dimensiones.

Usar el frame capturado del motor y sus contadores originales. El índice de frame no distingue por sí solo reposo y marcha. No introducir un reloj de animación independiente. Mantener estilo C, originales, sombras clásicas, orden, oclusiones y retorno clásico en claves o condiciones no cubiertas. 12× es variante provisional de trabajo; 8× permanece disponible.

## Evidencia reproducible

- [Inventario completo](evidence/soldier-pilot-inventory.json), con claves y geometría por fase.
- [Procedencia y hashes](evidence/soldier-pilot-build.json).
- [Log y trazas íntegros comprimidos](evidence/soldier-pilot-traces.json.gz), archivo compartido v1, reconstrucción exacta verificada.
- H3: **PASS, tres fases y 3405 estados**, contra selección de Amiga The One del reference-gameplay-v1.json original, sin regenerar referencias.

La herramienta build_soldier_inventory_probe.py emite una copia diagnóstica de Sprite_Core.cpp: no modifica Source. Se compila esa copia en un ejecutable local separado y se ejecuta la campaña con las opciones registradas en la procedencia. analyze_soldier_inventory.py resume el log mediante --log y --out. archive_replay_evidence.py conserva los archivos originales después del ensayo. El ejecutable diagnóstico no es el paquete Windows.

## Integración y prueba visible

Activación explícita mediante OPENFODDER_SOLDIER_BATCH=1 junto con OPENFODDER_SOLDIER_HD=8 o 12. Sin la opción de lote se conserva el piloto C01; clásico sigue siendo el valor por defecto. La selección valida clave, recurso, geometría y animación. Conserva contraste, orden, oclusiones, recortes y retorno clásico. El compositor completo y el de capas coinciden píxel a píxel en los tests.

PROBAR_SOLDADO_ANIMADO.cmd inicia Amiga The One, misión 1 fase 2, para jugar a velocidad normal (sin --unit-test). Solo el primer soldado y las orientaciones cubiertas cambian. SOLDADO_ANIMADO.html permite inspeccionar los derivados exactos de 12×, pausar y variar la velocidad ilustrativa. Su secuencia 0–1–2–1 no sustituye al reloj original. Revisar piernas, estabilidad de cuerpo/casco, pies y cambios de orientación como conjunto; C01 no necesita nueva aprobación aislada.

Con diagnóstico activo, SOLDIER_BATCH_PUBLISHED registra clave y contador acumulado en la primera sustitución y cada 256; tiempos de composición y SDL de esa muestra. No son percentiles ni incluyen todo el frame. Los motivos de retorno mantienen su diagnóstico acotado.

## Validación del candidato

- 24 combinaciones de seis claves, dos formatos y dos densidades; ASan/UBSan. Clave/recurso/animación incorrectos, actor repetido, oclusión, paleta y equivalencia del compositor completo/capas.
- Método real WindowHD: seis claves a ambas densidades, transición de paleta y recuperación; protecciones anteriores de pausa/mapa/renderer conservadas.
- Recorrido Amiga completo con las seis claves publicadas realmente por SDL y 3405 estados H3 originales: [informe local](evidence/soldier-batch-local.json), [log y trazas](evidence/soldier-batch-final-traces.json.gz). Ejecutable local GCC O3 sin mixer, SDL software/dummy; no certifica GPU Windows ni FPS.
- Visor: seis buffers, secuencia y pausa/reanudación comprobadas con Skia Canvas; revisión visual de los derivados. No es prueba de DOM del navegador ni una captura del juego.
- CI Windows/Linux añade el recorrido del lote conservando las pruebas existentes. El empaquetado exige que el informe del lote corresponda al ejecutable entregado. CI completa PASS: Windows 41359306896, Linux 41359307009 y comparador 41359306892.

[Verificación del ZIP](evidence/soldier-batch-package.json): artefacto 13106475504, 303 archivos; informe del lote y 29 fases sin omisiones corresponden al ejecutable incluido. Vista HTML idéntica tras normalizar CRLF. VERSION.txt identifica el merge temporal de CI, no una fusión del PR.

Siguiente: revisar el conjunto a velocidad normal. No cierra H7 ni cubre todas las direcciones, estados o soldados. Los antiguos planes continúan marcados como obsoletos.
