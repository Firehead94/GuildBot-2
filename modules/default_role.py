import discord
from discord.ext import commands
from pathlib import Path
import json
import logging

RESOURCES_FOLDER = Path("modules/default_role/")
SETTINGS_FILE = RESOURCES_FOLDER / "settings.json"


class DefaultRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Check if first time being run
        if not Path(SETTINGS_FILE).is_file():
            RESOURCES_FOLDER.mkdir()
            SETTINGS_FILE.write_text(json.dumps({}, indent=4), encoding='utf8')

    @commands.group(name = "default", pass_context=True)
    async def default(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @default.command(name = "set_role", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def setRole(self, ctx, role: discord.Role):
        settings = json.load(SETTINGS_FILE.open())
        settings[ctx.guild.id] = {"role_id":role.id,"enabled":True}
        SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')

    @default.command(name = "clear_role", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def clearRole(self, ctx):
        settings = json.load(SETTINGS_FILE.open())
        settings[ctx.guild.id] = {"role_id":None,"enabled":False}
        SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')

    @default.command(name = "enable", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def enable(self, ctx):
        settings = json.load(SETTINGS_FILE.open())
        settings[ctx.guild.id]["enabled"] = True
        SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')

    @default.command(name = "disable", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def disable(self, ctx):
        settings = json.load(SETTINGS_FILE.open())
        settings[ctx.guild.id]["enabled"] = False
        SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')

    @default.command(name = "toggle", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def toggle(self, ctx):
        settings = json.load(SETTINGS_FILE.open())
        try:
            settings[ctx.guild.id]["enabled"] = not settings[str(ctx.guild.id)]["enabled"]
        except:
            settings[ctx.guild.id]["enabled"] = False
        SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print('Command Error: '+str(error))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        settings = json.load(SETTINGS_FILE.open())
        if not member.bot and (str(member.guild.id) in settings) and settings[str(member.guild.id)]["enabled"]:
            SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')
            try:
                await member.add_roles(discord.utils.get(member.guild.roles, id=settings[str(member.guild.id)]["role_id"]))
            except KeyError:
                pass


def setup(bot):
    bot.add_cog(DefaultRole(bot))
