# AGENTS.md — OpenFodder

Instrucciones permanentes para agentes que trabajan en este repositorio. Aplican tanto a ChatGPT Work como a Codex u otras herramientas que lean este archivo. Trabajar en **español de España**.

## Repositorio, autoridad y alcance

- Repositorio: `Cacheirez/openfodder`. Rama de trabajo: `modernization/windows-foundation`.
- Mantener la **PR #1 abierta, en borrador y SIN fusionar**. No trabajar en `master` ni crear una PR alternativa salvo petición expresa.
- No usar subagentes ni delegar trabajo sin autorización explícita.
- Al comenzar, comprobar HEAD, estado de PR y CI *reales*. No dar por vigente un resultado de CI antiguo.
- Leer `docs/modernization/CONTINUIDAD.md` (estado y siguiente paso) y el apartado pertinente de `PLAN_TRABAJO.md` (plan 2.74 salvo actualización posterior explícita).
- Consultar `SOLDADOS_COBERTURA_COMPLETA.md`, `DESARROLLO.md` y `ALCANCE_H0_H10.md` **solo cuando afecten al bloque**. La documentación histórica y los informes son evidencia, no órdenes para rehacer trabajo ya terminado.

## Invariantes de calidad

- Objetivo: modernizar **Cannon Fodder 1**, priorizando CD32, sin alterar jugabilidad ni campo lógico visible.
- No modificar reglas, RNG, colisiones, secuencia, relojes lógicos ni selección original de frames. Respetar `mFaceDirection`, apuntado independiente y orden de dibujo. La marcha tiene **8 direcciones × 3 claves**, ciclo original 0–1–2–1 con sus excepciones: no introducir un reloj ligado a FPS ni sustituirlo por dos imágenes genéricas.
- Conservar intacta la base clásica `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`, la comparación independiente y las referencias H3: **11 fases, 11.361 estados (7.956 PC + 3.405 Amiga)**. No regenerar referencias para encubrir diferencias.
- Mantener estilo **C — Pintado moderado** y maestro C01 aceptado; las otras cinco poses son provisionales. No reabrir elecciones de estilo sin regresión demostrada.
- La alternancia entre soldado moderno y clásico en el piloto `PROBAR_SOLDADO_ANIMADO.cmd` **NO está aceptada**. Sustituir todos los soldados/estados del alcance, respetando variantes, agua, recortes, oclusiones y orden. Las 24 poses de marcha no equivalen a cobertura total.
- Conservar modo clásico por elección y recuperación coherente ante **fallos reales**. No quitar protecciones ni considerar la falta de arte o un retorno normal al clásico como funcionalidad terminada.
- No subir a Git datos comerciales CD32, partidas ni material privado.

## Ejecución eficiente sin rebajar calidad

1. Elegir el **siguiente bloque verificable** del plan vigente; delimitar objetivo, ficheros, hipótesis y criterio de salida.
2. Reutilizar pruebas y diagnósticos válidos; no releer todo el repositorio ni repetir investigaciones concluidas. Consultar solo fuentes y código necesarios.
3. Aplicar cambios pequeños pero completos; ejecutar primero pruebas focalizadas y sanitizadores pertinentes. Antes de entregar un ejecutable/ZIP, ejecutar la CI necesaria Windows/Linux, H3 y validación visual aplicable, con hashes y evidencia vinculada al commit.
4. No confundir compilación/CI verde, captura de claves o manifiesto vacío con cobertura HD ni aceptación visual. Marcar siempre lo no ejecutado como **PENDIENTE**.
5. Evitar refactorizaciones accesorias, generaciones masivas de arte sin comprobar una secuencia completa, logs gigantes y bucles de prueba sin información nueva. No eliminar controles para ahorrar tiempo o cuota.
6. Crear commits coherentes; actualizar `CONTINUIDAD.md` y la evidencia afectada cuando exista avance real, sin duplicar la historia en varios documentos.

## Detección de bloqueo y escalado de modelo

Usar por defecto el modelo de desarrollo económico que haya seleccionado el usuario. **No cambiar de modelo ni activar Astra de forma autónoma.**

- Si **dos hipótesis técnicas distintas**, comprobadas con pruebas relevantes, no producen progreso o se repite el mismo error sin nueva evidencia, detener la iteración especulativa.
- Antes de escalar, descartar problemas de permisos, dependencias, entorno, datos ausentes o herramientas; reducir a un caso reproducible.
- Sugerir **Astra (primero nivel Bajo, o Medio si se justifica)** para una causa raíz difícil, regresiones inexplicadas o una decisión arquitectónica importante. Se puede sugerir antes si la complejidad es manifiesta; no forzar fallos artificiales.
- Presentar un informe breve: commit SHA, resultado esperado/observado, pasos de reproducción, pruebas y logs, hipótesis descartadas, pregunta concreta para Astra y cómo devolver la implementación al modelo habitual.
- No prolongar pruebas infructuosas ni prometer que el modelo cambiará automáticamente. Si hay progreso real y medible, continuar sin escalado.

## Cierre de cada bloque

Responder con **Hecho**, **Situación del plan**, **Próximos pasos** y **Escalado: NO/SÍ (motivo)**. Distinguir claramente código implementado, tests ejecutados, limitaciones y aceptación visual del usuario.
