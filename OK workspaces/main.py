from flask import Flask, request, jsonify
from flask_cors import CORS
from hecate import Hecate
import argparse
import subprocess
import sys
import os

app = Flask(__name__)
CORS(app)

# Instantiate Hecate with speech enabled
hecate = Hecate(speak=True)


def run_server():
    """Start the Flask API server."""
    app.run(host="0.0.0.0", port=8080)

@app.route("/talk", methods=["POST"])
def talk():
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
    args = parser.parse_args()

    if args.background:
        # Relaunch this script detached from the current session
        cmd = [sys.executable, os.path.abspath(__file__)]
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
