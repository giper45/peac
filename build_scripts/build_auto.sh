#!/bin/bash
# Universal build script that detects OS and runs appropriate build
echo "PEaC Build Script - Auto-detecting OS..."

# Detect operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected: Linux"
    chmod +x build_scripts/build_linux_simple.sh
    ./build_scripts/build_linux_simple.sh
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected: macOS"
    chmod +x build_scripts/build_macos_simple.sh
    ./build_scripts/build_macos_simple.sh
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Detected: Windows"
    cmd.exe /c build_scripts\\build_windows.bat
else
    echo "Unknown OS: $OSTYPE"
    echo "Please run the appropriate build script manually:"
    echo "  Windows: build_scripts\\build_windows.bat"
    echo "  macOS:   build_scripts/build_macos_simple.sh"  
    echo "  Linux:   build_scripts/build_linux_simple.sh"
    exit 1
fi
