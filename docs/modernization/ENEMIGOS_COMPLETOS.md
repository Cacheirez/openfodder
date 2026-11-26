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

## Criterio obligatorio de sombras y cobertura — aclaración de Miguel

- **Criterio de Miguel — sombras y cobertura completa:** enemigos con la misma proyección fija abajo-derecha y luz arriba-izquierda que los protagonistas, independientemente de su orientación, con el mismo apoyo relativo de los pies y ajuste por pose. Cubrir cada estado, dirección/frame y transición producido por la fuente, incluidos reinicios, daño previo a IA y desangrado; registrar ocultos y filas no producidas. Conservar sombras independientes y tratamientos de agua/altura/caída; documentar ausencias nativas sin inventarlas. Inventario disponible no equivale a integración ni aceptación visual completa. [Requisito y fuente](evidence/enemy-shadow-coverage-requirement.json).

Inspección focalizada: propietarios5/36 comparten el controlador nativo de sombras con protagonistas. Los tres estados22/8D-F2 y97-F0/F1 ya están inventariados. Integración y comprobación jugando PENDIENTES; el bloqueo de plataforma E2.G1 continúa sin reintentos.

## E3.T1 — contrato técnico de enemigos

- **E3.T1 comprobado:** tabla nativa enemiga generada desde fuente: 965 contratos, 679 producidos (339 PC/340 Amiga), 286 solo declarados. Roles separados de cuerpo/sombra/asociado y máscaras de persona para daño inicial; cuatro pruebas y control de deriva PASS. Sin captura ni arte nuevo activados. [Evidencia](evidence/enemy-native-table-v1.json).

E3.T2 — conectar catálogo enemigo opt-in, captura de cuerpos y sombras propias, firmas nativas y rechazo de fallos reales; mantener catálogo de desarrollo explícitamente incompleto y protagonistas independientes. Validar en Windows/Linux antes de preparar candidato técnico.

## E3.T2 — integración técnica opt-in

- **E3.T2 comprobado:** catálogo enemigo opt-in y captura de cuerpos/sombras, 679 estados firmables obligatorios; cobertura artística separada. Windows/Linux: 18.284 casos de catálogo/despacho, 2.073 de captura enemiga, 15.441 de catálogo protagonista, 1.376 de densidad y 60 de captura previa PASS; sombras y sanitizadores focalizados PASS (LSan Linux). Fuente de simulación intacta; faltantes válidos conservan clásico y errores reales rechazan. Candidato/replay/H3/CI completa y contacto visual enemigos PENDIENTES. [Evidencia](evidence/enemy-catalog-integration-v1.json).

El manifiesto4 puede incorporar enemy_catalog schema1 a la misma densidad. Se exigen todos los contratos producidos, firmas por raster y ausencia nativa por firma cero, con assets vacíos solo como desarrollo explícito. complete_art impide declarar terminado un catálogo con cuerpos o sombras opacos sin arte. El entorno debe activar ambos catálogos; sin la opción enemiga se conserva la ruta anterior. Marcador C4 independiente, jefe sin sombra inventada.

E3.T3 — preparar candidatos técnicos privados por densidad con protagonistas conservados, 679 contratos enemigos firmados y arte E01 disponible; medir faltantes y sombras pendientes sin presentarlos como revisión final. Validar carga/recursos antes del replay técnico.

## E3.T3 — candidatos técnicos privados

- **E3.T3 comprobado:** candidatos privados 8×/12×, 679 contratos: 54 corporales E01, seis sombras modernas reutilizadas por igualdad nativa, 66 no-write, cuatro marcadores nativos y 549 cuerpos sin arte. 204 activos por densidad; 11.227.648/25.262.208 bytes, dentro de 64 MiB. Validación C++ con bancos retenidos Windows/Linux y sanitizadores PASS; tres pruebas de conversión PASS. Contacto de suelo, replay/H3/CI y revisión final PENDIENTES. [Evidencia](evidence/enemy-technical-candidates-v1.json).

Preparador: tools/modernization/prepare_enemy_technical_candidate.py. Validador C++: validate_enemy_technical_candidate.cpp. Recuperación local: C:\Users\migue\.codex\visualizations\2026\11\19\01a1f3ca-14cf-76a1-a9ab-bf2ff6bf17c3\enemy-technical-v2. Recalcula firmas desde cuatro bancos verificados, conserva descriptores/bytes protagonistas y separa faltantes de recursos vacíos. No hay lanzador de revisión final.

E3.T4 — cualificar y adjuntar la pintura de sombra de suelo aprobada a las 27 poses E01 existentes, con apoyo/proyección comunes por dirección y hashes corporales intactos; validar contratos y candidatos sin generar arte nuevo ni activar revisión final.

## E3.T4 — sombras de suelo cualificadas

Nueve grupos/27 poses/54 derivados con apoyo inferior y centro de sombra abajo-derecha; colocación común por dirección. Pintura aprobada y cuerpos intactos. Candidatos y catálogo conservados; validación Windows/Linux con bancos retenidos y sanitizadores PASS. [Evidencia](evidence/enemy-ground-contact-integration-v1.json). No es aceptación visual global.

E3.T5 — compilar diagnóstico privado con la integración actual; ejecutar replay técnico de cuerpos/sombras y H3 pertinente en Windows/Linux, consultar CI y medir continuidad/faltantes. No entregar el candidato parcial como revisión final.

## E3.T5 — replay/H3 local comprobados, CI pendiente

