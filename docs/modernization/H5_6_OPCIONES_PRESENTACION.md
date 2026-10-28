# H5.6 — primer incremento de opciones de presentación

Preparación del 28-10-2026. Implementación pendiente de aceptar visualmente la pausa de 63c4d6f y cerrar Linux global.

## Punto de partida

OptionsMenu.cpp ya ofrece Window mode, Window scale e Integer scaling, con snapshot para cancelar; Parameters.cpp guarda opciones en INI. Window.cpp contiene el cambio de modo y ToggleVSync. Se ampliará esa estructura, evitando un segundo menú y sin alterar simulación o referencias H3.

## Primer corte implementable

- Separar presentación «Clásica» y «Ajustada a ventana» de la selección artística. Ajustada no significa arte HD: conserva los gráficos originales, aspecto y bandas existentes.
- Persistir la preferencia, con Clásica como valor predeterminado y recuperación ante valor ausente o inválido. Mantener los lanzadores de prueba como overrides explícitos.
- Mostrar las condiciones actuales del ajuste: ventana, ratón absoluto desbloqueado y escenas admitidas. Mantener retorno coherente de dibujo y entrada al clásico ante incompatibilidad.
- Integrar aplicar/cancelar con el snapshot del menú. Para cambios de modo o tamaño, probar temporalmente, confirmar en 15 segundos y restaurar si se cancela, expira o falla SDL. Persistir solo tras confirmación. El contador usa tiempo real, independiente de ticks de simulación.
- Probar carga antigua, preferencias inválidas, cancelación, expiración, fallo de aplicación y correspondencia dibujo/ratón tras cambiar y restaurar. Comparar con H3 original y conservar F11.

## Cortes posteriores de H5.6

Enumeración de monitores/modos admitidos; resolución de ventana y pantalla sin bordes; exclusiva solo tras validación específica. Después, escala de interfaz, sincronización y límite de FPS separados de la velocidad del juego. No anunciar todas estas opciones como implementadas por el primer corte.

## Salida hacia arte

Con presentación y retorno validados, evaluar densidad maestra del arte C (incluido cursor y hotspot), comparando nitidez y memoria hasta 4K. No producir una colección de sprites por resolución de monitor ni fijar aún 2x/4x. Base clásica, mejoras y C01 se conservan. PR abierto en borrador y sin fusionar.
