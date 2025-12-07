--[[
================================================================================
TokenManager.lua - Spotify OAuth 2.0 Token Refresh Manager
================================================================================

Purpose:
  Automatically refreshes Spotify access tokens before expiry to maintain
  uninterrupted API access.

Flow:
  1. Initialize() - Load token expiry from @Vault\SpotifyCredentials.inc
  2. Update() - Called every 60s to check expiry
  3. RefreshToken() - Triggers WebParser measure to request new token
  4. OnTokenRefreshFinish() - Parses response and updates @Vault file

Token Lifecycle:
  - Access tokens expire after 3600 seconds (1 hour)
  - Refresh occurs when <300 seconds (5 minutes) remain
  - Refresh tokens are long-lived (unless manually revoked)

Dependencies:
  - MeasureTokenRefresh: WebParser measure that calls Spotify token endpoint
  - @Vault\SpotifyCredentials.inc: INI file with credentials

Author: Spotify Rainmeter Skin Project
License: MIT
================================================================================
]]--

-- Configuration
local REFRESH_THRESHOLD = 300  -- Refresh when <5 minutes remain (seconds)
local CHECK_INTERVAL = 60      -- Check expiry every 60 seconds

-- Global state
local tokenExpiry = 0          -- Unix timestamp of token expiry
local isRefreshing = false     -- Prevent concurrent refresh attempts
local vaultPath = ""           -- Path to SpotifyCredentials.inc
local lastCheckTime = 0        -- Timestamp of last expiry check

-- Logging levels
local LOG_DEBUG = true         -- Set to true for verbose logging
local LOG_INFO = true          -- Info-level logging

--[[
================================================================================
HELPER FUNCTIONS
================================================================================
]]--

--- Log message to Rainmeter log
-- @param level string - Log level (Notice, Warning, Error, Debug)
-- @param message string - Message to log
function Log(level, message)
    if level == "Debug" and not LOG_DEBUG then
        return
    end

    -- Escape quotes in message to prevent bang parsing errors
    local escapedMessage = message:gsub('"', '""')
    SKIN:Bang(string.format('[!Log "[TokenManager] %s" %s]', escapedMessage, level))
end

--- Get current Unix timestamp
-- @return number - Current time in seconds since epoch
function GetCurrentTime()
    return os.time()
end

--- Read entire file content
-- @param filepath string - Absolute path to file
-- @return string - File content, or nil on error
function ReadFile(filepath)
    local file = io.open(filepath, 'r')
    if not file then
        Log("Error", string.format("Cannot open file: %s", filepath))
        return nil
    end

    local content = file:read('*all')
    file:close()
    return content
end

--- Write content to file
-- @param filepath string - Absolute path to file
-- @param content string - Content to write
-- @return boolean - Success status
function WriteFile(filepath, content)
    local file = io.open(filepath, 'w')
    if not file then
        Log("Error", string.format("Cannot write to file: %s", filepath))
        return false
    end

    file:write(content)
    file:close()
    return true
end

--- Update a specific variable in the @Vault credentials file
-- @param varName string - Variable name (e.g., "SpotifyAccessToken")
-- @param newValue string - New value
-- @return boolean - Success status
function UpdateVaultVariable(varName, newValue)
    Log("Debug", string.format("UpdateVaultVariable called: varName=%s, newValue length=%d", varName, string.len(newValue)))

    local content = ReadFile(vaultPath)
    if not content then
        Log("Error", "Failed to read @Vault file")
        return false
    end

    Log("Debug", string.format("Read @Vault file successfully (length: %d bytes)", string.len(content)))

    -- Pattern: Match variable assignment (handles = signs with optional spaces)
    local pattern = string.format("(%s%s*=%s*)([^\n\r]*)", varName, "%s", "%s")
    local updated = content:gsub(pattern, "%1" .. newValue)

    if updated == content then
        Log("Warning", string.format("Variable %s not found in @Vault file", varName))
        return false
    end

    Log("Debug", string.format("Variable %s matched and replaced in content", varName))

    local writeResult = WriteFile(vaultPath, updated)
    Log("Debug", string.format("WriteFile result for %s: %s", varName, tostring(writeResult)))
    return writeResult
end

--[[
================================================================================
CORE FUNCTIONS (Called by Rainmeter)
================================================================================
]]--

