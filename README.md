
# Hecate-Auto

> The daemon who codes, commits, and controls the flame of your GitHub repo.

### Usage
1. Place your GitHub token in `config.json`
2. Run `node hecate-auto.js`
3. It will commit code into your repo automatically

This is the base of a fully interactive coding bot. Expand with AI core or Discord input.

### ChatGPT Integration
Hecate can now send your text prompts to OpenAI's ChatGPT. Set the `OPENAI_API_KEY` environment variable before running the Flask server:

```bash
export OPENAI_API_KEY=your_api_key
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

### Phone Integration
Configure Twilio to let Hecate text or call you. Set these variables:

```bash
export TWILIO_SID=your_account_sid
export TWILIO_AUTH_TOKEN=your_auth_token
export TWILIO_FROM=+15551234567  # your Twilio number
export TWILIO_TO=+15557654321    # destination number
```

Use `sms:your message` to send a text and `call:your message` to receive a phone call with the spoken text.
