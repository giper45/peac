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

echo Installing UPX for compression (if not present)...
where upx >nul 2>nul || choco install upx -y

echo Creating GUI executable (onedir - FAST STARTUP)...
poetry run pyinstaller --clean --onedir --windowed --name "PeacGUI_v%VERSION%" --add-data "peac/template.yaml;peac" --hidden-import=flet.core --hidden-import=flet.controls --hidden-import=flet.connection --collect-all=flet --hidden-import=yaml --hidden-import=bs4 --hidden-import=requests --hidden-import=pdfplumber peac/main.py

echo Creating GUI debug executable (console + verbose logs)...
poetry run pyinstaller --clean --onedir --console --log-level DEBUG --name "PeacGUI_v%VERSION%_debug" --add-data "peac/template.yaml;peac" --hidden-import=flet.core --hidden-import=flet.controls --collect-all=flet --hidden-import=yaml peac/main.py

echo Creating CLI executable (onefile for portability)...
poetry run pyinstaller --clean --onefile --name "PeacCLI_v%VERSION%" --add-data "peac/template.yaml;peac" --hidden-import=typer.testing --hidden-import=yaml --hidden-import=bs4 --hidden-import=requests --hidden-import=pdfplumber --upx-dir="C:\ProgramData\chocolatey\lib\upx\tools" peac/main.py

echo.
echo Build completed!
echo GUI folder: dist\PeacGUI_v%VERSION%\
echo GUI executable: dist\PeacGUI_v%VERSION%\PeacGUI_v%VERSION%.exe
echo CLI executable: dist\PeacCLI_v%VERSION%.exe
echo.
echo Creating distributable ZIP for GUI...
powershell Compress-Archive -Path "dist\PeacGUI_v%VERSION%" -DestinationPath "dist\PeacGUI_v%VERSION%_portable.zip" -Force
echo GUI portable ZIP: dist\PeacGUI_v%VERSION%_portable.zip
