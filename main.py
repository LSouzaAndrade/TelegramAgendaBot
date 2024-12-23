from utils.gemini_client import get_chat_response
from utils.telegram_bot import *


client = get_telegram_client()

@client.on(events.NewMessage())
async def listener(event):
    if event.chat_id == int(TELEGRAM_GROUP_CHAT_ID) and event.text != '':
        response = get_chat_response(event.text)
        await event.reply(response)

client.start(bot_token=TELEGRAM_BOT_TOKEN)
client.run_until_disconnected()
