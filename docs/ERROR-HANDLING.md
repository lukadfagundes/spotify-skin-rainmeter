# Error Handling Guide - Spotify Rainmeter Skin

## Overview

This document describes the error handling mechanisms implemented in the Spotify Rainmeter skin and provides troubleshooting guidance.

## Error Handling Layers

### 1. Token Management Errors

**Location:** `TokenManager.lua` + `MeasureTokenRefresh` in `SpotifyNowPlaying.ini`

**Handled Errors:**

| Error Type | Trigger | Handler | User Impact |
|------------|---------|---------|-------------|
| Connection Failed | Network unavailable during token refresh | `OnConnectErrorAction` → `OnTokenRefreshError('Connection failed')` | Logs error, allows retry on next check |
| Invalid Response | Malformed JSON from Spotify | `OnRegExpErrorAction` → `OnTokenRefreshError('Invalid response')` | Logs error, suggests re-running SpotifySetup.exe |
| Download Failed | HTTP error (401, 403, 500, etc.) | `OnDownloadErrorAction` → `OnTokenRefreshError('Download failed')` | Logs error, check credentials |
| Token Expired | Current time > expiry timestamp | `Update()` in TokenManager | Automatically triggers refresh |
| Missing Credentials | Empty client_id/client_secret | `Initialize()` validation | Logs warning, instructs to run SpotifySetup.exe |

**Recovery Actions:**
- Automatic retry on next `Update()` call (60 seconds)
- Logs provide troubleshooting guidance
- Persistent failures require user intervention (re-run SpotifySetup.exe)

**Error Logging:**
```lua
Log("Error", "Token refresh failed: Connection failed")
Log("Warning", "Troubleshooting: Check @Vault\\SpotifyCredentials.inc for valid refresh_token")
Log("Warning", "If issues persist, re-run SpotifySetup.exe to re-authorize")
```

---

### 2. Spotify API Errors (Currently Playing)

**Location:** `MeasureNowPlaying` in `SpotifyNowPlaying.ini`

**Handled Errors:**

| Error Type | Trigger | Handler | Display Fallback |
|------------|---------|---------|------------------|
| Not Playing | No active Spotify playback | `OnConnectErrorAction` | "Not Playing" |
| No Track Info | API returns 204 (No Content) | `OnRegExpErrorAction` | "No Track Info" |
| API Error | Rate limiting, server error, auth error | `OnDownloadErrorAction` | "API Error" |
| Network Error | Internet disconnected | `OnConnectErrorAction` | "Not Playing" |
| 401 Unauthorized | Token expired/invalid | Auto-refresh triggered | Temporary "API Error", resolves after refresh |

**Implementation:**
```ini
[MeasureNowPlaying]
; ...
OnConnectErrorAction=[!SetOption MeterTrackName Text "Not Playing"][!UpdateMeter MeterTrackName][!Redraw]
OnRegExpErrorAction=[!SetOption MeterTrackName Text "No Track Info"][!UpdateMeter MeterTrackName][!Redraw]
OnDownloadErrorAction=[!SetOption MeterTrackName Text "API Error"][!UpdateMeter MeterTrackName][!Redraw]
```

**User Experience:**
- Non-intrusive error messages displayed in track name field
- Skin continues polling every 1 second
- Automatically recovers when Spotify resumes playback

---

### 3. Album Art Download Errors

**Location:** `MeasureAlbumArt` in `SpotifyNowPlaying.ini`

**Handled Errors:**

| Error Type | Trigger | Handler | Fallback Image |
|------------|---------|---------|----------------|
| Empty URL | No album art available for track | `IfMatch=^$` | `default-album.png` |
| Download Failed | Image URL unreachable | `IfNotMatchAction` | `default-album.png` |
| Invalid Image | Corrupted download | Rainmeter's internal handling | Previous cached image or default |

**Implementation:**
```ini
[MeasureAlbumArt]
; ...
IfMatch=^$
IfNotMatchAction=[!SetOption MeterAlbumArt ImageName "#@#Images\default-album.png"]
```

