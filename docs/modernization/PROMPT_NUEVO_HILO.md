# Prompt universal de continuación — OpenFodder

Válido para **cualquier fase del proyecto** y cualquier hilo nuevo en Work/Codex. No contiene la tarea siguiente: esta se consulta en la cabecera del [plan vigente](PLAN_TRABAJO.md). [AGENTS.md](../../AGENTS.md) mantiene las reglas y [CONTINUIDAD.md](CONTINUIDAD.md) registra el último avance y las evidencias.

## Copiar al nuevo hilo

```text
Continúa la modernización de https://github.com/Cacheirez/openfodder en la rama modernization/windows-foundation.
PR #1 siempre abierta, en borrador y SIN fusionar. Trabaja en español de España, con autonomía y sin subagentes.

ARRANQUE LIGERO:
1. Lee AGENTS.md.
2. Comprueba HEAD remoto, PR y cambios locales sin sobrescribir trabajo existente.
3. Lee SOLO la sección inicial «Control operativo — siguiente paso» de docs/modernization/PLAN_TRABAJO.md y «Arranque rápido» de docs/modernization/CONTINUIDAD.md.
4. Si hay discrepancias con código, arte o commits reales, contrástalas y corrige los documentos; no supongas que una tarea está terminada por figurar como tal.
5. Consulta exclusivamente los fragmentos de código, contratos y evidencias necesarios para ejecutar la tarea seleccionada.

TRABAJO DE ESTA SESIÓN:
Ejecuta UNA sola tarea verificable indicada por el control operativo del plan. No elijas tareas por el historial del chat, no amplíes el alcance ni empieces automáticamente la siguiente. Para arte, un lote pequeño (máximo una dirección/familia por hilo); para código, un cambio acotado con pruebas.

PROTECCIÓN DEL CONTEXTO:
No pegues ni imprimas binarios, imágenes en Base64, HTML con data:image, manifiestos completos, grandes diffs o logs extensos. Trabaja sobre archivos y resume rutas, SHA-256, contadores y fallos concretos. Evita lecturas y pruebas repetitivas, e interrumpe los bucles sin progreso. Saturación del contexto = relevo corto, no motivo para cambiar a Astra.

CIERRE OBLIGATORIO:
- Comprueba los criterios de salida y ejecuta pruebas focalizadas; indica lo que NO se ha comprobado. La aceptación visual jugando sigue separada de la CI.
- Publica cambios válidos mediante commits coherentes en la rama, sin fusionar PR #1. Conserva recuperación reproducible de trabajo no publicado.
- Tras CADA paso terminado, actualiza el apartado «Control operativo» de PLAN_TRABAJO.md con el último paso terminado y la siguiente tarea única, y «Arranque rápido» de CONTINUIDAD.md con resultados, SHA y pendientes. No cambies la versión/alcance del plan si no hace falta.
- Si el paso queda incompleto o bloqueado, NO avances el plan: mantén esa tarea pendiente y documenta el bloqueo y la recuperación.
- Verifica que ambos documentos coinciden con GitHub, publica el relevo y DETENTE.

Finaliza con: Hecho / Estado del plan / Commit publicado / Trabajo no guardado / Próximos pasos / Escalado (NO o recomendación de Astra con motivo).
```

## Acceso y adjuntos

Con acceso a GitHub no hay adjuntos obligatorios. Si hay un defecto visual nuevo, aportar únicamente la captura o log reducido relevante; nunca publicar materiales comerciales privados. Sin acceso a GitHub, usar una copia reproducible de la rama con código, arte, herramientas e historial/submódulos cuando proceda.

## Regla de mantenimiento

**Plan = qué hacer después. Continuidad = qué se ha hecho y cómo recuperarlo. AGENTS = cómo trabajar.** Actualizar la pequeña cabecera operativa al cerrar cada paso; no añadir resúmenes completos de cada hilo ni desplazar la tarea siguiente al prompt.
