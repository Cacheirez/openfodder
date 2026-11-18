# Sombras — extensión autorizada al arte existente

18-11-2026. Miguel acepta el contacto del piloto y pide aplicar el mismo criterio a todas las imágenes existentes. **La revisión visual del piloto queda cerrada.** Se autoriza la corrección del lote existente y el soporte gráfico acotado necesario para llevar ese criterio al compositor, según el alcance ya presentado. No se solicita otra autorización rutinaria para ese soporte; se mantienen las garantías y las decisiones artísticas reservadas.

## Alcance y clasificación inicial

Candidato acumulado de daño: 230 activos a dos densidades, correspondientes a 115 poses, y 386 vínculos. Las copias de revisión, maestros y derivados no se cuentan como poses nuevas.

| Grupo existente | Poses / activos | Tratamiento |
|---|---|---|
| Marcha del aliado | 24 / 48 | Sombra de suelo en coordenadas de pantalla, con contacto y ancla por pose |
| Apuntado/tumbado del aliado | 8 / 16 | Comprobar raster y apoyo propio; no asumir pies verticales |
| Lanzamiento de granada del aliado | 24 / 48 | Sombra del cuerpo normal; proyectil y su sombra siguen independientes |
| Lanzacohetes del aliado | 24 / 48 | Sombra del cuerpo normal; no alterar proyectiles |
| Enemigo normal ya preparado | 3 / 6 | Dos marchas y una pose tumbada; conservar su estado de activación actual |
| Muerte de enemigo | 1 / 2 | Comprobar sombra independiente/estado; no añadir suelo por semejanza |
| Caídas de aliado | 3 / 6 | Conservar ruta de altura y sombra independiente comprobada |
| Nado | 12 / 24 | No pintar sombra de suelo; preservar recorte/agua |
| Daño/muerte de aliado | 16 / 32 | Conservar las sombras independientes y el contrato del lote aprobado |

La clasificación delimita **83 poses normales candidatas** y 32 poses especiales. No certifica por sí sola la presencia de sombra en todos los rasters: la comprobación nativa y del apoyo por pose debe acompañar la propagación. Recursos sin prueba suficiente quedarán pendientes, sin inventar sombras. El arte de enemigo permanece clásico durante el experimento que así lo exige; preparar su sombra HD no activa esos cuerpos.

## Criterio aprobado y contrato gráfico

- Dirección fija de pantalla **↘**, luz **↖**, independiente de la orientación del actor; ni espejo ni giro de la sombra al girar el cuerpo.
- Cuerpo existente, tamaño, ancla, frame y temporización intactos. Sombra bajo el apoyo y proyectada a la derecha/abajo; la posición/tamaño se verifican por pose. El desplazamiento del piloto no es un offset universal.
- Reutilizar la pintura aprobada; no generar nuevas familias ni rehacer los cuerpos.
- Presentar la sombra de suelo como componente visual del **mismo comando corporal nativo** cuando corresponda a su sombra embebida. Conservar la secuencia completa, terreno, oclusiones, ceros/igual color, Save/Restore, bordes, presupuesto y recuperación.
- Mantener la geometría lógica 16×14 u otra que realmente tenga cada cuerpo. El soporte gráfico debe permitir la extensión de sombra **sin retirar la comprobación de dimensiones del cuerpo**. Una componente de sombra separada en el descriptor HD permite también omitirla al aparecer altura o filas recortadas, sin dejar pintura embebida residual en el cuerpo.
- No añadir esa componente en agua, daño/muerte, vuelo, estados no verificados o donde exista una sombra independiente incompatible. No modificar su lógica nativa ni la simulación.

## Microbloques y siguiente tarea

1. **Inventario y cierre de aceptación — completado documentalmente.** Estado inicial y autorización registrados; activos originales conservados.
2. **Contrato de sombra de suelo — AUTORIZADO / siguiente tarea única.** Componente opcional en el descriptor de arte, vinculada por identidad exacta; composición en el turno del cuerpo y extensión acotada, con negativos, clásico independiente, estricto/híbrido y sanitizadores. No activar arte masivamente antes de comprobar este contrato.
3. **Propagación a poses normales — AUTORIZADO**, después del contrato y pruebas requeridas. Revisión de fuente nativa y apoyo por pose/dirección, reutilizando pintura y cuerpos. Validación y publicación por bloques acotados; registrar exclusiones y faltantes reales.
4. **Conjunto comprobado y revisión jugando — AUTORIZADO**, tras las poses disponibles. Medir publicaciones/retornos, verificar transición de suelo a daño, altura y agua, H3/CI pertinentes y revisión de Miguel. No declarar aceptación jugando a partir del piloto o de pruebas automáticas.

Hito en curso. No se amplía a B, nuevas escenas/familias, scroll ni 16:9. No se usan subagentes ni escalado de modelo. El plan y Arranque rápido registrarán cada punto comprobado y una única tarea siguiente.
