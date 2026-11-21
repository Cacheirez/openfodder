@echo off
setlocal
set "OPENFODDER_HD_DIAGNOSTICS=1"
set "OPENFODDER_HD_COMPARE=1"
cd /d "%~dp0"
set "OPENFODDER_MISSION_SCREEN_TRANSFORM=1"
set "OPENFODDER_MISSION_SCREEN_FIT=1"
set "OPENFODDER_CAPTURE_SOLDIER=1"
set "OPENFODDER_REPLACE_SOLDIER_POSE=0"
set "OPENFODDER_SOLDIER_ART=0"
set "OPENFODDER_PRESENT_MISSION_LAYERS=1"
set "OPENFODDER_AUDIT_MISSION_LAYERS=0"
set "OPENFODDER_SOLDIER_HD=12"
set "OPENFODDER_TEST_FIRST_PHASE=0"
set "OPENFODDER_TEST_MISSION_PAUSE=0"
set "OPENFODDER_TEST_MISSION_PRESENTATIONS="
echo Prueba automatica C01: PC Format completo. Puede tardar varios minutos.
echo Al terminar se abrira la comparacion. No requiere jugar manualmente.
openfodder.exe --appveyor --unit-test --nosound --window --alternate-mouse --campaign "PC Format" > C01_PRUEBA.log 2>&1
if errorlevel 1 goto failed
findstr /C:"SOLDIER_HD_COMPARE: saved C01_12.html" C01_PRUEBA.log >nul
if errorlevel 1 goto failed
start "" "C01_12.html"
exit /b 0
:failed
echo La prueba no ha confirmado C01. Conserva C01_PRUEBA.log.
pause
exit /b 1
