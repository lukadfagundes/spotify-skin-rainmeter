# .RMSKIN Package Build Guide

## Overview

This document provides instructions for creating a distributable `.rmskin` package for the Spotify Now Playing Rainmeter skin.

`.rmskin` files are Rainmeter's native distribution format - essentially ZIP archives with metadata that Rainmeter can automatically install.

---

## Prerequisites

### Required Software
- **Rainmeter 4.5+** installed with Skin Packager
- **Python 3.7+** (for building SpotifySetup.exe)
- **PyInstaller** (for compiling Python script to executable)

### Required Files
All files in `SpotifyNowPlaying/` directory:
- [x] `SpotifyNowPlaying.ini` - Main skin file
- [x] `SpotifySetup.py` - OAuth setup script (source)
- [x] `SpotifySetup.exe` - Compiled OAuth utility (built)
- [x] `@Resources/Variables.inc` - Configuration variables
- [x] `@Resources/SpotifyCredentials.inc.template` - Template for @Vault
- [x] `@Resources/Images/` - Button images (PNG or SVG)
- [x] `@Resources/Scripts/TokenManager.lua`
- [x] `@Resources/Scripts/Base64Encoder.lua`
- [x] `@Resources/Cache/.gitkeep` - Placeholder (cache directory)

### Excluded from Package
- [x] `@Vault/` folder (contains user credentials - **NEVER INCLUDE**)
- [x] `@Resources/Cache/*.jpg` (downloaded album art - user-specific)
- [x] Python build artifacts (`__pycache__/`, `build/`, `dist/`)
- [x] `.git/` directory
- [x] IDE config files (`.vscode/`, `.idea/`)

---

## Build Process

### Step 1: Build SpotifySetup.exe

Before packaging, compile the Python script into a standalone executable:

```bash
cd spotify-skin-rainmeter

# Install dependencies
pip install requests pyinstaller

# Build executable
pyinstaller --onefile --windowed --name SpotifySetup --icon=icon.ico SpotifySetup.py
```

**Output**: `dist/SpotifySetup.exe`

**Copy to skin folder**:
```bash
cp dist/SpotifySetup.exe SpotifyNowPlaying/SpotifySetup.exe
```

**File Size Check**:
- Expected size: ~8-12 MB (includes Python runtime)
- If larger: Review PyInstaller options, consider excluding unnecessary libraries

---

### Step 2: Prepare Image Assets

The package currently includes SVG placeholders. For production:

**Option A: Convert SVG to PNG**
```bash
# Using ImageMagick (requires installation)
cd SpotifyNowPlaying/@Resources/Images/
magick convert play.svg -resize 32x32 play.png
magick convert pause.svg -resize 32x32 pause.png
magick convert next.svg -resize 32x32 next.png
magick convert previous.svg -resize 32x32 previous.png
magick convert default-album.svg -resize 200x200 default-album.png
```

**Option B: Use Pre-made PNG Images**
- Download/create 32x32 PNG icons manually
- Place in `@Resources/Images/` directory
- Ensure transparency and proper naming

**Required Files**:
- [x] `play.png` (32x32)
- [x] `pause.png` (32x32)
- [x] `next.png` (32x32)
- [x] `previous.png` (32x32)
- [x] `default-album.png` (200x200)

---

### Step 3: Create RMSKIN.ini Metadata

Create `SpotifyNowPlaying/RMSKIN.ini` with package metadata:

```ini
[rmskin]
Name=Spotify Now Playing
Author=Your Name
Version=1.0.0
LoadType=Skin
Load=SpotifyNowPlaying\SpotifyNowPlaying.ini

[Metadata]
Name=Spotify Now Playing
Author=Your Name
Information=Displays currently playing Spotify track with playback controls. Requires Spotify account and OAuth setup.
Version=1.0.0
Tags=Spotify, Music, Now Playing, OAuth, Playback
License=MIT

[Variables]
; Default variables can be set here
; Users can override in Variables.inc

[Components]
Component1=SpotifyNowPlaying.ini
Component2=SpotifySetup.exe
Component3=@Resources

[Requirements]
Rainmeter=4.5

[Install]
Enabled=1
```

