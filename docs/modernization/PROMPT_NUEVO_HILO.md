# Prompt para continuar en un nuevo hilo

Copia el bloque siguiente. Con acceso al repositorio de GitHub **no necesitas adjuntar nada**: código, maestros, manifiestos, pruebas, catálogo y plan están allí. El ZIP f72d6e7 sirve para reproducir el defecto; no es el código fuente ni una solución corregida.

```text
Continúa la modernización de OpenFodder en https://github.com/Cacheirez/openfodder, rama modernization/windows-foundation. PR #1 debe permanecer abierto, en borrador y SIN fusionar. Trabaja en español de España y avanza con autonomía sin pedir confirmaciones rutinarias. No uses subagentes salvo que yo lo autorice.

Primero consulta el HEAD/PR/CI reales y lee docs/modernization/CONTINUIDAD.md, PLAN_TRABAJO.md y SOLDADOS_COBERTURA_COMPLETA.md. Usa DESARROLLO.md para preparar el entorno. El plan vigente es 2.74, salvo actualización posterior explícita. Los informes antiguos no determinan el próximo paso.

Incidencia confirmada por mí (Miguel): he probado PROBAR_SOLDADO_ANIMADO.cmd y el soldado moderno aparece intercalado con el antiguo. Esto NO está aceptado. Quiero recrear lo que hace el original, sustituyendo sus sprites por modernos en todas las direcciones y estados; no otra muestra que cambie de estilo durante el juego normal. Incluir todos los soldados presentes, y revisar enemigos y variantes; distinguir civiles/rehenes y efectos asociados en la matriz.

El piloto f72d6e792c359cec2f53d006d167738c2104bc66 solo cubre hojas 2/7, frames 0/1/2, primer jugador y un parche. Rechaza superposiciones, recortes y muchos estados. Añadir PNG sin ampliar captura y composición NO soluciona el problema. No elimines guards sin implementar orden/oclusiones correctos.

La revisión del código confirma 8 direcciones y 3 frames por dirección para marcha (24 claves por bando), con contador 0–1–2–1 y excepciones del motor. Hay agua, granadas, cuerpo a tierra, armas, muerte y rutas especiales. Respeta mFaceDirection, apuntado, selección de frame, ritmo y fase originales: no inventes dos frames globales ni un reloj a la frecuencia del monitor. El catálogo reproducible está en tools/modernization/inventory_soldier_catalog.py y docs/modernization/evidence/soldier-catalog.json. Sus entradas estáticas no son aceptación visual ni cobertura dinámica.

Siguiente trabajo: A1/A2 del plan. Completar matriz de estados/recursos/entidades y casos que detecten cualquier cuerpo clásico no previsto. Generalizar captura y composición ordenada de múltiples cuerpos con recortes/agua/oclusiones. Preparar el ciclo completo de 24 claves como paso interno y después todos los estados y variantes censados. No declarar soldado completo solo porque marcha en ocho direcciones o porque seis claves se publican alguna vez.

Conserva estilo C — Pintado moderado y maestro C01 (detalle, posición e integración ya aceptados). Los cinco maestros adicionales son provisionales y pueden necesitar ajuste al frame original. Originales/manifiestos en assets/modernization. No vuelvas a proponer estilos A/B/C. 12× provisional, 8× disponible; densidad final y GPU pendientes. No bloquees cobertura con más perfilado sin una hipótesis concreta.

No cambies reglas, RNG, tiempos lógicos, colisiones, campo visible ni orden de simulación; no regeneres H3 para hacer pasar cambios. Mantén contraste clásico independiente. Base clásica 5e6a4f3834a0a491468ea659f45f8e5f4fb785a8 intacta. Clásico disponible por elección y recuperación segura/coherente ante errores reales; no usar fallback normal por cobertura incompleta como criterio de terminado. CD32 es objetivo principal, pero sus datos privados no van a GitHub. Las demos públicas permiten avanzar; pide material privado solo si una tarea concreta lo necesita.

Último ejecutable probado: f72d6e7. CI Windows/Linux/comparador PASS, ZIP artefacto 13106475504, 29 fases sin omisiones y H3 del lote 3405 estados intactos. Esto no corrige ni invalida la mezcla observada. La revisión documental 2.74 NO cambia el motor. La evidencia exacta está en soldier-batch-package.json. No pedir que vuelva a aprobar ese mismo piloto parcial.

Agrupa cambios útiles, pruebas focalizadas y documentación breve. Antes de entregar otro ejecutable, CI pertinente completa, hashes e informes ligados al ZIP; validar giro continuo, marcha, apuntado, disparo, granadas, agua, daño/muerte, varios soldados, oclusiones y transiciones. Marcar casos no ejecutados como pendientes. Mantén el alcance final H0–H10 en ALCANCE_H0_H10.md y no cierres A/H7 por CI verde.

Termina tus mensajes con estas tres líneas:
Hecho: ...
Situación del plan: ...
Próximos pasos: ...
```

## Adjuntos

- **Con GitHub conectado:** ninguno obligatorio. Basta el prompt y acceso de lectura/escritura al repositorio.
- **Opcional y útil para diagnosticar la alternancia concreta:** `SOLDADO_ANIMADO.log` de la carpeta del juego y un vídeo corto donde se vea. No bloquean las correcciones ya identificadas.
- **Si el nuevo hilo no puede acceder a GitHub:** adjunta una copia de la rama de trabajo con código, assets, docs y tools. Para ejecutar pruebas de equivalencia contra commits antiguos se necesita también el historial Git y los submódulos/datos demo; el ZIP del ejecutable por sí solo no basta. El asistente debe explicar qué acceso falta antes de pedir más archivos.
- No adjuntar partidas ni datos comerciales CD32 salvo petición concreta para una prueba que los necesite. No hace falta volver a adjuntar C01 ni las cinco poses: ya están versionadas.
