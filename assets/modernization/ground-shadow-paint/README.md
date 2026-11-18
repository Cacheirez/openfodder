# Pintura compartida de sombra de suelo

18-11-2026. Se reutiliza la pintura generada en el piloto y aceptada por Miguel, con contacto bajo los pies y proyección inferior derecha. No es un actor, una familia nueva ni una sombra independiente del motor. La dirección es de pantalla, nunca un espejo/giro según el cuerpo.

Los dos activos de 7×3 lógico a 8×/12× conservan exactamente los RGBA de la región `[5,11,12,14]` de la pintura derivada del [maestro aprobado](../demo-a1-shadow-walk-00-f1/README.md). `manifest.json` registra origen, recorte y hashes. El cuerpo se conserva separado e inmutable. La colocación se expresa en el descriptor corporal mediante un vínculo `ground_shadow` al activo de pintura de la misma densidad, coordenadas de cuartos de píxel lógico y tipo de propietario.

Ejemplo del piloto aprobado, cuerpo 16×14:

```json
"ground_shadow": {
  "asset": "ground-shadow-7x3-12x",
  "x_quarters": 23,
  "y_quarters": 52,
  "owner_type": 0
}
```

La sombra comienza en `(5,75;13)`, el cuerpo conserva su ancla y se dibuja encima en el mismo turno. **Estos valores son del piloto**, no una colocación universal: verificar apoyo, dimensiones y raster por pose antes de propagar. El contrato desactiva la componente con altura, filas recortadas, estados o familias fuera del alcance normal, vehículo o destrucción pendiente. Las sombras nativas independientes conservan su lógica.

[Contrato, alcance y evidencias](../../../docs/modernization/SOMBRAS_LOTE_EXISTENTE.md).
