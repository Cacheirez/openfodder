# A.1 — Auditoría de la bala 0x7F/F0

## Resultado técnico

En Amiga The One, `eSprite_Bullet` es el tipo 6. El proyectil hereda `mPersonType` del tirador. `Sprite_Handle_Bullet` elige la hoja `0x7F` y el frame 0 para el jugador (`eSprite_PersonType_Human`, valor 0). La tabla `mSpriteSheetTypes_InGame_Amiga_TheOne` apunta a `stru_8D718`, de ocho frames. F0 usa `eGFX_IN_GAME2`, segmento 1, offset 2224, anclaje (0, 0) y una hoja Amiga8 de 320 × 256 y cuatro planos. [Tipo](../../Source/Sprites.hpp) · [Lógica](../../Source/Sprites/Sprite_Projectiles.cpp) · [Tabla](../../Source/Amiga/SpriteData_Amiga.hpp)

El recálculo independiente en Python reproduce primero una clave de control del mismo recurso. Entre los estados comprobados, el único que reproduce `6c2cdf76311d72391780febb69499a2f1b94325ed1509838b7af65f3141d5981` tiene persona, animación, vehículo, destrucción y ambas paletas a cero. El renderizador C++ valida la clave y devuelve un raster de **16 × 6**, con **seis píxeles opacos**, coincidente byte a byte con la decodificación planar independiente. La caja opaca abarca de (0, 0) a (4, 5), ambos inclusive. [Cálculo de la clave](../../Source/Utils/SoldierVariant.hpp) · [Renderizador](../../tools/modernization/render_walk_native.cpp)

El log manual del 14 de noviembre contiene 2.133 publicaciones HD, 1.847 rechazos por faltantes y seis interrupciones. Al descontar las claves del candidato de 333 vínculos quedan 799 intentos rechazados por faltantes y 59 claves residuales. La bala aparece en **450 intentos distintos** a 12× (1.314 comandos entre los intentos 1689 y 7574). En **47** es el único faltante y la secuencia completa contiene al menos un reemplazo. En los otros **403** coincide con otros faltantes.

Cubrir exclusivamente esta clave proyectaría **3.228 de 3.986 publicaciones posibles (80,98 %)**, 752 rechazos por faltantes y seis interrupciones en ese registro. Integración, recorte, oclusiones y recuperación HD con la bala quedan PENDIENTES. La aceptación visual jugando sigue PENDIENTE.

## Reproducción local

Desde la raíz del checkout. El script y sus salidas se conservan en `$work`. El raster y los recursos originales son locales.

```powershell
$work = 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1d961-42c0-7db0-bad9-4e57f50d84bc'
$session = 'C:/Users/migue/.codex/visualizations/2026/11/13/01a1d73b-c7f6-7d50-b9da-34a33fff21c4/a1-331/manual-20261114-004828'
$manifest = 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1d953-1f86-7b42-854d-607cc2d2194e/candidate333/candidate-manifest.json'
$ref = 'C:/Users/migue/.codex/visualizations/2026/11/08/01a1bb46-b87b-7671-82cd-0fdee66db3de/a1/snapshots'
$renderer = 'C:/Users/migue/.codex/visualizations/2026/11/06/01a1b328-fed4-7e22-8351-edd56f133b83/openfodder-d3-crops/openfodder_native_walk_renderer.exe'
python -B "$work/verify_bullet_7f_f0.py" . $session $manifest $ref $renderer
```

