from utility.enums import DataSource

BOT_TOKEN = 'NDExNTQzMTExNDA0MDkzNDQx.DV9O5g.lA9ETLB9Ckivac2iLeRm64VFpHE'
PLAYING = 'RaidquazaTesting'
PREFIX = '!'

LOG_PATH = '/home/bree/repos/pokemon-discord-report-bot/raidquaza/'

POLL_ENABLED = True
POLL_DB_HOST = 'localhost'
POLL_DB_USER = 'pollman'
POLL_DB_PASSWORD = 'bestpw'
POLL_DB_PORT = 3307
POLL_DB_NAME = 'polldb'
POLL_DB_DIALECT = 'mysql'
POLL_DB_DRIVER = 'mysqlconnector'

"""
Search section.
- Here we define the settings for the Search.
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
