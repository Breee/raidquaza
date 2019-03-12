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
Copy the file `config/config.ini.example` to `config/config.ini` (or create it). 
The configuration file can contain sections of the form: 

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
pokestop_table_name = pokestops
gym_table_name = forts

[geofences]
use_geofences = True
geofences = ["config/geofence1.txt", "config/geofence2.txt"]
channels = [12321425124, 12321425124]
```
where:

### [bot] section: 
 -`<bot_token>` is the token of your discord bot user.

### Defining the source of Point of Interests. 
You must choose between using a csv file or a database.
Just the section you need.

**Limitations:** 
- Currently we only support mysql/mariadb databases
- Currently we only support databases which have tables names tables  `forts`  and `pokestops`


####  [csv] section:
  * `<.csv file>` is a .csv file, which consists of 4 columns: Name, long, lat,Type(Arena/Pokestop)
  an example file is `data/gyms_stops.csv` which contains all pokestops and arenas of the city Freiburg.


#### [database] section: 
 In the `database` section you can define the database, from which the bot shall pull gyms and pokestops.  (e.g. monocle)
The database must have tables  `forts`  and `pokestops`,  both must have columns `name`, `lat`, `lon` 
  * `use_database`: True False - enables the use of database.
  * `host`:  Database host
  * `database`: Database Name
  * `user`: Database User
  * `password`: Database Password of your user.
  * `pokestop_table_name` : table which contains pokestops.
  * `gym_table_name`: table which contains gyms.

### [geofences] section:
 * If your set of Point of Interests is really big and covers multiple regions, you can use geofences 
 * `use_geofences`: True | False  - Enables the usage of geofences.
 * `geofences` defines a list of geofences, an entry in the list defines a path to a geofence (starting from the repository root)
 * `channels` defines a list of discord-channel IDs. You can find out the ID of a channel, by enabling the developer mode in discord; When enabled, you can right click a channel and copy its ID. Channel IDs are **integers**, not strings.
 
The lists  `geofences` and `channels` define a one-to-one mapping.

Example:
The follwing definition
```
geofences = ["config/geofence1.txt", "config/geofence2.txt"]
channels = [CHANNEL_ID_1, CHANNEL_ID_2]
```
- Defines a mapping: 
* `CHANNEL_ID_1` -> `"config/geofence1.txt"`
* `CHANNEL_ID_2` -> `"config/geofence2.txt"`

Which means that in channel `CHANNEL_ID_1` you can only search within the geofences defined in `"config/geofence1.txt"`,
and in channel `CHANNEL_ID_2` you can only search within the geofences defined in `"config/geofence2.txt"`.

If you do not need this feature, just delete the section in the config.

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
