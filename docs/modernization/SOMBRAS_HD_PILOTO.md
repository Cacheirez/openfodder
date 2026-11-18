# SOMBRAS-HD-PILOTO — una marcha con sombra recuperada

18-11-2026. Hito de continuidad **en curso**. La aprobación visual de Miguel de las siete direcciones nuevas de daño cierra esa revisión; registrada en `b6a7171`. Este piloto mínimo estaba autorizado por el plan `ea730de`. **Muestra preparada y comprobada técnicamente; aceptación artística pendiente.** No se activa en el juego normal ni se extiende a otras poses.

**Valoración posterior:** Miguel rechaza la posición de la primera muestra y considera que la intensidad puede ser adecuada. La versión vigente para revisión es [V2, cola inferior derecha](#revisión-2--posición-inferior-derecha). La primera muestra y sus pruebas se conservan como referencia histórica.

## Pose y evidencia nativa

Aliado Amiga The One, marcha frontal `0x00/F1`, animación 0, paleta 0, celda 16×14 y ancla `[0,14]`. Clave exacta `7917be958aed8713b310fcb3da2a50fc49cdf2121f3693c2f6a60a14e7f29670`, reconstruida mediante el renderizador C++ a partir de una captura real del replay retenido. El fichero y el recurso completo permanecen locales; sus hashes constan en la [evidencia](evidence/sombras-hd-piloto-20261118.json).

El raster contiene una componente oscura inferior de 16 píxeles `(16,32,0,255)`:

| Fila lógica | Columnas incluidas |
|---|---|
| 11 | 5–11 |
| 12 | 6–11 |
| 13 | 8–10 |

La extensión inferior derecha es visible en el original y falta en el HD actual. Se utiliza esa componente como **máscara acotada del piloto**. La separación artística exacta entre contacto del pie y sombra dentro del oscuro nativo no es una etiqueta de los datos; no se presenta como segmentación universal ni se extrapola a otras poses. El desplazamiento procede del raster, sin añadir un offset elegido a ojo.

En `Sprite_Troop.cpp`, la rama ordinaria de animación 0 sale antes de la creación de sombra asociada al daño. `Sprite_Create_Player_Shadow` y su manejador mantienen su ruta independiente. El reanálisis de la traza retenida conserva **6.170 estados ordinarios de aliado con `has_shadow=0`**. Esa traza no exporta hoja, altura ni identidad de propietario: no permite certificar el emparejamiento exacto de esta pose durante todo el vuelo. Se diferencia esa limitación del raster y de las pruebas de composición.

## Recurso y comparación

[Activos, compositor offline, prompt y manifiesto](../../assets/modernization/demo-a1-shadow-walk-00-f1/README.md).

`image_gen` integrado genera **solo un maestro de pintura de sombra**, RGBA 1254×1254; referencias: nativo y HD actual de esta pose. Recorte alfa explícito `[373,540,916,751]`. Se emplea el constructor existente para derivarlo en la zona lógica `[5,11,12,14]`, limitada después a los 16 píxeles de la máscara. El pequeño `compose.cpp` de autoría offline combina **cuerpo existente sobre sombra** con alfa recto. No es código del motor ni una capa añadida sobre la escena terminada.

Se obtienen dos activos finales, 128×112 y 192×168, para **una sola clave**. Todos los píxeles opacos del cuerpo y todos los píxeles fuera de la máscara permanecen exactamente iguales. Los semitransparentes del borde pueden mostrar la sombra por debajo, como corresponde al orden de composición. Cambian 882 píxeles a 8× y 1.959 a 12×; de ellos, 438 y 991 incorporan sombra donde el cuerpo era totalmente transparente. Las geometrías y el ancla permanecen intactos. El original y el lanzador normal no se sobrescriben.

La comparativa **original / HD actual / HD piloto** a 8× y 12× está en:

`C:/Users/migue/.codex/visualizations/2026/11/17/01a1ea7b-b727-78f2-a6ac-a4b32dc39150/shadow-walk-pilot/comparativa-sombras-8x-12x.png`

Es un **montaje diagnóstico fuera del juego**, con la misma celda/ancla sobre un recorte de fondo real retenido (`C01_12_fondo.bmp`, origen y SHA-256 registrados). No es una captura del piloto publicado jugando. Nativo, fondo y comparativa completa permanecen locales, fuera de Git. La comparación permite valorar fuerza, borde, color, apoyo y desplazamiento de la sombra sin cambiar el cuerpo aprobado.

## Pruebas y límites

**PASS técnico focalizado:**

- Exportación y hashes exactos, alfa real, cambios limitados a la máscara y cuerpo opaco intacto a 8×/12×.
- El compositor offline produce los mismos bytes en Windows y Linux, con ASan/UBSan y LSan en Linux.
- **56 casos Window/SDL software**: dos actores, densidades 8×/12×, estricto/híbrido y siete casos por plataforma: superposición entre actores, escritura posterior de cero, escritura anterior cubierta por cuerpos, borde derecho, borde inferior, Save/Restore y tres filas omitidas. Salida completa contrastada con composición calculada; error SDL inyectado con recuperación clásica íntegra. Modo clásico independiente comprobado.
- En el recorte de tres filas inferiores, la composición nueva es **idéntica a la del HD anterior**: no queda sombra añadida en esas filas omitidas. El caso ordinario sí difiere y hace visible la sombra.
- Las claves con cambios de hoja para daño, caída, agua, muerte o sombra independiente, y animación 1, no heredan el activo del piloto. Son pruebas de exclusión por selector, **no una reproducción completa de esas transiciones**. Los comandos independientes y los otros PNG no se modifican.

Las primeras posiciones de borde del nuevo fixture eran incompatibles con la vista y el ancla nativos: superficie 96×64, margen de 31 píxeles y ajuste vertical `+16`. Las protecciones rechazaron esas entradas. Se corrigieron únicamente vista/posiciones del fixture según `SpriteDrawState.hpp`; las pruebas finales pasan sin cambiar motor, datos nativos ni controles. La compilación offline reutiliza el runtime ASan ya disponible; no se descarga ni reconstruye infraestructura.

**PENDIENTE:** aceptación artística de Miguel; trayectoria completa y transición real a explosión/vuelo, daño, caída y agua; CD32, GPU y audio. No se declara resuelta toda sombra ni aceptada la continuidad jugando. El fixture verifica el contrato acotado y el recorte, pero no sustituye esas pruebas reales. H3 y referencias permanecen intactos; no se repiten matrices completas por dos activos aislados sin cambio de motor. No se entrega un ejecutable nuevo ni se atribuye PASS de CI no observada.

## Recuperación y siguiente decisión

Maestro, derivados, manifiesto, código de autoría y casos focalizados quedan versionados en el directorio de activos. El candidato local contiene solo dos activos/un vínculo y permanece aislado. El candidato normal de granadas conserva 198/363; el de daño, 230/386, sigue aislado. La aprobación del daño no acepta este piloto ni autoriza producción masiva de sombras.

Recuperación local: carpeta `shadow-walk-pilot/` indicada arriba, con `native.json`, `origin.json`, `native.rgba`, `current-*x.png`, `original-candidate/`, `candidate/`, `window-{win,linux}.log`, fuentes generadas de fixture y ejecutables. En su directorio padre están `export_shadow_pilot.py`, `compare_shadow_pilot.py`, `prepare-shadow-window.py`, `run-shadow-window-{win.ps1,linux.sh}`, `run-shadow-composer-linux.sh` y `finish_shadow_pilot.py`. El maestro de sombra se conserva también en `generated_images`. Los hashes originales del cuerpo están en cada comprobación del manifiesto; se reconstruye desde el candidato de granadas o desde los maestros de marcha y los constructores ya existentes.

Secuencia reproducible con las herramientas existentes: compilar `compose.cpp` usando la receta local `build-shadow-pilot.ps1`; ejecutar `python -X utf8 -B export_shadow_pilot.py`; ejecutar los fixtures focalizados Windows/Linux; ejecutar `compare_shadow_pilot.py` y `finish_shadow_pilot.py`. Para Linux, conservar LF en los scripts. No activar ni reemplazar el manifiesto normal durante esta recuperación.

| Paso | Objetivo / resultado esperado | Dependencia | Estado |
|---|---|---|---|
| 1. Valorar el piloto | Decidir sobre color, fuerza, borde y apoyo de esta única sombra | Comparativa local a 8×/12× | REQUIERE VALORACIÓN DE MIGUEL |
| 2. Resolver la muestra | Conservarla o corregir solo el piloto según la valoración | Paso 1 | AUTORIZADO para esta muestra |
| 3. Definir extensión | Proponer poses realmente afectadas y alcance limitado | Aceptación del piloto | PROPUESTO; ampliar requiere aprobación |
| 4. Conjunto de daño | Integrar dependencias verificadas y medir ejecución/continuidad, con H3 y CI pertinentes | Resolver prioridad del piloto | AUTORIZADO dentro del hito |
| 5. Revisar jugando | Verificar varios aliados, granadas, caída, agua y duplicados/pérdidas reales | Candidato coherente comprobado | AUTORIZADO; valoración humana pendiente |

**Siguiente tarea única:** valoración visual de esta muestra por Miguel. Hace falta esa decisión artística; no una autorización técnica rutinaria. El hito sigue en curso. Escalado: NO. Nuevo hilo: no necesario. Fase B, nuevas escenas/familias, scroll y 16:9 continúan fuera del alcance.

## Revisión 2 — posición inferior derecha

**Observación de Miguel:** la sombra debe salir hacia la derecha y abajo, mientras que V1 aparecía alta, detrás de los tobillos. La intensidad puede ser adecuada. Se corrige solo esta muestra, sin generación nueva ni extensión del lote.

La causa de V1 era mezclar toda la componente oscura inferior del original —que también incluye contacto/pies— con un cuerpo HD cuyo apoyo ya llega al borde inferior de la celda. Respetar esa componente en coordenadas absolutas no garantizaba una dirección equivalente respecto al pie HD. **La división exacta pie/contacto/sombra es una interpretación artística, no una etiqueta de los datos nativos.**

La revisión final **conserva tamaño, colocación y píxeles opacos del cuerpo**, y reutiliza la misma pintura/alfa de sombra. Retira el lóbulo superior: queda la mitad inferior de la fila 12 en columnas 9–11 y la fila 13 en columnas 8–10, dentro de la componente nativa verificada. No hay ampliación de la celda ni cambio de motor, ancla o selector. Al reducir la superficie pintada cambia el volumen total de sombra; conservar pintura/alfa no acredita idéntica intensidad percibida.

Se comprobó y descartó una alternativa local de reducción corporal. **No forma parte de V2**: el cuerpo final mantiene escala 1:1. El único cambio visual final está en la cola de sombra.

La sombra nueva solo modifica píxeles desde `Y=12,5` lógico. El centro de la parte expuesta queda aproximadamente en `(10,31; 13,07)`, frente a `(7,92; 12,42)` de la franja inferior del cuerpo usada como referencia de apoyo: derecha y abajo en ambas densidades. Son medidas de imagen, no cambios de coordenadas del actor ni una aceptación visual automática. La extensión inferior sigue limitada al marco nativo de 16×14; no se promete una sombra completa fuera de ese marco.

[Activos V2 y compositor offline](../../assets/modernization/demo-a1-shadow-walk-00-f1-v2/README.md) · [Evidencia V2](evidence/sombras-hd-piloto-v2-20261118.json).

Comparación local **original / V1 rechazada / V2**, a 8×/12× sobre el mismo fondo retenido:

`C:/Users/migue/.codex/visualizations/2026/11/17/01a1ea7b-b727-78f2-a6ac-a4b32dc39150/shadow-walk-pilot-v2/comparativa-revision-8x-12x.png`

**PASS V2:** exportación y alfa, cuerpo opaco intacto y cambios limitados a la cola; 56 casos Window/SDL Windows-Linux con ASan/UBSan y LSan en Linux; bytes del compositor iguales entre plataformas; clásico independiente, estricto/híbrido, dos actores, oclusión, bordes, Save/Restore y recuperación ante error SDL. En el recorte inferior de tres filas, el resultado vuelve a ser idéntico al **HD original a tamaño completo**. Se reutilizan los mismos ejecutables de fixture con el candidato nuevo: no se atribuye a V2 un PASS sobre una alternativa de escala distinta.

**PENDIENTE:** valoración visual de V2; transiciones jugables completas, explosión/vuelo, CD32, GPU y audio. No se repite H3 ni se entrega un ejecutable nuevo por esta revisión aislada. V1 queda marcada como rechazada en posición y permanece recuperable; el lanzador normal y el candidato de daño no se activan ni modifican.

Recuperación final: carpeta local `shadow-walk-pilot-v2/`, scripts `prepare-shadow-v2.py`, `build-shadow-v2.ps1`, **`export-shadow-v2-final.py`**, `test-shadow-v2-{win.ps1,linux.sh}` y **`finish-shadow-v2-final.py`** en el directorio padre. Los scripts antiguos sin sufijo `final` pertenecen a la alternativa de escala descartada y **no reproducen el candidato vigente**. Maestro de pintura, cuerpo de origen y fixtures se reutilizan desde V1, con hashes registrados. No ejecutar las recetas descartadas sobre los activos finales.

| Paso | Objetivo y resultado esperado | Dependencia | Estado |
|---|---|---|---|
| 1. Valorar V2 | Confirmar posición inferior derecha de esta muestra | Comparativa final | REQUIERE VALORACIÓN DE MIGUEL |
| 2. Resolver el piloto | Aceptarlo o corregir solo la muestra; delimitar cualquier extensión | Paso 1 | AUTORIZADO para el piloto; extensión PROPUESTA, requiere aprobación |
| 3. Integrar daño | Incorporar dependencias y medir continuidad del conjunto coherente | Resolver prioridad del piloto | AUTORIZADO |
| 4. Revisar jugando | Confirmar continuidad y sombras en estados reales | Candidato comprobado | AUTORIZADO; valoración humana pendiente |

**Siguiente acción única:** valorar la cola inferior derecha de V2, con el tamaño corporal conservado. Autorización técnica adicional: no necesaria para esta corrección. No hay bloqueo técnico ni trabajo artístico extendido. Escalado: NO. Nuevo hilo: no necesario.
