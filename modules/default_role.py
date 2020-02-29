import discord
from discord.ext import commands
from pathlib import Path
import json
import logging

MODULE_PREFIX = " default "
RESOURCES_FOLDER = Path("default_role/")
SETTINGS_FILE = RESOURCES_FOLDER / "settings.json"

class DefaultRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Check if first time being run
        if not Path(SETTINGS_FILE).is_file():
            SETTINGS_FILE.mkdir()
            with SETTINGS_FILE.open() as file:
                json.dump({},file,indent=4)

    @commands.command(name = MODULE_PREFIX+"set_role")
    @commands.has_permissions(administrator = True)
    async def setRole(self, ctx, role: discord.Role):
        with SETTINGS_FILE.open() as file:
            settings = json.load(file)
        settings[ctx.guild.id] = {"role_id":role.id}
        json.dump(settings, SETTINGS_FILE, indent=4)

    @commands.command(name = MODULE_PREFIX+"clear_role")
    @commands.has_permissions(administrator = True)
    async def clearRole(self, ctx):
        with SETTINGS_FILE.open() as file:
            settings = json.load(file)
        settings[ctx.guild.id] = {"role_id":None}
        json.dump(settings, SETTINGS_FILE, indent=4)

    @commands.command(name = MODULE_PREFIX+"enable")
    @commands.has_permissions(administrator = True)
    async def enable(self, ctx):
        with SETTINGS_FILE.open() as file:
            settings = json.load(file)
        settings[ctx.guild.id] = {"enabled":True}
        json.dump(settings, SETTINGS_FILE, indent=4)

    @commands.command(name = MODULE_PREFIX+"disable")
    @commands.has_permissions(administrator = True)
    async def disable(self, ctx):
        with SETTINGS_FILE.open() as file:
            settings = json.load(file)
        settings[ctx.guild.id] = {"enabled":False}
        json.dump(settings, SETTINGS_FILE, indent=4)

    @commands.command(name = MODULE_PREFIX+"toggle")
    @commands.has_permissions(administrator = True)
    async def toggle(self, ctx):
        with SETTINGS_FILE.open() as file:
            settings = json.load(file)
        settings[ctx.guild.id] = {"enabled":not settings[ctx.guild.id]["enabled"]}
        json.dump(settings, SETTINGS_FILE, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not member.bot:
            with SETTINGS_FILE.open() as file:
                settings = json.load(file)
            await member.add_roles(discord.utils.get(self.bot.guild.roles, id=settings[self.bot.guild.id]["role_id"]))

def setup(bot):
    bot.add_cog(DefaultRole(bot))
