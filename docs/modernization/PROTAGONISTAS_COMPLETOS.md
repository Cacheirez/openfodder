# Protagonistas completos — hito autorizado el 21-11-2026

Miguel solicita sustituir la detección caso a caso por investigación de todos los estados del motor y modernizar después todos los sprites/estados de los soldados protagonistas, sin pedir aprobación adicional hasta completar el alcance. No usar subagentes ni cambiar de modelo. No se declara aceptación visual de Miguel por autoría automática o CI.

La autorización cubre producción del arte de protagonistas que falte, en estilo C01, y decisiones técnicas necesarias para integrarlo de forma sistemática. Se reutiliza lo válido; una dirección/familia por microbloque artístico y commits/relevo tras cada bloque. No se detiene en revisiones parciales rutinarias. Los límites de permisos, plataforma, dos hipótesis sin progreso, errores reales y herramientas siguen vigentes.

## Ruta del hito

1. **R1 catálogo de fuente — COMPLETADO.** Enumerar selectores, estados, tablas y variantes CF1; distinguir cuerpos, invisibles, asociados y entradas no seleccionadas. Un catálogo estático antiguo no basta para probar alcanzabilidad. Registrar los huecos frente al arte real.
2. **R2 resolución sistemática — COMPROBADO LOCALMENTE, CI pendiente.** Separar pose visible e identidad/estado de animación, validar recurso nativo y evitar cientos de claves por colores no usados o por estado que no cambia la imagen. Eliminar retornos por recursos asociados válidos con una composición ordenada verificable, sin considerar válido lo desconocido.
3. **R3 completar arte — AUTORIZADO, activo.** Todas las poses de protagonistas que falten, incluidas agua, desangrado, muerte, entrada/ocultación y final de fase; estilo C, sin reflejar ni inventar estados. Revisión interna y validación por microbloques sin pedir autorización por pose.
4. **R4 integrar conjunto completo — AUTORIZADO.** Todos los estados legítimos del catálogo tienen arte o una decisión invisible verificada. Auditar también las transiciones de presentación y las causas de recuperación, no solo los slots de arte. Classic opcional independiente; orden/oclusiones/Save-Restore, bordes, múltiples soldados, sombras, memoria, SDL y errores reales intactos. No dibujar HD encima de una captura clásica final.
5. **R5 comprobación de cierre — AUTORIZADO.** Cobertura automática contra el catálogo de fuente, pruebas negativas/composición/presupuesto, Windows/Linux, sanitizadores pertinentes, H3 original 11/11.361 y CI. Preparar resultado jugable; registrar límites de CD32/GPU/datos disponibles y aceptación humana pendiente.

No se abre la fase B ni se crean escenarios/enemigos/vehículos nuevos, scroll o 16:9. Las poses del soldado al entrar en un vehículo sí pertenecen al hito; el vehículo como familia artística queda fuera. Los elementos asociados se verifican cuando condicionan continuidad; no se inventan sombras.

## Hechos iniciales

El motor enumera estados None/Hit/Hit2/Hit3/Die1/Die2/Die3/Die4/Die5/Slide1/Slide2/Slide3/Vehicle_Enter/Vehicle_Inside. La tabla humana tiene nueve grupos de ocho direcciones, más rutas directas fuera de ella. El inventario previo declara 159 pares hoja/frame humanos Amiga y 158 PC, pero incluye filas cuyo selector puede no alcanzar y no incluye todas las rutas especiales. El grupo etiquetado `Death-3` se usa también en el movimiento según `word_3AA1D`; la etiqueta no es una clasificación suficiente.

El herido prolongado `Die5` selecciona explícitamente 0x21 y alterna F0/F1 al crear sangre; no es un frame de la familia 0x28–0x2F ya integrada. Las claves anteriores incluyen animación y los 255 colores efectivos, lo que fragmenta poses idénticas y demuestra que añadir hashes sueltos no proporciona cobertura de estados.

CD32 sigue siendo el destino principal. Tablas retail Amiga, variante The One y PC se auditarán por separado. Datos comerciales y capturas fuera de GitHub; los directorios de pruebas localizados contienen demos públicas. No se promete prueba jugable CD32 sin sus recursos.

## R2 contrato de resolución

`OPENFODDER_PLAYER_CATALOG=1`, modo híbrido y manifiesto v3 activan exclusivamente el catálogo. V1/v2 y el clásico conservan sus rutas. `generate_player_pose_table.py --check` fija 385 contratos de fuente. Cada pose conserva formato, tipo, hoja/frame, geometría, segmento y paleta; comprueba además el SHA-256 del archivo fuente completo y la firma de índices/transparencias nativos. Los 14 estados lógicos válidos no generan arte adicional cuando mantienen la misma pose. Los colores de entradas de paleta no usadas tampoco crean otra pose. Se mantienen los controles de fundido y el orden/oclusiones originales.

