# OpenFodder para Windows: plan de modernización y primera auditoría

Fecha de revisión: 20 de octubre de 2026. Proyecto dirigido a conservar la jugabilidad y renovar la presentación 2D.

## 1. Decisión técnica

Mantener OpenFodder, C++ y SDL3. Construir gradualmente un renderizador moderno junto al clásico. No trasladar inicialmente el juego a Unity, Unreal o Godot: obligaría a reproducir demasiadas reglas y aumentaría el riesgo de perder el comportamiento original.

Primero reproduciremos una versión conocida y mediremos sus resultados. Después separaremos la presentación de la simulación, suavizaremos cámara y movimiento y añadiremos recursos gráficos de mayor resolución. La primera entrega visual será una misión pequeña completa, no una colección de imágenes inconexas.

Esta entrega es una auditoría y un equipo de pruebas inicial. Todavía NO contiene gráficos renovados ni un ejecutable Windows modificado. Incluye herramientas y un parche C++ separado para una lectura fuera de límites detectada durante la auditoría. Los resultados exactos se adjuntan en RESULTADOS.md y en los registros.

## 2. Vocabulario, sin dar nada por sabido

- **Repositorio:** carpeta de código con su historial. Git permite conservar versiones y volver atrás.
- **Commit:** una versión exacta identificada por una huella. Trabajaremos sobre commits concretos, no sobre una rama que cambia sin avisar.
- **Fork:** copia del repositorio en tu cuenta de GitHub. Sirve para guardar nuestros cambios sin modificar el proyecto de sus autores.
- **Compilar:** transformar el código C++ en un ejecutable. CMake prepara ese proceso; Visual Studio aporta el compilador para Windows.
- **SDL3:** biblioteca que proporciona ventana, eventos, entrada, audio y herramientas de dibujo.
- **Simulación:** reglas, posiciones, enemigos, disparos, colisiones y misiones.
- **Renderizado:** convertir el estado del juego en una imagen. El objetivo es dibujar más suavemente sin ejecutar más veces las reglas.
- **Tick:** avance de un reloj lógico. No equivale necesariamente a un fotograma mostrado.
- **Sprite:** imagen de un personaje, vehículo u objeto. Un atlas reúne muchas imágenes en una textura.
- **Tile:** pieza de terreno repetible. En las rutas revisadas se dibujan piezas de 16 × 16 píxeles originales.
- **Interpolación:** dibujar posiciones intermedias entre dos estados conocidos.
- **Headless:** ejecución sin ventana; útil para automatizar, insuficiente para evaluar gráficos.
- **Regresión:** algo que funcionaba y deja de hacerlo después de un cambio.

## 3. Base exacta inspeccionada

| Componente | Referencia |
|---|---|
| Motor | fefe3795805cdef8665694f834f56601952410af |
| Datos, submódulo Run | 070a6086c62164e859fc3274b75b5f536fa9d902 |
| Scripts, submódulo Run/Scripts | dad04730860bcdd1189aa8562860e379b0f5d783 |
| Grabaciones de prueba | c7722ef1a37c1e04ff28c6fedf9d3bdff197dc86 |
| SDL | release-3.4.0, a962f40bbba175e9716557a25d5d7965f134a3d3 |
| SDL_mixer | 3045b35335113e5e5ba258858cb403d8803bfbeb |

El motor identifica su proyecto CMake como 1.5.4 y usa C++14. Esto describe el código inspeccionado; no presupone que sea la última publicación empaquetada. El primer arranque Windows debe usar estos mismos datos y una configuración limpia. Conservaremos aparte tus partidas y configuraciones personales.

## 4. Lo que he encontrado en el código

