# Paquete de prueba Windows

Incluye ejecutable, dependencias y demos públicas; no campañas comerciales completas. Extraer el ZIP entero en una carpeta nueva antes de ejecutarlo. No hace falta instalar las herramientas de desarrollo para jugar.

## Arranque

- `INICIAR.cmd`: juego normal con presentación clásica por defecto.
- `PROBAR_SOLDADO_ANIMADO.cmd`: piloto experimental de seis poses a 12×, Amiga The One m1p2, velocidad normal.
- `SOLDADO_ANIMADO.html`: visor aislado del ciclo, con pausa; no es el render de la fase.

**Limitación confirmada del piloto f72d6e7:** alterna con el soldado clásico porque solo cubre algunas poses del primer jugador y hay retornos por composición. Está pendiente la sustitución completa. No interpretar el ZIP como soldado terminado ni pedir repetir esta misma validación sin una corrección.

## Descargar y comunicar incidencias

El artefacto se llama `OpenFodder-Windows-x64-demos` en Actions del repositorio Cacheirez/openfodder. Usar la ejecución vinculada al candidato indicado por el estado del proyecto; una ejecución verde no acredita aceptación visual completa. Los enlaces de Actions caducan.

Conservar `VERSION.txt`, `PRUEBAS.json`, `LOTE_PRUEBA.json` y, si se ejecutó el piloto, `SOLDADO_ANIMADO.log`. Indicar comando, fase, acción y error observado; un vídeo corto ayuda a localizar la alternancia. No es necesario volver a validar guardado/persistencia, estilo C ni C01 salvo una regresión concreta.

`VERSION.txt` puede identificar el merge temporal construido por CI. Eso no significa que el PR se haya fusionado. Los informes y el hash del ejecutable permiten relacionar cada paquete con sus pruebas. El alcance vigente y los cambios pendientes se consultan en docs/modernization/CONTINUIDAD.md del repositorio.
