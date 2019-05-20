from discord.ext import commands
import time


class UtilsCog(commands.Cog, name="Utility"):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command(help="Ping the bot, if he does not answer you're fucked.")
    async def ping(self, ctx):
        await ctx.send('pong!')

    @commands.command(help="Return how long the bot is operational.")
    async def uptime(self, ctx):
        seconds = time.time() - self.start_time
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        await ctx.send('Online for %.3f seconds (that are %.3f minutes or %.3f hours or %.3f days)' % (
            seconds, minutes, hours, days))

    @commands.command(aliases=['dracarys'])
    @commands.is_owner()
    async def purge(self, ctx, number):
        async for message in ctx.channel.history(limit=number):
            await message.delete()
