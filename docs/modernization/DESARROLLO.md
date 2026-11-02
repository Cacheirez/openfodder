# Recuperación, compilación y pruebas

Recetas técnicas; el estado y próximo trabajo están en [CONTINUIDAD.md](CONTINUIDAD.md). Los workflows vigentes son la autoridad para flags/dependencias y cobertura de CI.

## Recuperar y reproducir

Requisitos: Git con historial, C++14, CMake, Python 3; Windows con VS 2022 C++ x64, Linux con GCC/Ninja. Las recetas completas y las opciones vigentes están en [.github/workflows/windows-build.yml](../../.github/workflows/windows-build.yml), [linux-build.yml](../../.github/workflows/linux-build.yml) y CMakeLists.txt. Linux necesita además las bibliotecas de desarrollo listadas allí. No confundir compilación headless de análisis con paquete jugable.

```bash
git clone https://github.com/Cacheirez/openfodder.git
cd openfodder
git switch modernization/windows-foundation
git submodule update --init --recursive
git clone https://github.com/OpenFodder/tests.git Run/Tests
git -C Run/Tests checkout c7722ef1a37c1e04ff28c6fedf9d3bdff197dc86
```

Usar directorio nuevo para este ejemplo; no volver a clonar sobre Run/Tests existente. Para reproducir exactamente el motor validado, hacer checkout detached de `f72d6e792c359cec2f53d006d167738c2104bc66` **antes** de inicializar submódulos. En clones superficiales, obtener los commits originales que cada script declara en `BASELINE` antes de ejecutar equivalencia (`git fetch --no-tags origin <SHA>`). Conservar historia completa o un git bundle del repositorio y de los submódulos para un relevo sin red; no hacer squash que elimine las fuentes de comparación.

Pins: Run `070a6086c62164e859fc3274b75b5f536fa9d902`, Scripts `dad04730860bcdd1189aa8562860e379b0f5d783`, tests SHA anterior; SDL release-3.4.0, SDL_mixer `3045b35335113e5e5ba258858cb403d8803bfbeb`. Linux registra SHA efectivos en los artefactos. Las imágenes de Actions/paquetes del sistema no están congeladas: no se promete binario reproducible bit a bit. H2.5 describe un mixer Linux flotante **histórico**, corregido en H2.6.

Windows, desde Developer PowerShell:

```powershell
cmake -S . -B build-win -G "Visual Studio 17 2022" -A x64 -DOPENFODDER_ENABLE_FFMPEG=OFF
cmake --build build-win --config Release --parallel 4
ctest --test-dir build-win -C Release --output-on-failure
```

Linux, después de instalar SDL3/mixer conforme al workflow:

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DOPENFODDER_AUTO_FFMPEG=OFF
cmake --build build --parallel 4
ctest --test-dir build --output-on-failure
```

En Linux, exportar `SDL_VIDEODRIVER=dummy` y `SDL_AUDIODRIVER=dummy` para las siguientes pruebas. En Windows sustituir `build/openfodder` por `Run/openfodder.exe`. Cada directorio de informes debe ser nuevo:

```bash
python tools/modernization/audit_replays.py --exe build/openfodder --data Run --out reports/replays --timeout 600 --baseline tools/modernization/reference-completion.json
python tools/modernization/verify_gameplay_determinism.py --exe build/openfodder --data Run --campaign "PC Format" --out reports/pc --timeout 600
python tools/modernization/verify_gameplay_determinism.py --exe build/openfodder --data Run --campaign "Amiga The One" --out reports/amiga --timeout 600
python tools/modernization/check_gameplay_baseline.py --baseline tools/modernization/reference-gameplay-v1.json --traces reports/pc/run1/traces reports/amiga/run1/traces
```

Esperado: 29/29 fases públicas, cero omisiones, retorno 0; H3 7.956 estados PC + 3.405 Amiga = 11.361. H3 son muestras lógicas de 11 fases, no todos los estados de todas las campañas. La prueba manual H2.6 no acredita visualmente cada cambio H4 posterior. La preparación del minimapa se omite explícitamente en unit testing: no atribuirle cobertura de los replays. Su constructor ahora tiene comparación sintética propia contra el cuerpo original, sin validación visual comercial.

En Linux ejecutar también los diez scripts `check_final_timer_equivalence.py`, `check_sprite_draw_equivalence.py`, `check_sprite_raster_equivalence.py`, `check_sprite_resource_equivalence.py`, `check_terrain_equivalence.py`, `check_hud_cursor_equivalence.py`, `check_surface_draw_equivalence.py`, `check_surface_layers_equivalence.py`, `check_indexed_producer_equivalence.py` y `check_pause_presentation.py` de tools/modernization. Esperado respectivamente: 184.320, 306.432, 29.160, 10.944, 7.680, (2.304 cursor + 288 HUD), 27.648 de superficie, 2.944 de capas, (1.536 raster + 1.964 escenas + 1.024 tiles + 72 constructores) y 144 planificaciones de pausa. Usan GCC y fuentes originales de Git. El workflow añade pruebas Python/contratos y compilaciones del motor ASan/UBSan, LSan y TSan; reproducir sus flags y variables, no solo un build Release. No ignorar un timeout o un fallo de infraestructura como si fuese PASS.


## Recursos y límites

Los maestros C01 y del lote están en assets/modernization, junto con manifiestos y procedencia. Los datos comerciales CD32 no están en Git y no deben publicarse. Las pruebas públicas no certifican todas sus fases. Actions conserva binarios por un plazo limitado: si caduca el ZIP, reconstruir y verificar su commit; no prometer bytes idénticos. No hace falta recuperar ZIP antiguos para desarrollar.
