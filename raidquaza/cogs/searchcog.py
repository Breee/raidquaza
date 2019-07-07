import discord
from discord.ext import commands
from search.fuzzysearch import FuzzySearcher
from utility.globals import LOGGER
from search.enums import SCORING_TYPE, RECORD_TYPE
import config as config


class SearchCog(commands.Cog, name="Search"):
    def __init__(self, bot):
        self.bot = bot
        self.fuzzy_searcher = FuzzySearcher(config=config)

    @commands.command(help="Rebuild the index, you must be bot_owner to do this.")
    @commands.is_owner()
    async def reindex(self, ctx):
        LOGGER.info("Building new Index.")
        self.fuzzy_searcher.index()
        await ctx.channel.send("New index built, happy searching!")

    @commands.command(
            help="Change the scoring method of the searchengine.\n!scoring (needleman_wunsch | levenshtein | affine)")
    @commands.is_owner()
    async def scoring(self, ctx, type):
        msg = None
        if type == 'needleman_wunsch':
            self.fuzzy_searcher.point_of_interest_index.scoring_method = SCORING_TYPE.NEEDLEMAN_WUNSCH
            await ctx.send('Changed scoring method to %s' % type)
        elif type == 'levenshtein':
            self.fuzzy_searcher.point_of_interest_index.scoring_method = SCORING_TYPE.LEVENSHTEIN
            await ctx.send('Changed scoring method to %s' % type)
        elif type == 'affine':
            self.fuzzy_searcher.point_of_interest_index.scoring_method = SCORING_TYPE.AFFINE_GAPS

        else:
            msg = "Sorry, no such scoring method exists. Scoring methods: needleman_wunsch | levenshtein | affine"

        if not msg:
            msg = 'Changed scoring method to %s' % type
        await ctx.send(msg)

    @commands.command(help="Search for a Point of Interest", aliases=['s', 'query', 'q'])
    async def search(self, ctx, *, query):
        msg = ''
        results = self.fuzzy_searcher.search(query, num_results=5, channel_id=ctx.channel.id)
        if results:
            for (poi, location, type, ed) in results:
                maps_link = 'https://www.google.com/maps/place/%s,%s' % (location[0], location[1])
                msg += '- **%s:**\t[%s](%s)\t(ed: %d)\n' % (
                    type.value[0], poi.strip(), maps_link.replace('\n', '').strip(), ed)
        else:
            msg += 'No results found ...'
        embed = discord.Embed(color=11010048, title="Top results for query '%s'" % query, description=msg)
        await ctx.channel.send(content='', embed=embed)

    @commands.command(help="Search for a Gym", aliases=['arena'])
    async def gym(self, ctx, *, query):
        msg = ''
        results = self.fuzzy_searcher.search(query, num_results=15, channel_id=ctx.channel.id)
        result_count = 0
        if results:
            for (gym, location, type, ed) in results:
                maps_link = 'https://www.google.com/maps/place/%s,%s' % (location[0], location[1])
                if (type == RECORD_TYPE.GYM) and (result_count < 5):
                    msg += '- **%s:**\t[%s](%s)\t(ed: %d)\n' % (
                        type.value[0], gym.strip(), maps_link.replace('\n', '').strip(), ed)
                    result_count += 1
        else:
            msg += 'No results found ...'
        embed = discord.Embed(color=11010048, title="Top results for query '%s'" % query, description=msg)
        await ctx.channel.send(content='', embed=embed)

    @commands.command(help="Search for a Pokestop", aliases=['pokestop'])
    async def stop(self, ctx, *, query):
        msg = ''
        results = self.fuzzy_searcher.search(query, num_results=15, channel_id=ctx.channel.id)
        result_count = 0
        if results:
            for (pokestop, location, type, ed) in results:
                maps_link = 'https://www.google.com/maps/place/%s,%s' % (location[0], location[1])
                if (type == RECORD_TYPE.POKESTOP) and (result_count < 5):
                    msg += '- **%s:**\t[%s](%s)\t(ed: %d)\n' % (
                        type.value[0], pokestop.strip(), maps_link.replace('\n', '').strip(), ed)
                    result_count += 1
        else:
            msg += 'No results found ...'
        embed = discord.Embed(color=11010048, title="Top results for query '%s'" % query, description=msg)
        await ctx.channel.send(content='', embed=embed)

    async def cog_command_error(self, ctx, error):
        LOGGER.error(error)
        if isinstance(error, discord.ext.commands.errors.NotOwner):
            await ctx.send("Denied! You do not own this Bot!")
        super().cog_command_error(ctx, error)
