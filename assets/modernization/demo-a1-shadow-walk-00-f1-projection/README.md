# Proyección completa inferior derecha — propuesta visual

18-11-2026. Miguel precisa **luz desde arriba-izquierda y sombra hacia abajo-derecha en coordenadas de pantalla**, independientemente de que el actor mire de frente, lateralmente o de espaldas. V1 y V2 quedan rechazadas en posición. La intensidad de pintura puede ser adecuada; la extensión/posición nuevas esperan valoración.

Esta **única pose frontal de comparación**, a 8×/12×, conserva íntegramente el rectángulo RGBA del cuerpo de 16×14: mismos bytes, escala y colocación. Reutiliza toda la pintura de sombra anterior con alfa y colores intactos, trasladada +2 en X y +3 en Y de pantalla. **Esos números solo colocan esta propuesta**; no son un offset universal aprobado ni una regla de altura para las sombras independientes del motor.

`preview.cpp` genera una imagen de presentación 16×18, con margen inferior. No se genera arte nuevo, reduce el cuerpo ni recorta la cola. Los PNG/RGBA son **material de propuesta visual, no activos compatibles con el vínculo nativo actual**. `proposal.json` no tiene vínculos de ejecución. El compositor actual exige altura del activo igual a las 14 filas nativas; integrar una huella distinta requiere un microbloque gráfico explícito, sin retirar esa protección por conveniencia.

PASS de autoría offline: cuerpo idéntico byte a byte; todos los píxeles de sombra conservados; alfa y colores idénticos tras traslación; bytes iguales Windows/Linux con ASan/UBSan y LSan Linux. **PENDIENTE:** valoración de la propuesta; contrato/implementación de huella visual extendida y todas sus pruebas de motor. No atribuir a esta propuesta los 56 casos SDL de V1/V2.

[Maestro y prompt de pintura reutilizados](../demo-a1-shadow-walk-00-f1/README.md) · [Informe, comparación y alcance propuesto](../../../docs/modernization/SOMBRAS_HD_PILOTO.md#dirección-fija-de-luz--propuesta-de-proyección-completa).
