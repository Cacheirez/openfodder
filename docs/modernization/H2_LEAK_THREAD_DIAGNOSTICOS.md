# H2 — Ensayos de fugas y carreras (diagnóstico inicial)

Estos dos ensayos son **diagnósticos independientes**, ejecutados con SDL de vídeo y audio ficticios. Ambos usan exclusivamente las campañas de demostración incluidas en la suite de pruebas; no incorporan material comercial.

- **LeakSanitizer**: ejecuta de nuevo los 29 replays de OpenFodder con el binario `build-h2-asan`, `ASAN_OPTIONS=detect_leaks=1`, `LSAN_OPTIONS=exitcode=23:report_objects=1` y comparación con `reference-completion.json`. Evidencia: `reports/h2-leaksan/report.json` y `engine.log`.
- **ThreadSanitizer**: compila un segundo binario con `-fsanitize=thread` (nunca combinado con ASan) y recorre los ocho replays de PC Format. Evidencia: `reports/h2-threadsan/report.json` y `engine.log`. El runtime TSan puede no funcionar en determinados ejecutores CI Linux; un fallo de inicialización **no permite inferir que no haya carreras**.

**Criterio:** únicamente se puede afirmar `sin fugas detectadas` o `sin carreras detectadas` después de verificar los artefactos del sanitizador y la terminación de los replays. La ausencia de reportes no cubre rutas no ejecutadas, recursos todavía alcanzables por variables globales o la campaña CD32 privada.

**Estado CI al incorporar el diagnóstico:** los pasos son `continue-on-error: true` a propósito hasta comprobar que el runtime está disponible y las evidencias son interpretables; el resultado verde del workflow **no** representa su aprobación. La puerta ASan/UBSan anterior continúa siendo obligatoria.

## Comprobación ampliada (21-10-2026)

La ejecución Linux [39640639835](https://github.com/Cacheirez/openfodder/actions/runs/39640639835) sobre el código `93c8aae` pasó el informe JSON de LeakSanitizer con 29 fases, `returncode=0`, cero omisiones y ningún aviso de fuga en `engine.log`. ThreadSanitizer pasó 8/8 fases de PC Format con `returncode=0` y cero avisos de carrera; ASan/UBSan pasó 29/29 fases sin errores, y H3 mantuvo 11.361 muestras lógicas.

**Seguimiento histórico:** aquella revisión convirtió LeakSanitizer en paso **obligatorio** y amplió ThreadSanitizer a las 29 fases públicas, inicialmente como diagnóstico no bloqueante. El resultado final de esa ampliación está verificado más abajo. Ni LSan ni TSan acreditan seguridad de rutas no ejercitadas (audio real, CD32 privada, menús interactivos y Windows).

## Validación ampliada definitiva de las demos (21-10-2026)

Tras la ampliación de TSan, se inspeccionó el artefacto de [Linux 39641851896](https://github.com/Cacheirez/openfodder/actions/runs/39641851896) (código `82166539cc7dfdcc9c1e1f1995797b257d992e47` en el PR, checkout de merge temporal `a813e72`). El ZIP `OpenFodder-Linux-H3-evidence` tiene CRC válido. **Se revisaron los tres `report.json` y `engine.log`:**

| Detector | Fases | Omisiones | Código de salida | Avisos reportados |
|---|---:|---:|---:|---:|
| ASan + UBSan | 29/29 | 0 | 0 | 0 |
| LeakSanitizer | 29/29 | 0 | 0 | 0 |
| ThreadSanitizer | 29/29 | 0 | 0 | 0 |

Los tres informes registran `verdict: PASS`. También [Windows 39641852057](https://github.com/Cacheirez/openfodder/actions/runs/39641852057) supera compilación, 29 replays y las 11 fases de referencia H3 (11.361 muestras). El resultado limpio **solo cubre las rutas de prueba ejecutadas**; no cubre las 72 fases CD32 privadas, audio real ni todas las pantallas interactivas.

**Política de CI vigente:** ASan/UBSan y LeakSanitizer son obligatorios; **TSan aún declara `continue-on-error: true`**, aunque su informe 29/29 resulte PASS. Para aceptación H2.6 se recomienda eliminar ese carácter no bloqueante tras asegurar que el entorno TSan es estable. Ver también [inventario y matriz H2.5](H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md).
