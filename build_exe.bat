@echo off

echo Installing PyInstaller if not already installed...
pip install pyinstaller

echo.
echo Building executable...
pyinstaller --name="MapGenerator" --onefile --windowed --add-data="src/generation/object_gen/templates;templates" --add-data="src/ui/nasza_mapka.png;ui" --add-binary="h3mtxt.exe;." --hidden-import=PySide6.QtCore --hidden-import=PySide6.QtGui --hidden-import=PySide6.QtWidgets src/gui.py

echo.
echo Build complete! Executable is in the 'dist' folder.
echo You can find MapGenerator.exe in: %CD%\dist\
pause
