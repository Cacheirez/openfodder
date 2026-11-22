# Revisión final del pelotón modernizado — P1

Estado: **PASS técnico**, CI completa Windows/Linux y H6 sobre `b1d8bffa2183f149aa593b206c3243ffc8504b5d`. Catálogo 339/339 y 354 activos. **Aceptación visual/jugable global de Miguel pendiente.**

## Ejecutar en PowerShell

```powershell
& 'C:\Users\migue\.codex\visualizations\2026\11\19\01a1f3ca-14cf-76a1-a9ab-bf2ff6bf17c3\PROBAR_PROTAGONISTAS_COMPLETOS_P1.cmd'
```

El lanzador verifica SHA-256 del ejecutable, SDL3, manifiesto y todos los RGBA. Usa la misma partida pública Amiga The One M1P2 del diagnóstico anterior, con el catálogo completo y enemigos clásicos. Los originales comerciales y las capturas permanecen fuera de GitHub. El borrador previo al cierre de pausa se conserva en `player-review-before-pause-9709d08`; no es la entrega actual.

## Qué revisar en una partida

1. Aparición inicial y primer fotograma al reiniciar tras perder el pelotón: comprobar que el cuerpo visible ya usa el diseño moderno.
2. Pelotón dividido: mantener ambos grupos visibles, seleccionar cada grupo y lanzar una granada.
3. Daño, malherido desangrándose, caída y muerte: comprobar la continuidad del herido y de sus compañeros; observar sombras y apoyos.
4. Pausar y reanudar, también durante el fundido: conservar diseño, atenuación y texto de pausa; comprobar respuesta de ratón al reanudar.
5. Final de fase: revisar por separado saludo, celebración con brazo y salto, además del contacto/posición de sombras.

Si hay un defecto, basta indicar qué ocurrió y la ruta del registro que imprime el lanzador. No hace falta identificar claves ni fotogramas: el catálogo y el diagnóstico cubren las rutas del código. La comprobación humana valora apariencia y jugabilidad; no sustituye la cobertura automática ni obliga a descubrir estados uno a uno.

Comparación clásica: añadir `-Modo clasico` al mismo comando. Solo comprobar integridad: añadir `-Comprobar`. Se mantienen los lanzadores anteriores, incluido el de granadas.

## Alcance y continuación

Los cuerpos protagonistas, sus transiciones y sombras están cubiertos en el catálogo CF1. Los marcadores sin escritura conservan su función nativa; el actor flotante del mapa es independiente del protagonista muerto y sigue nativo. No se modernizan enemigos ni vehículos mediante este hito. El mapa general y escenas ajenas conservan su presentación propia.

Los replays disponibles son públicos PC/Amiga The One; las tablas Amiga/CD32 se han contrastado, pero no se atribuye aquí una ejecución comercial CD32 ni aceptación en GPU. El modo clásico, simulación, RNG, colisiones, reloj y referencia H3 permanecen independientes.

Siguiente tarea única tras completar la validación: revisión visual/jugable de Miguel. Correcciones dentro del hito están autorizadas si se observa un defecto. B, nuevas familias/escenarios, scroll y 16:9 requieren autorización específica.
