# Verde A en la marcha

## Dirección 7

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

El 11 de noviembre Miguel valoró el verde A como «mucho mejor» al ver el ciclo comparativo. Aceptación jugando, GPU y CD32 PENDIENTES.

## Dirección 6

11 de noviembre de 2026. Los tres perfiles derechos usan los mismos factores RGB de A y el mismo filtro cromático que la dirección 7. Las máscaras siguen el casco, la manga, la camisa y las dos perneras de cada pose. Las comprobaciones de región conservan cara, manos, correa, cartuchera, rifle y botas. El [manifiesto](../manifest.json) fija los hashes de los tres maestros recoloreados y de los seis derivados, y conserva las rutas y hashes de los maestros originales.

| Frame | Píxeles RGB modificados a 8× | Píxeles RGB modificados a 12× |
|---|---:|---:|
| 0 | 2.734 | 5.984 |
| 1 | 2.615 | 5.745 |
| 2 | 2.756 | 6.034 |

Reproducción desde la raíz con Pillow 11.3.0. Los tres PNG coinciden byte a byte.

```powershell
python -B tools/modernization/prepare_walk6_uniform.py --out <directorio>
```

`prepare_rocket_art.py` reconstruyó el candidato de 160 activos. La comparación con `1e1be63` confirmó alfa exacto, las 318 vinculaciones intactas y cambios exclusivamente RGB en los seis derivados previstos. `check_walk24_art.py` pasó en Windows x64 con SDL por software. Publicó 256 intervalos controlados y 236 con 94 instantáneas nativas PC/Amiga. En ambos casos hubo dos cuerpos por intervalo, recorte, oclusión y tres rechazos comprobados.

La prueba controlada de transiciones con `check_rocket_art.py` pasó en las ocho direcciones. Incluye marcha, apuntado, lanzacohetes y vuelta a marcha en 12.672 intervalos. SHA-256 de `transitions-controlled/window.log`: `cfb739ab48616ef4d334a3e9cfaeae7601e20c89a225d73681bda719da8122c5`. Se conserva la evidencia anterior de simulación H3 y sanitizadores.

Evidencias locales en `C:/Users/migue/.codex/visualizations/2026/11/11/01a1ccca-3551-7c82-bc41-3abe70984c2e`. El visor `marcha-6-comparativa.html` muestra el original, el verde A de dirección 6 y la dirección 7 a 8×/12×. Las dos láminas PNG muestran las tres poses de cada variante. Los informes `walk-controlled/validation.json` y `walk-native/validation.json` registran el censo y los hashes de los logs. La comparación visual interna de ambas densidades está hecha. El 12 de noviembre Miguel autorizó aplicar el verde A a todas las poses y retiró la revisión individual como requisito. Quedan PENDIENTES la aceptación jugando, GPU, CD32 y las dos claves ordinarias Amiga de 6/0 y 6/2.

## Dirección 5

12 de noviembre de 2026. Las tres poses de espalda diagonal conservan casco, ropa y equipo en sus posiciones originales. Las máscaras delimitan casco, mangas, espalda, faldón y pantalones. Las muestras de correajes, cinturón, cartuchera, mano, rifle y botas conservan sus píxeles. Se usan los factores RGB y el filtro cromático de la opción A.

| Frame | Píxeles RGB modificados a 8× | Píxeles RGB modificados a 12× |
|---|---:|---:|
| 0 | 2.657 | 5.783 |
| 1 | 2.645 | 5.779 |
| 2 | 2.728 | 5.957 |

```powershell
python -B tools/modernization/prepare_walk5_uniform.py --out <directorio>
```

Los tres PNG se reprodujeron byte a byte con Pillow 11.3.0. El exportador compartido reprodujo también los tres PNG de dirección 6. `prepare_rocket_art.py` reconstruyó 160 activos y 318 vinculaciones. Frente a `f4e6707`, solo variaron los canales RGB de los seis derivados previstos. SDL Windows x64 PASS con 256 intervalos controlados y 236 nativos, dos cuerpos, recorte, oclusión y tres rechazos por pasada. Se conserva la evidencia anterior de transiciones, simulación y sanitizadores.

En el directorio local de evidencia de dirección 6, `marcha-5-comparativa-8x.png` y `marcha-5-comparativa-12x.png` documentan la comparación visual interna con el original y la dirección 6. `w5-comparison.json`, `w5-controlled/validation.json` y `w5-native/validation.json` contienen los resultados. Los hashes de los maestros y derivados figuran en el [manifiesto](../manifest.json). Aceptación jugando, GPU y CD32 PENDIENTES.