Los elementos asociados solo conservan su dibujo clásico con procedencia, archivo completo conocido, extensión y geometría comprobados. Los cuerpos protagonistas y las sombras propias tienen entradas explícitas. Una fuente/firma desconocida, datos truncados, geometría inválida o fallo SDL siguen causando recuperación segura. Los marcadores 0x7C deben demostrar ausencia de escrituras, no reciben un cuerpo ficticio.

`prepare_player_catalog.py` reconstruye **todos** los slots desde los buffers privados retenidos, aunque el replay no haya seleccionado cada frame, y genera referencias nativas privadas, firmas y huecos de arte. No publica bitmaps comerciales. El manifiesto distingue `complete=false` de desarrollo y `complete=true`, que exige las 385 entradas y arte 8×/12× en todas las visibles. Los recursos conocidos proceden ahora de PC Format y Amiga The One; otros archivos, incluido CD32 retail, requieren verificar sus firmas antes de aceptarlos. No se considera probado ese destino por compartir tablas.

[Pruebas y candidato local](evidence/player-native-catalog-r2.json). Los 111 maestros existentes cubren 222 slots visibles y cuatro invisibles verificados. Faltan 159 entradas entre formatos, incluidas cuatro de sombra independiente: no son 159 dibujos nuevos independientes. Al hacer explícitas las sombras propias y el cadáver flotante, el candidato incompleto publica 3.255 escenas del replay y deja 1.302 faltantes. Es un diagnóstico de cobertura, **no un ejecutable entregado ni una mejora de continuidad aceptada**. R3 completa el arte; R4/R5 integran, miden y preparan el resultado jugable.

## R3 progreso del arte

- **0x21/F0–F1 comprobado (21-11):** dos maestros de desangrado/daño con override; cuatro derivados, cajas nativas exactas. PASS 64 casos de Window/SDL por plataforma con sanitizadores. Catálogo 113 maestros; 230/385 entradas del candidato, 155 pendientes. Sin activar el lote incompleto ni atribuir aceptación visual de Miguel. [Evidencia](evidence/player-pose-21.json). Siguiente dirección: 0x20, con asimetría PC/Amiga explícita.

- **0x20/F0–F1 comprobado:** dos maestros/cuatro derivados; F0 PC/Amiga y F1 solo Amiga. PASS 48 casos Window/SDL por sistema con sanitizadores; activo previo intacto. Candidato 252 activos, 233/385 entradas, 152 pendientes. [Evidencia](evidence/player-pose-20.json). Siguiente dirección 0x23; 0x22 ya cubierta.

- **0x23 comprobado:** 2 maestros, 4 derivados; Daño con override, dirección 3. PASS 64 casos Window/SDL por sistema con sanitizadores; activos/vínculos previos intactos. Candidato 256 activos, 237/385 entradas, 148 pendientes. [Evidencia](evidence/player-pose-23.json). Siguiente: R3 — daño con override dirección 4, 0x24/F0–F1.

- **0x24 comprobado:** 2 maestros, 4 derivados; Daño con override, dirección 4. PASS 64 casos Window/SDL por sistema con sanitizadores; activos/vínculos previos intactos. Candidato 260 activos, 241/385 entradas, 144 pendientes. [Evidencia](evidence/player-pose-24.json). Siguiente: R3 — daño con override dirección 5, 0x25/F0–F1.

## Criterios de integración R4 pendientes

385/385 entradas no bastan por sí solas para declarar continuidad. Contrastar sistemáticamente los guardas de `TryRenderMissionHD`: fundido/paleta, inicio/reinicio, pausa/mapa, callback y final de fase, superficie/escena retenida y estado SDL. Distinguir modos ajenos a la misión y errores reales de transiciones legítimas con protagonistas visibles; resolver estas últimas de forma verificable dentro del hito, sin desactivar protecciones, alterar el reloj ni atribuir aceptación humana. Medir los retornos por motivo y por actor.

Cruzar asimismo cada sombra independiente con la identidad/generación de su dueño y las placas opcionales de los cuerpos: comprobar que no se duplica una sombra cuando ambas rutas están presentes. Conservar orden, recorte/altura, agua, oclusiones y anclajes nativos. Las familias nuevas no reciben automáticamente una sombra de suelo por parecerse a una pose normal.

- **0x25 comprobado:** 2 maestros, 4 derivados; Daño con override, dirección 5. PASS 64 casos Window/SDL por sistema con sanitizadores; activos/vínculos previos intactos. Candidato 264 activos, 245/385 entradas, 140 pendientes. [Evidencia](evidence/player-pose-25.json). Siguiente: R3 — daño con override dirección 6, 0x26/F0–F1.

- **0x26 comprobado:** 2 maestros, 4 derivados; Daño con override, dirección 6. PASS 64 casos Window/SDL por sistema con sanitizadores; activos/vínculos previos intactos. Candidato 268 activos, 249/385 entradas, 136 pendientes. [Evidencia](evidence/player-pose-26.json). Siguiente: R3 — daño con override dirección 7, 0x27/F0–F1.

