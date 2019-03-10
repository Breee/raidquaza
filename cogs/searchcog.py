import discord
from discord.ext import commands
from _datetime import datetime, timedelta
import aiohttp
from search.FuzzySearcher import FuzzySearcher
from search.qgram_index import SCORING_TYPE
from globals.globals import LOGGER

class SearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

    @commands.command()
    async def uptime(self, ctx):
        await ctx.send('Online for %s' % str(datetime.datetime.utcnow() - self.bot.start_time))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reindex(self, ctx):
        self.bot.fuzzy_searcher.index(self.bot.config)
        await ctx.channel.send("new index built, happy searching!")

    @commands.command()
    async def scoring(self, ctx, type):
        if type == 'needleman_wunsch':
            self.bot.fuzzy_searcher.point_of_interest_index.scoring_method = SCORING_TYPE.NEEDLEMAN_WUNSCH
            await ctx.send('Changed scoring method to %s' % type)
        elif type == 'levenshtein':
            self.bot.fuzzy_searcher.point_of_interest_index.scoring_method = SCORING_TYPE.LEVENSHTEIN
            await ctx.send('Changed scoring method to %s' % type)
        elif type == 'affine':
            self.bot.fuzzy_searcher.point_of_interest_index.scoring_method = SCORING_TYPE.AFFINE_GAPS
            await ctx.send('Changed scoring method to %s' % type)
        await ctx.message.delete()

    @commands.command()
    async def search(self, ctx, *, query='adler'):
        msg = ''
        results = self.bot.fuzzy_searcher.search(query, num_results=5, channel_id=ctx.channel.id)
        if results:
            for (arena, location, type, ed) in results:
                maps_link = 'https://www.google.com/maps/place/%s,%s' % (location[0], location[1])
                msg += '- **%s:**\t[%s](%s)\t(ed: %d)\n' % (
                type.strip(), arena.strip(), maps_link.replace('\n', '').strip(), ed)
        else:
            msg += 'No results found ...'
        embed = discord.Embed(color=11010048, title="Top results for query '%s'" % query, description=msg)
        await ctx.channel.send(content='', embed=embed)

    @commands.command()
    async def arena(self, ctx, *, query):
        msg = ''
        results = self.bot.fuzzy_searcher.search(query, num_results=15, channel_id=ctx.channel.id)
        result_count = 0
        if results:
            for (arena, location, type, ed) in results:
                maps_link = 'https://www.google.com/maps/place/%s,%s' % (location[0], location[1])
                if (type == 'Arena') and (result_count < 5):
                    msg += '- **%s:**\t[%s](%s)\t(ed: %d)\n' % (
                    type.strip(), arena.strip(), maps_link.replace('\n', '').strip(), ed)
                    result_count += 1
        else:
            msg += 'No results found ...'
        embed = discord.Embed(color=11010048, title="Top results for query '%s'" % query, description=msg)
        await ctx.channel.send(content='', embed=embed)

    @commands.command()
    async def stop(self, ctx, *, query):
        msg = ''
        results = self.bot.fuzzy_searcher.search(query, num_results=15, channel_id=ctx.channel.id)
        result_count = 0
        if results:
            for (arena, location, type, ed) in results:
                maps_link = 'https://www.google.com/maps/place/%s,%s' % (location[0], location[1])
                if (type == 'Pokestop') and (result_count < 5):
                    msg += '- **%s:**\t[%s](%s)\t(ed: %d)\n' % (
                    type.strip(), arena.strip(), maps_link.replace('\n', '').strip(), ed)
                    result_count += 1
        else:
            msg += 'No results found ...'
        embed = discord.Embed(color=11010048, title="Top results for query '%s'" % query, description=msg)
        await ctx.channel.send(content='', embed=embed)