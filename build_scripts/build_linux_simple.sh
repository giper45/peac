#!/bin/bash
# Build script for Linux
echo "Building PEaC for Linux..."

# Clean previous builds
rm -rf dist build

# Install PyInstaller
echo "Installing PyInstaller..."
pip install pyinstaller

# Build GUI executable
echo "Creating GUI executable..."
pyinstaller \
    --onefile \
    --windowed \
    --name "PEaC-GUI" \
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
    --exclude-module "customtkinter" \
    --exclude-module "PIL" \
    --exclude-module "matplotlib" \
    --exclude-module "numpy" \
    --exclude-module "scipy" \
    peac/main.py

# Make executables executable
chmod +x dist/PEaC-GUI
chmod +x dist/PEaC-CLI

echo ""
echo "Build completed!"
echo "GUI executable: dist/PEaC-GUI"
echo "CLI executable: dist/PEaC-CLI"
echo ""
echo "You can now test the executables:"
echo "  ./dist/PEaC-GUI"
echo "  ./dist/PEaC-CLI --help"
echo ""
