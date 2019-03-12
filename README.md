# Discord Searchbot
Bot to search Point of Interests via discord.

# Setup
## 1. Requirements: 
- python 3.6+
- pip3
- discord bot user (https://discordapp.com/developers/applications/me)


## 2. Install requirements:
We recommend to use a virtual environment.
```
python3 -m venv searchbot-venv
source searchbot-venv/bin/activate
```

Then install the requirements.
```
pip3 install -U -r requirements.txt
```

## 3. Configuration:
Copy the file `config.ini.example` to `config.ini` (or create it). 
The configuration file is of the form: 

```
[bot]
token = <bot_token>
playing = u mom lel

[csv]  
point_of_interests = <.csv file>

[database]
use_database = True
host = localhost
database = db_name
user = user_name
password = password
port = 3306
```
where:

- [bot]: 
 -`<bot_token>` is the token of your discord bot user.
- [csv]:
  * `<.csv file>` is a .csv file, which consists of 4 columns: Name, long, lat,Type(Arena/Pokestop)
  an example file is `data/gyms_stops.csv` which contains all pokestops and arenas of the city Freiburg.
- [database]: 
 In the `database` section you can define the database, from which the bot shall pull gyms and pokestops.  (e.g. monocle)
The database must have tables  `forts`  and `pokestops`,  both must have columns `name`, `lat`, `lon` 
  * use_database: (True|False)
  * host:  Database host
  * database: Database Name
  * user: Database User
  * password: Database Password of your user.

You must choose between using a csv file or a database.

## 4. Starting the bot
Call:
```
python3 start_bot.py
```

# Commands
Search:
- `!search <query>`will search for an Arena/Pokestop and return the top 5 results. (Arena/Pokestop + Google maps link)
- `!arena <query>`will search for an Arena return the top 5 results. (Arena + Google maps link)
- `!stop <query>`will search for an Stop return the top 5 results. (Stop + Google maps link)
- `!reindex` rebuild the index  (Requires that you are Owner of the Bot)
- `!scoring` change scoring type to either one:  needleman_wunsch | levenshtein | affine (Requires that you are Owner of the Bot) 
This command should not bother you, the default is affine scoring, which we consider to perform good atm.

Utils:
- `!help` display help
- `!ping`ping the bot
- `!uptime` return how loing the bot is operational.