--- Initialize function - Called when skin loads
-- Loads token expiry from @Vault and determines Vault path
function Initialize()
    Log("Notice", "TokenManager initializing...")

    -- Get @Vault path from Rainmeter variables
    local skinsPath = SKIN:GetVariable("SKINSPATH")

    -- @Vault is at SKINSPATH\@Vault\
    vaultPath = skinsPath .. "@Vault\\SpotifyCredentials.inc"

    Log("Notice", string.format("Vault path: %s", vaultPath))

    -- Verify vault file exists and is readable
    local testRead = ReadFile(vaultPath)
    if testRead then
        Log("Notice", string.format("Vault file verified (size: %d bytes)", string.len(testRead)))
    else
        Log("Error", "Cannot read vault file at initialization!")
    end

    -- Load initial token expiry
    local expiryStr = SKIN:GetVariable("SpotifyTokenExpiry", "0")
    tokenExpiry = tonumber(expiryStr) or 0

    local currentTime = GetCurrentTime()
    local timeRemaining = tokenExpiry - currentTime

    if timeRemaining <= 0 then
        Log("Warning", "Token is already expired! Manual setup required via SpotifySetup.exe")
    elseif timeRemaining < REFRESH_THRESHOLD then
        Log("Notice", string.format("Token expires in %d seconds - will refresh immediately", timeRemaining))
    else
        Log("Notice", string.format("Token valid for %d seconds (%d minutes)", timeRemaining, math.floor(timeRemaining / 60)))
    end

    lastCheckTime = currentTime
    Log("Notice", "TokenManager initialized successfully")
end

--- Update function - Called periodically (every 60 seconds)
-- Checks token expiry and triggers refresh if needed
function Update()
    local currentTime = GetCurrentTime()

    -- Reload token expiry from skin variables (in case it was updated externally)
    local expiryStr = SKIN:GetVariable("SpotifyTokenExpiry", "0")
    tokenExpiry = tonumber(expiryStr) or 0

    local timeRemaining = tokenExpiry - currentTime

    Log("Debug", string.format("Token check: %d seconds remaining", timeRemaining))

    -- Check if refresh is needed
    if timeRemaining < REFRESH_THRESHOLD and not isRefreshing then
        if timeRemaining <= 0 then
            Log("Warning", "Token expired! Attempting refresh...")
        else
            Log("Notice", string.format("Token expires in %d seconds - triggering refresh", timeRemaining))
        end

        RefreshToken()
    end

    lastCheckTime = currentTime

    -- Return time remaining for optional display in skin
    return timeRemaining
end

--- Trigger token refresh via WebParser measure
function RefreshToken()
    Log("Debug", "=== RefreshToken() CALLED ===")

    if isRefreshing then
        Log("Debug", "Refresh already in progress, skipping")
        return
    end

    isRefreshing = true
    Log("Notice", "Initiating token refresh...")

    -- Force update of MeasureAuthHeader to ensure Base64 value is fresh
    SKIN:Bang('!UpdateMeasure', 'MeasureAuthHeader')

    -- Debug: Log the auth header value
    local authHeaderMeasure = SKIN:GetMeasure('MeasureAuthHeader')
    if authHeaderMeasure then
        local authValue = authHeaderMeasure:GetStringValue()
        Log("Debug", string.format("Auth header Base64 value: %s", authValue or "EMPTY"))
    else
        Log("Warning", "Could not get MeasureAuthHeader measure!")
    end

    -- Debug: Log the variable value that will be used in curl header
    local authVarValue = SKIN:GetVariable('AuthHeaderBase64', '')
    Log("Debug", string.format("AuthHeaderBase64 variable value: %s", authVarValue or "EMPTY"))

    -- Debug: Log the refresh token (first 20 chars only)
    local refreshToken = SKIN:GetVariable('SpotifyRefreshToken', '')
    if refreshToken and refreshToken ~= '' then
        Log("Debug", string.format("Refresh token: %s... (length: %d)", string.sub(refreshToken, 1, 20), string.len(refreshToken)))
    else
        Log("Warning", "Refresh token is EMPTY!")
        isRefreshing = false
        return
    end

    -- Trigger the RunCommand curl measure that handles OAuth refresh
    -- Note: POST data is directly embedded in curl Parameter using Rainmeter variables
    Log("Debug", "Triggering MeasureTokenRefresh...")
    SKIN:Bang('!CommandMeasure', 'MeasureTokenRefresh', 'Run')
    Log("Debug", "=== RefreshToken() COMPLETE ===")
end

--[[
================================================================================
CALLBACK FUNCTIONS (Called by TokenRefreshParser.lua)
================================================================================
]]--

