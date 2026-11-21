# Protagonistas completos — hito autorizado el 21-11-2026

Miguel solicita sustituir la detección caso a caso por investigación de todos los estados del motor y modernizar después todos los sprites/estados de los soldados protagonistas, sin pedir aprobación adicional hasta completar el alcance. No usar subagentes ni cambiar de modelo. No se declara aceptación visual de Miguel por autoría automática o CI.

La autorización cubre producción del arte de protagonistas que falte, en estilo C01, y decisiones técnicas necesarias para integrarlo de forma sistemática. Se reutiliza lo válido; una dirección/familia por microbloque artístico y commits/relevo tras cada bloque. No se detiene en revisiones parciales rutinarias. Los límites de permisos, plataforma, dos hipótesis sin progreso, errores reales y herramientas siguen vigentes.

## Ruta del hito

1. **R1 catálogo de fuente — AUTORIZADO, activo.** Enumerar selectores, estados, tablas y variantes CF1; distinguir cuerpos, invisibles, asociados y entradas no seleccionadas. Un catálogo estático antiguo no basta para probar alcanzabilidad. Registrar los huecos frente al arte real.
2. **R2 resolución sistemática — AUTORIZADO, depende de R1.** Separar pose visible e identidad/estado de animación, validar recurso nativo y evitar cientos de claves por colores no usados o por estado que no cambia la imagen. Eliminar retornos por recursos asociados válidos con una composición ordenada verificable, sin considerar válido lo desconocido.
3. **R3 completar arte — AUTORIZADO, depende del contrato R1/R2.** Todas las poses de protagonistas que falten, incluidas agua, desangrado, muerte, entrada/ocultación y final de fase; estilo C, sin reflejar ni inventar estados. Revisión interna y validación por microbloques sin pedir autorización por pose.
4. **R4 integrar conjunto completo — AUTORIZADO.** Todos los estados legítimos del catálogo tienen arte o una decisión invisible verificada. Classic opcional independiente; orden/oclusiones/Save-Restore, bordes, múltiples soldados, sombras, memoria, SDL y errores reales intactos. No dibujar HD encima de una captura clásica final.
5. **R5 comprobación de cierre — AUTORIZADO.** Cobertura automática contra el catálogo de fuente, pruebas negativas/composición/presupuesto, Windows/Linux, sanitizadores pertinentes, H3 original 11/11.361 y CI. Preparar resultado jugable; registrar límites de CD32/GPU/datos disponibles y aceptación humana pendiente.

No se abre la fase B ni se crean escenarios/enemigos/vehículos nuevos, scroll o 16:9. Las poses del soldado al entrar en un vehículo sí pertenecen al hito; el vehículo como familia artística queda fuera. Los elementos asociados se verifican cuando condicionan continuidad; no se inventan sombras.

## Hechos iniciales

El motor enumera estados None/Hit/Hit2/Hit3/Die1/Die2/Die3/Die4/Die5/Slide1/Slide2/Slide3/Vehicle_Enter/Vehicle_Inside. La tabla humana tiene nueve grupos de ocho direcciones, más rutas directas fuera de ella. El inventario previo declara 159 pares hoja/frame humanos Amiga y 158 PC, pero incluye filas cuyo selector puede no alcanzar y no incluye todas las rutas especiales. El grupo etiquetado `Death-3` se usa también en el movimiento según `word_3AA1D`; la etiqueta no es una clasificación suficiente.

El herido prolongado `Die5` selecciona explícitamente 0x21 y alterna F0/F1 al crear sangre; no es un frame de la familia 0x28–0x2F ya integrada. Las claves anteriores incluyen animación y los 255 colores efectivos, lo que fragmenta poses idénticas y demuestra que añadir hashes sueltos no proporciona cobertura de estados.

CD32 sigue siendo el destino principal. Tablas retail Amiga, variante The One y PC se auditarán por separado. Datos comerciales y capturas fuera de GitHub; los directorios de pruebas localizados contienen demos públicas. No se promete prueba jugable CD32 sin sus recursos.
