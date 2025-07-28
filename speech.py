import subprocess

def speak(text: str):
    """Speak the given text using espeak if available."""
    if not text:
        return
    try:
        subprocess.run(["espeak", text], check=True)
    except Exception:
        pass
