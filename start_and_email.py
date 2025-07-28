import os
import smtplib
import sys
from pathlib import Path
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS

# Ensure the hecate module can be imported when running from the repo root
ROOT_DIR = Path(__file__).resolve().parent
WORK_DIR = ROOT_DIR / "OK workspaces"
sys.path.insert(0, str(WORK_DIR))

from hecate import Hecate


def send_email_notification(link=None):
    """Send an optional start up email if credentials are provided."""
    if link is None:
        link = os.environ.get("HECATE_LINK", "http://localhost:8080")
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_username = os.environ.get("SMTP_USERNAME")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    to_email = os.environ.get("TO_EMAIL")

    if not all([smtp_server, smtp_username, smtp_password, to_email]):
        print("Email credentials missing. Skipping notification email.")
        return

    msg = MIMEText(
        f"Hecate server is running. Open {link} on your phone to talk to Hecate."
    )
    msg["Subject"] = "Hecate is ready"
    msg["From"] = smtp_username
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print("Notification email sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")


app = Flask(__name__)
CORS(app)

hecate = Hecate()


@app.route("/talk", methods=["POST"])
def talk():
    data = request.json
    user_input = data.get("message", "")
    response = hecate.respond(user_input)
    return jsonify({"reply": response})


if __name__ == "__main__":
    send_email_notification()
    app.run(host="0.0.0.0", port=8080)
