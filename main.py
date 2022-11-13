import discord
import os
from dccommands import handle

intents = discord.Intents.all()
client = discord.Client(intents=intents)


# Declare which user is logged in as
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


# Await and respond for commands
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('?'):
    await handle.interpret(message)


# Run
client.run(os.environ['GITTO_TOKEN'])
