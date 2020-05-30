import discord
from discord import Embed, Color
from discord.ext import commands, timers
from pathlib import Path
import json
import re
import time, datetime

RESOURCES_FOLDER = Path("modules/settings/")
SETTINGS_FILE = RESOURCES_FOLDER / "timers.json"


class Timers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.timer_manager = timers.TimerManager(self.bot)

        # Check if first time being run
        if not SETTINGS_FILE.is_file():
            if not RESOURCES_FOLDER.is_dir():
                RESOURCES_FOLDER.mkdir()
            SETTINGS_FILE.write_text(json.dumps({}, indent=4), encoding='utf8')

    @commands.group(name = "timer", pass_context = True)
    async def timer(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                await ctx.send("**Incorrect Command Usage**")
            except:
                pass

    @timer.command(name = "help")
    async def help(self, ctx):
        embed = discord.Embed(title="Timers for Guildbot")
        embed.add_field(name="Command", value="Start", inline=False)
        embed.add_field(name='Usage', value="!gb timer start <TIME> <MESSAGE>", inline=False)
        embed.add_field(name='<TIME>', value="Formatted as DD:HH:MM:SS, HH:MM:SS, MM:SS, SS", inline=False)
        embed.add_field(name='<MESSAGE>', value="Message to be sent at the end of timer. Can be used to ping users or roles as well.", inline=False)
        embed.add_field(name="Example", value="!gb timer start 15:00:00 @Hark, the world boss spawn window is now open", inline=False)
        await ctx.send(content=None, embed=embed)

    @timer.command(name = "start", aliases=["Start"])
    async def setTimer(self, ctx, time, message):
        vals = re.split("^(?:(?:(?:([0-9]?\d):)?([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)$", time)
        if len(vals) <= 1:
            await ctx.send("Incorrect Datetime format. Please use DD:HH:MM:SS, HH:MM:SS, MM:SS, SS for your timers format.")
        vals = [0 if v is None else v for v in vals]
        delta = datetime.timedelta(days=int(vals[1]), hours=int(vals[2]), minutes=int(vals[3]), seconds=int(vals[4]))
        self.bot.timer_manager.create_timer("reminder", delta, args=(ctx.channel.id, ctx.author.id, message))

    @commands.Cog.listener()
    async def on_reminder(self, channel_id, author_id, msg):
        channel = self.bot.get_channel(channel_id)
        await channel.send("<@{0}>, timer ended: {1}".format(author_id, msg))





def change_setting(guild_id, v):
    guild_id = str(guild_id)
    settings = json.load(SETTINGS_FILE.open())
    if guild_id not in settings:
        settings[guild_id] = []
    settings[guild_id] = v
    SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf-8')


def get_setting(guild_id: str):
    guild_id = str(guild_id)
    settings = json.load(SETTINGS_FILE.open())
    if guild_id in settings:
        r = settings[guild_id]
        return r
    return []


def setup(bot):
    bot.add_cog(Timers(bot))