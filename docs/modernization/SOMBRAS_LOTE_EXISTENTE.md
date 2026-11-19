# Sombras — extensión autorizada al arte existente

18-11-2026. Miguel acepta el contacto del piloto y pide aplicar el mismo criterio a todas las imágenes existentes. **La revisión visual del piloto queda cerrada.** Se autoriza la corrección del lote existente y el soporte gráfico acotado necesario para llevar ese criterio al compositor, según el alcance ya presentado. No se solicita otra autorización rutinaria para ese soporte; se mantienen las garantías y las decisiones artísticas reservadas.

## Alcance y clasificación inicial

Candidato acumulado de daño: 230 activos a dos densidades, correspondientes a 115 poses, y 386 vínculos. Las copias de revisión, maestros y derivados no se cuentan como poses nuevas.

| Grupo existente | Poses / activos | Tratamiento |
|---|---|---|
| Marcha del aliado | 24 / 48 | Sombra de suelo en coordenadas de pantalla, con contacto y ancla por pose |
| Apuntado/tumbado del aliado | 8 / 16 | Comprobar raster y apoyo propio; no asumir pies verticales |
| Lanzamiento de granada del aliado | 24 / 48 | Sombra del cuerpo normal; proyectil y su sombra siguen independientes |
| Lanzacohetes del aliado | 24 / 48 | Sombra del cuerpo normal; no alterar proyectiles |
| Enemigo normal ya preparado | 3 / 6 | Dos marchas y una pose tumbada; conservar su estado de activación actual |
| Muerte de enemigo | 1 / 2 | Comprobar sombra independiente/estado; no añadir suelo por semejanza |
| Caídas de aliado | 3 / 6 | Conservar ruta de altura y sombra independiente comprobada |
| Nado | 12 / 24 | No pintar sombra de suelo; preservar recorte/agua |
| Daño/muerte de aliado | 16 / 32 | Conservar las sombras independientes y el contrato del lote aprobado |

La clasificación delimita **83 poses normales candidatas** y 32 poses especiales. No certifica por sí sola la presencia de sombra en todos los rasters: la comprobación nativa y del apoyo por pose debe acompañar la propagación. Recursos sin prueba suficiente quedarán pendientes, sin inventar sombras. El arte de enemigo permanece clásico durante el experimento que así lo exige; preparar su sombra HD no activa esos cuerpos.

## Criterio aprobado y contrato gráfico

- Dirección fija de pantalla **↘**, luz **↖**, independiente de la orientación del actor; ni espejo ni giro de la sombra al girar el cuerpo.
- Cuerpo existente, tamaño, ancla, frame y temporización intactos. Sombra bajo el apoyo y proyectada a la derecha/abajo; la posición/tamaño se verifican por pose. El desplazamiento del piloto no es un offset universal.
- Reutilizar la pintura aprobada; no generar nuevas familias ni rehacer los cuerpos.
- Presentar la sombra de suelo como componente visual del **mismo comando corporal nativo** cuando corresponda a su sombra embebida. Conservar la secuencia completa, terreno, oclusiones, ceros/igual color, Save/Restore, bordes, presupuesto y recuperación.
- Mantener la geometría lógica 16×14 u otra que realmente tenga cada cuerpo. El soporte gráfico debe permitir la extensión de sombra **sin retirar la comprobación de dimensiones del cuerpo**. Una componente de sombra separada en el descriptor HD permite también omitirla al aparecer altura o filas recortadas, sin dejar pintura embebida residual en el cuerpo.
- No añadir esa componente en agua, daño/muerte, vuelo, estados no verificados o donde exista una sombra independiente incompatible. No modificar su lógica nativa ni la simulación.

## Microbloques y siguiente tarea

1. **Inventario y cierre de aceptación — completado documentalmente.** Estado inicial y autorización registrados; activos originales conservados.
2. **Contrato de sombra de suelo — AUTORIZADO / siguiente tarea única.** Componente opcional en el descriptor de arte, vinculada por identidad exacta; composición en el turno del cuerpo y extensión acotada, con negativos, clásico independiente, estricto/híbrido y sanitizadores. No activar arte masivamente antes de comprobar este contrato.
3. **Propagación a poses normales — AUTORIZADO**, después del contrato y pruebas requeridas. Revisión de fuente nativa y apoyo por pose/dirección, reutilizando pintura y cuerpos. Validación y publicación por bloques acotados; registrar exclusiones y faltantes reales.
4. **Conjunto comprobado y revisión jugando — AUTORIZADO**, tras las poses disponibles. Medir publicaciones/retornos, verificar transición de suelo a daño, altura y agua, H3/CI pertinentes y revisión de Miguel. No declarar aceptación jugando a partir del piloto o de pruebas automáticas.

Hito en curso. No se amplía a B, nuevas escenas/familias, scroll ni 16:9. No se usan subagentes ni escalado de modelo. El plan y Arranque rápido registrarán cada punto comprobado y una única tarea siguiente.

## Contrato de sombra de suelo — comprobaciones locales

**Implementado:** componente opcional `ground_shadow` por descriptor corporal, con referencia SHA-256 a pintura de la misma densidad, desplazamiento de pantalla en cuartos y tipo de propietario 0/5. Se mantiene la comprobación original `art.width/height == geometría nativa`: el cuerpo no se convierte en un recurso lógico más grande. La pintura se emite antes del cuerpo, **en el mismo comando**, sobre las celdas HD que correspondan, incluidos los márgenes visuales permitidos. No se superpone una sombra sobre la captura final.

