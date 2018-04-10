# pokemon-discord-report-bot
Bot which will post quest/raid/rareIV in an according channel, if a user sends the according command.

The idea is to have a single discord channel, in which trainers can post reports of spotted raids, nests, quests or rare/high IV pokemon.

# Setup
## 1. Requirements: 
- python3
- pip3
- discord bot user (https://discordapp.com/developers/applications/me)

## 2. Install discord.py using pip:
```
pip3 install discord.py
```
## 3. Configuration:
Copy the file `config.conf.dist` to `config.conf` (or create it). 
The configuration file is of the form: 

```
token=<discord bot user token>
playing=reporting for duty!
raid-channel-id=<channel-id>
rare-channel-id=<channel-id>
nest-channel-id=<channel-id>
quest-channel-id=<channel-id>
gyms-csv=<.csv file>
```
where:
- `<discord bot user token>` is the token of your discord bot user.
- `<channel-id>` is the ID of the discord channel where you want the bot to post. 
- `<.csv file>` is a .csv file, which consists of 3 colums: Name <tab> Location <tab> Type(Arena/Pokestop)
  an example file is `gyms_stops.csv` which contains all pokestops and arenas of the city Freiburg.

## 4. Starting the bot
Call:
```
python3 start_bot.py
```

# Commands
- `!raid <Boss + location + time>` to report a raid, the bot will post in the specified channel with the id `raid-channel-id`
- `!rare <Pokemon + IV + location>` to report a rare or high IV pokemon, the bot will post in the specified channel with the id `rare-channel-id`
- `!nest <Pokemon + location>` to report a pokemon cluster spawn / frequent spawn, the bot will post in the specified channel with the id `nest-channel-id`
- `!quest <Quest + reward + location>` to report a quest, the bot will post in the specified channel with the id `quest-channel-id`
- `!stats (here)` will send a ranking via PM/directly in a channel
- `!search <query>`will search for an Arena/Pokestop and return the top 5 results. (Arena/Pokestop + Google maps link)