| Archivo o función | Observación | Consecuencia |
|---|---|---|
| CMakeLists.txt | En Windows obtiene SDL3 y SDL3_mixer mediante FetchContent y fija sus revisiones. | Ya existe una ruta razonable de compilación Windows. |
| Source/Surface.cpp, cSurface::draw | Convierte índices de una paleta a píxeles y actualiza una textura SDL. | Cambiar el escalado final no crea detalles gráficos nuevos. |
| Source/Window.cpp, RenderAt | Dibuja una región de esa textura con SDL_RenderTexture. | Es una salida de imagen compuesta, no un sistema de sprites HD independientes. |
| Source/PC/Graphics_PC.cpp y Source/Amiga/Graphics_Amiga.cpp | Tienen rutas distintas para decodificar/dibujar terreno. | El formato PC/Amiga es una elección de datos, no del sistema operativo anfitrión. |
| Source/Sprites/Sprite_Core.cpp, Sprite_Draw_Frame | Calcula posición, recorte, paleta y mWasDrawn. | La sustitución de sprites necesita conservar anclajes, orden y recortes. |
| Source/Camera.cpp | Cámara de punto fijo con desplazamientos >>16, aceleración y relación con el ratón. | No debemos sustituir sus reglas por un seguimiento distinto si queremos fidelidad. |
| Source/Fodder.cpp | Interrupt_Sim, Interrupt_Redraw, Phase_Cycle y Video_Sleep coordinan temporización, entrada y dibujo. | Separar renderizado y lógica requiere una modificación arquitectónica. |
| Source/UnitTesting.cpp | Reproduce grabaciones y considera éxito completar la fase; omite grabaciones ausentes. | Su éxito no demuestra igualdad exacta del estado ni cobertura total. |

### Los dos ritmos

Parameters.cpp fija `sleep-delta=20`, descrito como 50 Hz. En la ruta normal revisada, Phase_Cycle espera al menos tres interrupciones antes de avanzar la lógica principal. Como aproximación nominal, son 20 ms por interrupción y 60 ms por ciclo principal; la ejecución real depende del trabajo y la sincronización. En reproducción se consultan también los ticks guardados en la grabación.

Por tanto, no es correcto decir simplemente «el juego funciona a 50 FPS» ni subir la velocidad cambiando sleep-delta a 8. Eso podría acelerar cámara, entrada y reglas. Mantendremos los ritmos y el orden lógico observados mientras aumentamos la frecuencia de presentación.

### Dibujar tiene efectos sobre el juego

`Sprite_Draw_Frame` modifica `mWasDrawn`. Ese indicador se consulta, entre otros sitios, en `Sprite_Handle_Civilian_Unk`, antes de decidir un ataque con una lanza, y en creación de sombras y estelas. No basta con llamar más veces al dibujado actual: debemos conservar el cálculo de visibilidad original en su momento lógico y hacer que el dibujo adicional sea de solo lectura.

También evitaremos aumentar inicialmente filas y columnas del mundo visible. Aunque el proyecto permite hacerlo, podría cambiar qué elementos se consideran visibles y conceder más información al jugador.

### Concurrencia

Hay un hilo de interrupciones, mutex y señales compartidas como mVideo_Ticked/mVideo_Done. Antes de alterar esta coordinación revisaremos la propiedad de cada dato. `volatile` por sí solo no garantiza sincronización entre hilos en C++. Esto es un punto de auditoría, no la afirmación de que ya haya demostrado una carrera concreta.

## 5. Arquitectura propuesta

Conservaremos el motor clásico como autoridad. Tras cada avance relevante se capturará un estado de presentación: cámara, entidades visibles, fotogramas de animación, terreno, paletas y cambios de escenario. El renderizador moderno leerá copias coherentes e inmutables; no modificará sprites del motor ni consumirá su generador aleatorio.

La salida tendrá capas separadas: terreno, objetos y personajes con el orden original, efectos cosméticos, interfaz y cursor. La interfaz no debe moverse con la cámara. Las llamadas al renderizador SDL se mantendrán en el hilo adecuado para la ventana; no se introducirán llamadas GPU arbitrarias desde el hilo de simulación.

