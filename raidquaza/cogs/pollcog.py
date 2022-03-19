import discord
from discord.ext import commands
from poll.polls import Poll, number_emojies
from poll.pollmanager import PollManager
from utility.globals import LOGGER
import uuid


class PollCog(commands.Cog, name="poll"):
    def __init__(self, bot):
        self.bot = bot
        self.pollmanager = PollManager()

    @commands.command(help="Create a poll", aliases=['umfrage', 'raid', 'voting', 'r'])
    @commands.guild_only()
    async def poll(self, ctx, poll_title, *options):
        LOGGER.info("Creating Poll: %s %s on Server %s" % (poll_title, options, ctx.guild))
        # create a new poll
        poll_id = str(uuid.uuid4())
        new_poll = Poll(poll_id, poll_title, list(options))
        # send it to discord
        msg, embed = new_poll.to_discord()
        sent_message: discord.Message = await ctx.channel.send(content=msg,
                                                               embed=embed)
        self.pollmanager.add_poll(poll=new_poll, received_message=ctx.message, sent_message=sent_message)
        # add reactions to the poll.
        for reaction in new_poll.reaction_to_option.keys():
            await sent_message.add_reaction(reaction)
        for reaction in number_emojies:
            await sent_message.add_reaction(discord.utils.get(self.bot.emojis, name=reaction))
    
    @commands.command(help="Create a poll without number emojis")
    @commands.guild_only()
    async def simplepoll(self, ctx, poll_title, *options):
        LOGGER.info("Creating Poll: %s %s on Server %s" % (poll_title, options, ctx.guild))
        # create a new poll
        poll_id = str(uuid.uuid4())
        new_poll = Poll(poll_id, poll_title, list(options))
        # send it to discord
        msg, embed = new_poll.to_discord()
        sent_message: discord.Message = await ctx.channel.send(content=msg,
                                                               embed=embed)
        self.pollmanager.add_poll(poll=new_poll, received_message=ctx.message, sent_message=sent_message)
        # add reactions to the poll.
        for reaction in new_poll.reaction_to_option.keys():
            await sent_message.add_reaction(reaction)

    @commands.command(help="Get poll statistics")
    async def pollstats(self, ctx, show=None):
        msg = 'Polls:'
        embed = discord.Embed(description=f'Total: {len(self.pollmanager.polls)}')
        if show:
            for id, poll in self.pollmanager.polls.items():
                embed.add_field(name=f'ID: {id}', value=f'  *{poll.poll_title} - {poll.options}\n', inline=False)
        await ctx.channel.send(content=msg, embed=embed)

    @commands.command(help="read a poll")
    @commands.is_owner()
    async def readpoll(self, ctx, command_msg_id, poll_msg_id, poll_title, *options):
        # create a new poll from given information
        poll_id = str(uuid.uuid4())
        new_poll = Poll(poll_id, poll_title, options, updated_since_start=False)
        new_poll.received_message = command_msg_id
        new_poll.sent_message = poll_msg_id

        self.pollmanager.add_poll(poll=new_poll,
                                  received_message=await ctx.channel.fetch_message(command_msg_id),
                                  sent_message=await ctx.channel.fetch_message(poll_msg_id))
        # fetch the existing poll_message from discord
        poll_message: discord.Message = await ctx.channel.fetch_message(poll_msg_id)
        print(poll_message.reactions)
        # Fully update it.
        await new_poll.full_update(reactions=poll_message.reactions, bot_user_id=self.bot.user.id)
        # Send the update to discord.
        msg, embed = new_poll.to_discord()
        self.pollmanager.update_poll(new_poll)
        await poll_message.edit(content=msg, embed=embed)

    async def process_raw_reaction_event(self, payload: discord.RawReactionActionEvent, add):
        data = {'count': 1, 'me': payload.user_id == self.bot.user.id,
                'emoji': {'id': payload.emoji.id, 'name': payload.emoji.name}
                }
        if data['me']:
            return
        channel: discord.ChannelType = self.bot.get_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id)
        reaction: discord.Reaction = discord.Reaction(message=message, data=data)
        guild = await self.bot.fetch_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)
        if self.pollmanager.is_sent_message(payload.message_id):
            poll = self.pollmanager.get_poll_by_msg_id(payload.message_id)
            if not poll.updated_since_start:
                await poll.full_update(reactions=message.reactions, bot_user_id=self.bot.user.id, guild=guild)
            else:
                poll.process_reaction(reaction, user, add=add)
            msg, embed = poll.to_discord()
            self.pollmanager.update_poll(poll)
            await message.edit(content=msg, embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        await self.process_raw_reaction_event(payload, add=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        await self.process_raw_reaction_event(payload, add=False)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        # check if message ID is a received msg.
        if self.pollmanager.is_received_message(payload.message_id):
            poll = self.pollmanager.get_poll_by_msg_id(payload.message_id)
            channel: discord.ChannelType = self.bot.get_channel(payload.channel_id)
            message: discord.Message = await channel.fetch_message(poll.sent_message)
            await message.delete()
            await channel.send(f'Deleted poll, **title:** {poll.poll_title}, **ID:** {poll.poll_id}')
