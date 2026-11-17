# A.1 — Reevaluación de daño y piloto 0x2D

17-11-2026. Continúa la autorización de Miguel para daño/granadas/sombras del hito de continuidad. Fuente de entrada `5b949a9`. No cambia simulación, selección de dirección/frame, altura, RNG, reloj ni referencias. Una sola dirección y sus dos poses; **el piloto queda aislado, sin activación en el lanzador**. Aceptación artística/jugable pendiente.

## Lo que falta tras integrar granadas

La base de esta reevaluación es el ciclo de [granadas y sombras](DEMO_A1_GRANADAS_SOMBRAS.md), con 198 activos/363 vínculos. Se estudian los tres registros retenidos, incluyendo las dos escenas del último registro y sin considerar publicados los comandos de intervalos rechazados.

Las ocho direcciones observadas del segundo grupo de daño/muerte usan `0x28, 0x29, 0x22, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F`. La selección original comparte `0x22` con otra rama. Hay 34 claves observadas del grupo y el marcador `0x7C`; cubrir una dirección aislada puede abrir nuevos tramos HD que terminan en otra dirección faltante.

Se comprueban dos dependencias sin generar arte ni activarlas:

- **Caída `0xB0/F0`:** la clave `f62237ff841552359982d169df42a32f8c9270f598af5e624f6cf7db3a3abb06` coincide exactamente con la fuente, geometría y paleta de la caída ya aprobada; cambia animación 0→1. Clave y raster contrastados por el renderizador C++. Puede reutilizar arte cuando se integre un conjunto coherente.
- **Jugador invisible `0x7C/F1`, animación 6:** clave `82a12b8640bd…`, snapshot real del replay, hash/clave/raster verificados y bytes de sus planos a cero. No se añade una exención general de cuerpos. La conservación futura debe comprobar ausencia de escrituras y recuperación; no se activa esta clave aquí.
- **Otro marcador invisible antiguo `8ccb9e19db5e…`:** la plantilla disponible no reconstruye su clave. Se confirma F1 y se acota la búsqueda a los estados conocidos; no se amplía por ensayo de paletas/personas. **PENDIENTE de captura nativa completa**, sin aprobar el recurso por su hoja o apariencia supuesta. Recuperar mediante el diagnóstico local ampliado cuando se reproduzca; los datos actuales no bastan para certificarlo.

Activar solo las dos dependencias verificadas empeora retornos y rachas en las tres muestras; por ello permanecen preparadas como datos, sin modificar el candidato de juego. La proyección del conjunto completo de ocho direcciones **más** las dos dependencias verificadas, manteniendo bloqueado el marcador antiguo desconocido, es:

| Registro | Base: publicaciones / retornos / rachas breves | Conjunto completo hipotético |
|---|---|---|
| Caídas 16:13 | 8.012 / 8 / 0 | 8.438 / 5 / 0 |
| Nado 17:32 | 12.937 / 13 / 5 | 13.294 / 7 / 0 |
| Impacto 19:54 | 7.276 / 4 / 0 | 7.777 / 0 / 4 |

Son **proyecciones de cobertura**, no arte entregado, pruebas de composición o aceptación visual. Ninguno de los 256 subconjuntos del grupo, con las dependencias verificadas, mejora simultáneamente retornos y la cuenta bruta de rachas en las tres muestras. Las cuatro rachas breves del último registro acaban en intentos `13484`, `13496`, `13508`, `13520`, todos `no-body`, sin faltantes y con cero jugadores presentes; no contienen retorno del mismo jugador moderno. La cuenta bruta se conserva en la tabla: se distingue el fin de escena de una interrupción de un actor, sin falsear un PASS global. Esta evidencia justifica preparar un piloto visual, no activar una selección parcial ni producir todas las direcciones sin revisión.

## Piloto de una dirección

Se elige atrás/derecha `0x2D`, frecuente en la captura reciente y con sus dos rasters reconstruidos. Claves verificadas: F0/animación 1, F1/animación 1 y F1/animación 6. Los dos estados de F1 tienen el mismo raster nativo. Celdas de 16×14; cajas nativas F0 `[3,0,13,12]`, F1 `[4,1,15,12]`, con coordenadas derecha/abajo exclusivas. Las imágenes no sustituyen esos selectores ni añaden animación ligada a FPS.

- [F0: maestro, prompt y manifiesto](../../assets/modernization/demo-a1-player-hitdeath-2d-f0/README.md).
- [F1: maestro, prompt y manifiesto](../../assets/modernization/demo-a1-player-hitdeath-2d-f1/README.md).

