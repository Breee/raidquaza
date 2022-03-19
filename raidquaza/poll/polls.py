from typing import List, Any
import time
from discord import Embed, Reaction
from utils import uniquify

# EMOJIS regional_indicator_A to regional_indicator_T
reaction_emojies = ['\U0001F1E6',
                    '\U0001F1E7',
                    '\U0001F1E8',
                    '\U0001F1E9',
                    '\U0001F1EA',
                    '\U0001F1EB',
                    '\U0001F1EC',
                    '\U0001F1ED',
                    '\U0001F1EE',
                    '\U0001F1EF',
                    '\U0001F1F0',
                    '\U0001F1F1',
                    '\U0001F1F2',
                    '\U0001F1F3',
                    '\U0001F1F4',
                    '\U0001F1F5',
                    '\U0001F1F6',
                    '\U0001F1F7',
                    '\U0001F1F8',
                    '\U0001F1F9']

number_emojies = {'rq_plus_one': 1, 'rq_plus_two': 2, 'rq_plus_three': 3, 'rq_plus_four': 4}


class PollCreationException(Exception):
    pass


class Poll(object):
    """
    A Poll object.
    """

    def __init__(self, poll_id: str, poll_title: str, options: List[Any], is_immortal=False, updated_since_start=True):
        if options is None:
            options = []
        self.poll_id = poll_id
        self.creation_time = time.time()
        self.last_update = time.time()
        self.poll_title = poll_title
        self.options = uniquify(options)
        self.reaction_to_option = {reaction_emojies[k]: options[k] for k in range(len(options))}
        self.option_to_reaction = {options[k]: reaction_emojies[k] for k in range(len(options))}
        self.participants = dict()
        self.option_to_participants = {key: [] for key in options}
        self.sent_message = None
        self.received_message = None
        self.is_immortal = is_immortal
        self.is_enabled = True
        self.updated_since_start = updated_since_start

    async def full_update(self, reactions: List[Reaction], bot_user_id: int, guild):
        if self.updated_since_start:
            return
        self.reaction_to_option = {reaction_emojies[k]: self.options[k] for k in range(len(self.options))}
        self.option_to_reaction = {self.options[k]: reaction_emojies[k] for k in range(len(self.options))}
        self.participants = dict()
        self.option_to_participants = {key: [] for key in self.options}
        for reaction in reactions:
            async for user in reaction.users():
                if bot_user_id != user.id:
                    member = await guild.fetch_member(user.id)
                    self.process_reaction(reaction=reaction, user=member, add=True)
        self.updated_since_start = True

    def process_reaction(self, reaction, user, add):
        # get users + reaction emoji
        if hasattr(user, 'nick') and user.nick is not None:
            nick = user.nick
        else:
            nick = user.display_name
        if reaction.emoji in self.reaction_to_option:
            # set list of users for the option the reaction belongs to.
            option = self.reaction_to_option[reaction.emoji]
            if add and nick not in self.option_to_participants[option]:
                self.option_to_participants[option].append(nick)
            elif not add:
                self.option_to_participants[option].remove(nick)
        if nick not in self.participants:
            self.participants[nick] = 1
        if hasattr(reaction.emoji, 'name') and reaction.emoji.name in number_emojies:
            amount = number_emojies[reaction.emoji.name]
            self.participants[nick] += (amount if add else -1 * amount)

    def to_discord(self):
        msg = f'Poll for **{self.poll_title}**'
        embed = Embed(color=0xbb1c1c)
        for option, participants in self.option_to_participants.items():
            reaction = self.option_to_reaction[option]
            name = f'{reaction} {option}'
            value = ', '.join(
                    sorted([f'{x} [{self.participants[x]}]' for x in participants])) if participants else '-'
            field_counters = [self.participants[x] for x in participants]
            total = sum(field_counters)
            embed.add_field(name=f'{name} [{total}]', value=value, inline=False)
            embed.set_footer(text=f'ID: {self.poll_id}')
        return msg, embed
