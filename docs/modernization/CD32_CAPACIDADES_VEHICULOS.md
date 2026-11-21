# CD32 — capacidades y estados de vehículos, primer incremento

26-10-2026. H8.3 con H4.2/H4.4. Fuentes inspeccionadas en `d42b052ea483c47b975fe894a9eb0a21e0c72fa7`. **Revisión estática parcial, no cobertura de ejecución.** No cambia el motor, sus referencias H3 ni la base clásica. El PR permanece en borrador y sin fusionar.

El [censo](CD32_CENSO_SPRITES.md) sigue siendo la referencia de presencia inicial. Este documento añade condiciones y relaciones; no sustituye sus recuentos. El [manifiesto verificable](evidence/cd32-vehicle-capabilities.json) fija fuentes por SHA-256, funciones, escenarios y tablas gráficas. Su comprobador detecta fuentes desactualizadas y relaciones inconsistentes, pero no demuestra jugabilidad ni causalidad por sí solo.

## Matriz de familias

Todos los nombres de función de esta tabla pertenecen a `Source/Sprites/Sprite_Helicopter.cpp` (H), `Sprite_Vehicle.cpp` (V) o `Sprite_Core.cpp` (C). Los IDs se contrastan con `Source/Sprites.hpp` y el despacho de `Source/Sprites.cpp`.

| Familia / IDs | Movilidad y control | Daño y ciclo de vida comprobados | Composición y fuentes |
|---|---|---|---|
| Helicópteros Human 49–52 | Voladores ocupables; los wrappers fijan tipo de vehículo y bando. Entrada por selección a altura cero, aproximación y proximidad; salida requiere aterrizaje y terreno aceptado | H::`Sprite_Handle_Helicopter_Human` deriva estados animados al manejador común; caída, humo y transformación a Explosion. No trasladar automáticamente la inmunidad a Hit del wrapper enemigo | H::`Sprite_Handle_Helicopter`: cuerpo 0x8B, rotor +1/0x8C, sombra +2/0x8D |
| Human Called 101–104 | H::`Sprite_Handle_Helicopter_*_Human_Called` ejecuta CallCheck y luego el wrapper Human. 101 está declarado pero ausente de los SPT censados | Misma ruta Human; `field_75` distingue llegada. No es un vehículo nuevo creado por la plataforma | H::`Sprite_Handle_Helicopter_Human_CallCheck`: objetivo de llamada, llegada con distancia <0x2C; fija `field_75=-1`, `mInVehicle=-1` |
| Helicópteros Enemy 40/42/43/44 | IA, búsqueda/retorno a posición de origen; el no armado omite la rama de ataque. Puede generar Enemy en la rama de altura cero | H::`Sprite_Handle_Helicopter_Enemy` anula `eSprite_Anim_Hit`; otros estados pasan al común. No significa inmunidad a todo daño | Mismos tres componentes y luz +3, tipo41; posición de luz depende del frame y conserva altura |
| Helicóptero Enemy2 107 | Wrapper Homing Enemy y condiciones de llamada adicionales | H::`Sprite_Handle_Helicopter`: si hay llamada, estado animado gira frames hasta el frame guardado y vuelve a None. Sin esa condición puede alcanzar la caída común; no clasificar como invulnerable absoluto | Rotor actualizado en esta rama especial; hay retornos tempranos, no asumir que todos los auxiliares se recalculan siempre |
| Plataforma 99 | Fija, activador; no ocupable como vehículo | H::`Sprite_Handle_Helicopter_CallPad` no implementa aquí una ruta de destrucción. Respuesta global a todos los impactos pendiente | Hoja0xE7, orden First; animación de llamada. InRange omite soldados ocupados o con estado animado |
| Jeep Human 63/64; Enemy 80/81/82 | V::`Sprite_Handle_Vehicle`: desplazamiento terrestre, gravedad, saltos, terreno. 63/80 Jeep; 64/81 JeepRocket; 82 DontTargetPlayer y objetivo adelantado | C::`Sprite_Animation_SlideOrDie`: Die1/Die3 → Explosion, elimina auxiliares. V::Terrain_Check añade caída, rebote y hundimiento; mRowsToSkip no es solo decoración | Cuerpo0xA5 y sombra +1 por C::`Sprite_Shadow_Update_From_Height`; Enemy añade luz +2. 64 usa `Vehicle_Handle_Cannon_Fire`/`Sprite_Create_Cannon`, no inferir proyectil del nombre JeepRocket |
| Tanque Human65 / Enemy69 | V::`Sprite_Handle_Tank`: terrestre, giro, terreno; torreta orientable independientemente | Ambos wrappers anulan Die1; otros estados llegan a SlideOrDie. Die3 conserva ruta de destrucción. No llamarlo indestructible | Cuerpo0xD1; +1/0xD2 por `Sprite_Vehicle_Turret_Update`, altura+9; Enemy añade luz +2. `Sprite_Handle_Tank_FireMissile` usa el auxiliar para disparar |
| Torretas Human78/79; Enemy84/85/105 | V::`Sprite_Handle_Turret`: sin traslación propia en este manejador, orientación y disparo; Human exige vehículo actual para apuntar | En CF1 Moors/Int anula **Die1**; Die3 sigue transformando a Explosion. Fuera de esos entornos Die1 también destruye. El comentario «can't be destroyed» no sustituye las ramas reales | Hoja0xD2; Enemy luz +1. Wrappers 78/84 seleccionan Turret_Cannon, 79/85 Missile, 105 Homing; `Sprite_Handle_Turret_Fire` crea Missile o MissileHoming. No deducir munición del enum Cannon |

