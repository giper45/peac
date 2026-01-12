@echo off
echo Building PEaC LITE for Windows...
echo.

REM Get version from pyproject.toml
for /f "tokens=3 delims= " %%a in ('findstr /r "^version" pyproject.toml') do (
    set "VERSION=%%a"
)
REM Remove quotes from version
set VERSION=%VERSION:"=%
echo Version: %VERSION%-lite
echo.

echo Installing dependencies (LITE - without RAG/torch)...
poetry install --with dev

echo Checking for UPX...
where upx >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: UPX not found!
    echo Please install UPX using: choco install upx -y (administrative rights)
    echo.
    exit /b 1
)
echo UPX found!

echo.
echo ==========================================
echo Building GUI LITE (onedir - FAST STARTUP)
echo ==========================================
poetry run pyinstaller --clean ^
  --onedir ^
  --windowed ^
  --name "PeacGUI_LITE_v%VERSION%-lite" ^
  --add-data "peac/template.yaml;peac" ^
  --hidden-import=flet.core ^
  --hidden-import=flet.controls ^
  --hidden-import=flet.connection ^
  --collect-all=flet ^
  --hidden-import=yaml ^
  --hidden-import=bs4 ^
  --hidden-import=requests ^
  --hidden-import=pdfplumber ^
  --hidden-import=openpyxl ^
  --hidden-import=docx ^
  --hidden-import=markdown ^
  --strip ^
  --noupx ^
  --exclude-module=torch ^
  --exclude-module=sentence-transformers ^
  --exclude-module=faiss ^
  --exclude-module=numpy ^
  peac/main.py

@REM echo.
@REM echo ==========================================
@REM echo Building CLI LITE (onefile - PORTABLE)
@REM echo ==========================================
@REM poetry run pyinstaller --clean ^
@REM   --onefile ^
@REM   --console ^
@REM   --name "PeacCLI_LITE_v%VERSION%-lite" ^
@REM   --add-data "peac/template.yaml;peac" ^
@REM   --hidden-import=typer.testing ^
@REM   --hidden-import=yaml ^
@REM   --hidden-import=bs4 ^
@REM   --hidden-import=requests ^
@REM   --hidden-import=pdfplumber ^
@REM   --hidden-import=openpyxl ^
@REM   --hidden-import=docx ^
@REM   --hidden-import=markdown ^
@REM   --strip ^
@REM   --noupx ^
@REM   --exclude-module=torch ^
@REM   --exclude-module=sentence-transformers ^
@REM   --exclude-module=faiss ^
@REM   --exclude-module=numpy ^
@REM   peac/main.py

echo.
echo Build completed!
echo.
echo GUI folder: dist\PeacGUI_LITE_v%VERSION%-lite\
echo GUI executable: dist\PeacGUI_LITE_v%VERSION%-lite\PeacGUI_LITE_v%VERSION%-lite.exe
echo CLI executable: dist\PeacCLI_LITE_v%VERSION%-lite.exe
echo.
echo Creating distributable ZIP for GUI...
powershell Compress-Archive -Path "dist\PeacGUI_LITE_v%VERSION%-lite" -DestinationPath "dist\PeacGUI_LITE_v%VERSION%-lite_portable.zip" -Force
echo.
echo GUI portable ZIP: dist\PeacGUI_LITE_v%VERSION%-lite_portable.zip
echo.
echo ==========================================
echo Size comparison:
echo ==========================================
powershell "Get-ChildItem dist\*.exe, dist\*.zip | Select-Object Name, @{Name='Size(MB)';Expression={[math]::Round($_.Length/1MB,2)}}"
echo.
echo Done! 🎉
