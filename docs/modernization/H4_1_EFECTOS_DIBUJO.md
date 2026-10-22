# H4.1 — Inventario inicial de efectos del dibujo

Fecha: 22 de octubre de 2026. Fuente inspeccionada: `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8` (motor idéntico a la candidata H2.6).
Estado: **H4.1 en curso: auditoría y primera extracción de efectos implementadas.**
El inventario inicial no cambió el motor. La implementación posterior descrita al final extrae funciones manteniendo sus puntos de ejecución, sin cambiar frecuencias, assets ni huellas H3.

## 1. Hallazgo principal: hay dos ritmos lógicos

No debe trasladarse toda la lógica a Phase_Cycle ni aumentar las llamadas a Interrupt_Redraw para obtener más FPS.

- `Interrupt_Sim → Interrupt_Redraw`, bajo `mSurfaceMtx`: avanza el contador de grabación cuando procede; llama a `Phase_Loop_Interrupt`; después ejecuta un callback o compone terreno/sprites/panel/cursor.
- `Phase_Loop_Interrupt`: incrementa ticks según pausa/entrada, lee entradas, actualiza cámara, procesa órdenes, audio y cambio de arma. Incluye una llamada al cursor.
- `Phase_Cycle`: espera los ticks originales o la marca del replay; actualiza panel, progreso, objetivos y escuadras; llama a `Mission_Sprites_Handle`; continúa temporizadores y captura H3.
- `Mission_Sprites_Handle`: actualiza animación/comportamientos, ordena sprites, actualiza parámetros de mapa desde cámara, destruye tiles y **también llama a Sprites_Draw**.
- `Video_Sleep`: presenta, restaura superficie, coordina señales con el hilo de interrupciones y procesa eventos.

**Consecuencia:** Sprites_Draw se usa tanto en la ruta de interrupción como al actualizar sprites. Cambiarlo a «una vez por Phase_Cycle» alteraría el calendario observado. El primer refactor debe conservar los puntos de llamada, las condiciones y su orden.

## 2. Matriz de efectos encontrados

Rutas relativas a la raíz; las funciones son la referencia estable para localizar el código.