- **E3.T5 local PASS, CI PENDIENTE:** diagnóstico compilado Windows/Linux; H3 clásico11 fases/11.361 estados y M1P2 técnico1.546 estados intactos, 4.635 publicaciones HD en ambos sistemas. Enemigo5: 1.673 dibujos modernos/5.022 clásicos por arte pendiente; sin missing de datos. CI Windows de37de241 falló por guardia de captura antigua; corrección y85 pruebas Python PASS locales, pendiente de CI. [Evidencia](evidence/enemy-technical-replay-v1.json).

Los analizadores antiguos de captura y diagnóstico se adaptan al contrato enemigo opt-in; nuevos controles negativos impiden clasificar cadáveres nativos como cuerpos. Se actualizan solo hashes de procedencia del inventario protagonista. No se modifican referencias H3 ni cuerpos/poses. Pendiente verificar CI completa de la corrección.

## E3.T5.CI — integración técnica comprobada (25-11-2026)

CI completa de14025f9: Windows, Linux y H6 PASS; ejecuciones PR y push confirmadas. El diagnóstico local conserva H3 en ambos sistemas y publica cuerpos E01/sombras con faltantes artísticos explícitos. [Cierre reproducible](evidence/enemy-technical-ci-20261125.json). No hay aceptación visual global ni revisión final de enemigos. Siguiente tarea única: E2.G1, resolver bloqueo de generación antes de continuar arte. No se ha repetido ni sorteado el rechazo.

## E2.G1.R — solicitud de revisión preparada (25-11-2026)

- **E2.G1.R — revisión preparada, NO enviada:** comprobado rechazo de salida concreto, no bloqueo general de cuenta/servicio demostrado. ImageGen no ofrece aquí acción de revisión/desbloqueo. Informe de soporte reproducible con petición d0b0ba1a-05a9-416c-aa3c-3c603d2441aa conservado localmente, sin imágenes ni recursos comerciales adjuntos. Sin nueva generación ni elusión. [Vía oficial y entrega](evidence/enemy-imagegen-review-request-20261125.json).

Siguiente paso: envío por el canal privado oficial de soporte. No equivale a una petición enviada ni a rechazo resuelto. El bloqueo de arte continúa y la integración técnica comprobada se conserva.

- **E2.A7 comprobado:** prone, dirección7, 59/F0; registro28 poses/56 activos. [Evidencia](evidence/enemy-v2-aim-d7.json). Próximo: E2.A0 — preparar apuntado bajo enemigo dirección 0, 52/F0, con E01 y referencias nativas; validar 8×/12×, apoyo de sombra y publicar antes de otra dirección. 4B/F0 queda pendiente sin bloquear otras poses.

- **E2.A0 comprobado:** prone, dirección0, 52/F0; registro29 poses/58 activos. [Evidencia](evidence/enemy-v2-aim-d0.json). Próximo: E2.A1 — preparar apuntado bajo enemigo dirección 1, 53/F0, con E01 y referencias nativas; validar 8×/12×, apoyo y publicar antes de otra dirección. 4B/F0 permanece pendiente.

- **E2.A1 comprobado:** prone, dirección1, 53/F0; registro30 poses/60 activos. [Evidencia](evidence/enemy-v2-aim-d1.json). Próximo: E2.A2 — preparar apuntado bajo enemigo dirección 2, 54/F0, con E01 y referencias nativas; validar 8×/12×, apoyo y publicar antes de otra dirección. 4B/F0 permanece pendiente.

- **E2.A2 comprobado:** prone, dirección2, 54/F0; registro31 poses/62 activos. [Evidencia](evidence/enemy-v2-aim-d2.json). Próximo: E2.A3 — preparar apuntado bajo enemigo dirección 3, 55/F0, con E01 y referencias nativas; validar 8×/12×, apoyo y publicar antes de otra dirección. 4B/F0 permanece pendiente.

- **E2.A3 comprobado:** prone, dirección3, 55/F0; registro32 poses/64 activos. [Evidencia](evidence/enemy-v2-aim-d3.json). Próximo: E2.A4 — preparar apuntado bajo enemigo dirección 4, 56/F0, con E01 y referencias nativas; validar 8×/12×, apoyo y publicar antes de otra dirección. 4B/F0 permanece pendiente.

- **E2.A4 comprobado:** prone, dirección4, 56/F0; registro33 poses/66 activos. [Evidencia](evidence/enemy-v2-aim-d4.json). Próximo: E2.A5 — preparar apuntado bajo enemigo dirección 5, 57/F0, con E01 y referencias nativas; validar 8×/12×, apoyo y publicar antes de otra dirección. 4B/F0 permanece pendiente.

- **E2.A5 comprobado:** prone, dirección5, 57/F0; registro34 poses/68 activos. [Evidencia](evidence/enemy-v2-aim-d5.json). Próximo: E2.A6 — preparar apuntado bajo enemigo dirección 6, 58/F0, con E01 y referencias nativas; validar 8×/12×, apoyo y publicar. Después revisar integración del conjunto de ocho direcciones sin activar un lote parcial como final.

- **E2.A6 comprobado:** prone, dirección6, 58/F0; registro35 poses/70 activos. [Evidencia](evidence/enemy-v2-aim-d6.json). Próximo: E3.A — integrar las ocho poses de apuntado bajo E01 en candidatos técnicos y verificar sombras por propietario5/36, geometría, faltantes y presupuesto. Conservar candidatos/lanzadores anteriores; no presentar lote parcial como final.

