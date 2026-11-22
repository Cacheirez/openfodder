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

E2.4 comprobado: dirección5,47/F0-F2; tres maestros/seis derivados nuevos, vista diagonal hacia arriba-derecha sin reflejos. [Evidencia](evidence/enemy-walk-d5.json). Registro total catorce poses/veintiocho activos; doce poses de marcha en cuatro direcciones.

E2.5 comprobado: dirección6,48/F0-F2; tres maestros/seis derivados nuevos, orientación derecha y proporciones de casco corregidas antes de publicar. [Evidencia](evidence/enemy-walk-d6.json). Registro total diecisiete poses/treinta y cuatro activos; quince poses de marcha en cinco direcciones.

E2.6 comprobado: dirección7,49/F0-F2; tres maestros/seis derivados nuevos, frente diagonal abajo-derecha y alternancia de pasos. [Evidencia](evidence/enemy-walk-d7.json). Registro total veinte poses/cuarenta activos; dieciocho poses de marcha en seis direcciones.

E2.7 comprobado: dirección 0, 42/F0-F2; tres maestros/seis derivados nuevos, cuerpo de frente hacia abajo. [Evidencia](evidence/enemy-walk-d0.json). Registro total 23 poses/46 activos;21 poses de marcha en siete direcciones.

E2.8 comprobado: dirección1,43/F0-F2; tres maestros/seis derivados nuevos, diagonal abajo-izquierda desde sus referencias. [Evidencia](evidence/enemy-walk-d1.json). Marcha completa: 8×3, 24 poses/48 derivados. Registro total 26 poses/52 activos; los cuatro paquetes enemigos anteriores siguen exactos. Source intacto respecto a 1b40748.

E2.9 siguiente: auditar candidatos de reutilización explícita por raster nativo y semántica, junto al presupuesto combinado, antes de las familias restantes. No añadir vínculos automáticamente por una coincidencia ni modernizar filas solo declaradas. Hito enemigo en curso, no integrado ni aceptado jugando.

Condición de E3: respetar el presupuesto existente de 64 MiB de activos. Medir el manifiesto combinado; reutilizar recursos equivalentes explícitos y organizar densidades cargadas sin elevar el límite ni perder verificación. La producción actual no activa ni cambia ese presupuesto.

## Recorrido autorizado hasta revisión

1. E1: inventario cerrado de estados, variantes, propietarios y firmas nativas.
2. E2: diseño y producción por una dirección/familia por microbloque; reutilizar maestros válidos con trazabilidad y conservar originales/derivados.
3. E3: integrar catálogo explícito de cuerpos y sombras en compositor ordenado; protagonistas y enemigos modernos con identidad estable.
4. E4: comprobaciones focalizadas, H3 independiente y CI Windows/Linux; medir publicaciones y retornos por errores reales, conservar clásico y recuperación.
5. E5: diagnóstico local congelado con hashes y revisión visual/jugable de Miguel. No inventar aceptación a partir de contadores.

IA, simulación, RNG, colisiones, reloj lógico, dirección/frame y referencias clásicas intactos. CD32 es el destino principal; metadatos Amiga/TheOne contrastados no equivalen a ejecutar campaña comercial CD32. Pruebas aún no ejercitadas permanecen pendientes.

## Revisión de identidad — petición de Miguel, 22-11

Miguel considera que los enemigos se parecen demasiado a los aliados; propone barba y un distintivo, observando rojo en el cuello original. Se ha verificado color rojizo en esa franja, sin atribuir con certeza una prenda al bitmap. Propuesta local sin integrar: casco liso gris verdoso, uniforme gris oliva, cuello rojo teja corto y barba corta como rasgo secundario. El casco/uniforme conservan reconocimiento desde atrás. [Muestra y recuperación](evidence/enemy-identity-proposal-v1.json). Esperar la elección artística de Miguel antes de extender diseño; las 24 poses anteriores se conservan. No se anula el hito completo autorizado.

