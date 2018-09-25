# pokemon-discord-search-bot
Bot to search a Arena/Pokestop via discord.

# Setup
## 1. Requirements: 
- python3
- pip3
- discord bot user (https://discordapp.com/developers/applications/me)

## 2. Install discord.py and numpy:
```
pip3 install discord.py
pip3 install numpy
```

## 3. Configuration:
Copy the file `config.conf.dist` to `config.conf` (or create it). 
The configuration file is of the form: 

```
token=<discord bot user token>
playing=hide and seek
gyms-csv=<.csv file>
```
where:
- `<discord bot user token>` is the token of your discord bot user.
- `<.csv file>` is a .csv file, which consists of 4 columns: Name, long, lat,Type(Arena/Pokestop)
  an example file is `data/gyms_stops.csv` which contains all pokestops and arenas of the city Freiburg.

## 4. Starting the bot
Call:
```
python3 start_bot.py
```

# Commands
- `!search <query>`will search for an Arena/Pokestop and return the top 5 results. (Arena/Pokestop + Google maps link)
- `!arena <query>`will search for an Arena return the top 5 results. (Arena + Google maps link)
- `!stop <query>`will search for an Stop return the top 5 results. (Stop + Google maps link)
