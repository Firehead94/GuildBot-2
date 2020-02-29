import asyncio
import json
import os
from os.path import isfile, join
import discord
from discord.ext import commands
import logging

MAIN_PREFIX = "!GB"
LOGGER = logging.basicConfig(filename="GuildBot.log", level=logging.DEBUG)
LOGGER_FORMATTING = logging.Formatter('%(asctime)s || %(name)s  [%(levelname)s] : %(message)s')

class GuildBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger("MAIN")

    def loadModules(self):
        cogFolder = 'Modules'
        for extension in [f.replace('.py', '') for f in os.listdir(cogFolder) if isfile(join(cogFolder, f))]:
            try:
                self.load_extension(name=cogFolder+'.'+extension)
                print('Extension {} Loaded Successfully!'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))