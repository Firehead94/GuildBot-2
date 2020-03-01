import re
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import asyncio
import json
from pathlib import Path
import traceback


RESOURCES_FOLDER = Path("modules/settings/")
SETTINGS_FILE = RESOURCES_FOLDER / "role_assist.json"
NO = ["no", "n", ""]
YES = ["yes", "y"]

class RoleAssist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Check if first time being run
        if not SETTINGS_FILE.is_file():
            if not RESOURCES_FOLDER.is_dir():
                RESOURCES_FOLDER.mkdir()
            SETTINGS_FILE.write_text(json.dumps({}, indent=4), encoding='utf8')

    @commands.group(name = "roleassist", aliases = ["ra", "RA"])
    async def roleassist(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("**Role Assist is active.**")

    @roleassist.command(name="TrackMessage", aliases=["TM", "trackmessage", "trackmsg", "trackMsg", "TrackMsg", "tm", "track"])
    @commands.has_permissions(administrator=True)
    async def track(self, ctx, msgid):
        msgid = str(msgid)
        conversation = [ctx.message]
        settings = json.load(SETTINGS_FILE.open())
        if str(ctx.guild.id) not in settings:
            settings[str(ctx.guild.id)] = {}
        settings = settings[str(ctx.guild.id)]

        try:
            tracking = await ctx.fetch_message(int(msgid))
        except:
            await ctx.send("**Command must be run in the same channel as the message you wish to track**", delete_after=10)
            await ctx.channel.delete_messages(conversation)
            return
        if msgid not in settings:
            settings[msgid] = {}
        else:
            conversation.append(await ctx.send("*Message already tracked*"))
            while True:
                conversation.append(await ctx.send("*Erase current settings? (yes/no)*"))
                reply = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
                conversation.append(reply)
                if reply.content.lower() in NO:
                    conversation.append(await ctx.send("*Exiting message tracking..."))
                    return
                elif reply.content.lower() in YES:
                    settings[msgid] = {}
                    break;
        sent = await ctx.send("*Please react to this message with the emote(s) you'd like to track. Reply with \"done\" when finished. Any emoji's used **MUST** be available on this server to use.*")
        conversation.append(sent)
        conversation.append(await self.bot.wait_for("message", check=lambda message: message.author == ctx.author and message.content.lower() == "done", timeout=300))
        sent = await ctx.fetch_message(sent.id)
        reactions = sent.reactions
        for reaction in reactions:
            conversation.append(await ctx.send("*Please mention the role(s) you'd like to give for  {.emoji}. Note, you may need to temporarily make the roles mentionable in their settings.*".format(reaction)))
            roles = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
            conversation.append(roles)
            if roles is not None:
                settings[msgid][str(reaction.emoji)] = []
                for role in roles.role_mentions:
                    settings[msgid][str(reaction.emoji)].append(role.id)
            try:
                await tracking.add_reaction(reaction.emoji)
            except:
                conversation.append(await ctx.send("**{.emoji}** *is not available to use on this server. Please contact your server administrator.*".format(reaction)))
        conversation.append(await ctx.send("*Now tracking message for role assignments.*"))

        while True:
            conversation.append(await ctx.send("*Would you like me to clear up the mess we made? (yes/no)*"))
            reply = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
            conversation.append(reply)
            if reply.content.lower() in ["no", "n", ""]:
                return
            elif reply.content.lower() in ["yes", "y"]:
                await cleanup(ctx, conversation)
                break
        change_settings(ctx.guild.id, settings)

    @roleassist.command(name="UntrackMessage", aliases=["UM", "untrackmessage", "untrackmsg", "untrackMsg", "UnTrackMsg", "utm", "untrack", "UT", "ut"])
    @commands.has_permissions(administrator=True)
    async def untrack(self, ctx, msgid):
        try:
            tracking = await ctx.fetch_message(int(msgid))
        except:
            await ctx.send("**Command must be run in the same channel as the message you wish to track**", delete_after=10)
            await ctx.channel.delete_messages([ctx.message])
            return
        try:
            settings = json.load(SETTINGS_FILE.open())
            if str(ctx.guild.id) not in settings:
                settings[str(ctx.guild.id)] = {}
            settings = settings[str(ctx.guild.id)]

            del settings[str(msgid)]
            change_settings(ctx.guild.id, settings)
            await tracking.clear_reactions()
            await ctx.send("*Message is no longer tracked.*", delete_after=5)
        except KeyError:
            await ctx.send("*Message was not being tracked.*", delete_after=5)
        await ctx.channel.delete_messages([ctx.message])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.user_id) == str(self.bot.user.id):
            pass
        else:
            settings = json.load(SETTINGS_FILE.open())
            guild_id = str(payload.guild_id)

            guild = self.bot.get_guild(payload.guild_id)
            message = str(payload.message_id)
            emoji = str(payload.emoji)
            member = guild.get_member(payload.user_id)
            if guild_id in settings:
                settings = settings[guild_id]
                if message in settings:
                    if emoji in settings[message]:
                        roles = settings[message][emoji]
                        for id in roles:
                            await member.add_roles(discord.utils.get(guild.roles, id=int(id)), reason="Auto Assign")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if str(payload.user_id) == str(self.bot.user.id):
            pass
        else:
            settings = json.load(SETTINGS_FILE.open())
            guild_id = str(payload.guild_id)

            guild = self.bot.get_guild(payload.guild_id)
            message = str(payload.message_id)
            emoji = str(payload.emoji)
            member = guild.get_member(payload.user_id)
            if guild_id in settings:
                settings = settings[guild_id]
                if message in settings:
                    if emoji in settings[message]:
                        roles = settings[message][emoji]
                        for id in roles:
                            await member.remove_roles(discord.utils.get(guild.roles, id=int(id)), reason="Auto Remove")


async def cleanup(ctx, conversation):
    await ctx.send("**GOODBYE**", delete_after=5)
    await asyncio.sleep(2)
    await ctx.channel.delete_messages(conversation)


def change_settings(guild_id, v):
    guild_id = str(guild_id)
    settings = json.load(SETTINGS_FILE.open())
    if guild_id not in settings:
        settings[guild_id] = {}
    settings[guild_id] = v
    SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf-8')


def get_setting(guild_id: str, *k: str):
    guild_id = str(guild_id)
    settings = json.load(SETTINGS_FILE.open())
    r = settings[guild_id]
    try:
        for i in k:
            r = r[str(i)]
        return r
    except:
        return None


def setup(bot):
    bot.add_cog(RoleAssist(bot))