--- Callback when token refresh completes successfully
-- Parses JSON response and updates @Vault file
-- @param expiresIn string - Token expiry time in seconds (passed by TokenRefreshParser.lua)
function OnTokenRefreshFinish(expiresIn)
    Log("Notice", "Token refresh response received")

    -- Get token values from variables (already set by TokenRefreshParser.lua)
    local accessToken = SKIN:GetVariable("SpotifyAccessToken")
    local refreshToken = SKIN:GetVariable("SpotifyRefreshToken")

    -- Validate response
    if not accessToken or accessToken == "" then
        Log("Error", "Token refresh failed - no access token received")
        isRefreshing = false
        return
    end

    -- expiresIn is now passed as parameter from TokenRefreshParser
    local expiresIn = tonumber(expiresIn) or 3600
    local currentTime = GetCurrentTime()
    local newExpiry = currentTime + expiresIn

    Log("Notice", string.format("New token received (expires in %d seconds)", expiresIn))

    -- Update @Vault file with new tokens
    local accessTokenSuccess = UpdateVaultVariable("SpotifyAccessToken", accessToken)
    Log("Debug", string.format("SpotifyAccessToken write result: %s", tostring(accessTokenSuccess)))

    -- Refresh token might not be returned if still valid (Spotify behavior)
    -- Note: Don't fail if refresh token write fails - it's optional
    if refreshToken and refreshToken ~= "" then
        Log("Debug", string.format("Attempting to write SpotifyRefreshToken (length: %d)", string.len(refreshToken)))
        local refreshTokenSuccess = UpdateVaultVariable("SpotifyRefreshToken", refreshToken)
        Log("Debug", string.format("SpotifyRefreshToken write result: %s", tostring(refreshTokenSuccess)))
    else
        Log("Debug", "Refresh token not returned (using existing)")
    end

    -- Always write the new expiry time (this is critical)
    Log("Debug", string.format("Attempting to write SpotifyTokenExpiry: %s", tostring(newExpiry)))
    local expirySuccess = UpdateVaultVariable("SpotifyTokenExpiry", tostring(newExpiry))
    Log("Debug", string.format("SpotifyTokenExpiry write result: %s", tostring(expirySuccess)))

    -- Success if we wrote both access token and expiry (refresh token is optional)
    local success = accessTokenSuccess and expirySuccess

    if success then
        tokenExpiry = newExpiry
        Log("Notice", "Token refresh complete - credentials saved to @Vault")

        -- Trigger skin refresh to reload variables from @Vault
        SKIN:Bang('!Refresh')
    else
        Log("Error", "Failed to write updated tokens to @Vault")
    end

    isRefreshing = false
end

--- Callback when token refresh fails
-- @param errorMsg string - Error message
function OnTokenRefreshError(errorMsg)
    Log("Error", string.format("Token refresh failed: %s", errorMsg or "Unknown error"))

    -- Reset state to allow retry
    isRefreshing = false

    -- Log troubleshooting steps
    Log("Warning", "Troubleshooting: Check @Vault\\SpotifyCredentials.inc for valid refresh_token")
    Log("Warning", "If issues persist, re-run SpotifySetup.exe to re-authorize")
end

--[[
================================================================================
UTILITY FUNCTIONS (Accessible from skin measures)
================================================================================
]]--

--- Get formatted time remaining string
-- @return string - Human-readable time remaining (e.g., "45 minutes")
function GetTimeRemainingString()
    local currentTime = GetCurrentTime()
    local timeRemaining = tokenExpiry - currentTime

    if timeRemaining <= 0 then
        return "Expired"
    elseif timeRemaining < 60 then
        return string.format("%d seconds", timeRemaining)
    elseif timeRemaining < 3600 then
        return string.format("%d minutes", math.floor(timeRemaining / 60))
    else
        return string.format("%d hours", math.floor(timeRemaining / 3600))
    end
end

--- Force immediate token refresh (for manual triggering)
function ForceRefresh()
    Log("Notice", "Manual token refresh requested")
    isRefreshing = false  -- Reset state in case stuck
    RefreshToken()
end

--- Get current refresh status
-- @return string - Current status ("Active", "Refreshing", "Expired")
function GetStatus()
    if isRefreshing then
        return "Refreshing"
    elseif tokenExpiry - GetCurrentTime() <= 0 then
        return "Expired"
    else
        return "Active"
    end
end
