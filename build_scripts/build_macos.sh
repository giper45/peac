#!/bin/bash
# Build script for macOS
echo "Building PEaC for macOS..."

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
    --icon="assets/icon.icns" \
    --add-data "peac/template.yaml:peac" \
    --hidden-import "peac.providers.pdf" \
    --hidden-import "peac.providers.docx" \
    --hidden-import "peac.gui_ctk.main_app" \
    --hidden-import "peac.gui_ctk.components.context_section" \
    --hidden-import "peac.gui_ctk.components.output_section" \
    --hidden-import "peac.gui_ctk.components.extends_section" \
    --hidden-import "peac.gui_ctk.components.shared_rule_components" \
    --hidden-import "customtkinter" \
    --hidden-import "PIL" \
    --hidden-import "PIL.Image" \
    --hidden-import "PIL.ImageTk" \
    --exclude-module "matplotlib" \
    --exclude-module "numpy" \
    --exclude-module "scipy" \
    --osx-bundle-identifier "com.giper45.peac" \
    peac/main.py

# Build CLI executable
echo "Creating CLI executable..."
poetry run pyinstaller \
    --onefile \
    --console \
    --name "PEaC-CLI" \
    --icon="assets/icon.icns" \
    --add-data "peac/template.yaml:peac" \
    --hidden-import "peac.providers.pdf" \
    --hidden-import "peac.providers.docx" \
    --exclude-module "customtkinter" \
    --exclude-module "PIL" \
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
