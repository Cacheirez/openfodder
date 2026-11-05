# Prompt breve para continuar OpenFodder

Usa este texto en un nuevo hilo de ChatGPT Work o Codex. Las reglas permanentes están en [AGENTS.md](../../AGENTS.md); el estado actual está en [CONTINUIDAD.md](CONTINUIDAD.md). Evita copiar aquí todo el historial.

## Prompt para copiar

```text
Continúa OpenFodder: https://github.com/Cacheirez/openfodder
Rama: modernization/windows-foundation.

Trabaja en español de España, con autonomía y sin pedir confirmaciones rutinarias. No uses subagentes sin mi autorización. Mantén la PR #1 abierta, en borrador y SIN fusionar.

Lee primero AGENTS.md en la raíz. Verifica HEAD, PR y CI actuales; después lee docs/modernization/CONTINUIDAD.md y la parte pertinente de PLAN_TRABAJO.md. Consulta SOLDADOS_COBERTURA_COMPLETA.md y DESARROLLO.md para los detalles técnicos necesarios. Los informes antiguos no determinan el próximo paso.

Incidencia aún NO aceptada: PROBAR_SOLDADO_ANIMADO.cmd intercala soldados modernos y clásicos. El objetivo es sustituir de forma coherente todos los soldados, orientaciones, animaciones y estados del alcance conservando la lógica y el render original. No presentes de nuevo el piloto de seis poses como una solución terminada.

Antes de modificar un checkout previo, revisa sus cambios y commits locales; CONTINUIDAD.md registra las limitaciones del último relevo. No des por respaldado trabajo local desconocido ni apliques recuperaciones antiguas sobre HEAD sin revisar.

Ejecuta el siguiente bloque verificable del plan: cambio útil, pruebas focalizadas, evidencia y commit coherente. Sigue las garantías de AGENTS.md. No atribuyas aceptación visual a una CI verde ni entregues ZIP sin las validaciones pertinentes.

Evita investigaciones repetidas y bucles sin progreso. Si hay bloqueo, aplica el protocolo de AGENTS.md: reproduce el fallo, documenta lo intentado y recomienda consultar Astra para una pregunta concreta. No cambies de modelo por tu cuenta. Vuelve al modelo habitual para implementar lo resuelto cuando sea adecuado.

Termina con Hecho, Situación del plan, Próximos pasos y Escalado (NO/SÍ y motivo).
```

## Adjuntos

- **Con GitHub conectado:** ninguno obligatorio; los recursos y la evidencia están versionados.
- **Opcionales para un defecto visual nuevo:** vídeo corto y `SOLDADO_ANIMADO.log`.
- **Sin GitHub:** aportar la rama con código, assets, documentación y herramientas, así como historial/submódulos/datos demo cuando se necesiten pruebas de equivalencia. Un ZIP del piloto no sustituye las fuentes.
- No compartir recursos comerciales CD32 ni partidas privadas sin una necesidad concreta.
