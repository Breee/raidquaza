from config.Configuration import Configuration
from discord.ext import commands
import discord
from _datetime import datetime
import aiohttp
from globals.globals import LOGGER
from cogs.searchcog import SearchCog
from cogs.utilscog import UtilsCog
from cogs.pollcog import PollCog
import traceback
import asyncio
from poll.utils import replace_quotes


class Raidquaza(commands.Bot):

    def __init__(self, description, config: Configuration):
        super().__init__(command_prefix=[config.prefix], description=description, pm_help=None,
                         help_attrs=dict(hidden=True))
        self.config = config
        if self.config.use_search:
            self.add_cog(SearchCog(self, self.config))
        if self.config.use_polls:
            self.add_cog(PollCog(self, self.config))
        self.add_cog(UtilsCog(self))
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

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            LOGGER.critical(f'In {ctx.command.qualified_name}:')
            traceback.print_tb(error.original.__traceback__)
            LOGGER.critical(f'{error.original.__class__.__name__}: {error.original}')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.author.send(
                    'Sorry. This command is not how this command works, !help <command_name> to display usage')
        else:
            LOGGER.critical(error)

    @asyncio.coroutine
    async def process_commands(self, message):
        """|coro|
        This function processes the commands that have been registered
        to the bot and other groups. Without this coroutine, none of the
        commands will be triggered.
        By default, this coroutine is called inside the :func:`.on_message`
        event. If you choose to override the :func:`.on_message` event, then
        you should invoke this coroutine as well.
        This is built using other low level tools, and is equivalent to a
        call to :meth:`~.Bot.get_context` followed by a call to :meth:`~.Bot.invoke`.
        This also checks if the message's author is a bot and doesn't
        call :meth:`~.Bot.get_context` or :meth:`~.Bot.invoke` if so.
        Parameters
        -----------
        message: :class:`discord.Message`
            The message to process commands for.
        """
        if message.author.bot:
            return
        message.content = replace_quotes(message.content)
        ctx = await self.get_context(message)
        await self.invoke(ctx)