| Función / archivo | Escrituras o efectos observados | Tratamiento requerido |
|---|---|---|
| `Interrupt_Redraw`, `Source/Fodder.cpp` | Tick de replay, Phase_Loop_Interrupt, callback, señales mVideo_Done/mVideo_Ticked | Mantener en el calendario heredado; el refresco extra no puede invocarlo |
| `Sprites_Draw`, `Source/Fodder.cpp` | Consume mPendingDestroy; pone mPosX=-32768; libera mSprite_SpareUsed y mSprite_SpareUsed2 | Retirada lógica de entidades; mantener instante, orden y exclusión de la rama que dibuja |
| `Sprite_Draw_Frame`, `Source/Sprites/Sprite_Core.cpp` | mWasDrawn=0/1, incluso sin vídeo; prepara registros mVideo_Draw_* | Separar evaluación lógica de visibilidad y escritura de píxeles sin cambiar PC/Amiga |
| `Sprite_OnScreen_Check`, backends PC/Amiga; `Sprite_OnScreen_ClipY/Bottom`, `Source/Graphics.cpp` | Modifican posición, tamaño y puntero de origen; consultan tamaño de pantalla | No son predicados puros. Futuro comando de dibujo debe contener recorte propio y dimensiones lógicas clásicas |
| `Video_Draw_8`, backends PC/Amiga | Modifica mVideo_Draw_Columns y saltos de origen/destino además de píxeles | No reutilizar registros globales ya consumidos al repetir una presentación |
| `GUI_Sidebar_Draw`, `Source/GUI_Element.cpp` | Llama a Mission_Final_TimeToDie; cambia mSquad_CurrentWeapon según munición/refresh; consume banderas de refresco | Conservar en el paso principal; extraer efectos antes de convertir el HUD en lectura de snapshot |
| `Mission_Final_TimeToDie`, mismo archivo | En CF1 retail, misión 24 fase 6: incrementa ticker, reduce tiempo restante; solo después considera DisableVideo | Caso comercial fuera de demos. Nunca actualizarlo por fotograma de pantalla |
| `Mouse_DrawCursor`, `Source/Mouse.cpp` | Copia mMouseSpriteNew a mMouseSpriteCurrent y consume solicitud (-1); prepara coordenadas de dibujo | Conservar semántica y condición DisableVideo; presentación adicional lee cursor resuelto |
| `Sprite_Sort_DrawList`, `Source/Sprites/Sprite_Core.cpp` | Reconstruye listas de punteros, ordena por Y y publica lista final bajo mSpriteMtx | Snapshot debe conservar orden y vida de entidades; no exponer punteros vivos a otro hilo |
| `MapTile_UpdateFromCamera / Map_Destroy_Tiles`, `Source/Map/MapRuntime.cpp` | Copia estado de cámara; procesa cola/cuenta atrás y modifica mapa | Permanece en Mission_Sprites_Handle, antes de Sprites_Draw; jamás repetir para actualizar terreno visual |
| `MapTiles_Draw`, backends PC/Amiga | Escribe buffer y lo guarda con Save; Amiga además lo limpia | Efecto de composición; separar memoria del snapshot de los buffers de destino |
| `Video_Sleep / Video_SurfaceRender`, `Source/Fodder.cpp` | Presentación SDL, Restore, señales de sincronización y eventos | No usar Video_Sleep como simple «presentar otra imagen»: afecta al calendario |
| `cSurface::draw / Save / Restore`, `Source/Surface.cpp` | Conversión paletizada, actualización de textura y copias de buffer | Recursos mutables del presentador; no tratarlos como estado inmutable compartido |
| `palette_FadeTowardNew`, `Source/Surface.cpp` y llamadas | Avanza paleta/estado de fundido; puede gobernar salida de bucles | Conservar cadencia de cada pantalla; nuevo render lee la paleta del estado publicado |
| `Service_ScrollUp_DrawList`, `Source/Service.cpp` | Mueve entradas y modifica condición de salida; llamado desde callback cada dos ticks | Animación/pantalla con estado; no ejecutar callback por cada FPS nuevo |

La matriz es un inventario inicial de rutas examinadas, no una prueba de ausencia de cualquier otro efecto.

## 3. Callbacks, pausa y pantallas auxiliares

Se localizaron asignaciones de `mInterruptCallback` en Fodder, Service, Recruits, CampaignSelect, OptionsMenu y Start_Emscripten. El callback de opciones llama a Sprites_Draw; el de reclutas avanza paleta y copia superficies. Deben clasificarse antes de extender el nuevo presentador fuera de la fase jugable.

Se observan asignaciones sin un lock local explícito en varias de esas pantallas. Esto **no prueba por sí solo una carrera**: falta auditar contexto de llamada, propiedad y vida del hilo. Es una revisión pendiente de H4.5, cubierta solo parcialmente por el TSan headless H2. No extrapolar la protección añadida a Menu_Loop a todos los callbacks.

Pausa y minimapa tienen bucles propios. Phase_Paused presenta, avanza fundidos y procesa eventos. El mapa de resumen se omite en ciertas rutas de unit testing. Las demos automáticas no sustituyen su comprobación interactiva.

## 4. Plan de implementación por cambios pequeños

1. Extraer la retirada diferida de sprites y preparación/visibilidad a una etapa explícita, **en los mismos puntos de llamada heredados**. Mantener inicialmente el dibujo clásico y los bloqueos.
2. Encapsular los registros de recorte/dibujo por operación, evitando que la presentación extra escriba mWasDrawn o consuma solicitudes y temporizadores.
3. Separar efectos del panel y cursor conservando sus condiciones y frecuencia. El caso de temporizador comercial necesita prueba focalizada.
4. Definir estados inmutables con cámara lógica, orden/identidad/generación de sprites, recursos, recortes, paleta, HUD y cursor (H4.2); establecer propiedad y publicación coherente (H4.5).
5. Introducir presentaciones adicionales únicamente desde esos estados; conservar ruta clásica seleccionable. Después ejecutar 0/1/N dibujos (H4.6).

