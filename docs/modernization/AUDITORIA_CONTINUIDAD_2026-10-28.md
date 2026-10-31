# Auditoría de continuidad — 28-10-2026

## Resultado y alcance

El relevo operativo puede continuar desde la rama de GitHub y [un prompt](PROMPT_NUEVO_HILO.md), sin recuperar este chat. Están guardados código/historia, plan, decisiones, pruebas, evidencia compacta, prompts, cuatro láminas originales y fuente C01. **No se afirma que todos los ZIP, logs, trazas antiguas o recursos comerciales estén archivados en GitHub.** Esas exclusiones no impiden continuar el desarrollo público y reconstruirlo; sí impiden recuperar exactamente toda evidencia binaria histórica sin fuentes adicionales.

Estado remoto comprobado al iniciar: HEAD `14bcd6fd58272996edc7ce240f1838b897f7f1b7`, PR #1 abierto/borrador/no fusionado. Motor e18b05b, Windows/Linux aprobados y paquete verificado según [evidencia](H5_9_VALIDACION_e18b05b.json). Este incremento solo cambia documentación y custodia de conceptos; no modifica Source, herramientas, workflows, datos, dependencias ni referencias H3.

## Lagunas encontradas y resolución

| Hallazgo | Corrección |
|---|---|
| README de relevo seguía en 2.37 y apuntaba a un motor/paquete antiguos | Índice renovado, último motor/CI/paquete, orden de lectura y CONTINUIDAD.md |
| Tabla central del plan aún citaba 46c180be y arte/opciones pendientes sin reconocer pilotos | Plan 2.53 actualiza estado real H5/H6 y distingue hito parcial de tarea no iniciada |
| Bitácora y siguientes pasos antiguos se podían leer como instrucciones actuales | Precedencia explícita: CONTINUIDAD y tarea activa; informes fechados conservados como historia |
| Documento B aún pedía elegir estilo | Elección C consolidada; B no elegida, A descartada; no repetir decisión |
| A/B/C estaban descritos y tenían prompts pero no PNG en Git | Cuatro originales recuperados, inspeccionados y archivados sin recodificación, manifiesto y galería |
| C01 ya estaba en Git, pero faltaba acceso visual sencillo y una comprobación de custodia | SHA-256 contrastado con manifiesto y copia original recuperada; enlaces desde galería/relevo |
| Resoluciones/transformaciones seguían describiendo solo el punto de partida | Separado alcance inicial del FIT común implementado y sus límites |
| Guía Windows arrancaba con el ZIP del piloto antiguo | Encabezado vigente con paquete e18b05b y lanzadores adecuados |
| No había un prompt autónomo vigente dentro del repositorio | PROMPT_NUEVO_HILO.md, con rama, lectura obligatoria, invariantes, pendientes y resumen final obligatorio |

## Desarrollo documentado y dónde recuperarlo

Los informes H2–H4 conservan contratos, fallos históricos, soluciones y suites; el plan conserva bitácora y tareas H0–H10. No se ha reescrito un fallo antiguo como si nunca hubiera ocurrido.

| Incremento | Evidencia/documentación |
|---|---|
| Estabilización y referencia clásica | H2_6_ACEPTACION_BASE_CLASICA.md, H2_* y H3_* |
| Raster, recursos, capas y publicación | H4_1_* y H4_3_PUBLICACION_ORDENES.md; evidence/ |
| 0/1/5, pausa y medición inicial | H4_6_PLANIFICACION_MISION.md, H4_6_PAUSA_MOTOR.md, H5_1_MEDICION_INICIAL.md |
| Soldado semántico y sustitución original | H4_2_SOLDADO_SEMANTICO.md, H4_4_POSE_INDIVIDUAL.md |
| Elección C y primera pose transparente | H6_1_*, H6_3_POSE_C01.md, assets/modernization/ |
| Ratón y multirresolución inicial | H5_5_*, H5_9_AJUSTE_VENTANAS.md, TRANSFORMACIONES_PANTALLA.md |
| Bordes, mapa y pausa | H5_9_INCIDENCIA_BORDES_300.md, H5_9_MAPA_GENERAL_Y_ACEPTACION_BORDES.md, H5_9_PAUSA_AJUSTADA.md y sus JSON |
| Opciones y briefing/reclutamiento | H5_6_OPCIONES_PRESENTACION.md, H5_6_VALIDACION_551eaf7.json |
| Heroes y política común ventana/F11 | H5_9_INVENTARIO_ESCENAS.md, H5_9_VALIDACION_e18b05b.json |
| Densidad, cursor y próximos pasos | H6_DENSIDAD_EVALUACION.md, PLAN_TRABAJO.md H6/H7, CONTINUIDAD.md |

