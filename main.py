import asyncio
import json
import os
from os.path import isfile, join
import discord
from discord.ext import commands




class GuildBot(commands.Bot):

    def loadModules(self):
        cogFolder = 'Modules'
        for extension in [f.replace('.py', '') for f in os.listdir(cogFolder) if isfile(join(cogFolder, f))]:
            try:
                self.load_extension(name=cogFolder+'.'+extension)
                print('Extension {} Loaded Successfully!'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))