**Caching Behavior:**
- Successful downloads cached in `DownloadFile\` (single file: current-album.jpg)
- Cache persists across skin reloads
- Failed downloads fall back to default image immediately

---

### 4. Playback Control Errors

**Location:** `MeasurePlayPause`, `MeasurePause`, `MeasureNext`, `MeasurePrevious`

**Handled Errors:**

| Error Type | Trigger | Current Handling | Improvement Opportunity |
|------------|---------|------------------|------------------------|
| No Active Device | User clicks control but no Spotify client active | Silent failure | Could show tooltip "No active device" |
| Premium Required | Free user clicks control | HTTP 403 from Spotify | Could show tooltip "Spotify Premium required" |
| Rate Limiting | Rapid button clicks | Spotify responds with 429 | Natural backoff from UpdateRate=-1 |

**Implementation:**
```ini
[MeasureNext]
; ...
FinishAction=[!Delay 500][!CommandMeasure MeasureNowPlaying "Update"]
```

**Design Decision:**
- Controls fail silently to avoid intrusive error popups
- Delay + immediate refresh ensures UI updates after control actions
- Spotify API provides natural error responses (e.g., ignoring next/previous when at playlist boundaries)

---

### 5. File I/O Errors

**Location:** `TokenManager.lua` - `ReadFile()`, `WriteFile()`, `UpdateVaultVariable()`

**Handled Errors:**

| Error Type | Trigger | Handler | Recovery |
|------------|---------|---------|----------|
| @Vault File Missing | SpotifyCredentials.inc not found | `ReadFile()` returns `nil` | Log error "Cannot open file", instruct to run SpotifySetup.exe |
| @Vault Write Failure | Permissions issue, disk full | `WriteFile()` returns `false` | Log error "Cannot write to file", token refresh aborted |
| Variable Not Found | Corrupted .inc file structure | `UpdateVaultVariable()` logs warning | Pattern match fails, returns false |

**Implementation:**
```lua
function ReadFile(filepath)
    local file = io.open(filepath, 'r')
    if not file then
        Log("Error", string.format("Cannot open file: %s", filepath))
        return nil
    end
    -- ...
