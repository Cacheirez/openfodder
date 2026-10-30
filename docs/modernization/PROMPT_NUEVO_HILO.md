# Prompt para continuar en otro hilo

**Estado vigente 30-10-2026 · plan 2.62:** Miguel acepta guardado y persistencia de opciones. [Composición HD eficiente por capas](H6_COMPOSICION_HD_POR_CAPAS.md) implementada y verificada localmente: fondo nativo + parche HD, mismos guards/fallback y equivalencia píxel a píxel. Sigue aislada, sin SDL; CI nueva pendiente. Último paquete verificado: 3d82ff2. Densidad final abierta.

**Histórico 2.60 (superado por el cierre 2.61):** CI Windows d2e05e8 falló por falta de `<string>` en el generador HD (MSVC std::to_string). Include corregido; nueva CI/paquete pendientes. No usar d2e05e8 como paquete aprobado. [Evidencia](evidence/windows-d2e05e8-build-failure.json).

```text
Continúa OpenFodder en https://github.com/Cacheirez/openfodder, rama modernization/windows-foundation, PR #1 abierto, borrador y sin fusionar.

Lee íntegros README.md, CONTINUIDAD.md, PLAN_TRABAJO.md, RELEVO_2026-10-29.md y este prompt en docs/modernization desde la rama. Comprueba HEAD/PR/CI antes de editar. El plan vigente es 2.62. 2479fea era el relevo inicial 2.57; 30ba0ec es la referencia anterior con paquete verificado. Consulta evidencia posterior antes de afirmar CI/paquete nuevos aprobados.

Conserva base clásica 5e6a4f3, mejoras, originales visuales y H3 sin regenerar huellas para ocultar divergencias. No publiques datos comerciales CD32 ni partidas privadas. No cambies reglas, RNG, tiempos, colisiones ni campo visible. No introduzcas hilos ni actualices dependencias sin necesidad.

Dirección C — Pintado moderado elegida. No repetir A/B/C. Originales en assets/modernization/concepts y soldier-c01. Cursor también deberá rediseñarse. Miguel revisó ambas densidades del comparador en resoluciones/fondos: ambas bien, algo mejor la alta; prefiere calidad si memoria/rendimiento lo permiten. Densidad final no fijada, falta medición. No solicitar repetir el comparador completo.

Contrato y piloto aislado HD C01 implementados: Source/Utils/SoldierArtHD.hpp y docs/modernization/H6_4_PILOTO_HD_AISLADO.md. CMake deriva 8×/12× del PNG original; 1× es oráculo exacto. Orden, destinos y anclaje conservados. Oclusiones/recortes/pitch no soportados provocan retorno clásico; no hay oclusión HD parcial. Presupuesto por salida, no memoria total. Pruebas locales ASan/UBSan; CTest añadido Windows/Linux. Sigue sin conexión SDL: el juego compone C01 a 16×14. El comparador HTML tampoco es integración HD. No producir animaciones masivas.

Escenas aceptadas. Miguel confirma alternancia correcta, pero Save cerraba tras cambiar opciones antes de KEEP/REVERT. Causa reproducida/corregida en 2.59: el signo ? de la confirmación solicita frame 54 de fuente Briefing de 37; el buscador devuelve nullptr y GUI_Draw_Frame_8 lo desreferencia. Se elimina ese signo, sin tocar fuentes/raster. check_options_font.py usa funciones y tamaños reales PC/Amiga: falla antes, pasa después en toda la cuenta atrás. Añadido a CTest/CI. Falta aceptación física, no afirmar prueba en su Windows. El registro OPENFODDER_OPTIONS_TRACE sigue activo en el lanzador y H5_OPCIONES.log para otros posibles fallos. La fixture de transacciones anterior omitía el dibujo; no bastaba para detectar esta causa. Consultar H5_6_INCIDENCIA_SAVE.md.

Siguiente: cerrar CI del incremento por capas y preparar consumidor SDL opcional con contraste/fallback y transformación común. Guardado/persistencia ya aceptados por Miguel. El coste CPU aislado ya está medido; falta coste integrado/GPU antes de fijar densidad. Se autorizan tareas independientes. Actualiza siempre documentación/evidencia y conserva en GitHub los recursos para continuar.

Finaliza TODOS los mensajes con:
Hecho: ...
Situación del plan: ...
Próximos pasos: ...
```
