# H4.1 — Registro de productores reales y contraste del frame

25-10-2026. Continúa el compositor `ba2ef207`, sobre el relevo `fb44314e`. PR #1 en borrador, sin fusionar; base clásica `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8` conservada.

## Cambio integrado

El motor puede registrar las órdenes reales de misión y contrastar su composición con la superficie clásica. Es un **modo diagnóstico optativo**: `OPENFODDER_AUDIT_MISSION_LAYERS=1`. La ruta clásica sigue dibujando y publicando; la composición del registro no sustituye la imagen visible. Sin esa variable, los hooks no capturan órdenes.

| Punto real | Datos retenidos |
|---|---|
| MapTiles_Draw PC/Amiga | TerrainDraw propio; Clear y Save siguen en sus puntos originales |
| Video_Draw_8_Prepared | Escrituras indexadas decodificadas ya capturadas por el adaptador |
| Video_Draw_8_Resolved | Escrituras decodificadas mientras el recurso es válido; sin volver a seleccionar recursos |
| CaptureCursorDraw | Marca de procedencia del cursor en PreparedSpriteDraw; nunca criterio de ordenación |
| Sidebar_Copy_To_Surface_Common | SidebarDraw retenido con destino real |
| cSurface::clearBuffer / Save / Restore | Operación correspondiente, antes del efecto clásico |

El registro comienza en Interrupt_Redraw antes de Phase_Loop_Interrupt, por lo que conserva el cursor temprano y el posterior al terreno. Comparte una secuencia ordenada entre `mSurface` y `mSurfaceFinal`, con identidades distintas y copias independientes de índices iniciales, fondo guardado y backing RGB. Los sprites del paso principal dirigidos a `mSurfaceFinal` se registran allí; no se añaden a la imagen visible de `mSurface`.

Se comprueba el registro al terminar la producción de interrupción, aunque no haya presentación. Se vuelve a comprobar en el punto final de conversión de Video_SurfaceRender, incluyendo los sprites y las paletas tardíos. La paleta efectiva se toma en ese punto: no se fija prematuramente en el comienzo del intervalo. La comprobación compara índices completos, fondo guardado, identidad/geometría y todos los píxeles RGB del resultado compuesto con la captura clásica vigente.

Una diferencia lanza `runtime_error` en el modo diagnóstico. No se reparan huecos copiando diferencias de imágenes. Una escritura de prueba que evita el registro demuestra que se detecta ese caso. El primer contraste correcto emite `MISSION_LAYER_AUDIT: verified real producer interval`; la nueva CI exige esa marca para no aceptar un replay que haya evitado la ruta de vídeo.

## Vida útil, pausa y sincronización

Cada Interrupt_Redraw sustituye el registro anterior, también cuando no hay presentaciones. Los intervalos no elegibles (pausa, overview, callback o vídeo desactivado) lo descartan. Phase_Paused también descarta el registro al entrar, antes de su primera producción. Al volver a misión, el siguiente intervalo captura su estado inicial actualizado; el backing persistente de pausa continúa gestionado por el mecanismo anterior.

Las capturas retenidas contienen valores y recursos propios, sin punteros a superficies del motor. La referencia compartida al registro se accede mediante las operaciones atómicas de shared_ptr; un mutex protege la inserción de órdenes y la copia de la secuencia. Esto protege el **estado nuevo del registro**; no convierte los buffers clásicos ni los productores en una API libremente concurrente. Captura y contraste mantienen los puntos de sincronización existentes del motor. No se añade hilo ni cambia ningún reloj lógico.

El modo diagnóstico copia índices, fondos, órdenes decodificadas y composiciones. No se ha medido su coste comparativo y no se propone activarlo por defecto. La vida está delimitada por intervalos de producción, no por el número de consumidores; no se introduce aún una cola ni un presupuesto duro de memoria.

## Pruebas y protección de los efectos clásicos

`check_mission_recording.py` ejecuta los cuerpos actuales, con hooks activos, de Interrupt_Redraw, Video_SurfaceRender, MapTiles_Draw/CaptureVisibleTerrain PC y Amiga, Video_Draw_8_Resolved, sidebar y Clear/Save/Restore. También compila Video_Draw_8_Prepared; su equivalencia de raster sigue cubierta por la suite histórica, sin afirmar aquí que este fixture ejercite su hook. Los recursos, la simulación, la selección de sprites y SDL son dobles explícitos. 24 escenarios y 48 presentaciones clásicas: PC/Amiga, padding 0/3, dos patrones y 0/1/5 presentaciones.

Comprueba dos destinos iguales de tamaño, cursor temprano/tardío, sprites tardíos separados, paleta tardía, recursos liberados, conservación de capturas, Restore, Clear, reinicio del registro, entrada/salida del intervalo de pausa y sustitución del destino. Una escritura no registrada debe fallar. Repetir la presentación no modifica índices/fondos/paletas ni vuelve a ejecutar los efectos modelados de sprites/cursor.

