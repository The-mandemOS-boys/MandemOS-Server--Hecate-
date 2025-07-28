from flask import Flask, request, jsonify
from flask_cors import CORS
from .hecate import Hecate

# store chat messages in memory
chat_messages = []

app = Flask(__name__)
CORS(app)

# Instantiate Hecate
hecate = Hecate()

@app.route("/talk", methods=["POST"])
def talk():
    data = request.json
    user_input = data.get("message", "")
    response = hecate.respond(user_input)
    return jsonify({"reply": response})


@app.route("/message", methods=["POST"])
def post_message():
    data = request.json or {}
    user = data.get("user", "anonymous")
    text = data.get("message", "")
    if text:
        chat_messages.append({"user": user, "message": text})
        if len(chat_messages) > 100:
            chat_messages.pop(0)
    return jsonify({"status": "ok"})


@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify({"messages": chat_messages})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