- **E3.A comprobado:** ocho poses de apuntado integradas; propietarios5/36 y transición51 verificados.35 poses,92 contratos modernos; candidatos anteriores conservados. [Evidencia](evidence/enemy-aim-integration-v1.json). Próximo: E2.R0 — modernizar la pose de lanzacohetes A8/F2, dirección0, con identidad E01/v2 y referencia nativa; validar exportación y sombra de propietario36. No reintentar la imagen4B/F0 pendiente.

- **E2.R0 comprobado:** pose, dirección0, A8/F2; registro36 poses/72 activos. [Evidencia](evidence/enemy-v2-rocket-d0.json). Próximo: E2.R1 — modernizar la pose de lanzacohetes A9/F2, dirección1, con identidad E01/v2, referencia nativa y sombra de propietario36. Conservar4B/F0 pendiente sin reintento.

- **E2.R1 comprobado:** pose, dirección1, A9/F2; registro37 poses/74 activos. [Evidencia](evidence/enemy-v2-rocket-d1.json). Próximo: E2.R2 — modernizar la pose de lanzacohetes AA/F2, dirección2, con identidad E01/v2, referencia nativa y sombra de propietario36. Conservar4B/F0 pendiente sin reintento.

- **E2.R2 comprobado:** pose, dirección2, AA/F2; registro38 poses/76 activos. [Evidencia](evidence/enemy-v2-rocket-d2.json). Próximo: E2.R3 — modernizar lanzacohetes AB/F2, dirección3, con identidad E01/v2 y sombra de propietario36. Conservar4B/F0 pendiente sin reintento.

- **E2.R3 comprobado:** pose, dirección3, AB/F2; registro39 poses/78 activos. [Evidencia](evidence/enemy-v2-rocket-d3.json). Próximo: E2.R4 — modernizar lanzacohetes AC/F2, dirección4, con identidad E01/v2 y sombra de propietario36. Conservar4B/F0 pendiente sin reintento.

- **E2.R4 comprobado:** pose, dirección4, AC/F2; registro40 poses/80 activos. [Evidencia](evidence/enemy-v2-rocket-d4.json). Próximo: E2.R5 — modernizar lanzacohetes AD/F2, dirección5, con identidad E01/v2 y sombra de propietario36. Conservar4B/F0 pendiente sin reintento.

- **E2.R5 comprobado:** pose, dirección5, AD/F2; registro41 poses/82 activos. [Evidencia](evidence/enemy-v2-rocket-d5.json). Próximo: E2.R6 — modernizar lanzacohetes AE/F2, dirección6, con identidad E01/v2 y sombra de propietario36. Conservar4B/F0 pendiente sin reintento.

- **E2.R6 comprobado:** pose, dirección6, AE/F2; registro42 poses/84 activos. [Evidencia](evidence/enemy-v2-rocket-d6.json). Próximo: E2.R7 — modernizar lanzacohetes AF/F2, dirección7, con identidad E01/v2 y sombra de propietario36. Conservar4B/F0 pendiente sin reintento.

- **E2.R7 comprobado:** pose, dirección7, AF/F2; registro43 poses/86 activos. [Evidencia](evidence/enemy-v2-rocket-d7.json). Próximo: E3.R — integrar las ocho poses de lanzacohetes A8..AF/F2 en candidatos nuevos8×/12×; validar contratos nativos, sombra de propietario36 y presupuesto. Mantener4B/F0 pendiente y candidatos previos intactos.

- **E3.R comprobado:** lanzacohetes8direcciones integrado,108contratos modernos,501cuerpos pendientes de arte; candidato privado conservado, no revisión final. [Evidencia](evidence/enemy-rocket-integration-v1.json). Próximo: E2.S0 — modernizar natación enemiga5A/F0,F1, dirección0, con identidad E01/v2 y referencias nativas. Preservar agua y ausencia de sombra de suelo; no reintentar4B/F0.

- **E2.S0 comprobado:** pose, dirección0, 5A/F0,1; registro45 poses/90 activos. [Evidencia](evidence/enemy-v2-swim-d0.json). Próximo: E2.S1 — modernizar natación enemiga5B/F0,F1, dirección1, con identidad E01/v2 y referencias nativas. Preservar agua y ausencia de sombra de suelo; no reintentar4B/F0.

- **E2.S1 comprobado:** pose, dirección1, 5B/F0,1; registro47 poses/94 activos. [Evidencia](evidence/enemy-v2-swim-d1.json). Próximo: E2.S2 — modernizar natación enemiga5C/F0,F1, dirección2, con identidad E01/v2 y referencias nativas. Preservar agua y ausencia de sombra de suelo; no reintentar4B/F0.

- **E2.S2 comprobado:** pose, dirección2, 5C/F0,1; registro49 poses/98 activos. [Evidencia](evidence/enemy-v2-swim-d2.json). Próximo: E2.S3 — modernizar natación enemiga5D/F0,F1, dirección3, con identidad E01/v2 y referencias nativas. Preservar agua y ausencia de sombra de suelo; no reintentar4B/F0.

- **E2.S3 comprobado:** pose, dirección3, 5D/F0,1; registro51 poses/102 activos. [Evidencia](evidence/enemy-v2-swim-d3.json). Próximo: E2.S4 — modernizar natación enemiga5E/F0,F1, dirección4, con identidad E01/v2 y referencias nativas directas. Preservar agua y ausencia de sombra de suelo; no reintentar4B/F0.

- **E2.S4 comprobado:** pose, dirección4, 5E/F0,1; registro53 poses/106 activos. [Evidencia](evidence/enemy-v2-swim-d4.json). Próximo: E2.S5 — modernizar natación enemiga5F/F0,F1, dirección5, con identidad E01/v2 y referencias nativas. Preservar agua y ausencia de sombra de suelo; no reintentar4B/F0.