No llamar más veces a Sprites_Draw, GUI_Sidebar_Draw, Interrupt_Redraw o Video_Sleep como atajo para aumentar FPS.

## 5. Verificación y límites

Ejecutados sobre el checkout inspeccionado:

- `check_visibility_contract.py`: PASS, 15 referencias en 9 archivos.
- `check_sprite_table_lengths.py`: PASS, 293 arrays Amiga y 297 PC; 1.309 entradas de tablas.
- Inspección de `GameplayTrace.cpp`: H3 ya registra mWasDrawn, pending_destroy, arma por escuadra y tiempo final restante. No registra explícitamente todos los temporales descubiertos (p. ej. ticker final, spare-used y solicitud del cursor).

Para el refactor, mantener **sin cambios** las huellas H3 originales y añadir observaciones/pruebas complementarias donde falte cobertura. No sustituir las 11.361 muestras por una referencia nueva.

Pruebas específicas pendientes: destrucción/reutilización entre ticks, bordes PC/Amiga y fotograma inválido, agotamiento de munición, temporizador retail 24/6, solicitud de cursor con vídeo desactivado, pausa/minimapa y transición de fase. Su ejecución 0/1/N requiere la implementación, todavía no realizada.

**Cierre de este bloque:** auditoría inicial y contrato de extracción preparados. H4.1 permanece en curso hasta preservar/extraer los efectos y verificar regresión; H4.2–H4.6 no se declaran implementados.

## 6. Primera extracción implementada — 22-10-2026

Commit de código: `4e4d57efc408d4a4f404b5f4f2ed7844fde261c3`. Base: `3e15dde7cbdb46610f15aa4567b85dfb600ff0d0`; base clásica recuperable sin mover: `baseline/classic-h2.6-2026-10-22`.

| Efecto extraído | Función nueva | Punto de ejecución conservado |
|---|---|---|
| Retirada diferida de entidad | Sprite_CommitPendingDestroy | Dentro del mismo bucle Sprites_Draw y lock mSpriteMtx, antes de decidir dibujar cada entidad |
| Preparación y visibilidad lógica | Sprite_PrepareLegacyFrame | Cada llamada antigua a Sprite_Draw_Frame; actualiza mWasDrawn antes del guard DisableVideo y del blit |
| Selección de arma por munición | GUI_Sidebar_UpdateWeaponSelection | Después del temporizador y de los iconos; antes de consumir banderas de refresco de munición |
| Avance del temporizador comercial | Mission_Final_TimeToDie_Update | Dentro de Mission_Final_TimeToDie, antes de comprobar DisableVideo; solo cuando avanza el contador se dibuja su actualización |
| Consumo de solicitud del cursor | Mouse_CommitCursorRequest | Después del guard de vídeo y de calcular coordenadas; antes de llamar al backend gráfico |

Se mantienen las funciones coordinadoras clásicas. No se trasladan estos efectos en bloque a Phase_Cycle, ni se cambia la frecuencia de interrupción, ni se crean llamadas adicionales. Se conservan incluso las condiciones de fotograma inválido, entidad pendiente de destrucción y vídeo desactivado.

### Pruebas locales sobre el código cambiado

