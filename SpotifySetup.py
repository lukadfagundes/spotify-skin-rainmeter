#!/usr/bin/env python3
"""
Spotify OAuth 2.0 Setup Utility for Rainmeter Skin
===================================================

This utility automates the OAuth 2.0 Authorization Code Flow for Spotify Web API.

Flow:
1. User provides Client ID + Client Secret from Spotify Developer Dashboard
2. Utility opens browser to Spotify authorization page
3. User authorizes the app
4. Spotify redirects to local callback server (http://127.0.0.1:8888/callback?code=...)
5. Utility captures authorization code
6. Utility exchanges code for access_token + refresh_token
7. Tokens written to @Vault\SpotifyCredentials.inc

Requirements:
- Python 3.7+
- Libraries: tkinter (built-in), requests, Pillow (for icon), webbrowser (built-in)

Build:
    pip install requests Pillow pyinstaller
    pyinstaller --onefile --windowed --name SpotifySetup SpotifySetup.py

Author: Spotify Rainmeter Skin Project
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
import http.server
import socketserver
import urllib.parse
import threading
import requests
import base64
import os
import time
from pathlib import Path

# Configuration
REDIRECT_URI = "http://127.0.0.1:8888/callback"
CALLBACK_PORT = 8888
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPES = "user-read-currently-playing user-modify-playback-state"

# Global variables for OAuth flow
authorization_code = None
server_thread = None
httpd = None


class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for OAuth callback"""

    def do_GET(self):
        """Handle GET request from Spotify redirect"""
        global authorization_code

        # Parse query parameters
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if 'code' in params:
            authorization_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = """
            <html>
            <head><title>Authorization Successful</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #1DB954;">
                <h1 style="color: white;">✓ Authorization Successful!</h1>
                <p style="color: white; font-size: 18px;">You can close this window and return to the setup utility.</p>
            </body>
            </html>
            """
            self.wfile.write(response.encode())
        elif 'error' in params:
            error = params['error'][0]
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = f"""
            <html>
            <head><title>Authorization Failed</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #E74C3C;">
                <h1 style="color: white;">✗ Authorization Failed</h1>
                <p style="color: white; font-size: 18px;">Error: {error}</p>
                <p style="color: white;">Please close this window and try again.</p>
            </body>
            </html>
            """
            self.wfile.write(response.encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Invalid callback')

    def log_message(self, format, *args):
        """Suppress HTTP server logs"""
        pass


class SpotifySetupApp:
    """Main application class for Spotify OAuth setup"""

    def __init__(self, root):
        self.root = root
        self.root.title("Spotify Rainmeter Skin - OAuth Setup")
        self.root.geometry("650x750")
        self.root.resizable(False, False)

        # Variables
        self.client_id_var = tk.StringVar()
        self.client_secret_var = tk.StringVar()

        # Try to load icon
        self.icon_photo = None
        try:
            # Look for icon in @Resources/Images/ relative to script location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "SpotifyNowPlaying", "@Resources", "Images", "default-album.png")
            if os.path.exists(icon_path):
                from PIL import Image, ImageTk
                icon_img = Image.open(icon_path).resize((40, 40), Image.LANCZOS)
                self.icon_photo = ImageTk.PhotoImage(icon_img)
        except Exception as e:
            # Icon loading is optional, continue without it
            pass

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        """Create UI components"""

        # Header
        header_frame = tk.Frame(self.root, bg="#1DB954", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Icon and title container
        title_container = tk.Frame(header_frame, bg="#1DB954")
        title_container.pack(expand=True)

        # Icon (if loaded)
        if self.icon_photo:
            icon_label = tk.Label(title_container, image=self.icon_photo, bg="#1DB954")
            icon_label.pack(side=tk.LEFT, padx=(0, 10))

        # Title
        title_label = tk.Label(
            title_container,
            text="Spotify Rainmeter Skin Setup" if self.icon_photo else "🎵 Spotify Rainmeter Skin Setup",
            font=("Arial", 18, "bold"),
            bg="#1DB954",
            fg="white"
        )
        title_label.pack(side=tk.LEFT)

        # Main content
        content_frame = tk.Frame(self.root, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Instructions
        instructions = tk.Label(
            content_frame,
            text="Step 1: Create Spotify Developer App",
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        instructions.pack(fill=tk.X, pady=(0, 5))

        instructions_text = tk.Label(
            content_frame,
            text="1. Click 'Open Spotify Developer Dashboard' below\n"
                 "2. Click 'Create App'\n"
                 "3. Fill in:\n"
                 "   • App Name: Rainmeter Spotify (or any name)\n"
                 "   • App Description: Personal Rainmeter skin\n"
                 f"   • Redirect URI: {REDIRECT_URI}\n"
                 "   • Which API/SDKs: Check 'Web API' only\n"
                 "4. Check agreement box → Click 'Save'\n"
                 "5. Click 'Settings' → Copy Client ID and Client Secret below",
            font=("Arial", 9),
            justify=tk.LEFT,
            anchor="w",
            fg="#333"
        )
        instructions_text.pack(fill=tk.X, pady=(0, 15))

        # Dashboard button
        dashboard_btn = tk.Button(
            content_frame,
            text="Open Spotify Developer Dashboard",
            command=self.open_dashboard,
            bg="#1DB954",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            cursor="hand2"
        )
        dashboard_btn.pack(pady=(0, 20))

        # Client ID
        tk.Label(content_frame, text="Client ID:", font=("Arial", 10, "bold")).pack(anchor="w")
        client_id_entry = tk.Entry(content_frame, textvariable=self.client_id_var, font=("Arial", 10), width=60)
        client_id_entry.pack(fill=tk.X, pady=(5, 15))

        # Client Secret
        tk.Label(content_frame, text="Client Secret:", font=("Arial", 10, "bold")).pack(anchor="w")
        client_secret_entry = tk.Entry(content_frame, textvariable=self.client_secret_var, show="*", font=("Arial", 10), width=60)
        client_secret_entry.pack(fill=tk.X, pady=(5, 5))

        # Show/Hide toggle
        show_secret_var = tk.BooleanVar()

        def toggle_secret():
            if show_secret_var.get():
                client_secret_entry.config(show="")
            else:
                client_secret_entry.config(show="*")

        show_secret_check = tk.Checkbutton(
            content_frame,
            text="Show Client Secret",
            variable=show_secret_var,
            command=toggle_secret,
            font=("Arial", 9)
        )
        show_secret_check.pack(anchor="w", pady=(0, 20))

        # Authorize button
        auth_btn = tk.Button(
            content_frame,
            text="Authorize with Spotify",
            command=self.start_oauth_flow,
            bg="#1DB954",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            height=2
        )
        auth_btn.pack(fill=tk.X, pady=(0, 15))

        # Log area
        tk.Label(content_frame, text="Setup Log:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(
            content_frame,
            height=12,
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#F5F5F5"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        """Append message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    def open_dashboard(self):
        """Open Spotify Developer Dashboard in browser"""
        webbrowser.open("https://developer.spotify.com/dashboard")
        self.log("✓ Opened Spotify Developer Dashboard in browser")

    def start_oauth_flow(self):
        """Start OAuth 2.0 authorization flow"""
        global authorization_code, httpd, server_thread

        # Validate inputs
        client_id = self.client_id_var.get().strip()
        client_secret = self.client_secret_var.get().strip()

        if not client_id or not client_secret:
            messagebox.showerror("Error", "Please enter both Client ID and Client Secret")
            return

        self.log("\n" + "="*60)
        self.log("Starting OAuth 2.0 Authorization Flow...")
        self.log("="*60)

        # Step 1: Start local callback server
        try:
            httpd = socketserver.TCPServer(("127.0.0.1", CALLBACK_PORT), CallbackHandler)
            server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            server_thread.start()
            self.log(f"✓ Local callback server started on port {CALLBACK_PORT}")
        except OSError as e:
            messagebox.showerror("Error", f"Port {CALLBACK_PORT} is already in use.\nPlease close any application using this port and try again.")
            self.log(f"✗ Error: Port {CALLBACK_PORT} already in use")
            return

        # Step 2: Build authorization URL
        auth_params = {
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'scope': SCOPES,
            'show_dialog': 'true'  # Always show authorization dialog
        }
        auth_url = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(auth_params)}"

        self.log(f"✓ Authorization URL built")
        self.log(f"   Scopes: {SCOPES}")

        # Step 3: Open browser for authorization
        webbrowser.open(auth_url)
        self.log("✓ Browser opened for authorization")
        self.log("   Waiting for user to authorize...")

        # Step 4: Wait for callback
        authorization_code = None
        timeout = 120  # 2 minutes timeout
        start_time = time.time()

        while authorization_code is None and time.time() - start_time < timeout:
            time.sleep(0.5)
            self.root.update()

        # Shutdown server
        if httpd:
            httpd.shutdown()

        if authorization_code is None:
            messagebox.showerror("Timeout", "Authorization timed out. Please try again.")
            self.log("✗ Authorization timed out (2 minutes)")
            return

        self.log("✓ Authorization code received")

        # Step 5: Exchange authorization code for tokens
        self.log("   Exchanging code for tokens...")
        try:
            # Encode Client ID:Secret in Base64 for Basic auth
            credentials = f"{client_id}:{client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()

            token_data = {
                'grant_type': 'authorization_code',
                'code': authorization_code,
                'redirect_uri': REDIRECT_URI
            }

            token_headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.post(SPOTIFY_TOKEN_URL, data=token_data, headers=token_headers)

            if response.status_code == 200:
                tokens = response.json()
                access_token = tokens.get('access_token')
                refresh_token = tokens.get('refresh_token')
                expires_in = tokens.get('expires_in', 3600)
                expiry_time = int(time.time()) + expires_in

                self.log("✓ Tokens obtained successfully")
                self.log(f"   Access token expires in: {expires_in} seconds ({expires_in // 60} minutes)")

                # Step 6: Write to @Vault
                self.write_credentials(client_id, client_secret, access_token, refresh_token, expiry_time)

            else:
                error_data = response.json()
                error_msg = error_data.get('error_description', response.text)
                messagebox.showerror("Token Exchange Failed", f"Error: {error_msg}")
                self.log(f"✗ Token exchange failed: {error_msg}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Failed to connect to Spotify API:\n{str(e)}")
            self.log(f"✗ Network error: {str(e)}")

    def write_credentials(self, client_id, client_secret, access_token, refresh_token, expiry_time):
        """Write credentials to @Vault\SpotifyCredentials.inc"""

        # Determine Rainmeter Skins path
        rainmeter_path = Path.home() / "Documents" / "Rainmeter" / "Skins"

        if not rainmeter_path.exists():
            messagebox.showerror(
                "Rainmeter Not Found",
                f"Rainmeter Skins folder not found at:\n{rainmeter_path}\n\n"
                "Please install Rainmeter or manually create the @Vault folder."
            )
            self.log(f"✗ Rainmeter path not found: {rainmeter_path}")
            return

        # Create @Vault folder
        vault_path = rainmeter_path / "@Vault"
        vault_path.mkdir(exist_ok=True)
        self.log(f"✓ @Vault folder: {vault_path}")

        # Write credentials file
        creds_file = vault_path / "SpotifyCredentials.inc"

        config_content = f""";==============================================================================
; Spotify API Credentials
;==============================================================================
; Auto-generated by SpotifySetup.exe on {time.strftime('%Y-%m-%d %H:%M:%S')}
;
; SECURITY WARNING:
; - NEVER commit this file to version control
; - NEVER share this file publicly
; - Keep this file in the @Vault folder (excluded from .rmskin distribution)
;==============================================================================

[Variables]
; OAuth 2.0 Credentials
SpotifyClientID={client_id}
SpotifyClientSecret={client_secret}

; Access Token (expires every hour, auto-refreshed by TokenManager.lua)
SpotifyAccessToken={access_token}

; Refresh Token (long-lived, use to get new access tokens)
SpotifyRefreshToken={refresh_token}

; Token Expiry (Unix timestamp, updated on each refresh)
SpotifyTokenExpiry={expiry_time}

;==============================================================================
; DO NOT manually edit SpotifyAccessToken, SpotifyRefreshToken, or SpotifyTokenExpiry
; These values are automatically managed by the skin's TokenManager.lua script
;==============================================================================
"""

        try:
            with open(creds_file, 'w', encoding='utf-8') as f:
                f.write(config_content)

            self.log(f"✓ Credentials written to: {creds_file}")
            self.log("\n" + "="*60)
            self.log("✓✓✓ SETUP COMPLETE! ✓✓✓")
            self.log("="*60)
            self.log("\nNext steps:")
            self.log("1. Open Rainmeter")
            self.log("2. Load the 'SpotifyNowPlaying' skin")
            self.log("3. Enjoy your Spotify integration!")
            self.log("\nNote: Tokens will auto-refresh every ~55 minutes.")

            messagebox.showinfo(
                "Setup Complete!",
                f"Credentials successfully saved to:\n{creds_file}\n\n"
                "You can now load the SpotifyNowPlaying skin in Rainmeter!\n\n"
                "Tokens will automatically refresh, so you never need to "
                "run this setup again (unless you revoke the app in Spotify settings)."
            )

        except Exception as e:
            messagebox.showerror("Write Error", f"Failed to write credentials:\n{str(e)}")
            self.log(f"✗ Failed to write credentials: {str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SpotifySetupApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