CF2 111–117 queda fuera de esta matriz CD32. Los tipos 112/113 no se necesitan para explicar la resistencia condicional de las torretas CF1.

## Entrada, ocupación y aterrizaje: condiciones separadas

| Paso | Condición exacta observada | Fuente |
|---|---|---|
| Descubrimiento | Slot no libre (`mPosX != -32768`), Human y `mVehicleEnabled`; lista cacheada | V::`Sprite_Find_HumanVehicles` |
| Seleccionar destino de entrada | Escuadra seleccionada; slot presente, habilitado, Human, altura cero y clic dentro de caja lógica. Asigna `mVehicleWalkTarget` a los miembros | `Source/Squad.cpp::Squad_Assign_Target_From_Mouse` |
| Entrar | Objetivo asignado y distancia calculada <0x0D; asigna `mCurrentVehicle`, `mInVehicle=-1`; líder inicia temporizador0x190 | V::`Sprite_Handle_Player_Enter_Vehicle`; `Sprite_Troop.cpp::Sprite_Handle_Player` lo llama tras filtros de animación/fin de misión |
| Permanecer dentro | Soldado usa hoja0x7C/frame0 y sigue posición/altura del vehículo | V::`Sprite_Handle_Player_InVehicle` |
| Vehículo destruido | Slot libre o tipo Explosion: borra referencias de ocupación y coloca Hit en soldado, con dirección aleatoria | Misma función; preservar RNG y ejecución original |
| Solicitar salida en vuelo | Clic dentro de caja del vehículo actual Human, altura no cero: marca `mInVehicle=-1` **en el vehículo** y deshabilita entrada de control | V::`Vehicle_Try_Exit_On_Mouse` |
| Descenso | Cerca del objetivo, Human con esa marca: resta0xC000 de altura fija, acota a cero; hay rama de corrección según terreno | H::`Sprite_Handle_Helicopter`, `Sprite_Handle_Helicopter_Terrain_Check` |
| Salir en tierra | Altura cero y consulta de terreno aceptada; limpia vínculos de los soldados de la escuadra y asigna posiciones/objetivos de salida | V::`Vehicle_Try_Exit_On_Mouse` |

**No hay una comprobación universal de «plazas libres» en estas funciones.** No inventar capacidad máxima o exclusividad sin seguir las rutas de escuadra. `mInVehicle` en soldado expresa ocupación, pero en vehículo participa en aterrizaje/salida: el contrato semántico debe separarlos. `mOwnerSprite` tampoco significa siempre padre visual: en `Sprite_Create_MissileHoming` apunta al objetivo del misil.

La llamada requiere que el número de plataformas pulsadas coincida con el total, que aún no haya destino y una tropa válida (`Sprite_HelicopterCallPad_Check`). InRange exige distancia <9 y tropa no ocupada/sin animación. Called no equivale a aparición dinámica: esos helicópteros ya existen en SPT y CallCheck cambia su destino.

## Grafo parcial de auxiliares y entidades dinámicas

