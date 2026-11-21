# H5.9 — criterio común de presentación e inventario de escenas

Incremento 2.51, 28-10-2026. Miguel acepta briefing/reclutamiento maximizados de 551eaf7 y comunica que «Heroes in Victory» no se amplía. Pide revisar todas las escenas antes, durante y después de misión, incluido F11. Se sustituye la lista limitada de escenas FIT por una política en las rutas comunes de dibujo. La aceptación anterior no se extiende automáticamente a esta ampliación.

## Criterio

Con FIT y ratón alternativo desbloqueado: ocupar la mayor área física posible, centrar, conservar el aspecto lógico y dejar bandas cuando sea necesario. Igual criterio en ventana restaurada, maximizada y F11. No estirar a 16:9, ampliar campo visible o cambiar colisiones. Los DPI no se aplican dos veces. CLASSIC conserva su geometría y entrada históricas; el antiguo piloto SCREEN_TRANSFORM=1/FIT=0 conserva su alcance de ventana.

RenderAt mantiene exactamente su recorte original y ajusta su destino físico para todas las superficies. RenderShrunk mantiene toda la textura y el aspecto lógico que tenía su destino clásico; en particular, el mapa cuadrado conserva el aspecto de pantalla ya aceptado. Sus coordenadas GUI se expresan en el dominio lógico de pantalla, no en texeles de PNG/mapa. El vídeo mantiene su relación de aspecto propia.

La inversa se publica después de presentar. Se distinguen misión, briefing, reclutamiento y GUI general: los menús con la misma geometría comparten el dominio GUI. Cambiar tamaño lógico o físico, F11, fallo de dibujo/presentación o cambio entre dominio GUI y misión invalida/bloquea coordenadas antiguas. Pausa y mapa no publican coordenadas de mundo. Las bandas suprimen clics y entregan el cursor al sistema; un clic iniciado en una banda debe soltarse antes de actuar dentro. Configuraciones SDL incompatibles y ratón relativo/bloqueado conservan juntos dibujo y entrada clásicos.

## Inventario revisado en código

| Momento / pantalla | Productor o bucle | Ruta final y tratamiento |
|---|---|---|
| Selección de campaña, plataforma y archivos | CampaignSelect.cpp, Campaign_Selection / Campaign_Select_File_Loop | Video_Sleep → RenderAt; GUI FIT |
| Menús específicos de demos y selección de mapas personalizados | Fodder.cpp, Demo_Amiga_ShowMenu / Custom_ShowMapSelection / Menu_Loop | RenderAt; GUI FIT, incluye altura Amiga 260 |
| Opciones y confirmación KEEP/REVERT | OptionsMenu.cpp, Options_Menu_Run | RenderAt; GUI FIT y restauración de 15 s |
| Cargar/guardar, listas y entrada de nombres | GUI_Element.cpp, GUI_Select_File_Loop; Recruits.cpp | RenderAt; GUI FIT con modificadores originales |
| Introducción Open Fodder y helicóptero | Intro_OpenFodder; Briefing_Intro_Helicopter_Play; Graphics_PC/Amiga | Video_Sleep → RenderAt; FIT |
| Mensajes iniciales e intros de CF1/CF2/demos | Intro_Main / Intro_Retail / Intro_LegionMessage / Intro_AmigaTheOne | RenderAt; FIT y fundidos originales |
| Protección por manual si la edición la utiliza | CopyProtection.cpp | Video_Sleep → RenderAt; GUI FIT |
| Reclutamiento, colina, camión, escuadras y tumbas | Recruits.cpp, Recruit_Loop | mSurfaceRecruit → RenderAt; FIT |
| Briefing de misión/fase y objetivos | Briefing_Show_PreReady / Briefing_Show_Ready | mSurface → RenderAt; FIT |
| Misión, HUD, cámara, cursor y mensajes de fase/game over | Phase_Loop / Video_SurfaceRender | RenderAt; FIT y coordenadas de mundo verificadas |
| Pausa | Phase_Paused | RenderAt; mismo destino, sin inversa de mundo |
| Mapa general | Phase_Map_Overview_Show | RenderShrunk; FIT y cierre original por clic |
| Diálogos durante misión | mInterruptCallback / GUI_Select_File_Loop | RenderAt; dominio GUI, no inversa de mundo |
| Bajas y homenaje | Service_Show / Service_KIA_Loop | Video_Sleep → RenderAt; GUI FIT |
| Ascensos / «Heroes in Victory» | Service_Promotion_Loop | Video_Sleep → RenderAt; GUI FIT |
| Reintento, fin de fase y regreso a reclutamiento | Mission_Loop / Phase_GameOver / Service_Show | Rutas anteriores; mismos estados y orden de simulación |
| Victoria final / pantalla WON y finales de demos | Fodder.cpp, WonGame | RenderAt; FIT, incluidas alturas alternativas |
| Acerca de, créditos y fondo PNG | About.cpp, cAbout::Cycle | RenderShrunk + RenderAt; destinos ajustados y GUI lógica |
| Imágenes y fundidos compartidos | Image.cpp | Video_Sleep → RenderAt; FIT, paleta y Save/Restore intactos |
| Playground y presentaciones desde scripts | Fodder.cpp / ScriptingEngine.cpp | RenderAt; política común |
| Vídeo introductorio MPEG opcional | VideoMPEG.cpp, Render | Única textura fuera de Window: ya ajusta al output físico; ahora invalida inversa anterior y conserva clic para saltar |

