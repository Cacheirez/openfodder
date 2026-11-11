# Marcha del jugador: ocho direcciones, 24 claves

Lote artístico interno del plan 2.74, A3. Las siete direcciones pendientes tienen tres poses preparadas y revisadas junto con el ciclo C01. **No equivale a todos los estados del soldado, enemigos ni a una campaña moderna terminada.** A3 permanece abierto y Miguel no ha aceptado visualmente este lote.

## Fuentes y selección

| Hoja/dirección | Fuentes seleccionadas | Revisión interna |
|---|---|---|
| 0, delante | `s0-f0/1/2.png` | Zancadas opuestas, pose intermedia compacta; cámara elevada. |
| 1, delante/izquierda | Los tres maestros anteriores de `../soldier-pilot/s2-f*.png` | Su orientación visual es diagonal; se reutilizan aquí con colocación corregida. El piloto antiguo no se modifica. |
| 2, izquierda | `s2-f0/1/2.png` | Nuevo perfil izquierdo: torso y arma apuntan al lado, sin reutilizar la diagonal. |
| 3, izquierda/atrás | `s3-f0.png`, `s3-f1.png`, `s3-f2-v3.png` | Espalda diagonal; zancada duplicada descartada, inversión y longitud de pierna corregidas. |
| 4, atrás | `s4-f0/1/2.png` | Espalda recta, correajes conservados, alternancia de apoyos. |
| 5, atrás/derecha | `s5-f0.png`, `s5-f1.png`, `s5-f2-v3.png` | El candidato aplica el verde A a los tres frames de espalda diagonal. [Verificación y recuperación](uniform-a/README.md#dirección-5). |
| 6, derecha | `s6-f0/1/2.png` | El candidato aplica el verde A a los tres frames del perfil derecho. [Verificación y recuperación](uniform-a/README.md#dirección-6). |
| 7, derecha/delante | C01 y los dos maestros de `../soldier-walk-review/review.json` | El candidato aplica el verde A a los tres frames. [Verificación y recuperación](uniform-a/README.md). |

Son **18 maestros nuevos seleccionados**, tres anteriores reutilizados en la diagonal correcta y los tres del ciclo C01. Los cuatro intentos descartados no se convierten en fotogramas válidos. [Prompts exactos y procedencia](generation.json). Herramienta integrada `image_gen`, con transparencia real; C01 como identidad/estilo, poses nativas de demos públicas como guía de orientación y maestros de espalda generados para conservar el equipo. No se usan datos comerciales CD32. No se retocan los PNG maestros con scripts ni se reflejan imágenes para obtener otra dirección.

## Colocación y derivados

`manifest.json` contiene cada fuente, SHA-256, recorte y colocación explícitos. Se inspeccionó el alfa de los maestros para preparar estos valores; el build no infiere recortes ni cambia decisiones artísticas. Las tres poses de cada nueva dirección usan el mismo tamaño de recorte y la misma escala; la colocación se registra respecto al casco y al apoyo de los pies. Se conserva una pequeña oscilación corporal del paso, sin cambiar tiempos del motor. Los 24 cuerpos conservan el marco lógico 16×14 de esas tablas, sin convertirlo en una restricción para otros estados.

`prepare_walk24.py` reutiliza los constructores existentes y la función de derivación/exportación compartida con el ciclo diagonal. Produce 48 PNG/RGBA exactos (24 × 8×/12×), manifiesto v2 y visor autónomo con pausa, paso y giro continuo. Se comprueban hashes de fuentes/evidencia y unicidad de claves. C01 usa su constructor original; no se normaliza otra vez ni se modifica su recorte aprobado.

El [visor anterior al verde A](../../../docs/modernization/reviews/walk24.html) contiene únicamente arte moderno. Su ciclo 0–1–2–1 a 180 ms es ilustrativo: el juego sigue seleccionando la hoja/frame con sus contadores originales. La [hoja de revisión anterior](../../../docs/modernization/evidence/soldier-walk24-contact.png) conserva las poses reducidas vistas juntas. El visor generado por `prepare_walk24.py` muestra el candidato vigente.

## Vinculaciones y prueba

Hay **94 claves reales observadas de marcha ordinaria**: 48 PC y 46 Amiga. El censo anterior tenía 112 instantáneas incluyendo daño/deslizamiento; no eran 96 claves ordinarias completas. Faltan observar 6/0 y 6/2 en el recurso Amiga cuyo hash comienza `3e0bf624`. No se inventan sus claves ni se aprueban por inferencia. Sí existen las 24 imágenes modernas y esas dos poses están probadas con otros recursos reales.

`check_walk24_art.py` prepara el lote y ejecuta el método real de Window/SDL. Modo controlado: 256 intervalos/512 cuerpos, recorrido de ocho direcciones y ciclo original por PC/Amiga a 8×/12×. Modo real: 236/472, tres grupos completos de 24 claves con recorrido continuo y 22 claves del cuarto grupo comprobadas individualmente. Verifica 188 combinaciones reales clave/densidad, dos soldados, recorte y oclusión. Las claves reales no se reasignan a bytes sintéticos. En ambos modos se compara la salida SDL, se verifica el alfa de C01 y se comprueba el rechazo coherente de enemigos, otros estados y paletas no vinculadas. La evidencia ASan/UBSan local del lote original se conserva.

Los recursos nativos y las paletas permanecen locales. El CTest `soldier_walk24_art` usa recursos controlados y el arte real; el modo con instantáneas reales se ejecuta aparte con `--native-snapshots`. [Evidencia del bloque](../../../docs/modernization/evidence/soldier-walk24-validation.json).

H3 con este manifiesto: 11 fases/11.361 estados originales y 22 pausas/reanudaciones PASS. Source del motor no cambia. **No hubo publicación HD ordenada de campaña**: siguen faltando otros estados y entidades. H3 comprueba simulación/guards; las publicaciones de arte quedan acreditadas por los escenarios aislados anteriores, no por el replay completo. GPU/CD32 y aceptación visual siguen pendientes.

## Continuación

Siguiente bloque de desarrollo: reposo/apuntado del jugador y transición marcha → reposo/apuntado → marcha, según [continuidad vigente](../../../docs/modernization/CONTINUIDAD.md). Completar también las dos variantes ordinarias no observadas y, después, las demás familias de estados y enemigos. La vinculación Slide1 comprobada en el bloque anterior se conserva en su manifiesto diagonal; este manifiesto nuevo está limitado explícitamente a marcha ordinaria. No se promueven daño/deslizamiento a marcha por compartir hoja. Faltan transiciones, cobertura HD completa de campaña, GPU/CD32 y aceptación visual. El lanzador anterior sigue igual; sin ZIP de sustitución completa.
