# Hecate-v3

This project exposes a small voice assistant named **Hecate**. The assistant can remember short facts, run user provided code snippets, search the web and even modify its own source file.

## Requirements
Install dependencies with:

```
pip install flask flask-cors requests beautifulsoup4
```

## Running
Start the server using:

```
python3 src/main.py
```

Then open `index.html` in a browser and click the microphone to talk with Hecate.

### Self update
Send a message starting with `selfupdate:` followed by Python code and Hecate will append that snippet to `hecate.py`.
The code is placed inside an `if __name__ == '__main__':` block so it only runs
if the file is executed directly, preventing accidental execution when imported.