- **E2.S5 comprobado:** pose, dirección5, 5F/F0,1; registro55 poses/110 activos. [Evidencia](evidence/enemy-v2-swim-d5.json). Próximo: E2.S6 — modernizar natación enemiga60/F0,F1, dirección6, con identidad E01/v2 y referencias nativas. Preservar agua y ausencia de sombra de suelo; no reintentar4B/F0.

- **E2.S6 comprobado:** pose, dirección6, 60/F0,1; registro57 poses/114 activos. [Evidencia](evidence/enemy-v2-swim-d6.json). Próximo: E2.S7 — modernizar natación enemiga61/F0,F1, dirección7, con identidad E01/v2 y referencias nativas. Preservar agua y ausencia de sombra de suelo; no reintentar4B/F0.

- **E2.S7 comprobado:** pose, dirección7, 61/F0,1; registro59 poses/118 activos. [Evidencia](evidence/enemy-v2-swim-d7.json). Próximo: E3.S — integrar las16 poses de natación5A..61/F0,F1 en candidatos nuevos8×/12×; validar contratos nativos, ausencia de sombra de suelo y presupuesto. Mantener4B/F0 pendiente y candidatos anteriores intactos.

- **E3.S comprobado:** natación16poses integrada sin suelo añadido;59poses,140contratos modernos,469cuerpos pendientes. [Evidencia](evidence/enemy-swim-integration-v1.json). Próximo: E3.CI — cerrar CI Windows/Linux/H6 del código y arte actuales; conservar resultados focalizados válidos, resolver solo fallos demostrados. Después retomar la siguiente dirección/familia producida del hito enemigo. No entregar aún revisión parcial como final.

- **E3.CI comprobado:** CI completa del código/arte76db816 PASS: Windows push/Linux PR/H6; PR Windows duplicado cancelado60min, separado de PASS equivalente.87 pruebas Python. [Evidencia](evidence/enemy-ci-20261125-76db816.json). Próximo: E3.V0 — contrastar proporciones de natación5A/F0,F1 (una dirección) frente al maestro y referencia nativa: el ajuste independiente X/Y parece alargar el casco. Preparar comparación y corregir solo si se confirma, conservando fuentes, derivados/candidatos anteriores, caja16×14, ancla y agua. Después retomar daño enemigo62/F0,F1.

- **E3.V0 comprobado:** corregida deformación de casco en5A/F0,F1 por escala no uniforme; fuentes/derivados previos intactos. [Evidencia](evidence/enemy-swim-proportions-d0.json). Próximo: E3.V1 — corregir proporciones de natación5B/F0,F1, dirección1, con recorte/escala compartidos, conservando originales, caja/ancla/agua. Tras las ocho direcciones, validar candidato nuevo y retomar daño62/F0,F1.

- **E3.V1 comprobado:** natación5B/F0,F1 proporcional, originales conservados. [Evidencia](evidence/enemy-swim-proportions-d1.json). Próximo: E3.V2 — corregir proporciones de natación5C/F0,F1, dirección2, conservando fuentes/derivados previos, geometría/ancla/agua. Tras las ocho direcciones, validar candidato nuevo y retomar daño62/F0,F1.

- **E3.V2 comprobado:** natación5C/F0,F1 proporcional, originales conservados. [Evidencia](evidence/enemy-swim-proportions-d2.json). Próximo: E3.V3 — corregir proporciones de natación5D/F0,F1, dirección3, conservando fuentes/derivados previos, geometría/ancla/agua. Tras las ocho direcciones, validar candidato nuevo y retomar daño62/F0,F1.

- **E3.V3 comprobado:** natación5D/F0,F1 proporcional, originales conservados. [Evidencia](evidence/enemy-swim-proportions-d3.json). Próximo: E3.V4 — corregir proporciones de natación5E/F0,F1, dirección4, conservando fuentes/derivados previos, geometría/ancla/agua. Tras las ocho direcciones, validar candidato nuevo y retomar daño62/F0,F1.

- **E3.V4 comprobado:** natación5E/F0,F1 proporcional, originales conservados. [Evidencia](evidence/enemy-swim-proportions-d4.json). Próximo: E3.V5 — corregir proporciones de natación5F/F0,F1, dirección5, conservando fuentes/derivados previos, geometría/ancla/agua. Tras las ocho direcciones, validar candidato nuevo y retomar daño62/F0,F1.

- **E3.V5 comprobado:** natación5F/F0,F1 proporcional, originales conservados. [Evidencia](evidence/enemy-swim-proportions-d5.json). Próximo: E3.V6 — corregir proporciones de natación60/F0,F1, dirección6, conservando fuentes/derivados previos, geometría/ancla/agua. Tras las ocho direcciones, validar candidato nuevo y retomar daño62/F0,F1.

- **E3.V6 comprobado:** natación60/F0,F1 proporcional, originales conservados. [Evidencia](evidence/enemy-swim-proportions-d6.json). Próximo: E3.V7 — corregir proporciones de natación61/F0,F1, dirección7, conservando fuentes/derivados previos, geometría/ancla/agua. Tras las ocho direcciones, validar candidato nuevo y retomar daño62/F0,F1.

