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
SkinHeight=400
SkinCornerRadius=8

AlbumArtSize=200
AlbumArtX=100
AlbumArtY=20

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

TrackNameX=20
TrackNameY=235
TrackNameW=360
TrackNameH=30

ArtistNameX=20
ArtistNameY=265
ArtistNameW=360
ArtistNameH=25

AlbumNameX=20
AlbumNameY=290
AlbumNameW=360
AlbumNameH=25

ProgressBarX=20
ProgressBarY=325
ProgressBarW=360
ProgressBarH=6

ControlButtonsY=345
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
