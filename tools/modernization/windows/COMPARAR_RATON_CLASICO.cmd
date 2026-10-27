@echo off
setlocal
cd /d "%~dp0"
set "OPENFODDER_MISSION_SCREEN_TRANSFORM=0"
set "OPENFODDER_CAPTURE_SOLDIER=0"
set "OPENFODDER_REPLACE_SOLDIER_POSE=0"
set "OPENFODDER_SOLDIER_ART=0"
set "OPENFODDER_PRESENT_MISSION_LAYERS=0"
set "OPENFODDER_AUDIT_MISSION_LAYERS=0"
openfodder.exe --window --alternate-mouse --skipintro > H5_RATON_CLASICO.log 2>&1
if errorlevel 1 (
  echo Error: see H5_RATON_CLASICO.log
  pause
)
endlocal
