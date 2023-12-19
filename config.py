# config.py

import os
from dotenv import load_dotenv

#Load .env variables
load_dotenv()

RAWG_API_BASE_URL = os.getenv("RAWG_API_BASE_URL")
RAWG_API_KEY = os.getenv("RAWG_API_KEY")
GAMEFILTER_DB_PATH = os.getenv("GAMEFILTER_DB_PATH")