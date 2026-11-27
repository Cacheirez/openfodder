# Procedencia del lote

Generación mediante la herramienta integrada image_gen, con transparencia real. Referencia única: ../soldier-c01/source.png (C01 aceptado). No se usaron gráficos comerciales como entrada. Los cinco PNG son maestros generados; no se retocaron con scripts. Los derivados de compilación se calculan por promedio de área con alfa premultiplicado y se guardan en el directorio de build; el maestro se conserva.

## Conjunto de prompts finales

Invariante común: un solo soldado completo, acabado pintado moderado, casco y uniforme oliva, correajes marrones, rifle oscuro, botas, cámara elevada oblicua y proporciones de C01. Fondo realmente transparente, sin suelo, sombra proyectada, texto ni cuadrícula. Conservar identidad y equipo. Cambiar solo orientación y pose necesarias.

- **2/0:** orientación hacia la izquierda; zancada con el pie del lado izquierdo de la imagen adelantado. Cámara elevada, no vista a nivel de los ojos. Procede de la generación de zancada izquierda.
- **2/1:** orientación hacia la izquierda; pose central compacta, pies próximos bajo el torso. Procede de la generación neutral izquierda.
- **2/2:** editar las piernas de la pose central izquierda. Muslo cercano bajo la bolsa derecha hacia abajo y a la derecha, bota derecha más baja en el lienzo; pierna lejana hacia la izquierda. Mantener casco, torso, arma, cámara y paleta. La indicación anatómica izquierda/derecha produjo inicialmente una zancada repetida; se corrigió con posiciones explícitas en la imagen.
- **7/1:** editar solo piernas y botas de C01. Pose central de paso del ciclo 0–1–2–1; rodillas y botas juntas debajo de las caderas, suelas casi a la misma altura. Sin zancada larga. Mantener torso, casco, cara, rifle, brazos, textura, paleta, cámara y encuadre.
- **7/2:** editar solo las piernas. La bota del lado izquierdo de la imagen debe avanzar hacia la parte inferior; la del lado derecho se recoge por detrás y queda más alta. No reflejar la imagen completa ni cambiar el arma. Conservar dirección diagonal de C01 y transparencia.

Se revisaron los maestros y los seis derivados juntos. No implica aceptación artística de Miguel: pueden requerir ajuste de oscilación corporal o perspectiva al verlos en movimiento. La captura nativa decide el frame; el visor aislado no define tiempos del motor. El crop y la colocación explícitos están en ../soldier-pilot-batch.json con hashes SHA-256.
