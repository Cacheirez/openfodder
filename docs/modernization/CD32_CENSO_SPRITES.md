# CD32 — censo de tipos, recursos y capacidades de entidades

26-10-2026. Inspección de los recursos CD32 privados suministrados, sin modificar ni publicar imágenes, mapas, posiciones ni ficheros originales. Resultado: **24 misiones, 72 fases, 1.951 registros SPT, 167 de tipo Null; 72 IDs distintos contando Null (71 excluyéndolo)**. Son registros iniciales, no el total de objetos visibles ni de entidades generadas durante una partida. Los 72 IDs encontrados tienen manejador localizado en el motor. Cinco conjuntos de entorno: jun, des, ice, mor, int.

## Dónde está cada parte

| Capa | Fuente | Papel |
|---|---|---|
| Orden de misión/fase | `Run/Campaigns/Cannon Fodder.ofc` y `Source/Campaign.cpp` | Asocia misión/fase a `mapmN`; 72 mapas no significa 72 misiones |
| Instancias iniciales | `mapmN.spt` | Registros de cinco palabras big-endian, 10 bytes: dos campos iniciales que el cargador no usa como capacidades, X, Y, ID de tipo |
| Terreno y selección de recursos | `mapmN.map` | Cabecera con nombres base/sub y geometría; mosaico de tiles |
| Tipos y despacho | `Source/Sprites.hpp`, `Source/Sprites.cpp` | Enum de tipos y tabla que elige `Sprite_Handle_*`; 118 slots incluyen reservados y tipos CF2 |
| Comportamiento | `Source/Sprites/Sprite_*.cpp` | Movimiento, daño, entradas/salidas, armas, creación de auxiliares y transformaciones |
| Imágenes Amiga/CD32 | `<prefijo>army.lbm`, `<prefijo>copt.lbm` | Hojas gráficas seleccionadas por la cabecera de mapa |
| Fotogramas y geometría gráfica | `Source/Amiga/SpriteData_Amiga.hpp`, `Source/SpriteSheet.*` | Segmento, offset, dimensiones y anclajes; ID de tipo no equivale a índice de hoja |
| Colisión/destrucción del terreno | `*.hit`, `*.bht`, `*.swp`, `Source/Tiles.cpp`, `Source/Map/MapRuntime.cpp` | Tipos y filas de terreno, sustituciones al destruir, excepciones de indestructibilidad |

`Source/Map/Original.cpp::loadCF1Spt` consume 10 bytes por registro aunque su estimación inicial de capacidad utiliza `/8`: no confundir esa reserva con el tamaño del registro. El inventario usa el recorrido real de cinco palabras, corroborado por `saveCF1Sprites`. Falla ante tamaños incompletos o entradas comprimidas no soportadas; no rellena silenciosamente datos.

## Helicóptero controlable: comprobación concreta

Los tipos 49/50/51/52 son variantes Human (granadas/sin armas/misiles/guiados). Los tipos 101–104 son variantes Human_Called; 99 es la plataforma. El censo CD32 encuentra 102/103/104, pero no 101 colocado inicialmente. Hay variantes enemigas 40/42/43/44 y 107. Un mismo aspecto puede tener distinto comportamiento.

| Ejemplo confirmado en los ficheros | ID | Misión/fase | Imagen seleccionada para IN_GAME2 |
|---|---:|---|---|
| `mapm30.spt`, helicóptero sin armas Human | 50 | 11/3 | `juncopt.lbm` |
| `mapm38.spt`, Human con misiles guiados | 52 | 14/1 | `descopt.lbm` |
| `mapm42.spt`, Human con granadas | 49 | 15/2 | `morcopt.lbm` |
| `mapm49.spt`, Human con misiles | 51 | 18/3 | `intcopt.lbm` |
| `mapm36.spt`, Human_Called sin armas + plataformas | 102, 99 | 12/6 | `icecopt.lbm` |
| `mapm52.spt`, Human_Called con misiles + plataformas | 103, 99 | 19/1 | `intcopt.lbm` |
| `mapm72.spt`, Human_Called guiado + plataformas | 104, 99 | 24/6 | `intcopt.lbm` |

En `Sprite_Helicopter.cpp` el cuerpo selecciona hoja `0x8B`; los slots auxiliares adyacentes seleccionan `0x8C` y `0x8D` para hélice/sombra. En la tabla Amiga CF1 corresponden a `stru_8D798`, `stru_8D898`, `stru_8D8D8`, todas del segmento `eGFX_IN_GAME2`; `Graphics_Amiga.cpp::Map_Load_Resources` carga ese segmento desde `copt.lbm`. Es un objeto compuesto: capturarlo como una única escritura o ignorar sus auxiliares perdería animación, altura y orden.

