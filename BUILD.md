# PEaC Build System

This document explains the clean build system for PEaC.

## Build Variants

PEaC supports two variants:

1. **LITE** - FastEmbed only (smaller, faster)
   - Document parsers (PDF, DOCX, XLSX, HTML)
   - RAG with fastembed embeddings
   - No FAISS dependency
   - Recommended for most users

2. **FULL** - FAISS + FastEmbed (complete RAG)
   - All LITE features
   - FAISS vector database support
   - Advanced RAG capabilities
   - Larger executable size

## Quick Build Commands (Windows)

```cmd
# GUI builds
make build-gui-lite    # Recommended for most users
make build-gui-full    # With FAISS support

# CLI builds
make build-cli-lite    # Portable CLI executable
make build-cli-full    # CLI with FAISS support
```

## Build Output

Executables are in the `dist/` folder:

- **GUI**: `dist/peac-gui-lite/` or `dist/peac-gui-full/`
- **CLI**: `dist/peac-cli-lite.exe` or `dist/peac-cli-full.exe`

ZIP archives are created automatically for distribution.

## Development Workflow

1. **Install dependencies**
   ```cmd
   make install-lite    # For lite development
   make install-full    # For full development
   ```

2. **Run from source**
   ```cmd
   make gui            # Launch GUI
   poetry run peac gui # Alternative
   ```

3. **Build executable**
   ```cmd
   make build-gui-lite
   ```

## Build Files

All build specifications are in `build_scripts/`:

- `peac-cli-lite.spec` - CLI lite build
- `peac-cli-full.spec` - CLI full build
- `peac-gui-lite.spec` - GUI lite build
- `peac-gui-full.spec` - GUI full build
- `build.bat` - Unified Windows build script

## Clean Build Structure

The build system has been reorganized:

✅ **Removed**: 13 legacy .spec files from root  
✅ **Created**: 4 modular .spec files in build_scripts/  
✅ **Unified**: Single build.bat script with parameters  
✅ **Makefile**: Windows-compatible build targets  

## Dependencies by Variant

### Base (all variants)
- typer, pyyaml, requests, validators, markdown
- flet (GUI framework)
- beautifulsoup4, python-docx, pdfplumber, openpyxl

### LITE extra
- fastembed

### FULL extra
- fastembed
- faiss-cpu
