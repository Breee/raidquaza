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
from _datetime import datetime, timedelta
import aiohttp
import logging
import os
import re

from messages.MessageManager import MessageManager
from storage.StorageManager import StorageManager
from stats.StatisticManager import StatisticManager, ReportType
from search.FuzzySearcher import FuzzySearcher
from search.qgram_index import SCORING_TYPE

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
        self.add_command(self.exterminate)
        self.add_command(self.search)
        self.add_command(self.arena)
        self.add_command(self.stop)
        self.add_command(self.collect)
        self.add_command(self.scoring)
        self.start_time = 0
        self.session = aiohttp.ClientSession(loop=self.loop)
        #
        self.fuzzy_searcher = FuzzySearcher(self.config.gyms_csv)

    """
    ################ EVENTS ###############
    """

    #async def on_member_join(self, member):
    #    LOGGER.info("ban %s" % member.name)
    #    await self.ban(member,delete_message_days=7)

    async def on_ready(self):
        LOGGER.info("Bot is ready.")
        self.start_time = datetime.utcnow()
        await self.change_presence(game=discord.Game(name=self.config.playing))

    def run(self):
        super().run(self.config.token, reconnect=True)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_resumed(self):
        print('resumed...')


    """
    ################ COMMANDS ###############
    """

    @commands.command(hidden=True)
    async def ping(self):
        await self.say("pong!")

    @commands.command(hidden=True)
    async def uptime(self):
        await self.say("Online for %s" % str(datetime.datetime.utcnow() - self.start_time))


    @commands.command(hidden=True, pass_context=True)
    async def exterminate(self, ctx, number):
        mgs = []  # Empty list to put all the messages in the log
        number = int(number)  # Converting the amount of messages to delete to an integer
        async for x in self.logs_from(ctx.message.channel, limit=number):
            mgs.append(x)
        await self.delete_messages(mgs)

    @commands.command(hidden=True, pass_context=True)
    async def scoring(self, ctx, type):
        if type == "needleman_wunsch":
            self.fuzzy_searcher.fuzzy.scoring_method = SCORING_TYPE.NEEDLEMAN_WUNSCH
            await self.say("Changed scoring method to %s" % type)
        elif type == "levenshtein":
            self.fuzzy_searcher.fuzzy.scoring_method = SCORING_TYPE.LEVENSHTEIN
            await self.say("Changed scoring method to %s" % type)
        elif type == "affine":
            self.fuzzy_searcher.fuzzy.scoring_method = SCORING_TYPE.AFFINE_GAPS
            await self.say("Changed scoring method to %s" % type)
        await self.delete_message(ctx.message)


    @commands.command(pass_context=True)
    async def help(self, ctx, here=None):
        if not here:
            await self.send_message(destination=ctx.message.author, content=HELP_MSG)
        else:
            await self.say(HELP_MSG)


    @commands.command(pass_context=True, enabled=True)
    async def search(self, ctx, *, query):
        msg = ""
        results = self.fuzzy_searcher.search(query, num_results=5)
        if results:
            for arena, location, type, ed in results:
                maps_link = "https://www.google.com/maps/place/%s,%s" % (location[0], location[1])
                msg += "- **%s:**\t[%s](%s)\t(ed: %d)\n" % (
                type.strip(), arena.strip(), maps_link.replace("\n", "").strip(), ed)
        else:
            msg += "No results found ..."
        embed = discord.Embed(color=0xa80000, title="Top results for query '%s'" % query,
                              description=msg)
        await self.send_message(destination=ctx.message.channel, content="", embed=embed)


    @commands.command(pass_context=True)
    async def arena(self, ctx, *, query):
        msg = ""
        results = self.fuzzy_searcher.search(query, num_results=15)
        result_count = 0
        if results:
            for arena, location, type, ed in results:
                maps_link = "https://www.google.com/maps/place/%s,%s" % (location[0], location[1])
                if type == "Arena" and result_count < 5:
                    msg += "- **%s:**\t[%s](%s)\t(ed: %d)\n" % (
                    type.strip(), arena.strip(), maps_link.replace("\n", "").strip(), ed)
                    result_count += 1
        else:
            msg += "No results found ..."
        embed = discord.Embed(color=0xa80000, title="Top results for query '%s'" % query,
                              description=msg)
        await self.send_message(destination=ctx.message.channel, content="", embed=embed)


    @commands.command(pass_context=True)
    async def stop(self, ctx, *, query):
        msg = ""
        results = self.fuzzy_searcher.search(query, num_results=15)
        result_count = 0
        if results:
            for arena, location, type, ed in results:
                maps_link = "https://www.google.com/maps/place/%s,%s" % (location[0], location[1])
                if type == "Pokestop" and result_count < 5:
                    msg += "- **%s:**\t[%s](%s)\t(ed: %d)\n" % (
                        type.strip(), arena.strip(), maps_link.replace("\n", "").strip(), ed)
                    result_count += 1
        else:
            msg += "No results found ..."
        embed = discord.Embed(color=0xa80000, title="Top results for query '%s'" % query,
                              description=msg)
        await self.send_message(destination=ctx.message.channel, content="", embed=embed)

    @commands.command(pass_context=True)
    async def collect(self, ctx, number, type):
        LOGGER.info("Collecting and storing messages...")
        mgs = []  # Empty list to put all the messages in the log
        number = int(number)  # Converting the amount of messages to delete to an integer
        async for x in self.logs_from(ctx.message.channel, limit=number):
            if x.author != self.user:
                mgs.append(x)

        with open("%s.log" % type, "w") as message_file:
            for message in mgs:
                message_file.write("%s\t%s\n" % (type, message.content))
        LOGGER.info("Done")
        await self.delete_message(ctx.message)


