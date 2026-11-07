# AGENTS.md — reglas permanentes de OpenFodder

Trabaja en **español de España**. Repositorio `Cacheirez/openfodder`, rama `modernization/windows-foundation`. **PR #1 abierta, en borrador y SIN fusionar**; nunca modificar `master`. No usar subagentes sin permiso explícito.

## Fuente de verdad y arranque con contexto mínimo

1. Comprueba HEAD, estado de la PR y, solo si afectan al bloque, CI reciente. Revisa `git status --short` antes de tocar un checkout existente; no destruyas cambios locales.
2. Lee **solo «Control operativo — siguiente paso»**, al principio de `docs/modernization/PLAN_TRABAJO.md`, y «Arranque rápido» de `CONTINUIDAD.md` (primeras líneas). No cargues de entrada documentos completos ni informes históricos.
3. Amplía la lectura **por fichero y fragmento**, únicamente ante una necesidad técnica. `DESARROLLO.md` contiene recetas de pruebas. Las decisiones y evidencias antiguas siguen disponibles, pero no se releen sistemáticamente.
4. **`PLAN_TRABAJO.md` es la única autoridad sobre la siguiente tarea**, en su sección de control operativo. **`CONTINUIDAD.md` registra el último trabajo comprobado, evidencias, bloqueos y recuperación**. Si discrepan, contrastar HEAD y corregir ambos antes de trabajar. El plan 2.74 sigue vigente salvo cambio de alcance explícito.

## Presupuesto de contexto y trabajo artístico

- Una sesión de generación artística debe abordar **una sola dirección de una sola familia**, normalmente sus tres frames, seguida de validación, commit y relevo. Reducir a un solo frame si el intercambio de imágenes vuelve a ser excesivo. No pedir «completa todas las direcciones» en un solo hilo. No abrir tareas posteriores automáticamente.
- Para cada pose consultar únicamente **C01, los maestros necesarios de esa dirección y las referencias nativas pertinentes**. Reutilizar assets, prompts y contratos aprobados; no volver a recuperar todas las hojas o a regenerar marchas, granadas y apuntado si siguen siendo válidos.
- **Nunca volcar en la conversación** PNG/JPG binarios, cadenas Base64, `data:image`, HTML de visores con imágenes incrustadas, grandes manifiestos, JSON completos, diffs extensos ni logs completos. Para inspeccionarlos, usar archivos del workspace y mostrar solo ruta, dimensiones, SHA-256, contadores, estadísticas y fragmentos pertinentes. Visualizar imágenes específicas por separado cuando haga falta valorarlas.
- Limitar salidas de comandos y herramientas a lo relevante (idealmente menos de 8 KB por llamada); redirigir logs a archivos y leer solo errores, últimas líneas o intervalos filtrados. No volver a transmitir bloques enormes por intentar resumirlos.
- Antes de saturar la sesión: guardar originales/derivados, validar y publicar commits coherentes. **Tras cada microbloque completado, actualizar el control operativo del plan con una sola tarea siguiente y «Arranque rápido» con evidencias breves**, preferiblemente en el mismo cierre; no avanzar de tarea sin publicar el relevo. Si no se puede publicar, dejar ruta, hashes e instrucciones reproducibles, mantener el paso pendiente y no darlo por entregado. Abrir otro hilo si se acerca el límite.
- **Publicación de binarios:** preferir `git push` desde un checkout con autenticación Git/GitHub ya configurada. Antes de empezar un bloque con PNG, comprobar una vez que el mecanismo de publicación es viable, sin publicar cambios de prueba ni exponer credenciales. **Si `git push` falla por falta de credenciales, NO reconstruir automáticamente commits con PNG mediante el conector de GitHub ni enviar archivos como Base64 a herramientas o al chat.** Conservar el commit local, indicar SHA, ubicación recuperable y modo de publicar desde un entorno autenticado, y detenerse. El conector sí puede servir para consultar GitHub y modificar texto pequeño cuando proceda.
- No confundir **contexto agotado** con **dificultad técnica**: cambiar a Astra no resuelve un exceso de imágenes/texto. Si ocurre, cerrar/relevar, reducir el lote y evitar salidas voluminosas.

## Garantías del proyecto

- Modernizar Cannon Fodder 1, con CD32 como destino principal, **sin alterar simulación**: reglas, RNG, colisiones, reloj lógico, orden, campo visible, dirección/frame elegidos por el motor (`mFaceDirection` y apuntado). Marcha: 8 direcciones × 3 claves, ciclo original 0–1–2–1 con excepciones, no reloj ligado a FPS.
- Mantener intocada base clásica `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`, referencia independiente y H3 de 11 fases / 11.361 estados. No modificar referencias para ocultar regresiones.
- Estilo **C — Pintado moderado**, C01 aceptado; otros maestros según su estado documentado. No reflejar arte, reinventar estados ni mezclar estilos por comodidad.
- La alternancia del piloto `PROBAR_SOLDADO_ANIMADO.cmd` **no está aceptada**. Son necesarias cobertura completa, variantes, múltiples soldados, oclusiones, recortes y transiciones; un lote parcial/CI verde no demuestra aceptación jugable.
- Conservar modo clásico opcional y recuperación segura ante fallos reales; no desactivar protecciones. Datos comerciales CD32, partidas y recursos privados fuera de GitHub.

## Calidad, bloqueo y cierre

Delimitar **una única tarea del control operativo del plan**, dimensionada para una sesión; cambios mínimos y completos; pruebas focalizadas primero, H3/CI Windows-Linux y revisión visual pertinentes antes de entregar un ejecutable. No repetir pruebas válidas salvo regresión. Marcar lo no ejercitado **PENDIENTE**. Publicar commits y evidencia breve; actualizar plan y continuidad cuando el paso esté verificado. Si queda a medias, conservarlo como tarea pendiente con criterios explícitos; no iniciar el siguiente.

Tras **dos hipótesis técnicas distintas** sin progreso, descartar causas de entorno/permisos, preparar caso reproducible y **proponer**, no activar, Astra Bajo/Medio. El informe de escalado debe contener SHA, esperado/observado, pruebas, hipótesis descartadas y pregunta concreta. Volver al modelo habitual tras el diagnóstico. La falta de contexto exige un relevo más corto, no escalado de modelo.

**Sugerencia de hilo nuevo al cerrar un microbloque:** una vez que el trabajo esté validado, los commits válidos publicados y `PLAN_TRABAJO.md` / `CONTINUIDAD.md` sincronizados con HEAD, **recomendar expresamente abrir un hilo nuevo en Codex** para abordar el siguiente bloque usando `PROMPT_NUEVO_HILO.md`. Es una **recomendación, no una obligación**: el usuario decide. No sugerir el cambio automáticamente tras una sola compactación si la tarea continúa progresando. Si hay cambios sin publicar o falta el relevo, indicar primero qué falta y cómo recuperarlo; no presentar el bloque como cerrado.

Finalizar cada bloque con **Hecho**, **Situación del plan**, **Próximos pasos**, **Escalado: NO/SÍ** y **Nuevo hilo: recomendado/no necesario (motivo)**. Separar pruebas técnicas de aceptación visual.
