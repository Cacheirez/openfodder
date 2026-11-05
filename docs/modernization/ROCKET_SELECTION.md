# Lanzacohetes del jugador: contrato de selección

Bloque interno A3, plan 2.74. Se ha comprobado la selección antes de producir arte. No se modifica el motor, el proyectil, los relojes ni las referencias H3. [Resultados y hashes](evidence/soldier-rocket-selection.json).

## Frames que hay que preparar

La familia se selecciona con offset `0x38` de la tabla humana: ocho hojas `0x39–0x40`. PC y Amiga declaran tres entradas por dirección, salvo la dirección 5, hoja `0x3E`, que declara cuatro. Las tablas y las funciones utilizadas se contrastan con la base clásica `5e6a4f3834a0a491468ea659f45f8e5f4fb785a8`.

| Ruta probada | Selección mientras dispara | Retorno |
|---|---|---|
| `Sprite_Handle_Troop_Animation` directamente | Reinicia frame/tick a 0 al cambiar a la hoja de cohete; mantiene frame 0 durante siete llamadas | La octava llamada limpia disparo/giro/tick y selecciona la postura nativa |
| Ratón con `field_43` | El llamador restaura el frame previo 0, 1 o 2, incluso después de cambiar de hoja | También conserva el frame al volver a marcha |
| Objetivo del arma con `field_43` | La misma conservación del frame previo 0, 1 o 2 | También conserva el frame al volver a marcha |
| Llamadores sin `field_43` | No restauran el frame previo; entrada en frame 0 | Postura del selector |

Por tanto, el encargo de las rutas ordinarias probadas necesita **ocho direcciones × tres poses**, vinculadas al frame que pide el original. No es un ciclo artístico 0–1–2 ni se debe introducir un reloj de presentación. Las siete llamadas no se convierten en una duración fija en segundos: el manejador completo puede invocar al selector varias veces.

La entrada 3 de la dirección 5 no aparece en estos casos con frame previo normal 0/1/2. Esto no demuestra inalcanzabilidad desde cualquier estado: un llamador puede restaurar un frame arbitrario. No producir o vincular ese cuarto frame sin una ruta/evidencia que lo requiera.

## Prioridades y límites

- Cambiar de hoja por dirección reinicia el tick del disparo.
- El apuntado estacionario válido se evalúa antes del cohete y no avanza su tick.
- El cohete se evalúa antes de la rama de agua; al terminar puede volver a nadar.
- Dos soldados intercalados conservan su propia dirección, frame y tick; la variable temporal compartida no impone la pose del otro.
- La creación del cohete inicializa tick 1, giro −1 y tipo 3. Se contrasta su función completa con la base clásica, pero no se ejecuta la asignación de proyectiles en esta prueba.

La fixture ejecuta los tres cuerpos de función originales, con geometría simulada. **2.703 aserciones y 576 muestras**, incluidas las rutas de restauración y regreso. Las aserciones siguen activas con NDEBUG; ejecución local con UBSan PASS. No ejecuta el manejador completo del jugador, no acredita cobertura de campaña, render SDL, GPU/CD32 ni aceptación de Miguel. No hay arte nuevo de cohetes todavía.

## Reproducción

Con historial de Git y la base clásica disponible, desde la raíz:

```bash
python tools/modernization/check_rocket_selection.py --out /ruta/nueva/rocket-selection.json
```

La opción `--emit` escribe la fixture C++ sin compilarla. CMake añade `openfodder_rocket_selector_tests` y CTest `soldier_rocket_original_selection`; la receta normal de compilación está en [DESARROLLO.md](DESARROLLO.md). La CI del commit que incorpora esta prueba debe comprobarse por separado; no atribuirle el verde del commit anterior.

Siguiente entrega: preparar primero los tres frames de una dirección, compararlos con sus poses nativas y probar la transición completa con dos soldados, oclusión y 8×/12× en WindowHD/SDL. Solo después ampliar las otras direcciones. Conservar intactos marcha, apuntado, granadas y C01.
