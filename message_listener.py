import os
from db_handler import init_db, save_message
from dotenv import load_dotenv
from telethon import TelegramClient, events


load_dotenv()
TELEGRAM_API_ID = os.environ['TELEGRAM_API_ID']
TELEGRAM_API_HASH = os.environ['TELEGRAM_API_HASH']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_GROUP_CHAT_ID = os.environ['TELEGRAM_GROUP_CHAT_ID']
client = TelegramClient('message_listener', api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

@client.on(events.NewMessage())
async def listener(event):
    if event.chat_id == int(TELEGRAM_GROUP_CHAT_ID):
        message_id = event.message.id
        reply_to_message_id = ''
        if event.message.reply_to_msg_id:
            reply_to_message_id = event.message.reply_to_msg_id
        content = event.text
        save_message(message_id, reply_to_message_id, content)

init_db()
client.start(bot_token=TELEGRAM_BOT_TOKEN)
client.run_until_disconnected()
