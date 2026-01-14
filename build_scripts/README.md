# PEaC Build Scripts (Windows Only)

Build PEaC executables for Windows using PyInstaller. Pre-compiled binaries are recommended for end-users.

## Build Variants

Two build variants are available:

- **LITE**: Includes fastembed for RAG embeddings (no FAISS)
  - Smaller executable, faster startup
  - Recommended for most use cases
  
- **FULL**: Includes FAISS + fastembed for advanced RAG
  - Complete vector database support
  - Larger executable, more memory intensive

Both variants support CLI and GUI builds.

## Requirements

- Windows 10/11
- Python 3.11+ (for building)
- Poetry
- PyInstaller (installed automatically)
- UPX (optional, for compression) - Install with: `choco install upx`

## Building

### Using Makefile (recommended)

```cmd
# Build GUI executables
make build-gui-lite      # GUI lite version
make build-gui-full      # GUI full version

# Build CLI executables  
make build-cli-lite      # CLI lite version
make build-cli-full      # CLI full version
```

### Using build.bat directly

```cmd
cd build_scripts
build.bat gui lite       # GUI lite
build.bat gui full       # GUI full
build.bat cli lite       # CLI lite
build.bat cli full       # CLI full
```

## Output

All builds are placed in the `dist/` folder:

- **CLI**: Single executable file
  - `dist/peac-cli-lite.exe`
  - `dist/peac-cli-full.exe`
  
- **GUI**: Folder with executable and all dependencies
  - `dist/peac-gui-lite/peac-gui-lite.exe`
  - `dist/peac-gui-full/peac-gui-full.exe`
  - Portable ZIP files are created automatically

## Build Specifications

- `peac-cli-lite.spec` - CLI build without FAISS
- `peac-cli-full.spec` - CLI build with FAISS
- `peac-gui-lite.spec` - GUI build without FAISS
- `peac-gui-full.spec` - GUI build with FAISS
- `build.bat` - Unified Windows build script

## Notes

- macOS/Linux users: Use `poetry install` for development/usage instead of building executables
- Executables are built with UPX compression for smaller size
- Build time: 2-5 minutes depending on variant and system specifications

## Output

Each build script creates two executables in the `dist/` directory:

- **PEaC** (or **PEaC.exe** on Windows) - Flet-based GUI version
- **PEaC-CLI** (or **PEaC-CLI.exe** on Windows) - Command-line version

## GUI Framework

The new GUI uses **Flet** for cross-platform support:
- Single codebase for Windows, macOS, Linux, iOS, Android
- Modern Material Design 3 interface
- Fast performance (Flutter-based)
- No dependency on native toolkits

## Advanced Building

For more control, you can use the PyInstaller spec file:

```bash
poetry run pyinstaller build_scripts/peac.spec --gui  # For GUI version
poetry run pyinstaller build_scripts/peac.spec        # For CLI version
```

## Troubleshooting

### Missing Dependencies
If the executable fails to run due to missing modules, add them to the `hiddenimports` list in the build scripts.

### Large File Size
To reduce executable size:
- Remove unused dependencies from `pyproject.toml`
- Add more modules to the `excludes` list
- Use `--onedir` instead of `--onefile` (creates a directory with dependencies)

### Platform-Specific Issues

#### Windows
- Install Visual C++ Redistributable if users get DLL errors
- Use `--console` for debugging version

#### macOS
- Code signing required for distribution
- Use `--osx-bundle-identifier` for proper app bundle

#### Linux
- Test on different distributions
- Consider AppImage format for better compatibility

## Distribution

### Windows
- Distribute the `.exe` file
- Optional: Create installer with NSIS or Inno Setup

### macOS
- Code sign the `.app` bundle
- Create `.dmg` disk image for distribution
- Notarize for Gatekeeper compatibility

### Linux
- Create `.deb` or `.rpm` packages
- Consider AppImage or Flatpak for universal distribution

## GitHub Actions

For automated builds across platforms, see `.github/workflows/build.yml` (if available).