## Custodia visual

[Galería completa](../../assets/modernization/concepts/README.md): B00 inicial, B01 refinada, A01 píxel, C01 pintada. PNG 1536×1024 originales; SHA-256 y procedencia en manifest.json. [Fuente transparente C01](../../assets/modernization/soldier-c01/source.png) 1353×1162, SHA-256 `9fb5dd519e8589de6c6420e4385c8eb2e12ac1f24c83f9a64678a2d943e31c77`; su manifiesto conserva límites alfa, caja 16×14 y anclajes. El header Source/Utils/SoldierArtPixels.hpp y generador tools/modernization/build_soldier_art.cpp ya están versionados. La fuente recuperada coincide byte a byte con la guardada previamente.

Todavía **no existen** atlas completos, animaciones nuevas, tiles finales, diseño artístico del cursor ni muestras controladas 8×/12×. No confundir una lámina de jungla con terreno integrado. Los prompts documentan la generación; no garantizan reproducir sus píxeles. Por eso se archivan los originales.

## Comprobaciones de esta auditoría

- Inventario de todos los Markdown de modernización y JSON de evidencia; clasificación siguiente. Revisión de estado operativo frente a código/documentos y commits recientes, sin ejecutar otra batería de motor por cambios documentales.
- Destinos de enlaces Markdown relativos comprobados; los enlaces remotos de motor/PR/CI/paquete se verificaron en la sesión de cierre. No se afirma haber abierto cada URL histórica externa.
- JSON legibles, SHA-256/tamaño/dimensiones de los cuatro conceptos y fuente C01 comprobados. Ningún gráfico se recodifica ni se altera.
- `git diff --check`; alcance del diff limitado a README, docs y assets conceptuales. Source, herramientas y referencias H3 sin modificaciones.

## Límites que debe conocer el siguiente hilo

Los artefactos Windows de e18b05b caducan el 27-11-2026. Los JSON en Git conservan resultados e identificadores, no logs/trazas/ZIP completos. Si el enlace caduca, repetir el workflow sobre el commit exacto y registrar la nueva procedencia; no afirmar hashes idénticos de un binario recompilado. Los workflows y submódulos fijan fuentes/datos públicos y las herramientas; los runners/paquetes del sistema no están congelados bit a bit.

Los recursos comerciales CD32 y partidas privadas no se publican. Demos y grabaciones públicas fijadas permiten retomar; pruebas comerciales necesitarán los datos de Miguel cuando corresponda. No hay validación física nueva de Heroes/opciones; no convertir esta auditoría en aceptación manual. La edición o resultado de una misión puede impedir ver una escena: registrarla como no visitada.

## Índice completo de documentos

“Histórico/contrato” conserva detalles técnicos y resultados de su revisión; para su estado actual prevalecen CONTINUIDAD y plan. Los JSON son evidencia fechada, no listas de tareas actuales. Este índice cubre todos los Markdown y JSON de docs/modernization en esta auditoría.

