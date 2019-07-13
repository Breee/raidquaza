[![Build Status](https://travis-ci.com/Breee/raidquaza.svg?branch=master)](https://travis-ci.com/Breee/raidquaza)
# Discord bot Raidquaza
- Bot to create polls via discord.
- Bot to search Point of Interests via discord.

Try it out and add it to your discord :) 
https://discordapp.com/api/oauth2/authorize?client_id=410240526701559829&permissions=280640&scope=bot 


# Setup

## 1. Requirements: 
- python 3.7
- pip3
- discord bot user (https://discordapp.com/developers/applications/me)
- Add Emojis from directory `/poll/emojis/` to your discord server, name them equally. (`rq_plus_one`,`rq_plus_two`,`rq_plus_three`, `rq_plus_four`)
- A database of your choice, which is supported by sqlalchemy (https://docs.sqlalchemy.org/en/13/core/engines.html).


## 2. Configuration:
Copy the file `config.py.dist` to `config.py` (or create it). 
The configuration file is plain python and looks as follows: 

```
from utility.enums import DataSource

# Directory where the log file of the bot shall be stored
LOG_PATH = '/home/logs/raidquaza'

"""
Discord Section.
"""
# The Token of your botuser.
BOT_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# Discord Status
PLAYING = 'RaidquazaTesting'
# Command prefix
PREFIX = '!'

"""
Poll Section.
"""
# If you want to use the poll COG, set this to true
POLL_ENABLED = True
# The host of the DB in which we store polls
POLL_DB_HOST = 'localhost'
# The user of the DB
POLL_DB_USER = 'pollman'
# The password of user POLL_DB_USER
POLL_DB_PASSWORD = 'bestpw'
# The port of the DB-server
POLL_DB_PORT = 3306
# The name of the DB in which we store polls
POLL_DB_NAME = 'polldb'
# The dialect of the database-server
POLL_DB_DIALECT = 'mysql'
# The driver of the database-server
POLL_DB_DRIVER = 'mysqlconnector'

"""
Search section.

Here we define the settings for the Search.
"""
# If you want to use the search COG, set this to True.
SEARCH_ENABLED = True

"""
Choosing the datasource. 

The datasource is either DataSource.DATABASE or DataSource.CSV
If DataSource.DATABASE is chosen, we pull the gyms and stops from a database.
If DataSource.CSV is chosen, we pull the gyms and stops from a csv file, an example can be found in 
'data/gyms_stops.csv'
"""
SEARCH_DATASOURCE = DataSource.DATABASE

# The csv file we pull data from, example in 'data/gyms_stops.csv'. Leave this empty if you do not need it.
SEARCH_CSV_FILE = ''

# If you have chosen DataSource.DATABASE, you have to define from which database you pull data.
# The host of the DB
SEARCH_DB_HOST = 'localhost'
# The name of the database
SEARCH_DB_NAME = 'monocledb'
# The user of the database
SEARCH_DB_USER = 'monocleuser'
# The password to connect with SEARCH_DB_USER.
SEARCH_DB_PASSWORD = 'test123'
# The port of the database-server
SEARCH_DB_PORT = 3309
# The dialect of the database-server
SEARCH_DB_DIALECT = 'mysql'
# The driver of the database-server
SEARCH_DB_DRIVER = 'mysqlconnector'

# The table in database SEARCH_DB_NAME, which contains pokestops
SEARCH_POKESTOP_TABLE = 'pokestops'
# The table in database SEARCH_DB_NAME, which contains gyms
SEARCH_GYM_TABLE = 'forts'


"""
Choosing the datasource for portals. 

The datasource is either DataSource.DATABASE or DataSource.CSV
If DataSource.DATABASE is chosen, we pull the gyms and stops from a database.
If DataSource.CSV is chosen, we pull the from a csv file SEARCH_CSV_FILE an example can be found in 
'data/gyms_stops.csv'
"""
SEARCH_USE_PORTALS = True
# if you want CSV, use SEARCH_CSV_FILE
SEARCH_PORTALS_DATASOURCE = DataSource.DATABASE

# If you have chosen DataSource.DATABASE, you have to define from which database you pull data.
# The host of the DB
SEARCH_PORTALS_DB_HOST = 'localhost'
# The name of the database
SEARCH_PORTALS_DB_NAME = 'monocledb'
# The user of the database
SEARCH_PORTALS_DB_USER = 'monocleuser'
# The password to connect with SEARCH_DB_USER.
SEARCH_PORTALS_DB_PASSWORD = 'test123'
# The port of the database-server
SEARCH_PORTALS_DB_PORT = 3309
# The dialect of the database-server
SEARCH_PORTALS_DB_DIALECT = 'mysql'
# The driver of the database-server
SEARCH_PORTALS_DB_DRIVER = 'mysqlconnector'

# The table in database SEARCH_PORTALS_DB_NAME, which contains portals
SEARCH_PORTALS_DB_TABLE = 'ingress_portals'

"""
Geofencing.

When the amount of pokestops/gyms if big and you cover different cities / regions, you might want to restrict the 
search space for different channels.
We define a mapping DISCORD_CHANNEL -> GEOFENCE, if you then use the search functionality in a specified 
DISCORD_CHANNEL, the search space is restricted to point of interests which are in the according GEOFENCE.
"""
# Set to true if you want to use geofencing.
SEARCH_USE_GEOFENCES = True
# DISCORD_CHANNEL -> GEOFENCE
SEARCH_CHANNELS_TO_GEOFENCES = {434387358817976350: "data/geofences/freiburg.txt",
                                434618437419925504: "data/geofences/emmendingen.txt",
                                554074442272211045: "data/geofences/krozingen.txt"
                                }


```
where:

### Discord section: 
 -`BOT_TOKEN` is the token of your discord bot user.

### Search section:

If you want to enable search, set `SEARCH_ENABLED = True`

#### Defining the source of Point of Interests. 
You must choose between using a csv file or a database.

* `SEARCH_DATASOURCE` defines which is  either `DataSource.DATABASE` or `DataSource.CSV`. 

####  `DataSource.CSV` approach:
  * `SEARCH_CSV_FILE` is a path to .csv file, which consists of 4 columns: Name, long, lat,Type(Arena/Pokestop)
  an example file is `data/gyms_stops.csv` which contains all pokestops and arenas of the city Freiburg.


#### `DataSource.DATABASE` approach: 
you must define the database, from which the bot shall pull gyms and pokestops.  (e.g. monocle)
  * `SEARCH_DB_HOST`:  Database host.
  * `SEARCH_DB_NAME`: Database name.
  * `SEARCH_DB_USER`: Database user.
  * `SEARCH_DB_PORT` : Database port.
  * `SEARCH_DB_PASSWORD`: Database password of your user.
  * `SEARCH_DB_DIALECT`: Dialect of your database-server.
  * `SEARCH_DB_DRIVER`: Driver of your database-server.
  * `SEARCH_POKESTOP_TABLE` : table which contains pokestops.
  * `SEARCH_GYM_TABLE`: table which contains gyms.
  The tables `SEARCH_POKESTOP_TABLE` + `SEARCH_GYM_TABLE` must have columns `name`, `lat`, `lon`.

### Geofencing settings:
 * If your set of Point of Interests is really big and covers multiple regions, you can use geofences 
 * `SEARCH_USE_GEOFENCES`: True | False  - Enables the usage of geofences.
 * `SEARCH_CHANNELS_TO_GEOFENCES` defines a mapping of discord-channel IDs to geofence-files.
 You can find out the ID of a channel, by enabling the developer mode in discord; When enabled, you can right click a channel and copy its ID.
 Channel IDs are **integers**, not strings.
 Geofences are defined as a path to a geofence-file (starting from the repository root).
 Examples of geofence-files can be found in `data/geofences`.

Example:
The following definition
```
SEARCH_CHANNELS_TO_GEOFENCES = {
                                CHANNEL_ID_1: "data/geofences/freiburg.txt",
                                CHANNEL_ID_2: "data/geofences/emmendingen.txt"
                                }
```
- Defines a mapping: 
* `CHANNEL_ID_1` -> `"data/geofences/freiburg.txt"`
* `CHANNEL_ID_2` -> `"data/geofences/emmendingen.txt"`

Which means that in channel `CHANNEL_ID_1` you can only search within the geofences defined in `"data/geofences/freiburg.txt"`,
and in channel `CHANNEL_ID_2` you can only search within the geofences defined in `"data/geofences/emmendingen.txt"`.



## 3. Deploy:
### Configure
Fill in everything necessary in `config.py`

### Install python3 requirements
We recommend to use a virtual environment.
```
python3 -m venv raidquaza-venv
source raidquaza-venv/bin/activate
```

Then install the requirements.
```
pip3 install -U -r requirements.txt
```

### Start the bot
Call:
```
python3 start_bot.py
```




## Deploy with docker
We expect you to know about docker, docker-compose and how you deploy.

There is a `docker-compose.yml` located in the root directory.

```yaml
version: '2.4'
services:

  raidquaza:
    build:
      context: ""
      dockerfile: Dockerfile
    entrypoint: ["/entrypoint.sh"]
    volumes:
      - ./raidquaza/:/usr/src/app/
    restart: always
    depends_on:
      - poll-db
    networks:
      - default

  poll-db:
    image: mariadb
    environment:
      MYSQL_ROOT_PASSWORD: root1234
      MYSQL_DATABASE: polldb
      MYSQL_USER: pollman
      MYSQL_PASSWORD: bestpw
    command: ['mysqld', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_unicode_ci']
    volumes:
      - ./volumes/mysql/db:/var/lib/mysql
    restart: always
    networks:
      - default
``` 

An example config for a bot with polls and search (with CSV as datasource for simplicity) would be: 
```
from utility.enums import DataSource

# Directory where the log file of the bot shall be stored
LOG_PATH = '/home/logs/raidquaza'

"""
Discord Section.
"""
# The Token of your botuser.
BOT_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# Discord Status
PLAYING = 'RaidquazaTesting'
# Command prefix
PREFIX = '!'

"""
Poll Section.
"""
# If you want to use the poll COG, set this to true
POLL_ENABLED = True
# The host of the DB in which we store polls
POLL_DB_HOST = 'poll-db'
# The user of the DB
POLL_DB_USER = 'pollman'
# The password of user POLL_DB_USER
POLL_DB_PASSWORD = 'bestpw'
# The port of the DB-server
POLL_DB_PORT = 3306
# The name of the DB in which we store polls
POLL_DB_NAME = 'polldb'
# The dialect of the database-server
POLL_DB_DIALECT = 'mysql'
# The driver of the database-server
POLL_DB_DRIVER = 'mysqlconnector'
"""
Search section.

Here we define the settings for the Search.
"""
# If you want to use the search COG, set this to True.
SEARCH_ENABLED = True

"""
Choosing the datasource. 

The datasource is either DataSource.DATABASE or DataSource.CSV
If DataSource.DATABASE is chosen, we pull the gyms and stops from a database.
If DataSource.CSV is chosen, we pull the gyms and stops from a csv file, an example can be found in 
'data/gyms_stops.csv'
"""
SEARCH_DATASOURCE = DataSource.CSV

# The csv file we pull data from, example in 'data/gyms_stops.csv'. Leave this empty if you do not need it.
SEARCH_CSV_FILE = 'data/gyms_stops.csv'

# If you have chosen DataSource.DATABASE, you have to define from which database you pull data.
# The host of the DB
SEARCH_DB_HOST = ''
# The name of the database
SEARCH_DB_NAME = ''
# The user of the database
SEARCH_DB_USER = ''
# The password to connect with SEARCH_DB_USER.
SEARCH_DB_PASSWORD = ''
# The port of the database-server
SEARCH_DB_PORT = 0
# The dialect of the database-server
SEARCH_DB_DIALECT = ''
# The driver of the database-server
SEARCH_DB_DRIVER = ''

# The table in database SEARCH_DB_NAME, which contains pokestops
SEARCH_POKESTOP_TABLE = ''
# The table in database SEARCH_DB_NAME, which contains gyms
SEARCH_GYM_TABLE = ''

"""
Geofencing.

When the amount of pokestops/gyms if big and you cover different cities / regions, you might want to restrict the 
search space for different channels.
We define a mapping DISCORD_CHANNEL -> GEOFENCE, if you then use the search functionality in a specified 
DISCORD_CHANNEL, the search space is restricted to point of interests which are in the according GEOFENCE.
"""
# Set to true if you want to use geofencing.
SEARCH_USE_GEOFENCES = False
# DISCORD_CHANNEL -> GEOFENCE
SEARCH_CHANNELS_TO_GEOFENCES = {}


```

If you want to use the search feature, you have to add the configuration to the above.
If you use a DB as data_source for the search, you should add the DB to the `docker-compose.yml` or run it in the same network as these services.
To bring the services up, simply `docker-compose up -d poll-db`, `docker-compose up -d raidquaza`.

# Commands
Commands consist of a `prefix` and an `alias`.

You can specify a `prefix` in `raidquaza/config/config.ini`, the default prefixes are `!` and `@bot_user_name#1337`.

Search:
- `![search | s | query | q] <query>`will search for an Arena/Pokestop and return the top 5 results. (Arena/Pokestop + Google maps link)
- `![gym|arena] <query>`will search for an Arena return the top 5 results. (Arena + Google maps link)
- `![stop | pokestop] <query>`will search for an Stop return the top 5 results. (Stop + Google maps link)
- `![portal | poi] <query>`will search for an Portal return the top 5 results. (Stop + Google maps link)
- `!reindex` rebuild the index  (Requires that you are Owner of the Bot)
- `!scoring` change scoring type to either one:  needleman_wunsch | levenshtein | affine (Requires that you are Owner of the Bot) 
This command should not bother you, the default is affine scoring, which we consider to perform good atm.

Utils:
- `!help` display help
- `!ping` ping the bot
- `!uptime` return how long the bot is operational.

Poll:
- `!poll <title> <option_1> .. <option_17>` to create a new poll.
Polls may have at most 17 vote options, as discord supports a maximum of 21 reactions the bot adds 4 extra reactions.
