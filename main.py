import discord
from discord.ext import commands
import config as cfg
from discord.ext import tasks

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(case_insensitive=True,
                         command_prefix=commands.when_mentioned_or("%"), 
                         intents=intents)

bot = Bot()

@tasks.loop(seconds=240)  # Status updates every 4 minutes = 240 seconds
async def status_update_task():

    with open(cfg.CONSOLE_FILE_PATH, "r") as f:  # Opening the file in read mode
        content = f.readlines()  # reading the content of it

    # reverse the list so we can search from the end of the file
    content.reverse()

    # look for the line containing "IngameTime"
    ingame_time_line = None
    for line in content:
        if "IngameTime" in line:
            ingame_time_line = line
            break

    if ingame_time_line is not None:
        # Getting the hour and minute using index positions
        hours_minute_time = ingame_time_line[-5]+ingame_time_line[-4]+ingame_time_line[-3]+ingame_time_line[-2]+ingame_time_line[-1]
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'PZ AT {hours_minute_time}'))
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'PZ AT Recalculating'))

    f.close()  # Closing the file so it opens the updated file next time

@bot.event
async def on_ready():
    print(f'--------------------------------------------------------------')
    print(f'Logged in as {bot.user.name} | {bot.user.id}')
    print(f'--------------------------------------------------------------')
    status_update_task.start()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'PZ AT Recalculating')) 

bot.run(cfg.TOKEN)
