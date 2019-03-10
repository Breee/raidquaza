'\nMIT License\n\nCopyright (c) 2018 Breee@github\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'
from config.Configuration import Configuration
from discord.ext import commands
import discord
from _datetime import datetime, timedelta
import aiohttp
from search.FuzzySearcher import FuzzySearcher
from search.qgram_index import SCORING_TYPE
from globals.globals import LOGGER
from cogs.searchcog import SearchCog


class ReportBot(commands.Bot):

    def __init__(self, prefix, description, config_file):
        super().__init__(command_prefix=prefix, description=description, pm_help=None, help_attrs=dict(hidden=True))
        self.config = Configuration(config_file)
        self.fuzzy_searcher = FuzzySearcher(self.config)
        self.add_cog(SearchCog(self))
        self.start_time = 0
        self.session = aiohttp.ClientSession(loop=self.loop)

    '################ EVENTS ###############'

    async def on_ready(self):
        LOGGER.info('Bot is ready.')
        self.start_time = datetime.utcnow()
        await self.change_presence(activity=discord.Game(name=self.config.playing))

    def run(self):
        super().run(self.config.token, reconnect=True)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_resumed(self):
        print('resumed...')