# C01 — visor técnico de densidades 8×/12×

29-10-2026. Trabajo independiente autorizado por Miguel mientras queda pendiente probar opciones. Dirección C conservada, sin elección de densidad ni cambios en el juego.

Descargar [C01_DENSIDADES.html](C01_DENSIDADES.html) con **Download raw file** en GitHub y abrirlo en un navegador. Es un archivo autónomo: contiene el PNG C01 original y el visor, sin servidor, instalaciones ni conexión de red para funcionar. Los enlaces de documentación sí abren GitHub. No es una captura del motor ni una demo jugable.

El visor ofrece 4:3/16:9 hasta UHD, geometría PC/Amiga, fondo neutro/claro/oscuro/cuadrícula, guías de caja/pies y ampliación 2×/4×. Arriba muestra el cuadro físico calculado; abajo, una ampliación de inspección. El DPR del navegador se usa para compensar la escala del escritorio, no para multiplicar de nuevo el tamaño. Si una captura se reduce o se visualiza mediante escritorio remoto, deja de garantizar tamaño físico observado.

Ambas densidades usan el mismo maestro, recorte alfa, caja lógica y anclaje del piloto C01. Se aplica el promedio de área con alfa premultiplicada del generador nativo. 8× tiene cuadro 128×112 y 12× 192×168; al presentarse ocupan la misma huella. La caja de contenido del piloto sigue siendo una aproximación de proporciones, no una anatomía HD ya aceptada.

## Reproducción

Desde la raíz del repositorio:

```bash
python3 tools/modernization/check_density_preview.py
python3 tools/modernization/build_density_preview.py --out assets/modernization/density-review/C01_DENSIDADES.html
```

La comprobación requiere C++14, Node.js y Python estándar, sin npm para el modelo. El builder verifica el SHA-256 de source.png y lo incorpora sin recodificar. La CI independiente [density-review.yml](../../../.github/workflows/density-review.yml) añade Chromium/Playwright fijado, comprueba la página real y conserva capturas. Estas capturas son evidencia del navegador Linux, no de Windows/SDL ni aceptación artística.

## Alcance y límites

- Equivalencia exacta de los 224 píxeles nativos al preparar 1×; variantes 8/12 deterministas, márgenes transparentes, alfa y anclajes comprobados.
- 96 combinaciones matemáticas de salida/plataforma/DPR. Navegador automatizado: 1080p/1440p/UHD, PC/Amiga y DPR 1/3.
- Filtro final del navegador configurado en alta calidad; puede diferir de SDL/GPU. Color de navegador y redondeos de alfa no constituyen equivalencia pixel a pixel con el render futuro.
- Solo fondos de inspección. No hay terreno artístico de producción, sombras nuevas, animación, oclusión ni movimiento.
- El motor aún compone la pose en 16×14: esta herramienta no activa HD ni resuelve su composición. La integración posterior debe conservar orden, clipping, cámara, anclajes y fallback clásico.

[Originales y decisión C](../concepts/README.md) · [Evaluación y siguiente trabajo](../../../docs/modernization/H6_DENSIDAD_EVALUACION.md).

Primera validación completa: [CI 40800565963](https://github.com/Cacheirez/openfodder/actions/runs/40800565963), [evidencia](../../../docs/modernization/H6_DENSIDAD_VALIDACION_f842b3d.json). Capturas inspeccionadas; ajuste posterior de zoom inicial/scroll cubierto por una nueva aserción. Comprobar la CI del HEAD antes de atribuirle ese resultado.

**Versión final verificada:** 30ba0ec, [CI 40800994726](https://github.com/Cacheirez/openfodder/actions/runs/40800994726) PASS; capturas DPR 1/3 inspeccionadas y HTML idéntico al de Git. [Evidencia](../../../docs/modernization/VALIDACION_30ba0ec.json). No requiere ninguna prueba de Miguel para conservar o usar la herramienta; la elección artística sigue abierta.
