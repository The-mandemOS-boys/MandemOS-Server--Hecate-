
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
3. It will commit and push code to your repo automatically

This is the base of a fully interactive coding bot. Expand with AI core or Discord input.

### ChatGPT Integration
Hecate can now send your text prompts to OpenAI's ChatGPT. By default it looks
for the API key in the `OPENAI_API_KEY` environment variable. If that isn't
present, it will attempt to load a key from a file named `openai_key.txt` in the
repository root.

```bash
# Option 1: environment variable
export OPENAI_API_KEY=your_api_key

# Option 2: place the key in openai_key.txt
echo your_api_key > openai_key.txt

python "OK workspaces/main. py"
```

In the browser interface, type your message into the text box or use the voice button.

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
Use `delete:filename` to remove a file from the `scripts/` folder.

### Location Tagging
Capture your current browser location and email it using the command format `location:lat|lon|recipient`.
The web interface provides buttons to fetch your coordinates and send them via email.
