# Estado operativo para continuar sin el chat

28-10-2026 · plan 2.53. Prioridad de lectura: este estado y el plan vivo prevalecen sobre pendientes de informes históricos. Comprobar siempre la rama y CI en GitHub al retomar.

## Referencias y objetivo

Repositorio `Cacheirez/openfodder`, rama `modernization/windows-foundation`, PR #1 abierto, borrador y sin fusionar. Base clásica intocable: `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`. Último motor probado: `e18b05bd46c35bf471863985e732b2b89f8513c7`; árbol `1a470115106c3c6d2c471385d022d52590674a05`. Revisiones documentales posteriores no son otro binario. HEAD cambia: leerlo del repositorio, no inferirlo de este documento.

Meta: modernizar Cannon Fodder 1, con CD32 como edición principal, presentación suave y arte nuevo, conservando reglas, RNG, tiempos, colisiones, campo visible y base clásica. Windows 11 de Miguel: 3840×2160, escala 300 %. Soportar 4:3/16:9 hasta UHD, sin estirar ni ampliar información táctica. No acelerar simulación para aumentar FPS. No regenerar H3 para ocultar divergencias. No publicar recursos comerciales ni partidas privadas.

## Avances que no hay que repetir

| Área | Implementado y evidencia | Pendiente real |
|---|---|---|
| Base H0–H3 | Windows jugable, correcciones RNC/UB/índices/hilos, 29 fases públicas; H3 original 11 fases/11.361 estados; aceptación H2.6 | Exclusión histórica RNC documentada, cobertura comercial completa |
| Presentación H4 | Capturas propias, núcleos de raster, terreno/HUD/cursor/paleta, capas ordenadas, registro y publicación opcional con contraste y fallback | Generalización semántica, transiciones completas, independencia global |
| Programación H4.6 | 0/1/5 de misión con H3; sonda pausa acotada PC/Amiga 301 estados y sanitizadores declarados | Pausas largas, eventos y demás transiciones; no equivale a interpolación |
| Soldado H4.2/H4.4 | Captura semántica mínima y sustitución de una pose original | Resto de estados, entidades y helicóptero compuesto |
| Arte H6 | C elegida; PNG transparente y manifiesto; piloto C01 hoja 7/frame 0, 16×14, fuente incorporada y fallback | HD real, densidad, animación, terrenos y cursor artístico |
| Pantalla H5.5/H5.9 | Transformación e inversa, DPI físico, bandas/clic sostenido, mapa, pausa, briefing/reclutamiento, ahora todas las rutas RenderAt/RenderShrunk y F11 FIT | Aceptación física del ajuste común; matriz completa, relativo/bloqueado y viewport moderno |
| Opciones H5.6 | CLASSIC/FIT, borrador, SAVE/KEEP/REVERT 15 s, restauración y persistencia comprobadas automáticamente | Aceptación manual; monitores/modos, interfaz independiente, sincronización/FPS |
| Suavidad H5 | Medición inicial del tiempo de proceso conservada | Interpolación de cámara/entidades, medidas por frame p95/p99, 60/120/144 Hz |

## Última validación y paquete

[Evidencia e18b05b](H5_9_VALIDACION_e18b05b.json): Windows 40760804335 y Linux 40760804513 PASS completos; siete CTest Windows, 29 fases públicas sin omisiones y regresiones/sanitizadores según pasos registrados. No implica cobertura GPU, audio físico, todos los finales ni toda CD32.

