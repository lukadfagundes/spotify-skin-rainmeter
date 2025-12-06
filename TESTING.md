# Testing Guide - Spotify Now Playing Skin

This guide walks you through testing the skin locally before distribution.

---

## Prerequisites

Before you can test, you need to complete these steps:

### 1. Build SpotifySetup.exe

```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# OR: .\venv\Scripts\Activate.ps1  # PowerShell
# OR: venv\Scripts\activate.bat    # CMD

# Install dependencies (Pillow for icon display)
pip install requests Pillow pyinstaller

# Build executable
pyinstaller --onefile --windowed --name SpotifySetup SpotifySetup.py

# Copy to skin folder
cp dist/SpotifySetup.exe SpotifyNowPlaying/

# Deactivate venv (optional)
deactivate
```

**Verify**: Check that `SpotifyNowPlaying/SpotifySetup.exe` exists (~8-12 MB)

---

### 2. Create PNG Button Images

The skin currently has SVG placeholders. You need PNG files:

**Option A: Quick Testing (Use Existing SVGs)**

For initial testing, you can modify the skin to use SVG files directly:

Edit `SpotifyNowPlaying/SpotifyNowPlaying.ini`:

```ini
; Change .png to .svg in all image references
[MeterButtonPrevious]
ImageName=#@#Images\previous.svg  ; Changed from .png

[MeterButtonPlayPause]
ImageName=#@#Images\play.svg  ; Changed from .png

[MeterButtonNext]
ImageName=#@#Images\next.svg  ; Changed from .png
```

**Option B: Convert to PNG (Production)**

```bash
# Using ImageMagick
cd SpotifyNowPlaying/@Resources/Images/
magick convert play.svg -resize 32x32 play.png
magick convert pause.svg -resize 32x32 pause.png
magick convert next.svg -resize 32x32 next.png
magick convert previous.svg -resize 32x32 previous.png
magick convert default-album.svg -resize 200x200 default-album.png
```

**Option C: Download Free Icons**

Use any 32x32 PNG icons from free icon sites:
- https://www.flaticon.com/ (search "play pause next previous")
- https://icons8.com/
- https://www.iconfinder.com/

Place them in `SpotifyNowPlaying/@Resources/Images/`

---

## Testing Steps

### Step 1: Install Rainmeter (if not already installed)

1. Download from https://www.rainmeter.net/
2. Run installer
3. Complete setup

**Verify**: Rainmeter icon appears in system tray

---

### Step 2: Copy Skin to Rainmeter Skins Folder

```bash
# Copy entire SpotifyNowPlaying folder to Rainmeter Skins directory
cp -r SpotifyNowPlaying "C:\Users\YOUR_USERNAME\Documents\Rainmeter\Skins\"
```

**Replace `YOUR_USERNAME`** with your actual Windows username.

**Verify**:
```bash
ls "C:\Users\YOUR_USERNAME\Documents\Rainmeter\Skins\SpotifyNowPlaying\"
# Should show: SpotifyNowPlaying.ini, SpotifySetup.exe, @Resources folder
```

---

### Step 3: Create Spotify Developer App

1. Go to https://developer.spotify.com/dashboard
2. Log in with your Spotify account
3. Click **"Create App"**
4. Fill in:
   - **App Name**: `Rainmeter Test` (or any name)
   - **App Description**: `Testing Rainmeter skin`
   - **Website**: (leave blank, optional)
   - **Redirect URI**: `http://127.0.0.1:8888/callback` ⚠️ **MUST BE EXACT**
   - **Which API/SDKs are you planning to use?**:
     - ✅ Check **"Web API"** only
     - ❌ Leave unchecked: Web Playback SDK, Android, iOS, Ads API
5. Check "I understand and agree with Spotify's Developer Terms of Service and Design Guidelines"
6. Click **Save**
7. Click **Settings** to view your credentials

**Verify**: You see Client ID and Client Secret

---

### Step 4: Run OAuth Setup

