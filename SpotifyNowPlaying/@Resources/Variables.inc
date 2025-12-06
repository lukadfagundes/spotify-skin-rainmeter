;==============================================================================
; Variables.inc - Skin Configuration Variables
;==============================================================================
; This file contains UI customization variables for the Spotify Now Playing skin.
; Users can edit these values to customize appearance without modifying the main skin.
;==============================================================================

[Variables]

;------------------------------------------------------------------------------
; UI Dimensions
;------------------------------------------------------------------------------

SkinWidth=400
SkinHeight=250
SkinCornerRadius=8

AlbumArtSize=150
AlbumArtX=10
AlbumArtY=10

;------------------------------------------------------------------------------
; Colors (RGBA format)
;------------------------------------------------------------------------------

; Background
ColorBackground=20,20,20,230
ColorBorder=29,185,84,255

; Text
ColorTrackName=255,255,255,255
ColorArtistName=180,180,180,255
ColorAlbumName=150,150,150,255
ColorTimeText=150,150,150,255

; Progress Bar
ColorProgressBarBG=60,60,60,255
ColorProgressBarFill=29,185,84,255

; Spotify Brand Green (Primary)
ColorSpotifyGreen=29,185,84,255

;------------------------------------------------------------------------------
; Fonts
;------------------------------------------------------------------------------

FontFace=Segoe UI
FontSizeTrack=14
FontSizeArtist=11
FontSizeAlbum=10
FontSizeTime=9
FontWeightTrack=600
FontWeightNormal=400

;------------------------------------------------------------------------------
; Layout Positions
;------------------------------------------------------------------------------

TrackNameX=170
TrackNameY=20
TrackNameW=220
TrackNameH=30

ArtistNameX=170
ArtistNameY=55
ArtistNameW=220
ArtistNameH=25

AlbumNameX=170
AlbumNameY=80
AlbumNameW=220
AlbumNameH=25

ProgressBarX=170
ProgressBarY=120
ProgressBarW=220
ProgressBarH=6

ControlButtonsY=170
ControlButtonSize=32
ControlButtonSpacing=10

;------------------------------------------------------------------------------
; Update Rates (seconds)
;------------------------------------------------------------------------------

; How often to check for currently playing track (seconds)
UpdateRateNowPlaying=5

; How often to check token expiry (seconds)
UpdateRateTokenCheck=60

;------------------------------------------------------------------------------
; Cache Directory
;------------------------------------------------------------------------------

CacheDir=#@#Cache\

;------------------------------------------------------------------------------
; Debug Mode
;------------------------------------------------------------------------------

; Set to 1 to show debug information (token status, API errors)
; Set to 0 to hide debug info for production
DebugMode=1