| Evidencia | SHA-256 |
|---|---|
| `engine.log` | `4fa4f351ee3cd0bd4b1ebfda108a195ab7f844ab0e1700495d22b487a558c75c` |
| Candidato de 333 vínculos | `dc3eabe3b0ded46ad957d7b4e4546b6539a0526050821cd00133c54f248c105e` |
| Recurso Amiga decodificado | `3dd8d73e4700b42f081f25b25b547b5bd76c9124580ecbd5e01729527e9d8f11` |
| Renderizador nativo | `1ebfebb0575e4c27681ba8bdc2e53acfce414d06861c6b8bfa4368122dcf48ae` |
| `verify_bullet_7f_f0.py` | `c4641e0501ee292f96cf6e3e43c07cbeb14d5d9cb2a73ea40f879192af7bbc6e` |
| `bullet-derived.json` | `81f45c6a3a05fe6940d2674cb5ef90166a137179908ec03caf435c4fbc0be1dc` |
| `bullet-native.rgba` | `90f52dc87b9c093b4fc34d0892f9b98fe3c34f670d542b19d2f63887635263bb` |
| `bullet-verification.json` | `d3d2672787db720becd833e89af4391fe0304bd31165c1c3941342878d9cd2dd` |

## Integración y prueba SDL

`--with-bullet-7f` añade al candidato de 333 vínculos un solo `keep-associated` para la clave auditada. El de 334 contiene 323 reemplazos y 11 dibujos asociados. Los 333 vínculos anteriores conservan su orden y los 168 activos coinciden byte a byte. `--with-tree-90` reproduce el manifiesto anterior con el mismo SHA-256.

SDL software Windows x64 con Clang 23.1.5, SDL 3.4.0 y ASan/UBSan **PASS** a 8×/12×. En ambas densidades la bala hace seis escrituras nativas, cinco de ellas en celdas ocupadas por HD. El orden decide qué dibujo queda visible. Al recortar cuatro filas por arriba quedan dos escrituras con el valor y el desplazamiento esperados. El framebuffer SDL coincide con el oráculo del compositor, incluida la recuperación HD tras el retorno íntegro a clásico por un faltante. Otra clave de bala se rechaza incluso con un vínculo `keep-associated` explícito. Pasan también las regresiones del fixture.

El primer pase detectó una coordenada de recorte incorrecta en el fixture. Se corrigió el estímulo conforme al anclaje del motor y el pase siguiente completó todas las aserciones. El log inicial se conserva como `bullet-sdl-clipping-fixture-failed.log`. GPU, audio, CD32, LSan local y aceptación jugando PENDIENTES.

Desde la raíz del checkout, con `$work` y `$ref` de la sección anterior:

```powershell
$base = 'C:/Users/migue/.codex/visualizations/2026/11/11/01a1ccf2-ba36-78a2-8403-b24f50437a5c/qa-rocket-native/art/candidate-manifest.json'
$previous = 'C:/Users/migue/.codex/visualizations/2026/11/14/01a1d953-1f86-7b42-854d-607cc2d2194e'
python -B tools/modernization/prepare_demo_a1_manifest.py --base $base --out "$work/candidate334" --with-bullet-7f
python -B tools/modernization/prepare_demo_a1_manifest.py --base $base --out "$work/candidate333-regression" --with-tree-90
python -B "$work/prepare_bullet_integration.py" $previous "$work/candidate334" "$work/candidate333-regression" $ref
& "$work/run_bullet_sdl.ps1"
```

Para repetirlo sin sobrescribir la evidencia, copiar `bullet-derived.json` y los dos scripts de integración a un directorio de trabajo nuevo.

| Evidencia | SHA-256 |
|---|---|
| Manifiesto Windows de 334 vínculos | `7ad4ba2c28208a107ff98651a414692059ca7fdd0e4381de2e2d257f167b7882` |
| `prepare_bullet_integration.py` | `f08f4bff7c69e6c664acfaea25983fa5485ea203e0a0b89d43abecda9352beb3` |
| `run_bullet_sdl.ps1` | `43724ac411f460e698316b4495b48720c67c4de9b2407ff78d48012ceeaf450c` |
| `tree-sdl.log` (salida del fixture) | `d322ee281c00e16f6eb22a6d1e4346f320445035f3d884f13105da78c0357052` |
