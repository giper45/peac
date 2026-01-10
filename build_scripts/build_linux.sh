#!/bin/bash
# Build script for Linux
echo "Building PEaC for Linux..."

# Clean previous builds
rm -rf dist build

# Install dependencies
echo "Installing dependencies..."
poetry install --with dev

# Build GUI executable
echo "Creating GUI executable..."
poetry run pyinstaller \
    --onefile \
    --windowed \
    --name "PEaC" \
    --add-data "peac/template.yaml:peac" \
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

# Build CLI executable
echo "Creating CLI executable..."
poetry run pyinstaller \
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

echo ""
echo "Build completed!"
echo "GUI executable: dist/PEaC"
echo "CLI executable: dist/PEaC-CLI"
echo ""

# Make executables executable
chmod +x dist/PEaC
chmod +x dist/PEaC-CLI
echo "Executables are ready to use!"