No se alteran estos productores ni su contenido para añadir escalado individual. La auditoría automática enumera todos los puntos SDL_RenderTexture/Geometry/Present del código: dos texturas y presentación en Window, una textura en VideoMPEG. Una nueva ruta directa hará fallar la auditoría para que se revise. El adaptador de entrada de navegador queda fuera del alcance Windows/Linux de este incremento.

## Pruebas y límites

Métodos reales con dobles SDL, ASan/UBSan: 864 combinaciones GUI común, con/sin callback, imagen cargada/indexada, ventana/F11, alturas 200/225/260, seis DPI hasta 300 %, salidas 4:3/16:9 hasta UHD e impar. Comprueba destino, aspecto, coordenadas, fuente completa en RenderShrunk y dominio GUI. Incluye bandas/clic sostenido, cursor, fallo de dibujo/presentación, retorno clásico por renderer no compatible, diálogo durante misión y vuelta a mundo. Render MPEG real extraído: aspecto 4:3 sobre UHD, fallo de consulta y clic para saltar sin inversa antigua.

Se mantienen 544.000 coordenadas clásicas, 228 casos de misión, 216 mapas, 72 transiciones de pausa y 144 de briefing/reclutamiento; las expectativas de F11/FIT y otras superficies se amplían deliberadamente. Regresiones locales: 27.648 superficies (paleta/Save/Restore), transacción real de opciones, 1.536 raster/1.964 escenas/1.024 tiles/72 minimapas. Compilación sintáctica de Window/Options contra SDL 3.4.0.

Cobertura de rutas y geometría no significa validación visual de todas las ediciones: disponibilidad de pantallas depende de datos, demos, bajas/ascensos y final de campaña. No se ha ejecutado un escritorio Windows por el asistente. CI de e18b05b cerrada PASS en Windows/Linux; [paquete verificado](H5_9_VALIDACION_e18b05b.json). Prueba visual del paquete nuevo pendiente. La comparación 8×/12× va después de comprobar este recorrido y las opciones.

## Prueba en Windows

Usar el paquete nuevo, no el ZIP 551eaf7 anterior. `PROBAR_ESCENAS_H5.cmd` activa FIT sin saltar intros; `PROBAR_RESOLUCIONES_H5.cmd` sigue sirviendo para pruebas rápidas de misión. Con los datos de la edición que mostró Heroes in Victory:

1. Intro/selección → reclutamiento → briefing → misión, alternando maximizar y F11. Comprobar proporciones, centrado y botones.
2. Pausa → mapa → cierre → misión; no arrastrar un clic desde banda al juego.
3. Completar misión → bajas si existen → Heroes in Victory/ascensos → siguiente reclutamiento/briefing. Verificar ambas modalidades de pantalla.
4. Cargar/guardar, opciones y créditos; pulsar controles de extremos. Para persistencia usar PROBAR_OPCIONES_H5.cmd, que no fuerza flags.
5. Final de campaña y vídeo, cuando estén disponibles, se validan por separado; no marcarlos aprobados por haber probado una misión.
