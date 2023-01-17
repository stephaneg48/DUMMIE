import os
import random
import discord
import string
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv(dotenv_path='lib/.env')

# access variables
token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')  # the one to look for
me = os.getenv('ME')
owner = os.getenv('OWNER')

# greetings
greetings =  {
    "creator" : "Hello, creator!",
     "owner" : "Hello, Xarth!",
     "member" : [
         "Hi, friend!",
         "I think we're going to do great, friend.",
         "High-five!",
         "I just polished my grapple :robot:",
         "Hey, that's me!"
                ]
             }

# commands
list_of_commands =  {
    "help" : "DUMMIE (me!) sends this list of commands to you (not a DUMMIE!)",
    "wowmods" : "Sends a list of some useful World of Warcraft mods to the current channel"
                    }

"""WoW-Related"""
mods =  {
        "Silver Dragon (tracks rares)" : "https://www.curseforge.com/wow/addons/silver-dragon",
        "Bagnon (bag interface improvements)" : "https://www.curseforge.com/wow/addons/bagnon",
        "BtWQuests (quest journal)" : "https://www.curseforge.com/wow/addons/btw-quests",
        "Auctionator (auction improvements)" : "https://www.curseforge.com/wow/addons/auctionator",
        "World Quest Tracker" : "https://www.curseforge.com/wow/addons/world-quest-tracker",
        "HealBot Continued (healer QoL)" : "https://www.curseforge.com/wow/addons/heal-bot-continued",
        "Deadly Boss Mods (raid/dungeon warnings on HUD, separate installs)" : "https://www.curseforge.com/wow/addons/deadly-boss-mods",
        "Scrap (instantly sell grey junk items)" : "https://www.curseforge.com/wow/addons/scrap",
        "Peggle Classic" : "https://www.curseforge.com/wow/addons/peggle-classic",
        "Clique (click-to-cast)" : "https://www.curseforge.com/wow/addons/clique"
        }

"""END WoW-Related"""

def_intents = discord.Intents.default()  # required as of version 2
def_intents.members = True               # MUST ALSO enable in Dev Portal -> Bot -> Gateway Intents
def_intents.message_content = True       # ditto
bot = commands.Bot(
    command_prefix='!d ',
    case_insensitive=True,
    help_command=None,
    intents=def_intents)
@bot.event
async def on_ready():
    current_guild = discord.utils.get(bot.guilds, name=guild)

    print(
        f'{bot.user} has connected to Discord!\n'
        f'{bot.user} is currently connected to:\n'
        f'{current_guild.name} (id: {current_guild.id})'
    )

    print('Guild members: ')
    for member in current_guild.members:
        print(member.name)

    try:
        syncing = await bot.tree.sync()
        print(f"Synced {len(syncing)} command(s)")
    except Exception as e:
        print(e)

# EVENTS
@bot.event
async def on_message(message):
    if message.author == bot.user: # check if the bot sent the message itself
        return

    msg = message.content.lower()
    split = msg.split()
    words = []
    for word in split:
        words.append(word.strip(string.punctuation))

    if ("hi" in words or "hey" in words or "hello" in words) and "dummie" in words:
        if message.author.id == int(me): # me
            response = greetings["creator"]
            await message.channel.send(response)
        elif message.author.id == int(owner): # server owner
            response = greetings["owner"]
            await message.channel.send(response)
        else:
            response = random.choice(greetings["member"])
            await message.channel.send(response)

    await bot.process_commands(message)  # check if any commands were sent

@bot.event  # invalid command check
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command... \n\n'
                       'Please use **!d help** to be DMed a list of commands. Make sure your DMs are open!')

# END EVENTS

# COMMANDS
@bot.tree.command(name='namesake', description="Prints where DUMMIE's name comes from.")
async def first_command(interaction):
    await interaction.response.send_message("https://apexlegends.fandom.com/wiki/DUMMIE")
@bot.command(name='wowmods', description='Sends a list of some useful World of Warcraft mods to the current channel')
async def wow_info(ctx):
    if ctx.author.bot: # make sure the user wasn't a bot
        return

    response = "\n" # so it lines up better

    for key, value in mods.items():
        mod = key + ' - ' + value + '\n'
        response += mod

    await ctx.send(response)


@bot.command(name='help', description='DUMMIE (me!) sends this list of commands to you (not a DUMMIE!)')
async def list_commands(ctx):
    if ctx.author.bot:
        return

    prefix = "The commands you can give me are listed below.\n"
    response = "```\n"

    for key, value in list_of_commands.items():
        comm = "{}{}\n\n".format(key.ljust(20), value)
        response += comm

    response += "\n```"
    await ctx.author.send(prefix + response)

# END COMMANDS

bot.run(token)
