# Soldados enemigos completos — A3

Miguel autoriza expresamente el 22-11-2026 la modernización completa de soldados enemigos hasta su revisión jugando. Protagonistas aceptados y conservados; no se autoriza B, escenarios, civiles en general, vehículos, scroll ni 16:9. El jefe tipo106 pertenece al alcance enemigo aunque su controlador sea el de rehenes. PR #1 abierta, borrador y sin fusionar, rama modernization/windows-foundation.

## E1.1 — inventario inicial de fuente comprobado

[Catálogo reproducible](evidence/enemy-state-catalog-v1.json), generado por `tools/modernization/inventory_enemy_states.py`; ocho pruebas de límites en `test_enemy_state_catalog.py`. PC y Amiga: 423 contratos por formato, 228 filas de metadatos distintas. Cuenta por tipo: 5/36, 182 cada uno; jefe106, 52; sombra22, tres (creación8D/F2 y actualización97/F0-F1, propietarios5/36 explícitos); marcador41/C4, cuatro asociaciones. Son límites iniciales conservadores, no 423 imágenes distintas ni declaración de arte completo.

- Tabla enemiga de nueve grupos: marcha, daño direccional y balístico, modo cero, agua, granada, apuntado, cohete y caída. Las filas72..79 no heredan la prueba de latencia del protagonista: el selector depende de estado temporal compartido.
- El controlador de lanzacohetes fuerza F2 después de seleccionar; no se aplica por semejanza el ciclo del arma del jugador.
- Sangrado irrecuperable63/F0-F1, hundimiento7A, deslizamientoA7, entradaCC y marcadores7C quedan explícitos. CC y7C exigen raster nativo verificado; ningún cuerpo ficticio ni vínculo automático.
- Un enemigo que vigila un rehén puede elegir DC/F0. La presencia de esa hoja no moderniza por extensión una familia de civiles.
- El jefe106 recorre D8/D9 (dirección × tres frames), DA/F0-F2 e invisible7C/F0; marcador C4 independiente. No crea sombra de suelo en su controlador: no inventarla.
- Un enemigo del mapa empieza con persona nativa0 y el controlador cambia a IA después de comprobar daño. La cobertura anterior al primer cambio exige investigación explícita, no una suposición.

El catálogo conserva metadatos, rutas y hashes de funciones nativas. No contiene bitmaps comerciales. La igualdad de metadatos solo propone reutilización: no demuestra equivalencia artística ni de identidad. Los cuatro recursos enemigos del experimento previo son maestros disponibles, no aceptación global.

## Próximo microbloque único

E1.2 comprobado: [límites y referencias](evidence/enemy-source-native-audit.json). Catálogo revisión3: 483 filas Amiga/482 PC, de las cuales 342/341 con productor (incluido límite conservador del daño anterior a IA) y 141 declaradas por formato. Once pruebas PASS; 965 referencias privadas, cuatro bancos por SHA, 310 rasters distintos. Los recursos posteriores vacíos de la demo Amiga conservan ausencia nativa; no prueban ausencia de un jefe en el juego comercial. No se ha modificado el motor ni la simulación.

E2.1 comprobado: dirección2, 44/F0-F2, con F1 anterior conservado y F0/F2 nuevos; [evidencia](evidence/enemy-walk-d2.json). Registro de arte disponible: seis poses/doce activos, sin integrarlos todavía como cobertura completa.

E2.2 comprobado: dirección3,45/F0-F2; F1 anterior intacto, F0/F2 nuevos, tres poses/seis derivados. [Evidencia](evidence/enemy-walk-d3.json). Registro total ocho poses/dieciséis activos.

E2.3 comprobado: dirección4,46/F0-F2; tres maestros y seis derivados nuevos, marcha atrás hacia arriba con alternancia nativa de piernas. [Evidencia](evidence/enemy-walk-d4.json). Registro total once poses/veintidós activos.

E2.4 siguiente: marcha enemiga dirección5,47/F0-F2. Un solo grupo de tres frames, validación y commit antes de otra dirección. No se altera ni se activa parcialmente el diagnóstico aceptado de protagonistas.

## Recorrido autorizado hasta revisión

1. E1: inventario cerrado de estados, variantes, propietarios y firmas nativas.
2. E2: diseño y producción por una dirección/familia por microbloque; reutilizar maestros válidos con trazabilidad y conservar originales/derivados.
3. E3: integrar catálogo explícito de cuerpos y sombras en compositor ordenado; protagonistas y enemigos modernos con identidad estable.
4. E4: comprobaciones focalizadas, H3 independiente y CI Windows/Linux; medir publicaciones y retornos por errores reales, conservar clásico y recuperación.
5. E5: diagnóstico local congelado con hashes y revisión visual/jugable de Miguel. No inventar aceptación a partir de contadores.

IA, simulación, RNG, colisiones, reloj lógico, dirección/frame y referencias clásicas intactos. CD32 es el destino principal; metadatos Amiga/TheOne contrastados no equivalen a ejecutar campaña comercial CD32. Pruebas aún no ejercitadas permanecen pendientes.
