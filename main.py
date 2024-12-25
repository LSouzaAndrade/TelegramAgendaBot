from datetime import datetime
from utils.gpt_api_handler import ChatInstance
from utils.telegram_bot import *
from utils.tool_functions import function_map, tools


model = 'gpt-4o-mini'

client = get_telegram_client()
system_prompt = '''Você faz parte de um sistema de reservas, e pode fazer consultas e reservas de objetos.
                   Não tente inferir informações que não foram fornecidas.
                   Sempre valide as informações com o usuário antes de fazer uma Function Call com o seguinte formato de mensagem
                   "Para [função a ser executada], preciso confirmar os seguintes dados:

                    - Objeto da reserva: [objeto]
                    - Data de início: [dd] de [mês] de [aaaa], às [HH:mm]
                    - Data de término: [dd] de [mês] de [aaaa], às [HH:mm]

                    Confirma?"
                    A função de reserva já inclui a função de validação de dados, então não há necessidade de validá-los antes de chamar a função.'''
chat = ChatInstance(model, 
                    tools=tools, 
                    function_map=function_map,
                    system_prompt=system_prompt)

@client.on(events.NewMessage())
async def listener(event):
    if event.chat_id == int(TELEGRAM_GROUP_CHAT_ID) and event.text != '':
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = '[' + now + '] ' + event.text
        print(message)
        response = chat.send_message(message)
        await event.reply(response)

client.start(bot_token=TELEGRAM_BOT_TOKEN)
client.run_until_disconnected()
