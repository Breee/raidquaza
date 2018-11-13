# pokemon-discord-search-bot
Bot to search a Arena/Pokestop via discord.

# Setup
## 1. Requirements: 
- python3
- pip3
- discord bot user (https://discordapp.com/developers/applications/me)

## 2. Install discord.py and numpy:
```
pip3 install -r requirements.txt
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
- `<bot_token>` is the token of your discord bot user.
- `<.csv file>` is a .csv file, which consists of 4 columns: Name, long, lat,Type(Arena/Pokestop)
  an example file is `data/gyms_stops.csv` which contains all pokestops and arenas of the city Freiburg.
- In the `database` section you can define the database, from which the bot shall pull gyms and pokestops.  (e.g. monocle)
The database must have tables  `forts`  and `pokestops`,  both must have columns `name`, `lat`, `lon` 

You must either use csv file or a database. 


## 4. Starting the bot
Call:
```
python3 start_bot.py
```

# Commands
- `!search <query>`will search for an Arena/Pokestop and return the top 5 results. (Arena/Pokestop + Google maps link)
- `!arena <query>`will search for an Arena return the top 5 results. (Arena + Google maps link)
- `!stop <query>`will search for an Stop return the top 5 results. (Stop + Google maps link)