1. Navigate to: `C:\Users\YOUR_USERNAME\Documents\Rainmeter\Skins\SpotifyNowPlaying\`
2. Double-click **SpotifySetup.exe**
3. In the setup window:
   - Paste **Client ID** from Spotify Dashboard
   - Paste **Client Secret** from Spotify Dashboard
   - Click **"Authorize with Spotify"**
4. Your browser opens with Spotify authorization
5. Click **"Agree"** to authorize the app
6. Browser shows: **"✓ Authorization Successful!"**
7. Setup utility shows: **"✓✓✓ SETUP COMPLETE! ✓✓✓"**

**Verify**:
```bash
ls "C:\Users\YOUR_USERNAME\Documents\Rainmeter\Skins\@Vault\"
# Should show: SpotifyCredentials.inc
```

**Check credentials file**:
```bash
cat "C:\Users\YOUR_USERNAME\Documents\Rainmeter\Skins\@Vault\SpotifyCredentials.inc"
```

Should contain:
```ini
SpotifyClientID=your_client_id_here
SpotifyClientSecret=your_client_secret_here
SpotifyAccessToken=BQD... (long token)
SpotifyRefreshToken=AQD... (long token)
SpotifyTokenExpiry=1733... (unix timestamp)
```

---

### Step 5: Load Skin in Rainmeter

1. Right-click **Rainmeter** icon in system tray
2. Click **Manage**
3. In Rainmeter Manager, navigate to **SpotifyNowPlaying** in left panel
4. Click **Load** button next to `SpotifyNowPlaying.ini`

**Expected Result**: Skin appears on your desktop (400x250 pixel window)

**If skin doesn't appear**:
- Check Rainmeter log: `About → Log`
- Look for error messages
- Common issues:
  - Missing @Vault\SpotifyCredentials.inc (run SpotifySetup.exe)
  - Image files missing (.png not found - use SVG temporarily)
  - Syntax errors in .ini file

---

### Step 6: Test Track Display

1. Open Spotify (desktop app, web player, or mobile)
2. Play any song
3. Wait up to 5 seconds

**Expected Result**: Skin displays:
- ✅ Track name
- ✅ Artist name
- ✅ Album name
- ✅ Progress bar moving
- ✅ Time display updating (MM:SS format)

**If "Not Playing" shows**:
- Verify Spotify is actually playing (not paused)
- Check you're streaming from Spotify catalog (not local files)
- Wait 60 seconds (token might be refreshing)
- Check Rainmeter log for API errors

---

### Step 7: Test Album Art

**Expected Result**: Album artwork downloads and displays

**If default placeholder shows**:
- Check `@Resources\Cache\` folder - should have .jpg files downloading
- Verify internet connection
- Check Rainmeter log for download errors
- Some tracks may not have album art (rare)

**Test caching**:
1. Play track A (album art downloads)
2. Play track B (different album art downloads)
3. Play track A again (should load from cache instantly - no download)

---

### Step 8: Test Playback Controls (Premium Only)

⚠️ **Requires Spotify Premium subscription**

**Test Previous Button**:
1. Click left button (previous track icon)
2. Spotify should skip to previous track
3. Skin updates within 5 seconds

**Test Play/Pause Button**:
1. Click center button (play/pause icon)
2. Spotify should pause
3. Button icon changes to play icon
4. Click again to resume
5. Button icon changes to pause icon

**Test Next Button**:
1. Click right button (next track icon)
2. Spotify should skip to next track
3. Skin updates within 5 seconds

**If controls don't work**:
- Verify Spotify Premium subscription
- Ensure Spotify app is open on ANY device
- Check Rainmeter log for 403 errors (Premium required)
- Check OAuth scopes include `user-modify-playback-state`

---

### Step 9: Test Token Refresh

This test takes ~1 hour.

**Option A: Wait for Natural Refresh**

1. Leave skin loaded for 55+ minutes
2. Watch Rainmeter log around 55-minute mark
3. Look for log messages:
   ```
   Info: Token expires in 287 seconds - triggering refresh
   Info: New token received (expires in 3600 seconds)
   Info: Token refresh complete - credentials saved to @Vault
   ```

**Expected Result**:
- Skin continues working without interruption
- @Vault\SpotifyCredentials.inc updated with new tokens
- No "API Error" displayed

---

**Option B: Force Token Expiry (Advanced)**

1. Open `@Vault\SpotifyCredentials.inc`
2. Find `SpotifyTokenExpiry=1733...`
3. Change to a past timestamp: `SpotifyTokenExpiry=1000000000`
4. Save file
5. Refresh skin: Right-click skin → Refresh
6. Watch Rainmeter log

**Expected Result**:
- Within 60 seconds, TokenManager detects expired token
- Automatic refresh triggered
- New token obtained
- Skin continues working

---

### Step 10: Test Error Scenarios

**Test Offline Mode**:
1. Disconnect internet
2. Wait 5 seconds

**Expected Result**: Skin displays "Not Playing" or "API Error" gracefully (no crash)

**Reconnect internet**:
- Skin should resume within 5 seconds

---

**Test No Playback**:
1. Pause Spotify
2. Wait 5 seconds

**Expected Result**: Skin displays "Not Playing" or shows paused state

---

**Test Missing Credentials**:
1. Rename `@Vault\SpotifyCredentials.inc` to `.bak`
2. Refresh skin

**Expected Result**:
- Rainmeter log shows error: "Cannot open file"
- Skin displays error state
- No crash

**Restore**:
- Rename file back
- Refresh skin

---

## Testing Checklist

Before declaring the skin "ready", verify all these work:

### Core Functionality
- [ ] Skin loads without errors
- [ ] Track name displays correctly
- [ ] Artist name displays correctly
- [ ] Album name displays correctly
- [ ] Progress bar moves smoothly
- [ ] Time display updates (MM:SS format)
- [ ] Album art downloads and displays
- [ ] Album art caching works (no re-download for same track)

### Playback Controls (Premium)
- [ ] Previous button skips to previous track
- [ ] Play/Pause button toggles playback
- [ ] Play/Pause icon changes based on state
- [ ] Next button skips to next track
- [ ] Skin updates after control actions

### Token Management
- [ ] OAuth setup completes successfully
- [ ] Credentials saved to @Vault
- [ ] Tokens loaded on skin startup
- [ ] Token refresh occurs automatically (wait 55+ min OR force expiry)
- [ ] Skin continues working after refresh

### Error Handling
- [ ] "Not Playing" when Spotify paused
- [ ] "API Error" when offline (graceful)
- [ ] Default album art when no image available
- [ ] No crashes on missing credentials
- [ ] Rainmeter log shows helpful error messages

### Performance
- [ ] CPU usage <1% average (check Task Manager)
- [ ] RAM usage <15 MB (check Task Manager)
- [ ] No lag or stuttering in UI
- [ ] Progress bar animates smoothly

### Customization
- [ ] Edit Variables.inc (change color)
- [ ] Refresh skin
- [ ] Changes apply correctly

---

## Debugging Tips

### Enable Debug Mode

Edit `@Resources\Variables.inc`:
```ini
DebugMode=1
```

Refresh skin. Now you'll see token status at the bottom:
```
Token: Active | Expires: 45 minutes
```

### View Rainmeter Log

```
Rainmeter → About → Log
```

Filter by:
- `[TokenManager]` - Token refresh events
- `[WebParser]` - API calls and errors

### Common Error Messages

**"Token expired! Attempting refresh..."**
- Normal! Happens when token <5 min from expiry
- Should auto-resolve within 60 seconds

**"Token refresh failed: Connection failed"**
- Check internet connection
- Will retry in 60 seconds

**"Cannot open file: C:\...\@Vault\SpotifyCredentials.inc"**
- Run SpotifySetup.exe to create credentials

**"✗ Port 8888 already in use"**
- Close any app using port 8888
- Or change port in SpotifySetup.py and Spotify redirect URI

---

## Testing on Fresh Machine

To test the installation experience:

1. **Use a VM or separate computer** (if available)
2. Install Rainmeter
3. Install .rmskin package (once built)
4. Run SpotifySetup.exe
5. Verify end-to-end flow works

**Simulates**: Real user experience from scratch

---

## Performance Testing

### CPU Usage Test

```bash
# Windows Task Manager
1. Open Task Manager (Ctrl+Shift+Esc)
2. Go to Details tab
3. Find Rainmeter.exe
4. Monitor CPU % column
```

**Expected**: <1% average, brief spikes to ~1-2% during updates

---

### Memory Usage Test

```bash
# Task Manager → Details → Rainmeter.exe → Memory column
```

**Expected**:
- Fresh load: ~8 MB
- Active playback: ~10 MB
- After 1 hour: ~12-15 MB (album art cache)

---

### Network Usage Test

```bash
# Task Manager → Performance → Network
# Play music for 1 minute, observe network usage
```

**Expected**: ~400-500 bytes/sec average

---

## Automated Testing (Optional)

Create a test script to verify API responses:

**test_api.py**:
```python
import requests
import json

