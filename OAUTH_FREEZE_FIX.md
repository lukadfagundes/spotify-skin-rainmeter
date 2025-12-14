# SpotifySetup.exe Freeze Fix - 2025-12-14

## Problem Description

The SpotifySetup.exe utility would frequently freeze after the user clicked "Authorize with Spotify" and completed authorization in their browser. The UI would become unresponsive, showing "(Not Responding)" in the title bar, and the authorization would fail to complete.

**User Experience:**
1. User clicks "Authorize with Spotify" button
2. Browser opens correctly
3. User authorizes in browser successfully
4. **Application window freezes** and shows "(Not Responding)"
5. Window becomes unresponsive - cannot be moved or interacted with
6. Authorization eventually times out or never completes

## Root Causes

There were **TWO separate blocking issues**:

### Issue #1: Blocking Wait Loop (Initial Fix)

The freeze was initially caused by a **blocking event loop** in the `start_oauth_flow()` method:

```python
# OLD CODE - PROBLEMATIC
while authorization_code is None and time.time() - start_time < timeout:
    time.sleep(0.5)      # <-- BLOCKS the main thread
    self.root.update()   # <-- Insufficient to prevent freezing
```

**Why This Caused Freezing:**
1. `time.sleep(0.5)` blocks the entire thread
2. Tkinter event loop conflicts when calling `update()` manually
3. No guarantee of UI responsiveness during brief `update()` call
4. Thread safety issues with callback server in daemon thread

### Issue #2: Blocking Network Request (Second Fix)

Even after fixing the wait loop, the UI still froze because the **network request to Spotify's token endpoint ran on the main thread**:

```python
# STILL PROBLEMATIC
def exchange_code_for_tokens(self, auth_code, client_id, client_secret):
    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data, headers=token_headers)
    # ^^ This blocks the UI thread for 1-3 seconds while waiting for response
```

**Why This Caused Freezing:**
1. Network I/O is blocking - waits for server response
2. Can take 1-3 seconds depending on network conditions
3. Runs on main UI thread, freezing all UI updates
4. User sees "(Not Responding)" during network operation

## Solution

### Fix #1: Non-Blocking Callback Waiting

Replaced the blocking `while` loop with **Tkinter's non-blocking `after()` method**:

```python
# NEW CODE - NON-BLOCKING
def start_oauth_flow(self):
    # ... setup code ...

    # Store state for callback checking
    self.oauth_start_time = time.time()
    self.oauth_timeout = 120
    self.client_id = client_id
    self.client_secret = client_secret

    # Schedule first check (non-blocking)
    self.root.after(500, self.check_authorization_callback)

def check_authorization_callback(self):
    """Non-blocking check called via Tkinter's scheduler"""
    global authorization_code, httpd

    # Check if code received
    if authorization_code is not None:
        self.exchange_code_for_tokens(...)
        return

    # Check timeout
    if time.time() - self.oauth_start_time >= self.oauth_timeout:
        # Handle timeout
        return

    # Not ready yet - reschedule check in 500ms
    self.root.after(500, self.check_authorization_callback)
```

### Fix #2: Background Thread for Network Request

Moved the token exchange network request to a **background thread**:

```python
# NEW CODE - RUNS IN BACKGROUND
def exchange_code_for_tokens(self, auth_code, client_id, client_secret):
    """Exchange authorization code (spawns background thread)"""
    self.log("   Exchanging code for tokens...")

    # Run in background thread to prevent UI freeze
    exchange_thread = threading.Thread(
        target=self._do_token_exchange,
        args=(auth_code, client_id, client_secret),
        daemon=True
    )
    exchange_thread.start()

def _do_token_exchange(self, auth_code, client_id, client_secret):
    """Background worker for token exchange"""
    try:
        # Network request happens in background
        response = requests.post(SPOTIFY_TOKEN_URL, data=token_data, headers=token_headers, timeout=10)

        if response.status_code == 200:
            tokens = response.json()
            # ... process tokens ...

            # Schedule UI updates on main thread (thread-safe)
            self.root.after(0, lambda: self.log("✓ Tokens obtained successfully"))
            self.root.after(0, lambda: self.write_credentials(...))
        else:
            # Handle errors on main thread
            self.root.after(0, lambda: messagebox.showerror(...))
    except requests.exceptions.RequestException as e:
        # Handle exceptions on main thread
        self.root.after(0, lambda: self.log(f"✗ Network error: {str(e)}"))
```

### Benefits of This Approach:

1. **Non-blocking callback detection** - Uses `after()` for scheduling
2. **Non-blocking network requests** - Runs in background thread
3. **Thread-safe UI updates** - Uses `after(0, lambda: ...)` to schedule UI updates on main thread
4. **Responsive UI** - Window can be moved, log updates smoothly, no "(Not Responding)"
5. **Timeout protection** - 10-second timeout on network request
6. **Proper error handling** - All errors handled gracefully on main thread

## Testing Recommendations

Before rebuilding the `.exe`, test the fix:

```bash
cd "c:\Users\lukaf\Desktop\Dev Work\spotify-skin-rainmeter"
python SpotifySetup.py
```

**Test scenarios:**
1. ✅ Normal flow - Authorize successfully
2. ✅ Timeout - Wait 2 minutes without authorizing
3. ✅ Port conflict - Run twice simultaneously
4. ✅ Window responsiveness - Move window during authorization
5. ✅ Multiple authorizations - Cancel and retry multiple times

## Rebuild Instructions

After testing, rebuild the executable:

```bash
# Install dependencies (if needed)
pip install requests pyinstaller

# Build
pyinstaller --onefile --windowed --name SpotifySetup SpotifySetup.py

# Copy to skin folder
cp dist/SpotifySetup.exe SpotifyNowPlaying/SpotifySetup.exe
```

## Code Changes Summary

**Files Modified:**
- `SpotifySetup.py`

**Methods Changed:**
- `start_oauth_flow()` - Removed blocking loop, added state variables, schedule callback
- `check_authorization_callback()` - **NEW method**, non-blocking callback checker using `after()`
- `exchange_code_for_tokens()` - **MODIFIED**, now spawns background thread for network request
- `_do_token_exchange()` - **NEW method**, background worker thread for token exchange

**Key Technical Changes:**
1. Replaced `while` loop with `root.after()` recursive scheduling
2. Moved network I/O to background thread
3. All UI updates use `root.after(0, lambda: ...)` for thread safety
4. Added 10-second timeout to network request

**Lines Changed:** ~100 lines refactored

**Backward Compatibility:** 100% - No changes to command-line interface, file outputs, or behavior

## Expected Outcome

After this fix:
- ✅ UI remains responsive during authorization
- ✅ Log updates appear smoothly in real-time
- ✅ Window can be moved/minimized during authorization
- ✅ Authorization completes reliably
- ✅ No freezing or "Not Responding" dialogs

---

**Fix Implemented:** 2025-12-14
**Issue:** UI freezing during OAuth authorization
**Resolution:** Replaced blocking `time.sleep()` loop with non-blocking `after()` scheduler
**Status:** Ready for testing and rebuild