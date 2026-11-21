# Locomoción baja 0x30/F0 — maestro existente, derivados propios

21-11-2026. Se reutiliza exactamente `source.png` de B0/F0, sin generar otra imagen ni modificar el B0 aceptado. Los derivados de 0x30 se exportan en su caja nativa (4,1,7,10), con celda lógica 16×14, centro 7,5 y apoyo inferior 11. Esto mantiene una escala coherente con F1/F2; las imágenes B0 para caída siguen intactas. No se comparte automáticamente la proyección RGBA entre acciones.

SHA del maestro y prueba nativa PC/Amiga en manifest.json y player-pose-reuse.json. Prueba de contenido de maestro, geometría y raster; rechaza desconocidos, duplicados y maestros alterados. PASS del conjunto: 96 casos Window/SDL por sistema con estados 0/1, dos actores, altura/recorte/oclusión, alias, negativos y recuperación; Windows ASan/UBSan y Linux ASan/UBSan/LSan. Fuente C01 y sangre/sombras independientes conservadas. Autoría dentro del criterio delegado por Miguel; aceptación global pendiente.

No hay prompt nuevo: el maestro original y su procedencia se conservan en ../demo-a1-player-fall-b0-f0/README.md.
