# Estado operativo — 2 de noviembre de 2026

**Plan 2.74. Tarea activa: sustitución completa de soldados.** Leer [plan](PLAN_TRABAJO.md) y [revisión de cobertura](SOLDADOS_COBERTURA_COMPLETA.md). La siguiente implementación empieza por A1/A2: cerrar matriz y composición; los seis frames actuales no cumplen el objetivo.

## Última observación de Miguel

Probó `PROBAR_SOLDADO_ANIMADO.cmd`: el nuevo soldado aparece intercalado con el antiguo. Pide sustituirlo en todos los casos, revisar todos los sprites y reproducir las ocho direcciones y el movimiento original. **No interpretar esta prueba como aceptación del lote.** No volver a pedirle validar la misma muestra parcial antes de corregirla.

## Estado comprobado

- Repositorio: https://github.com/Cacheirez/openfodder · rama `modernization/windows-foundation` · PR #1 abierto, borrador, sin fusionar.
- Último código/ZIP probado: `f72d6e792c359cec2f53d006d167738c2104bc66`. CI Windows 41359306896, Linux 41359307009 y comparador 41359306892 PASS. ZIP 13106475504: 303 archivos; 29 fases públicas sin omisiones; lote publica seis claves y conserva 3405 estados H3 Amiga. [Verificación y hashes](evidence/soldier-batch-package.json).
- Ese PASS es técnico, no cobertura visual completa. Solo dos orientaciones, primer jugador, un parche y retornos conservadores. [Diagnóstico de los cuatro límites](SOLDADOS_COBERTURA_COMPLETA.md#por-qué-se-intercala-el-clásico).
- Inventario estático nuevo: PC jugador 158 claves, Amiga jugador 159, enemigos 160 por formato; 71 hojas por bando. Marcha: 24 claves por bando. No confundir entradas de tablas con imágenes únicas por producir o estados ya probados. Rutas especiales/civiles/efectos clasificados aparte.
- No se ha modificado el motor ni arreglado la alternancia en la revisión documental 2.74. No hay un ZIP posterior que la corrija.

## Decisiones que se conservan

Estilo **C — Pintado moderado**; C01 aceptado en detalle, posición e integración del comparador. Guardado/persistencia y recorrido común de escenas aceptados. No repetir elección A/B/C ni esas pruebas sin una regresión concreta. Cinco maestros adicionales generados, provisionales. 12× de trabajo y 8× alternativa; GPU/densidad final pendientes.

Objetivo: CF1 modernizado, CD32 principal, presentación suave y nueva sin alterar jugabilidad ni campo lógico. Equipo de prueba de Miguel: Windows 11, 3840×2160, escala 300 %. Base clásica `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`, no mover ni reescribir. H3 original: 11 fases y 11361 estados (7956 PC + 3405 Amiga). Mantener contraste independiente, orden, anclaje, sombras y recortes. Datos comerciales privados fuera de GitHub.

## Para continuar

1. Comprobar HEAD, PR y CI reales. HEAD documental puede ser posterior al código validado.
2. Leer el catálogo y el productor/compositor afectados; ampliar las pruebas para impedir mezcla normal, no solo verificar que HD aparece alguna vez.
3. Implementar captura/múltiples cuerpos y cobertura original completa con pasos internos verificables. Entregar otro ZIP solo después de las pruebas pertinentes.
4. Registrar aceptación visual exacta y límites; no cerrar A/H7 por CI verde.

Recuperación y compilación: [DESARROLLO.md](DESARROLLO.md). Relevo: [PROMPT_NUEVO_HILO.md](PROMPT_NUEVO_HILO.md). Mensajes al usuario: terminar con `Hecho:`, `Situación del plan:` y `Próximos pasos:`. Sin subagentes salvo autorización expresa.
