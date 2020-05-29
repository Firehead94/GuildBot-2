import discord
from discord import Embed, Color
from discord.ext import commands
from pathlib import Path
import json

RESOURCES_FOLDER = Path("modules/settings/")
SETTINGS_FILE = RESOURCES_FOLDER / "blacklist.json"


class Blacklist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Check if first time being run
        if not SETTINGS_FILE.is_file():
            if not RESOURCES_FOLDER.is_dir():
                RESOURCES_FOLDER.mkdir()
            SETTINGS_FILE.write_text(json.dumps({}, indent=4), encoding='utf8')

    @commands.group(name = "blacklist", pass_context = True)
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                await ctx.send("**Incorrect Command Usage**")
            except:
                pass

    @blacklist.command(name = "add", pass_context = True)
    @commands.has_permissions(kick_members = True)
    async def add(self, ctx, *words):
        phrase = ""
        for word in words:
            phrase = phrase + word + " "
        list = get_setting(ctx.guild.id)
        if phrase not in list:
            list.append(phrase)
            change_setting(ctx.guild.id, list)

    @blacklist.command(name = "remove", pass_context = True)
    @commands.has_permissions(kick_members = True)
    async def remove(self, ctx, *words):
        phrase = ""
        for word in words:
            phrase = phrase + word + " "
        list = get_setting(ctx.guild.id)
        if phrase in list:
            list.remove(phrase)
            change_setting(ctx.guild.id, list)

    @blacklist.command(name = "print", pass_context = True)
    @commands.has_permissions(kick_members = True)
    async def print(self, ctx):
        try:
            content = ""
            list = get_setting(ctx.guild.id)
            for word in list:
                content = content + word + "\n"
            await ctx.send(embed=Embed(title="Blacklist", description=content, color=Color(0xFF0000)))
        except:
            await ctx.send(content="No blacklist found.")

    @commands.Cog.listener()
    async def on_message(self, msg):
        list = get_setting(msg.guild.id)
        list = [x.lower() for x in list]
        string = msg.content.lower()
        for x in list:
            if x in string:
                await msg.delete()
                await msg.author.send(content="Message deleted, **{}** violates {}'s discord blacklist.".format(x, msg.guild.name))


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
    bot.add_cog(Blacklist(bot))