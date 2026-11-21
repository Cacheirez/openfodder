# Cierre de CI y paquete HD SDL

31-10-2026 · plan 2.66. Commit probado: `a05e656c1201c38ad750efdfcfd266c70915c4ed`. PR #1 abierto, borrador y sin fusionar.

| Comprobación | Resultado |
|---|---|
| [Windows](https://github.com/Cacheirez/openfodder/actions/runs/41197313659) | completed/success |
| [Linux](https://github.com/Cacheirez/openfodder/actions/runs/41197313403) | completed/success |
| [Comparador](https://github.com/Cacheirez/openfodder/actions/runs/41197313475) | completed/success |
| HD 8× y 12×, Windows/Linux | Cada ejecución: 11 fases, 22 pausas/reanudaciones, 11.361 estados H3 originales y publicación HD real en PC/Amiga |
| Paquete Windows | SHA-256, CRC, manifiesto, VERSION y ejecutable contrastados; 281 archivos, 29 demos PASS sin omisiones |

La ejecución 75a91ff falló porque la sonda buscaba ticks absolutos 8/16 en grabaciones que restauran relojes avanzados. 4856a8f cuenta pasos por fase sin alterar la simulación y exige ambas parejas completas. Su Windows pasó 8× y PC 12×, pero agotó 35 minutos durante Amiga 12×. a05e656 amplía el presupuesto a 60 minutos sin reducir cobertura. La nueva ejecución terminó correctamente.

## Paquete y trazabilidad

[Descargar OpenFodder Windows x64 demos](https://github.com/Cacheirez/openfodder/actions/runs/41197313659/artifacts/13041734254).

- ZIP SHA-256: `3941883aad06af016962780a79ca98fe4e01934e64c1a47e88856b0be4bb6ac6`.
- Ejecutable SHA-256: `f310774b50e673d91a50d299f058bd8ad0a904090eee0bfc4a9e5fd4982deead`, coincidente con PRUEBAS.json y los informes HD.
- VERSION: `1385a699d9bcfb519b0864d628792d8aefa14e4a`, merge temporal de CI, no fusión del PR.
- Árbol VERSION y commit probado: `51ffee365e23bf1ab3f5d1e3a8643546aa048ced`.
- Ambos lanzadores `PROBAR_HD_8X.cmd` y `PROBAR_HD_12X.cmd` presentes y coincidentes con Git; densidad correspondiente comprobada.
- El verificador rechaza partidas/configuraciones privadas, rutas inseguras, demos fuera del conjunto público y discrepancias entre ejecutable probado y empaquetado.
- El artefacto de Actions caduca el 30-11-2026; los informes compactos y el manifiesto quedan en Git.

[Manifiesto del paquete](evidence/windows-a05e656-package.json). Informes: [Windows 8×](evidence/windows-a05e656-hd8.json), [Windows 12×](evidence/windows-a05e656-hd12.json), [Linux 8×](evidence/linux-a05e656-hd8.json), [Linux 12×](evidence/linux-a05e656-hd12.json). [Corrección y resultados locales](evidence/hd-sdl-replay-fix-2026-10-31.json).

## Prueba visual pendiente en Windows

1. Extraer el ZIP en una carpeta nueva. Ejecutar `PROBAR_HD_12X.cmd` y después `PROBAR_HD_8X.cmd` para comparar el mismo recorrido.
2. Durante una misión, comprobar anclaje del soldado, orden visual y ausencia de restos al moverlo, pausar/reanudar y abrir/cerrar el mapa. Comprobar también redimensionado y F11 con HD activo.
3. Cerrar el juego y usar `INICIAR.cmd` para volver al arranque clásico. No hace falta repetir la aceptación del guardado de opciones.
4. Si se ve un defecto, conservar `H6_HD_12X.log` o `H6_HD_8X.log` y anotar demo, fase, resolución y acción que lo reproduce.

Es un piloto de una pose C01, no una sustitución de todas las animaciones. Los casos de oclusión/recorte no soportados vuelven al clásico. La presencia del marcador `SOLDIER_HD_SDL` en el log confirma que llegó a publicarse el parche; puede no aparecer en la primera fase PC.

## Límites conservados

La CI usa SDL software: no acredita prueba física Windows/GPU ni FPS en el equipo de Miguel. Las pruebas automatizadas cubren escalado entero/fraccionario, transiciones controladas y recuperación ante fallos. A escala fraccionaria se conserva exactamente el exterior clásico y el anclaje, sin prometer igualdad con un canvas completo expandido. La ruta crea texturas temporales; falta medir coste integrado/GPU antes de decidir caché y densidad definitiva. Se mantienen las exclusiones históricas documentadas de sanitizadores y la falta de cobertura comercial CD32.

Siguiente paso: aceptación visual acotada en Windows/GPU y medición integrada. Guardado/persistencia ya aceptados. Base clásica, H3, arte original y PR en borrador conservados.
