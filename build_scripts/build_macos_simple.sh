#!/bin/bash
# Build script for macOS
echo "Building PEaC for macOS..."

# Clean previous builds
rm -rf dist build

# Install PyInstaller
echo "Installing PyInstaller..."
pip install pyinstaller

# Build GUI executable as macOS app bundle
echo "Creating GUI app bundle..."
pyinstaller \
    --onefile \
    --windowed \
    --name "PEaC-GUI" \
    --add-data "peac/template.yaml:peac" \
    --osx-bundle-identifier "com.example.peac" \
    --hidden-import "peac.providers.pdf" \
    --hidden-import "peac.providers.docx" \
    --hidden-import "peac.gui.main_app" \
    --hidden-import "peac.gui.ui.app" \
    --hidden-import "peac.gui.ui.components" \
    --hidden-import "peac.gui.ui.rule_card" \
    --hidden-import "flet" \
    --hidden-import "flet.core" \
    --hidden-import "bs4" \
    --hidden-import "requests" \
    --hidden-import "pdfplumber" \
    --exclude-module "matplotlib" \
    --exclude-module "numpy" \
    --exclude-module "scipy" \
    peac/main.py

# Create CLI version
echo "Creating CLI executable..."
pyinstaller \
    --onefile \
    --console \
    --name "PEaC-CLI" \
    --add-data "peac/template.yaml:peac" \
    --hidden-import "peac.providers.pdf" \
    --hidden-import "peac.providers.docx" \
    --exclude-module "flet" \
    --exclude-module "matplotlib" \
    --exclude-module "numpy" \
    --exclude-module "scipy" \
    peac/main.py

# Make executables executable
chmod +x dist/PEaC-CLI

echo ""
echo "Build completed!"
echo "GUI app bundle: dist/PEaC-GUI.app"
echo "CLI executable: dist/PEaC-CLI"
echo ""
echo "You can now test the executables:"
echo "  open dist/PEaC-GUI.app"
echo "  ./dist/PEaC-CLI --help"
echo ""
