# Revisión jugando — soldados enemigos P1

Estado: candidato preparado para revisión de Miguel; sin aceptación visual/jugable global. Hito enemigo en curso, con producción e integración del inventario finito comprobadas salvo la excepción documentada 4B/F0.

En PowerShell:

```powershell
& 'C:\Users\migue\.codex\visualizations\2026\11\19\01a1f3ca-14cf-76a1-a9ab-bf2ff6bf17c3\PROBAR_ENEMIGOS_P1.cmd'
```

El lanzador abre la fase de prueba existente Amiga The One, misión1/fase2. Verifica primero el ejecutable, SDL, manifiesto y473descriptores de activo (457archivos RGBA distintos; variantes de dueño comparten bytes comprobados). No cambia datos comerciales, partidas ni los lanzadores anteriores.

Para comprobar los archivos sin abrir el juego:

```powershell
& 'C:\Users\migue\.codex\visualizations\2026\11\19\01a1f3ca-14cf-76a1-a9ab-bf2ff6bf17c3\PROBAR_ENEMIGOS_P1.cmd' -Comprobar
```

Para comparar con el modo clásico:

```powershell
& 'C:\Users\migue\.codex\visualizations\2026\11\19\01a1f3ca-14cf-76a1-a9ab-bf2ff6bf17c3\PROBAR_ENEMIGOS_P1.cmd' -Modo clasico
```

Durante la partida, comprobar:

1. Diferenciación respecto al pelotón: uniforme gris oliva, casco gris verdoso, barba corta, detalle rojo teja y correajes rojizos.
2. Continuidad al caminar, apuntar, lanzar granadas, recibir daño, caer, deslizarse y entrar/salir de estados que aparezcan durante la partida.
3. Sombra fija abajo-derecha, luz arriba-izquierda y pies apoyados; agua, altura y sombras independientes conservan su tratamiento específico.
4. Varios soldados y pelotones, oclusiones, bordes, reinicios y final de fase: señalar cualquier retorno visible al cuerpo clásico, recorte o cambio de escala.
5. Jugabilidad y comparación clásica: señalar cualquier comportamiento distinto. No se han modificado simulación, RNG, colisiones ni reloj lógico.

El lanzador imprime la ruta del registro temporal `OpenFodder-P1-Enemigos-...` y conserva capturas nativas en `enemigos-snapshots-...` junto al CMD. Para informar de un defecto, indicar situación y ruta del registro/capturas; las imágenes nativas privadas no se publican en GitHub.

## Cobertura y límites

- 267poses/560derivados artísticos; líder106:51posesPC preparadas e integradas, Amiga vacío firmado conservado. Candidato12×:473activos/59.969.664bytes, dentro de64MiB.
- 679contratos enemigos:607modernos (601cuerpos y6sombras independientes),66órdenes vacías sin escritura,4marcadores nativos y2contratos de cuerpo sinHD.
-  **Excepción conocida:**4B/F0 enPC yAmiga conserva el cuerpo clásico. El rechazo aislado de ImageGen sigue auditado, sin reintento ni cambio de herramienta. Continuar sin esa imagen estaba autorizado; esto no es una cobertura artística del100%.
-  ReplayM1P2 Windows/Linux:1546estados intactos y4635publicacionesHD por sistema;6524apariciones modernas de infantería y171keep del marcador vacío7C/F1. Cero cuerpos enemigos visibles clásicos en ese replay y cero faltantes.
-  GuardiaDC, lanzacohetes36 y líder106 no aparecen en ese replay. Sus contratos se comprueban con recursos nativos y pruebas de composición; su ausencia en la reproducción no acredita aceptación jugando.
-  H3 Windows/Linux11fases/11361estados por sistema, Window/A2 y los cinco workflows completos pasan sobre el código `a192e5c2`. Los commits posteriores de evidencia no cambian Source; no se atribuye un nuevo PASS a sus ejecuciones CI pendientes.

Binario verificado: `e3029320f31aae51259e3acd3709c63ac97edf034d73753d6f42d1304b8b46ab`. Manifiesto: `a8f0d59f2db825ea281d7842fbc4d2a2ac3bfda077ea4216901de397beea6123`. Copia recuperable: `C:/Users/migue/.codex/visualizations/2026/11/19/01a1f3ca-14cf-76a1-a9ab-bf2ff6bf17c3/enemy-final-review`.

Si falla la integridad, el lanzador detiene la ejecución; conservar el mensaje y usar el lanzador anterior para recuperar la prueba previa. Los fallos reales del compositor mantienen la recuperación clásica segura. No se ha activado B, otro escenario artístico, scroll ni16:9.

Siguiente intervención: revisión visual/jugable de Miguel. Corregir defectos observados dentro del mismo hito; solo cerrar la aceptación enemiga con su valoración explícita.
