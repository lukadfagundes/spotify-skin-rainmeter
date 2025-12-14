# Spotify Now Playing - Rainmeter Skin

A beautiful, lightweight Rainmeter skin that displays your currently playing Spotify track with full playback controls. Features automatic OAuth 2.0 token management, album artwork caching, and a sleek design that complements any desktop setup.

![Version](https://img.shields.io/badge/version-1.0.0-green)
![Rainmeter](https://img.shields.io/badge/rainmeter-4.5%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## Features

- **Real-time Track Information**: Song title, artist, album, and playback progress
- **Album Artwork**: Automatically downloads and caches album art
- **Playback Controls**: Play/pause, next track, previous track buttons
- **Progress Bar**: Visual playback progress with time display (MM:SS format)
- **Automatic Token Refresh**: Set it and forget it - OAuth tokens refresh automatically every ~55 minutes
- **Low Resource Usage**: Real-time updates with 1-second API polling
- **Error Handling**: Graceful fallbacks for network errors, missing data, and API issues
- **Customizable**: Easy-to-edit variables for colors, fonts, and layout

---

## Screenshots

![Playing State](screenshots/playing.png)
*Spotify Now Playing skin displaying current track with album art*

![Paused State](screenshots/paused.png)
*Skin appearance when playback is paused

![Next State](screenshots/next.png)
*Skin appearance when skipping to next song

![Paused State](screenshots/previous.png)
*Skin appearance when going back to the previous track

![Spotify.exe](screenshots/spotify-exe.png)
*Spotify.exe screen

---

## Requirements

### System Requirements
- **Windows**: 7 or later
- **Rainmeter**: Version 4.5 or higher ([Download](https://www.rainmeter.net/))
- **Internet**: Active internet connection for Spotify API access

### Spotify Requirements
- **Spotify Account**: Free or Premium (Premium required for playback controls)
- **Spotify Developer App**: Create at https://developer.spotify.com/dashboard
- **Active Playback**: Spotify must be playing on any device (desktop, mobile, web)

---

## 🔒 Security & Privacy Notice

**PLEASE READ BEFORE INSTALLING**

### Credential Storage
This skin stores Spotify OAuth credentials in **plaintext** at:
```
C:\Users\{YOU}\Documents\Rainmeter\Skins\@Vault\SpotifyCredentials.inc
```

### Security Risks
- ⚠️ **Malware** with user-level access can read these credentials
- ⚠️ **Backup software** may sync this file to cloud storage
- ⚠️ **Screen sharing** may expose credentials if folder is open

### Security Best Practices
✅ **DO**:
- Keep your system malware-free (use antivirus)
- Exclude `@Vault` folder from backup/sync software (Dropbox, OneDrive, etc.)
- Only use on trusted, personal computers

❌ **DON'T**:
- Share screenshots of the `@Vault` folder
- Use on shared/public computers
- Commit `@Vault` folder to git (already in `.gitignore`)

### Scope of Access
These credentials grant **LIMITED** API access to:
- ✅ View currently playing track
- ✅ Control playback (play/pause/skip)

They do **NOT** grant access to:
- ❌ Change account password or email
- ❌ Modify billing information
- ❌ Delete playlists or saved songs

### Privacy Policy
- **No Telemetry**: This skin does NOT collect or transmit any data to third parties
- **Data Flow**: Your computer → Spotify API (HTTPS) → Your computer
- **Local Only**: Album artwork cached locally in `DownloadFile\`
- **No Analytics**: No usage tracking or statistics collection

---

## Documentation

📚 **Complete Documentation Available**:
- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- **[Error Handling Guide](docs/ERROR-HANDLING.md)** - Troubleshooting and error recovery
- **[Performance Guide](docs/PERFORMANCE.md)** - Optimization techniques and benchmarks
- **[Build Guide](docs/RMSKIN_BUILD.md)** - Package creation and distribution
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Complete technical overview
- **[Changelog](docs/CHANGELOG.md)** - Version history and release notes

---

## Installation

### Quick Setup (Recommended)

1. **Install Rainmeter** (if not already installed):
   - Download from https://www.rainmeter.net/
   - Run installer and complete setup

2. **Download this skin**:
   - Download `SpotifyNowPlaying.rmskin` from [Releases](#)
   - Double-click the `.rmskin` file
   - Rainmeter will automatically install the skin

3. **Run OAuth Setup**:
   - Navigate to: `Documents\Rainmeter\Skins\SpotifyNowPlaying\`
   - Run `SpotifySetup.exe`
   - Follow the on-screen instructions:
     - Click "Open Spotify Developer Dashboard"
     - Create a new app:
       - App Name: Any name (e.g., "Rainmeter Spotify")
       - Redirect URI: `http://127.0.0.1:8888/callback` (EXACT)
       - Which API/SDKs: Check "Web API" only
     - Click Settings → Copy Client ID and Client Secret
     - Paste into SpotifySetup.exe
     - Click "Authorize with Spotify"
     - Complete authorization in your browser

4. **Load the Skin**:
   - Right-click Rainmeter system tray icon
   - Click "Manage"
   - Navigate to `SpotifyNowPlaying`
   - Click "Load"

5. **Enjoy!**
   - Play music on Spotify (any device)
   - The skin will display your currently playing track

---

### Manual Setup (Advanced)

<details>
<summary>Click to expand manual installation steps</summary>

1. **Clone or Download**:
   ```bash
   git clone https://github.com/yourusername/spotify-skin-rainmeter.git
   ```

2. **Copy to Rainmeter Skins folder**:
   ```
   Copy SpotifyNowPlaying folder to:
   C:\Users\[YourUsername]\Documents\Rainmeter\Skins\
   ```

3. **Create @Vault folder**:
   ```
   C:\Users\[YourUsername]\Documents\Rainmeter\Skins\@Vault\
   ```

4. **Create Spotify Developer App**:
   - Go to https://developer.spotify.com/dashboard
   - Click "Create App"
   - Fill in:
     - App Name: `Rainmeter Spotify Skin` (or any name)
     - App Description: `Personal Rainmeter integration`
     - Redirect URI: `http://127.0.0.1:8888/callback` ⚠️ **EXACT MATCH REQUIRED**
   - Click "Save"
   - Copy your Client ID and Client Secret

5. **Run SpotifySetup.py** (if building from source):
   ```bash
   cd SpotifyNowPlaying
   python SpotifySetup.py
   ```
   OR use pre-built `SpotifySetup.exe`

6. **Load Skin in Rainmeter**:
   - Right-click Rainmeter → Manage
   - Navigate to SpotifyNowPlaying
   - Click "Load" on `SpotifyNowPlaying.ini`

</details>

---

## Usage

### Basic Controls

- **Left-click Previous**: Skip to previous track
- **Left-click Play/Pause**: Toggle playback
- **Left-click Next**: Skip to next track

### Advanced Usage

**Force Token Refresh**:
```
Rainmeter → Manage → SpotifyNowPlaying → Custom Actions
Run: [!CommandMeasure MeasureTokenManager "ForceRefresh()"]
```

**Check Token Status**:
- Look at the debug text at the bottom of the skin (if DebugMode=1)
- Shows: `Token: Active | Expires: 45 minutes`

**Album Art Cache**:
```
Location: Documents\Rainmeter\Skins\SpotifyNowPlaying\DownloadFile\current-album.jpg
Size: ~50-200 KB (single file, automatically overwrites - no cleanup needed)
```

---

## Customization

### Colors and Fonts

Edit `SpotifyNowPlaying\@Resources\Variables.inc`:

```ini
[Variables]
; Background colors (RGBA)
ColorBackground=20,20,20,230
ColorBorder=29,185,84,255  ; Spotify green

; Text colors
ColorTrackName=255,255,255,255  ; White
ColorArtistName=180,180,180,255 ; Light gray
ColorAlbumName=150,150,150,255  ; Gray

; Fonts
FontFace=Segoe UI
FontSizeTrack=14
FontSizeArtist=11
FontSizeAlbum=10
```

### Layout Dimensions

Edit `Variables.inc`:

```ini
; Skin size
SkinWidth=400
SkinHeight=250

; Album art
AlbumArtSize=150
AlbumArtX=10
AlbumArtY=10

; Track info positioning
TrackNameX=170
TrackNameY=20
```

### Update Rates

**Currently Playing Data:** The skin polls the Spotify API every **1 second** for real-time track updates. This frequency is currently fixed and not user-configurable.

**Token Expiry Check:** The skin checks for token expiration every **60 seconds**.

**Note**: The 1-second polling provides real-time responsiveness but uses more network bandwidth than typical skins. Future versions may add configurable update rates.

---

## Troubleshooting

### Common Issues

#### "Not Playing" Despite Active Playback

**Causes:**
- Spotify is playing local files only (skin only works with Spotify catalog streaming)
- Private session enabled
- Token expired (auto-refresh should fix within 60 seconds)

**Solutions:**
1. Verify Spotify is streaming from Spotify catalog
2. Disable private session
3. Wait 60 seconds for automatic token refresh
4. Check Rainmeter log: `About → Log`

---

#### "API Error" Displayed

**Causes:**
- Invalid or expired access token
- Network connectivity issues
- Spotify API outage

**Solutions:**
1. Wait 60 seconds for automatic token refresh
2. Check internet connection
3. Check Spotify API status: https://status.spotify.com/
4. Re-run `SpotifySetup.exe` if persistent

---

#### Token Refresh Fails Repeatedly

**Causes:**
- Refresh token revoked (user revoked app in Spotify settings)
- Client secret changed in Spotify dashboard

**Solutions:**
1. Go to https://www.spotify.com/account/apps/
2. Check if "Rainmeter Spotify Skin" is authorized
3. If missing or you revoked it, re-run `SpotifySetup.exe`
4. Verify credentials in `@Vault\SpotifyCredentials.inc`

---

#### Playback Controls Don't Work

**Causes:**
- Spotify Free account (playback control requires Premium)
- No active Spotify device
- Missing OAuth scope

**Solutions:**
1. Verify Spotify Premium subscription
2. Ensure Spotify app is open and playing on ANY device
3. Re-run `SpotifySetup.exe` to ensure correct scopes (`user-modify-playback-state`)

---

#### Album Art Not Loading

**Causes:**
- Track has no album art (rare)
- Network error downloading image
- Cache directory missing

**Solutions:**
1. Verify `DownloadFile\` folder exists in skin directory
2. Check folder permissions (Rainmeter must be able to write)
3. Default placeholder image will show if download fails

---

#### International Characters Display as Question Marks

**Limitation:**
- Track, artist, and album names with international characters (Japanese, Korean, Cyrillic, etc.) display as `?` characters
- Example: "インフェルノ" displays as "????????"

**Cause:**
- Rainmeter's Lua script engine uses ANSI/Windows-1252 encoding internally
- Lua variables don't support UTF-8 encoding, which is required for international characters

**Status:**
- This is a known limitation of Rainmeter's Lua implementation
- Full Unicode support will require updates to the Rainmeter codebase itself
- See [Roadmap](#roadmap) for "Unicode/UTF-8 Support" as an upcoming feature

**Workaround:**
- None available at this time while using OAuth 2.0 approach
- Alternative: Use WebNowPlaying plugin (requires browser extension instead of OAuth)

---

### Debug Mode

Enable detailed logging in `@Resources\Variables.inc`:

```ini
DebugMode=1
```

This displays token status at the bottom of the skin and enables verbose logging.

View logs:
```
Rainmeter → About → Log
Filter by: [TokenManager] or [WebParser]
```

---

### Re-Authorization

If you need to completely reset OAuth tokens:

1. Delete `@Vault\SpotifyCredentials.inc`
2. Run `SpotifySetup.exe`
3. Complete authorization flow
4. Reload skin: `Rainmeter → Refresh`

---

## File Structure

```
SpotifyNowPlaying/
├── SpotifyNowPlaying.ini       # Main skin file
├── SpotifySetup.exe            # OAuth setup utility
├── README.md                   # This file
│
├── @Resources/
│   ├── Variables.inc           # Customization variables
│   ├── SpotifyCredentials.inc.template  # Template for @Vault
│   │
│   ├── Images/
│   │   ├── play.png            # Play button icon
│   │   ├── pause.png           # Pause button icon
│   │   ├── next.png            # Next button icon
│   │   ├── previous.png        # Previous button icon
│   │   ├── default-album.png   # Fallback album art
│   │   └── README_IMAGES.md    # Image specifications
│   │
│   ├── Scripts/
│   │   ├── TokenManager.lua    # Token refresh logic
│   │   └── Base64Encoder.lua   # Base64 encoding for OAuth
│   │
│   └── DownloadFile/
│       └── current-album.jpg   # Downloaded album art (auto-generated)
│
└── @Vault/ (SEPARATE LOCATION)
    └── SpotifyCredentials.inc  # OAuth credentials (NEVER commit!)
```

**Security Note**: The `@Vault` folder is located at:
```
C:\Users\[YourUsername]\Documents\Rainmeter\Skins\@Vault\
```
This is intentionally separate from the skin folder to prevent accidental sharing.

---

## Security & Privacy

### Credentials Storage

- **OAuth tokens** are stored in `@Vault\SpotifyCredentials.inc`
- **@Vault** is excluded from `.rmskin` packages by design
- **Client Secret** is only used locally, never transmitted except to Spotify

### API Scopes

This skin requests the following OAuth scopes:

- `user-read-currently-playing`: Read current track information
- `user-modify-playback-state`: Control playback (play, pause, next, previous)

**These scopes allow the skin to:**
- ✅ Read what you're currently playing
- ✅ Control playback on active devices
- ❌ **CANNOT** access your playlists, listening history, or personal data
- ❌ **CANNOT** make purchases or modify your account

### Network Activity

- Connects to `https://api.spotify.com` only
- Polls currently playing endpoint every 1 second (when loaded)
- Refreshes OAuth token every ~55 minutes
- All connections use HTTPS (encrypted)

### Revocation

To revoke access at any time:
1. Go to https://www.spotify.com/account/apps/
2. Find your app (e.g., "Rainmeter Spotify Skin")
3. Click "Remove Access"
4. Delete `@Vault\SpotifyCredentials.inc`

---

## Performance

### Resource Usage

| Metric | Value | Notes |
|--------|-------|-------|
| RAM | ~5-10 MB | Includes Rainmeter overhead |
| CPU | <1% average | Spikes briefly during updates |
| Network | ~400-500 bytes/sec | API polling (1-second intervals) |
| Disk | ~50-200 KB | Album art cache (single file, auto-overwrites) |

### Optimization Tips

1. **Reduce API polling frequency** (advanced - requires code modification):
   - Not user-configurable via Variables.inc
   - Requires editing `SpotifyNowPlaying.ini` line 122
   - Change `UpdateDivider=1` to `UpdateDivider=5` for 5-second polling
   - Trade-off: Less responsive but lower network usage

2. **Disable debug mode** (production):
   ```ini
   DebugMode=0
   ```

3. **Album art cache** (no action needed):
   ```
   Single file auto-overwrites - no cleanup required
   ```

4. **Unload skin when not in use**:
   ```
   Right-click Rainmeter → Manage → SpotifyNowPlaying → Unload
   ```

---

## Building from Source

### Prerequisites

- Python 3.7+
- `pip install requests pyinstaller`

### Build SpotifySetup.exe

```bash
cd spotify-skin-rainmeter
pip install -r requirements.txt
pyinstaller --onefile --windowed --name SpotifySetup SpotifySetup.py
```

Output: `dist/SpotifySetup.exe`

### Create .rmskin Package

1. Ensure all files are in `SpotifyNowPlaying/` folder
2. Use Rainmeter Skin Packager:
   - `Rainmeter → Manage → Package`
   - Select `SpotifyNowPlaying` folder
   - Ensure `@Vault` is excluded
   - Generate `.rmskin`

---

## FAQ

<details>
<summary><b>Do I need Spotify Premium?</b></summary>

- **For track display:** No, works with Spotify Free
- **For playback controls:** Yes, requires Spotify Premium (Spotify API limitation)

</details>

<details>
<summary><b>Does this work with Spotify Web Player?</b></summary>

Yes! The skin uses the Spotify Web API, which works with:
- Spotify Desktop App (Windows/Mac/Linux)
- Spotify Mobile App (iOS/Android)
- Spotify Web Player (browser)

As long as you're actively playing music on ANY device, the skin will display it.

</details>

<details>
<summary><b>Why do I need to create a Spotify Developer App?</b></summary>

Spotify requires OAuth 2.0 authentication for API access. Creating a developer app gives you a unique Client ID and Secret, which allows this skin to request permission to access your currently playing track.

**Your app is private** - only you can use these credentials.

</details>

<details>
<summary><b>How often does the token refresh?</b></summary>

- **Access tokens** expire after 1 hour (3600 seconds)
- **Automatic refresh** occurs when <5 minutes remain
- **Refresh tokens** are long-lived (unless manually revoked)

You should never need to re-authorize unless you revoke the app.

</details>

<details>
<summary><b>Can I customize the appearance?</b></summary>

Yes! Edit `@Resources\Variables.inc` to change:
- Colors (background, text, progress bar)
- Fonts (face, size, weight)
- Layout (positions, dimensions)
- Update rates

For advanced changes, edit `SpotifyNowPlaying.ini` directly.

</details>

<details>
<summary><b>Does this work offline?</b></summary>

No. The skin requires an active internet connection to:
- Poll the Spotify API for currently playing track
- Refresh OAuth tokens
- Download album artwork

If you go offline, the skin will display "Not Playing" or the last known state.

</details>

<details>
<summary><b>Is this safe? Will it access my private data?</b></summary>

Yes, it's safe. The skin:
- Only requests minimal OAuth scopes (currently playing + playback control)
- Stores credentials locally in `@Vault` (not uploaded anywhere)
- Connects exclusively to official Spotify API endpoints
- Source code is open and auditable

**The skin CANNOT access:**
- Your playlists
- Listening history
- Email or personal info
- Payment details

</details>

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push to branch: `git push origin feature/my-feature`
5. Open a Pull Request

**Guidelines:**
- Follow existing code style
- Test thoroughly before submitting
- Update documentation for new features
- Never commit credentials or tokens

---

## Changelog

### Version 1.0.0 (2025-01-XX)

**Initial Release**
- ✅ Real-time track display (song, artist, album)
- ✅ Album artwork with caching
- ✅ Playback controls (play/pause, next, previous)
- ✅ Progress bar with time display
- ✅ Automatic OAuth 2.0 token refresh
- ✅ Error handling and graceful fallbacks
- ✅ SpotifySetup.exe GUI utility
- ✅ Comprehensive documentation

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

**TL;DR**: Free to use, modify, and distribute. No warranty provided.

---

## Acknowledgements

- **Spotify Web API**: https://developer.spotify.com/documentation/web-api
- **Rainmeter**: https://www.rainmeter.net/
- **Contributors**: (List contributors here)

---

## Support

**Issues & Questions:**
- Open an issue: https://github.com/yourusername/spotify-skin-rainmeter/issues
- Check [Troubleshooting](#troubleshooting) section
- Review [Error Handling Guide](docs/ERROR-HANDLING.md) for detailed error scenarios

**Before reporting issues:**
1. Enable `DebugMode=1` in `Variables.inc`
2. Check Rainmeter log: `About → Log`
3. Try re-running `SpotifySetup.exe`
4. Include log output (redact tokens!) in issue report

---

## Roadmap

Future enhancements being considered:

- [ ] **Unicode/UTF-8 Support** - Full international character display (requires Rainmeter codebase updates)
- [ ] ~~Volume control slider~~ - Attempted but removed due to curl conflicts with frequent API polling (data reliability prioritized)
- [ ] Playlist management (add to playlist)
- [ ] Like/unlike current track
- [ ] Multiple skin variants (compact, large, mini)
- [ ] Visualizer integration
- [ ] Shuffle/repeat toggle
- [ ] Device selection dropdown
- [ ] Lyrics display (via third-party API)

**Suggestions?** Open a feature request!

---

## Support the Project

If you find this skin useful and want to support its development, consider buying me a coffee!

**Venmo**: @strawhatluka
**Cash App**: $strawhatluka

Your support helps keep this project maintained and updated. Thank you! ☕

---

**Made with ❤️ for the Rainmeter community**

*Star this repo if you find it useful!*
