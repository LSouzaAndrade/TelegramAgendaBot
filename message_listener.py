import os
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
        print('Conteúdo da mensagem: ' + event.text)
        print('ID da mensagem: ' + str(event.message.id))
        if event.message.reply_to_msg_id:
            print('ID da mensagem respondida: ' + str(event.message.reply_to_msg_id))

client.start(bot_token=TELEGRAM_BOT_TOKEN)
client.run_until_disconnected()
