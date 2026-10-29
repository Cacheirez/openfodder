# H5.6 — cierre al pulsar Save

29-10-2026, plan 2.58. Miguel confirma que ahora puede cambiar las opciones. Nuevo fallo: tras cambiarlas, al pulsar **Save** el programa se cierra **antes de mostrar KEEP/REVERT**. No atribuirlo al antiguo clic repetido ni declarar aceptadas las opciones completas. Escenas siguen aceptadas.

## Estado del diagnóstico

La fixture actual de métodos reales de menú/INI/ventana y dispatcher de ratón/GUI pasa localmente con ASan/UBSan. Simula SDL y no ejecuta toda la ventana ni el dibujo de confirmación reales. Por tanto, **no reproduce ni descarta el fallo comunicado; causa y reparación pendientes**. Save entra en captura de ventana, aplicación de preview, recaptura y confirmación; la escritura del INI sucede después de KEEP cuando hay cambios de presentación. No afirmar que el archivo INI cause el cierre sin evidencia.

Se incorpora instrumentación optativa `OPENFODDER_OPTIONS_TRACE`: marcas vaciadas inmediatamente en stderr, sin rutas ni contenido de configuración/partidas. Distingue entrada a Save, captura, aplicación, confirmación pendiente, comienzo/fin de dibujo, escritura INI y commit. `PROBAR_OPCIONES_H5.cmd` la activa y conserva `H5_OPCIONES.log`, como ya hacía con la salida general. No se modifica la transacción ni se anuncia un arreglo. La huella de la puerta de menú se actualiza únicamente para esta instrumentación; las dos llamadas de fade y su posición siguen comprobadas contra la base.

## Próxima prueba manual, cuando haya paquete propio verificado

Usar el paquete de este incremento (no el anterior 30ba0ec para obtener las marcas nuevas), extraído en carpeta nueva. Ejecutar `PROBAR_OPCIONES_H5.cmd`, cambiar las mismas opciones y pulsar Save. Si vuelve a cerrar, conservar `H5_OPCIONES.log` y comunicar las opciones cambiadas. El código de salida y las últimas marcas permitirán distinguir preview de dibujo. No pedir repetir escenas aceptadas ni publicar automáticamente ningún archivo privado. No hay acceso físico al Windows de Miguel.

Conservar también versión exacta del paquete probado. No se considera resuelta la incidencia por pasar CI ni por añadir un registro. KEEP significa conservar el cambio; REVERT, restaurarlo. Caducidad de 15 segundos y persistencia siguen pendientes de poder completar este recorrido real.
