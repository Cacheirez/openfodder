# Catálogo de protagonistas CF1 — investigación de fuente

21-11-2026. R1 del hito PROTAGONISTAS-COMPLETOS autorizado por Miguel. Este inventario fija el espacio de poses de la fuente; **no declara completado el arte ni la integración**. [Catálogo verificable](evidence/player-state-catalog-v1.json), generador `tools/modernization/inventory_player_states.py`, cuatro pruebas de contrato y comprobación de deriva incorporadas a CTest.

## Cierre de estados y selección

Se enumeran los 14 estados nativos None, Hit/Hit2/Hit3, Die1/Die2/Die3/Die4/Die5, Slide1/Slide2/Slide3 y Vehicle_Enter/Vehicle_Inside. Sus rutas se cruzan con los nueve grupos humanos y las asignaciones directas de `Sprite_Handle_Soldier_Animation`, `Sprite_Handle_Player_MissionOver`, `Sprite_Update_Direction_Anim`, entrada/ocupación de vehículo y cadáver flotante. Las funciones y las tablas de ambos formatos quedan referenciadas por ruta, línea y hash; cambios en la fuente invalidan el catálogo comprobado.

| Familia | Selección | Observación relevante |
|---|---|---|
| Marcha | 0x00–0x07, F0–F2 | ciclo nativo 0–1–2–1 y variantes, sin reloj de pantalla |
| Daño con override | 0x20–0x27 | 0x22 compartida con el grupo siguiente; PC 0x20 tiene una sola fila válida |
| Daño balístico | 0x28/0x29/0x22/0x2B–0x2F | dos frames, altura y sombra independiente |
| Locomoción baja | 0x30–0x37, F0–F2 | rama del modo de pelotón 0; no clasificar como muerte por el comentario `Death-3` |
| Agua | 0x18–0x1F, F0–F1 | selección de frame y recorte propios |
| Granada | 0x08–0x0F, F0–F2 | secuencia independiente del proyectil y su sombra |
| Apuntado bajo | 0x10–0x17, F0 | depende de objetivo/seguimiento/modo, no solo reposo |
| Cohete | 0x39–0x40 | filas F0–F2 inventariadas; fila F3 de 0x3E declarada pero sin selector legítimo |
| Caída | 0xB0–0xB7/F0 | rama separada; algunos bitmaps se comparten con la locomoción baja |
| Desangrado prolongado | **0x21/F0–F1, Die5** | temporizador `field_3A`; cambia F0/F1 al crear sangre; no es el grupo 0x28 ya preparado |
| Saludo/hundimiento | 0x38/F0–F5 | contextos distintos con el mismo cuerpo; conservar recorte |
| Salto final | 0x41/F0–F5 | altura derivada del frame, sombra independiente |
| Celebración | 0x9F/F0–F3 | secuencia 0,1,2,3,2,1,2 |
| Deslizamiento | 0xA4/F0–F7 | cuantización nativa de dirección; no reflejar arte |
| Entrada en vehículo | 0xCC/F4→F0 | cinco frames, después oculto |
| Oculto/intermitencia/ocupante | 0x7C/F0–F1 | no necesita dibujo nuevo; exige verificar ausencia de escrituras |
| Cadáver flotante | tipo 27, 0x9E/F0–F1 | el manejador retiene frame inicial; se incluyen ambas filas declaradas de forma conservadora |

Las condiciones espaciales, recortes/altura, visibilidad, estado de daño y animación no multiplican automáticamente el número de dibujos. Tampoco autorizan sustituir otra pose parecida: la forma nativa y el contexto de la acción siguen teniendo que corresponder.

## Denominador y arte existente

Amiga/CD32: **189 pares visibles inventariados**, PC: **188**, más dos marcadores invisibles por formato. La diferencia de PC es la fila inexistente de 0x20; el código clásico ya rechaza frames sin metadatos. Una fila adicional 0x3E/F3 se registra como sobrante, sin inventar un estado para ella. Los casos conservadores quedan identificados, sin presentarlos como observación de ejecución de todas las ramas.

**111 pares tienen maestro existente.** Otros tres tienen una coincidencia exacta de metadatos con un dibujo de otra acción; se registran como candidatos de reutilización, no como arte automáticamente correcto. Quedan 75 pares Amiga y 74 PC sin maestro; algunas filas sin maestro comparten el mismo bitmap entre sí. La autoría deberá resolver el contexto, además de la igualdad de bytes.

Las entradas de protagonistas de las tablas Amiga retail y The One son exactamente iguales. Las únicas diferencias entre esas dos tablas completas son 0xA0/0xA1 (textos), que no se mezclan ni se consideran cuerpos. Esto acredita contrato de fuente para CD32; no sustituye una prueba con datos comerciales CD32. Los directorios de prueba localizados contienen demos públicas, no datos retail.

## Por qué no bastan más hashes de partida

