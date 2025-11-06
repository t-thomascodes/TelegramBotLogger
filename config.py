import os
from dotenv import load_dotenv

load_dotenv()

#PostgresSQL Connection Settings 

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

#Telgram Bot Credentials 
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
TELEGRAM_BOT_NAME = os.getenv("TELEGRAM_BOT_NAME")


