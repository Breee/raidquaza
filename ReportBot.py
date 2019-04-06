from config.Configuration import Configuration
from discord.ext import commands
import discord
from _datetime import datetime
import aiohttp
from globals.globals import LOGGER
from cogs.searchcog import SearchCog
from cogs.utilscog import UtilsCog
from cogs.pollcog import PollCog


class ReportBot(commands.Bot):

    def __init__(self, prefix, description, config_file):
        super().__init__(command_prefix=[prefix], description=description, pm_help=None, help_attrs=dict(hidden=True))
        self.config = Configuration(config_file)
        self.add_cog(SearchCog(self, self.config))
        self.add_cog(UtilsCog(self))
        self.add_cog(PollCog(self, self.config))
        self.session = aiohttp.ClientSession(loop=self.loop)

    '################ EVENTS ###############'

    async def on_ready(self):
        LOGGER.info('Bot is ready.')
        self.start_time = datetime.utcnow()
        await self.change_presence(activity=discord.Game(name=self.config.playing))
        # make mentionable.
        self.command_prefix.extend([f'<@!{self.user.id}> ', f'<@{self.user.id}> '])

    def run(self):
        super().run(self.config.token, reconnect=True)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_resumed(self):
        print('resumed...')