- **0x27 comprobado:** 2 maestros, 4 derivados; Daño con override, dirección 7; grupo completo. PASS 64 casos Window/SDL por sistema con sanitizadores; activos/vínculos previos intactos. Candidato 272 activos, 253/385 entradas, 132 pendientes. [Evidencia](evidence/player-pose-27.json). Siguiente: R3 — locomoción baja dirección 0, 0x30/F0–F2; verificar reutilización de F0 con 0xB0 y completar F1/F2.

- **0x30 comprobado:** 2 maestros, 4 derivados; Locomoción baja 0x30, tres frames con F0 reutilizado. PASS 96 casos Window/SDL por sistema con sanitizadores; activos/vínculos previos intactos. Candidato 276 activos, 259/385 entradas, 126 pendientes. [Evidencia](evidence/player-pose-30.json). Siguiente: R3 — locomoción baja dirección 1, 0x31/F0–F2.

## Reutilización nativa explícita de R3

`player-pose-reuse.json` declara únicamente revisiones concretas dentro del catálogo. El primer vínculo es 0x30/F0 → B0/F0: mismo cuerpo y metadatos completos PC/Amiga; el maestro C01 compacto sin arma sirve también al contexto de locomoción baja. El generador comprueba la tabla y el constructor contrasta las firmas de raster de ambos usos con recursos privados retenidos. No se incorporan automáticamente otros candidatos ni las 53 referencias desconocidas. Pruebas negativas rechazan poses desconocidas, geometría distinta y duplicados.

El contrato permite compartir RGBA solo cuando la revisión del contexto lo acredita; `master-reexport` conserva la imagen original y prepara derivados propios. En 0x30/F0 se usa este último: PNG idéntico a B0, proyección ajustada para locomoción, B0 intacto. Hoja/frame, acción, altura, reloj y política de sombra siguen siendo los originales. Las placas opcionales no se habilitan por semejanza. F1/F2 de 0x30 son maestros nuevos; el perfil de F2 se ajustó dentro de la caja nativa para mantener escala sin desplazar su centro o apoyo. [Pruebas y colocación final](evidence/player-pose-30.json). Los recuentos de maestro indican **poses con maestro disponible**, incluidas reutilizaciones explícitas, no necesariamente imágenes originales distintas.

- **Corrección de coherencia 0x30:** derivados propios de F0 desde el mismo maestro B0, sin nueva generación ni cambios de B0. Conjunto final 278 activos y 259/385 entradas. PASS 96 casos por sistema con sanitizadores; fuente de maestro y raster nativo iguales, proyección RGBA separada y explícita. Tabla nativa generada con independencia del arte; candidatos y catálogo completo siguen verificando su integridad. [Evidencia actualizada](evidence/player-pose-30.json).

- **0x31 comprobado:** 3 maestros, 6 derivados; Locomoción baja 0x31, tres frames. PASS 96 casos Window/SDL por sistema con sanitizadores; activos/vínculos previos intactos. Candidato 284 activos, 265/385 entradas, 120 pendientes. [Evidencia](evidence/player-pose-31.json). Siguiente: R3 — locomoción baja dirección 2, 0x32/F0–F2; verificar maestros B6/B7 para F0/F1 y completar F2.

## Corrección de alcanzabilidad R3 — 21-11-2026

La investigación inicial conservadora incluía las 24 filas 0x30–0x37 de cada formato. La revisión de sus productores demuestra que pertenecen al modo de pelotón cero: las cinco posiciones de `word_3BED5` solo se escriben con 2; el jugador carga ese valor antes de la selección normal. El reinicio a cero de la variable temporal no constituye una selección humana de ese modo. Las caídas reales seleccionan B0–B7/F0 mediante otra rama. No se crean cuerpos modernos para las siluetas rojas de una rama inactiva.

Se conservan las **385 filas como auditoría de fuente**, con una marca explícita de producción: **337 entradas requeridas** (165 cuerpos Amiga, 164 PC, cuatro ocultas y cuatro sombras con propietario), más **48 declaradas sin productor actual**. El contrato completo exige las 337 y rechaza vincular las inactivas; una aparición inesperada conserva la recuperación segura por faltante. La prueba invalida la auditoría si aparece otra referencia/escritura de modo y rechaza expresamente una nueva escritura cero. No cambia el motor ni reduce los requisitos de sus estados reales.

PASS: seis pruebas Python y 15.348 casos de resolución/mutación por sistema con ASan/UBSan; LSan en Linux. Los cinco maestros recientes de 0x30/F1–F2 y 0x31/F0–F2 coinciden con B1–B5 en tabla y raster privado: se integrarán mediante revisiones explícitas, sin generar imágenes nuevas. Tras ello quedan 35 cuerpos reales por crear y las dos sombras independientes. Los recuentos anteriores de 385 entradas se conservan como resultados históricos del inventario conservador. [Evidencia y límites](evidence/player-pose-reachability.json).