| Origen → resultado | Relación y condiciones | Fuente |
|---|---|---|
| Helicóptero → rotor/sombra | Slots +1/+2; durante funcionamiento normal se dejan como Null, aunque sus hojas se dibujan. Null no implica ausencia gráfica | H::`Sprite_Handle_Helicopter_Human`, `Sprite_Handle_Helicopter_Enemy`, `Sprite_Handle_Helicopter` |
| Helicóptero Enemy → luz41 | Slot +3, actualizado por frame del cuerpo | H::`Sprite_Handle_Helicopter_Enemy` |
| Helicóptero → granada2 / misil45 / guiado97 o46 | Creación condicionada por arma, altura, objetivo, contadores y slots. Human dispara por encima de0x1F; guiado sin bloqueo recurre a Missile | H::Human_Deploy_Weapon; `Sprite_Projectiles.cpp::Sprite_Create_Grenade2`, `Sprite_Create_Missile`, `Sprite_Create_MissileHoming` |
| Misil guiado → sombra3 | Reserva dos slots, segundo ShadowSmall; Human crea MissileHoming2(97), AI MissileHoming(46) | `Sprite_Create_MissileHoming` |
| Helicóptero en caída → humo57 | Creación exige mWasDrawn y slot libre; puede consumir RNG | H::`Sprite_Handle_Helicopter`; `Sprite_Effects.cpp::Sprite_Create_Smoke` |
| Helicóptero destruido → Explosion12 + PropCrash53 | Mismo slot del cuerpo cambia de tipo; rotor +1 cambia a53; sombra +2 destruida, luz según indicador. Human se retira de lista de vehículos | H::`Sprite_Handle_Helicopter` |
| PropCrash53 → Explosion12 + FireTrail48 | Handler cambia a Explosion tras movimiento; no inventar una larga animación autónoma de rotor caído por su nombre | H::`Sprite_Handle_Helicopter_PropCrash`; `Sprite_Projectiles.cpp::Sprite_Create_FireTrail` |
| Helicóptero Enemy → Enemy5 | Rama en suelo y decisión aleatoria; creación pendiente de observación por replay | H::`Sprite_Handle_Helicopter_Enemy` |
| Jeep/tanque → humo57 / hundimiento86–87 | Humo y efectos de hundimiento dependen de visibilidad lógica/slots; 86 usa0xDE y87 usa0xDF | V::`Sprite_Handle_Vehicle`, `Sprite_Handle_Tank`, `Sprite_Handle_Vehicle_Sinking` |
| Jeep armado → Cannon77 | `Vehicle_Handle_Cannon_Fire` llama a creador con contador y disponibilidad de slot; no confundir con torreta estacionaria | V::`Sprite_Create_Cannon` |

Esta lista no cierra todos los descendientes (explosiones secundarias, impactos, enemigos, proyectiles y tiles). No volver a ejecutar creadores al presentar: modifican slots, contadores y RNG. El inventario de terreno/destrucción permanece separado (`Tiles.cpp`, `MapRuntime`, hit/bht/swp); no convertir las capacidades de sprites en flags de tiles.

## Recursos y variantes del primer compuesto

`Graphics_Amiga.cpp::Map_Load_Resources` llama al decodificador real `DecodeIFF`: Copt → IN_GAME2, Army → IN_GAME1. La tabla CF1 es `mSpriteSheetTypes_InGame_Amiga`, no CF2 ni TheOne. Se debe conservar el recurso seleccionado por el mapa; no usar un atlas de jungla para todos los entornos.

| Componente | Hoja / tabla | Frames declarados | Geometría relevante |
|---|---|---:|---|
| Cuerpo | 0x8B / stru_8D798 | 16 | mColCount3; alturas32 salvo frame7 de30 con mModY2. No fijar un anclaje uniforme ignorando metadata |
| Rotor | 0x8C / stru_8D898 | 4 | mColCount3, filas16; posición Y+1 y altura del cuerpo+14 |
| Sombra | 0x8D / stru_8D8D8 | 3 | columnas3/2/2, filas11/7/5; frame min(altura>>4,2), desplazamiento por altura y orden First |

Los recuentos de columnas son unidades de la tabla Amiga, **no anchuras finales en píxeles**. Para exportar utilizar layout/planos y raster real, no recortar el LBM con estas cifras como si fueran píxeles. El rotor avanza módulo4, condicionado por altura, paridad del tick y actividad; no darle un reloj cosmético que cambie la animación lógica.

## Escenarios propuestos: presencia acreditada, ejecución pendiente

| Mapa (misión/fase) | Entorno | Tipos de interés | Captura pendiente |
|---|---|---|---|
| mapm30 (11/3) | jun | 50 | Entrada, despegue, vuelo, aterrizaje, salida; compuesto original |
| mapm36 (12/6) | ice | 99,102 | Todas las plataformas, llamada, llegada y ocupación |
| mapm38 (14/1) | des | 52 | Guiado con/sin blanco y auxiliares de proyectil |
| mapm42 (15/2) | mor | 49 | Granada, caída, rotor desprendido y ocupantes |
| mapm49 (18/3) | int | 51 | Misil, anclajes y paleta interior |
| mapm52 (19/1) | int | 99,103 | Called armado |
| mapm72 (24/6) | int | 99,104,107 | Called guiado y rama de recuperación Enemy2 |