- **E3.V7 comprobado:** natación61/F0,F1 proporcional, originales conservados. [Evidencia](evidence/enemy-swim-proportions-d7.json). Próximo: E3.VI — integrar las16 poses de natación corregidas en candidatos nuevos8×/12×; verificar contratos nativos, agua, ausencia de suelo, presupuesto y continuidad. Conservar candidatos anteriores; después retomar daño62/F0,F1.

- **E3.VI comprobado:** natación proporcional integrada con originales conservados;679contratos por densidad/plataforma y sanitizadores PASS. [Evidencia](evidence/enemy-swim-proportions-integration-v2.json). Próximo: E2.D0 — modernizar daño enemigo62/F0,F1, dirección0, con identidad E01/v2, maestros protagonistas20 necesarios y referencias nativas62. Mantener sombras específicas/independientes, sin suelo añadido; no reintentar4B/F0.

- **E2.D0 comprobado:** death, dirección0, 62/F0,1; registro61 poses/122 activos. [Evidencia](evidence/enemy-v2-damage-d0.json). Próximo: E2.D1 — modernizar daño enemigo63/F0,F1, dirección1, con identidad E01/v2, maestros protagonistas21 necesarios y referencias nativas63. Mantener sombras específicas/independientes, sin suelo añadido; no reintentar4B/F0.

- **E2.D1 comprobado:** death, dirección1, 63/F0,1; registro63 poses/126 activos. [Evidencia](evidence/enemy-v2-damage-d1.json). Próximo: E2.D2 — modernizar daño enemigo64/F0,F1, dirección2, con identidad E01/v2, maestros protagonistas22 necesarios y referencias nativas64. Mantener sombras específicas/independientes, sin suelo añadido; no reintentar4B/F0.

- **E2.D2 comprobado:** death, dirección2, 64/F0,1; registro65 poses/130 activos. [Evidencia](evidence/enemy-v2-damage-d2.json). Próximo: E2.D3 — modernizar daño enemigo65/F0,F1, dirección3, con identidad E01/v2, maestros protagonistas23 necesarios y referencias nativas65. Mantener sombras específicas/independientes, sin suelo añadido; no reintentar4B/F0.

- **E2.D3 comprobado:** death, dirección3, 65/F0,1; registro67 poses/134 activos. [Evidencia](evidence/enemy-v2-damage-d3.json). Próximo: E3.DA0 — ajustar exportación de62/F0,F1 a la caja/ancla nativa de cada frame, con escala proporcional y originales intactos; después63 y64. Retomar luego producción65..69 pendiente (siguiente66/F0,F1).

- **E3.DA0 comprobado:** daño62, ajuste proporcional por frame, originales conservados. [Evidencia](evidence/enemy-damage-native-anchor-d0.json). Próximo: E3.DA1 — ajustar exportación de63/F0,F1 a la caja/ancla nativa de cada frame, escala proporcional y originales intactos; retomar luego producción66..69.

- **E3.DA1 comprobado:** daño63, ajuste proporcional por frame, originales conservados. [Evidencia](evidence/enemy-damage-native-anchor-d1.json). Próximo: E3.DA2 — ajustar exportación de64/F0,F1 a la caja/ancla nativa de cada frame, escala proporcional y originales intactos; retomar luego producción66..69.

- **E3.DA2 comprobado:** daño64, ajuste proporcional por frame, originales conservados. [Evidencia](evidence/enemy-damage-native-anchor-d2.json). Próximo: E2.D4 — modernizar daño enemigo66/F0,F1, dirección4, con identidad E01/v2, maestros protagonistas24 necesarios y referencias nativas66. Ajuste proporcional/ancla por frame; conservar sombras específicas/independientes, sin suelo añadido.

- **E2.D4 comprobado:** death, dirección4, 66/F0,1; registro69 poses/138 activos. [Evidencia](evidence/enemy-v2-damage-d4.json). Próximo: E2.D5 — modernizar daño enemigo67/F0,F1, dirección5, con identidad E01/v2, maestros protagonistas25 necesarios y referencias nativas67. Ajuste proporcional/ancla por frame; conservar sombras específicas/independientes, sin suelo añadido.

- **E2.D5 comprobado:** death, dirección5, 67/F0,1; registro71 poses/142 activos. [Evidencia](evidence/enemy-v2-damage-d5.json). Próximo: E2.D6 — modernizar daño enemigo68/F0,F1, dirección6, con identidad E01/v2, maestros protagonistas26 necesarios y referencias nativas68. Ajuste proporcional/ancla por frame; conservar sombras específicas/independientes, sin suelo añadido.

- **E2.D6 comprobado:** death, dirección6, 68/F0,1; registro73 poses/146 activos. [Evidencia](evidence/enemy-v2-damage-d6.json). Próximo: E2.D7 — modernizar daño enemigo69/F0,F1, dirección7, con identidad E01/v2, maestros protagonistas27 necesarios y referencias nativas69. Ajuste proporcional/ancla por frame; conservar sombras específicas/independientes, sin suelo añadido.69/F2 sigue solo declarado, sin arte/vínculo.

- **E2.D7 comprobado:** death, dirección7, 69/F0,1; registro75 poses/150 activos. [Evidencia](evidence/enemy-v2-damage-d7.json). Próximo: E3.DI — integrar las16 poses de daño62..69/F0,F1 en candidatos nuevos8×/12×; verificar contratos nativos, anclas, ausencia de suelo, presupuesto y continuidad. Conservar candidatos anteriores; no activar69/F2 ni4B/F0.