Una interfaz de renderizado permitirá elegir clásico o moderno. Si falta un recurso HD, se usará el original. Una opción experimental estará desactivada hasta que cumpla las pruebas de su etapa. No prometemos un nombre de argumento concreto hasta implementarlo.

### Scroll suave y movimiento

1. Capturar estados previos y actuales de cámara con su tiempo lógico, sin redondear prematuramente.
2. Presentar a 60 Hz inicialmente, aunque la lógica conserve sus ritmos originales.
3. Interpolar la cámara entre estados. Fórmula conceptual: `visual = anterior + alpha × (actual - anterior)`.
4. Interpolar posiciones de entidades usando el intervalo que corresponda a sus actualizaciones, no suponiendo que cámara y soldados comparten frecuencia.
5. Mantener fotogramas discretos de animación al principio; mover suavemente un sprite no requiere mezclar sus imágenes.
6. Reiniciar los estados interpolados al cargar una fase, cambiar de escuadrón con salto de cámara, reaparecer, teletransportar o salir de pausa. Usar identificadores con generación para no interpolar un sprite antiguo con otro nuevo que reutiliza su casilla.
7. Recortar contra los límites del mapa y dibujar margen suficiente alrededor de la zona visible. No estirar el borde de la última imagen para ocultar huecos.

La interpolación entre estados añade retraso visual, que mediremos. No usaremos extrapolación sin límites porque puede mostrar posiciones imposibles junto a obstáculos. La prueba de apuntado es obligatoria: un clic debe corresponder a lo mostrado, respetando el modelo de entrada clásico. Habrá que definir y verificar la transformación entre ventana, interfaz, cámara visual y coordenadas del mundo. No se puede prometer simultáneamente cualquier retraso visual y equivalencia de todos los clics sin resolverlo.

VSync puede evitar cortes de imagen, pero no genera posiciones intermedias. El filtrado bilineal suaviza píxeles, pero tampoco suaviza el tiempo. Mezclar dos capturas completas produciría estelas y movería también el HUD: no es la solución propuesta.

### Gráficos HD

Dirección inicial recomendada: 2D ilustrado, vista y siluetas reconocibles, colores legibles y detalles contenidos. El aspecto militar caricaturesco encaja mejor con esta jugabilidad que un cambio a perspectiva 3D.

Un tile de 16 × 16 unidades lógicas puede tener una imagen de 64 × 64 píxeles: más detalle, misma superficie en el juego. Los soldados conservarán su punto de apoyo y sus áreas de interacción. La imagen puede mejorar sin ampliar la colisión ni cambiar la distancia de los disparos.

Diseñaremos un manifiesto para cada atlas con identificador, región, escala, anclaje, dirección y animación. Comprobaremos dimensiones, bordes transparentes, filtrado, orientación, suelo/pies, recorte por agua y superposición con árboles y edificios. Los tiles deben encajar sin costuras. La primera selección cubrirá terreno de jungla, soldado, enemigo, árbol, edificio, proyectil y explosión.

Los efectos nuevos serán cosméticos: humo, luz de explosión, sombras y agua. Tendrán su propio presupuesto y aleatoriedad, separados de las plazas de sprites y del RNG de la simulación. Los fundidos y cambios de paleta originales necesitan una traducción explícita para texturas RGBA; no se pueden simplemente perder al cambiar de formato.

La IA puede ayudar a diseñar y generar material, pero no garantiza atlas utilizables: habrá que verificar consistencia entre direcciones y fotogramas, pivotes, transparencias y legibilidad. Produciremos una pequeña muestra validada antes de multiplicar recursos para todo el juego.

## 6. Etapas y condiciones para avanzar

