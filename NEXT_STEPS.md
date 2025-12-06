# Next Steps - Quick Reference

**Status**: ✅ Code Complete | ✅ PNGs Ready | ⏳ Testing Required

---

## Immediate Actions (Before You Can Test)

### 0️⃣ Clean Old Build Artifacts (If Re-testing)

If you've already built once and need to rebuild:

```bash
# Navigate to root directory
cd "c:\Users\lukaf\Desktop\Dev Work\spotify-skin-rainmeter"

# Remove old build files
rm -rf build/ dist/ SpotifySetup.spec

# Remove old executable from skin folder
rm SpotifyNowPlaying/SpotifySetup.exe

# Remove old Rainmeter installation (for completely fresh test)
rm -rf "$HOME/Documents/Rainmeter/Skins/SpotifyNowPlaying"

# Optional: Remove virtual environment (if starting completely fresh)
# rm -rf venv/
```

---

### 1️⃣ Build SpotifySetup.exe ⚠️ **REQUIRED**

**With Virtual Environment**

```bash
# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
# On Windows (Git Bash):
source venv/Scripts/activate
# On Windows (PowerShell):
# .\venv\Scripts\Activate.ps1
# On Windows (CMD):
# venv\Scripts\activate.bat

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Build executable
pyinstaller --onefile --windowed --name SpotifySetup SpotifySetup.py

# Copy to skin folder
cp dist/SpotifySetup.exe SpotifyNowPlaying/

# Deactivate when done (optional)
deactivate
```

**Verify**: `SpotifyNowPlaying/SpotifySetup.exe` exists (~8-12 MB)

**What's New**:
- ✅ Icon displays in header (using default-album.png)
- ✅ Detailed instructions include API/SDK selection
- ✅ All fields pre-specified for you

---

## Testing Workflow

Once Step 1 is complete:

### 3️⃣ Copy Skin to Rainmeter

```bash
# Copy entire folder to Rainmeter Skins directory
cp -r SpotifyNowPlaying "$HOME/Documents/Rainmeter/Skins/"
```

### 4️⃣ Create Spotify Developer App

1. Go to https://developer.spotify.com/dashboard
2. Click **"Create App"**
3. Fill in:
   - **App Name**: `Rainmeter Spotify` (or any name)
   - **App Description**: `Personal Rainmeter skin`
   - **Redirect URI**: `http://127.0.0.1:8888/callback` ⚠️ **MUST BE EXACT**
   - **Which API/SDKs**: Check **"Web API"** only
4. Check agreement box → Click **Save**
5. Click **Settings** → Copy **Client ID** and **Client Secret**

### 5️⃣ Run OAuth Setup

```bash
# Navigate to
cd "$HOME/Documents/Rainmeter/Skins/SpotifyNowPlaying/"

# Run
./SpotifySetup.exe
```

1. Paste Client ID + Secret
2. Click "Authorize with Spotify"
3. Approve in browser
4. Verify success message

### 6️⃣ Load Skin in Rainmeter

```
Right-click Rainmeter → Manage → SpotifyNowPlaying → Load
```

### 7️⃣ Test Features

✅ **Play music on Spotify**
✅ **Skin should display track info within 5 seconds**
✅ **Album art should download**
✅ **Controls should work** (if Premium)

---

## Full Testing Guide

See **[TESTING.md](TESTING.md)** for comprehensive testing checklist

---

## Pre-Release Checklist

Before publishing v1.0.0:

- [ ] SpotifySetup.exe built
- [ ] PNG images created (or SVG references updated)
- [ ] Tested on local machine successfully
- [ ] All features verified working
- [ ] Token refresh tested (wait 55 min OR force expiry)
- [ ] Error scenarios tested (offline, no playback, etc.)
- [ ] Documentation reviewed
- [ ] .rmskin package created (see [docs/RMSKIN_BUILD.md](docs/RMSKIN_BUILD.md))
- [ ] .rmskin tested on fresh Rainmeter install
- [ ] Screenshots captured for README
- [ ] GitHub release created with v1.0.0 tag

---

## Quick Commands Reference

**Build executable**:
```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --name SpotifySetup SpotifySetup.py
```

**Convert images**:
```bash
magick convert input.svg -resize 32x32 output.png
```

**Copy to Rainmeter**:
```bash
cp -r SpotifyNowPlaying "$HOME/Documents/Rainmeter/Skins/"
```

**View Rainmeter log**:
```
Rainmeter → About → Log
```

**Enable debug mode**:
Edit `SpotifyNowPlaying/@Resources/Variables.inc`:
```ini
DebugMode=1
```

**Force token refresh**:
```
Rainmeter → Manage → SpotifyNowPlaying → Custom Actions
Run: [!CommandMeasure MeasureTokenManager "ForceRefresh()"]
```

---

## Troubleshooting

**SpotifySetup.exe won't run**:
- Antivirus may flag PyInstaller executables (false positive)
- Add exception or run from source: `python SpotifySetup.py`

**Images not showing**:
- Use Option A (SVG references) for quick testing
- Check file paths are correct

**Skin won't load**:
- Check Rainmeter log for errors
- Verify @Vault\SpotifyCredentials.inc exists
- Ensure Variables.inc has correct @Include path

**"API Error" after setup**:
- Wait 60 seconds for token refresh
- Check internet connection
- Verify credentials in @Vault file

---

## Documentation

- **[README.md](README.md)** - Main documentation
- **[TESTING.md](TESTING.md)** - Complete testing guide
- **[docs/](docs/)** - All user documentation
- **[docs/QUICK_START.md](docs/QUICK_START.md)** - 5-minute user setup guide

---

## Support

Questions during testing? Check:
1. [TESTING.md](TESTING.md) troubleshooting sections
2. [docs/ERROR-HANDLING.md](docs/ERROR-HANDLING.md) for error scenarios
3. Rainmeter log with `DebugMode=1`

---

**Current Status**: Ready for local testing after Steps 1 & 2!

**Time to Test**: ~15-30 minutes (including OAuth setup)
