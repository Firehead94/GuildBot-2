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
            settings = json.load(SETTINGS_FILE.open())
            if str(ctx.guild.id) in settings:
                role_id = settings[str(ctx.guild.id)]["role_id"]
                await ctx.send("{} *is the current default role applied to new users.*".format(discord.utils.get(ctx.guild.roles, id=role_id)))
            else:
                await ctx.send("*There is no current default role applied to new users.*")

    @default.command(name = "set_role", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def setRole(self, ctx, role: discord.Role):
        settings = json.load(SETTINGS_FILE.open())
        settings[ctx.guild.id] = {"role_id":role.id,"enabled":True}
        SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')
        await ctx.send("**SETTING CHANGED:** *Default discord role applied to new users set to* {}".format(role.mention))

    @default.command(name = "clear_role", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def clearRole(self, ctx):
        settings = json.load(SETTINGS_FILE.open())
        role_id = settings[str(ctx.guild.id)]["role_id"]
        settings[ctx.guild.id] = {"role_id":None,"enabled":False}
        SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')
        await ctx.send("**SETTING CHANGED:** {} *is no longer the default discord role applied to new users".format(discord.utils.get(ctx.guild.roles, id=role_id)))

    @default.command(name = "enable", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def enable(self, ctx):
        settings = json.load(SETTINGS_FILE.open())
        settings[ctx.guild.id]["enabled"] = True
        SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')
        await ctx.send("**SETTING CHANGED:** *Default role will now be applied to new users.")

    @default.command(name = "disable", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def disable(self, ctx):
        settings = json.load(SETTINGS_FILE.open())
        settings[ctx.guild.id]["enabled"] = False
        SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')
        await ctx.send("**SETTING CHANGED:** *Default role will no longer be applied to new users.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print('Command Error: '+str(error))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        settings = json.load(SETTINGS_FILE.open())
        if not member.bot and str(member.guild.id) in settings and settings[str(member.guild.id)]["enabled"]:
            SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')
            try:
                await member.add_roles(discord.utils.get(member.guild.roles, id=settings[str(member.guild.id)]["role_id"]))
            except KeyError:
                pass


def setup(bot):
    bot.add_cog(DefaultRole(bot))