| Etapa | Entrega | Condición de aceptación |
|---|---|---|
| 0. Base reproducible | Código fijado, compilación, registro de pruebas, primer arranque Windows. | Ejecutable clásico funcionando y cobertura identificada; problemas previos registrados. |
| 1. Protección de jugabilidad | Trazas de estado y escenario de comparación determinista. | Misma secuencia lógica relevante con idénticas entradas y semilla. |
| 2. Separación de presentación | Estados de lectura y rutas clásica/moderna con gráficos originales. | Dibujar 0, 1 o varias veces entre ticks no altera el estado lógico. |
| 3. Fluidez | Cámara y entidades interpoladas; métricas de fotogramas. | Pruebas de pausa, bordes, saltos, cursor y clics superadas; 60 Hz medidos en Windows. |
| 4. Misión de muestra HD | Un conjunto gráfico coherente y sustituible. | Misma misión y colisiones; recortes y visibilidad correctos; aprobación visual. |
| 5. Ampliación | Más biomas, vehículos, interfaz y efectos. | Cada paquete pasa la matriz de escenarios; fallback siempre funcional. |
| 6. Distribución | Paquete Windows con versión, instrucciones y datos separados. | Instalación limpia probada, licencias y recursos correctamente incluidos. |

Empezaremos con el área de juego original, escalada a una ventana moderna. La adaptación panorámica de la interfaz puede estudiarse después sin ampliar necesariamente el mundo visible. 120/144 Hz será una segunda meta, tras demostrar 60 Hz estables. No doy una duración cerrada sin completar la etapa de separación: la producción artística también puede dominar el esfuerzo.

## 7. Cómo comprobaremos que sigue siendo el mismo juego

Las partidas grabadas existentes son una primera barrera. Para tener más confianza añadiremos una representación canónica del estado: posiciones lógicas y fracciones, vida, munición, selección, proyectiles, objetivos, estado RNG y cambios del mapa. Compararemos por tick y mostraremos el primer campo divergente. No se calculará un hash directamente de memoria de estructuras: contiene punteros y relleno dependientes de plataforma.

Habrá que fijar semillas, versión de datos y orden de eventos, y confirmar primero la estabilidad del motor sin cambios. Si no es determinista entre plataformas, compararemos inicialmente cada plataforma contra su propia referencia. No sustituiremos esa comprobación por tolerancias amplias que oculten diferencias.

| Prueba | Qué detecta | Qué no garantiza |
|---|---|---|
| Compilación Linux y Windows x64 | Errores de código y dependencias. | Funcionamiento visual. |
| Replays headless | Misiones rotas y parte del comportamiento. | Igualdad completa ni suavidad. |
| Traza lógica por tick | Cambios en estado relevante. | Calidad artística. |
| Detector de memoria | Accesos fuera de límites, usos tras liberación, etc. en rutas ejecutadas. | Ausencia de todos los fallos posibles. |
| Replays con renderizado | Rutas de dibujo y cambios de pantalla. | Comodidad subjetiva del control. |
| Escenarios de cámara y ratón | Desajustes al apuntar, recortes, saltos y escala. | Todos los monitores/controladores. |
| Medición Windows | Tiempo CPU/GPU y distribución de intervalos entre fotogramas. | Rendimiento en cualquier PC. |

Escenarios mínimos: movimiento lento y rápido, cuatro bordes y esquinas del mapa, pausa, Alt+Tab, ventana/pantalla completa, cambio de escuadrón, minimapa, cargas, muerte, vehículos, explosiones, agua, edificios y selección junto al panel. Monitor de 60 Hz primero; después 120/144 y escalado Windows 100/125/150 %. Objetivo inicial de presentación: presupuesto de 16,67 ms por fotograma a 60 Hz, midiendo percentiles y saltos, no solo FPS medios.

No haremos cientos de pruebas equivalentes por volumen. Cada prueba debe proteger una propiedad concreta. La cobertura comercial necesita los datos correspondientes; las demos no prueban toda la campaña original.

## 8. Primer paso en tu Windows, explicado

El objetivo de esta sesión local es solo conseguir que el OpenFodder clásico compile y arranque. No necesitas aprender C++ antes de hacerlo.

### Preparar herramientas

