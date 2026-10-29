# H5.6 — cierre al pulsar Save

29-10-2026, plan 2.59. Miguel confirma que ahora puede cambiar las opciones. Nuevo fallo: tras cambiarlas, al pulsar **Save** el programa se cierra **antes de mostrar KEEP/REVERT**. No atribuirlo al antiguo clic repetido ni declarar aceptadas las opciones completas. Escenas siguen aceptadas.

## Causa reproducida y corrección 2.59

La confirmación nueva decía `KEEP CHANGES? 15`. La ruta real `String_Print` convierte `?` en el fotograma 54 (0x24 + posición 18 de la tabla especial). Las fuentes Briefing PC (`stru_42928`) y Amiga (`stru_A6DD8`) tienen solo 37 fotogramas. `Sprite_Get_Sheet` rechaza el 54 y devuelve nullptr; `GUI_Draw_Frame_8` lo desreferencia. La reproducción local con las funciones reales y los tamaños derivados de las tablas originales produce:

```
::warning::Invalid sprite sheet/frame: type=0 frame=54 available=37
runtime error: member access within null pointer of type 'const struct sSpriteSheet'
```

Corrección acotada: la confirmación pasa a `KEEP CHANGES 15`, usando solo glifos disponibles. No se cambia la fuente original, tablas, buscador, raster ni sus límites. Se añade `check_options_font.py`, también CTest Windows/Linux, que compila las funciones reales de texto, dibujo GUI y consulta de sprite con los tamaños reales de ambas tablas. Comprueba el texto extraído directamente de Draw, cuenta atrás 0..15 y KEEP/REVERT. La prueba falla antes y pasa después con ASan/UBSan. No ejecuta todo SDL ni usa arte comercial; demuestra esta ruta concreta, no la interacción física de Miguel. Si todavía cerrase en Windows, usar el registro para investigar otra causa.

La fixture anterior de transacción omitía el dibujo de la confirmación: por eso pasaba sin detectar el error. Se conserva, junto a la nueva cobertura. El primer incremento 2.58 solo añadió diagnóstico; su texto histórico no es el estado final. `OPENFODDER_OPTIONS_TRACE` conserva marcas vaciadas a stderr sin rutas ni contenidos privados. El lanzador lo activa y guarda `H5_OPCIONES.log`. Las llamadas de fade y su posición siguen comprobadas contra la base; la huella de menú cambia únicamente por el texto revisado además de la instrumentación anterior.

## Próxima prueba manual, cuando haya paquete propio verificado

Usar el paquete de este incremento (no el anterior 30ba0ec para obtener las marcas nuevas), extraído en carpeta nueva. Ejecutar `PROBAR_OPCIONES_H5.cmd`, cambiar las mismas opciones y pulsar Save. Si vuelve a cerrar, conservar `H5_OPCIONES.log` y comunicar las opciones cambiadas. El código de salida y las últimas marcas permitirán distinguir preview de dibujo. No pedir repetir escenas aceptadas ni publicar automáticamente ningún archivo privado. No hay acceso físico al Windows de Miguel.

Conservar también versión exacta del paquete probado. La causa de código está corregida y cubierta; aceptación física pendiente. KEEP significa conservar el cambio; REVERT, restaurarlo. Caducidad de 15 segundos y persistencia siguen pendientes de poder completar este recorrido real.
