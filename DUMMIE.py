import os
import random
import discord
import string
import datetime
import urllib
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
import mysql.connector

load_dotenv(dotenv_path='lib/.env')

# access variables
token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')  # the one to look for
me = os.getenv('ME')
owner = os.getenv('OWNER')
announcements_ch = os.getenv('ANNOUNCEMENTS_CH')

# access variables (database)
db_url = os.getenv('JAWSDB_URL')
out = urllib.parse.urlsplit(db_url)
db_host = out.hostname
db_user = out.username
db_pw = out.password
db_name = out.path[1::]

# greetings
greetings =  {
    "creator" : "Hello, creator!",
     "member" : [
         "Hi, friend!",
         "I think we're going to do great, friend.",
         "High-five!",
         "I just polished my grapple :robot:",
         "Hey, that's me!"
                ]
             }

# start of day
startOfDay = datetime.time(hour=5, minute=0, second=0)  # adjusted for UTC... hour=0 => UTC
currentMonth = datetime.date.today().month
currentDay = datetime.date.today().day

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
        "Clique (click-to-cast)" : "https://www.curseforge.com/wow/addons/clique",
        "Watcher (casting rotations timeline)" : "https://www.curseforge.com/wow/addons/shotwatch"
        }

"""END WoW-Related"""

"""Helper Functions"""
def webpageWordCount(url): # returns a dictionary containing the five most frequently occurring words on a Web page
    d = {}
    mostFrequent = {}

    newURL = urllib.request.urlopen(url)
    if newURL.getcode() == 200:
        print("DUMMIE successfully scraped a Web page. The web server responded with: \n{} OK".format(newURL.getcode()))
    webpageContent = newURL.read()
    soup = BeautifulSoup(webpageContent, features="html.parser") # default parameter to avoid warning
    res = soup.get_text('\n').split()
    for word in res:
        for char in string.punctuation:
            if char in word:
                word = word.replace(char,'')
        if word not in d and not word.isspace():
            d[word] = 1
        else:
            d[word] += 1

    counter = 0

    # prepare the dictionary to return to the bot here
    while counter != 6:
        # spaces are far more common than other characters, so add a 6th entry
        # entries following the space won't have spaces
        current_max = max(d, key=d.get)
        mostFrequent[current_max] = d[current_max]
        del d[current_max]  # update for next highest...
        counter += 1

    d.clear()
    for key in mostFrequent.keys():
        if key in string.whitespace:
            del mostFrequent[key]
            break  # will fail if omitted
    return mostFrequent

"""END Helper Functions"""

def_intents = discord.Intents.default()  # required as of version 2
def_intents.members = True               # MUST ALSO enable in Dev Portal -> Bot -> Gateway Intents
def_intents.message_content = True       # ditto
bot = commands.Bot(
    command_prefix='!d ',
    case_insensitive=True,
    help_command=None,
    intents=def_intents)

# TASKS

@tasks.loop(time=startOfDay)
async def birthdayCheck():
    # get database of birthdays...
    # find any birthdays where it's the current date
    # if found, print to announcements
    # otherwise, just print no birthdays found in console...
    try:
        db = mysql.connector.connect(host=db_host, user=db_user, password=db_pw, database=db_name)
        print("Successfully connected to database...")
    except Exception as e:
        print(e)

    db_cursor = db.cursor()
    select_stmt = ("SELECT name FROM birthdays WHERE month=%(month)s AND day=%(day)s")
    db_cursor.execute(select_stmt, { 'month' : currentMonth, 'day' : currentDay })
    db_res = db_cursor.fetchall()
    # check length; if > 1, then say it to everyone in the list...
    if db_res:
        print("Found a birthday today!")
        if len(db_res) > 2:
            who = ""
            for row in db_res:
                if row != db_res[-1] and row != db_res[-2]:
                    who += row[0] + ', '
                elif row != db_res[-1] and row == db_res[-2]:
                    who += row[0] + ' '
                else:
                    who += 'and ' + row[0]
            birthday_message = "Today is the birthday of {}! DUMMIE and OTC wish you all a Happy Birthday!! :tada: "\
                               ":gift: :robot:".format(who)
            channel = bot.get_channel(int(announcements_ch))
            await channel.send(birthday_message)
        elif len(db_res) > 1:
            who = ""
            for row in db_res:
                if row != db_res[-1]:
                    who += row[0] + ' '
                else:
                    who += 'and ' + row[0]
            birthday_message = "Today is the birthday of {}! DUMMIE and OTC wish you both a Happy Birthday!! :tada: "\
                               ":gift: :robot:".format(who)
            channel = bot.get_channel(int(announcements_ch))
            await channel.send(birthday_message)
        else:
            birthday_message = "Today is the birthday of {}! DUMMIE and OTC wish you a Happy Birthday!! :tada: :gift: "\
                               ":robot:".format(db_res[0][0])
            channel = bot.get_channel(int(announcements_ch))
            await channel.send(birthday_message)
    else:
        print("No birthdays found today.")
    db.close()
    print("DB connection closed.")


# END TASKS
@bot.event
async def on_ready():
    current_guild = discord.utils.get(bot.guilds, id=int(guild))

    print("{} has connected to Discord!\n"
          "{} is currently connected to:\n"
          "{} (id: {})".format(bot.user, bot.user, current_guild.name, current_guild.id))

    print('Guild members: ')
    for member in current_guild.members:
        print(member.name)

    try:
        syncing = await bot.tree.sync()
        print("Synced {} command(s)".format(len(syncing)))
    except Exception as e:
        print(e)

    if not birthdayCheck.is_running():
        birthdayCheck.start()
        print("Today's date is {}-{}.".format(currentMonth, currentDay))
        print("Checking if there are any birthdays today...")
        
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
@bot.tree.command(name='namesake',
                  description="Prints where DUMMIE's name comes from.")
async def first_command(interaction):
    await interaction.response.send_message("https://apexlegends.fandom.com/wiki/DUMMIE")

@bot.command(name='wowmods',
             description='Sends a list of some useful World of Warcraft mods to the current channel')
async def wow_info(ctx):
    if ctx.author.bot: # make sure the user wasn't a bot
        return

    response = "\n" # so it lines up better

    for key, value in mods.items():
        mod = key + ' - ' + value + '\n'
        response += mod

    await ctx.send(response)

@bot.command(name='wc',
             description='Scrapes a web page to find the five most frequently used words on it, then sends them'\
                         ' to the current channel')
async def webScrape(ctx, url):
    if ctx.author.bot:
        return

    try:
        webpageResult = webpageWordCount(url)

        response = "I carefully scanned the page and found that these are the five most frequently used words:\n```\n"
        for key, value in webpageResult.items():
            response += "{} : {}\n".format(key, value)
        response += "```\n\nI hope none of these are bad words..."

    except Exception as e:
        response = "Ouch! I had a problem fetching or parsing the web page: {}\n" \
                   "If you didn't include a URL to a web page in your message, I need one... !d wc **<URL>**".format(e)

    await ctx.send(response)
@bot.command(name='help',
             description='DUMMIE (me!) sends this list of commands to you (not a DUMMIE!)')
async def list_commands(ctx):
    if ctx.author.bot:
        return

    prefix = "The commands you can give me are listed below.\n"
    response = "```\n"

    for command in bot.commands:
        comm = "{}{}\n\n".format(command.name.ljust(20), command.description)
        response += comm

    response += "\n```"
    await ctx.author.send(prefix + response)

# END COMMANDS

bot.run(token)
