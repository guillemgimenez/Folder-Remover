@echo off
REM Genera dist\Limpiador.exe (no requiere Python en el equipo de destino)
py -m pip install -r requirements.txt pyinstaller
py -m PyInstaller --noconsole --onefile --collect-all customtkinter --name Limpiador limpiador.py
echo.
echo Listo: dist\Limpiador.exe
pause
