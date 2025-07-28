# Hecate-v3

This simple project exposes a small voice assistant named **Hecate**. The
assistant can remember short facts, load and run code snippets and even modify
her own source file.

### Self update

Send a message starting with `selfupdate:` followed by Python code and Hecate
will append that snippet to `hecate.py`.

## Deploying on iPhone

You can run Hecate locally on an iPhone using Pythonista 3 or a similar Python environment. A helper script `make_ios_zip.sh` is included to package the project files into a single zip archive.

1. Run `./make_ios_zip.sh` on your computer. This creates `Hecate_ios.zip` with the necessary files.
2. Transfer `Hecate_ios.zip` to your iPhone (AirDrop, iCloud, etc.).
3. Open the zip file in Pythonista and extract the contents.
4. In Pythonista, open `main. py` and run it. This starts the Flask server on port 8080.
5. Open Safari and navigate to `http://localhost:8080` to use the web interface.

The index page uses the Web Speech API, which works best in Safari on iOS 14 or later.
