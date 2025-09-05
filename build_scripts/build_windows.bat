@echo off
echo Building PEaC for Windows...

REM Get version from pyproject.toml
for /f "tokens=3 delims= " %%a in ('findstr /r "^version" pyproject.toml') do (
    set "VERSION=%%a"
)
REM Remove quotes from version
set VERSION=%VERSION:"=%
echo Version: %VERSION%

echo Installing PyInstaller development version...
poetry install --with dev

echo Creating GUI executable...
poetry run pyinstaller --onefile --windowed --name "PeacGUI_v%VERSION%" --add-data "peac/template.yaml;peac" --hidden-import=customtkinter --collect-all=customtkinter --collect-all=yaml --collect-all=bs4 --collect-all=requests --collect-all=pdfplumber peac/gui_launcher.py

echo Creating CLI executable...
poetry run pyinstaller --onefile --name "PeacCLI_v%VERSION%" --add-data "peac/template.yaml;peac" --hidden-import=typer.testing --collect-all=yaml --collect-all=bs4 --collect-all=requests --collect-all=pdfplumber peac/main.py

echo.
echo Build completed!
echo GUI executable: dist/PeacGUI_v%VERSION%.exe
echo CLI executable: dist/PeacCLI_v%VERSION%.exe
echo.
echo You can now test the executables:
echo   dist\PeacGUI_v%VERSION%.exe
echo   dist\PeacCLI_v%VERSION%.exe --help
echo.
pause