La selección abarca los cinco recursos base, no todas las combinaciones de estados/armas. El manifiesto comprueba presencia, misión/fase y recursos contra el censo. Ninguno de estos escenarios se ha ejecutado en este incremento. Las muestras de daño deben grabarse con entradas reales, sin inyectar estados ni alterar la dificultad para producir una imagen.

## Contrato semántico mínimo propuesto — aún no implementado

1. Identidad `(sceneEpoch, slot, generation)` propia de presentación. La generación cambia al asignar/reutilizar slot; no basta comparar puntero o tipo. `Sprite_Get_Free_Max42` limpia slots con Clear y `Sprite_Destroy` marca retirada pendiente. Auditar todas las asignaciones antes de instrumentar; no introducir campos en la traza lógica ni consumir RNG.
2. Captura coherente bajo la serialización existente: tick lógico, revisión de escena/cámara, posición fija X/Y/altura con fracciones, dirección/frame y rol. Distinguir ocupante, vehículo, objetivo de misil y componente visual; transformar referencias en IDs propios, no conservar punteros.
3. Tipo actual y continuidad de pose separados de generación: cuerpo→Explosion y rotor→PropCrash interrumpen interpolación aunque el slot no se libere. Pausa, carga, cambio de fase y saltos de cámara invalidan continuidad.
4. Cada operación mantiene orden real, destino, recorte, mRowsToSkip, paleta efectiva tardía, recurso propio, hoja/frame y mModX/mModY. Agrupar por entidad no autoriza reordenar sombra/rotor/luz ni deduplicar escrituras.
5. Primer piloto: un soldado en demo pública reproducible. Capturar identidad/cámara/posición junto al productor real, reproducir el recurso original y contrastar con H3 y el compositor vigente. Después una pose sustituible con retorno al original; helicóptero como siguiente compuesto. No esperar a cerrar todo el catálogo.

## Preparación de captura privada y pendientes

Se localizaron de nuevo los datos privados históricos; no se copiaron a Git ni se regeneró el censo. La extracción sigue pendiente: cargar fase con el decodificador real, capturar los recursos propios y metadata resuelta en el productor existente, guardar privadamente índices + RGB efectivo y generar hojas de contacto etiquetadas por entorno, componente, dirección/frame, altura, daño y ocupación. Debe contrastarse cada captura con la ruta clásica antes de utilizarla como referencia artística. Una hoja con los 16 frames del cuerpo no acredita entrada/salida ni todos los estados dinámicos.

Siguiente incremento: instrumentar el piloto semántico mínimo del soldado y sus discontinuidades; ampliar el grafo/capturas de vehículos por lotes. Pendientes todas las observaciones de juego de esta matriz, capacidades de las demás familias, tiles y catálogo artístico. H4 y H8 siguen abiertos; H6 conceptual puede avanzar.

## Verificación de este incremento

`python3 tools/modernization/check_cd32_vehicle_capabilities.py` verifica hashes de fuentes, símbolos, tablas/frame counts y relaciones de escenarios con el censo existente. Las pruebas negativas alteran fuente, presencia y tabla para comprobar rechazo. No ejecuta una simulación alternativa ni afirma probar aterrizaje/daño real. No se recompila ni repite la batería del motor por este cambio de documentación/herramienta.

Resultado local: **25 pruebas Python PASS**, incluidas seis del manifiesto (cinco negativas); comprobador PASS sobre 12 fuentes, siete escenarios y tres componentes. Comprobación de metadata gráfica existente: 1.309 entradas PC/Amiga PASS. `git diff --check` sin incidencias. Estos resultados no son replays ni una compilación nueva.

Al iniciar: HEAD d42b052e; PR abierto/draft/no merged; base clásica5e6a4f38 confirmada por API. Windows40279655995 success. Linux40279655989 in_progress en ASan/UBSan tras superar H3 y misión/pausa; sin conclusión global en esa consulta. Los fallos históricos y la incidencia de escritura local permanecen registrados en sus informes.


### Corrección de portabilidad del comprobador

Windows run40317433141 (commit d12cbba9) falló antes de compilar: las cinco pruebas que necesitaban fuentes válidas rechazaron Sprite_Helicopter.cpp por hash diferente. Los checkouts CRLF reproducen el fallo; la huella de revisión ahora normaliza **solo CRLF→LF**, manteniendo significativos el resto de bytes y los saltos adicionales. Los SHA de referencia y H3 no se regeneran. JSON se lee explícitamente como UTF-8. Dos pruebas añadidas aceptan el mismo contenido CRLF y rechazan un cambio real de hoja0x8B→0x8C incluso con CRLF. Resultado local: 27 pruebas PASS; nueva CI pendiente. Se conserva el fallo Windows como evidencia histórica, no como fallo del motor.