`Sprite_Vehicle.cpp::Sprite_Find_HumanVehicles` comprueba bando Human y `mVehicleEnabled`, además de existencia; `Sprite_Handle_Player_Enter_Vehicle` comprueba objetivo/proximidad y asigna `mCurrentVehicle`/`mInVehicle`. La salida y el vuelo tienen condiciones de altura/terreno. Por tanto, “manejable” es capacidad del tipo **y** disponibilidad del estado actual, no un booleano del SPT.

## Clasificación: varias dimensiones, no categorías excluyentes

| Dimensión | Qué registrar y comprobar |
|---|---|
| Movilidad | Fijo en reposo, móvil, volador; un objeto inicialmente fijo puede moverse como escombro |
| Daño | Indestructible, destruible, resistente/condicional; tipos de impacto y excepciones |
| Control | IA, jugador, ocupable, control remoto/llamada; requisitos de bando, activación, altura y ocupación |
| Papel | Actor, decoración, arma, efecto, proyectil, objetivo, generador o auxiliar |
| Composición | Cuerpo/hélice/sombra/luces, padre y auxiliares; orden y altura |
| Ciclo de vida | Inicial en SPT, creado dinámicamente, transformación y reutilización de slot |
| Apariencia | Plataforma, tileset, segmento, hoja, frame, paleta, dimensiones y anclajes |

Ejemplos de revisión ya verificados: arbusto/árbol/tejado/muñeco de nieve (13–17) llaman a `Sprite_Handle_Exploidable`; no son simplemente decorado permanente. Cascada (18) anima tres frames en su manejador sin desplazamiento propio. Puertas generan enemigos y tienen rutas de explosión. Puerta reforzada (100) tiene resistencia condicionada al estado y contador; no etiquetarla automáticamente como invulnerable. Los nombres Turret_Missile_Human/Enemy no bastan: algunos seleccionan internamente `eVehicle_Turret_Cannon`. Los tipos explícitamente Invulnerable 112/113 están bajo CF2 y no aparecen en estos SPT de CD32; no usarlos para completar artificialmente una categoría de CF1.

Los elementos del terreno requieren un inventario aparte: una pared/roca dibujada como tile no tiene por qué existir como sprite. Las listas `mTiles_Indestructible_*` contienen excepciones por entorno. Tampoco todos los efectos están colocados en SPT: proyectiles, humo, explosiones, sombras y enemigos generados deben añadirse siguiendo creación y transformación en el código, y comprobarse durante ejecución.

## Qué queda por hacer antes de dar el catálogo por completo

1. Revisar capacidades de cada familia y sus condiciones, con referencia a función/estado; el JSON marca esta revisión pendiente y no inventa etiquetas a partir del nombre.
2. Completar el grafo de creación/transformación y los auxiliares, además del censo de tiles y destrucción.
3. Resolver variantes gráficas por los cinco entornos y estados de animación/daño/ocupación; exportar un atlas de contacto privado mediante el decodificador real.
4. Seleccionar fases representativas que cubran todas las familias/estados, incluida entrada, vuelo, aterrizaje, salida y destrucción de helicópteros. Censo estático de 72 fases no equivale a 72 fases jugadas ni a cobertura de todos los estados.
5. Usar esa identidad semántica para el piloto gráfico. Mantener el primer soldado como caso mínimo, añadiendo el helicóptero como primer caso compuesto exigente; no diseñar el catálogo completo extrapolando las demos.

## Reproducción

```bash
python3 tools/modernization/inventory_cf1_sprites.py \
  --data /ruta/privada/Data/Amiga_CD \
  --campaign 'Run/Campaigns/Cannon Fodder.ofc' \
  --out /ruta/privada/censo.json
```

[Datos derivados: mapa, tipo, recuentos y selección de recursos](evidence/cd32-sprite-census.json). No contienen coordenadas ni bytes gráficos. No se ha ejecutado la lógica de las fases para construir este censo ni alterado el motor.

## Tipos colocados inicialmente

`Null` incluye reservas/auxiliares; no tratar cada registro como objeto independiente visible. La columna de mapas de cada tipo está completa en el JSON.