**Field Descriptions**:
- `Name`: Display name in Rainmeter installer
- `Author`: Your name or organization
- `Version`: Semantic versioning (Major.Minor.Patch)
- `LoadType=Skin`: Automatically load skin after install
- `Load`: Path to main skin file
- `Requirements`: Minimum Rainmeter version

---

### Step 4: Verify File Structure

Before packaging, ensure correct structure:

```
SpotifyNowPlaying/
├── SpotifyNowPlaying.ini
├── SpotifySetup.exe
├── RMSKIN.ini
├── README.md (optional, recommended)
│
└── @Resources/
    ├── Variables.inc
    ├── SpotifyCredentials.inc.template
    │
    ├── Images/
    │   ├── play.png
    │   ├── pause.png
    │   ├── next.png
    │   ├── previous.png
    │   └── default-album.png
    │
    ├── Scripts/
    │   ├── TokenManager.lua
    │   └── Base64Encoder.lua
    │
    └── Cache/
        └── .gitkeep
```

**Verification Commands**:
```bash
cd SpotifyNowPlaying
ls -la
ls -la @Resources/
ls -la @Resources/Images/
ls -la @Resources/Scripts/
```

**Expected Total Size**: ~10-15 MB (mostly SpotifySetup.exe)

---

### Step 5: Package with Rainmeter Skin Packager

**Method A: GUI Packager (Recommended)**

1. Open Rainmeter
2. Right-click system tray icon → **Manage**
3. Navigate to **SpotifyNowPlaying** in left panel
4. Click **More** → **Create .rmskin package**
5. Rainmeter Skin Packager opens

**Configuration**:
- **Name**: Spotify Now Playing
- **Author**: Your Name
- **Version**: 1.0.0
- **Load on install**: ✅ Checked
- **Skin to load**: `SpotifyNowPlaying\SpotifyNowPlaying.ini`

**Advanced Options**:
- **Minimum Rainmeter version**: 4.5.0.0
- **Header image**: (optional, 400x60 banner)
- **Readme**: Link to README.md or external documentation

6. Click **Create package**
7. Save as: `SpotifyNowPlaying_v1.0.0.rmskin`

---

**Method B: Manual Packaging (Advanced)**

1. Create ZIP archive:
```bash
cd SpotifyNowPlaying
7z a -tzip ../SpotifyNowPlaying.zip *
```

2. Rename `.zip` to `.rmskin`:
```bash
mv ../SpotifyNowPlaying.zip ../SpotifyNowPlaying_v1.0.0.rmskin
```

3. Verify archive contents:
```bash
7z l ../SpotifyNowPlaying_v1.0.0.rmskin
```

**Expected Contents**:
```
SpotifyNowPlaying.ini
SpotifySetup.exe
RMSKIN.ini
@Resources/Variables.inc
@Resources/SpotifyCredentials.inc.template
@Resources/Images/play.png
@Resources/Images/pause.png
@Resources/Images/next.png
@Resources/Images/previous.png
@Resources/Images/default-album.png
@Resources/Scripts/TokenManager.lua
@Resources/Scripts/Base64Encoder.lua
@Resources/Cache/.gitkeep
```

**CRITICAL: Verify @Vault is NOT included**:
```bash
7z l ../SpotifyNowPlaying_v1.0.0.rmskin | grep -i vault
# Should return NOTHING - no vault files!
```

---

### Step 6: Test Installation

**Fresh Install Test**:

1. **Uninstall existing version** (if present):
   - Rainmeter → Manage → SpotifyNowPlaying → More → Delete folder
   - Delete `@Vault\SpotifyCredentials.inc` (to simulate new user)

