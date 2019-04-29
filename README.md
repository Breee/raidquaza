# Discord bot Raidquaza
- Bot to create polls via discord.
- Bot to search Point of Interests via discord.

# Setup

## 1. Requirements: 
- python 3.6+
- pip3
- discord bot user (https://discordapp.com/developers/applications/me)
- Add Emojis from directory `/poll/emojis/` to your discord server, name them equally. (`rq_plus_one`,`rq_plus_two`,`rq_plus_three`, `rq_plus_four`)

## 2. Install Python3 requirements:
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
token = <discord_bot_token>
playing = Raidquaza!

[search]
# database / csv
data_source = database
host = localhost
database = monocle
user = monocleuser
password = test123
port = 3306
pokestop_table_name = pokestops
gym_table_name = forts
use_geofences = True
geofences = ["config/freiburg.txt","config/emmendingen.txt"]
channels = ["411547369096740864", "410357320464465929"]


[polls]
host = localhost
user = pollman
password = bestpw
port = 3307
database = polldb
dialect = mysql
driver = mysqlconnector
```
where:

### [bot] section: 
 -`<bot_token>` is the token of your discord bot user.

### Defining the source of Point of Interests. 
You must choose between using a csv file or a database.
Just use the section you need.

**Limitations:** 
- Currently we only support mysql/mariadb databases

### [search] section:

* `data_source` defines which is either `database` or `csv`. 

####  csv settings:
  * `csv_file` is a path to .csv file, which consists of 4 columns: Name, long, lat,Type(Arena/Pokestop)
  an example file is `data/gyms_stops.csv` which contains all pokestops and arenas of the city Freiburg.


#### database settings: 
 In the `database` section you can define the database, from which the bot shall pull gyms and pokestops.  (e.g. monocle)
  * `use_database`: True False - enables the use of database.
  * `host`:  Database host.
  * `database`: Database name.
  * `user`: Database user.
  * `port` : Database port.
  * `password`: Database password of your user.
  * `pokestop_table_name` : table which contains pokestops.
  * `gym_table_name`: table which contains gyms.
  The tables `pokestop_table_name` + `gym_table_name` must have columns `name`, `lat`, `lon`.

### geofence settings:
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

### [polls] section:
In the `polls` section you define a database, where the bot shall store its polls.
* `host`:  Database host.
* `database`: Database name.
* `user`: Database user.
* `password`: Database password of your user.
* `port` : Database port.
* `dialect` : SQL Dialect of the database.
* `driver` : Driver for the database.

## 4. Starting the bot
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

An example config would be: 
```
[bot]
token = <bot_token>
prefix = !
playing = Raidquaza

[polls]
host = poll-db
user = pollman
password = bestpw
port = 3306
database = polldb
dialect = mysql
driver = mysqlconnector
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
