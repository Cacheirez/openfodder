# Piloto de sombra — revisión inferior derecha

18-11-2026. Miguel rechaza la posición de V1 y considera que su intensidad puede ser adecuada. **Esta revisión conserva tamaño, colocación y píxeles opacos del cuerpo HD**, así como el maestro y el alfa de la pintura de sombra. Solo retira el lóbulo superior y limita el dibujo a la cola inferior derecha: mitad inferior de la fila lógica 12, columnas 9–11, y fila 13, columnas 8–10. Son celdas pertenecientes a la componente oscura nativa ya comprobada; su separación respecto a pies/contacto sigue siendo una interpretación artística del piloto.

No hay generación nueva de imágenes. [Maestro y prompt originales](../demo-a1-shadow-walk-00-f1/README.md). `compose.cpp` es un exportador offline para esta única pose, no código del motor. Se conserva el marco 16×14, el ancla `[0,14]`, una clave exacta y dos densidades. `manifest.json` registra hashes, máscara y medidas de posición. El volumen total de sombra cambia al retirar la parte alta, aunque los valores de pintura/alfa conservados son iguales.

PASS 56 casos Window/SDL Windows-Linux con sanitizadores y exportación idéntica entre plataformas. Se reutilizan los fixtures de V1 con el candidato nuevo; la referencia del recorte inferior vuelve a ser el **HD original a tamaño completo**. El piloto sigue aislado y pendiente de valoración visual; no modifica el lanzador normal ni las sombras independientes.

[Informe, comparación y recuperación](../../../docs/modernization/SOMBRAS_HD_PILOTO.md#revisión-2--posición-inferior-derecha).
