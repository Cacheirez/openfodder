# A.1 — viabilidad de una patrulla tranquila

8 de noviembre de 2026. Entrada `d381097`; ejecutable de implementación `babb62b` reutilizado sin recompilar. Plan 2.74 intacto. [Evidencia y hashes](evidence/demo-a1-patrol.json).

**Dictamen: VIABLE en reproducción técnica.** Existe un recorrido mediante entradas normales de ratón con una ventana de **60 segundos nominales**, cinco soldados presentes y dibujados, sin enemigos dibujados y con publicación HD efectiva continua. **Velocidad normal interactiva y aceptación visual de Miguel PENDIENTES. B sigue sin autorización.**

## Recorrido y conservación del original

Se copia el directorio de datos públicos a un directorio nuevo. Se conservan el ejecutable, manifiesto A.1, semillas, ticks iniciales, parámetros grabados y todos los `mVideoTicks` originales. Solo cambian `mStates` de ratón y `mEvents`; no se toca la grabación original, ninguna entidad, IA, reglas, RNG ni relojes del motor. Sin disparar, suprimir enemigos, forzar direcciones ni aprobar claves nuevas.

La ruta `balanced-loop` conserva las entradas originales hasta el tick de demo 150. Desde 151, clic izquierdo durante seis ticks cada 180, alternando las coordenadas de entrada originales `(188,100)`, `(188,55)`, `(218,55)` y `(218,100)`; entre clics, cursor en `(100,77)` sin botones. Son coordenadas internas del replay, no píxeles de una ventana escalada. El cursor también dirige la cámara: separarlo de la posición del clic evita la deriva de las primeras tentativas.

La ventana elegida comprende ticks de demo **1001–4001**, 1.001 muestras lógicas, diferencia de 3.000 interrupciones a 50 Hz: **60 s nominales**. No se divide el contador de muestras lógicas entre 50. Los cinco soldados están presentes y dibujados en cada muestra; ningún enemigo tipo 5 está dibujado en todo el replay. Los enemigos siguen presentes en la simulación. No se acredita que esta ruta permanezca segura indefinidamente.

## Publicación efectiva y tiempo real

| Medida del replay HD completo | Resultado |
|---|---:|
| Intentos elegibles / publicaciones SDL efectivas | **4.655 / 4.655** |
| Publicaciones de cuerpos | **23.275**; 4.655 por cada slot 0–4 |
| Retornos por faltantes / comandos sin censar | **0 / 0** |
| Muestras lógicas con cinco jugadores dibujados | **1.546 / 1.546** |
| Entradas disponibles | Hasta tick 4.640: **92,8 s nominales** |
| Tiempo de proceso de la medición cronometrada | **35,978 s reales** |
| Primera a última publicación, recepción del log | **34,992 s reales** |

No se cuentan decisiones `replace` como publicaciones. Todos los resultados son `outcome=published`, con cinco reemplazos y cero faltantes. Intentos 365–9673, intervalo de primer comando 364–9672, paso serial constante de dos: cada intervalo auditado tiene su publicación, sin huecos seriales después del arranque. El segundo replay HD y el clásico conservan exactamente las mismas 1.546 muestras de estado.

Los tiempos de recepción del log son externos y pueden incluir latencia de las tuberías; no miden latencia de pantalla. El modo `--unit-test` existente acelera el reloj de pared. Por tanto, **34,992 s reales no equivalen a jugar 60 s a velocidad normal**. No se altera ese reloj para fabricar una demostración. El cargador normal `--demo-play` tampoco es un sustituto directo: la grabación conserva `mPhaseNumber=0` y la selección de m1p2 la realiza el arnés de pruebas; no se modifica ese metadato para atribuir una prueba interactiva.

Las 4.655 publicaciones incluyen la cola que el guard original permite después del último input; **la ventana de 60 s termina mucho antes de esa cola**. El juego informa `Phase Failed` y devuelve `4294967295` al agotar las entradas sin cumplir los objetivos. Es el final acotado previsto, **no victoria ni PASS de una misión completa**.

## Primeros bloqueos reproducibles

