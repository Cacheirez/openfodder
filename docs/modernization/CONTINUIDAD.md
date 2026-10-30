# Estado operativo para continuar sin el chat

**Estado vigente 30-10-2026 · plan 2.61:** `3d82ff2` tiene CI Windows/Linux/comparador completa PASS y [paquete verificado](https://github.com/Cacheirez/openfodder/actions/runs/41017089830/artifacts/12961100516). [Cierre y evidencia](VALIDACION_3d82ff2.md). [Costes HD medidos](H6_COSTE_HD_AISLADO.md): evitar integrar tal cual el escalado completo CPU; 12× sigue candidato de textura y 8× parametrizado. Save pendiente de aceptación física; HD aún aislado, densidad final abierta.

**Histórico 2.60 (superado por el cierre 2.61):** CI Windows d2e05e8 falló por falta de `<string>` en el generador HD (MSVC std::to_string). Include corregido; nueva CI/paquete pendientes. No usar d2e05e8 como paquete aprobado. [Evidencia](evidence/windows-d2e05e8-build-failure.json).

30-10-2026 · plan 2.61. Prioridad de lectura: este estado y el plan vivo prevalecen sobre pendientes de informes históricos. Comprobar siempre la rama y CI en GitHub al retomar.

## Referencias y objetivo

Repositorio `Cacheirez/openfodder`, rama `modernization/windows-foundation`, PR #1 abierto, borrador y sin fusionar. Base clásica intocable: `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`. Referencia anterior probada: `30ba0eccc752cf693b56f1f120842b51f3fd937e`, árbol `14edfa9575a0f1297e31058a75e868b4e8299e3a`. Incluye el arreglo del menú a1c8856 y el visor independiente. Windows, Linux y navegador completos PASS; [evidencia](VALIDACION_30ba0ec.json). HEAD cambia: leerlo del repositorio, no inferirlo de este documento.

Meta: modernizar Cannon Fodder 1, con CD32 como edición principal, presentación suave y arte nuevo, conservando reglas, RNG, tiempos, colisiones, campo visible y base clásica. Windows 11 de Miguel: 3840×2160, escala 300 %. Soportar 4:3/16:9 hasta UHD, sin estirar ni ampliar información táctica. No acelerar simulación para aumentar FPS. No regenerar H3 para ocultar divergencias. No publicar recursos comerciales ni partidas privadas.

## Avances que no hay que repetir

| Área | Implementado y evidencia | Pendiente real |
|---|---|---|
| Base H0–H3 | Windows jugable, correcciones RNC/UB/índices/hilos, 29 fases públicas; H3 original 11 fases/11.361 estados; aceptación H2.6 | Exclusión histórica RNC documentada, cobertura comercial completa |
| Presentación H4 | Capturas propias, núcleos de raster, terreno/HUD/cursor/paleta, capas ordenadas, registro y publicación opcional con contraste y fallback | Generalización semántica, transiciones completas, independencia global |
| Programación H4.6 | 0/1/5 de misión con H3; sonda pausa acotada PC/Amiga 301 estados y sanitizadores declarados | Pausas largas, eventos y demás transiciones; no equivale a interpolación |
| Soldado H4.2/H4.4 | Captura semántica mínima y sustitución de una pose original | Resto de estados, entidades y helicóptero compuesto |
| Arte H6 | C elegida; PNG transparente y manifiesto; piloto C01 hoja 7/frame 0, 16×14, fuente incorporada y fallback | HD real, densidad, animación, terrenos y cursor artístico |
| Pantalla H5.5/H5.9 | Transformación e inversa, DPI físico, bandas/clic sostenido, mapa, pausa, briefing/reclutamiento, ahora todas las rutas RenderAt/RenderShrunk y F11 FIT | Escenas aceptadas por Miguel («Probar escenas está ok»); matriz completa, relativo/bloqueado y viewport moderno pendientes |
| Opciones H5.6 | CLASSIC/FIT, borrador, SAVE/KEEP/REVERT 15 s, restauración y persistencia comprobadas automáticamente | Fallo manual de alternancia repetida corregido y publicado (2.54); CI/paquete aprobados en 30ba0ec; alternancia aceptada; nuevo cierre en Save reproducido/corregido; aceptación física pendiente y resto de H5.6 pendientes |
| Suavidad H5 | Medición inicial del tiempo de proceso conservada | Interpolación de cámara/entidades, medidas por frame p95/p99, 60/120/144 Hz |

## Validación anterior y paquete 30ba0ec (histórico)

[Evidencia 30ba0ec](VALIDACION_30ba0ec.json): Windows 40800994744, Linux 40800994727 y navegador 40800994726 PASS completos. Siete CTest Windows, incluida la pulsación única del menú, y 29 fases sin omisiones. Sanitizadores y regresiones según pasos registrados; no acredita cobertura universal.

[Paquete Windows corregido](https://github.com/Cacheirez/openfodder/actions/runs/40800994744/artifacts/12866468476): 279 entradas; SHA-256 `18fb4f30d54a62d9a6c10608401777f48ae4dc8144819ceaac9b3bd0ebb48aed`. VERSION `078aa7fed5b328d9a2b88a6683df3bae96e63237` es el merge temporal de CI, árbol idéntico a 30ba0ec, no fusión del PR. Incluye el arreglo de clics. El ZIP e18b05b anterior no lo incluye. Caduca el 28-11-2026; reconstruir desde commit/workflows si ya no existe.

[Visor 8×/12×](../../assets/modernization/density-review/README.md) y [artefacto con capturas](https://github.com/Cacheirez/openfodder/actions/runs/40800994726/artifacts/12865961333) verificados; HTML coincide byte a byte con Git, capturas DPR 1/3 inspeccionadas. El HTML autónomo está conservado permanentemente en Git. No es el render del motor.

## Aceptaciones manuales y límites

| Observación de Miguel | Alcance registrado |
|---|---|
| «funciona perfectamente, no noto diferencias con respecto a Open Fodder original» | Piloto inicial de pantalla/ratón c8c54ab; no matriz exhaustiva |
| Bordes corregidos, puntos 4 y 5 aprobados | Cursor al cruzar límites laterales maximizado, UHD/300 %, incremento 1447abb |
| «el mapa se queda centrado, se cierra y vuelve a misión» | Arreglo 6e98fda; problema era maximizado, F11 ya funcionaba |
| «funciona la pausa perfectamente» | Incremento 63c4d6f |
| «solucionado el problema de las dos ventanas… al maximizar» | Briefing y reclutamiento de 551eaf7 |
| «Probar escenas está ok» | Aceptación general del recorrido propuesto con e18b05b, incluido el arreglo común; no acredita finales/ediciones no visitados |
| Alternancia corregida, Save cierra antes de KEEP/REVERT | Confirmación manual 29-10; [fallo reproducido y corregido](H5_6_INCIDENCIA_SAVE.md) |
| Ambas densidades se ven bien, algo mejor la alta | Comparador revisado; preferencia por calidad condicionada a memoria/rendimiento, no decisión final |

No extrapolar aceptaciones anteriores al paquete nuevo ni pedir repetir todo sin motivo. El asistente no dispone de escritorio Windows físico; CI Windows no es interacción humana.

## Autorización de avance independiente (histórico anterior a 2.58)

Miguel pide continuar con puntos que no necesiten su validación, antes de revisar opciones. Se adelanta la preparación técnica 8×/12×: [visor autónomo y pruebas](../../assets/modernization/density-review/README.md). No bloquea ese trabajo la aceptación del menú; siguen pendientes la elección visual de densidad y la aceptación de opciones. El visor no modifica el render del juego. La CI final de navegador 40800994726 está aprobada, incluida la corrección de scroll/zoom. Windows anterior a1c8856 fue cancelado por una publicación posterior; Windows/Linux finales 30ba0ec están cerrados PASS. [Evidencia final](VALIDACION_30ba0ec.json).

## Incremento actual y siguiente paso

[Contrato/piloto HD aislado](H6_4_PILOTO_HD_AISLADO.md) implementado para 8×/12×. No está conectado a SDL: el juego sigue con C01 nativo. Conserva orden, destinos y anclaje; oclusiones/recortes no soportados vuelven al clásico. PNG y derivados reproducibles preservados. Pruebas locales y límites en el contrato.

Miguel confirma que ambas densidades se ven bien en las resoluciones y fondos revisados, algo mejor la alta; prefiere calidad si memoria/rendimiento lo permiten. No repetir A/B/C ni el comparador completo. Falta medir coste en el motor antes de cerrar densidad.

Miguel confirma alternancia correcta; **Save cerraba tras cambiar opciones, antes de mostrar KEEP/REVERT**. [Causa reproducida y corregida](H5_6_INCIDENCIA_SAVE.md): el signo `?` solicita frame 54 en fuente de 37; acceso nulo en dibujo. Se elimina el glifo incompatible y se añade fixture de texto real PC/Amiga, que falla antes y pasa después. Falta aceptación física. Registro H5_OPCIONES.log conservado para diagnosticar si hubiera otro fallo. No usar el paquete anterior para obtener marcas que aún no contenía.

Próximo trabajo: validar en Windows Save con el paquete 3d82ff2; preparar una composición HD eficiente y opcional a partir de los costes medidos, antes de fijar densidad. Mantener clásico por defecto. No producir animaciones ni introducir hilos. Escenas ya aceptadas: no pedir repetirlas.

## Validaciones pendientes de Miguel

1. Cuando haya paquete propio verificado, reproducir solo Save con el lanzador y conservar el log si cierra; indicar opciones cambiadas.
2. Con el paquete corregido, completar KEEP/REVERT, caducidad 15 s y persistencia.
3. Densidad final condicionada a coste medido; revisión del comparador ya recibida. Integración HD y cursor aún pendientes de prueba visual específica.

## Decisiones visuales y custodia

Miguel: «mi favorito es C, con diferencia»; le gusta el toque Nintendo. A descartada, B no elegida. La recomendación inicial B del asistente está superada. [Galería original A/B/C y B inicial](../../assets/modernization/concepts/README.md), con SHA-256. [Maestro C01](../../assets/modernization/soldier-c01/source.png), [metadatos](../../assets/modernization/soldier-c01/manifest.json) y [prompt](../../assets/modernization/soldier-c01/README.md). Se conservan píxeles originales, no nuevas recreaciones.

El cursor también se rediseñará: estados, hotspot, contraste, tamaño físico/DPI y fallback. No existen todavía sus bocetos ni fondos/atlas finales. No crear un juego de sprites por cada resolución: decidir densidad y derivar variantes conservando coordenadas lógicas.

## Protocolo de trabajo

Leer README/plan y documentos afectados completos; comprobar HEAD/PR/CI antes de editar. Preservar cambios ajenos y usar actualizaciones con comprobación del HEAD esperado. Mantener PR en borrador sin fusionar. No introducir hilos, actualizar dependencias o ampliar alcance sin necesidad. Ejecutar pruebas adecuadas al cambio y registrar límites; una revisión documental no necesita otra batería de motor.

Al cerrar cada mensaje, incluir exactamente estas etiquetas, con contenido concreto: **Hecho:**, **Situación del plan:** y **Próximos pasos:**. Mantener este estado, plan, evidencia y originales artísticos actualizados para que el siguiente hilo no dependa de memoria externa.
