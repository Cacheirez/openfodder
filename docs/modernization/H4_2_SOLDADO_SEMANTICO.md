# H4.2/H4.4 — piloto semántico de un soldado con gráficos originales

26-10-2026. Base de implementación: d1d30f12. PR #1 en borrador y sin fusionar; base clásica5e6a4f38 intacta. No se activa la ruta por defecto.

## Implementación

`OPENFODDER_CAPTURE_SOLDIER=1`, junto con auditoría o publicación de misión, captura el primer slot Player presente. Se excluyen pausa, overview, fuera de misión, ocupantes de vehículos, retirada pendiente y dibujos no visibles. Los demás sprites siguen su ruta actual. Es un piloto del cuerpo de un soldado, no una captura de todos los actores ni de sus sombras/insignias.

`Sprite_PrepareLegacyFrame` sigue resolviendo el recurso, preparando recortes y actualizando los registros/mWasDrawn en sus momentos originales. Su hook llama a `CaptureSoldierSemantic` y guarda por valor escena, slot, generación, tick lógico (int16 heredado, no reloj monotónico), cámara fija, posición y fracciones, altura, dirección, estado, hoja/frame/segmento y geometría/anclaje originales. La posición entera, recorte de filas y anclajes están en geometry; sus fracciones se conservan aparte. La proyección usa los valores reales de mMapTile_DrawX/Y, además de conservar mCameraX/Y: no son intercambiables.

La generación de presentación se renueva en `sSprite::Clear`, con un contador atómico propio que no consume RNG ni entra en las trazas H3 o en la serialización explícita de mapas. `Sprite_Clear_All` renueva la escena; recargar los mismos sprites del mapa no reutiliza la identidad anterior de escena. El slot completa la identidad. La copia de un objeto conserva su token, pero una recarga tiene otra escena y Clear cambia el token. No se garantiza aún un contrato genérico para todas las transformaciones o asignaciones de otros tipos: el piloto solo acepta Player y no interpola.

`Video_Draw_8_Resolved` conserva el raster clásico. Cuando hay captura válida, el registro recibe una operación Soldier en su posición original, con destino original y recurso de bytes inmutables propio. El registro elimina los punteros prestados de draw/geometry. La operación recompone la geometría desde el snapshot y rasteriza desde el recurso retenido; no copia el resultado clásico. Antes de rasterizar exige igualdad exacta de geometría preparada (posición, dimensiones, recorte, formato y paleta) con la preparación clásica. Una discrepancia falla, aunque otra capa pudiera taparla. No se permite aún transformar/interpolar esas coordenadas.

El contraste vigente verifica índices, fondos guardados y RGB con paleta efectiva tardía. No se recrean soldados, no se invocan manejadores ni se consumen eventos durante presentación. Las presentaciones 0/1/5 no repiten la captura. La escena de órdenes se invalida como antes al entrar en pausa; cada registro tiene un ID de intervalo nuevo. El snapshot retenido se puede reproducir privadamente, pero no autoriza publicar una escena obsoleta ni unir intervalos a través de pausa/carga.

## Activación y reproducción

```bash
SDL_VIDEODRIVER=dummy SDL_RENDER_DRIVER=software SDL_AUDIODRIVER=dummy \
python3 tools/modernization/check_mission_publication_replays.py \
  --exe build/openfodder --data Run --out reports/h4-soldier-full --soldier-probe
```

El runner registra la opción, la desactiva explícitamente cuando no se solicita y exige una marca de captura contrastada por escena/fase, sin aceptar solo que el proceso termine. Conserva H3 original. Para la matriz acotada añadir `--presentations 0|1|5 --pause-probe --first-phase`: dos fases y301 estados por política, no la campaña completa.

Linux CI mantiene las pruebas anteriores y añade once fases con el piloto activo, más pausa0/1/5 acotada. ASan/UBSan/LSan y TSan de pausa incorporan el piloto en sus dos fases declaradas. Windows añade la matriz acotada0/1/5 con pausa después de sus replays clásicos. Vídeo software no sustituye Windows/GPU/manual.

## Evidencia y límites

- CI anterior d1d30f12: Windows40317787797 y Linux40317787809 completed/success, consultados al terminar la revisión. Resuelve el fallo CRLF documentado del comprobador anterior; no acredita automáticamente este código nuevo.
- `check_soldier_semantic.py`: PASS local ASan/UBSan, ejecuta los cuerpos reales de Clear, Sprite_Clear_All y CaptureSoldierSemantic con entradas controladas. Comprueba datos, filtros, primer slot, reutilización de slot y recarga de escena. Consulta de hoja/SDL son fixtures; no hay una simulación alternativa.
- `check_mission_recording.py`: PASS local ASan/UBSan, las cuatro configuraciones conservan la huella15155017350506417091 y192 transiciones. Ahora los dibujos de soldado sintéticos usan el productor y la operación semántica reales. Comprueba recurso liberado, destino, pausa, 0/1/5, geometría alterada e identidad nula rechazadas. Sigue siendo una fixture, no una prueba manual.
- 28 pruebas Python PASS, incluido rechazo de cobertura semántica ausente/duplicada. Metadata gráfica y contrato de visibilidad se mantienen. Las huellas del manifiesto de capacidades se actualizaron exclusivamente para los tres archivos revisados con hooks de identidad; no se cambiaron goldens H3.
- Equivalencia anterior de recursos:10.944 casos PASS con ASan/UBSan. LSan local falló por acceso a /proc; la ejecución sin LSan se identifica como tal y CI mantiene LSan.
- Primer build local rechazado: un objeto PC salió vacío y el enlazado falló. Build posterior en tmpfs completo (72 unidades) aprobado antes de los últimos controles de geometría/marcadores. No se atribuye ese resultado al código final.
- Los resultados temporales del replay inicial y del último build se perdieron al reiniciarse el entorno; solo se observó finalización de las ocho fases PC antes del reinicio. No se declara aprobado H3 completo ni el build final por esa observación. La aceptación final del motor nuevo depende de su CI. La incidencia de escritura local permanece abierta.

Los seriales son identidad local de presentación, no IDs persistentes entre procesos. No se exportaron imágenes comerciales, mapas, partidas ni coordenadas privadas. El nuevo informe contiene solo código y evidencia de demos/fixtures.

## Continuación

Actualización: CI Windows de d28d99f9 aprobada (40374586200); Linux pendiente (40374585563). La [sustitución acotada de pose](H4_4_POSE_INDIVIDUAL.md) ya está implementada con pruebas locales de anclaje y retorno al clásico; su CI sigue pendiente. Después, conceptos H6.1; helicóptero como primer compuesto. Interpolación, contrato temporal completo, catálogo CD32, GPU y validación manual siguen pendientes. H4 global no queda cerrado.
