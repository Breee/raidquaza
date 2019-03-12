import discord
from discord.ext import commands
from search.FuzzySearcher import FuzzySearcher
from search.qgram_index import SCORING_TYPE
from globals.globals import LOGGER

class SearchCog(commands.Cog, name="Search"):
    def __init__(self, bot, config):
        self.bot = bot
        self.fuzzy_searcher = FuzzySearcher(config)

    @commands.command(help="Rebuild the index, you must be bot_owner to do this.")
    @commands.is_owner()
    async def reindex(self, ctx):
        LOGGER.info("Building new Index.")
        self.fuzzy_searcher.index(self.bot.config)
        await ctx.channel.send("New index built, happy searching!")

    @commands.command(help="Change the scoring method of the searchengine.\n!scoring (needleman_wunsch | levenshtein | affine)")
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
        await ctx.message.delete()

    @commands.command(help="Search for a Point of Interest")
    async def search(self, ctx, *, query):
        msg = ''
        results = self.fuzzy_searcher.search(query, num_results=5, channel_id=ctx.channel.id)
        if results:
            for (arena, location, type, ed) in results:
                maps_link = 'https://www.google.com/maps/place/%s,%s' % (location[0], location[1])
                msg += '- **%s:**\t[%s](%s)\t(ed: %d)\n' % (
                type.strip(), arena.strip(), maps_link.replace('\n', '').strip(), ed)
        else:
            msg += 'No results found ...'
        embed = discord.Embed(color=11010048, title="Top results for query '%s'" % query, description=msg)
        await ctx.channel.send(content='', embed=embed)

    @commands.command(help="Search for an Arena")
    async def arena(self, ctx, *, query):
        msg = ''
        results = self.fuzzy_searcher.search(query, num_results=15, channel_id=ctx.channel.id)
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

    @commands.command(help="Search for a Pokestop")
    async def stop(self, ctx, *, query):
        msg = ''
        results = self.fuzzy_searcher.search(query, num_results=15, channel_id=ctx.channel.id)
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

    async def cog_command_error(self, ctx, error):
        LOGGER.error(error)
        if isinstance(error, discord.ext.commands.errors.NotOwner):
            await ctx.send("Denied! You do not own this Bot!")
        super().cog_command_error(ctx, error)
