# Icons Directory

Place your application icons here:

- `icon.ico` - Windows icon (32x32 or larger, .ico format)
- `icon.icns` - macOS icon (.icns format with multiple sizes)
- `icon.png` - Linux/universal icon (256x256 recommended)

## Creating Icons

### From PNG to ICO (Windows)
You can use online converters or tools like ImageMagick:
```bash
magick icon.png -define icon:auto-resize=16,24,32,48,64,128,256 icon.ico
```

### From PNG to ICNS (macOS)
Use the iconutil command on macOS:
```bash
# Create iconset directory
mkdir icon.iconset
# Add different sizes (16x16, 32x32, 128x128, 256x256, 512x512, 1024x1024)
# Then convert:
iconutil -c icns icon.iconset
```

### Recommended Sizes
- 16x16, 32x32, 48x48, 64x64, 128x128, 256x256, 512x512, 1024x1024
