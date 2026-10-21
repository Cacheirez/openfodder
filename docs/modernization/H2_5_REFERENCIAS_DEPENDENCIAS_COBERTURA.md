# H2.5 — Referencias, dependencias y matriz de cobertura

**Fecha del inventario:** 21 de octubre de 2026 (Europe/Madrid).  
**Resultado:** H2.5 **cerrado como auditoría de dependencias y cobertura existente**. No se modifican el motor, las referencias H3, las dependencias ni los replays con este cierre documental. La eventual normalización de versiones entre plataformas es una **decisión/acción pendiente para H2.6**, no una compatibilidad ya demostrada.

**Repositorio:** [Cacheirez/openfodder](https://github.com/Cacheirez/openfodder), rama `modernization/windows-foundation`, [PR #1](https://github.com/Cacheirez/openfodder/pull/1) abierta en borrador. Código H2.3/H2.4 aceptado en la regresión: `93c8aae6c79120071982c39380c517f2ae3142e7`; ampliación de CI LeakSanitizer/ThreadSanitizer: `82166539cc7dfdcc9c1e1f1995797b257d992e47`. El job de PR usa el commit de **merge temporal** `a813e72` (HEAD de la ejecución), por lo que no debe confundirse ese SHA con el SHA de la rama. El HEAD documental de la rama puede avanzar sin modificar el binario.

## 1. Referencia reproducible del motor y los recursos

| Elemento | Revisión/configuración comprobada | Procedencia |
|---|---|---|
| Motor base | OpenFodder `project(openfodder VERSION 1.5.4 LANGUAGES CXX)`, **C++14** | `CMakeLists.txt` |
| Rama con estabilización | `modernization/windows-foundation` y PR #1, sin fusionar | GitHub |
| Datos públicos `Run` | `070a6086c62164e859fc3274b75b5f536fa9d902` | Gitlink del repositorio `OpenFodder/data`; `.gitmodules` |
| Scripts dentro de `Run` | `dad04730860bcdd1189aa8562860e379b0f5d783` | Gitlink anidado `OpenFodder/data:Scripts`, repo `OpenFodder/scripts` |
| Grabaciones de prueba `Run/Tests` | `c7722ef1a37c1e04ff28c6fedf9d3bdff197dc86` | `OpenFodder/tests` clonado y `git checkout` explícito en ambos workflows |
| Huellas de finalización | `tools/modernization/reference-completion.json` | 29 fases públicas y resultados esperados de campaña; no son hashes del estado |
| Huellas lógicas H3 | `tools/modernization/reference-gameplay-v1.json` | 11 fases, 11.361 estados muestreados; sin rebaselinar |

No incluir ni publicar el archivo ZIP privado con datos comerciales CD32. Que la carpeta personal contenga archivos CD32 **no** significa que exista una referencia automatizada de las 72 fases de esa campaña.

## 2. Matriz de versiones y procedencia de dependencias

| Componente | Windows x64 | Linux x64 | Riesgo o diferencia |
|---|---|---|---|
| Ejecutor probado | GitHub Actions `windows-2022` | `ubuntu-latest`, resuelto como **Ubuntu 24.04** (imagen `ubuntu24/20261012.334`) | Imágenes de CI pueden renovarse |
| Generador / compilador | Visual Studio 17 2022, **MSVC 19.44.35229.0**, compilador MSVC 14.44.35207 | Ninja, **GNU C++ 13.3.0**, CMake 3.28.3 según paquetes del job | Toolchain distinto y no fijado a un contenedor inmutable |
| Python en CI | `actions/setup-python@v5` pide **3.12** | Python 3.12.3 localizado durante CMake | Python de Linux procede del ejecutor |
| SDL3 | Etiqueta `release-3.4.0` obtenida con CMake `FetchContent` | Clon `--depth 1 --branch release-3.4.0`; log `SDL-3.4.0-release-3.4.0` | Versión nominal fijada por etiqueta, no SHA completo registrado en CI |
| SDL3_mixer | Commit `3045b35335113e5e5ba258858cb403d8803bfbeb`, configurado como **3.1.0** | Clon de la rama predeterminada **sin commit ni etiqueta**, configurado como **3.3.0** el 21/10 | **Principal brecha de reproducibilidad:** futuras ejecuciones Linux pueden cambiar |
| Decodificación MOD/XMP | `SDLMIXER_VENDORED=ON`, `SDLMIXER_MOD_XMP=ON`, `LITE=ON` | `SDLMIXER_VENDORED=OFF`, `MOD_XMP=ON`, `LITE=OFF`; libxmp sistema 4.6.0-2 | Diferencias reales del backend de audio; no se comparó reproducción audible bit a bit |
| FFmpeg | `OPENFODDER_ENABLE_FFMPEG=OFF` | Compilación normal: `OPENFODDER_AUTO_FFMPEG=ON`, `Found FFmpeg`, bibliotecas dev de Ubuntu (p. ej. libavcodec de FFmpeg 6.1.1); ASan/TSan: `OPENFODDER_AUTO_FFMPEG=OFF` | Diferencia de funcionalidad opcional: intros/vídeo no reciben una regresión equivalente |
| hilos/SDL audio y vídeo | SDL con DLL en paquete; prueba manual inicial anterior | Ejecución de sanitizadores con `SDL_VIDEODRIVER=dummy` y `SDL_AUDIODRIVER=dummy` | El modo dummy no valida dispositivo real, latencia ni callbacks reales |
| FFmpeg/vcpkg | `vcpkg.json` declara FFmpeg opcional con manifiesto `version-string=0.0.0`, baseline vcpkg `af752f21c9d79ba3df9cb0250ce2233933f58486` | CI utiliza paquetes apt, no vcpkg | La presencia del manifiesto vcpkg no significa que esa versión se use en los jobs descritos |

**Observación verificable:** los logs [Windows 39641852057](https://github.com/Cacheirez/openfodder/actions/runs/39641852057) y [Linux 39641851896](https://github.com/Cacheirez/openfodder/actions/runs/39641851896) contienen las versiones anteriores. En Linux no se registra el **SHA exacto** del checkout de SDL3_mixer; `3.3.0` identifica la versión configurada en *esa* ejecución, no constituye una revisión fijada.

**No es una incompatibilidad demostrada:** ambos entornos pasaron su regresión disponible. Tampoco es una diferencia técnicamente inevitable. Para H2.6, conviene fijar el checkout Linux por SHA, registrar las revisiones efectivas de SDL3 y SDL3_mixer e identificar una matriz de audio soportada antes de aceptar una base reproducible.

## 3. Matriz de cobertura funcional y de plataformas

Los 29 casos de finalización del manifiesto provienen de **siete campañas públicas**, sin contar como fases adicionales los registros de resumen de campaña.

| Campaña / origen | Fases de finalización comprobadas Windows/Linux | Traza lógica H3 por fase | ASan/UBSan, LSan y TSan Linux |
|---|---:|---|---|
| Cannon Fodder Plus | 4 | No | Sí, en modo headless |
| Amiga The One | 3 | **Sí** | Sí, en modo headless |
| Amiga Action | 4 | No | Sí, en modo headless |
| Amiga Power Alien Levels | 4 | No | Sí, en modo headless |
| Amiga Format Christmas Special | 2 | No | Sí, en modo headless |
| Amiga Format Not Very Festive | 4 | No | Sí, en modo headless |
| PC Format | 8 | **Sí** | Sí, en modo headless |
| **Total** | **29/29** | **11/29 fases: 11.361 estados** | **29/29 fases** |

Las trazas H3 suman **7.956 estados de PC Format** y **3.405 de Amiga The One**, idénticos entre repeticiones y entre Windows/Linux para los campos registrados. Se mantienen sus metadatos por plataforma. Los replays de finalización no equivalen a trazas completas para las otras 18 fases.

| Escenario de uso | Windows | Linux | Valoración |
|---|---|---|---|
| Compilación y tests unitarios CTest | PASS | PASS | Demostrado en CI |
| 29 replays demo de finalización | PASS | PASS | Demostrado en CI |
| H3: 11 fases, 11.361 estados | PASS | PASS | Demostrado para campos/ticks muestreados |
| ASan/UBSan sobre 29 fases | No ejecutado en el workflow Windows | PASS, sin hallazgos | Demostrado solo en Linux |
| LeakSanitizer sobre 29 fases | No ejecutado | PASS, cero fugas detectadas | Demostrado solo en Linux |
| ThreadSanitizer sobre 29 fases | No ejecutado | PASS, cero carreras detectadas | Demostrado solo en Linux; paso de CI aún no bloqueante |
| Gameplay manual clásico, mando/ratón/teclado/sonido/pausa/F11/Alt+Tab | Confirmado por el usuario en la versión anterior | No documentado | No implica validación manual de la revisión actual |
| Audio físico, alternar opciones, pantalla real, diferentes FPS | Cobertura automática insuficiente | Solo dispositivo dummy en sanitizadores | Pendiente |
| Campaña privada CF1 CD32 (72 pares MAP/SPT presentes localmente) | Arranque y jugabilidad inicial confirmados manualmente | No cubierta por CI | 72 fases sin replay/equivalencia automatizada |
| Cannon Fodder 2 | Compilación de rutas del motor, no campaña completa | Idem | Fuera del alcance de modernización v1; no prometer cobertura exhaustiva |
| H4: 0/1/N dibujos por tick y `mWasDrawn` | No ejecutado | No ejecutado | Pendiente de separación del renderizado |

## 4. Evidencias y fiabilidad de los resultados

- [Linux Actions 39641851896](https://github.com/Cacheirez/openfodder/actions/runs/39641851896): ASan/UBSan, LSan y TSan terminan cada uno **29 fases, 0 omisiones y retorno 0**. Se inspeccionó el artefacto `OpenFodder-Linux-H3-evidence`, incluidos los tres `report.json` y `engine.log`; ZIP íntegro (CRC correcto). No hay `ERROR: AddressSanitizer`, `runtime error:`, `ERROR: LeakSanitizer` ni `WARNING: ThreadSanitizer` en esas ejecuciones.
- [Windows Actions 39641852057](https://github.com/Cacheirez/openfodder/actions/runs/39641852057): compilación x64 Release, CTest, 29 replays y baseline H3 con resultado satisfactorio.
- [H3_VALIDACION_2026-10-21.md](H3_VALIDACION_2026-10-21.md): metodología, origen de 11.361 estados y limitaciones.
- [H2_LEAK_THREAD_DIAGNOSTICOS.md](H2_LEAK_THREAD_DIAGNOSTICOS.md): hallazgos originales, correcciones y auditoría ampliada.
- [PLAN_MODERNIZACION_ES.md](PLAN_MODERNIZACION_ES.md): separación entre simulación y presentación; reglas de no alteración de gameplay.

Los artefactos Actions tienen caducidad. La evidencia permanente mínima la constituyen las referencias de replays y huellas en el repositorio más este inventario; conviene conservar el ZIP de la prueba cuando se haga la decisión H2.6.

## 5. Riesgos residuales y recomendación para H2.6

1. **Dependencia no congelada:** SDL3_mixer Linux se clona desde la rama predeterminada sin SHA. Registrar/fijar ese commit y volver a pasar la batería antes de calificar el build de reproducible.
2. **Variantes de audio y vídeo:** SDL_mixer 3.1 Windows vs 3.3 Linux, backend XMP y disponibilidad de FFmpeg distintos. El resultado CI prueba la base de simulación y carga de recursos, **no** equivalencia acústica/vídeo.
3. **Cobertura comercial limitada:** CD32 privada no puede publicarse ni introducirse en runners públicos; es necesaria una matriz de fases/replays de ejecución privada si se desea aceptar cobertura comercial.
4. **H2.1 pendiente documental:** se reparó y probó el lector RNC acotado (H2.2); la atribución exacta del primer recurso mínimo histórico sigue abierta y debe quedar aceptada expresamente como riesgo residual o cerrarse con evidencia defensiva.
5. **Carreras de interacción no ensayadas:** TSan cubrió 29 replays con SDL dummy, no todas las transiciones de GUI ni callback de audio real. `continue-on-error: true` para TSan sigue presente pese al informe limpio; conviene convertirlo en barrera obligatoria después de asegurar diagnóstico reproducible.
6. **No anticipar H4:** `mWasDrawn`, visibilidad lógica, cámara, tiempo y entrada deben mantenerse al separar dibujo; la prueba 0/1/N aún no se ha ejecutado.

**Dictamen H2.5:** inventario, diferencias y cobertura **cerrados y trazables**. Esto **no** equivale a aprobar H2.6 ni a proclamar soporte probado de toda CF1 CD32. La acción siguiente será elaborar la ficha de aceptación H2.6, resolver o aceptar los riesgos concretos y conservar una base recuperable sin fusionar el PR automáticamente.
