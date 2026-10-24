# H3.6 — Auditoría del contrato de visibilidad clásica

**Fecha:** 21 de octubre de 2026. **Estado:** revisión de usos y efectos lógicos cerrada. **Pendiente separado:** implementar en H4 la visibilidad independiente del renderizador, y probar 0/1/N dibujos entre ticks.

## Resultado de la revisión

El inventario se realizó sobre los archivos de código fuente `Source/*.cpp` y `Source/*.hpp` de la rama de modernización. Se añadió el verificador `tools/modernization/check_visibility_contract.py` a Windows y Linux CI para rechazar cualquier nueva lectura/escritura no inventariada.

| Archivo | Ocurrencias | Operación y efecto |
|---|---:|---|
| `Source/Sprites.hpp` | 1 | Declaración de `sSprite::mWasDrawn` |
| `Source/Sprites.cpp` | 1 | Inicialización a cero en `sSprite::Clear` |
| `Source/Sprites/Sprite_Core.cpp` | 3 | Escritor ordinario durante `Sprite_Draw_Frame` (1/0); retorno seguro de fotograma inválido escribe 0 |
| `Source/Sprites/Sprite_Civilian.cpp` | 4 | Condiciona ataque de civiles, generación de nativos y temporizadores/comportamientos fuera de pantalla |
| `Source/Sprites/Sprite_Effects.cpp` | 2 | Condiciona creación de humo y efectos de explosión; este último llama a `Sprite_Handle_Explosion_MapTiles` |
| `Source/Sprites/Sprite_Projectiles.cpp` | 1 | Condiciona creación de estelas de fuego |
| `Source/Sprites/Sprite_Troop.cpp` | 1 | Condiciona creación de sombras de soldados |
| `Source/Sprites/Sprite_Vehicle.cpp` | 1 | Condiciona efecto de hundimiento |
| `Source/GameplayTrace.cpp` | 1 | Lectura de auditoría en JSONL, sin mutación |
| **Total** | **15** | **9 archivos** |

La evaluación de `mWasDrawn` **no** depende solo de escribir píxeles: en `Sprite_Core.cpp` se actualiza aunque `mDisableVideo` impida la llamada final de dibujo. La prueba de referencia H3 ya incluye el campo; el comparador detectó una divergencia inducida en una copia de una traza real.

## Contrato para H4/H5

1. Mantener los cálculos de visibilidad y su frecuencia **lógica original**, derivados del área visible clásica, no de una ventana HD ampliada.
2. Guardar el resultado lógico en el instante del motor equivalente al clásico; preservar el orden con respecto a las actualizaciones de civiles, explosiones, proyectiles, sombras y vehículos.
3. Usar `mWasDrawn` como **entrada inmutable** en la ruta de presentación moderna. La presentación 60/120/144 Hz nunca modificará el indicador ni consumirá el RNG del motor.
4. La presentación puede dibujar márgenes o interpolar posiciones, pero ello no amplía el campo de visión **lógico** ni concede nueva información o decisiones a enemigos.
5. Ensayar 0/1/N presentaciones entre ciclos, pausa, cambios de fase, bordes de cámara y condiciones de recorte; comparar las trazas canónicas H3.
6. Controlar las llamadas a `Sprite_OnScreen_Check`: las rutas PC y Amiga tienen reglas particulares de recorte. Una unificación visual debe conservar los resultados lógicos.

**Aceptación H3.6:** inventario exhaustivo de usos, contratos escritos, comprobación automática para cambios y evidencia de detección en trazas; logrado. **No se declara H4 listo** ni que dibujar múltiples veces preserve el estado: eso exige la separación de lógica y presentación.

**Actualización H2.3:** se protege la consulta de fotogramas inexistentes y se fija `mWasDrawn=0` únicamente para referencias inválidas. Los fotogramas válidos conservan el cálculo de visibilidad clásico; la prueba automatizada de referencias espera ahora 15 apariciones en 9 archivos. Las pruebas de independencia del renderizado permanecen en H4.
