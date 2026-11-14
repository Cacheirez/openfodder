# Prompt universal de continuación — OpenFodder

Válido para **cualquier fase del proyecto** y cualquier hilo nuevo en Work/Codex. No contiene la tarea siguiente: esta se consulta en la cabecera del [plan vigente](PLAN_TRABAJO.md). [AGENTS.md](../../AGENTS.md) mantiene las reglas y [CONTINUIDAD.md](CONTINUIDAD.md) registra el último avance y las evidencias.

## Copiar al nuevo hilo

```text
Continúa la modernización de https://github.com/Cacheirez/openfodder en la rama modernization/windows-foundation.
PR #1 siempre abierta, en borrador y SIN fusionar. Trabaja en español de España, con autonomía y sin subagentes.

ARRANQUE LIGERO:
1. Lee AGENTS.md.
2. Comprueba HEAD remoto, PR y cambios locales sin sobrescribir trabajo existente.
   Si la tarea incluye PNG u otros binarios, verifica también que tienes un procedimiento de publicación Git autenticado. No crees commits de prueba.
3. Lee SOLO la sección inicial «Control operativo — siguiente paso» de docs/modernization/PLAN_TRABAJO.md y «Arranque rápido» de docs/modernization/CONTINUIDAD.md.
4. Si hay discrepancias con código, arte o commits reales, contrástalas y corrige los documentos; no supongas que una tarea está terminada por figurar como tal.
5. Consulta exclusivamente los fragmentos de código, contratos y evidencias necesarios para ejecutar la tarea seleccionada.

TRABAJO DE ESTA SESIÓN:
Mantén UNA sola tarea activa cada vez, siempre del control operativo del plan. Al validarla, publicar cambios y sincronizar plan/continuidad; si la tarea siguiente sigue dentro del MISMO hito autorizado y no requiere decisión humana, continuar automáticamente con otro microbloque. No elegir tareas del historial, no cambiar de hito/familia por iniciativa propia ni comenzar una fase no autorizada. Para arte, un lote pequeño por microbloque; para código, un cambio acotado y probado. Si está autorizado A.1-HYBRID-P1, trabajar en el prototipo de compositor híbrido seguro, no en completar individualmente cientos de variantes del antiguo modo estricto.

PROTECCIÓN DEL CONTEXTO:
No pegues ni imprimas binarios, imágenes en Base64, HTML con data:image, manifiestos completos, grandes diffs o logs extensos. Trabaja sobre archivos y resume rutas, SHA-256, contadores y fallos concretos. Evita lecturas y pruebas repetitivas, e interrumpe los bucles sin progreso. Saturación del contexto = relevo corto, no motivo para cambiar a Astra.

CIERRE OBLIGATORIO:
- Comprueba los criterios de salida y ejecuta pruebas focalizadas; indica lo que NO se ha comprobado. La aceptación visual jugando sigue separada de la CI.
- Publica cambios válidos mediante commits coherentes en la rama, sin fusionar PR #1. Si `git push` falla por credenciales, **NO intentes volcar PNG/Base64 ni reconstruir el commit binario por el conector de GitHub**. Conserva el SHA local, proporciona una ruta de recuperación y detente; no des el trabajo por publicado.
- Tras CADA paso terminado, actualiza el apartado «Control operativo» de PLAN_TRABAJO.md con el último paso terminado y la siguiente tarea única, y «Arranque rápido» de CONTINUIDAD.md con resultados, SHA y pendientes. No cambies la versión/alcance del plan si no hace falta.
- Si el paso queda incompleto o bloqueado, NO avances el plan: mantén esa tarea pendiente y documenta el bloqueo y la recuperación.
- Verifica que ambos documentos coinciden con GitHub y publica el relevo. **Continúa solo si el siguiente microbloque pertenece al mismo hito autorizado**. Detente si el hito termina, hay que valorar el resultado jugando o artísticamente, cambia el alcance, la CI obligatoria falla, falta autorización/credenciales, se agota el presupuesto de reintentos o la plataforma impone un límite. No afirmes que puedes trabajar en segundo plano si no existe esa capacidad.

Al detenerte, finaliza con: Hecho / Estado del plan / Commits publicados / Trabajo no guardado / Próximos pasos / Escalado (NO o recomendación de Astra con motivo) / Nuevo hilo (recomendado al terminar un hito o degradarse el contexto). Respeta el límite de AGENTS.md: a lo sumo un reintento idéntico justificado; tras dos hipótesis diferentes sin progreso, documenta y detén la investigación.
```

## Acceso y adjuntos

Con acceso a GitHub no hay adjuntos obligatorios. Si hay un defecto visual nuevo, aportar únicamente la captura o log reducido relevante; nunca publicar materiales comerciales privados. Sin acceso a GitHub, usar una copia reproducible de la rama con código, arte, herramientas e historial/submódulos cuando proceda.

## Regla de mantenimiento

**Plan = qué hacer después. Continuidad = qué se ha hecho y cómo recuperarlo. AGENTS = cómo trabajar.** Actualizar la pequeña cabecera operativa al cerrar cada paso; no añadir resúmenes completos de cada hilo ni desplazar la tarea siguiente al prompt.
