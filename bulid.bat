@echo off
cd /d %~dp0src
echo Building ChipFlasher.exe...

:: Clean previous builds
del /f /q dist\ChipFlasher.exe 2>nul
rmdir /s /q build
del main.spec

pyinstaller --onefile ^
    --noconsole ^
    --name ChipFlasher ^
    --icon=assets\icon.ico ^
    --add-data "tools\\fastboot.exe;tools" ^
    --add-data "tools\\AdbWinApi.dll;tools" ^
    --add-data "tools\\AdbWinUsbApi.dll;tools" ^
    --add-data "SDK1.2.0\\*;SDK1.2.0" ^
    --add-data "script.img;." ^
    --add-data "assets\\checkbox_on.png;assets" ^
    --add-data "assets\\checkbox_off.png;assets" ^
    main.py

pause