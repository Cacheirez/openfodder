# Cierre completo del fundido y primer HD de misión

20-11-2026. Hito de continuidad en curso; división del pelotón valorada favorablemente por Miguel en la partida 16:43, reinicio aún pendiente. No se declara aceptación de todos los casos de muerte ni del saludo final.

## Evidencia y límite de la corrección

En la escena de reinicio 12933, el diagnóstico registra `palette-transition` en la presentación 6148, `black-palette` en 6151 y primera publicación HD en 6235, sin faltantes tempranos. El primer turno publicado contiene cuerpos ya enlazados. El caso mínimo con la función nativa exacta demuestra que se alcanza el destino RGB una llamada antes de limpiar `mPaletteAdjusting`; esa función se conserva byte a byte frente a la referencia ya usada por las pruebas de pausa.

`cSurface::paletteMatchesTarget()` lee los 255 RGB actuales y objetivo, sin escribirlos ni avanzar el fundido. `WindowHD` conserva el rechazo de transición mientras haya cualquier diferencia, incluso una entrada no usada por el cuerpo. Si todos los colores coinciden, continúa por la ruta normal de auditoría, paleta negra, identidad/recursos, compositor y recuperación SDL. No modifica `palette_FadeTowardNew`, número de llamadas, ticks, RNG, simulación, manifiesto 244/399 ni píxeles de arte. Modo clásico independiente. **No añade HD durante el fundido parcial**.

## Pruebas focalizadas y pendientes

PASS Window real/SDL software en Windows y Linux a 8×/12×, estricto/híbrido; transición parcial, última entrada diferente y negro rechazados; paleta completa aun marcada ajustando produce exactamente el resultado compuesto y mantiene la recuperación completa ante fallo SDL. Windows ASan/UBSan y Linux ASan/UBSan/LSan. El censo de pruebas no se cambia: se ejercita el nuevo estado en las publicaciones/recuperaciones ya existentes.

La prueba Linux de superficie real incorpora el accesor, demuestra su lectura sin efectos, compara la rutina de fundido con la referencia histórica y conserva 144 secuencias de pausa con 0/1/5 presentaciones. [Huellas y estado](evidence/cierre-fundido-20261120.json).

PENDIENTE antes de entregar prueba: H3/replay del motor nuevo Windows/Linux, contraste de primera publicación y CTest/A2/CI pertinentes. Aceptación jugando reservada a Miguel. La paleta parcial sigue clásica; si el defecto observado requiere representarla en HD, hará falta un contrato separado y decisión de alcance, sin desactivar guardias.

Recuperación local en la carpeta diagnóstica del 19-11: `palette-probe/`, `palette-probe-linux/`, motores separados `palette-probe-build/Release/native_probe.exe`, `palette-probe-linux-build/native_probe`; `test-palette-win.ps1`, `test-palette-linux.sh`, `check_palette_runtime.py`. Los motores/lanzadores anteriores permanecen intactos.

La escena posterior 28147 comienza con un enemigo sin resolución y no publica HD: está fuera del experimento Amiga The One M1P2. No se extiende ese experimento a otra fase por este diagnóstico. El final de fase incluye textos y poses sin vínculo y permanece sin aceptación ni producción de arte.
