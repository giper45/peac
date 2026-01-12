# PyInstaller Troubleshooting Guide

## Common Error: "Failed to load Python DLL 'python311.dll'"

### Symptoms
```
[PYI-26060:ERROR] Failed to load Python DLL 'C:\Users\...\AppData\Local\Temp\_MEI...\python311.dll'.
```

---

## 🔧 Quick Fixes (Try in order)

### Fix 1: Run as Administrator ⭐ (Most Common)
**Right-click** the `.exe` → **Run as administrator**

**Why**: Windows security might block DLL extraction to Temp folder.

---

### Fix 2: Add Antivirus Exclusion
Windows Defender or other antivirus software might block the DLL.

#### Windows Defender:
1. Open **Windows Security** → **Virus & threat protection**
2. Click **Manage settings** → **Add or remove exclusions**
3. Add exclusion for:
   - The `.exe` file
   - `C:\Users\<YourUser>\AppData\Local\Temp`

#### Other Antivirus:
Check your antivirus quarantine/blocked files list.

---

### Fix 3: Extract to Different Location
Sometimes the Temp folder has permission issues:

1. Extract the portable ZIP to a simple path like `C:\PEaC\`
2. Avoid paths with:
   - Spaces
   - Special characters
   - Long paths
   - Network drives

---

### Fix 4: Install Visual C++ Redistributables
PyInstaller requires Microsoft Visual C++ runtime:

**Download and install**:
- [VC++ 2015-2022 Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

### Fix 5: Check Temp Folder Permissions
Ensure your user has write access to:
```
C:\Users\<YourUser>\AppData\Local\Temp
```

**Fix permissions**:
1. Right-click Temp folder → **Properties**
2. **Security** tab → **Edit**
3. Give your user **Full Control**

---

### Fix 6: Use `onedir` Build Instead of `onefile`
The `onedir` build extracts DLLs only once and is more reliable.

**Instead of**: `PeacCLI_LITE_v0.2.5-lite.exe` (onefile)  
**Use**: `PeacGUI_LITE_v0.2.5-lite_portable.zip` (onedir)

1. Extract the ZIP
2. Run the `.exe` from the extracted folder
3. Much faster startup + no temp extraction issues

---

## 🔨 Rebuild Options (If none of the above work)

### Option A: Rebuild without UPX Compression
UPX compression can cause issues on some systems.

**Use the new build script**:
```cmd
cd C:\Users\gper4\Git\peac
build_scripts\build_windows_lite.bat
```

This script uses `--noupx` flag which avoids compression issues.

---

### Option B: Use `--debug=all` for More Info
Rebuild with debug mode to see detailed error:

```cmd
poetry run pyinstaller --debug=all --onefile --name "PeacCLI_DEBUG" peac/main.py
```

Run the debug executable to get more error details.

---

### Option C: Test with Different Python Version
If using Python 3.13 (new), try Python 3.11 (more stable with PyInstaller):

```cmd
poetry env use 3.11
poetry install --with dev
build_scripts\build_windows_lite.bat
```

---

## 🐛 Advanced Debugging

### Check if DLL is in the package
For `onefile` builds, extract manually:

```cmd
# Extract the exe contents
.\PeacCLI_LITE_v0.2.5-lite.exe --extract-dir C:\temp\extracted
```

Check if `python311.dll` exists in the extracted folder.

---

### Check PyInstaller Logs
Look for warnings during build:

```cmd
poetry run pyinstaller --log-level DEBUG peac/main.py
```

Check for missing dependencies or module errors.

---

### Try with Latest PyInstaller
The project uses PyInstaller from git (for Python 3.13+ support).

Try stable version:
```cmd
poetry remove pyinstaller
poetry add pyinstaller@^6.0.0 --group dev
```

Then rebuild.

---

## 📊 Build Comparison

| Build Type | Size | Startup | DLL Issues | Recommended |
|------------|------|---------|------------|-------------|
| **onedir** (GUI) | ~250MB folder | 3-5s | ✅ Rare | ⭐ Best |
| **onefile** (CLI) | ~120MB file | 5-10s | ⚠️ Common | Use with caution |
| **onefile + UPX** | ~60MB file | 10-15s | ❌ Frequent | Avoid on Windows |

**Recommendation**: Always prefer `onedir` builds for Windows distribution.

---

## 🎯 Prevention for Future Builds

### Best Practices:
1. ✅ Use `--noupx` (no compression)
2. ✅ Use `--onedir` for GUI apps
3. ✅ Add `--strip` to remove debug symbols (size reduction)
4. ✅ Test on clean Windows VM
5. ✅ Explicitly exclude unused modules:
   ```cmd
   --exclude-module=torch
   --exclude-module=numpy
   --exclude-module=pandas
   ```

### LITE Build Checklist:
- [ ] No torch/transformers/faiss in dependencies
- [ ] `--noupx` flag set
- [ ] All parsing libraries included (bs4, pdfplumber, docx)
- [ ] Template.yaml included in data files
- [ ] Test on Windows without Python installed

---

## 🆘 Still Not Working?

1. Check GitHub Issues: [github.com/pyinstaller/pyinstaller/issues](https://github.com/pyinstaller/pyinstaller/issues)
2. Run with `--debug=all` and share the output
3. Try the `onedir` build instead
4. Rebuild with the new `build_windows_lite.bat` script

---

## Quick Command Reference

```cmd
# Rebuild LITE version locally
build_scripts\build_windows_lite.bat

# Test build
dist\PeacCLI_LITE_v0.2.4-lite.exe --help

# Check dependencies
poetry show

# Clean build artifacts
rmdir /s /q build dist
del /q *.spec
```
