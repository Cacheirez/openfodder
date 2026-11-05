# OpenFodder — documentación vigente

**Estado único:** [CONTINUIDAD.md](CONTINUIDAD.md). **Plan único:** [PLAN_TRABAJO.md](PLAN_TRABAJO.md), versión 2.74.

La alternancia moderno/clásico observada por Miguel sigue sin resolver como producto completo. El lanzador conserva el piloto de seis poses. La rama ya incluye 24 poses de marcha, ocho de apuntado bajo y 24 de granada, con pruebas internas y CI de implementación PASS; falta cubrir los demás estados/variantes y obtener aceptación visual. El siguiente bloque técnico es el lanzacohetes del jugador, según CONTINUIDAD.md.

## Leer para trabajar

1. [Estado, CI y límites del relevo](CONTINUIDAD.md).
2. [Plan y orden de implementación](PLAN_TRABAJO.md).
3. [Soldados: catálogo, diagnóstico y criterio de cobertura completa](SOLDADOS_COBERTURA_COMPLETA.md).
4. [Recuperación, compilación y pruebas](DESARROLLO.md), cuando haga falta ejecutar.
5. [Prompt para otro hilo y adjuntos](PROMPT_NUEVO_HILO.md).

## Referencias que siguen aportando

- [Requisitos completos H0–H10](ALCANCE_H0_H10.md): alcance final; no es un segundo plan.
- [Lote f72d6e7](LOTE_SOLDADO_PILOTO.md) y [paquete comprobado](evidence/soldier-batch-package.json): evidencia técnica de la muestra incompleta, no aceptación del soldado.
- Código, tests y workflows: autoridad para comportamiento y construcción. Los contratos H3/H4/H5/H6 describen su revisión; consultar solo los que afecte el cambio.
- [Maestros y conceptos](../../assets/modernization/concepts/README.md), [C01](../../assets/modernization/soldier-c01/manifest.json), [lote provisional](../../assets/modernization/soldier-pilot/GENERACION.md).
- [Inventario CD32](CD32_CENSO_SPRITES.md): metadatos, no datos comerciales ni cobertura dinámica completa.
- [Política de limpieza y referencias históricas](DOCUMENTACION.md): qué se eliminó y qué se conserva.

No usar versiones antiguas, informes de validación o bitácoras como lista de próximas tareas. Consultar la CI por commit en CONTINUIDAD.md; un verde no demuestra cobertura completa ni aceptación.