1. Instala **Git para Windows** desde https://git-scm.com/downloads/win. Permite descargar el código y conservar versiones.
2. Instala **Visual Studio 2022** o sus Build Tools con **Desarrollo para el escritorio con C++**. Incluye MSVC, Windows SDK y herramientas CMake. El proyecto documenta el generador `Visual Studio 17 2022`; no confundas Visual Studio con Visual Studio Code, que por sí solo no incluye ese compilador. Si ya tienes otra versión, revisaremos su generador antes de cambiar los comandos.
3. Para nuestras herramientas de auditoría, instala **Python 3.10 o posterior** desde https://www.python.org/downloads/windows/. Comprueba que funciona `py --version`. El juego no necesita Python para jugar.
4. Abre **Developer PowerShell for VS 2022** desde Inicio. Es una consola con acceso al compilador. Comprueba `git --version` y `cmake --version`. Si no existen, no sigas copiando comandos: corrige la instalación o comparte el mensaje.

### Descargar una versión conocida

Ejecuta cada línea por separado. Usa una carpeta nueva; estos pasos no sustituyen una instalación existente.

```powershell
New-Item -ItemType Directory -Force C:\Dev
Set-Location C:\Dev
git clone https://github.com/OpenFodder/openfodder.git OpenFodderModern
Set-Location C:\Dev\OpenFodderModern
git checkout fefe3795805cdef8665694f834f56601952410af
git switch -c modernization/base
git submodule update --init --recursive
git clone https://github.com/OpenFodder/tests.git Run/Tests
git -C Run/Tests checkout c7722ef1a37c1e04ff28c6fedf9d3bdff197dc86
```

`checkout` selecciona la revisión auditada; `switch -c` crea una rama propia. `--recursive` es imprescindible: los datos tienen a su vez un submódulo de scripts. No añadas archivos originales de pago ni partidas al repositorio público.

### Compilar

```powershell
cmake -S . -B build-win -G "Visual Studio 17 2022" -A x64 -DOPENFODDER_ENABLE_FFMPEG=OFF
cmake --build build-win --config Release --parallel 4
```

El primer comando prepara la construcción y descarga dependencias. El segundo crea el ejecutable. La primera vez tarda más. Desactivamos el vídeo introductorio opcional FFmpeg para reducir dependencias; no se elimina la jugabilidad. CMake copia el ejecutable y las DLL de SDL en `Run`. Una DLL es una biblioteca que el programa carga al ejecutarse: no muevas solo el EXE a otra carpeta.

### Probar y arrancar

```powershell
Set-Location C:\Dev\OpenFodderModern\Run
.\openfodder.exe --appveyor --unit-test-headless *> baseline-windows.log
$LASTEXITCODE
.\openfodder.exe --window --skipintro
```

La prueba automática no muestra ventana. Conserva el registro incluso si termina con código 0. Para jugar usa el segundo comando y elige una demo disponible. Para salir usa los controles normales del juego. Esta auditoría verificó la compilación Linux; todavía tenemos que confirmar estos pasos de Windows en tu máquina o en un runner Windows.

No cambies `sleep-delta`, número de sprites, filas/columnas ni actives trucos para nuestra referencia. Los datos originales de Cannon Fodder pueden incorporarse más tarde según INSTALL.md. No necesitas comprarlos antes de validar el arranque con las demos disponibles.

### Aplicar el primer parche, después de guardar la referencia

El archivo `map-tracks-bounds.patch` corrige una lectura fuera del buffer al recoger casillas con pistas. Conserva el desplazamiento de lectura original y deja de leer cuando no quedan dos bytes completos. Es una corrección experimental de estabilidad, no un cambio gráfico. Las 29 fases disponibles completan tanto antes como después en la prueba Linux normal; la igualdad completa por tick todavía no está verificada.

Copia el parche a la raíz del repositorio y ejecuta desde allí:

```powershell
git apply --check map-tracks-bounds.patch
git apply map-tracks-bounds.patch
cmake --build build-win --config Release --parallel 4
```

