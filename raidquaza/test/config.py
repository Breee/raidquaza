from utility.enums import DataSource

# Directory where the log file of the bot shall be stored
LOG_PATH = '.'

"""
Discord Section.
"""

# The Token of your botuser.
BOT_TOKEN = 'wrseresresresresresr'

SEARCH_DATASOURCE = DataSource.CSV
# The csv file we pull data from, example in 'data/gyms_stops.csv'. Leave this empty if you do not need it.
SEARCH_CSV_FILE = 'raidquaza/test/test_data.csv'
SEARCH_USE_GEOFENCES = False
SEARCH_USE_PORTALS = False
SEARCH_CHANNELS_TO_GEOFENCES = dict()
