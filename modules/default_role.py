import traceback

import discord
from discord.ext import commands
from pathlib import Path
import json
import logging
import typing

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
            try:
                await ctx.send("{} *is the current default role applied to new users.*".format(discord.utils.get(ctx.guild.roles, id=get_setting(ctx.guild.id, "role_id")).mention))
            except KeyError as e:
                print(traceback.format_exc())
                await ctx.send("*There is no current default role applied to new users.*")

    @default.command(name = "set_role", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def setRole(self, ctx, role: discord.Role):
        if role < ctx.author.top_role:
            change_setting(ctx.guild.id, "role_id", role.id)
            change_setting(ctx.guild.id, "enabled", True)
            await ctx.send("**SETTING CHANGED:** *Default discord role applied to new users set to* {}.".format(role.mention))
        else:
            await ctx.send("**ERROR:** *You do not have high enough permissions to manage this role.*")

    @default.command(name = "clear_role", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def clearRole(self, ctx):
        role_id = get_setting(ctx.guild.id, "role_id")
        change_setting(ctx.guild.id, "role_id", None)
        change_setting(ctx.guild.id, "enabled", False)
        if role_id is not None:
            await ctx.send("**SETTING CHANGED:** {} *is no longer the default discord role applied to new users.*".format(discord.utils.get(ctx.guild.roles, id=role_id).mention))
        else:
            await ctx.send("**ERROR:** *No default role was set.*")

    @default.command(name = "enable", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def enable(self, ctx):
        change_setting(ctx.guild.id, "enabled", True)
        await ctx.send("**SETTING CHANGED:** *Default role will now be applied to new users.*")

    @default.command(name = "disable", pass_context=True)
    @commands.has_permissions(administrator = True)
    async def disable(self, ctx):
        change_setting(ctx.guild.id, "enabled", False)
        await ctx.send("**SETTING CHANGED:** *Default role will no longer be applied to new users.*")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print('Command Error: '+str(error))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            if not member.bot and get_setting(member.guild.id, "enabled"):
                await member.add_roles(discord.utils.get(member.guild.roles, id=get_setting(member.guild.id, "role_id")))
        except KeyError:
            pass


def change_setting(guild_id, k, v):
    guild_id = str(guild_id)
    settings = json.load(SETTINGS_FILE.open())
    settings[guild_id][k] = v
    SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')


def get_setting(guild_id: str, k: str):
    guild_id = str(guild_id)
    settings = json.load(SETTINGS_FILE.open())
    return settings[guild_id][k]


def setup(bot):
    bot.add_cog(DefaultRole(bot))
