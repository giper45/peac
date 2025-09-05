#!/bin/bash
# Universal build script
# Detects OS and runs appropriate build script

echo "PEaC Build Script"
echo "================="

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected: Linux"
    ./build_scripts/build_linux.sh
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected: macOS"
    ./build_scripts/build_macos.sh
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Detected: Windows"
    ./build_scripts/build_windows.bat
else
    echo "Unknown OS: $OSTYPE"
    echo "Please run the appropriate build script manually:"
    echo "  Windows: build_scripts/build_windows.bat"
    echo "  macOS:   build_scripts/build_macos.sh"
    echo "  Linux:   build_scripts/build_linux.sh"
    exit 1
fi