| ID | Tipo del motor | Registros SPT | Mapas que lo contienen | Primer mapa por orden de campaña |
|---:|---|---:|---:|---|
| 0 | Player | 254 | 72 | mapm1 |
| 4 | Null | 167 | 51 | mapm7 |
| 5 | Enemy | 215 | 38 | mapm1 |
| 13 | Shrub | 19 | 11 | mapm1 |
| 14 | Tree | 25 | 15 | mapm1 |
| 15 | BuildingRoof | 55 | 22 | mapm3 |
| 16 | Snowman | 8 | 6 | mapm9 |
| 17 | Shrub2 | 2 | 2 | mapm13 |
| 18 | Waterfall | 14 | 6 | mapm28 |
| 20 | BuildingDoor | 114 | 44 | mapm3 |
| 24 | GroundHole | 23 | 15 | mapm7 |
| 25 | BuildingDoor2 | 17 | 9 | mapm7 |
| 27 | Floating_Dead_Soldier | 4 | 4 | mapm3 |
| 36 | Enemy_Rocket | 127 | 39 | mapm9 |
| 37 | GrenadeBox | 33 | 17 | mapm3 |
| 38 | RocketBox | 26 | 15 | mapm8 |
| 40 | Helicopter_Grenade_Enemy | 5 | 5 | mapm29 |
| 41 | Flashing_Light | 188 | 48 | mapm16 |
| 42 | Helicopter_Unarmed_Enemy | 4 | 4 | mapm23 |
| 43 | Helicopter_Missile_Enemy | 8 | 7 | mapm39 |
| 44 | Helicopter_Homing_Enemy | 2 | 2 | mapm64 |
| 49 | Helicopter_Grenade_Human | 5 | 5 | mapm42 |
| 50 | Helicopter_Unarmed_Human | 11 | 11 | mapm30 |
| 51 | Helicopter_Missile_Human | 4 | 4 | mapm49 |
| 52 | Helicopter_Homing_Human | 8 | 8 | mapm38 |
| 54 | Mine | 42 | 12 | mapm26 |
| 55 | Mine2 | 4 | 3 | mapm8 |
| 56 | Spike | 28 | 10 | mapm17 |
| 60 | BoilingPot | 4 | 4 | mapm7 |
| 61 | Civilian | 14 | 7 | mapm7 |
| 62 | Civilian2 | 9 | 6 | mapm13 |
| 63 | VehicleNoGun_Human | 4 | 4 | mapm11 |
| 64 | VehicleGun_Human | 9 | 9 | mapm16 |
| 65 | Tank_Human | 15 | 14 | mapm27 |
| 66 | Bird_Left | 13 | 13 | mapm1 |
| 67 | Bird_Right | 9 | 5 | mapm2 |
| 68 | Seal | 37 | 10 | mapm15 |
| 69 | Tank_Enemy | 17 | 11 | mapm25 |
| 70 | Civilian_Spear | 9 | 8 | mapm16 |
| 72 | Hostage | 13 | 7 | mapm35 |
| 73 | Hostage_Rescue_Tent | 8 | 8 | mapm35 |
| 74 | Door_Civilian | 7 | 6 | mapm21 |
| 75 | Door2_Civilian | 9 | 8 | mapm13 |
| 76 | Door_Civilian_Spear | 19 | 9 | mapm20 |
| 78 | Turret_Missile_Human | 31 | 18 | mapm18 |
| 79 | Turret_Missile2_Human | 12 | 9 | mapm25 |
| 80 | VehicleNoGun_Enemy | 4 | 3 | mapm20 |
| 81 | VehicleGun_Enemy | 6 | 6 | mapm21 |
| 82 | Vehicle_Unk_Enemy | 1 | 1 | mapm60 |
| 83 | Civilian_Invisible | 1 | 1 | mapm60 |
| 84 | Turret_Missile_Enemy | 91 | 29 | mapm21 |
| 85 | Turret_Missile2_Enemy | 39 | 9 | mapm24 |
| 88 | BuildingDoor3 | 97 | 33 | mapm18 |
| 90 | Door_Civilian_Rescue | 2 | 2 | mapm29 |
| 91 | Seal_Mine | 8 | 5 | mapm31 |
| 92 | Spider_Mine | 19 | 3 | mapm33 |
| 93 | Bonus_RankToGeneral | 2 | 2 | mapm19 |
| 94 | Bonus_Rockets | 1 | 1 | mapm19 |
| 95 | Bonus_Armour | 1 | 1 | mapm34 |
| 96 | Bonus_RankHomingInvin_SquadLeader | 1 | 1 | mapm53 |
| 98 | Bonus_RankHomingInvin_Squad | 1 | 1 | mapm59 |
| 99 | Helicopter_CallPad | 9 | 3 | mapm36 |
| 100 | BuildingDoor_Reinforced | 1 | 1 | mapm36 |
| 102 | Helicopter_Unarmed_Human_Called | 1 | 1 | mapm36 |
| 103 | Helicopter_Missile_Human_Called | 1 | 1 | mapm52 |
| 104 | Helicopter_Homing_Human_Called | 1 | 1 | mapm72 |
| 105 | Turret_HomingMissile_Enemy | 8 | 3 | mapm59 |
| 106 | Enemy_Leader | 1 | 1 | mapm71 |
| 107 | Helicopter_Homing_Enemy2 | 1 | 1 | mapm72 |
| 108 | Computer_1 | 1 | 1 | mapm70 |
| 109 | Computer_2 | 1 | 1 | mapm71 |
| 110 | Computer_3 | 1 | 1 | mapm72 |
