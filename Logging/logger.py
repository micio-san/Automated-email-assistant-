import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", filename="./Logging/logFile.log", encoding="UTF-8")
logger.setLevel(logging.DEBUG)