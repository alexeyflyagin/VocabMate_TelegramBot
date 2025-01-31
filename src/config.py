import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from src import loggers

ROOT_PATH = Path(__file__).parent.parent
PATH_TO_ENV = ROOT_PATH / '.env'
LOG_FOLDER_PATH = ROOT_PATH / 'logs'

# Code
os.makedirs(LOG_FOLDER_PATH, exist_ok=True)
load_dotenv(PATH_TO_ENV)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_URL = os.getenv('DB_URL')

# Configurate loggers
CONSOLE_LOG_FORMAT = "%(asctime)s [%(levelname)s] | %(name)s | (%(filename)s:%(lineno)d) - %(message)s"
INDIVIDUAL_FILE_LOG_FORMAT = "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s"

# Configurate loggers: Console
logging.getLogger('aiogram').setLevel(level=logging.WARNING)
logging.getLogger('asyncio').setLevel(level=logging.WARNING)
logging.basicConfig(
    level=logging.DEBUG,
    format=CONSOLE_LOG_FORMAT,
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Configurate loggers: File
file_handler = logging.FileHandler(LOG_FOLDER_PATH / 'bot.log')
file_handler.setFormatter(logging.Formatter(INDIVIDUAL_FILE_LOG_FORMAT))
file_handler.setLevel(logging.INFO)
loggers.bot_logger.addHandler(file_handler)

file_handler = logging.FileHandler(LOG_FOLDER_PATH / 'service.log')
file_handler.setFormatter(logging.Formatter(INDIVIDUAL_FILE_LOG_FORMAT))
file_handler.setLevel(logging.INFO)
loggers.service_logger.addHandler(file_handler)
