# Documentation - Spotify Now Playing Skin

Welcome to the complete documentation for the Spotify Now Playing Rainmeter skin.

---

## 📖 Documentation Index

### Getting Started

**[Quick Start Guide](QUICK_START.md)** - 5-minute setup guide
- Installation steps
- OAuth configuration
- First use instructions
- Common troubleshooting

**Use this if**: You just want to get the skin working quickly.

---

### Troubleshooting & Support

**[Error Handling Guide](ERROR-HANDLING.md)** - Comprehensive error reference
- Error scenarios and causes
- Recovery strategies
- Troubleshooting workflows
- Logging and debugging
- Security best practices

**Use this if**: You're encountering errors or unexpected behavior.

---

### Performance & Optimization

**[Performance Guide](PERFORMANCE.md)** - Optimization techniques
- Resource usage benchmarks
- API call optimization
- Caching strategies
- Tuning for different use cases (low-power, high-responsiveness, minimal network)
- Profiling tools

**Use this if**: You want to optimize resource usage or understand performance characteristics.

---

### Distribution & Packaging

**[Build Guide](RMSKIN_BUILD.md)** - Creating .rmskin packages
- Build prerequisites
- Step-by-step packaging process
- Testing checklist
- Distribution strategies
- Version management

**Use this if**: You want to build from source or distribute the skin.

---

### Project Information

**[Project Summary](PROJECT_SUMMARY.md)** - Complete technical overview
- Implementation metrics
- Feature completeness breakdown
- Architecture details
- Security implementation
- Performance characteristics
- Future roadmap

**Use this if**: You want to understand the project architecture or contribute.

---

**[Changelog](CHANGELOG.md)** - Version history
- Release notes
- New features
- Bug fixes
- Breaking changes
- Upgrade notes

**Use this if**: You want to see what's changed between versions.

---

## 🗂️ Documentation by Topic

### Installation
- [Quick Start Guide](QUICK_START.md) - Installation steps
- [Build Guide](RMSKIN_BUILD.md#installation) - Advanced installation

### Configuration
- [Quick Start Guide](QUICK_START.md#step-2-configure-spotify-oauth) - OAuth setup
- [Main README](../README.md#customization) - Customization options

### Usage
- [Main README](../README.md#usage) - Basic controls
- [Quick Start Guide](QUICK_START.md#using-playback-controls) - Playback controls

### Troubleshooting
- [Error Handling Guide](ERROR-HANDLING.md) - Complete error reference
- [Quick Start Guide](QUICK_START.md#troubleshooting) - Quick fixes
- [Main README](../README.md#troubleshooting) - Common issues

### Performance
- [Performance Guide](PERFORMANCE.md) - Complete optimization guide
- [Performance Guide](PERFORMANCE.md#tuning-for-different-use-cases) - Use case tuning

### Development
- [Build Guide](RMSKIN_BUILD.md) - Packaging and distribution
- [Project Summary](PROJECT_SUMMARY.md) - Technical architecture
- [Changelog](CHANGELOG.md) - Version history

### Security
- [Error Handling Guide](ERROR-HANDLING.md#security-best-practices) - Security practices
- [Main README](../README.md#security--privacy) - Privacy policy
- [Project Summary](PROJECT_SUMMARY.md#security-implementation) - Security architecture

---

## 📋 Quick Reference

### File Locations

```
Documents\Rainmeter\Skins\
├── SpotifyNowPlaying\          # Main skin folder
│   ├── SpotifyNowPlaying.ini   # Main skin file
│   ├── SpotifySetup.exe        # OAuth utility
│   └── @Resources\
│       ├── Variables.inc       # Customization variables
│       ├── Images\             # Button images
│       ├── Scripts\            # Lua scripts
│       └── Cache\              # Album art cache
│
└── @Vault\
    └── SpotifyCredentials.inc  # OAuth credentials (NEVER COMMIT!)
```

### Update Rates

| Component | Default | Adjustable In |
|-----------|---------|---------------|
| Currently Playing | 5 seconds | `Variables.inc` → `UpdateRateNowPlaying` |
| Token Check | 60 seconds | `Variables.inc` → `UpdateRateTokenCheck` |
| UI Redraw | 1 second | `SpotifyNowPlaying.ini` → `[Rainmeter] Update` |

### OAuth Scopes

- `user-read-currently-playing` - Read track info
- `user-modify-playback-state` - Control playback (Premium only)

### API Endpoints

| Endpoint | Purpose | Frequency |
|----------|---------|-----------|
| `/v1/me/player/currently-playing` | Track info | Every 5s |
| `/api/token` | Token refresh | ~Once/hour |
| `/v1/me/player/play` | Resume playback | On demand |
| `/v1/me/player/pause` | Pause playback | On demand |
| `/v1/me/player/next` | Next track | On demand |
| `/v1/me/player/previous` | Previous track | On demand |

---

## 🆘 Getting Help

### For Users

1. Check [Quick Start Guide](QUICK_START.md#troubleshooting)
2. Review [Error Handling Guide](ERROR-HANDLING.md#common-error-scenarios)
3. Enable Debug Mode: `Variables.inc` → `DebugMode=1`
4. Check Rainmeter log: `About → Log`
5. Open GitHub issue with log output (redact tokens!)

### For Developers

1. Review [Project Summary](PROJECT_SUMMARY.md#technical-architecture)
2. Check [Build Guide](RMSKIN_BUILD.md) for packaging
3. Read source code comments (extensively documented)
4. Open GitHub issue or pull request

---

## 📝 Documentation Standards

All documentation follows these principles:

- ✅ **User-focused**: Written for end users, not developers
- ✅ **Comprehensive**: Covers all features and edge cases
- ✅ **Actionable**: Provides clear steps and solutions
- ✅ **Searchable**: Organized by topic with clear headings
- ✅ **Up-to-date**: Updated with each release

**Total Documentation**: ~3,000 lines across 6 files

---

## 🔗 External Resources

- **Rainmeter Documentation**: https://docs.rainmeter.net/
- **Spotify Web API**: https://developer.spotify.com/documentation/web-api
- **OAuth 2.0 Spec**: https://oauth.net/2/
- **Rainmeter Forums**: https://forum.rainmeter.net/

---

**Need something not covered here?** [Open an issue](https://github.com/yourusername/spotify-skin-rainmeter/issues) requesting documentation improvements!
