# Resultados reales de esta auditoría

> Documento histórico: las fechas, pendientes y recetas siguientes describen su revisión original. Para el estado vigente y el relevo técnico, consultar [README.md](README.md) y [PLAN_TRABAJO.md](PLAN_TRABAJO.md). No aplicar parches iniciales de nuevo sobre la rama actual.

20 de octubre de 2026. Entorno de ejecución: Linux x86-64, GCC 13, CMake 4.4.4. No se ha ejecutado Windows ni se ha medido una GPU o un monitor real.

## Cambios entregados

1. Control de replays en Python: registra salida y huella SHA-256 del ejecutable; comprueba errores, cobertura vacía, omisiones, timeout y nombres/resultados frente a una referencia. Ocho pruebas de la herramienta pasan.
2. Parche de `Source/Map/MapRuntime.cpp`: `Map_Collect_TileTracks` usa un desplazamiento comprobado contra el tamaño del buffer antes de leer cada palabra de dos bytes. Conserva el inicio original 0x62. No pretende resolver aquí por qué algunos mapas declaran dimensiones que exceden los datos recorridos.
3. Ocho casos sintéticos sobre el cuerpo real extraído de esa función pasan con AddressSanitizer y UndefinedBehaviorSanitizer: buffer vacío, menor que el comienzo, justo en el comienzo, palabra incompleta, una palabra, byte sobrante, mapa completo con coordenadas/tipos esperados y dimensiones grandes con buffer pequeño.

## Ejecuciones

| Registro | Resultado | Alcance |
|---|---|---|
| audit-baseline | FAIL, pese al código de salida 0 y 29 fases completadas | Detectó ausencia de Settings.js. Faltaba inicializar el submódulo anidado Scripts. Corregido con actualización recursiva de submódulos. |
| audit-complete | PASS, 29 fases, 0 omitidas | Base original con datos y scripts completos; 7 campañas demo disponibles. |
| audit-asan | FAIL antes de completar fases | Lectura de dos bytes fuera del buffer en Map_Collect_TileTracks. |
| audit-patched | PASS, 29 fases, 0 omitidas | Motor con parche; mismos nombres y resultados de replays que la base. |
| audit-asan-patched | FAIL tras 11 fases completadas | Segundo acceso fuera de límites en Source/Amiga/dernc.cpp, lword/bit_advance durante descompresión RNC. Pendiente. |
| audit-asan-pc | PASS, 8 fases | Selección explícita de la demo PC Format, con el parche y AddressSanitizer. |

No deben sumarse esas ejecuciones como si fueran misiones diferentes. Las 8 fases PC son parte de las 29 disponibles.

La ejecución completa usa Cannon Fodder Plus, Amiga The One, Amiga Action, Amiga Power Alien Levels, Amiga Format Christmas Special, Amiga Format Not Very Festive y PC Format. No había datos comerciales de las campañas completas. Las campañas sin datos pueden no aparecer siquiera en la enumeración, por lo que cero omisiones no significa cobertura de todo Cannon Fodder.

Los registros headless contienen avisos de inicialización de audio; no se ha comprobado sonido. El detector de fugas LeakSanitizer no pudo operar en este entorno; en los pases posteriores se utilizó `ASAN_OPTIONS=detect_leaks=0`. Eso desactiva la comprobación de fugas, no la de accesos inválidos de AddressSanitizer. No afirmamos ausencia de fugas.

La compilación SDL local se configuró sin X11/Wayland/OpenGL/Vulkan ni backends de audio ALSA/Pulse para las pruebas sin ventana. SDL_mixer se compiló sin libxmp y otros códecs de sistema; FFmpeg se desactivó. Es una base de análisis headless, no un paquete de juego para distribuir. El build Windows propuesto conserva las dependencias del CMake original salvo FFmpeg opcional desactivado.

## Interpretación del parche

La lectura fuera del buffer está reproducida por el registro previo. Tras limitar la lectura, ese fallo deja de ser el bloqueo y las pruebas avanzan hasta otro componente. Los casos sintéticos validan los límites. Las partidas completadas apoyan que la corrección no rompe esas misiones; no prueban identidad de cada evento interno. Todavía no existe una traza canónica por tick ni se han comparado capturas o controles reales.

## Reproducción de las pruebas locales

Con SDL3 y SDL3_mixer instalados en una ruta apropiada para tu entorno Linux:

```bash
cmake -S . -B build-audit -G Ninja -DCMAKE_PREFIX_PATH=/ruta/dependencias -DOPENFODDER_AUTO_FFMPEG=OFF
cmake --build build-audit --parallel 4
python tools/modernization/audit_replays.py --exe build-audit/openfodder --data Run --out reports/base
cmake -S . -B build-asan -G Ninja -DCMAKE_PREFIX_PATH=/ruta/dependencias -DOPENFODDER_AUTO_FFMPEG=OFF -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS='-fsanitize=address -fno-omit-frame-pointer -O1' -DCMAKE_EXE_LINKER_FLAGS=-fsanitize=address
cmake --build build-asan --parallel 4
ASAN_OPTIONS=detect_leaks=0 python tools/modernization/check_map_tracks.py
ASAN_OPTIONS=detect_leaks=0 python tools/modernization/audit_replays.py --exe build-asan/openfodder --data Run --out reports/asan-pc --campaign 'PC Format'
```

`check_map_tracks.py` requiere g++ y está destinado a este diagnóstico Linux. Las instrucciones principales de Windows están en PLAN_MODERNIZACION_ES.md. No se afirma que las instrucciones Windows se hayan ejecutado aquí.

## Pendiente antes de considerar la base estable

- Investigar la lectura RNC en dernc.cpp con sus longitudes de entrada y salida; no ocultarla desactivando el detector ni añadiendo relleno sin justificar.
- Compilar y probar el parche en Windows x64.
- Mantener por separado la referencia original y la rama corregida.
- Introducir trazas lógicas y confirmar reproducibilidad antes de separar dibujo y simulación.
- Ejecutar pruebas con ventana, entrada y audio y revisar el resultado en el PC del usuario.

No se han generado todavía recursos HD, no hay scroll nuevo y no se ha publicado ningún fork o ejecutable. El objetivo de esta entrega es establecer una dirección técnica y pruebas reales para comenzar el proyecto con evidencia.