- **2026-11-26 E3.DI:** primera familia de daño16poses integrada;204contratos modernos frente a140anteriores, sin suelo añadido.679dibujos por densidad/plataforma y sanitizadores Windows/Linux PASS. [Evidencia](evidence/enemy-damage-integration-v1.json). Próximo: E2.D20 — modernizar segunda reacción de daño6A/F0,F1, dirección0, con identidad E01/v2, maestros protagonistas28 y referencias nativas6A. Ajuste proporcional/ancla por frame; conservar altura y sombras independientes, sin suelo añadido. No reintentar4B/F0.

- **E2.D20 comprobado:** death, dirección0, 6A/F0,1; registro77 poses/154 activos. [Evidencia](evidence/enemy-v2-damage2-d0.json). Próximo: E2.D21 — modernizar segunda reacción de daño6B/F0,F1, dirección1, con identidad E01/v2, maestros protagonistas29 y referencias nativas6B. Mantener anclas por frame, altura y sombras independientes; sin suelo añadido.64 se reutiliza en dirección2 por fuente; no crear6C.

- **E2.D21 comprobado:** death, dirección1, 6B/F0,1; registro79 poses/158 activos. [Evidencia](evidence/enemy-v2-damage2-d1.json). Próximo: E2.D23 — modernizar segunda reacción de daño6D/F0,F1, dirección3, con identidad E01/v2, maestros protagonistas2B y referencias nativas6D. Mantener anclas por frame, altura y sombras independientes; sin suelo añadido. Dirección2 ya cubierta por64; no crear6C.

- **E2.D23 comprobado:** death, dirección3, 6D/F0,1; registro81 poses/162 activos. [Evidencia](evidence/enemy-v2-damage2-d3.json). Próximo: E2.D24 — modernizar segunda reacción de daño6E/F0,F1, dirección4, con identidad E01/v2, maestros protagonistas2C y referencias nativas6E. Mantener anclas por frame, altura y sombras independientes; sin suelo añadido.

- **E2.D24 comprobado:** death, dirección4, 6E/F0,1; registro83 poses/166 activos. [Evidencia](evidence/enemy-v2-damage2-d4.json). Próximo: E2.D25 — modernizar segunda reacción de daño6F/F0,F1, dirección5, con identidad E01/v2, maestros protagonistas2D y referencias nativas6F. Mantener anclas por frame, altura y sombras independientes; sin suelo añadido.

- **E2.D25 comprobado:** death, dirección5, 6F/F0,1; registro85 poses/170 activos. [Evidencia](evidence/enemy-v2-damage2-d5.json). Próximo: E2.D26 — modernizar segunda reacción de daño70/F0,F1, dirección6, con identidad E01/v2, maestros protagonistas2E y referencias nativas70. Mantener anclas por frame, altura y sombras independientes; sin suelo añadido.

- **E2.D26 comprobado:** death, dirección6, 70/F0,1; registro87 poses/174 activos. [Evidencia](evidence/enemy-v2-damage2-d6.json). Próximo: E2.D27 — modernizar segunda reacción de daño71/F0,F1, dirección7, con identidad E01/v2, maestros protagonistas2F y referencias nativas71. Mantener anclas por frame, altura y sombras independientes; sin suelo añadido. Después integrar familia completa sin6C.

- **E2.D27 comprobado:** death, dirección7, 71/F0,1; registro89 poses/178 activos. [Evidencia](evidence/enemy-v2-damage2-d7.json). Próximo: E3.D2I — integrar las14 poses propias de segunda reacción6A,6B,6D..71/F0,F1 en candidatos nuevos8×/12×, junto a64 reutilizado por la fuente. Verificar contratos nativos, anclas, ausencia de suelo, presupuesto y sanitizadores Windows/Linux. Conservar candidatos anteriores; sin6C ni4B/F0.

- **2026-11-26 E3.D2I:** segunda reacción integrada,260contratos modernos y274activos dentro de64MiB.679dibujos por densidad/plataforma y sanitizadores Windows/Linux PASS. [Evidencia](evidence/enemy-damage2-integration-v1.json). Próximo: E3.RA — auditar reutilización explícita de maestros E01 en daño inicial enemigo tipo5/persona0, empezando solo20/F0,F1. Verificar productor, acción/dirección/frame, geometría y procedencia; decidir exportación propia sin alias nativo ni generación redundante. No incorporar53referencias ni claves declaradas por lote.

- **2026-11-26 E3.RA:** reutilización artística explícita de E01 para20/F0,F1 viable por acción/dirección/frame y procedencia. Sin alias de firmas ni exportación aún. [Auditoría](evidence/enemy-initial-master-reuse-audit-v1.json). Próximo: E3.R0 — exportar daño inicial20/F0 (PC/Amiga) y20/F1 (soloAmiga) reutilizando maestros E01 de62, con firma/geometría/ancla y procedencia propias. Ajustar verificador a formatos realmente producidos, excluir suelo y comprobar PNG/RGBA. Sin vínculo20/F1PC, alias nativo, nuevas generaciones ni cambios protagonistas.

- **2026-11-26 E3.R0:** daño inicial20,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage-d0.json). Próximo: E3.R1 — verificar y exportar daño inicial21/F0,F1 de tipo5/persona0, dirección1, reutilizando maestros E01 de63 con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones.

- **2026-11-26 E3.R1:** daño inicial21,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage-d1.json). Próximo: E3.R2 — verificar y exportar daño inicial22/F0,F1 de tipo5/persona0, dirección2, reutilizando maestros E01 de64 con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones.

- **2026-11-26 E3.R2:** daño inicial22,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage-d2.json). Próximo: E3.R3 — verificar y exportar daño inicial23/F0,F1 de tipo5/persona0, dirección3, reutilizando maestros E01 de65 con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones.