`SoldierVariantKey` incluye estado de animación y los 255 colores, incluso los no usados por el cuerpo. Un mismo dibujo puede adquirir numerosas claves al recibir daño o cambiar otros colores. Además, el experimento conserva recursos asociados/enemigos solo en M1P2; un faltante ajeno al cuerpo provoca recuperación de toda la escena. Ningún número de poses nuevas, por sí solo, resuelve esas dos limitaciones.

R2 debe resolver por pose nativa verificada, con identidad de recurso y geometría, sin usar un estado lógico o un color no usado como otro dibujo. Debe conservar en orden los comandos clásicos completos y verificables de otros elementos, sin promover datos desconocidos ni ocultar fallos reales. Los cuerpos de otras acciones no se fusionan solo porque el original reutilice memoria. Sombras de propietario/altura, marcadores sin escrituras y estados finales requieren contratos explícitos.

## Límites y siguiente trabajo

R1 no modifica selectores, RNG, física, reloj ni referencias. Las pruebas de regeneración de catálogo/contrato pasan en Windows y Linux; H3 válido anterior se conserva, sin repetirlo por investigación. La siguiente tarea única es R2, resolución sistemática y procedencia nativa. Después se completará automáticamente el arte que falta por dirección/familia y la integración de todos los estados, según la autorización de Miguel; no se pide revisión parcial para continuar.

CF2, enemigos y vehículos como nuevas familias artísticas, nuevos escenarios, fase B, scroll y 16:9 quedan fuera. El cuerpo del protagonista al entrar en un vehículo pertenece al hito; el vehículo no. Las pantallas de menú/reclutamiento no se confunden con la máquina de estados jugable y deben permanecer identificadas como contexto separado en cualquier afirmación de cobertura.

## Corrección de alcanzabilidad R3 — 21-11-2026

La investigación inicial conservadora incluía las 24 filas 0x30–0x37 de cada formato. La revisión de sus productores demuestra que pertenecen al modo de pelotón cero: las cinco posiciones de `word_3BED5` solo se escriben con 2; el jugador carga ese valor antes de la selección normal. El reinicio a cero de la variable temporal no constituye una selección humana de ese modo. Las caídas reales seleccionan B0–B7/F0 mediante otra rama. No se crean cuerpos modernos para las siluetas rojas de una rama inactiva.

Se conservan las **385 filas como auditoría de fuente**, con una marca explícita de producción: **337 entradas requeridas** (165 cuerpos Amiga, 164 PC, cuatro ocultas y cuatro sombras con propietario), más **48 declaradas sin productor actual**. El contrato completo exige las 337 y rechaza vincular las inactivas; una aparición inesperada conserva la recuperación segura por faltante. La prueba invalida la auditoría si aparece otra referencia/escritura de modo y rechaza expresamente una nueva escritura cero. No cambia el motor ni reduce los requisitos de sus estados reales.

PASS: seis pruebas Python y 15.348 casos de resolución/mutación por sistema con ASan/UBSan; LSan en Linux. Los cinco maestros recientes de 0x30/F1–F2 y 0x31/F0–F2 coinciden con B1–B5 en tabla y raster privado: se integrarán mediante revisiones explícitas, sin generar imágenes nuevas. Tras ello quedan 35 cuerpos reales por crear y las dos sombras independientes. Los recuentos anteriores de 385 entradas se conservan como resultados históricos del inventario conservador. [Evidencia y límites](evidence/player-pose-reachability.json).

## Entrada en vehículo — contraste por formato

CC/F4–F0 no son cinco posturas humanas adicionales. En PC, el recurso retenido contiene cinco pequeños efectos grises (13, 53, 30, 15 y 5 píxeles en el orden de reproducción); se modernizarán como transición, sin dibujar un cuerpo inventado. En Amiga The One, los cinco rasters están vacíos. El lanzador `PROBAR_REINICIO_P1` usa esa campaña pública. El contador y el movimiento del actor se conservan; después se selecciona 7C/F0.

La clasificación depende del formato y exige procedencia/hash del recurso completo, firma nativa y ausencia real de escrituras para conservar un paso invisible. Una prueba negativa firma deliberadamente recursos no vacíos y comprueba que los nueve contratos ocultos los rechazan por escrituras, no solo por un hash desconocido. No se generaliza el vacío a datos comerciales CD32 no inspeccionados. La primera hipótesis de vacío en ambos formatos fue rechazada por el constructor y su salida fallida nunca se activó.

Se conservan 337 entradas obligatorias: 160 cuerpos Amiga, 159 PC, cinco efectos PC, nueve pasos sin escrituras y cuatro sombras con propietario. PASS seis pruebas Python, 15.357 casos CPU por sistema y 96 Window/SDL por sistema con sanitizadores. Candidato aislado 338 activos / 324 entradas, trece pendientes. Faltan dos cuerpos flotantes, cinco efectos PC y dos pinturas de sombra independiente; después R4 debe cualificar sombras/continuidad y R5 validar el conjunto. [Evidencia](evidence/player-vehicle-transition-audit.json).
