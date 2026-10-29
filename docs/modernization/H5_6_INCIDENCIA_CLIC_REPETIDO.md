# H5.6 — opciones que vuelven inmediatamente al valor anterior

29-10-2026 · incremento 2.54. Miguel confirma «Probar escenas está ok». Al probar opciones, CLASSIC cambia a FIT y vuelve a CLASSIC en menos de 0,2 s; lo mismo con ON/OFF del ratón. Esto bloquea la aceptación de opciones, aunque la transacción y la CI anterior pasaran.

## Causa y corrección

Mouse_UpdateButtons marca la pulsación nueva con -1, la consumida con +1 y la liberación con 0. Options_Menu_Run comprobaba solo que el valor no fuese cero y llamaba cada vuelta a GUI_Handle_Element_Mouse_Check. El dispatcher no consume el clic por sí mismo. AllowInput limita las acciones repetidas a 90 ms, pero no las convierte en una sola pulsación: un clic normal algo prolongado podía cambiar dos veces el toggle y parecer que no guardaba la selección.

El bucle ahora usa `Mouse_Button_Left_Toggled() > 0`, que consume el flanco una vez y espera a la liberación para rearmarse. Se aplica a todas las acciones del menú, incluidos tabs, flechas y SAVE/KEEP. Un clic fuera que se arrastra dentro no activa un control. No se cambia Mouse_UpdateButtons, el dispatcher compartido, los efectos de cursor, la simulación ni los fades. El limitador previo permanece, pero ya no provoca repeticiones mientras el botón siga pulsado.

## Reproducción y validación local

La fixture `check_presentation_options.py` incorpora los cuerpos reales de Mouse_UpdateButtons, Mouse_Button_Left_Toggled y GUI_Handle_Element_Mouse_Check, el callback real del menú y el bloque de clic extraído de Options_Menu_Run. Usa dobles SDL/elementos GUI, no un escritorio físico.

- Antes de corregir: falla la aserción de que Presentation conserva el primer cambio durante una pulsación sostenida; no es una suposición basada solo en el reporte.
- Después: Presentation, Alternate mouse y Mouse locked cambian una vez durante 120 vueltas de 16 ms; soltar y pulsar permite otro cambio, sin escribir el INI durante la edición.
- Pulsar fuera y arrastrar dentro no activa una opción sin una pulsación nueva.
- Mantener SAVE pulsado durante la pantalla de confirmación no ejecuta KEEP; hay que soltar y pulsar otra vez.
- Conserva pruebas de 15 s/wraparound, KEEP tardío, cancelar/Escape, restauración, fallo SDL, escritura y persistencia. ASan/UBSan local PASS.

Regresión de superficies: 27.648 casos PASS, incluidos colores efectivos y orden fade/Save/Restore. Compilación sintáctica de OptionsMenu.cpp contra SDL 3.4.0 PASS.

La prueba se emite también para el CTest Windows/Linux existente `presentation_options_transaction`. Se actualiza únicamente la huella exacta del menú revisado en options_presentation_contract.py; no se debilita la igualdad de efectos ni se alteran referencias H3.

## Paquete y prueba de Miguel

CI y paquete nuevos pendientes al publicar. El ZIP e18b05b/12849036551 todavía contiene el fallo; no pedir repetir con él. Una vez verificado el paquete corregido, abrir PROBAR_OPCIONES_H5.cmd y comprobar:

1. OPTIONS → VID → Presentation: un clic cambia CLASSIC/FIT una sola vez; mantenerlo un segundo no vuelve a alternar.
2. IN: Alternate mouse ON, Mouse locked OFF; cada cambio permanece hasta guardar/cancelar.
3. SAVE aplica provisionalmente; soltar y pulsar KEEP confirma. REVERT o esperar 15 segundos recupera el estado anterior. No redimensionar ni pulsar F11 durante la confirmación.
4. Cerrar y abrir el mismo lanzador conserva lo confirmado. FIT ajusta la imagen; CLASSIC conserva el escalado original. No cambian el arte.

Escenas ya aceptadas; no se requiere repetir el recorrido completo por esta corrección del menú. Densidad C 8×/12× después de aceptar opciones. Base clásica, mejoras, bocetos y PR sin fusionar conservados.
