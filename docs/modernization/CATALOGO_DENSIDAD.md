# Carga de arte por densidad explícita

E3.D del hito enemigo autorizado. La medición [E2.9](evidence/enemy-reuse-budget-v1.json) estima 81.404.544 bytes al cargar ambas densidades del conjunto. El límite de activos sigue siendo **64 MiB**, con preflight antes de abrir ficheros. La solución carga solo la densidad que solicita la presentación.

El manifiesto ordenado versión4 exige `density: 8` o `density: 12`. Todos sus activos y vínculos deben corresponder a esa densidad. Su `player_catalog` usa schema2 y repite exactamente el mismo valor `density`; cada pose visible requiere un activo de esa densidad, mientras que las poses nativas ocultas y asociaciones mantienen su contrato sin cuerpo moderno. `complete` continúa exigiendo todos los estados producidos del catálogo.

Las versiones1/2/3 conservan el comportamiento anterior. Versión3/schema1 sigue requiriendo las parejas8×/12×. Un schema2 no se acepta a través de esa ruta antigua. El lanzador y candidato congelados de protagonistas no se modifican.

Una solicitud con densidad distinta a la declarada lanza un error de configuración; no se clasifica como arte faltante. La ruta existente de publicación conserva la recuperación clásica ante errores. No se cambia la elección lógica de dirección/frame ni la simulación.

Pruebas focalizadas Windows/Linux: catálogo completo por separado a8× y12×, rechazo de etiquetas y geometría incompatibles, parejas indebidas, estados omitidos y exceso de presupuesto antes de acceso a ficheros. También se conserva el resultado de los casos anteriores del catálogo y de composición de sombras. [Evidencia](evidence/enemy-density-loading-v1.json).

Este bloque proporciona el contrato de carga; no integra todavía el catálogo enemigo ni acredita aceptación visual o jugable. H3/CI completa y la revisión de Miguel se realizarán sobre el candidato enemigo integrado.