E1.3 comprobado: catálogo revisión4, 340 contratos producidos Amiga/339 PC y 143 solo declarados por formato; 69/F2 no lo produce el controlador de daño acotado a 0/1. Once pruebas PASS, sin cambios en Source ni arte activo. [Evidencia](evidence/enemy-source-bounds-r4.json). E2.9 está en curso y pendiente de cierre; sus candidatos preliminares de reutilización no se han convertido en vínculos.

## Identidad E01/v2 aprobada —22-11

Miguel acepta expresamente la propuesta completa: casco y uniforme gris verdoso, cuello rojo teja y barba corta. [Decisión y SHA](evidence/enemy-identity-approved-v2.json) · [maestro](../../assets/modernization/enemy-identity-v2/). No requiere otra aprobación rutinaria para propagarla por el hito autorizado. Se preservan los 26 maestros verdes versión 1; nuevos paquetes/registros separados para evitar mezcla. La aprobación es de identidad, no una aceptación jugable anticipada.

Siguiente microbloque único E2.V2.0: marcha dirección 0, 42/F0-F2; reutilizar exactamente F1 aprobado y editar F0/F2 manteniendo postura, anclas, orden y tamaños nativos. Validar/exportar 8×/12×, publicar y encadenar otras direcciones/estados. Reutilización y presupuesto (E2.9) siguen pendientes antes del conjunto restante/integración.

## Registro de arte E01/v2

- **E2.V2.0 comprobado:** walk, dirección0, 42/F0,1,2; registro3 poses/6 activos. [Evidencia](evidence/enemy-v2-walk-d0.json). Próximo: E2.V2.1 — adaptar marcha enemiga dirección1, 43/F0-F2, a E01/v2; mantener poses y geometría, validar8×/12× y publicar antes de otra dirección. Continuar dentro del hito completo autorizado.

- **E2.V2.1 comprobado:** walk, dirección1, 43/F0,1,2; registro6 poses/12 activos. [Evidencia](evidence/enemy-v2-walk-d1.json). Próximo: E2.V2.2 — adaptar marcha enemiga dirección 2, 44/F0-F2, a E01/v2; validar 8×/12× y publicar antes de otra dirección. Continuar dentro del hito completo autorizado.

- **E2.V2.2 comprobado:** walk, dirección2, 44/F0,1,2; registro9 poses/18 activos. [Evidencia](evidence/enemy-v2-walk-d2.json). Próximo: E2.V2.3 — adaptar marcha enemiga dirección 3, 45/F0-F2, a E01/v2; validar 8×/12× y publicar antes de otra dirección. Continuar dentro del hito completo autorizado.

- **E2.V2.3 comprobado:** walk, dirección3, 45/F0,1,2; registro12 poses/24 activos. [Evidencia](evidence/enemy-v2-walk-d3.json). Próximo: E2.V2.4 — adaptar marcha enemiga dirección 4, 46/F0-F2, a E01/v2; validar 8×/12× y publicar antes de otra dirección. Continuar dentro del hito completo autorizado.

- **E2.V2.4 comprobado:** walk, dirección4, 46/F0,1,2; registro15 poses/30 activos. [Evidencia](evidence/enemy-v2-walk-d4.json). Próximo: E2.V2.5 — adaptar marcha enemiga dirección 5, 47/F0-F2, a E01/v2; validar 8×/12× y publicar antes de otra dirección. Continuar dentro del hito completo autorizado.

- **E2.V2.5 comprobado:** walk, dirección5, 47/F0,1,2; registro18 poses/36 activos. [Evidencia](evidence/enemy-v2-walk-d5.json). Próximo: E2.V2.6 — adaptar marcha enemiga dirección 6, 48/F0-F2, a E01/v2; validar 8×/12× y publicar antes de otra dirección. Continuar dentro del hito completo autorizado.

