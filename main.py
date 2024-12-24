from utils.GPT_API_handler import ChatInstance
from utils.telegram_bot import *
from utils.Tool_functions import function_map, tools


model = 'gpt-4o-mini'
client = get_telegram_client()
chat = ChatInstance(model, tools=tools, function_map=function_map)

@client.on(events.NewMessage())
async def listener(event):
    if event.chat_id == int(TELEGRAM_GROUP_CHAT_ID) and event.text != '':
        response = chat.send_message(event.text)
        await event.reply(response)

client.start(bot_token=TELEGRAM_BOT_TOKEN)
client.run_until_disconnected()
