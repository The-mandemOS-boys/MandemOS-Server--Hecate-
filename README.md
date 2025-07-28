
# Hecate-Auto

> The daemon who codes, commits, and controls the flame of your GitHub repo.

### Usage
1. Create a `config.json` file with your GitHub token and remote URL:
   ```json
   {
     "token": "YOUR_GITHUB_TOKEN",
     "remote": "https://github.com/username/repo.git"
   }
   ```
2. Run `node hecate-auto.js`
3. It will pull the latest changes and then commit and push code to your repo automatically

This is the base of a fully interactive coding bot. Expand with AI core or Discord input.

### Memory Tools
Use `remember:your fact` to store a memory and `recall` to read them back. The command `summarize` or the **Summarize Memory** button in the browser returns a short summary of everything remembered.

### ChatGPT Integration
Hecate can now send your text prompts to OpenAI's ChatGPT. It uses the `gpt-4o`
model for generating replies. By default it looks
for the API key in the `OPENAI_API_KEY` environment variable. If that isn't
present, it will attempt to load a key from a file named `openai_key.txt` in the
repository root.

```bash
# Option 1: environment variable
export OPENAI_API_KEY=your_api_key

# Option 2: place the key in openai_key.txt
echo your_api_key > openai_key.txt

python "OK workspaces/main.py"
```

In the browser interface, type your message into the text box or use the voice button.
Choose a voice from the dropdown labeled "Voice" to hear Hecate reply aloud.
You can also click **Summarize Memory** to get a short summary of all remembered facts.

### Run Locally

1. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the local API server (add `-b` to run in the background):

   ```bash
   python "OK workspaces/main.py"    # foreground
   python "OK workspaces/main.py" -b # background
   ```

3. Open `index.html` in your browser. The page will communicate with the server running on `localhost:8080`.

### Command Line Chat
If you prefer to talk to Hecate directly in your terminal, run the small CLI utility:

```bash
python "OK workspaces/cli.py"
```

Type your message and press Enter to receive a response. Use `quit` or `exit` to leave the session.

### Gmail Integration
Set the following environment variables so Hecate can send and receive email via Gmail:

```bash
export GMAIL_USER=your_address@gmail.com
export GMAIL_PASS=your_app_password
```

Use the commands `email:recipient|subject|body` to send an email and `inbox:n` to read your latest `n` emails.

### File Utilities
Use `retrieve:url|filename` to download a remote file into the `scripts/` folder.
Use `create:filename|content` to create a file with optional content.
Use `move:src|dest` to move or rename files within the `scripts/` folder.

### Location Tagging
Capture your current browser location and email it using the command format `location:lat|lon|recipient`.
The web interface provides buttons to fetch your coordinates and send them via email.

You can configure an emergency contact by setting the environment variable `DISTRESS_EMAIL`.
If your location has been tagged and you type **"Alika in distress"**, Hecate will
email the saved location to this address.

### Running from a zipped archive
You can bundle Hecate into a single executable zip using Python's `zipapp` module. First make sure `__main__.py` is present (it runs the server). Create the archive:

```bash
python -m zipapp . -p '/usr/bin/env python3' -o hecate.pyz
```

Run it with:

```bash
python hecate.pyz
```

This will start the API server directly from the zip file.
