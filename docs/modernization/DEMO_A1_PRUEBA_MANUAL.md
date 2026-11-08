# A.1 — prueba manual a velocidad normal

8 de noviembre de 2026. Entrada `f91682d`. **Prueba manual NO ACEPTADA por Miguel:** los diseños nuevos aparecen de forma minoritaria e intermitente. La patrulla técnica acotada anterior sigue siendo evidencia de ese replay, no aceptación jugando. **No hace falta repetir la prueba ahora.** Plan 2.74 conservado; B no iniciado.

## Qué quedó preparado y qué se comprobó

`tools/modernization/run_demo_a1_interactive.py` reutiliza el ejecutable y el manifiesto A.1 exactos, copia los datos públicos a un directorio nuevo y arranca directamente **Amiga The One, misión 1, fase 2: Find Grenades**, con ratón manual y reloj normal. No usa `--unit-test`, `--demo-play` ni override del reloj. Renderizado software y sin sonido; no acredita GPU/audio/CD32. No modifica Source, recursos, vínculos, lanzadores existentes ni crea un paquete de entrega.

La ventana de prueba se vio con cinco nombres de soldados. La sesión con registros terminó normalmente: **4.456 intentos, 92 publicaciones HD y 4.364 retornos por faltantes; 2,06 % HD**. La racha mayor fue de 21 publicaciones, **0,409 s reales entre extremos**; no hay patrulla manual continua de 30–60 s acreditada. El muestreo de arranque produjo aproximadamente 48,83 resultados por segundo de pared con la cadencia normal de 20 ms conservada.

Primer rechazo después de publicar HD: intento **3913**, intervalo **3912**, rango tipo 21, **0x95/F4**, clave `84a0ee13d651ee9f27afe2d9284cacb3b3b53c18658c934effc0ba0942a0be5f`. En ese intervalo los cinco cuerpos sí resuelven, pero falta el rango y se rechaza la vista completa. Esa variante figura ausente en 4.162 comandos; no se equipara ese contador a 4.162 causas exclusivas porque un intervalo puede contener varios faltantes.

`Sprite_Handle_Player_Rank` toma el frame de `mMissionTroop->mRank`; cuando hay pasos de marcha pendientes usa el marcador nativo 0x7C/F0. A.1 solo conserva explícitamente 0x95/F0 y ese marcador. Por tanto, **una variante ordinaria del rango puede devolver al clásico a todos los cuerpos al detenerse**. Es consistente con la observación de Miguel, sin atribuirle una postura exacta no registrada. También faltaron tejado/caja/enemigos y otros elementos; no se aprueban vínculos por observarlos.

[Evidencia, hashes y primer bloqueo](evidence/demo-a1-interactive.json). Las dos sesiones fueron cerradas por Miguel. La primera no pudo redirigir logs: `Debugger::ConsoleOpen` sustituía stdout/stderr por su consola. El script conserva esos registros mediante `--appveyor`, que solo cambia su tratamiento diagnóstico y no activa pruebas ni acelera el reloj.

La tentativa de grabación de entradas con `--demo-record` guardó un solo estado y ningún `mVideoTicks`: **NO es un replay utilizable** y no se atribuye recuperación de los movimientos de Miguel. Se conserva como evidencia de esa limitación. El script final omite esa opción; sintaxis y ayuda comprobadas, pero no se ha vuelto a abrir el juego después del cierre del usuario solo para repetir el arranque sin grabación. Los logs de la sesión cerrada sí son válidos para los contadores anteriores.

## Pasos para repetir una revisión cuando proceda

1. Cerrar cualquier ventana anterior de OpenFodder. Abrir PowerShell. No hace falta compilar ni descargar nada.
2. Copiar este bloque completo. Cada ejecución genera un directorio nuevo y conserva su evidencia local:

```powershell
$repoA1 = 'C:\Users\migue\Projects\openfodder'
$fuenteA1 = 'C:\Users\migue\.codex\visualizations\2026\11\08\01a1bb46-b87b-7671-82cd-0fdee66db3de\a1'
$salidaA1 = 'C:\Users\migue\.codex\visualizations\2026\11\08\01a1bbd5-0759-7e10-8ff4-5c706a4a0b02\manual-miguel-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
python -B "$repoA1\tools\modernization\run_demo_a1_interactive.py" --source "$fuenteA1" --out "$salidaA1"
```

3. Si la ventana aparece pequeña o minimizada, restaurarla y ampliarla con su botón habitual. Confirmar que el título corresponde a **Find Grenades** y que hay cinco soldados en la lista. Si falta alguno, anotar ese primer fallo.
4. Revisar primero al grupo quieto durante unos segundos. Anotar si sus diseños cambian al aparecer la insignia de rango. **Este paso ya puede fallar con A.1 actual**; no es necesario conseguir 60 s si la alternancia aparece antes.
5. Para un recorrido acotado, usar clic izquierdo en suelo libre de la parte alta del claro y hacer desplazamientos cortos hacia la izquierda, alejándose del tejado de la derecha. Mantener a los cinco juntos; no bajar hacia enemigos ni buscar agua/combate. El cursor también mueve la cámara: después del clic llevarlo cerca del grupo, sin arrastrarlo a los bordes. Esto orienta la prueba manual, no garantiza repetir exactamente las coordenadas del replay técnico.
6. Si la imagen se mantiene estable, observar 30–60 s reales y alternar tramos cortos de marcha con paradas. Si vuelve al clásico, parpadea o cambia al girar/pararse, anotar el primer instante aproximado y qué estaba ocurriendo; no compensarlo cambiando repetidamente de camino para forzar un resultado favorable.
7. Revisar cinco aspectos: número de soldados visibles; continuidad del diseño al andar/girar/pararse; insignia de rango; ave cuando aparezca; desapariciones o dibujo incorrecto al solaparse con soldados/vegetación. Marcar **NO EJERCITADO** lo que no aparezca. No se necesita probar pausa/mapa/transiciones en esta sesión de patrulla.
8. Cerrar con la **X de la ventana del juego**. Esperar a que el comando termine. Enviar al asistente la ruta que imprime como «Evidencia» y una descripción breve del primer fallo; no pegar logs completos. Si se quiere conservar una captura o vídeo corto, usarlo como apoyo a la observación, no como sustituto de los registros.

El terminal muestra aproximadamente cada cinco segundos `HD=<publicaciones acumuladas>` y `retornos=<rechazos acumulados por faltantes>`. Son contadores acumulados: los retornos iniciales no desaparecen. Para comprobar continuidad se analizan las marcas de tiempo y transacciones del log; **que HD aumente alguna vez no equivale a PASS**. No hace falta alternar continuamente entre el juego y el terminal durante la prueba.

Para un contraste clásico separado, ejecutar el mismo bloque con una salida nueva y añadir `--classic` al comando Python. Comparar legibilidad y movimiento en una zona parecida; no equiparar dos recorridos manuales distintos a una comparación exacta de simulación. La grabación automática de entradas no forma parte del script final.

Formato de respuesta útil:

> Duración aproximada: … s. Cinco soldados: sí/no. Primer cambio: al andar/girar/pararme, aproximadamente en … s. Rango/ave: correcto/fallo/no ejercitado. Recortes/solapamientos: correcto/fallo/no ejercitado. Valoración: aceptable/no aceptable. Evidencia: ruta …

## Única tarea siguiente

**Auditar la variante original de rango 0x95/F4 y reconstruir/verificar su clave nativa exacta para proponer una corrección acotada dentro de A.** No añadirla por mera observación, no iniciar B, no ampliar arte/familias ni suprimir el rechazo transaccional. La prueba manual actual queda no aceptada; una corrección posterior necesitará su validación focalizada antes de pedir otra revisión a Miguel.
