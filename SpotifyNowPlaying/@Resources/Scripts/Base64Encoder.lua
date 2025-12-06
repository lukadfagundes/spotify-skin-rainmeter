--[[
================================================================================
Base64Encoder.lua - Base64 Encoding for HTTP Basic Authentication
================================================================================

Purpose:
  Encodes Spotify Client ID and Client Secret in Base64 format for
  OAuth 2.0 token refresh requests using HTTP Basic Authentication.

Usage:
  Returns encoded string: Base64(client_id:client_secret)
  Used in Authorization header: "Authorization: Basic <encoded_string>"

Author: Spotify Rainmeter Skin Project
License: MIT
================================================================================
]]--

-- Base64 encoding table
local base64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

--- Encode string to Base64
-- @param data string - Input string to encode
-- @return string - Base64 encoded string
function base64_encode(data)
    return ((data:gsub('.', function(x)
        local r,b='',x:byte()
        for i=8,1,-1 do r=r..(b%2^i-b%2^(i-1)>0 and '1' or '0') end
        return r;
    end)..'0000'):gsub('%d%d%d?%d?%d?%d?', function(x)
        if (#x < 6) then return '' end
        local c=0
        for i=1,6 do c=c+(x:sub(i,i)=='1' and 2^(6-i) or 0) end
        return base64_chars:sub(c+1,c+1)
    end)..({ '', '==', '=' })[#data%3+1])
end

--- Initialize function - Called when skin loads
-- Encodes client credentials and returns the encoded string
function Initialize()
    -- Get credentials from Rainmeter variables
    local clientID = SKIN:GetVariable('SpotifyClientID', '')
    local clientSecret = SKIN:GetVariable('SpotifyClientSecret', '')

    if clientID == '' or clientSecret == '' then
        SKIN:Bang('[!Log "Base64Encoder: Missing client credentials!" Warning]')
        return ''
    end

    -- Combine as "client_id:client_secret"
    local credentials = clientID .. ':' .. clientSecret

    -- Encode to Base64
    local encoded = base64_encode(credentials)

    SKIN:Bang('[!Log "Base64Encoder: Credentials encoded successfully" Debug]')

    return encoded
end

--- Update function - Returns the encoded string
-- This allows the measure to be used dynamically
function Update()
    return Initialize()
end
