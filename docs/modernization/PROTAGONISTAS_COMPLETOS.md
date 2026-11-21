# Protagonistas completos — hito autorizado el 21-11-2026

Miguel solicita sustituir la detección caso a caso por investigación de todos los estados del motor y modernizar después todos los sprites/estados de los soldados protagonistas, sin pedir aprobación adicional hasta completar el alcance. No usar subagentes ni cambiar de modelo. No se declara aceptación visual de Miguel por autoría automática o CI.

La autorización cubre producción del arte de protagonistas que falte, en estilo C01, y decisiones técnicas necesarias para integrarlo de forma sistemática. Se reutiliza lo válido; una dirección/familia por microbloque artístico y commits/relevo tras cada bloque. No se detiene en revisiones parciales rutinarias. Los límites de permisos, plataforma, dos hipótesis sin progreso, errores reales y herramientas siguen vigentes.

## Ruta del hito

1. **R1 catálogo de fuente — COMPLETADO.** Enumerar selectores, estados, tablas y variantes CF1; distinguir cuerpos, invisibles, asociados y entradas no seleccionadas. Un catálogo estático antiguo no basta para probar alcanzabilidad. Registrar los huecos frente al arte real.
2. **R2 resolución sistemática — COMPROBADO LOCALMENTE, CI pendiente.** Separar pose visible e identidad/estado de animación, validar recurso nativo y evitar cientos de claves por colores no usados o por estado que no cambia la imagen. Eliminar retornos por recursos asociados válidos con una composición ordenada verificable, sin considerar válido lo desconocido.
3. **R3 completar arte — AUTORIZADO, activo.** Todas las poses de protagonistas que falten, incluidas agua, desangrado, muerte, entrada/ocultación y final de fase; estilo C, sin reflejar ni inventar estados. Revisión interna y validación por microbloques sin pedir autorización por pose.
4. **R4 integrar conjunto completo — AUTORIZADO.** Todos los estados legítimos del catálogo tienen arte o una decisión invisible verificada. Classic opcional independiente; orden/oclusiones/Save-Restore, bordes, múltiples soldados, sombras, memoria, SDL y errores reales intactos. No dibujar HD encima de una captura clásica final.
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
