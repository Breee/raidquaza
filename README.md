[![Breee](https://circleci.com/gh/Breee/raidquaza.svg?style=svg)](https://app.circleci.com/pipelines/github/Breee/raidquaza)
[![CodeFactor](https://www.codefactor.io/repository/github/breee/raidquaza/badge)](https://www.codefactor.io/repository/github/breee/raidquaza)
# Discord Poll Bot Raidquaza
- Bot to create polls via discord.

![raidquaza_example](https://s18.directupload.net/images/190713/g6ob9ptw.jpg)

Try it out and add it to your discord:
https://discordapp.com/api/oauth2/authorize?client_id=410240526701559829&permissions=280640&scope=bot 

Questions? I'm Bree#2002 @ Discord


Docker image:  https://cloud.docker.com/repository/docker/breedocker/raidquaza

Discord server: https://discord.gg/Mamfk3Q

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
import os

# Directory where the log file of the bot shall be stored
LOG_PATH = os.getenv("BOT_LOG_PATH", "./log")

"""
Discord Section.
"""
# The Token of your botuser.
BOT_TOKEN = os.getenv("BOT_TOKEN", "xxxxx")
# Discord Status
PLAYING = os.getenv("TAG", "BLA")
# Command prefix
PREFIX = os.getenv("BOT_PREFIX", "!")

"""
Poll Section.
"""
# The host of the DB in which we store polls
POLL_DB_HOST = os.getenv("POLL_DB_HOST", "localhost")
# The user of the DB
POLL_DB_USER = os.getenv("POLL_DB_USER", "pollman")
# The password of user POLL_DB_USER
POLL_DB_PASSWORD = os.getenv("POLL_DB_PASSWORD", "bestpw")
# The port of the DB-server
POLL_DB_PORT = os.getenv("POLL_DB_PORT", 3306)
# The name of the DB in which we store polls
POLL_DB_NAME = os.getenv("POLL_DB_NAME", "polldb")
# The dialect of the database-server
POLL_DB_DIALECT =  os.getenv("POLL_DB_DIALECT", "mysql")
# The driver of the database-server
POLL_DB_DRIVER =  os.getenv("POLL_DB_DRIVER", "mysqlconnector")
```

## 3. Deploy:
### Configure
Fill in everything necessary in `config.py` or set ENV variables accordingly.

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
    image: breedocker/raidquaza
    entrypoint: ["/entrypoint.sh"]
    environment:
      - "BOT_TOKEN=xxxx"
      - "BOT_PREFIX=!"
      - "POLL_DB_HOST=poll-db"
      - "POLL_DB_PORT=3306"
      - "POLL_DB_NAME=polldb"
      - "POLL_DB_USER=pollman"
      - "POLL_DB_PASSWORD=bestpw"
      - "POLL_DB_DIALECT=mysql"
      - "POLL_DB_DRIVER=mysqlconnector"
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
      - "MYSQL_ROOT_PASSWORD: root1234"
      - "MYSQL_DATABASE: polldb"
      - "MYSQL_USER: pollman"
      - "MYSQL_PASSWORD: bestpw"
    command: ['mysqld', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_unicode_ci']
    volumes:
      - ./volumes/mysql/db:/var/lib/mysql
    restart: always
    networks:
      - default
``` 

To bring the services up, simply `docker-compose up -d poll-db`, `docker-compose up -d raidquaza`.

# Commands
Commands consist of a `prefix` and an `alias`.

You can specify a `prefix` in `raidquaza/config/config.ini`, the default prefixes are `!` and `@bot_user_name#1337`.

Utils:
- `!help` display help
- `!ping` ping the bot
- `!uptime` return how long the bot is operational.

Poll:
- `!poll <title> <option_1> .. <option_17>` to create a new poll with number reactions.
- `!simplepoll <title> <option_1> .. <option_21>`  to create a new poll without number reactions
Polls may have at most 17 vote options, as discord supports a maximum of 21 reactions the bot adds 4 extra reactions.
Simple Polls have at most 21 reactions
