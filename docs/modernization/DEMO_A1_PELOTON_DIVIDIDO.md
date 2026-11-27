# Continuidad al dividir pelotón y diagnóstico del reinicio

20-11-2026. Hito de continuidad en curso. Miguel observa clásico al dividir mientras dos grupos siguen visibles, y al aparecer soldados tras reinicio por muerte total. Las muertes parecen mejorar, sin asegurar todos los casos. No se declara aceptación global. [Captura y censo](evidence/reinicio-division-revision-20261120.json).

## Evidencia y corrección acotada

La partida correcta 13:24 registra 12.427 publicaciones HD, 1.049 faltantes y diez retornos brutos del mismo jugador. Cinco claves de postura baja 0x12–0x16/F0 afectan 1.022 intentos. Sus capturas independientes coinciden exactamente en semántica, geometría, recursos y paleta con las referencias cualificadas en el bloque de sombras; los descriptores de cuerpo y sombra también coinciden con los actuales. Se enlazan **solo esas cinco claves observadas**, sin crear imágenes ni incorporar el lote de 53 referencias. Microbloque publicado en `2004160`. [Evidencia de cinco poses](evidence/peloton-apuntado-cinco-20261120.json).

Después se comprueban 0x10/0x11/0x17/F0, ya observadas en el registro 15:13, con la misma prueba de procedencia y cualificación. No son direcciones nuevas de arte: completan las ocho poses existentes de esta misma familia y evitan depender de otra orientación para conservarla. Constructor `tools/modernization/prepare_observed_aim_bindings.py`: paso inicial y opción explícita `--completion`, cada uno con su contrato, claves y descriptores cualificados. [Evidencia del cierre](evidence/peloton-apuntado-completo-20261120.json).

Candidato final **244 activos /399 vínculos**, ocho claves observadas nuevas sobre 244/391; todos los píxeles, sombras, anclajes y vínculos anteriores intactos. No cambian selectores de pose/dirección, física ni lógica. Se conserva la recuperación completa ante fallos reales y no se incorpora arte enemigo nuevo.

## Pruebas y medición

PASS 40 casos Window por plataforma en el primer bloque, 24 en el segundo y ocho de carga/composición del manifiesto completo: **72 casos por plataforma**. Densidades 8×/12×, dos actores solapados, altura 12, recorte de tres filas, oclusión con escritura de cero, claves/datos incorrectos rechazados, igualdad píxel a píxel de SDL con el oráculo de composición expandida y recuperación clásica completa ante fallo SDL. Windows ASan/UBSan y Linux ASan/UBSan/LSan sin hallazgos.

La copia diagnóstica nueva pasa H3 local completo Windows/Linux, 11 fases/11.361 estados por sistema. Replay real del primer bloque a 244/396: mismos 1.546 estados M1P2, 4.465 publicaciones y 89 faltantes en ambos sistemas. Las tres últimas claves no requieren repetir ese replay: manifiesto completo 244/399 ya probado en Window, mismos píxeles/motor y sin claves nuevas presentes en esa muestra. Se mantiene la distinción entre pruebas ejecutadas y proyecciones.

**Proyecciones de registros retenidos, no partidas nuevas:** con las ocho claves, 13:24 pasa de 12.427 a 13.449 publicaciones y de 1.049 a 27 faltantes; diez a siete retornos brutos y cuatro rachas breves conservadas. 15:13 pasa de 8.161 a 9.112 publicaciones y de cinco a tres retornos, con cero rachas breves. El recorrido 23:57 y el replay público no cambian respecto al candidato 244/391. No se afirma que toda división futura esté cubierta ni se confunde esto con aceptación jugando.

CI completa de `46229d6` PASS Windows/Linux/densidades. Código de producción de renderizado intacto; CI de los nuevos metadatos/constructores pendiente al publicar. Las pruebas focalizadas anteriores siguen siendo válidas y no se repiten por rutina.

Consulta antes del relevo: `2004160` pasa [densidades](https://github.com/Cacheirez/openfodder/actions/runs/44737908744); [Windows](https://github.com/Cacheirez/openfodder/actions/runs/44737908801) y [Linux](https://github.com/Cacheirez/openfodder/actions/runs/44737908817) siguen en curso, sin atribuirles PASS completo. La CI del cierre de tres direcciones se consultará por su propio SHA.

## Reinicio: diagnóstico, sin desactivar protecciones

La escena posterior del registro 13:24 tiene 293 publicaciones HD y ningún faltante. Los avisos antiguos `palette-transition` y `black-palette` carecen de escena, por lo que **no acreditan por sí solos la causa del tramo clásico observado**. No se declara corregido ni se fuerza HD durante una transición no verificada.

`tools/modernization/make_hd_scene_probe.py` transforma únicamente el bloque de diagnóstico de la copia local ya instrumentada: razones una vez por escena, máximo 40 por escena y 256 por proceso, con número de escena y de llamada de presentación. La reversión exacta de las sustituciones demuestra que no cambian guardias, rasterizado ni simulación. Esta copia se compila aparte; no sustituye los motores anteriores. Los campos nuevos pasan comprobación real Windows/Linux (límites, llamadas monótonas e identidad de escena coincidente con las publicaciones).

## Próxima revisión y recuperación

Ejecutar `PROBAR_PELOTONES_P1.cmd` en `C:/Users/migue/.codex/visualizations/2026/11/19/01a1f3ca-14cf-76a1-a9ab-bf2ff6bf17c3/`. `Probar-P1-Pelotones.ps1 -Comprobar` verifica SHA-256 del motor/manifiesto y los 244 activos/399 vínculos. Logs `OpenFodder-P1-Pelotones-*.log` en TEMP; capturas `pelotones-snapshots-*`. Probar división con dos pelotones y orientaciones, reinicio por muerte total y aparición. La valoración visual y jugable sigue reservada a Miguel.

Fuentes y proyectos locales `split-probe/`, `split-probe-linux/`; motores `split-probe-build/Release/native_probe.exe`, `split-probe-linux-build/native_probe`; candidato `split-complete-candidate/`; scripts `prepare_split.py`, `prepare_split_completion.py`, `check_split_runtime.py`. Pruebas/huellas en las evidencias; recursos privados y capturas fuera de GitHub. Constructor requiere archivos nativos y directorio de recursos, conserva salida existente y exige destino nuevo. Los originales/lanzadores anteriores y ZIP ajeno permanecen intactos.

**Siguiente tarea única:** revisión jugando de Miguel; después contrastar el reinicio y faltantes restantes, sin ampliar arte ni familias automáticamente. Hito en curso; ambos microbloques técnicos comprobados; aceptación pendiente. Agua/granadas/final pendientes, B/scroll/16:9 sin autorización. Escalado NO; nuevo hilo no necesario.
