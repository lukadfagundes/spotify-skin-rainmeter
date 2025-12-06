# Changelog

All notable changes to the Spotify Now Playing Rainmeter Skin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Volume control slider
- Playlist management (add to playlist button)
- Like/unlike current track
- Multiple skin variants (compact, large, mini)
- Visualizer integration
- Shuffle/repeat toggle buttons
- Device selection dropdown
- Lyrics display integration

## [1.0.0] - 2025-01-XX

### Added
- Initial release of Spotify Now Playing skin
- Real-time currently playing track display
  - Track name, artist, album
  - Progress bar with time display (MM:SS format)
  - Playback state indicator (playing/paused)
- Album artwork with intelligent caching
  - Auto-download from Spotify API
  - Disk cache to prevent redundant downloads
  - Fallback to default image on failure
- Playback controls
  - Play/Pause toggle button
  - Next track button
  - Previous track button
  - Spotify Premium required for controls
- Automatic OAuth 2.0 token management
  - Access token refresh every ~55 minutes
  - Proactive refresh (5 minutes before expiry)
  - No manual intervention required
  - Automatic retry on failure
- SpotifySetup.exe OAuth utility
  - User-friendly tkinter GUI
  - One-click Spotify authorization
  - Automatic credential writing to @Vault
  - Comprehensive error handling and logging
- Comprehensive error handling
  - Graceful fallback for network errors
  - User-friendly error messages
  - Detailed logging for troubleshooting
  - Automatic recovery mechanisms
- Customization support
  - Variables.inc for easy color/font changes
  - Adjustable update rates
  - Debug mode toggle
  - Layout customization options
- Complete documentation
  - README.md with setup instructions
  - ERROR-HANDLING.md with troubleshooting guide
  - PERFORMANCE.md with optimization tips
  - RMSKIN_BUILD.md with packaging instructions
- Security features
  - @Vault pattern for credential storage
  - Credentials excluded from .rmskin distribution
  - .gitignore configured to prevent token leakage
  - OAuth scope minimization (only required permissions)

### Technical Details
- Rainmeter 4.5+ compatibility
- Spotify Web API integration
  - `GET /v1/me/player/currently-playing` endpoint
  - `POST /api/token` OAuth refresh endpoint
  - `PUT /v1/me/player/play` playback control
  - `PUT /v1/me/player/pause` playback control
  - `POST /v1/me/player/next` skip track
  - `POST /v1/me/player/previous` previous track
- OAuth 2.0 Authorization Code Flow
  - Client credentials authentication
  - Refresh token rotation support
  - Automatic token expiry management
- Lua scripting
  - TokenManager.lua for token lifecycle
  - Base64Encoder.lua for OAuth headers
- WebParser measures for API communication
- Optimized performance
  - 5-second API polling interval
  - Album art caching to disk
  - Conditional UI updates
  - <1% CPU usage average
  - <15 MB RAM footprint

### Dependencies
- Python 3.7+ (for building SpotifySetup.exe)
- Requests library (for HTTP in setup utility)
- PyInstaller (for building executable)

### Known Limitations
- Playback controls require Spotify Premium
- Only works with Spotify catalog streaming (not local files)
- Requires active internet connection
- No offline mode support
- Album art cache grows unbounded (manual cleanup required)

### Security
- OAuth tokens stored in @Vault (excluded from skin distribution)
- Client secrets never transmitted except to Spotify
- All API communication over HTTPS
- No third-party tracking or analytics
- Minimal OAuth scopes requested:
  - `user-read-currently-playing`
  - `user-modify-playback-state`

---

## Version History

### [1.0.0] - 2025-01-XX
- Initial public release

---

## Upgrade Notes

### Upgrading to 1.0.0 (First Release)

This is the initial release. No upgrade path needed.

**Fresh Installation**:
1. Download `SpotifyNowPlaying_v1.0.0.rmskin`
2. Double-click to install
3. Run `SpotifySetup.exe` to configure OAuth
4. Load skin in Rainmeter

---

## Breaking Changes

None (initial release)

---

## Contributors

- Spotify Rainmeter Skin Project Team
- (Add contributor names here)

---

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/yourusername/spotify-skin-rainmeter/issues
- Documentation: See README.md and ERROR-HANDLING.md
- Rainmeter Forums: https://forum.rainmeter.net/

---

**Note**: Version dates will be updated upon official release.
