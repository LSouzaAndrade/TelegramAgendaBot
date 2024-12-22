import os
from dotenv import load_dotenv
from telethon import TelegramClient, events


load_dotenv()
TELEGRAM_API_ID = os.environ['TELEGRAM_API_ID']
TELEGRAM_API_HASH = os.environ['TELEGRAM_API_HASH']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_GROUP_CHAT_ID = os.environ['TELEGRAM_GROUP_CHAT_ID']

def get_telegram_client():
    client = TelegramClient('message_listener', api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)
    return client