| Documento | Función |
|---|---|
| [AUDITORIA_CONTINUIDAD_2026-10-28.md](AUDITORIA_CONTINUIDAD_2026-10-28.md) | Auditoría fechada |
| [CD32_CAPACIDADES_VEHICULOS.md](CD32_CAPACIDADES_VEHICULOS.md) | Histórico/contrato; ver estado vigente |
| [CD32_CENSO_SPRITES.md](CD32_CENSO_SPRITES.md) | Histórico/contrato; ver estado vigente |
| [CONTINUIDAD.md](CONTINUIDAD.md) | Estado/guía vigente |
| [DIFERENCIAS_PC_AMIGA.md](DIFERENCIAS_PC_AMIGA.md) | Histórico/contrato; ver estado vigente |
| [H2_3_CORRECCION_DIRECCIONES_2026-10-21.md](H2_3_CORRECCION_DIRECCIONES_2026-10-21.md) | Histórico/contrato; ver estado vigente |
| [H2_3_DIAGNOSTICO_ASAN_2026-10-21.md](H2_3_DIAGNOSTICO_ASAN_2026-10-21.md) | Histórico/contrato; ver estado vigente |
| [H2_3_INDICES_SPRITES_HUFFMAN_2026-10-21.md](H2_3_INDICES_SPRITES_HUFFMAN_2026-10-21.md) | Histórico/contrato; ver estado vigente |
| [H2_3_PROTECCION_FOTOGRAMAS_2026-10-21.md](H2_3_PROTECCION_FOTOGRAMAS_2026-10-21.md) | Histórico/contrato; ver estado vigente |
| [H2_3_UBSAN_CLEAN_2026-10-21.md](H2_3_UBSAN_CLEAN_2026-10-21.md) | Histórico/contrato; ver estado vigente |
| [H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md](H2_5_REFERENCIAS_DEPENDENCIAS_COBERTURA.md) | Histórico/contrato; ver estado vigente |
| [H2_6_ACEPTACION_BASE_CLASICA.md](H2_6_ACEPTACION_BASE_CLASICA.md) | Histórico/contrato; ver estado vigente |
| [H2_ESTABILIZACION_2026-10-21.md](H2_ESTABILIZACION_2026-10-21.md) | Histórico/contrato; ver estado vigente |
| [H2_H3_AVANCE.md](H2_H3_AVANCE.md) | Histórico/contrato; ver estado vigente |
| [H2_LEAK_THREAD_DIAGNOSTICOS.md](H2_LEAK_THREAD_DIAGNOSTICOS.md) | Histórico/contrato; ver estado vigente |
| [H3_6_CONTRATO_VISIBILIDAD.md](H3_6_CONTRATO_VISIBILIDAD.md) | Histórico/contrato; ver estado vigente |
| [H3_VALIDACION_2026-10-21.md](H3_VALIDACION_2026-10-21.md) | Histórico/contrato; ver estado vigente |
| [H4_1_CAPAS_DESTINOS_INDEXADOS.md](H4_1_CAPAS_DESTINOS_INDEXADOS.md) | Histórico/contrato; ver estado vigente |
| [H4_1_CAPAS_MISION.md](H4_1_CAPAS_MISION.md) | Histórico/contrato; ver estado vigente |
| [H4_1_DESTINOS_PRESENTACION.md](H4_1_DESTINOS_PRESENTACION.md) | Histórico/contrato; ver estado vigente |
| [H4_1_EFECTOS_DIBUJO.md](H4_1_EFECTOS_DIBUJO.md) | Histórico/contrato; ver estado vigente |
| [H4_1_ESTADO_PAUSA.md](H4_1_ESTADO_PAUSA.md) | Histórico/contrato; ver estado vigente |
| [H4_1_FRAME_MISION.md](H4_1_FRAME_MISION.md) | Histórico/contrato; ver estado vigente |
| [H4_1_HUD_CURSOR_ESTABLES.md](H4_1_HUD_CURSOR_ESTABLES.md) | Histórico/contrato; ver estado vigente |
| [H4_1_PALETA_DESTINOS.md](H4_1_PALETA_DESTINOS.md) | Histórico/contrato; ver estado vigente |
| [H4_1_PRODUCTORES_GUI_ESCENAS.md](H4_1_PRODUCTORES_GUI_ESCENAS.md) | Histórico/contrato; ver estado vigente |
| [H4_1_RECURSOS_ESTABLES.md](H4_1_RECURSOS_ESTABLES.md) | Histórico/contrato; ver estado vigente |
| [H4_1_REGISTRO_PRODUCTORES.md](H4_1_REGISTRO_PRODUCTORES.md) | Histórico/contrato; ver estado vigente |
| [H4_1_RUTAS_Y_RECURSOS.md](H4_1_RUTAS_Y_RECURSOS.md) | Histórico/contrato; ver estado vigente |
| [H4_1_TERRENO_ESTABLE.md](H4_1_TERRENO_ESTABLE.md) | Histórico/contrato; ver estado vigente |
| [H4_2_SOLDADO_SEMANTICO.md](H4_2_SOLDADO_SEMANTICO.md) | Histórico/contrato; ver estado vigente |
| [H4_3_PUBLICACION_ORDENES.md](H4_3_PUBLICACION_ORDENES.md) | Histórico/contrato; ver estado vigente |
| [H4_4_POSE_INDIVIDUAL.md](H4_4_POSE_INDIVIDUAL.md) | Histórico/contrato; ver estado vigente |
| [H4_4_VALIDACION_46c180be.json](H4_4_VALIDACION_46c180be.json) | Evidencia fechada |
| [H4_6_PAUSA_MOTOR.md](H4_6_PAUSA_MOTOR.md) | Histórico/contrato; ver estado vigente |
| [H4_6_PLANIFICACION_MISION.md](H4_6_PLANIFICACION_MISION.md) | Histórico/contrato; ver estado vigente |
| [H5_1_MEDICION_INICIAL.md](H5_1_MEDICION_INICIAL.md) | Histórico/contrato; ver estado vigente |
| [H5_5_ACEPTACION_MANUAL_WINDOWS.md](H5_5_ACEPTACION_MANUAL_WINDOWS.md) | Histórico/contrato; ver estado vigente |
| [H5_5_CIERRE_CI_c8c54ab.json](H5_5_CIERRE_CI_c8c54ab.json) | Evidencia fechada |
| [H5_5_CI_fb4a997.json](H5_5_CI_fb4a997.json) | Evidencia fechada |
| [H5_5_TRANSFORMACION_MISION.md](H5_5_TRANSFORMACION_MISION.md) | Histórico/contrato; ver estado vigente |
| [H5_5_VALIDACION_4e8e211.json](H5_5_VALIDACION_4e8e211.json) | Evidencia fechada |
| [H5_6_OPCIONES_PRESENTACION.md](H5_6_OPCIONES_PRESENTACION.md) | Estado/guía vigente |
| [H5_6_VALIDACION_551eaf7.json](H5_6_VALIDACION_551eaf7.json) | Evidencia fechada |
| [H5_9_AJUSTE_VENTANAS.md](H5_9_AJUSTE_VENTANAS.md) | Histórico/contrato; ver estado vigente |
| [H5_9_CIERRE_CI_45de47a4.json](H5_9_CIERRE_CI_45de47a4.json) | Evidencia fechada |
| [H5_9_INCIDENCIA_BORDES_300.md](H5_9_INCIDENCIA_BORDES_300.md) | Histórico/contrato; ver estado vigente |
| [H5_9_INVENTARIO_ESCENAS.md](H5_9_INVENTARIO_ESCENAS.md) | Estado/guía vigente |
| [H5_9_MAPA_GENERAL_Y_ACEPTACION_BORDES.md](H5_9_MAPA_GENERAL_Y_ACEPTACION_BORDES.md) | Histórico/contrato; ver estado vigente |
| [H5_9_PAUSA_AJUSTADA.md](H5_9_PAUSA_AJUSTADA.md) | Histórico/contrato; ver estado vigente |
| [H5_9_VALIDACION_1447abb.json](H5_9_VALIDACION_1447abb.json) | Evidencia fechada |
| [H5_9_VALIDACION_63c4d6f.json](H5_9_VALIDACION_63c4d6f.json) | Evidencia fechada |
| [H5_9_VALIDACION_6e98fda.json](H5_9_VALIDACION_6e98fda.json) | Evidencia fechada |
| [H5_9_VALIDACION_e18b05b.json](H5_9_VALIDACION_e18b05b.json) | Evidencia fechada |
| [H6_1_COMPARATIVA_ABC.md](H6_1_COMPARATIVA_ABC.md) | Histórico/contrato; ver estado vigente |
| [H6_1_MUESTRA_B01.md](H6_1_MUESTRA_B01.md) | Histórico/contrato; ver estado vigente |
| [H6_3_CI_1bcf69c.json](H6_3_CI_1bcf69c.json) | Evidencia fechada |
| [H6_3_POSE_C01.md](H6_3_POSE_C01.md) | Estado/guía vigente |
| [H6_DENSIDAD_EVALUACION.md](H6_DENSIDAD_EVALUACION.md) | Estado/guía vigente |
| [H6_PILOTO_VISUAL.md](H6_PILOTO_VISUAL.md) | Histórico/contrato; ver estado vigente |
| [PLAN_MODERNIZACION_ES.md](PLAN_MODERNIZACION_ES.md) | Histórico/contrato; ver estado vigente |
| [PLAN_TRABAJO.md](PLAN_TRABAJO.md) | Estado/guía vigente |
| [PLAN_TRABAJO_HISTORICO_HASTA_2_19.md](PLAN_TRABAJO_HISTORICO_HASTA_2_19.md) | Histórico/contrato; ver estado vigente |
| [PRIMER_ARRANQUE_WINDOWS.md](PRIMER_ARRANQUE_WINDOWS.md) | Histórico/contrato; ver estado vigente |
| [PROMPT_NUEVO_HILO.md](PROMPT_NUEVO_HILO.md) | Estado/guía vigente |
| [README.md](README.md) | Estado/guía vigente |
| [RESOLUCIONES_PC_HASTA_4K.md](RESOLUCIONES_PC_HASTA_4K.md) | Estado/guía vigente |
| [RESULTADOS.md](RESULTADOS.md) | Histórico/contrato; ver estado vigente |
| [TRANSFORMACIONES_PANTALLA.md](TRANSFORMACIONES_PANTALLA.md) | Histórico/contrato; ver estado vigente |
| [VALIDAR_RATON_WINDOWS_H5.md](VALIDAR_RATON_WINDOWS_H5.md) | Estado/guía vigente |
| [evidence/049439d-reports.json](evidence/049439d-reports.json) | Evidencia fechada |
| [evidence/1e1f93d3-reports.json](evidence/1e1f93d3-reports.json) | Evidencia fechada |
| [evidence/40d67a0-reports.json](evidence/40d67a0-reports.json) | Evidencia fechada |
| [evidence/793e347-reports.json](evidence/793e347-reports.json) | Evidencia fechada |
| [evidence/7eeb6f7-reports.json](evidence/7eeb6f7-reports.json) | Evidencia fechada |
| [evidence/9aaaf448-ci-summary.json](evidence/9aaaf448-ci-summary.json) | Evidencia fechada |
| [evidence/a133afb-reports.json](evidence/a133afb-reports.json) | Evidencia fechada |
| [evidence/acfc099a-reports.json](evidence/acfc099a-reports.json) | Evidencia fechada |
| [evidence/b34373b0-archive.json](evidence/b34373b0-archive.json) | Evidencia fechada |
| [evidence/b34373b0-reports.json](evidence/b34373b0-reports.json) | Evidencia fechada |
| [evidence/ba2ef207-reports.json](evidence/ba2ef207-reports.json) | Evidencia fechada |
| [evidence/bd2b3d2-reports.json](evidence/bd2b3d2-reports.json) | Evidencia fechada |
| [evidence/c6af094-reports.json](evidence/c6af094-reports.json) | Evidencia fechada |
| [evidence/cd32-sprite-census.json](evidence/cd32-sprite-census.json) | Evidencia fechada |
| [evidence/cd32-vehicle-capabilities.json](evidence/cd32-vehicle-capabilities.json) | Evidencia fechada |
| [evidence/cost-local-rejected-2026-10-26.json](evidence/cost-local-rejected-2026-10-26.json) | Evidencia fechada |
| [evidence/cost-pilot-2026-10-26.json](evidence/cost-pilot-2026-10-26.json) | Evidencia fechada |
| [evidence/d35e267-reports.json](evidence/d35e267-reports.json) | Evidencia fechada |
| [evidence/destination-local-2026-10-24.json](evidence/destination-local-2026-10-24.json) | Evidencia fechada |
| [evidence/ff15219-reports.json](evidence/ff15219-reports.json) | Evidencia fechada |
| [evidence/mission-local-2026-10-24.json](evidence/mission-local-2026-10-24.json) | Evidencia fechada |
| [evidence/pause-probe-local-2026-10-26.json](evidence/pause-probe-local-2026-10-26.json) | Evidencia fechada |
