import discord
from discord.ext import commands
from pathlib import Path
import json
from discord import Embed, Color
import datetime

class Developer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="dev", pass_context=True)
    async def dev(self, ctx):
        pass

    @dev.command(name="embed", pass_context=True)
    async def embedTest(self, ctx):
        embed = Embed()
        embed.title = "Title"
        embed.type = "rich"
        embed.description = "description lorim ipsum"
        embed.url = "http://classic.wowhead.com"
        embed.timestamp = datetime.datetime.now()
        embed.colour = Color.blue()
        embed.set_footer(text="footer", icon_url="https://cdn3.iconfinder.com/data/icons/capsocial-round/500/facebook-512.png")
        embed.set_image(url="https://wow.zamimg.com/uploads/screenshots/small/5439.jpg")
        embed.set_thumbnail(url="https://wow.zamimg.com/images/wow/icons/large/inv_weapon_halberd_11.jpg")
        embed.set_author(name="wowhead", url="http://classic.wowhead.com", icon_url="https://i.pinimg.com/favicons/eca28199c2fbf0ae23373b839916551feae2fe02d04f827a4acaa859.png?8318cd0d651bce539d8d09e39d4f2da5")
        embed.add_field(name="fieldA1", value="valueA1", inline=True)
        embed.add_field(name="fieldA2", value="valueA2", inline=True)
        embed.add_field(name="fieldA3", value="valueA3", inline=True)
        embed.add_field(name="fieldB1", value="valueB1", inline=False)
        embed.add_field(name="fieldB2", value="valueB2", inline=False)
        embed.add_field(name="fieldB3", value="valueB3", inline=False)
        await ctx.send(content=None, embed=embed)

    @dev.command(name="weapon", pass_context=True)
    async def weapon(self, ctx):
        embed = Embed(title="{:50}".format("The Blackrock Slicer"), url="https://classic.wowhead.com/item=13285/the-blackrock-slicer")
        embed.set_author(name="Wowhead", url="http://classic.wowhead.com", icon_url="https://wow.zamimg.com/images/logos/favicon-standard.png")
        embed.set_thumbnail(url="https://wow.zamimg.com/images/wow/icons/large/inv_weapon_halberd_11.jpg")
        embed.colour = Color.blue()
        embed.add_field(name="Item Level 58", value="Binds when picked up", inline=False)
        embed.add_field(name="{:60}".format("Two-Hand"), value="{:60}".format("159 - 239 Damage"), inline=True)
        embed.add_field(name="{:^10}".format("Axe"), value="{:>10}".format("Speed 4.00"), inline=True)
        embed.add_field(name="(49.75 damage per second)", value="Durability 100/100", inline=False)
        embed.add_field(name="Requires Level 53", value="[Chance on hit: Wounds the target for 50 to 150 damage and deals an additional 6 damage every 1 sec for 25 sec.](https://classic.wowhead.com/spell=17407)", inline=False)
        embed.add_field(name="Sell Price: 5g 49s 24c", value="Dropped by: Spirestone Battle Lord \n Drop Chance: 38.14%", inline=False)
        await ctx.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Developer(bot))