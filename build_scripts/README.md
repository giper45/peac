# PEaC Build Scripts

This directory contains scripts to build PEaC executables for different platforms.

## Requirements

- Python 3.11+
- Poetry
- PyInstaller (installed automatically with `poetry install --with dev`)

## Quick Start

### Windows
```cmd
build_scripts\build_windows.bat
```

### macOS
```bash
chmod +x build_scripts/build_macos.sh
./build_scripts/build_macos.sh
```

### Linux
```bash
chmod +x build_scripts/build_linux.sh
./build_scripts/build_linux.sh
```

### Universal (Auto-detect OS)
```bash
chmod +x build_scripts/build.sh
./build_scripts/build.sh
```

## Output

Each build script creates two executables in the `dist/` directory:

- **PEaC** (or **PEaC.exe** on Windows) - GUI version
- **PEaC-CLI** (or **PEaC-CLI.exe** on Windows) - Command-line version

## Icons

Place your application icons in the `assets/` directory:
- `icon.ico` - Windows icon
- `icon.icns` - macOS icon
- `icon.png` - Linux icon (optional)

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
