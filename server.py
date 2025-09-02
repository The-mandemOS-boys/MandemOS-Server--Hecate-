# server.py — Render entrypoint (root of the repo)
import os
import sys
from pathlib import Path

# Add "OK workspaces" to import path (folder has a space)
BASE = Path(__file__).parent
sys.path.append(str(BASE / "OK workspaces"))

# Import your Flask app object from OK workspaces/main.py
from main import app  # noqa: E402

if __name__ == "__main__":
    # Local dev convenience; Render uses gunicorn below
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
