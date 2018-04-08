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

import logging
from enum import Enum
import operator
LOGGER = logging.getLogger('discord')

class ReportType(Enum):
    QUEST = 0
    RAID = 1
    RARE = 2
    NEST = 3

class StatisticManager(object):

    def __init__(self):
        self.user_to_quest_reports = dict()
        self.user_to_raid_reports = dict()
        self.user_to_rare_reports = dict()
        self.user_to_nest_reports = dict()
        self.user_to_total_reports = dict()

    def increase_user_stats(self, user, report_type: ReportType):
        if report_type is ReportType.QUEST:
            self.user_to_quest_reports[user] = self.user_to_quest_reports.get(user, 0) + 1
        elif report_type is ReportType.RAID:
            self.user_to_raid_reports[user] = self.user_to_raid_reports.get(user, 0) + 1
        elif report_type is ReportType.RARE:
            self.user_to_rare_reports[user] = self.user_to_rare_reports.get(user, 0) + 1
        elif report_type is ReportType.NEST:
            self.user_to_nest_reports[user] = self.user_to_nest_reports.get(user, 0) + 1
        self.user_to_total_reports[user] = self.user_to_total_reports.get(user, 0) + 1

    def king_of_the_hill(self):
        msg = ""
        sorted_quests = sorted(self.user_to_quest_reports.items(), key=operator.itemgetter(1))
        msg +=  "__**Quest report ranking**__\n"
        for rank, user_amount in enumerate(sorted_quests):
            msg += "Rank #%d -- %s (%d) \n" % (rank+1, user_amount[0].name, user_amount[1])

        sorted_raids= sorted(self.user_to_raid_reports.items(), key=operator.itemgetter(1))
        msg += "\n__**Raid report ranking**__\n"
        for rank, user_amount in enumerate(sorted_raids):
            msg += "Rank #%d -- %s (%d) \n" % (rank + 1, user_amount[0].name, user_amount[1])

        sorted_rare = sorted(self.user_to_rare_reports.items(), key=operator.itemgetter(1))
        msg += "\n__**Rare and high IV report ranking**__\n"
        for rank, user_amount in enumerate(sorted_rare):
            msg += "Rank #%d -- %s (%d) \n" % (rank + 1, user_amount[0].name, user_amount[1])

        sorted_nest = sorted(self.user_to_nest_reports.items(), key=operator.itemgetter(1))
        msg += "\n__**Nest report ranking**__\n"
        for rank, user_amount in enumerate(sorted_nest):
            msg += "Rank #%d -- %s (%d) \n" % (rank + 1, user_amount[0].name, user_amount[1])
        return msg








