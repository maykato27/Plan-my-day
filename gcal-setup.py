#!/usr/bin/env python3
"""One-time Google Calendar OAuth setup for gcalcli.

Copy .env.example to .env and fill in your credentials before running.
"""

import os
import sys
import pickle
from pathlib import Path

def load_env():
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        sys.exit("Missing .env file. Copy .env.example to .env and fill in your credentials.")
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())

load_env()

sys.path.insert(0, '/Users/mayumikato/Library/Python/3.9/lib/python/site-packages')
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = os.environ["GCAL_CLIENT_ID"]
CLIENT_SECRET = os.environ["GCAL_CLIENT_SECRET"]

client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
    }
}

SCOPES = ["https://www.googleapis.com/auth/calendar"]

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)

print("\n=== Google Calendar Auth ===\n")
print("A browser window should open. If not, copy the URL below into your browser.\n")

credentials = flow.run_local_server(port=0, open_browser=True)

oauth_path = Path.home() / ".gcalcli_oauth"
with open(oauth_path, "wb") as f:
    pickle.dump(credentials, f)

print("\nAuthentication successful! Credentials saved to ~/.gcalcli_oauth")