No lo apliques si `--check` falla. Ejecuta entonces el control `windows-cambio1` indicado abajo. El informe de memoria completo todavía detecta otro fallo en la descompresión Amiga; no consideramos cerrada la etapa de estabilización.

### Usar el control de pruebas incluido

Copia la carpeta `tools` del paquete entregado dentro de `C:\Dev\OpenFodderModern`. Desde la raíz ejecuta:

```powershell
py -m unittest discover -s tools/modernization -v
py tools/modernization/audit_replays.py --exe Run/openfodder.exe --data Run --out reports/windows-base
```

Se guardan `engine.log` y `report.json`. Para una versión posterior:

```powershell
py tools/modernization/audit_replays.py --exe Run/openfodder.exe --data Run --out reports/windows-cambio1 --baseline reports/windows-base/report.json
```

Cada salida debe usar una carpeta nueva. El control falla si no hay ninguna fase completada, hay errores estructurados, falla el proceso, vence el tiempo, hay omisiones o cambian nombres/resultados frente a la referencia. `--allow-skips` existe solo para una auditoría parcial explícita; nunca convierte esa cobertura en completa. La comparación ignora tiempos porque fluctúan entre ejecuciones. Esta herramienta no detecta todavía estados lógicos distintos dentro de una misión completada.

## 9. Reparto del trabajo

Yo puedo examinar el código, preparar parches pequeños, compilar en el entorno disponible, ejecutar pruebas, investigar fallos y mantener instrucciones reproducibles. Cada entrega debe identificar base, cambios, pruebas realizadas y pendientes. Podré preparar automatización Windows en GitHub Actions; ejecutarla y conservar el proyecto en tu cuenta requiere disponer de ese repositorio y de acceso autorizado. No hay todavía un fork tuyo creado ni un workflow ejecutado allí.

Tú aportarás las comprobaciones que no puedo sustituir desde este entorno: arrancar en Windows, comprobar apuntado y sensación de juego en tu monitor, elegir el estilo visual y aportar los datos comerciales que quieras usar. Tu PC parece sobrado para plantear este proyecto 2D, pero los objetivos de FPS se medirán; la potencia del hardware no corrige fallos de sincronización.

## 10. Recursos y distribución

El código del motor se identifica como GPL-3.0 y sus cabeceras permiten GPL versión 3 o posterior. Conservaremos avisos y revisaremos las condiciones al distribuir cambios. Los datos gráficos y sonoros originales son recursos separados: no asumiremos que la licencia del motor los convierte en libres. El paquete de esta auditoría no incluye datos comerciales ni un juego completo.

## Fuentes técnicas

- Motor y documentación: https://github.com/OpenFodder/openfodder
- Compilación fijada: https://github.com/OpenFodder/openfodder/blob/fefe3795805cdef8665694f834f56601952410af/COMPILING.md
- Instalación: https://github.com/OpenFodder/openfodder/blob/fefe3795805cdef8665694f834f56601952410af/INSTALL.md
- Temporización: https://github.com/OpenFodder/openfodder/blob/fefe3795805cdef8665694f834f56601952410af/Source/Fodder.cpp
- Cámara: https://github.com/OpenFodder/openfodder/blob/fefe3795805cdef8665694f834f56601952410af/Source/Camera.cpp
- Sprites: https://github.com/OpenFodder/openfodder/blob/fefe3795805cdef8665694f834f56601952410af/Source/Sprites/Sprite_Core.cpp
- Pruebas: https://github.com/OpenFodder/openfodder/blob/fefe3795805cdef8665694f834f56601952410af/Source/UnitTesting.cpp
- Grabaciones: https://github.com/OpenFodder/tests

Las conclusiones técnicas proceden de la lectura de los archivos de esta revisión. Las propuestas de arquitectura son decisiones de este proyecto, no prestaciones ya presentes en OpenFodder.