| Tentativa | Resultado y primer bloqueo |
|---|---|
| `loop`, cerca de la salida | Cinco soldados y ningún enemigo dibujado, pero **0/4.655 publicaciones**. Primer intento 365: tejado tipo 15/0x91/F0, clave `5fc9fc6b277ef4b4f27f2552b6a212827b18f31e8e3dc4c6979cb98c4e64d9f7`. También falta caja de granadas tipo 37/0xC2/F0, clave `c967c720f08747d3eae8abb253c3ed16d3684ca547ca65df3627d275f9c3e6e5`. |
| `west-loop`, aproximación original y cursor junto al clic | **136 publicaciones / 4.519 retornos**. El tejado reaparece en intento 587, intervalo 586; el cursor desplaza la cámara hacia el este. |
| `bounded-loop`, cursor separado | **847 publicaciones / 3.808 retornos**. Primer faltante en intento 2031, intervalo 2030: enemigo tipo 5/0x59/F0, clave `0ae80fd93ee8120c3e003e5b0e9383b2514910c7353812e498a587247d5455d8`. Primer enemigo dibujado en tick de demo 920, **18,4 s nominales**; deriva hacia el oeste. |
| `balanced-loop` | Corrige únicamente las coordenadas del recorrido anterior; **4.655 publicaciones / cero retornos**. |

Salir de la zona ensayada puede provocar rechazo transaccional de toda la vista. Se conservan estos casos sin añadir arte, vínculos ni excepciones.

## Rango, ave, recortes y transiciones

En la medición final se conservan clásicamente las cuatro claves A.1: rango 0x95/F0 **4.088** veces y marcador 0x7C/F0 **567**; ave 0x98/F0 **511** y F1 **507**. Se cuentan dentro de transacciones efectivamente publicadas. Las garantías de raster clásico, recortes y oclusiones mantienen las pruebas exactas previas de A.1 a 8×/12×; no se han cambiado compositor, recursos ni resolver.

En esta ruta, `rows_to_skip` del jugador vale cero en la ventana elegida: no se atribuye nueva cobertura de recortes. La auditoría clásica del intervalo permanece activa y no diverge. Las oclusiones específicas de una escena nueva, GPU, audio, CD32 y pausa/mapa/reanudación siguen **PENDIENTES**. Diagnósticos iniciales: `palette-transition` y `black-palette`; después, `ordered-published`. No hay otro motivo registrado ni hueco serial dentro de la secuencia publicada. Esto no verifica otras puertas de transición.

## Pruebas técnicas y CI consultada

Trazas HD inicial, HD cronometrada y clásica **idénticas byte a byte**, SHA-256 `a86deab0205c57b5d5b841ac098658be214149cea46522cafcfd9d14d5385eaf`. Son entradas nuevas: se contrastan con el clásico del mismo recorrido, **no se exige coincidencia con el recorrido H3 antiguo ni se cambia su referencia**. H3 completo y pruebas válidas anteriores no repetidos. No se ha recompilado el motor, reintentado WSL ni reconstruido LLVM.

CI de `babb62b`: Windows [42484711149](https://github.com/Cacheirez/openfodder/actions/runs/42484711149) **cancelada**, Linux [42484711218](https://github.com/Cacheirez/openfodder/actions/runs/42484711218) y densidades [42484711137](https://github.com/Cacheirez/openfodder/actions/runs/42484711137) **PASS**. CI del relevo `d381097`: Windows [42485328657](https://github.com/Cacheirez/openfodder/actions/runs/42485328657), Linux [42485328592](https://github.com/Cacheirez/openfodder/actions/runs/42485328592) y densidades [42485328579](https://github.com/Cacheirez/openfodder/actions/runs/42485328579), **PASS**. Los pasos generales Linux ASan/UBSan/LSan pasan en ambas ejecuciones; no se atribuye una nueva medición local Linux de esta patrulla. Linux D6 `42469760868` conserva su evidencia previa, sin relanzarlo ni atribuirlo al código A.1.

## Recuperación y siguiente tarea única

Directorio local `C:/Users/migue/.codex/visualizations/2026/11/08/01a1bbd5-0759-7e10-8ff4-5c706a4a0b02`, subdirectorios `patrol-*`. Válido final: **`patrol-balanced-timed`**; contraste `patrol-balanced-classic`; primer resultado equivalente `patrol-balanced-loop`. Los otros tres conservan bloqueos, no cobertura válida de patrulla HD. Rutas, hashes, comandos y contadores en la evidencia. Datos públicos copiados, logs, inputs derivados y trazas se conservan localmente; no se publican sus bytes. El ZIP de recuperación sin seguimiento sigue intacto.

Reproducción desde el repositorio con Python y las herramientas existentes:

```powershell
python -B tools/modernization/probe_demo_a1_patrol.py --source <directorio-local-A.1> --out <directorio-nuevo> --route balanced-loop
```

Añadir `--classic` en otro directorio nuevo para el contraste. `--out` debe estar en un directorio autorizado y no existir; no reutilizar `verified` ni sobrescribir originales.

**Única tarea siguiente:** revisar con Miguel este recorrido acotado y acordar dentro de A la validación a velocidad normal y visual que falta. **No iniciar B, activación ni paquete.** Detenerse tras publicar el relevo; recomendado abrir un hilo nuevo con `PROMPT_NUEVO_HILO.md`.
