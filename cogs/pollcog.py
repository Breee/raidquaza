import discord
from discord.ext import commands
from globals.globals import LOGGER
from poll.poll import Poll, number_emojies
from poll.pollmanager import PollManager
import uuid
from config.Configuration import Configuration


class PollCog(commands.Cog, name="Poll"):
    def __init__(self, bot, config: Configuration):
        self.bot = bot
        self.pollmanager = PollManager(config)

    @commands.command(help="Create a poll", aliases=['umfrage', 'raid', 'voting'])
    async def poll(self, ctx, poll_title, *options):
        # create a new poll
        poll_id = str(uuid.uuid4())
        new_poll = Poll(poll_id, poll_title, options)
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

    async def process_raw_reaction_event(self, payload: discord.RawReactionActionEvent, add):
        data = {'count': 1, 'me': payload.user_id == self.bot.user.id,
                'emoji': {'id': payload.emoji.id, 'name': payload.emoji.name}
                }
        if data['me']:
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.Reaction(message=message, data=data)
        user = self.bot.get_user(payload.user_id)
        if self.pollmanager.is_sent_message(payload.message_id):
            poll = self.pollmanager.get_poll_by_msg_id(payload.message_id)
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
