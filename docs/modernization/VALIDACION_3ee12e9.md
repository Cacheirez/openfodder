# Cierre del diagnóstico y prueba visible C01

01-11-2026 · plan 2.68. Motor probado: `3ee12e978c21b3157521c0e1fb65573bb4c56a26`. PR #1 abierto, borrador y sin fusionar.

| Comprobación | Resultado |
|---|---|
| [Windows](https://github.com/Cacheirez/openfodder/actions/runs/41288644622) | completed/success |
| [Linux](https://github.com/Cacheirez/openfodder/actions/runs/41288644597) | completed/success, incluidos los diagnósticos declarados del workflow |
| [Comparador de densidades](https://github.com/Cacheirez/openfodder/actions/runs/41288644598) | completed/success |
| C01 visible 8×/12×, Windows y Linux | Publicación HD y exportación real; ocho fases PC y 7.956 estados H3 originales por densidad |
| HD 8×/12×, Windows y Linux | 11 fases PC/Amiga, 22 pausas/reanudaciones y 11.361 estados H3 por ejecución |
| ZIP Windows | 300 archivos, 29 fases públicas PASS sin omisiones; hashes, CRC, VERSION y ejecutable comprobados |

7d27b59 falló en Windows por faltar `<string>` explícito para std::to_string. 3ee12e9 corrige los includes y pasa las tres ejecuciones completas. Los intentos locales rechazados quedan registrados en [la evidencia local](evidence/c01-diagnostic-local-2026-11-01.json); H3 no se ha regenerado.

## Paquete verificado

[OpenFodder Windows x64 demos](https://github.com/Cacheirez/openfodder/actions/runs/41288644622/artifacts/13077821521).

- ZIP SHA-256: `04cd7fa886aa93acc28830f01a9c522e0471b00120b62bf0d57383a115760e5a`.
- Ejecutable SHA-256: `b804a58ea63c26779e823499be4693de7632d2bc773c212c910d2465d65b27d7`, coincidente con PRUEBAS.json, C01_PRUEBA.json y ambos informes HD Windows.
- VERSION: `b7fddc75c83a27d9dcae0a05d66c12bfe30e80ac`; merge temporal de CI, no fusión del PR. Su árbol coincide con el motor probado: `a726c734dca4a54a89b247cfb64a275772dcd105`.
- Incluye C01_8.html/C01_12.html y sus seis BMP; sus hashes coinciden con CI Windows, Linux y el recorrido local final. Se verificaron carga BMP, recorte Src, ampliación y alternancia ejecutando el JavaScript generado con Skia Canvas. No es una prueba DOM/navegador ni GPU física.
- Incluye PROBAR_C01_VISIBLE.cmd y exactamente ocho grabaciones PC públicas de tests `c7722ef1a37c1e04ff28c6fedf9d3bdff197dc86`, contrastadas byte a byte. El README de tests solo difiere por CRLF Windows, comprobado tras normalizar saltos; no se normalizan los binarios OFD.
- Todos los lanzadores coinciden con Git. El informe de comparación coincide con el artefacto de evidencia CI. Sin partidas privadas, configuraciones personales ni datos comerciales.
- El artefacto caduca el 01-12-2026; código, informes compactos y manifiestos quedan en Git. Reconstruir desde el commit/workflows si caduca; los hashes no reconstruyen el ZIP.

Evidencia: [CI](evidence/3ee12e9-ci.json), [manifiesto del ZIP](evidence/windows-3ee12e9-package.json), [control adicional C01](evidence/windows-3ee12e9-c01-package.json), [C01 Windows](evidence/windows-3ee12e9-c01.json), [C01 Linux](evidence/linux-3ee12e9-c01.json), [HD Windows 8×](evidence/windows-3ee12e9-hd8.json), [HD Windows 12×](evidence/windows-3ee12e9-hd12.json), [HD Linux 8×](evidence/linux-3ee12e9-hd8.json), [HD Linux 12×](evidence/linux-3ee12e9-hd12.json).

## Uso y alcance

1. Extraer en carpeta nueva y abrir C01_12.html para ver inmediatamente clásico/HD y sus detalles ampliados. Conservar los BMP a su lado.
2. Ejecutar PROBAR_C01_VISIBLE.cmd para repetir PC Format completo con HD 12×. Puede tardar varios minutos y abre la comparación solo tras una exportación nueva confirmada. Si falla, conservar C01_PRUEBA.log.
3. Para jugar con diagnóstico, usar PROBAR_HD_8X.cmd o PROBAR_HD_12X.cmd. Sus logs incluyen SOLDIER_HD_REASON una vez por motivo. SOLDIER_HD_SDL confirma publicación efectiva; los motivos pueden ser transitorios.

En CI se observaron palette-transition, no-eligible-c01, black-palette y later-layer-overlap, además de publicación y exportación correctas. Eso no determina retrospectivamente la causa de los logs antiguos de Miguel, que carecían del diagnóstico. La prueba visible evita tener que encontrar una pose apta manualmente.

Sigue siendo una pose C01, con tamaño lógico 16×14 y retorno clásico en recortes/oclusiones no soportados. Falta aceptación visual en el Windows/GPU de Miguel y medir coste integrado antes de fijar densidad o preparar más animaciones. Guardado/persistencia ya aceptados; no repetirlos. Clásico por defecto, H3 y originales preservados.
