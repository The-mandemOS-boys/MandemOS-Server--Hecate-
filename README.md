# Hecate-v3

This simple project exposes a small voice assistant named **Hecate**. The
assistant can remember short facts, load and run code snippets and even modify
her own source file.

### Flask API

Run `python OK\ workspaces/main.\ py` and use `/talk` to chat with Hecate.
You can now retrieve remembered facts via a `GET /memory` request.

### Self update

Send a message starting with `selfupdate:` followed by Python code and Hecate
will append that snippet to `hecate.py`.
