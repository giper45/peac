@echo off
REM PEaC Build Script for Windows
REM Usage: build.bat [cli|gui] [lite|full] [fast]
REM Example: build.bat gui lite fast

setlocal enabledelayedexpansion

REM Get version from pyproject.toml in parent directory
for /f "tokens=3 delims= " %%a in ('findstr /r "^version" ..\pyproject.toml') do (
    set "VERSION=%%a"
)
set VERSION=%VERSION:"=%
echo PEaC Build Script v%VERSION%
echo ========================================

REM Parse arguments
set TYPE=%1
set VARIANT=%2
set FAST=%3

REM Validate arguments
if "%TYPE%"=="" (
    echo Error: Missing TYPE argument
    echo Usage: build.bat [cli^|gui] [lite^|full]
    echo.
    echo Examples:
    echo   build.bat cli lite   - Build CLI with fastembed only
    echo   build.bat cli full   - Build CLI with FAISS + fastembed
    echo   build.bat gui lite   - Build GUI with fastembed only
    echo   build.bat gui full   - Build GUI with FAISS + fastembed
    exit /b 1
)

if "%VARIANT%"=="" (
    echo Error: Missing VARIANT argument
    echo Usage: build.bat [cli^|gui] [lite^|full]
    exit /b 1
)

if not "%TYPE%"=="cli" if not "%TYPE%"=="gui" (
    echo Error: TYPE must be 'cli' or 'gui'
    exit /b 1
)

if not "%VARIANT%"=="lite" if not "%VARIANT%"=="full" (
    echo Error: VARIANT must be 'lite' or 'full'
    exit /b 1
)

REM Set spec file path (relative from parent directory)
set SPEC_FILE=build_scripts\peac-%TYPE%-%VARIANT%.spec

echo.
echo Configuration:
echo   Type: %TYPE%
echo   Variant: %VARIANT%
echo   Spec: %SPEC_FILE%
echo   Version: %VERSION%
if "%FAST%"=="fast" (
    echo   Mode: FAST BUILD ^(no compression, no cache cleanup^)
) else (
    echo   Mode: STANDARD BUILD
)
echo.

REM Install dependencies
echo Step 1/3: Installing dependencies...
cd ..
echo Installing base dependencies with dev tools
poetry install --with dev

if errorlevel 1 (
    echo Error: Failed to install dependencies
    cd build_scripts
    exit /b 1
)

REM Add FAISS if building full variant
if "%VARIANT%"=="full" (
    echo Installing FAISS for full build...
    poetry install -E faiss-cpu
    if errorlevel 1 (
        echo Warning: FAISS installation failed, continuing without it
    )
)

REM Check if UPX is available
echo.
echo Step 2/3: Checking UPX...
if "%FAST%"=="fast" (
    echo FAST mode: UPX disabled for speed
) else (
    where upx >nul 2>nul
    if errorlevel 1 (
        echo UPX not found. Install with: choco install upx
        echo Continuing without UPX ^(larger executables^)
    ) else (
        echo UPX found
    )
)

REM Build with PyInstaller
echo.
echo Step 3/3: Building with PyInstaller...
REM Always copy spec file to root so relative paths work correctly
copy %SPEC_FILE% peac-build-temp.spec >nul

if "%FAST%"=="fast" (
    REM Fast build: skip cleanup, reuse cache
    poetry run pyinstaller peac-build-temp.spec
) else (
    REM Standard build: clean and full rebuild
    poetry run pyinstaller --clean peac-build-temp.spec
)

del peac-build-temp.spec

if errorlevel 1 (
    echo.
    echo Error: Build failed
    cd build_scripts
    exit /b 1
)

REM Success message
echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.

if "%TYPE%"=="cli" (
    echo CLI executable: dist\peac-%TYPE%-%VARIANT%.exe
    echo.
    echo Test with: dist\peac-%TYPE%-%VARIANT%.exe --help
) else (
    echo GUI folder: dist\peac-%TYPE%-%VARIANT%\
    echo GUI executable: dist\peac-%TYPE%-%VARIANT%\peac-%TYPE%-%VARIANT%.exe
    echo.
    echo Creating portable ZIP...
    powershell -Command "Compress-Archive -Path 'dist\peac-%TYPE%-%VARIANT%' -DestinationPath 'dist\peac-%TYPE%-%VARIANT%-v%VERSION%.zip' -Force"
    echo Portable ZIP: dist\peac-%TYPE%-%VARIANT%-v%VERSION%.zip
)

echo Build type: %VARIANT%
if "%VARIANT%"=="lite" (
    echo Features: RAG with fastembed only ^(no FAISS, smaller executable^)
) else (
    echo Features: Full RAG with FAISS + fastembed ^(advanced vector database^)
)

cd build_scripts
endlocal