Los fixtures históricos siguen aislando sus adaptadores mediante `without_audit`, que elimina únicamente los fragmentos exactos de hooks enumerados en `audit_contract.py`. El nuevo test exige que, retirados esos fragmentos, los cinco archivos de productores/coordinación sean idénticos a `fb44314e`, y compila **los cuerpos con hooks**, usando `preserve_audit=True`. No se eliminan verificaciones de píxeles ni se actualizan goldens H3. Los ensayos antiguos de pausa (144), misión/pausa (240/672), compositor (192/384), destinos (97/627), recursos y kernels siguen vigentes.

Local: nueva prueba PASS con ASan/UBSan y 13 pruebas Python PASS. La ejecución local con LeakSanitizer encontró la restricción de `/proc` del entorno (no una fuga del programa); las suites se ejecutan aquí con `detect_leaks=0`. CI mantiene `detect_leaks=1`. No hay CMake/dependencias SDL locales en esta sesión: la compilación del motor y el replay con vídeo se comprueban en CI.

## Reproducción

```bash
python3 tools/modernization/check_mission_recording.py
SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy \
OPENFODDER_AUDIT_MISSION_LAYERS=1 \
python3 tools/modernization/audit_replays.py --exe build/openfodder --data Run \
  --campaign "PC Format" --video --out reports/h4-recording-pc --timeout 600
```

Repetir para `Amiga The One` con otro directorio de salida. `--video` selecciona `--unit-test --nosound`; el comportamiento predeterminado del runner sigue siendo `--unit-test-headless`. La CI exige 8 fases PC y 3 Amiga, sin omisiones y con marca de contraste real. SDL dummy/software ejercita los productores y las superficies reales, pero no acredita GPU, ventana visible, audio ni inspección visual comercial.

## Límites y siguiente paso

La ruta jugable continúa publicando la captura compuesta clásica. Este incremento conecta el registro y su oráculo; no activa aún la publicación desde las órdenes. Otros destinos/escenas, cargas PNG y las rutas de escritura no incluidas siguen fuera del registro: las diferencias que afecten a los dos destinos auditados deben investigarse, no ocultarse.

0/1/5 está cubierto por los fixtures; el replay de motor con vídeo usa su frecuencia clásica. No se afirma replay del motor completo con presentación omitida/repetida ni pausa interactiva automática. La base CD32 conserva la validación manual previa, pero no se presenta como una prueba manual de este incremento.

Siguiente, tras aprobar CI y documentar las diferencias encontradas: usar el registro validado como fuente de una presentación opcional, manteniendo el contraste con la captura clásica y ampliando 0/1/N del motor completo y la transición de pausa. Interpolación, cadencias nuevas y arte HD siguen pendientes.

## Resultado CI verificado

Motor `b34373b0d1f7fbbbecec78ecafedea8bf9a96fb4`: [Linux 40178254127](https://github.com/Cacheirez/openfodder/actions/runs/40178254127) y [Windows 40178254139](https://github.com/Cacheirez/openfodder/actions/runs/40178254139), ambos aprobados.

| Comprobación | Resultado |
|---|---|
| Registro real focalizado, ASan/UBSan/LSan | 24 escenarios, 48 presentaciones; 0/1/5 PASS |
| Replay con registro y vídeo software, PC Format | 8 fases, cero omisiones, 76,254 s; marca de contraste real |
| Replay con registro y vídeo software, Amiga The One | 3 fases, cero omisiones, 67,684 s; marca de contraste real |
| H3 original Windows/Linux | 11 fases y 11.361 estados sin divergencia |
| Windows | Compilación, 6 CTests y 29/29 fases, cero omisiones, 24,344 s |
| Linux ASan/UBSan, modo headless habitual | 29/29 fases, cero omisiones, 27,941 s; sin hallazgos |
| Linux LSan, modo headless habitual | 29/29 fases, cero omisiones, 27,935 s; sin hallazgos |
| Linux TSan, modo headless habitual | 29/29 fases, cero omisiones, 179,351 s; sin hallazgos |
| Suites anteriores | Todas PASS, incluida pausa 144, misión 240/672, compositor 192/384 y destinos 97/627 |

Los sanitizadores del motor completo no llevan activado el registro: su cobertura con registro activo corresponde al fixture focalizado. No confundirla con una prueba del replay con vídeo bajo TSan. Los tiempos son observaciones de CI, no un benchmark comparativo controlado.

[Evidencia compacta conservada](evidence/b34373b0-reports.json): metadatos y SHA del código, pasos, informes originales y hashes. Ambos ZIP descargados y comprobados por tamaño/SHA-256/integridad; 11 informes PASS, 14 engine.log revisados y marca diagnóstica comprobada en cada replay con vídeo. ZIP/trazas completos siguen en Actions y caducan el 24-11-2026 UTC; el JSON no sustituye un archivo permanente de todos los logs.
