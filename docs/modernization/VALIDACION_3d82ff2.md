# Cierre CI y paquete — 3d82ff2

30-10-2026 · plan 2.61. Revisión probada `3d82ff2b4774c8d9939a2315e19bef3fe21122de`, árbol `536cae4a1b1468e1d1f942f94710691c85c993d8`. Incluye corrección Save y dependencia explícita `<string>` del generador HD. PR #1 abierto, borrador y sin fusionar.

| Validación | Ejecución | Resultado |
|---|---|---|
| Windows | [41017089830](https://github.com/Cacheirez/openfodder/actions/runs/41017089830) | Completa PASS |
| Linux | [41017089777](https://github.com/Cacheirez/openfodder/actions/runs/41017089777) | Completa PASS |
| Comparador | [41017089624](https://github.com/Cacheirez/openfodder/actions/runs/41017089624) | Completa PASS |

[Pasos Windows](evidence/ci-3d82ff2-windows.json) y [Linux](evidence/ci-3d82ff2-linux.json) conservados. Incluyen CTest, H3 original, replays, sondas y diagnósticos de memoria/concurrencia declarados por los workflows; sus límites de cobertura siguen vigentes. La notificación Discord Linux fue omitida, no una prueba omitida. No afirma HD SDL, Windows físico o GPU probados.

## Paquete comprobado

[OpenFodder-Windows-x64-demos](https://github.com/Cacheirez/openfodder/actions/runs/41017089830/artifacts/12961100516). Artefacto 12961100516, caduca el 29-11-2026. ZIP descargado e inspeccionado, 279 archivos. SHA-256 `ed41bb8b8ad23e11b6cb5d8df39dc11e15038a71d537c96d5d00ebb76e3708d6`, igual al digest de Actions. Ejecutable SHA-256 `7ed1ec4d104a3b294bcaa4f8d5dd5ef762da044f1ee2b9df9641cfa76b451e0c`, idéntico al de PRUEBAS.json: 29 fases PASS, cero omisiones.

VERSION.txt identifica `afadf961f4de0a5799e3235b2ad1c9753d66a750`, merge temporal de CI cuyo árbol coincide exactamente con 3d82ff2. No se ha fusionado el PR. Verificadas DLL, licencias, siete demos permitidas, ausencia de partidas/configuración/logs privados, integridad ZIP, lanzadores y guías contra Git. Las guías usan CRLF de Windows: coincidencia exacta al normalizar CRLF a LF; se corrigió esa comparación en el verificador, sin cambiar el paquete.

[Manifiesto completo y hashes](evidence/windows-package-3d82ff2.json). Receta en `tools/modernization/verify_windows_package.py`. Los hashes no sustituyen el ZIP tras caducar; reconstruir desde revisión/workflows si desaparece. Evidencia Actions Windows adicional: artefacto 12960423332, digest `91d24a4d6bb226c16df41a03654792cdf0da717e698bbb9b341b0fd6af58ae6d`; no se afirma archivado permanente de ese ZIP completo.

## Prueba pendiente de Miguel

Extraer el ZIP en una carpeta nueva. Ejecutar `PROBAR_OPCIONES_H5.cmd`, cambiar CLASSIC/FIT y pulsar SAVE. Debe aparecer la confirmación sin cerrarse: KEEP conserva, REVERT restaura y dejar pasar 15 segundos también restaura. Tras KEEP, cerrar/abrir y comprobar persistencia. Si cierra, conservar `H5_OPCIONES.log`. Escenas y alternancia ya aceptadas: no hace falta repetir toda la matriz.

## HD

[Informe de costes](H6_COSTE_HD_AISLADO.md), 21.600 muestras: no integrar tal cual el escalado CPU completo; conservar textura 12× candidata y 8× parametrizado. La densidad definitiva queda pendiente de composición eficiente, coste integrado y prueba visual/GPU. Los cambios posteriores de documentación/herramientas no deben confundirse con el commit exacto del paquete.
