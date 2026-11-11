# Muestra de verde del uniforme C01

11 de noviembre de 2026. Etapa 1 del [ajuste del verde](../../../../docs/modernization/PLAN_TRABAJO.md#ajuste-del-verde-del-uniforme--programado). Una pose de marcha, hoja 7, frame 0, diagonal hacia delante y a la derecha. El [maestro C01](../source.png) y su encuadre de 16 × 14 unidades conservan su geometría y el anclaje de pies (8, 14).

- **A** ofrece un verde oliva más oscuro.
- **B** ofrece un verde más frío y más oscuro.

La [herramienta](../../../../tools/modernization/prepare_c01_uniform_sample.py) delimita casco y zonas textiles con polígonos, suaviza los bordes con un radio de 2 píxeles del maestro y pondera por tono y saturación para preservar piel, cuero y metal. Dentro de la máscara aplica `RGB × (1 − peso × (1 − factor))` con factores RGB A `(0.77, 0.90, 0.83)` y B `(0.60, 0.81, 0.80)`. El constructor de C01 aplica el recorte y promediado de área original a las dos densidades.

| Variante | Dimensiones | Píxeles RGB modificados | SHA-256 del PNG |
|---|---|---:|---|
| [A 8×](c01-verde-a-8x.png) | 128 × 112 | 3.328 | `2d72556213c6e7b3cc71814b24a221c4cbcc3a71ddd795014d34b5376d8cfd4e` |
| [B 8×](c01-verde-b-8x.png) | 128 × 112 | 3.354 | `60a91180052e3594f849527491298677ff46f8ebea8a1fcdd128b3b214a3f249` |
| [A 12×](c01-verde-a-12x.png) | 192 × 168 | 7.280 | `447d3fe3e4162a865b5778d9a235dafa468e0191aaa99a82f8f11f4c54e3ea02` |
| [B 12×](c01-verde-b-12x.png) | 192 × 168 | 7.310 | `a2f35b49dd9bc1f150fede514146fdad4bd0f8f1c7b2f4d7ecc0ce7697f95907` |

## Verificación técnica

Alfa idéntico al maestro y al derivado original, con cambios RGB limitados al soporte de la máscara. Comparación exacta de píxeles en regiones de control de cara, ambas manos, correa, rifle y ambas botas. SHA-256 de la máscara L sin comprimir `0199b95e185885e09b8130a073608ab0ea0c986fdc98e2f75e6de556ae561e96`. SHA-256 RGBA de los maestros temporales A `380ad8461985b33ff724a8d2e9bc6527fcfc7044be33707aa88b0e8bb6128076`, B `3a198bd04073117155dc776555c4d908fa2c370acf10cfb7be452b5db5859435`.

Los derivados actuales de C01 coinciden byte a byte con los `s7-f0-8.rgba` y `s7-f0-12.rgba` de `art-complete`. En PC Format, escena 815, la composición del actual en (155, 56) reproduce exactamente ambos parches SDL de la [exportación de diagnóstico](../../../../docs/modernization/H6_C01_DIAGNOSTICO_VISIBLE.md). A y B se componen fuera del juego sobre el mismo fondo y anclaje. La revisión de la muestra es estática. Elección de Miguel, validación en movimiento y aplicación al lote PENDIENTES.

## Reproducción

Desde la raíz del repositorio, con Python y Pillow 11.3.0 y el constructor `openfodder_art_builder` compilado por CMake.

```powershell
python -B tools/modernization/prepare_c01_uniform_sample.py --builder <ejecutable> --out <directorio>
```

Para repetir la comparación técnica y generar las dos láminas privadas, añade `--reference-rgba <a1>/art-complete --captures <a1>/data`. Se reutilizaron los HTML/BMP `C01_8` y `C01_12` del [diagnóstico registrado](../../../../docs/modernization/H6_C01_DIAGNOSTICO_VISIBLE.md). En un entorno sin Arial, indica una fuente TrueType instalada con `--font`. Las láminas contienen terreno y gráficos clásicos del juego y se guardan localmente.

La ruta local de las láminas es `C:/Users/migue/.codex/visualizations/2026/11/11/01a1cc60-c5ca-7b43-87de-eeaa20afaf93/muestra-verde`. SHA-256 de `comparacion-local-8x.png` `2722193538cd3e15427462d7cd34365303eff38d7349a060464a0849b598ee57` y de `comparacion-local-12x.png` `c42f33a307641ca6bdc92a06e9db224aed8620b31d0a196f2a866bcc8edb5e97`. Constructor reutilizado SHA-256 `a9b1d4234e7b72ffe03ce1f875a2df3c302b9a04205724fea4c8ef9e8f7a32cc`.