- **E2.V2.6 comprobado:** walk, dirección6, 48/F0,1,2; registro21 poses/42 activos. [Evidencia](evidence/enemy-v2-walk-d6.json). Próximo: E2.V2.7 — adaptar marcha enemiga dirección 7, 49/F0-F2, a E01/v2; validar 8×/12× y publicar. Después retomar E2.9, reutilización y presupuesto, antes de restantes estados e integración.

- **E2.V2.7 comprobado:** walk, dirección7, 49/F0,1,2; registro24 poses/48 activos. [Evidencia](evidence/enemy-v2-walk-d7.json). Próximo: E2.9 — medir reutilización nativa verificable y presupuesto combinado de protagonistas/enemigos, manteniendo el límite de 64 MiB; fijar organización de carga antes de restantes estados e integración. Continuar autónomamente dentro del hito autorizado.

## E2.9 — reutilización y presupuesto comprobados

- **E2.9 comprobado:** 268 poses corporales opacas distintas por clave; once candidatos de reutilización nativa explícitos, sin vínculos automáticos. Estimación combinada sin ahorros: 81.404.544 bytes a ambas densidades (excede 64 MiB), 56.356.992 a 12×; con reserva de tres sombras, quedan 10.364.800 bytes. Cinco pruebas del informe PASS. Decisión: cargar solo la densidad elegida, sin elevar el límite; implementación PENDIENTE. [Medición reproducible](evidence/enemy-reuse-budget-v1.json).

E3.D — implementar catálogo de densidad explícita (8× o 12×), con preflight de 64 MiB y rechazo seguro de densidad incorrecta; mantener manifiestos y candidato de protagonistas previos. Validar el cambio focalizado antes de restantes estados e integración enemiga.

## E3.D — carga por densidad comprobada

- **E3.D comprobado:** carga explícita por densidad, manifiesto4/schema2; versiones anteriores intactas y preflight64 MiB conservado. Windows/Linux: 1.376 casos nuevos de densidad, 15.441 previos de catálogo y cuatro grupos de sombras PASS con ASan/UBSan; LSan Linux PASS. Integración enemiga, H3/CI completa del candidato y aceptación jugando PENDIENTES. [Contrato](CATALOGO_DENSIDAD.md), [evidencia](evidence/enemy-density-loading-v1.json).

E2.G0 — preparar granada enemiga dirección 0, 4A/F0-F2, con identidad E01 aprobada y referencias nativas; validar 8×/12× y publicar antes de otra dirección. Continuar hasta revisión jugando dentro del hito autorizado.

- **E2.G0 comprobado:** pose, dirección0, 4A/F0,1,2; registro27 poses/54 activos. [Evidencia](evidence/enemy-v2-grenade-d0.json). Próximo: E2.G1 — preparar granada enemiga dirección 1, 4B/F0-F2, con identidad E01 y referencias nativas; validar 8×/12× y publicar antes de otra dirección. Continuar hasta revisión jugando dentro del hito autorizado.

## E2.G1 — bloqueo de generación

- **BLOQUEO E2.G1 de plataforma:** ImageGen rechazó la salida de 4B/F0 con HTTP400, moderation_blocked/illicit (output), petición d0b0ba1a-05a9-416c-aa3c-3c603d2441aa. Un intento, sin imagen utilizable y sin reintento/cambio de herramienta o modelo. [Reproducción y recuperación](evidence/enemy-generation-blocked-4b-f0.json). Arte publicado: 27 poses/54 activos, último bloque 6ff562b; carga por densidad 805f426. No hay ejecutable enemigo nuevo. CI de 6ff562b: H6 PASS; Windows/Linux EN CURSO, sin PASS completo.

E2.G1 BLOQUEADO — resolver el rechazo de plataforma antes de retomar granada dirección 1, 4B/F0-F2. Conservar prompt/referencias y 27 poses/54 activos; no sortear el bloqueo ni activar un lote parcial. Requiere intervención sobre la herramienta, no otra aprobación artística.
