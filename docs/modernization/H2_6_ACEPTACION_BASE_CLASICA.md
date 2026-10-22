# H2.6 — Revisión de aceptación de la base clásica

Fecha: 22 de octubre de 2026 (Europe/Madrid).

## Decisión actual

**Aceptación pendiente de la nueva batería CI.** Se conserva la base clásica candidata; no se inicia H4, no se fusiona el PR #1 y no se declara cobertura completa de CD32.

## Referencias comprobadas

- HEAD al retomar: `df99c6781d1dbfac12375f8577796463919ffe23`, PR #1 abierto en borrador. Este HEAD documental no tiene ejecuciones propias.
- Código estabilizado: `93c8aae6c79120071982c39380c517f2ae3142e7`.
- CI de referencia: `82166539cc7dfdcc9c1e1f1995797b257d992e47`; Linux [39641851896](https://github.com/Cacheirez/openfodder/actions/runs/39641851896) y Windows [39641852057](https://github.com/Cacheirez/openfodder/actions/runs/39641852057), ambos completados con éxito, reconfirmados mediante API.
- Los pasos individuales Linux de ASan/UBSan, LSan, TSan y comparación H3 figuran satisfactorios. Los informes internos 29/29 sin hallazgos fueron inspeccionados en la sesión anterior, según H2.5; no se presentan como una nueva inspección de esos ZIP.
- Referencias Run, Scripts, grabaciones y H3: se conservan las de [H2.5](H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md), sin rebaselinar.

## Cambio de infraestructura

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

Miguel comunica pruebas satisfactorias de las mejoras que denomina «H6», también usando la carpeta FODDER CD32. Se conserva ese resultado sin exigir repetirlo. No se dispone del VERSION.txt de esa prueba concreta: no se atribuye a un commit exacto. El H6 formal de arte/atlas del plan sigue pendiente.

La búsqueda de llamadas en Source encuentra la ruta de carga en Resources.cpp usando `rnc_unpack_bounded`. Las funciones heredadas `rnc_unpack` y `rnc_ulen` permanecen declaradas/definidas, sin llamadas encontradas en Source. La atribución del recurso mínimo del fallo histórico H2.1 permanece abierta; no se confunde con un fallo reproducido de la ruta actual.

## Condiciones para cerrar

- Confirmar compilación y regresiones del commit de infraestructura: 29 fases, H3 original y sanitizadores obligatorios; inspeccionar informes, no solo el indicador verde.
- Mantener como exclusiones expresas: 72 fases CD32 sin replays, interacción/ventana/audio físico sin instrumentación completa, versión exacta de la prueba manual no atribuida y caso mínimo histórico H2.1.
- Si se cumplen las puertas, emitir decisión de aceptación limitada para iniciar H4 conservando esta referencia recuperable. El PR seguirá en borrador.