end
```

**Error Messaging:**
- Detailed log messages with file paths
- Guidance for user action (e.g., "Run SpotifySetup.exe")

---

## Error Recovery Strategies

### Automatic Recovery

1. **Token Expiry:**
   - **Detection:** `Update()` checks `tokenExpiry - currentTime < 300`
   - **Action:** Triggers `RefreshToken()` automatically
   - **Retry:** Every 60 seconds until successful

2. **Transient Network Errors:**
   - **Detection:** `OnConnectErrorAction` in WebParser measures
   - **Action:** Log error, wait for next update cycle
   - **Retry:** Automatic via `UpdateRate` (1s for NowPlaying, 60s for TokenManager)

3. **API Rate Limiting:**
   - **Detection:** Spotify returns HTTP 429
   - **Action:** Natural backoff from update intervals
   - **Retry:** Next scheduled update

### Manual Recovery

**Required When:**
- Refresh token revoked/expired (user revoked app in Spotify dashboard)
- Credentials corrupted/deleted
- OAuth scope changed

**User Action:**
1. Run `SpotifySetup.exe`
2. Re-authorize with Spotify
3. New tokens written to @Vault
4. Reload skin: `[!Refresh]`

---

## Common Error Scenarios

### Scenario 1: "API Error" Displayed

**Possible Causes:**
- Token expired (should auto-fix within 60 seconds)
- Invalid credentials in @Vault
- Spotify API outage
- Network disconnected

**Troubleshooting:**
1. Check Rainmeter log for details: `About → Log`
2. Wait 60 seconds for automatic token refresh
3. Verify internet connection
4. Check Spotify API status: https://status.spotify.com/
5. If persistent: Re-run SpotifySetup.exe

---

### Scenario 2: "Not Playing" Despite Active Playback

**Possible Causes:**
- Spotify client not streaming (local files only)
- Spotify in private session mode
- Incorrect OAuth scopes (missing `user-read-currently-playing`)

**Troubleshooting:**
1. Verify Spotify is streaming from Spotify catalog (not local files)
2. Disable private session
3. Check @Vault credentials include correct scope
4. Re-run SpotifySetup.exe to ensure correct scopes

---

### Scenario 3: Token Refresh Fails Repeatedly

**Possible Causes:**
- Refresh token revoked by user
- Refresh token expired (extremely rare - usually long-lived)
- Client secret changed in Spotify dashboard

**Troubleshooting:**
1. Check Rainmeter log: Look for "Token refresh failed" messages
2. Verify credentials in @Vault\SpotifyCredentials.inc
3. Go to https://www.spotify.com/account/apps/ and check authorized apps
4. Re-run SpotifySetup.exe to re-authorize

---

### Scenario 4: Controls Don't Work

**Possible Causes:**
- No active Spotify device
- Spotify Premium required (playback control not available for Free users)
- Rate limiting from Spotify API

**Troubleshooting:**
1. Ensure Spotify app is open and playing on ANY device
2. Verify Spotify Premium subscription status
3. Wait a few seconds between rapid button clicks
4. Check skin includes `user-modify-playback-state` scope

---

## Logging and Debugging

### Enable Debug Logging

**In Variables.inc:**
```ini
DebugMode=1
```

**In TokenManager.lua:**
```lua
local LOG_DEBUG = true  -- Line 23
```

### Log Locations

**Rainmeter Log:**
- Open: `Rainmeter → About → Log`
- Filters: `[TokenManager]`, `[WebParser]`

**Expected Log Messages:**

**Normal Operation:**
```
Info: TokenManager initialized successfully
Info: Token valid for 3423 seconds (57 minutes)
Info: Token expires in 287 seconds - triggering refresh
Info: New token received (expires in 3600 seconds)
Info: Token refresh complete - credentials saved to @Vault
```

**Error States:**
```
Error: Token refresh failed: Connection failed
Warning: Troubleshooting: Check @Vault\SpotifyCredentials.inc for valid refresh_token
Error: Cannot open file: C:\Users\...\@Vault\SpotifyCredentials.inc
```

---

## Error Prevention

### Setup Validation

**SpotifySetup.exe includes:**
- Client ID/Secret validation before authorization
- Port availability check (8888)
- Rainmeter installation detection
- @Vault folder creation with proper permissions

### Runtime Safeguards

**TokenManager.lua:**
- Prevents concurrent refresh attempts (`isRefreshing` flag)
- Validates token values before writing to @Vault
- Graceful degradation on file I/O errors

**SpotifyNowPlaying.ini:**
- All WebParser measures include error callbacks
- Fallback values for missing data
- Default album art for failed downloads
- DynamicVariables for safe interpolation

---

## Future Enhancements

### Potential Improvements

1. **User-Facing Error UI:**
   - Add error meter showing specific issues (e.g., "Premium Required")
   - Tooltip hints on control buttons

2. **Advanced Retry Logic:**
   - Exponential backoff for repeated failures
   - Separate retry counters for different error types

3. **Health Check Measure:**
   - Periodic validation of @Vault file integrity
   - Proactive token validation before expiry

4. **Offline Mode:**
   - Cache last known track info for display when offline
   - Visual indicator for offline state

---

## Support

**For Issues:**
1. Check this guide for known scenarios
2. Review Rainmeter log with `DebugMode=1`
3. Verify @Vault\SpotifyCredentials.inc exists and contains valid tokens
4. Re-run SpotifySetup.exe as first troubleshooting step
5. Report persistent issues with log output

**Security Note:**
When reporting errors, **NEVER** share:
- SpotifyCredentials.inc contents
- Access tokens or refresh tokens
- Client secrets

Share only:
- Error messages from Rainmeter log (redact tokens)
- Steps to reproduce
- Spotify account type (Free/Premium)