2. **Install .rmskin package**:
   - Double-click `SpotifyNowPlaying_v1.0.0.rmskin`
   - Rainmeter Skin Installer opens
   - Review installation details
   - Click **Install**

3. **Verify installation**:
   - Skin should auto-load (if `LoadType=Skin` in RMSKIN.ini)
   - Check file structure:
     ```
     Documents\Rainmeter\Skins\SpotifyNowPlaying\
     ```
   - Run `SpotifySetup.exe` from installed location
   - Complete OAuth flow
   - Verify skin displays track info

4. **Test all features**:
   - [x] Track info displays correctly
   - [x] Album art downloads and caches
   - [x] Playback controls work (Premium users)
   - [x] Progress bar updates smoothly
   - [x] Token refresh occurs automatically
   - [x] Error states display gracefully

---

### Step 7: Distribution

**Publish .rmskin file**:

**Option A: GitHub Release**
1. Create new release: https://github.com/yourusername/spotify-skin-rainmeter/releases/new
2. Tag version: `v1.0.0`
3. Upload `SpotifyNowPlaying_v1.0.0.rmskin`
4. Add release notes (see CHANGELOG.md)
5. Publish release

**Option B: Rainmeter DeviantArt**
1. Create DeviantArt account (if needed)
2. Join Rainmeter group: https://www.deviantart.com/rainmeter
3. Submit skin with description, screenshots, and .rmskin file

**Option C: Reddit r/Rainmeter**
1. Create showcase post with screenshots
2. Provide download link (GitHub, Google Drive, etc.)
3. Include setup instructions and requirements

---

## Post-Release Checklist

After publishing:

- [ ] Test download link (verify file integrity)
- [ ] Monitor issue reports (GitHub Issues)
- [ ] Respond to user questions
- [ ] Collect feedback for future versions
- [ ] Update README with download link

---

## Version Updates

When releasing updates (e.g., v1.1.0):

1. **Update version numbers**:
   - `SpotifyNowPlaying.ini` → `[Metadata] Version=1.1.0`
   - `RMSKIN.ini` → `Version=1.1.0`
   - `README.md` → Update version badge and changelog

2. **Document changes**:
   - Update `CHANGELOG.md` with new features, bug fixes, breaking changes
   - Tag release in git: `git tag -a v1.1.0 -m "Version 1.1.0"`

3. **Rebuild package**:
   - Repeat Steps 1-6 above
   - Save as: `SpotifyNowPlaying_v1.1.0.rmskin`

4. **Test upgrade path**:
   - Install v1.0.0
   - Configure OAuth credentials
   - Upgrade to v1.1.0 (should preserve @Vault credentials)
   - Verify backward compatibility

---

## Troubleshooting

### "Package failed to install"

**Causes**:
- Corrupt .rmskin file
- Incompatible Rainmeter version
- Missing required files in package

**Solutions**:
1. Re-download package (may be corrupted)
2. Verify Rainmeter version: `Rainmeter → About`
3. Extract .rmskin (rename to .zip) and check contents

---

### "@Vault credentials not found after install"

**Expected Behavior**: Users must run `SpotifySetup.exe` after installation.

**Clarify in README**:
> "After installing the .rmskin, you MUST run SpotifySetup.exe to configure OAuth credentials. The skin will not work without this step."

---

### "SpotifySetup.exe flagged as malware"

**Cause**: PyInstaller executables sometimes trigger false positives.

**Solutions**:
1. **Code signing**: Sign executable with certificate (costs money)
2. **Submit to VirusTotal**: Share VirusTotal report showing safe
3. **Provide source**: Include `SpotifySetup.py` for users to build themselves
4. **Documentation**: Add security FAQ to README

---

### "Images not displaying after install"

**Cause**: PNG files missing or incorrect paths

**Solutions**:
1. Verify PNG files in `@Resources/Images/`
2. Check file names match exactly (case-sensitive)
3. Test on fresh Rainmeter install

