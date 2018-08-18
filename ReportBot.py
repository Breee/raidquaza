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
        self.add_command(self.quest)
        self.add_command(self.raid)
        self.add_command(self.rare)
        self.add_command(self.nest)
        self.add_command(self.stats)
        self.add_command(self.exterminate)
        self.add_command(self.search)
        self.add_command(self.arena)
        self.add_command(self.stop)
        self.add_command(self.collect)
        self.add_command(self.scoring)
        self.start_time = 0
        self.session = aiohttp.ClientSession(loop=self.loop)
        #
        self.message_manager = MessageManager()
        self.storage_manager = StorageManager()
        self.statistic_manager = StatisticManager()
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
        # restore messages.
        self.load_and_restore()

    def run(self):
        super().run(self.config.token, reconnect=True)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_resumed(self):
        print('resumed...')

    async def on_message_edit(self, before, after):
        """
        Fucntion which handles the editing of messages.
        :param before: message before edit
        :param after: message after edit
        :return:
        """

        if before.content is not after.content:
            # get old state of the posted message, delete it, process after state
            LOGGER.info("Processing edited message")
            storedmessage = self.message_manager.get_message(commandmessage_id=before.id)
            if storedmessage is not None:
                await self.delete_message(storedmessage.postedmessage)
                self.message_manager.delete_message(storedmessage.id)
                await self.process_commands(after)


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
    async def stats(self, ctx, here=None):
        content = self.statistic_manager.king_of_the_hill()
        if here:
            await self.send_message(destination=ctx.message.channel, content=content)
        else:
            await self.send_message(destination=ctx.message.author, content=content)


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

    @commands.command(pass_context=True)
    async def quest(self, ctx, *, report):
        # Send report to the quest-channel-id specified in the config.
        chan = self.get_channel(id=self.config.quest_channel_id)
        timestamp = datetime.now()
        msg = "__**Quest: %s**__\n\nReported by %s || %s" % (report, ctx.message.author.mention, '{:%H:%M:%S}'.format(timestamp))
        await self.send_and_store_message(ctx_message=ctx.message, channel=chan, message_content=msg, report_type=ReportType.QUEST)

    @commands.command(pass_context=True)
    async def raid(self, ctx, *, report):
        chan = self.get_channel(id=self.config.raid_channel_id)
        timestamp = datetime.now()
        search_results = self.fuzzy_searcher.search(query=report, num_results=3)
        top_arenas = ""
        if search_results:
            for arena, location, type, ed in search_results:
                if type == "Arena":
                    top_arenas += "**-%s:** [%s](%s) (ed: %d)\n" % (
                        type, arena, location.replace("\n", "").strip(), ed)

        else:
            top_arenas = "*No results found, maybe you did not write the Arena-name correctly*"
        msg = "__**Raid: %s**__\n\nReported by %s || %s" % (report, ctx.message.author.mention, '{:%H:%M:%S}'.format(timestamp))
        embed = discord.Embed(color=0xa80000, title="Top gym results",
                              description=top_arenas)
        await self.send_and_store_message(ctx_message=ctx.message, channel=chan, message_content=msg, report_type=ReportType.RAID, embed=embed)

    @commands.command(pass_context=True)
    async def rare(self, ctx, *, report):
        chan = self.get_channel(id=self.config.rare_channel_id)
        timestamp = datetime.now()
        msg = "__**Rare: %s**__\n\nReported by %s || %s" % (report, ctx.message.author.mention, '{:%H:%M:%S}'.format(timestamp))
        await self.send_and_store_message(ctx_message=ctx.message, channel=chan, message_content=msg, report_type=ReportType.RARE)

    @commands.command(pass_context=True)
    async def nest(self, ctx, *, report):
        chan = self.get_channel(id=self.config.nest_channel_id)
        timestamp = datetime.now()
        msg = "__**Nest: %s**__\n\nReported by %s || %s" % (report, ctx.message.author.mention, '{:%H:%M:%S}'.format(timestamp))
        await self.send_and_store_message(ctx_message=ctx.message, channel=chan, message_content=msg, report_type=ReportType.NEST)



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




    """
    ################ UTILS ###############
    """

    async def get_message_if_exists(self, channel, msg_id):
        try:
            message = await self.get_message(channel=channel, id=msg_id)
            return message
        except discord.NotFound:
            return None

    def load_and_restore(self):
        LOGGER.info("Loading storage and restoring messages.")
        storage = self.storage_manager.load_storage()
        if storage:
            self.message_manager.restore_messages(storage=storage)
            self.statistic_manager = storage.statistic_manager
        else:
            LOGGER.info("Storage is empty..")

    async def send_and_store_message(self, ctx_message, channel, message_content, report_type, embed=None):
        if embed:
            postedmessage = await self.send_message(destination=channel, content=message_content, embed=embed)
        else:
            postedmessage = await self.send_message(destination=channel, content=message_content)
        # finally, Store the message.
        self.statistic_manager.increase_user_stats(user=ctx_message.author, report_type=report_type)
        self.message_manager.create_message(commandmessage=ctx_message, postedmessage=postedmessage)
        self.storage_manager.update_storage(self.message_manager, self.messages, self.statistic_manager)