La extensión se recorta a vista/superficie, respeta skip/bordes, oclusiones en ambos sentidos, escrituras de cero/igual color, terreno, Save/Restore y el presupuesto conjunto de celdas. Las referencias anidadas, identidad/densidad/tipo/coordenadas/huella inválidos se rechazan. La posición parte del ancla completa anterior al recorte nativo, evitando que el redondeo PC/Amiga del borde izquierdo desplace la sombra.

El vínculo solo se activa para las familias normales existentes verificables: aliado hojas 0–23 y 57–64, enemigo preparado 0x44/0x45/0x59, animación 0, sin vehículo/destrucción, altura cero y cero filas omitidas. En otro estado se conserva el cuerpo que su vínculo exacto ya autorizaba y se omite la componente de suelo. Los alias de impacto de animación 1 no heredan la sombra. Los enemigos del experimento clásico continúan resolviéndose por su ruta clásica anterior.

**PASS local observado:**

- CPU: cuatro grupos PC/Amiga a 8×/12× para contrato nuevo, con dimensiones, negativos de manifiesto, recortes, presupuesto, altura/agua/estado, terreno y orden; 156 escenarios del compositor anterior conservados.
- SDL: 388 casos de publicación, recorte, fallos y reentrada con sombras extendidas, en ambos sistemas. ASan/UBSan Windows y ASan/UBSan/LSan Linux.
- Window real: 56 casos del piloto con componente separada, dos cuerpos, estricto/híbrido, bordes, oclusión, Save/Restore, recorte inferior idéntico al cuerpo sin sombra y recuperación íntegra por error SDL. La compatibilidad con el candidato anterior también se recompiló/comprobó.
- H3 Windows con nuevo binario aislado: **11 fases / 11.361 estados**, referencias originales intactas.
- Replay real público M1P2, manifiesto opt-in de 200 activos/363 vínculos: **4.096 publicaciones y 458 faltantes**, conservando los 1.546 estados H3. Solo el cuerpo piloto tiene aquí la componente; **no es aún el lote completo ni aceptación jugando**.

**Contrato verificado el 19-11:** [CI Windows completa](https://github.com/Cacheirez/openfodder/actions/runs/44416432197) PASS; [CI Linux](https://github.com/Cacheirez/openfodder/actions/runs/44416432186) PASS observado en CTest (incluye `soldier_ground_shadow`), A2, H3 original y publicación ordenada pertinentes. Diagnósticos completos Linux aún en curso. H3 local Linux también conserva **11 fases / 11.361 estados**. Se cierra el soporte y continúa la propagación autorizada. La CI completa, GPU, CD32, audio y aceptación jugando no se declaran PASS. El lanzador habitual y su ejecutable anterior permanecen intactos.

[Evidencia local del contrato](evidence/sombras-contrato-suelo-20261118.json). Recuperación: carpeta local del 17-11 `01a1ea7b-b727-78f2-a6ac-a4b32dc39150`, subdirectorios `ground-contract/`, `ground-probe-build/`, `ground-runtime-pilot-20261118/` y `ground-shadow-h3-20261118-{pc,amiga}/`; scripts `prepare-ground-contract-pilot.py`, `run-ground-contract-{win.ps1,linux.sh}`, `run-ground-pilot-linux.sh`, `check_ground_contract_h3.py`, `run-ground-runtime-pilot.py`. Fuentes y recursos nativos privados permanecen locales.

## Cualificación previa de contacto — 19-11

83 poses normales / 166 activos pasan WindowHD real: **332 casos Windows y 332 Linux**, con sanitizadores focalizados. Las 80 referencias aliadas se reconstruyen desde tabla/recurso verificados, no son observaciones de ejecución; solo 27 claves de paleta 0 coinciden con vínculos existentes. No se añaden aquí las otras 53 ni se alteran referencias históricas. Las tres referencias enemigas proceden de capturas verificadas.

Copiar la posición piloto falla el contacto en 89/166 derivados. El ajuste reutiliza la pintura, anchura 7–16 y cuartos de píxel por dirección, compartidos por sus frames y densidades. Los 35 grupos conservan SHA corporal, contacto completo y proyección derecha/abajo. No es aceptación visual del conjunto. Evidencia local: `ground-contract/contact-fit/contact-qualification.json` y `ground-contract/qualified/*/window-{win,linux}.log`.

## Propagación reproducible

Primer grupo comprobado: marcha dirección 0, tres frames / seis activos. `assets/modernization/ground-shadow-paint/placements.json` fija SHA del cuerpo y colocación común; `manifest.json` fija las pinturas derivadas del maestro aprobado. No se modifican PNG/RGBA corporales ni se añaden claves nativas. La herramienta comprueba todos los bytes de entrada y crea otro candidato, sin sobrescribir el origen:

```powershell
python tools/modernization/prepare_ground_shadows.py --base RUTA/candidate-manifest.json --out NUEVO_DIRECTORIO
```

Con el primer grupo: 232 activos / 386 vínculos desde el candidato de daño 230/386. Los 32 estados especiales conservan sus descriptores. La extensión al resto consiste en publicar sus ajustes ya cualificados, no en regenerar cuerpos ni encargar arte. [Evidencia por dirección y plataforma](evidence/sombras-lote-contacto-20261119.json).
