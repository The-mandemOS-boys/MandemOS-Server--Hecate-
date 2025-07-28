# Hecate-v3

This project contains a simple voice assistant named Hecate. A small Flask
server provides an endpoint for the web interface in `index.html`. The assistant
can also run as a Discord bot.

## Requirements
- Python 3.8+
- `flask`, `flask_cors`, `requests`, `beautifulsoup4`, and `discord`

## Running the Web Server
```bash
python main.py
```
Open `index.html` in your browser to interact with Hecate.

## Running the Discord Bot
Set the `DISCORD_TOKEN` environment variable with your bot token and run:
```bash
python discord_bot.py
```