---

## Security Best Practices

### Before Packaging

- [x] Remove all OAuth credentials from package
- [x] Verify `.gitignore` excludes `@Vault/` and `**/SpotifyCredentials.inc`
- [x] Review all INI files for hardcoded secrets
- [x] Test with dummy credentials (should fail gracefully)

### During Distribution

- [x] Use HTTPS for download links
- [x] Provide SHA256 checksum for .rmskin file
- [x] Document security model in README
- [x] Warn users about credential storage (@Vault)

### Post-Release

- [x] Monitor for unauthorized forks with embedded credentials
- [x] Respond quickly to security reports
- [x] Keep dependencies updated (Python libraries in SpotifySetup.exe)

---

## Automated Build Script (Optional)

Create `build.sh` (Bash) or `build.ps1` (PowerShell) to automate packaging:

**build.sh**:
```bash
#!/bin/bash
set -e

VERSION="1.0.0"
SKIN_NAME="SpotifyNowPlaying"

echo "Building $SKIN_NAME v$VERSION..."

# Step 1: Build executable
echo "Compiling SpotifySetup.exe..."
pip install -q requests pyinstaller
pyinstaller --onefile --windowed --name SpotifySetup --clean SpotifySetup.py
cp dist/SpotifySetup.exe $SKIN_NAME/

# Step 2: Convert SVG to PNG (requires ImageMagick)
echo "Converting images..."
cd $SKIN_NAME/@Resources/Images/
for svg in *.svg; do
    png="${svg%.svg}.png"
    magick convert "$svg" -resize 32x32 "$png" 2>/dev/null || echo "Skipping $svg"
done
cd ../../../

# Step 3: Create package
echo "Creating .rmskin package..."
cd $SKIN_NAME
7z a -tzip ../${SKIN_NAME}_v${VERSION}.zip * >/dev/null
mv ../${SKIN_NAME}_v${VERSION}.zip ../${SKIN_NAME}_v${VERSION}.rmskin

# Step 4: Verify
echo "Verifying package..."
7z l ../${SKIN_NAME}_v${VERSION}.rmskin | grep -q "SpotifySetup.exe" && echo "✓ SpotifySetup.exe included"
! 7z l ../${SKIN_NAME}_v${VERSION}.rmskin | grep -q "@Vault" && echo "✓ @Vault excluded"

echo "Build complete: ${SKIN_NAME}_v${VERSION}.rmskin"
echo "Size: $(du -h ../${SKIN_NAME}_v${VERSION}.rmskin | cut -f1)"
```

**Usage**:
```bash
chmod +x build.sh
./build.sh
```

---

## Final Package Checklist

Before releasing v1.0.0:

- [ ] SpotifySetup.exe built and tested
- [ ] All PNG images created (or SVG converted)
- [ ] RMSKIN.ini metadata accurate
- [ ] Version numbers consistent across all files
- [ ] README.md complete with screenshots
- [ ] CHANGELOG.md up to date
- [ ] @Vault excluded from package
- [ ] Fresh install tested successfully
- [ ] OAuth flow tested end-to-end
- [ ] All features functional (track display, controls, caching)
- [ ] SHA256 checksum generated for .rmskin file
- [ ] Documentation reviewed (no broken links)
- [ ] License file included (MIT)

**Generate SHA256**:
```bash
sha256sum SpotifyNowPlaying_v1.0.0.rmskin > checksum.txt
cat checksum.txt
```

**Include in release notes**:
```
SHA256: a1b2c3d4e5f6... (verify download integrity)
```

---

## Conclusion

This guide ensures a professional, secure, and user-friendly .rmskin distribution.

**Next Steps**:
1. Complete build checklist
2. Test installation on clean machine
3. Publish to GitHub Releases
4. Share with Rainmeter community

**Support**: See [README.md](README.md) for user documentation and troubleshooting.
