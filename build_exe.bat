@echo off
echo Building Logimat WEC JSON Generator...

REM Activate venv if needed
REM call venv\Scripts\activate

pyinstaller --noconfirm ^
 --onefile ^
 --windowed ^
 --exclude-module cx_Oracle ^
 --exclude-module oracledb ^
 main.py

echo Build complete.
pause