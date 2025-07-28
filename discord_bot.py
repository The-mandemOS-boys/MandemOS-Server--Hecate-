import os
import discord
from hecate import Hecate

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise SystemExit("DISCORD_TOKEN environment variable not set")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
hecate = Hecate()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    reply = hecate.respond(message.content)
    await message.channel.send(reply)

bot.run(TOKEN)
