# Primera prueba en Windows

Esta compilación sigue mostrando los gráficos originales. Incluye un parche de límites al leer pistas de los mapas y las demos públicas del paquete de datos del proyecto. No incluye las campañas comerciales completas. El vídeo introductorio FFmpeg está desactivado.

## Descargar

1. Abre https://github.com/Cacheirez/openfodder/actions e inicia sesión.
2. Selecciona la ejecución de **Windows - modernization foundation** correspondiente a la rama `modernization/windows-foundation`.
3. Solo utiliza el paquete si la ejecución termina en verde. Abre el artefacto `OpenFodder-Windows-x64-demos` al final de esa página.
4. Extrae todo el ZIP a una carpeta nueva, por ejemplo `C:\Juegos\OpenFodder-Prueba`. No ejecutes el juego dentro del ZIP ni lo copies encima de otra instalación.

## Arrancar

Haz doble clic en **INICIAR.cmd**. Abre el juego en ventana y omite la introducción. El archivo se asegura de que el programa encuentre los datos de esa misma carpeta.

No necesitas Git, Python ni Visual Studio para jugar con este paquete. Si Windows informa de que falta MSVCP140.dll o VCRUNTIME140.dll, consulta la instalación del redistribuible de Visual C++ x64 en la documentación oficial de Microsoft: https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist . No descargues DLL sueltas.

## Primera comprobación, cinco minutos

1. Elige una demo disponible y entra en una misión.
2. Comprueba que puedes mover el grupo y disparar con el ratón.
3. Mueve la cámara y observa si el cursor coincide con lo que señalas.
4. Pausa y reanuda; cambia de aplicación y vuelve al juego.
5. Prueba F11 para cambiar entre ventana y pantalla completa.

Cuéntame qué demo has elegido, si se oye el sonido, si el ratón responde bien y cualquier error literal. Una captura de la pantalla del juego ayuda. No esperamos todavía gráficos HD ni un scroll distinto.

## Qué significa que las pruebas pasen

El paquete solo se prepara después de completar 29 fases de demos y comparar sus nombres/resultados con la referencia Linux. Eso no demuestra identidad por tick, ausencia de todos los errores de memoria ni funcionamiento correcto del audio o del renderizado real. Sigue pendiente un problema de lectura en el descompresor Amiga registrado en `RESULTADOS.md`.

`VERSION.txt` identifica la revisión. `PRUEBAS.json` contiene el resultado de esa ejecución Windows. Conserva ambos al comunicar problemas.
