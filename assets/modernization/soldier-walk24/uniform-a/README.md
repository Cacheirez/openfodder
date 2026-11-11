# Verde A en la marcha de dirección 7

11 de noviembre de 2026. Primer microbloque de aplicación del [verde oliva elegido por Miguel](../../soldier-c01/uniform-sample/README.md). El [manifiesto](../manifest.json) conserva los maestros originales, recortes, colocaciones y claves nativas. La entrada `uniform_a` selecciona cada nuevo maestro para el candidato y fija los SHA-256 de sus dos derivados RGBA.

La herramienta reutiliza los factores RGB de A `(0.77, 0.90, 0.83)`, la máscara superior y los filtros cromáticos de C01. Ajusta los paneles del pantalón a las zancadas de los frames 1 y 2. Verifica alfa exacto, cambios limitados a la máscara y muestras intactas de cara, manos, correa, rifle y botas. El frame 0 reproduce la muestra aprobada a ambas densidades píxel a píxel.

| Frame | Píxeles RGB modificados a 8× | Píxeles RGB modificados a 12× |
|---|---:|---:|
| 0 | 3.328 | 7.280 |
| 1 | 3.355 | 7.371 |
| 2 | 3.245 | 7.108 |

La comparación de candidatos sobre `f0a771e` comprobó 160 activos y 318 vinculaciones idénticas. Los seis derivados de la dirección 7 tienen cambios exclusivamente RGB. El resto conserva los bytes RGBA y los descriptores originales.

## Reproducción y verificación

Desde la raíz, con Pillow 11.3.0 y un directorio de salida nuevo. Los tres PNG se reprodujeron byte a byte.

```powershell
python -B tools/modernization/prepare_walk7_uniform.py --out <directorio>
```

`prepare_walk24.py` exporta el candidato con los constructores originales. `check_walk24_art.py` usa los mismos constructores y verifica los hashes y la salida del renderizador SDL por software. En Windows x64, 256 publicaciones/512 cuerpos con claves controladas y 236/472 con 94 instantáneas nativas PC/Amiga. Ambas pasadas ejercitaron dos soldados, recorte por filas, oclusión por una capa posterior y tres rechazos sin publicación.

Las regresiones controladas de transición pasaron en el mismo SDL: apuntado (640 intervalos), granada (1.344) y lanzacohetes (12.672). Se conservan los informes `validation.json` de cada ejecución. H3 y sanitizadores locales no se repitieron para este cambio de RGB en activos externos.

Evidencias locales en `C:/Users/migue/.codex/visualizations/2026/11/11/01a1ccb7-f18f-7491-b7d5-0a64e7725590`. `walk-controlled/window.log` tiene SHA-256 `1862e8564965a66350fab36d8f0d33552bee39565eba6618255b0b01b1a05fb9` y `walk-native/window.log` tiene `ca31a8db4362501ca5359f1c9871fd2111713c36748449ee725965d7ab4de07a`. `marcha-7-comparativa.html` permite comparar el ciclo ilustrativo anterior y el verde A a 8×/12×.

El 11 de noviembre Miguel valoró el verde A como «mucho mejor» al ver el ciclo comparativo. Comparación con otras direcciones/familias, aceptación jugando, GPU y CD32 PENDIENTES.
