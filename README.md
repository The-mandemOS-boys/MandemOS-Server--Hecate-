# Hecate-v3

This simple project exposes a small voice assistant named **Hecate**. The
assistant can remember short facts, load and run code snippets and even modify
her own source file.

### Self update

Send a message starting with `selfupdate:` followed by Python code and Hecate
will append that snippet to `hecate.py`.

### Mobile access

To use Hecate from another device like an iPhone, run the Flask app so it
listens on your machine's IP address:

```bash
python "OK workspaces/main. py"
```

Then open `http://<your-ip>:8080/index.html` in Safari. The page now sends
requests to `/talk` on the same host, so it works across the network. If the
browser lacks speech recognition, it will prompt you to type your request
instead.
