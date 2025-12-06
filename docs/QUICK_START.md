# Quick Start Guide - Spotify Now Playing Skin

**Get up and running in 5 minutes!**

---

## Prerequisites

- ✅ Windows 7 or later
- ✅ [Rainmeter 4.5+](https://www.rainmeter.net/) installed
- ✅ Active Spotify account (Free or Premium)
- ✅ Internet connection

---

## Installation (3 Steps)

### Step 1: Install the Skin

1. Download `SpotifyNowPlaying_v1.0.0.rmskin`
2. Double-click the file
3. Click **Install** in the Rainmeter installer

**Done!** The skin is now installed.

---

### Step 2: Configure Spotify OAuth

1. Navigate to your Rainmeter Skins folder:
   ```
   Documents\Rainmeter\Skins\SpotifyNowPlaying\
   ```

2. Run **SpotifySetup.exe**

3. In the setup window:
   - Click **"Open Spotify Developer Dashboard"**
   - Log in to Spotify
   - Click **"Create App"**
   - Fill in:
     - **App Name**: `Rainmeter Spotify` (or any name)
     - **App Description**: `Personal Rainmeter skin`
     - **Redirect URI**: `http://127.0.0.1:8888/callback` ⚠️ **EXACT MATCH**
   - Click **Save**

4. Copy your **Client ID** and **Client Secret** from Spotify dashboard

5. Paste them into SpotifySetup.exe

6. Click **"Authorize with Spotify"**

7. Your browser opens → Click **"Agree"** to authorize

8. See success message: **"✓ Authorization Successful!"**

**Done!** Credentials are saved to @Vault.

---

### Step 3: Load the Skin

1. Right-click Rainmeter icon in system tray
2. Click **Manage**
3. Navigate to **SpotifyNowPlaying** in left panel
4. Click **Load** on `SpotifyNowPlaying.ini`

**Done!** The skin appears on your desktop.

---

## First Use

### Start Playing Music

1. Open Spotify (desktop, mobile, or web player)
2. Play any song
3. Watch the skin update within 5 seconds!

### Using Playback Controls

- **Play/Pause**: Click the center button
- **Next Track**: Click the right button
- **Previous Track**: Click the left button

**Note**: Controls require **Spotify Premium**. Free users can view track info only.

---

## Troubleshooting

### "Not Playing" despite music playing

**Solutions**:
- ✅ Ensure Spotify is streaming from Spotify catalog (not local files)
- ✅ Wait 5 seconds for update
- ✅ Check internet connection
- ✅ Disable private session in Spotify

---

### "API Error" displayed

**Solutions**:
- ✅ Wait 60 seconds for automatic token refresh
- ✅ Check Rainmeter log: `Rainmeter → About → Log`
- ✅ Re-run `SpotifySetup.exe` if persistent

---

### Controls don't work

**Causes**:
- ❌ Spotify Free account (Premium required for controls)
- ❌ No active Spotify device

**Solutions**:
- ✅ Upgrade to Spotify Premium
- ✅ Ensure Spotify app is open on any device

---

### Album art not showing

**Solutions**:
- ✅ Check `@Resources\Cache\` folder exists
- ✅ Verify internet connection
- ✅ Default placeholder shows if download fails

---

## Customization

Want to change colors, fonts, or layout?

Edit `Documents\Rainmeter\Skins\SpotifyNowPlaying\@Resources\Variables.inc`

**Example**: Change background color
```ini
ColorBackground=20,20,20,230  ; Change these RGBA values
```

**Apply changes**:
```
Right-click skin → Refresh
```

See [README.md](README.md#customization) for full customization guide.

---

## Advanced

### Debug Mode

Enable detailed logging:
1. Edit `Variables.inc`
2. Set `DebugMode=1`
3. Refresh skin
4. Check Rainmeter log for diagnostic info

### Force Token Refresh

If tokens seem stale:
1. Right-click Rainmeter → Manage
2. Select SpotifyNowPlaying
3. Click **Custom Actions**
4. Run: `[!CommandMeasure MeasureTokenManager "ForceRefresh()"]`

### Clear Album Art Cache

Free up disk space:
```
Delete: Documents\Rainmeter\Skins\SpotifyNowPlaying\@Resources\Cache\*.jpg
```

---

## Support

**Need Help?**
- 📖 Full documentation: [README.md](README.md)
- 🔧 Troubleshooting: [ERROR-HANDLING.md](ERROR-HANDLING.md)
- 🐛 Report issues: [GitHub Issues](https://github.com/yourusername/spotify-skin-rainmeter/issues)

---

## FAQ

**Q: Do I need Spotify Premium?**
- Track display: No (works with Free)
- Playback controls: Yes (Premium required)

**Q: Does this work with mobile Spotify?**
- Yes! Displays whatever is playing on ANY device.

**Q: How often does it update?**
- Every 5 seconds (configurable)

**Q: Will I need to re-authorize?**
- No! Tokens auto-refresh. Only re-authorize if you revoke the app.

**Q: Is my data safe?**
- Yes! Credentials stored locally in @Vault. No tracking or third-party access.

---

**Enjoy your new Spotify skin!** 🎵

*Made with ❤️ for the Rainmeter community*
