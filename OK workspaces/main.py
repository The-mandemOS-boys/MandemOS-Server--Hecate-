from flask import Flask, request, jsonify
from flask_cors import CORS
from hecate import Hecate
import argparse
import subprocess
import sys
import os

app = Flask(__name__)
CORS(app)

# Hecate instance will be created in __main__ after parsing args
hecate = None


def run_server():
    """Start the Flask API server."""
    app.run(host="0.0.0.0", port=8080)

@app.route("/talk", methods=["POST"])
def talk():
    global hecate
    data = request.json
    user_input = data.get("message", "")
    response = hecate.respond(user_input)
    return jsonify({"reply": response})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hecate API server")
    parser.add_argument(
        "-b",
        "--background",
        action="store_true",
        help="Run the front end API server in the background",
    )
    parser.add_argument(
        "--speak",
        action="store_true",
        help="Enable voice output on the server",
    )
    args = parser.parse_args()

    hecate = Hecate(speak=args.speak)

    if args.background:
        # Relaunch this script detached from the current session
        cmd = [sys.executable, os.path.abspath(__file__)]
        if args.speak:
            cmd.append("--speak")
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        print("Server started in background")
    else:
        run_server()
