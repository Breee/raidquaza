"""
MIT License

Copyright (c) 2018 Breee@github

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from config.Configuration import Configuration
from discord.ext import commands
import discord
import datetime
import aiohttp
import logging
import os

LOGGER = logging.getLogger('discord')
if os.path.isfile('help_msg.txt'):
    with open('help_msg.txt', 'r') as helpfile:
        HELP_MSG = helpfile.read()

BANNED_USERS = []
if os.path.isfile('banned_users.txt'):
    with open('banned_users.txt', 'r') as banned_users:
        for line in banned_users:
            BANNED_USERS.append(line)

class ReportBot(commands.Bot):
    def __init__(self, prefix, description, config_file):
        super().__init__(command_prefix=prefix, description=description, pm_help=None, help_attrs=dict(hidden=True))
        self.config = Configuration(config_file)
        self.add_command(self.ping)
        self.add_command(self.uptime)
        self.remove_command("help")
        self.add_command(self.help)
        self.add_command(self.quest)
        self.add_command(self.raid)
        self.add_command(self.rare)
        self.add_command(self.nest)
        self.start_time = 0
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def on_ready(self):
        LOGGER.info("Bot is ready.")
        self.start_time = datetime.datetime.utcnow()
        await self.change_presence(game=discord.Game(name=self.config.playing))

    def run(self):
        super().run(self.config.token, reconnect=True)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_resumed(self):
        print('resumed...')

    @commands.command(hidden=True)
    async def ping(self):
        await self.say("pong!")

    @commands.command(hidden=True)
    async def uptime(self):
        await self.say("Online for %s" % str(datetime.datetime.utcnow() - self.start_time))


    @commands.command(pass_context=True)
    async def help(self, ctx, here=None):
        if not here:
            await self.send_message(destination=ctx.message.author, content=HELP_MSG)
        else:
            await self.say(HELP_MSG)

    @commands.command(pass_context=True)
    async def quest(self, ctx, *, report):
        chan = self.get_channel(id=self.config.quest_channel_id)
        msg = "__**Quest: %s**__\n\nreported by %s" % (report, ctx.message.author.mention)
        await self.send_message(destination=chan, content=msg)

    @commands.command(pass_context=True)
    async def raid(self, ctx, *, report):
        chan = self.get_channel(id=self.config.raid_channel_id)
        msg = "__**Raid: %s**__\n\nreported by %s" % (report, ctx.message.author.mention)
        await self.send_message(destination=chan, content=msg)

    @commands.command(pass_context=True)
    async def rare(self, ctx, *, report):
        chan = self.get_channel(id=self.config.rare_channel_id)
        msg = "__**Rare: %s**__\n\nreported by %s" % (report, ctx.message.author.mention)
        await self.send_message(destination=chan, content=msg)

    @commands.command(pass_context=True)
    async def nest(self, ctx, *, report):
        chan = self.get_channel(id=self.config.nest_channel_id)
        msg = "__**Nest: %s**__\n\nreported by %s" % (report, ctx.message.author.mention)
        await self.send_message(destination=chan, content=msg)

    async def get_message_if_exists(self, channel, msg_id):
        try:
            message = await self.get_message(channel=channel, id=msg_id)
            return message
        except discord.NotFound:
            return None

