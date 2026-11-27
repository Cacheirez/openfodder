# H2.6 — Revisión de aceptación de la base clásica

Fecha: 22 de octubre de 2026 (Europe/Madrid).

## Decisión actual

**H2.6 CERRADO: base clásica aceptada en el alcance documentado.** Miguel valida expresamente el motor con los archivos originales CD32. La nueva batería CI Windows/Linux ha terminado satisfactoriamente y se han inspeccionado sus informes internos. Se permite iniciar H4.1; el PR #1 permanece en borrador, sin fusionar. No se declara cobertura automática completa de CD32.

## Referencias comprobadas

- HEAD al retomar: `df99c6781d1dbfac12375f8577796463919ffe23`, PR #1 abierto en borrador. Este HEAD documental no tiene ejecuciones propias.
- Código estabilizado: `93c8aae6c79120071982c39380c517f2ae3142e7`.
- CI de referencia: `82166539cc7dfdcc9c1e1f1995797b257d992e47`; Linux [39641851896](https://github.com/Cacheirez/openfodder/actions/runs/39641851896) y Windows [39641852057](https://github.com/Cacheirez/openfodder/actions/runs/39641852057), ambos completados con éxito, reconfirmados mediante API.
- Los pasos individuales Linux de ASan/UBSan, LSan, TSan y comparación H3 figuran satisfactorios. Los informes internos 29/29 sin hallazgos fueron inspeccionados en la sesión anterior, según H2.5; no se presentan como una nueva inspección de esos ZIP.
- Referencias Run, Scripts, grabaciones y H3: se conservan las de [H2.5](H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md), sin rebaselinar.

## Cambio de infraestructura (registro previo a la ejecución)

Commit `5c564b1943e30a2504452e8ad51832a687b8988a`:

1. Linux fija SDL3_mixer a `3045b35335113e5e5ba258858cb403d8803bfbeb`, la revisión ya usada por Windows. Es un cambio respecto al mixer Linux 3.3.0 observado anteriormente: su compatibilidad Linux queda pendiente de CI.
2. El checkout verifica el SHA esperado y conserva los SHA efectivos SDL3/mixer en el artefacto de evidencias.
3. ThreadSanitizer deja de permitir fallos; su código de salida y la auditoría de replays bloquean el workflow.
4. El ejecutor se fija a `ubuntu-24.04`. Esto no congela paquetes apt ni la imagen exacta; no se promete reproducibilidad binaria absoluta.
5. Se mantienen backends XMP y FFmpeg por plataforma. No se atribuye equivalencia acústica a la igualdad del SHA de mixer.

Comprobación local: YAML parseado, pasos sin `continue-on-error`, `git diff --check` limpio y 13 pruebas Python existentes satisfactorias. No se ha recompilado aquí el motor completo con la nueva dependencia.

## Verificación privada CD32

ZIP aportado en este hilo: CRC correcto, 276 archivos; 72 MAP y 72 SPT. Original intacto; copia y manifiesto SHA-256 por archivo fuera del repositorio.

Sobre el lector real `dernc_bounded.cpp`, con el harness existente `test_rnc_bounded.cpp`, compilado localmente con GCC, ASan y UBSan:

- 41 recursos RNC-1 válidos descomprimidos.
- 488 variantes inválidas rechazadas.
- Retorno 0, stderr vacío; UBSan configurado para detenerse en el primer hallazgo.
- LeakSanitizer desactivado en esta prueba aislada; no se presenta como prueba de fugas.
- No se ejecutaron las 72 fases ni el motor completo. Esta evidencia valida el lector y esos recursos, no toda la campaña ni equivalencia gráfica.

Ningún archivo comercial, manifiesto privado ni binario se incorpora a GitHub.

## Evidencia manual y riesgo histórico

Miguel comunica pruebas satisfactorias de las mejoras que denomina «H6», también usando la carpeta FODDER CD32, y en esta sesión confirma explícitamente que H2.6 queda validada por su parte con el motor y los archivos originales CD32. Se conserva ese resultado sin exigir repetirlo. No se dispone del VERSION.txt de esa prueba concreta: no se atribuye a un commit exacto. El H6 formal de arte/atlas del plan sigue pendiente.

La búsqueda de llamadas en Source encuentra la ruta de carga en Resources.cpp usando `rnc_unpack_bounded`. Las funciones heredadas `rnc_unpack` y `rnc_ulen` permanecen declaradas/definidas, sin llamadas encontradas en Source. La atribución del recurso mínimo del fallo histórico H2.1 permanece abierta; no se confunde con un fallo reproducido de la ruta actual.

## Condiciones previas para cerrar (resueltas por la decisión siguiente)

- Confirmar compilación y regresiones del commit de infraestructura: 29 fases, H3 original y sanitizadores obligatorios; inspeccionar informes, no solo el indicador verde.
- Mantener como exclusiones expresas: 72 fases CD32 sin replays, interacción/ventana/audio físico sin instrumentación completa, versión exacta de la prueba manual no atribuida y caso mínimo histórico H2.1.
- Si se cumplen las puertas, emitir decisión de aceptación limitada para iniciar H4 conservando esta referencia recuperable. El PR seguirá en borrador.

## Cierre técnico verificado el 22-10-2026

Commit probado: `5c564b1943e30a2504452e8ad51832a687b8988a`.
Referencia conservada: [baseline/classic-h2.6-2026-10-22](https://github.com/Cacheirez/openfodder/tree/baseline/classic-h2.6-2026-10-22) → `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`. Solo añade documentación al commit probado, sin modificar motor, workflows, datos ni huellas. Esta rama se reserva como punto de retorno y no recibirá H4.

| Comprobación | Resultado verificado |
|---|---|
| [Windows 39735380194](https://github.com/Cacheirez/openfodder/actions/runs/39735380194) | Job completo SUCCESS; 6 CTests PASS, 29 fases, 0 omisiones, retorno 0 |
| H3 Windows | Dos pasadas por campaña: 7.956 + 3.405 estados; 11.361 coinciden con baseline canónico original |
| [Linux 39735380183](https://github.com/Cacheirez/openfodder/actions/runs/39735380183) | Job completo SUCCESS con TSan obligatorio |
| H3 Linux | 7.956 + 3.405 estados; 11.361 coinciden con baseline original, sin rebaselinar |
| ASan/UBSan, LSan, TSan Linux | Cada informe: PASS, 29 fases, 0 omisiones, retorno 0, reasons vacío; logs sin los diagnósticos de sanitizador buscados |
| RNC público Linux | 88 recursos válidos y 1.047 variantes inválidas, PASS |
| Dependencias efectivas del artefacto Linux | SDL3 `a962f40bbba175e9716557a25d5d7965f134a3d3`; mixer `3045b35335113e5e5ba258858cb403d8803bfbeb` |
| Datos privados CD32 | Prueba aislada de lector descrita arriba: 41 recursos y 488 rechazos, sin hallazgos |
| Prueba manual | Aceptación explícita de Miguel con datos originales CD32; no se exige repetición |

Se descargaron y comprobaron CRC, report.json y engine.log de los ZIP de evidencias, además de los logs de jobs. Integridad SHA-256:

- Linux, artefacto `12407815405`: `544012cb178959643ddf43688c709f7619ede404cb017d0ec607b0899131b2fa`.
- Windows, artefacto `12406842071`: `eb52d8433c34532f4583d198326b2495789738bb4911ea20db9c73126a6a540d`.
- Paquete jugable Windows, artefacto `12406489083`: digest publicado por GitHub `ea2147a56166d6f28635a439e20e36fd046165740f1e806de57e082d275a0f3a` (no se ha vuelto a inspeccionar su contenido en este cierre).

Las evidencias Actions caducan según su retención. La rama permite recuperar código, configuración y referencias; no se promete retención permanente del ejecutable ni compilación bit a bit idéntica con futuros paquetes apt/ejecutores.

### Decisión y exclusiones aceptadas

Se acepta esta base **para continuar el desarrollo H4**, conservando modo clásico y referencia H3. No es aceptación de un producto final HD ni certificación de ausencia universal de defectos.

H2.1 permanece como atribución histórica del caso mínimo sin resolver; se acepta como deuda documental delimitada porque la carga actual usa el lector acotado, se han validado fixtures públicos y privados y no hay un fallo reproducible pendiente en la cobertura ejecutada. No se marca falsamente H2.1 como resuelto.

Permanecen excluidos de la garantía: replay/equivalencia de las 72 fases CD32, instrumentación de audio físico y todas las pantallas/transiciones, equivalencia acústica entre backends y atribución exacta del ejecutable probado manualmente. Las revisiones de callbacks y presentación corresponden a H4, no a una afirmación de cobertura TSan total.

### Siguiente trabajo autorizado

[H4.1 — efectos del dibujo](H4_1_EFECTOS_DIBUJO.md): inventario inicial realizado; extracción/preservación de efectos y regresión pendientes. Se mantienen las frecuencias heredadas, incluyendo la actualización lógica de interrupción, y las huellas H3 originales.