- **2026-11-26 E3.R3:** daño inicial23,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage-d3.json). Próximo: E3.R4 — verificar y exportar daño inicial24/F0,F1 de tipo5/persona0, dirección4, reutilizando maestros E01 de66 con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones.

- **2026-11-26 E3.R4:** daño inicial24,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage-d4.json). Próximo: E3.R5 — verificar y exportar daño inicial25/F0,F1 de tipo5/persona0, dirección5, reutilizando maestros E01 de67 con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones.

- **2026-11-26 E3.R5:** daño inicial25,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage-d5.json). Próximo: E3.R6 — verificar y exportar daño inicial26/F0,F1 de tipo5/persona0, dirección6, reutilizando maestros E01 de68 con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones.

- **2026-11-26 E3.R6:** daño inicial26,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage-d6.json). Próximo: E3.R7 — verificar y exportar daño inicial27/F0,F1 de tipo5/persona0, dirección7, reutilizando maestros E01 de69 con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones.

- **2026-11-26 E3.R7:** daño inicial27,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage-d7.json). Próximo: E3.RI — integrar daño inicial20..27 producido, con formatos y contratos propios, en candidatos nuevos8×/12×. Verificar sanitizadores Windows/Linux, presupuesto y ausencia de suelo; no crear frames inexistentes ni tocar protagonistas.

- **2026-11-26 E3.RI:**31contratos iniciales pasan aHD con16maestros E01reutilizados;291contratos modernos y290activos.679dibujos por densidad/plataforma y sanitizadores Windows/Linux PASS. [Evidencia](evidence/enemy-initial-damage-integration-v1.json). Próximo: E3.R20 — verificar y exportar segunda reacción inicial28/F0,F1 de tipo5/persona0, dirección0, reutilizando maestros E01 de6A. Comprobar acción/frame/procedencia, formatos producidos, firmas y anclas propias; sin suelo añadido, alias ni nuevas generaciones.2A no se crea: la fuente reutiliza22.

- **2026-11-26 E3.R20:** daño inicial28,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage2-d0.json). Próximo: E3.R21 — verificar y exportar segunda reacción inicial29/F0,F1 de tipo5/persona0, dirección1, reutilizando maestros E01 de6B con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones. Dirección2 ya cubierta por22; no crear2A.

- **2026-11-26 E3.R21:** daño inicial29,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage2-d1.json). Próximo: E3.R23 — verificar y exportar segunda reacción inicial2B/F0,F1 de tipo5/persona0, dirección3, reutilizando maestros E01 de6D con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones. Dirección2 ya cubierta por22; no crear2A.

- **2026-11-26 E3.R23:** daño inicial2B,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage2-d3.json). Próximo: E3.R24 — verificar y exportar segunda reacción inicial2C/F0,F1 de tipo5/persona0, dirección4, reutilizando maestros E01 de6E con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones. Dirección2 ya cubierta por22; no crear2A.

- **2026-11-26 E3.R24:** daño inicial2C,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage2-d4.json). Próximo: E3.R25 — verificar y exportar segunda reacción inicial2D/F0,F1 de tipo5/persona0, dirección5, reutilizando maestros E01 de6F con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones. Dirección2 ya cubierta por22; no crear2A.

- **2026-11-26 E3.R25:** daño inicial2D,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage2-d5.json). Próximo: E3.R26 — verificar y exportar segunda reacción inicial2E/F0,F1 de tipo5/persona0, dirección6, reutilizando maestros E01 de70 con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones. Dirección2 ya cubierta por22; no crear2A.

- **2026-11-26 E3.R26:** daño inicial2E,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage2-d6.json). Próximo: E3.R27 — verificar y exportar segunda reacción inicial2F/F0,F1 de tipo5/persona0, dirección7, reutilizando maestros E01 de71 con acción/frame/procedencia comprobados. Firmas, formatos y anclas propios; sin suelo añadido, alias ni nuevas generaciones. Dirección2 ya cubierta por22; no crear2A.

- **2026-11-26 E3.R27:** daño inicial2F,2maestros E01 reutilizados explícitamente, contratos y formatos propios. [Evidencia](evidence/enemy-initial-damage2-d7.json). Próximo: E3.R2I — integrar segunda reacción inicial28,29,2B..2F producida en candidatos nuevos8×/12×, junto a22 reutilizado por la fuente. Verificar contratos, sanitizadores Windows/Linux, presupuesto y ausencia de suelo; sin2A ni frames inexistentes.

- **2026-11-26 E3.R2I:**59contratos iniciales enHD con30maestros E01reutilizados;319contratos modernos y304activos.679dibujos por densidad/plataforma y sanitizadores Windows/Linux PASS. [Evidencia](evidence/enemy-initial-damage2-integration-v1.json). Próximo: E2.TA — auditar tercera tabla de daño enemiga72/F0,F1,F2 (una dirección), su productor real y relación con caídaB8..BF. Consultar solo controladores, referencias nativas y maestros pertinentes; fijar poses, anclas y tratamiento de sombra antes de exportar/generar. No extrapolar la prueba de estados dormidos protagonista a enemigos.

