import asyncio
import json
import os
from os.path import isfile, join
import discord
from discord.ext import commands
from pathlib import Path
import traceback

MAIN_PREFIX = "!gb "
RESOURCES_FOLDER = Path("")
SETTINGS_FILE = RESOURCES_FOLDER / "settings.json"


class GuildBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if first time being run
        if not Path(SETTINGS_FILE).is_file():
            SETTINGS_FILE.write_text(json.dumps({}, indent=4), encoding='utf8')

        settings = json.load(SETTINGS_FILE.open())
        if "api_token" not in settings:
            print("\nPlease provide valid Discord API key: ")
            settings["api_token"] = input()
            SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding='utf8')

    async def on_command_error(self, ctx, error):
        await ctx.send("**"+str(error)+"**")

    async def send_cmd_help(self, ctx):
        await ctx.send(content="No subcommand found. Please visit <https://github.com/Firehead94/RetBot> for usage information.")

    def load_modules(self):
        cogfolder = "modules"
        for extension in [f.replace('.py', '') for f in os.listdir(cogfolder) if isfile(join(cogfolder, f))]:
            try:
                self.load_extension(name=cogfolder+'.'+extension)
                print('Extension {} Loaded Successfully!'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}\n\n'.format(extension, exc))
                print(traceback.format_exc())


async def main(bot):
    settings = json.load(SETTINGS_FILE.open())
    bot.load_modules()
    await bot.login(settings['api_token'])
    await bot.connect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    bot = GuildBot(command_prefix=MAIN_PREFIX)
    try:
        loop.create_task(main(bot))
        loop.run_forever()
    except discord.LoginFailure:
        print('\nGuildBot Failed to Login: Invalid Credentials.\n'
              'This may be a temporary issue, consult Discords\n'
              'Login Server Status before attemping again.\n'
              'If servers are working properly, you may need\n'
              'a new token. Please replace the token in the\n'
              'GuildBot.ini file with a new token.\n')
    except KeyboardInterrupt:
        loop.run_until_complete(bot.logout())
    except Exception as e:
        print("Fatal exception, attempting graceful logout.\n{}".format(e))
        loop.run_until_complete(bot.logout())
    finally:
        loop.close()
        exit(1)