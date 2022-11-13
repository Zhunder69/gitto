import discord
import os
from dccommands import handle

intents = discord.Intents.all()
client = discord.Client(intents=intents)


# imprimir el nombre de usuario del bot que inicio sesion
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


# reaccionar a los comandos de los usuarios
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('?'):
    await handle.interpret(message)


# iniciar el bot
client.run(os.environ['TOKEN'])