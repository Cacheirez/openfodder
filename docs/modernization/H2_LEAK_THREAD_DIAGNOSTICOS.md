# H2 — Ensayos de fugas y carreras (diagnóstico inicial)

Estos dos ensayos son **diagnósticos independientes**, ejecutados con SDL de vídeo y audio ficticios. Ambos usan exclusivamente las campañas de demostración incluidas en la suite de pruebas; no incorporan material comercial.

- **LeakSanitizer**: ejecuta de nuevo los 29 replays de OpenFodder con el binario `build-h2-asan`, `ASAN_OPTIONS=detect_leaks=1`, `LSAN_OPTIONS=exitcode=23:report_objects=1` y comparación con `reference-completion.json`. Evidencia: `reports/h2-leaksan/report.json` y `engine.log`.
- **ThreadSanitizer**: compila un segundo binario con `-fsanitize=thread` (nunca combinado con ASan) y recorre los ocho replays de PC Format. Evidencia: `reports/h2-threadsan/report.json` y `engine.log`. El runtime TSan puede no funcionar en determinados ejecutores CI Linux; un fallo de inicialización **no permite inferir que no haya carreras**.

**Criterio:** únicamente se puede afirmar `sin fugas detectadas` o `sin carreras detectadas` después de verificar los artefactos del sanitizador y la terminación de los replays. La ausencia de reportes no cubre rutas no ejecutadas, recursos todavía alcanzables por variables globales o la campaña CD32 privada.

**Estado CI al incorporar el diagnóstico:** los pasos son `continue-on-error: true` a propósito hasta comprobar que el runtime está disponible y las evidencias son interpretables; el resultado verde del workflow **no** representa su aprobación. La puerta ASan/UBSan anterior continúa siendo obligatoria.