# Load credentials
with open(r'C:\Users\YOUR_USERNAME\Documents\Rainmeter\Skins\@Vault\SpotifyCredentials.inc') as f:
    for line in f:
        if 'SpotifyAccessToken=' in line:
            token = line.split('=')[1].strip()

# Test currently playing endpoint
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Track: {data['item']['name']}")
    print(f"Artist: {data['item']['artists'][0]['name']}")
    print("✅ API working!")
else:
    print(f"❌ Error: {response.text}")
```

Run: `python test_api.py`

---

## Next Steps After Testing

Once all tests pass:

1. ✅ Document any issues found
2. ✅ Fix bugs
3. ✅ Re-test
4. ✅ Build .rmskin package (see [docs/RMSKIN_BUILD.md](docs/RMSKIN_BUILD.md))
5. ✅ Test .rmskin installation
6. ✅ Publish release!

---

## Getting Help

**If you encounter issues during testing**:

1. Check this guide's troubleshooting sections
2. Review [docs/ERROR-HANDLING.md](docs/ERROR-HANDLING.md)
3. Check Rainmeter log with `DebugMode=1`
4. Open GitHub issue with:
   - Error message (redact tokens!)
   - Rainmeter version
   - Windows version
   - Steps to reproduce

---

**Happy Testing!** 🧪