- Linux Release, GCC 13, SDL3/mixer de las referencias fijadas; FFmpeg desactivado.
- 6/6 CTests PASS y 13 tests Python existentes PASS.
- H3 PC Format: dos pasadas, 8 fases / 7.956 estados idénticos.
- H3 Amiga The One: dos pasadas, 3 fases / 3.405 estados idénticos.
- Comparación con `reference-gameplay-v1.json`: **11 fases / 11.361 estados canónicos coincidentes**, sin actualizar referencias.
- 29 replays: PASS, 29 fases, 0 omisiones, retorno 0.
- Contrato mWasDrawn y metadatos de sprites: PASS.
- La primera ejecución de CTest no pudo iniciar el binario local de endian porque faltaba su permiso de ejecución. Se corrigió el permiso del artefacto recién compilado; la repetición completa pasó. No hubo modificación de fuente ni supresión de prueba.

### Prueba focalizada de la misión comercial

`tools/modernization/check_final_timer_equivalence.py` extrae el cuerpo original de H2.6 y los cuerpos actuales de actualización/coordinación, los compila con UBSan en un entorno mínimo y compara estado y llamadas gráficas tras cada paso.

**184.320 transiciones idénticas**: combinaciones retail/no retail, CF1/no CF1, misiones/fases elegibles y no elegibles, bordes del ticker, tiempo restante y vídeo activado/desactivado. Las funciones gráficas son sustitutos que registran llamadas; no se afirma equivalencia de píxeles ni ejecución de la campaña CD32 completa.

La prueba se incorpora a Linux CI con obtención explícita del commit de referencia H2.6. Windows conserva los CTests y H3 del motor completo.

### Lo que esta extracción todavía no hace

Las coordinadoras clásicas siguen siendo **con estado**: llamar más veces a Sprites_Draw o GUI_Sidebar_Draw aún puede modificar el juego. Sprite_PrepareLegacyFrame usa registros temporales de recorte que el backend consume; no es un comando inmutable reutilizable.

Siguen pendientes encapsulación de dichos registros, estados de presentación de solo lectura, publicación entre hilos y pruebas 0/1/N. Paletas, buffers, refresco de HUD y callbacks auxiliares conservan sus rutas existentes; no se declara completada toda H4.1 ni H4.2–H4.6.

Siguiente bloque: preparar comandos de dibujo independientes de los registros globales y delimitar las actualizaciones restantes, conservando la secuencia clásica y verificando de nuevo H3.

**CI del cambio:** [Linux 39772995975](https://github.com/Cacheirez/openfodder/actions/runs/39772995975) y [Windows 39772996056](https://github.com/Cacheirez/openfodder/actions/runs/39772996056), **ambos completados con éxito**, con la evidencia final siguiente.

### Validación CI final del commit 4e4d57ef

- Windows 39772996056: compilación y CTests satisfactorios; report.json de replays PASS, 29 fases, cero omisiones, retorno 0.
- Linux 39772995975: compilación, CTests y prueba focalizada de **184.320 transiciones del temporizador** satisfactorios.
- H3 en ambas plataformas: PC Format 7.956 estados + Amiga The One 3.405; **11.361 estados coincidentes con el baseline original**, además de determinismo entre dos pasadas por campaña.
- Linux ASan/UBSan, LeakSanitizer y ThreadSanitizer: cada report.json muestra PASS, 29 fases, cero omisiones, retorno 0 y reasons vacío. Los engine.log examinados no contienen diagnósticos ASan, UBSan, LSan ni TSan.
- Se descargaron los ZIP de evidencia, comprobaron CRC y SHA-256 y leyeron los informes internos. SHA-256 Windows: `3a0ae910de4cb3cd705d0a471986c68c937d5a9d5ae5eea5b2bfde81f2290b8b`; Linux: `4bc235b3683828d72def03206257ae5819f812d51f6950d1fe90950aa3a6061a`.
- El workflow Windows generó el [paquete de demos](https://github.com/Cacheirez/openfodder/actions/runs/39772996056/artifacts/12422944078); no se exige a Miguel repetir ahora su validación manual de H2.6.

**Decisión:** primera extracción aceptada dentro de la cobertura demostrada. H4.1 continúa para los registros de dibujo y efectos restantes; no se declaran dibujos adicionales seguros ni 60 FPS implementados. PR sin fusionar y baseline clásica sin modificar.