Se usa `image_gen` integrado: nativo de esta dirección, marcha D5 verde A y C01 como referencias. F0 necesitó una corrección focalizada para eliminar el brillo del impacto; F1 deriva de ese maestro provisional y de su nativo. Se conservan originales y prompts. Ninguna marcha, granada o pose aceptada se regenera. Los maestros de 1254×1254 RGBA se exportan con los constructores existentes a 8×/12×, respetando las cajas nativas y con alfa real. La marca roja es una interpretación provisional del acento nativo, pendiente de valoración artística.

**Contenido preparado:** dos maestros, cuatro derivados PNG/RGBA, tres vínculos exactos. Candidato de ensayo `hitdeath-2d-candidate/`: 202 activos/366 vínculos; conserva los 198 activos y 363 vínculos de granadas. **El lanzador mantiene `granada-candidate/` con 198/363**. No se incorporan las dependencias ni este piloto al juego normal para evitar una activación parcial con regresión de continuidad.

## Validación técnica y sombras

**PASS focalizado:** las tres claves reales, dos poses y dos densidades pasan los fixtures WindowHD/SDL software en Windows Clang 23.1.5 ASan/UBSan y Linux Clang 18.1.3 ASan/UBSan/LSan: dos actores HD, clave incorrecta rechazada y recuperación clásica íntegra ante error SDL. Se comprueban dimensiones, alfa, colocación y hashes por la exportación determinista y el constructor de activos.

**PASS con sombras independientes:** las mismas poses se prueban a alturas lógicas 0 y 12, en ambas densidades y plataformas: 24 casos de pareja cuerpo/sombra. Dos sombras tipo 22 se dibujan antes de los cuerpos con la fórmula nativa `X+5+(h>>2)`, `Y-3+(h>>2)`, altura propia cero, F1 para h≤8 y F0 para h>8. Se contrasta salida SDL completa con la composición calculada y se inyecta fallo SDL para recuperar toda la imagen clásica. No se dibuja sombra proyectada dentro del PNG del cuerpo.

Las máscaras completas verificadas tienen **11 escrituras en F0 y 24 en F1**. Una expectativa inicial de siete para F0 confundía un caso de campaña recortado con el recurso completo: se corrigió tras contar independientemente los planos nativos y cotejar el raster. No se alteraron recursos ni controles del motor. En altura cero puede quedar sombra ocluida por las celdas de cuerpo; en altura 12 se exige sombra expuesta fuera de ellas. Que existan comandos correctos no acredita coherencia artística final de cuerpo HD/sombra clásica.

No se repiten H3 ni matrices de CI para este piloto aislado sin código del motor ni activación nueva. H3 del binario de granadas ya conserva 11 fases/11.361 estados; CTest y A2/H3 Windows/Linux del código están comprobados. La CI completa del código se consulta aparte; no se atribuye PASS antes de observarla. GPU, audio, CD32, reproducción jugable del piloto y aceptación visual quedan **PENDIENTES**.

## Recuperación y siguiente acción

Carpeta local del 17-11 `C:/Users/migue/.codex/visualizations/2026/11/17/01a1ea7b-b727-78f2-a6ac-a4b32dc39150/`: `project_death_after_grenades.py`, `inspect_damage_dependencies.py`, `prepare_death_2d_native.py`, `export_hitdeath_2d.py`, `death-2d-native/`, `hitdeath-2d-candidate/`, `run-hitdeath-linux.sh`, `run-hitdeath-shadow-*`, los fixtures y logs por estado. Datos originales fuera de Git. [Evidencias, hashes y límites](evidence/dano-piloto-2d-20261117.json).

**Siguiente tarea única:** Miguel revisa F0/F1 del piloto: orientación, forma/tamaño, lectura de impacto, desplazamiento entre poses y adecuación al estilo C. Es aceptación artística, no una nueva solicitud de permiso general. Tras esa decisión se puede continuar dentro del hito autorizado, una dirección por microbloque, sin activar conjuntos que provoquen alternancia adicional. La revisión jugable del ciclo de granadas y la captura del marcador antiguo permanecen pendientes.

Próximos pasos: (1) revisión visual de este piloto, **AUTORIZADO / pendiente de Miguel**; (2) obtener procedencia completa del marcador antiguo y verificar las dependencias antes de integrarlas, **AUTORIZADO / pendiente de datos**; (3) continuar las direcciones de daño con el diseño que acepte Miguel, **AUTORIZADO / condicionado a esa aceptación**; (4) validar e integrar un conjunto con continuidad medida y revisión jugando, **AUTORIZADO dentro del hito**, sin nuevos escenarios, B, scroll ni 16:9. No iniciar automáticamente arte de otras familias.
