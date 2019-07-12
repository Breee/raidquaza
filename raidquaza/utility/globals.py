import logging
import os

try:
    import config as config

    log_path = config.LOG_PATH

except:
    log_path = "."
# LOGGING
logging.getLogger('discord').setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.WARNING)

if not os.path.exists(log_path):
    os.makedirs(log_path)

logFormatter = logging.Formatter("[%(asctime)s] [%(module)s] [%(levelname)-5.5s]  %(message)s")
LOGGER = logging.getLogger('raidquaza')

fileHandler = logging.FileHandler("{0}/raidquaza.log".format(config.LOG_PATH))
fileHandler.setFormatter(logFormatter)
LOGGER.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
LOGGER.addHandler(consoleHandler)
LOGGER.setLevel(level=logging.INFO)
