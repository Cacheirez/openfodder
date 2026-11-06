# Inicio ligero de un nuevo hilo — OpenFodder

Las reglas permanentes están en [AGENTS.md](../../AGENTS.md). El bloque «Arranque rápido» al principio de [CONTINUIDAD.md](CONTINUIDAD.md) es la **única lectura de estado obligatoria**; el resto es consulta bajo demanda. Este prompt no copia la historia del proyecto.

## Prompt para copiar

```text
Continúa OpenFodder en https://github.com/Cacheirez/openfodder
Rama modernization/windows-foundation. PR #1 abierta, en borrador y SIN fusionar.
Trabaja en español de España, sin subagentes ni confirmaciones rutinarias.

Lee AGENTS.md y SOLO la sección «Arranque rápido» (primeras ~12 líneas) de docs/modernization/CONTINUIDAD.md. Verifica HEAD, cambios locales y estado de la PR; si detectas arte más reciente, ajusta el siguiente paso. NO leas completos el plan, informes históricos, catálogos o manifiestos salvo necesidad justificada.

Tarea de ESTA sesión: realizar exclusivamente el siguiente microbloque artístico pendiente según el arranque rápido: UNA dirección del lanzacohetes (habitualmente 3 poses/frame), sin regenerar familias ya terminadas. Sigue el contrato artístico y de selección del repositorio, reutilizando C01 y solo las referencias necesarias. No avances automáticamente a otra dirección.

CRÍTICO — Presupuesto de contexto: no imprimas ni pegues imágenes codificadas en Base64, data:image, HTML de visores, grandes JSON, diffs ni logs; conserva los archivos en el workspace y comunica rutas, SHA, conteos, errores filtrados y resúmenes breves (idealmente menos de 8 KB por salida de herramienta). Visualiza únicamente los maestros que sea necesario inspeccionar.

Tras generar una dirección: valida consistencia, alfa, derivados 8×/12×, vinculaciones y pruebas focalizadas, sin atribuir aceptación jugable a CI verde. Crea commits coherentes y actualiza SOLO el arranque rápido de CONTINUIDAD.md y evidencia pertinente. Si no puedes publicar, conserva recuperación reproducible y dilo. Si se llena el contexto, DETENTE y releva; no cambies a Astra por este motivo.

Finaliza con Hecho / Situación del plan / Próximos pasos / Escalado.
```

## Adjuntos

Con GitHub conectado, ninguno obligatorio: maestros y arte versionados están en el repositorio. Para revisar un defecto visual nuevo, adjuntar solo la captura o el log acotado pertinente, nunca un volcado completo de medios o datos privados CD32.

## Relevo tras el microbloque

Antes de iniciar otro hilo, exige commits y actualización del «Arranque rápido»: dirección/frames producidos, SHA, pruebas que sí se ejecutaron, bloqueos, archivos no publicados y **una sola siguiente dirección**. No transcribir la sesión anterior a la documentación.