- **2026-11-26 E2.TA:**72/F0..2 de infantería5 y equivalentesB8..BA verificados en6contratos PC/Amiga; tipo36solo declarado. Reloj y maestros30 identificados; no generación ni alias automático. [Auditoría](evidence/enemy-mode-zero-d0-audit-v1.json). Próximo: E2.T0 — modernizar72/F0,F1,F2 (dirección0 de tabla modo-cero) con identidad E01/v2, maestros protagonistas30/F0..2 y nativos72. Respetar pose/orientación de cada frame, anclas y reloj nativo; sin suelo añadido, conservando sombras independientes. Exportaciones propias; B8..BA se vincularán solo en paso explícito posterior.

- **E2.T0 comprobado:** pose, dirección0, 72/F0,1,2; registro122 poses/244 activos. [Evidencia](evidence/enemy-v2-mode-zero-d0.json). Próximo: E2.T1 — verificar y modernizar73/F0,F1,F2 (dirección1 de tabla modo-cero), con E01/v2, maestros protagonistas31 y nativos73. Confirmar equivalencia de cuerposBB..BD y conservar cada pose/orientación/ancla; sin suelo añadido ni vínculo automático de caída. Solo contratos producidos de infantería5.

- **E2.T1 comprobado:** pose, dirección1, 73/F0,1,2; registro125 poses/250 activos. [Evidencia](evidence/enemy-v2-mode-zero-d1.json). Próximo: E2.T2 — verificar y modernizar74/F0,F1,F2 (dirección2 de tabla modo-cero), con E01/v2, maestros protagonistas32 y nativos74. Comprobar pose/ancla de cada frame y relación BE/BF de los dos primeros; no extender equivalencias al tercero sin prueba. Sombras según fuente, sin vincular caída automáticamente.

- **E2.T2a comprobado:** pose, dirección2, 74/F0,1; registro127 poses/254 activos. [Evidencia](evidence/enemy-v2-mode-zero-d2-first-pair.json). Próximo: E2.T2R — resolver semántica y referencia de74/F2 antes de generar/vincular. Contrastar productor modo-cero, alias de datos CF/D0 y bancos privados disponibles; Amiga conserva86píxeles índice15, PC cuerpo multicolor. No convertir silueta en soldado, inventar maestro32 ni declarar dirección2 completa. Conservar74/F0,F1 comprobados.

- **2026-11-26 E2.T2R:** referencia de postura74/F2 identificada en datos PC/Plus; hipótesis de igualdad de máscaras descartada, sin alias. Anclas14/12 exigen exportación por formato. [Diagnóstico](evidence/enemy-mode-zero-74-f2-reference-diagnosis.json). Próximo: E2.T2b — producir74/F2 de infantería5 usando E01 y postura PC/Plus como referencia artística explícita (no alias nativo). Exportar por formato con anclas propias PC14/Amiga12, ampliando solo verificadores/preparador de catálogo; mantener firmas y recuperación nativas, sin activar otros bancos/campañas ni civiles. Validar679contratos y sanitizadores Windows/Linux antes de cerrar.

- **E2.T2b comprobado:** pose, dirección2, 74/F2; registro128 poses/258 activos. [Evidencia](evidence/enemy-v2-mode-zero-d2-last-frame.json). Próximo: E3.F0 — verificar y exportar caídaB8/F0, dirección0, de enemigos5/36 reutilizando maestro E01 de72/F0 por igualdad nativa comprobada. Mantener firmas/anclas propias, altura y sombra independiente; sin suelo añadido ni alias automático. Solo esta dirección antes de validar/publicar.

- **2026-11-26 E3.TI:**337contratos modernos y314activos;74/F2 con anclas por formato14/12.679dibujos por densidad/plataforma, sanitizadores y rechazo al intercambiar formatos PASS;23Python PASS. [Evidencia](evidence/enemy-mode-zero-first3-integration-v1.json). Próximo: E3.F0 — verificar y exportar caídaB8/F0, dirección0, de enemigos5/36 reutilizando maestro E01 de72/F0 por igualdad nativa comprobada. Mantener firmas/anclas propias, altura y sombra independiente; sin suelo añadido ni alias automático. Solo esta dirección antes de validar/publicar.

- **2026-11-26 E3.F0:** caídaB8/F0 con E01reutilizado sin alterar píxeles;4contratos nativos propios. [Evidencia](evidence/enemy-v2-fall-d0.json). Próximo: E3.F1 — verificar y exportar caídaB9/F0, dirección1, para enemigos5/36 con maestro E01 equivalente de tabla modo-cero. Igualdad nativa/geométrica y procedencia explícitas; firmas/anclas propias, altura y sombra independiente. Sin suelo añadido ni nueva generación; solo esta dirección antes de validar/publicar.

- **2026-11-26 E3.F1:** caídaB9/F0 con E01reutilizado sin alterar píxeles;4contratos nativos propios. [Evidencia](evidence/enemy-v2-fall-d1.json). Próximo: E3.F2 — verificar y exportar caídaBA/F0, dirección2, para enemigos5/36 con maestro E01 equivalente de tabla modo-cero. Igualdad nativa/geométrica y procedencia explícitas; firmas/anclas propias, altura y sombra independiente. Sin suelo añadido ni nueva generación; solo esta dirección antes de validar/publicar.

- **2026-11-26 E3.F2:** caídaBA/F0 con E01reutilizado sin alterar píxeles;4contratos nativos propios. [Evidencia](evidence/enemy-v2-fall-d2.json). Próximo: E3.F3 — verificar y exportar caídaBB/F0, dirección3, para enemigos5/36 con maestro E01 equivalente de tabla modo-cero. Igualdad nativa/geométrica y procedencia explícitas; firmas/anclas propias, altura y sombra independiente. Sin suelo añadido ni nueva generación; solo esta dirección antes de validar/publicar.
