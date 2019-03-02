import os
from logging import getLogger, DEBUG, FileHandler, Formatter, INFO

logger = getLogger("logger")

os.makedirs("store/logs", exist_ok=True)
fh = FileHandler("store/logs/events.log")
logger.addHandler(fh)

formatter = Formatter('%(asctime)s - %(module)s:%(lineno)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

if "DEBUG" in os.environ:
  logger.setLevel(DEBUG)
else:
  logger.setLevel(INFO)