[Paquete Windows verificado](https://github.com/Cacheirez/openfodder/actions/runs/40760804335/artifacts/12849036551): 279 entradas; SHA-256 `15a756c7e39981f7b5dc2b31a1549b8f78c70f4738b7b8fd3342a7223da481d6`; ejecutable `4e0bd5de3d40823889bce0fd2ee9d88bbdaf9423d43fe881abb54dee487e532a`. VERSION `b87c5e1fa34668f8a03b21f83727377dc2b14530` es el merge temporal de CI, con árbol idéntico a e18b05b, no una fusión del PR. Incluye el arreglo Heroes/F11 común. Los ZIP anteriores no lo incluyen. Artefacto caducable el 27-11-2026; después reconstruir desde commit y workflows.

## Aceptaciones manuales y límites

| Observación de Miguel | Alcance registrado |
|---|---|
| «funciona perfectamente, no noto diferencias con respecto a Open Fodder original» | Piloto inicial de pantalla/ratón c8c54ab; no matriz exhaustiva |
| Bordes corregidos, puntos 4 y 5 aprobados | Cursor al cruzar límites laterales maximizado, UHD/300 %, incremento 1447abb |
| «el mapa se queda centrado, se cierra y vuelve a misión» | Arreglo 6e98fda; problema era maximizado, F11 ya funcionaba |
| «funciona la pausa perfectamente» | Incremento 63c4d6f |
| «solucionado el problema de las dos ventanas… al maximizar» | Briefing y reclutamiento de 551eaf7 |
| Heroes in Victory no se amplía | Arreglo e18b05b implementado y CI PASS; todavía sin aceptación visual |
| Opciones SAVE/KEEP/REVERT/persistencia | Todavía sin aceptación manual |

No extrapolar aceptaciones anteriores al paquete nuevo ni pedir repetir todo sin motivo. El asistente no dispone de escritorio Windows físico; CI Windows no es interacción humana.

## Próximo incremento, en orden

1. Registrar la respuesta de Miguel al paquete e18b05b. Con `PROBAR_ESCENAS_H5.cmd`, recorrer intro → reclutamiento → briefing → misión → pausa/mapa → servicio/Heroes → siguiente misión, alternando maximizar/F11. Ediciones/finales no visitados siguen pendientes.
2. Con `PROBAR_OPCIONES_H5.cmd`, comprobar CLASSIC/FIT, ratón alternativo desbloqueado, SAVE/KEEP, REVERT/caducidad y reinicio. Este lanzador limpia overrides; el de escenas los fuerza. Guardar FIT y reiniciar para solicitar alta densidad al crear la ventana.
3. Corregir incidencias concretas si aparecen. Linux de e18b05b ya está cerrado; no repetir su cierre como tarea pendiente.
4. Tras aceptación, comparar **8× frente a 12×** con C, misma pose/anclaje/fondo, vistas a 1080p/1440p/UHD y tamaños reales. [Cálculos](H6_DENSIDAD_EVALUACION.md). No producir animaciones ni prometer que ampliar el PNG activa HD: el compositor actual reduce a 16×14.

## Decisiones visuales y custodia

Miguel: «mi favorito es C, con diferencia»; le gusta el toque Nintendo. A descartada, B no elegida. La recomendación inicial B del asistente está superada. [Galería original A/B/C y B inicial](../../assets/modernization/concepts/README.md), con SHA-256. [Maestro C01](../../assets/modernization/soldier-c01/source.png), [metadatos](../../assets/modernization/soldier-c01/manifest.json) y [prompt](../../assets/modernization/soldier-c01/README.md). Se conservan píxeles originales, no nuevas recreaciones.

El cursor también se rediseñará: estados, hotspot, contraste, tamaño físico/DPI y fallback. No existen todavía sus bocetos ni fondos/atlas finales. No crear un juego de sprites por cada resolución: decidir densidad y derivar variantes conservando coordenadas lógicas.

## Protocolo de trabajo

Leer README/plan y documentos afectados completos; comprobar HEAD/PR/CI antes de editar. Preservar cambios ajenos y usar actualizaciones con comprobación del HEAD esperado. Mantener PR en borrador sin fusionar. No introducir hilos, actualizar dependencias o ampliar alcance sin necesidad. Ejecutar pruebas adecuadas al cambio y registrar límites; una revisión documental no necesita otra batería de motor.

Al cerrar cada mensaje, incluir exactamente estas etiquetas, con contenido concreto: **Hecho:**, **Situación del plan:** y **Próximos pasos:**. Mantener este estado, plan, evidencia y originales artísticos actualizados para que el siguiente hilo no dependa de memoria externa.
